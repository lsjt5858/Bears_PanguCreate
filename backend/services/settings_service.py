"""
系统设置服务
管理系统配置
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from typing import Any, Dict, List, Optional, Tuple
from models.system_setting import SystemSetting
from extensions import db


class SettingsService:
    """系统设置服务类"""
    
    # 设置分类
    CATEGORIES = {
        'general': '通用设置',
        'security': '安全设置',
        'notification': '通知设置',
        'generation': '数据生成设置',
        'export': '导出设置',
        'api': 'API 设置'
    }
    
    # 默认设置
    DEFAULT_SETTINGS = {
        # 通用设置
        'site_name': {
            'value': 'Bears PanguCreate',
            'value_type': 'string',
            'category': 'general',
            'description': '站点名称',
            'is_public': True
        },
        'site_description': {
            'value': '企业级测试数据生成平台',
            'value_type': 'string',
            'category': 'general',
            'description': '站点描述',
            'is_public': True
        },
        'default_language': {
            'value': 'zh-CN',
            'value_type': 'string',
            'category': 'general',
            'description': '默认语言',
            'is_public': True
        },
        'maintenance_mode': {
            'value': False,
            'value_type': 'boolean',
            'category': 'general',
            'description': '维护模式',
            'is_public': True
        },
        
        # 安全设置
        'max_login_attempts': {
            'value': 5,
            'value_type': 'integer',
            'category': 'security',
            'description': '最大登录尝试次数',
            'is_public': False
        },
        'session_timeout': {
            'value': 3600,
            'value_type': 'integer',
            'category': 'security',
            'description': '会话超时时间（秒）',
            'is_public': False
        },
        'password_min_length': {
            'value': 8,
            'value_type': 'integer',
            'category': 'security',
            'description': '密码最小长度',
            'is_public': True
        },
        
        # 数据生成设置
        'max_generate_count': {
            'value': 10000,
            'value_type': 'integer',
            'category': 'generation',
            'description': '单次最大生成数量',
            'is_public': True
        },
        'default_generate_count': {
            'value': 100,
            'value_type': 'integer',
            'category': 'generation',
            'description': '默认生成数量',
            'is_public': True
        },
        
        # 导出设置
        'max_export_count': {
            'value': 50000,
            'value_type': 'integer',
            'category': 'export',
            'description': '单次最大导出数量',
            'is_public': True
        },
        'export_formats': {
            'value': ['json', 'csv', 'sql', 'xml'],
            'value_type': 'json',
            'category': 'export',
            'description': '支持的导出格式',
            'is_public': True
        },
        
        # API 设置
        'api_rate_limit': {
            'value': 100,
            'value_type': 'integer',
            'category': 'api',
            'description': 'API 速率限制（每分钟）',
            'is_public': False
        },
        'api_key_max_count': {
            'value': 10,
            'value_type': 'integer',
            'category': 'api',
            'description': '每用户最大 API 密钥数',
            'is_public': True
        },
        
        # 通知设置
        'email_notifications': {
            'value': True,
            'value_type': 'boolean',
            'category': 'notification',
            'description': '启用邮件通知',
            'is_public': False
        },
        'webhook_timeout': {
            'value': 10,
            'value_type': 'integer',
            'category': 'notification',
            'description': 'Webhook 超时时间（秒）',
            'is_public': False
        }
    }
    
    def get_categories(self) -> dict:
        """获取设置分类"""
        return self.CATEGORIES
    
    def init_default_settings(self):
        """初始化默认设置"""
        for key, config in self.DEFAULT_SETTINGS.items():
            existing = SystemSetting.get_by_key(key)
            if not existing:
                SystemSetting.set_setting(key, **config)
    
    def get_setting(self, key: str, default: Any = None) -> Any:
        """获取单个设置值"""
        setting = SystemSetting.get_by_key(key)
        if setting:
            return setting.get_value()
        
        # 返回默认值
        if key in self.DEFAULT_SETTINGS:
            return self.DEFAULT_SETTINGS[key]['value']
        return default
    
    def get_setting_detail(self, key: str) -> Optional[dict]:
        """获取设置详情"""
        setting = SystemSetting.get_by_key(key)
        if setting:
            return setting.to_dict()
        return None
    
    def set_setting(self, key: str, value: Any, **kwargs) -> Tuple[Optional[SystemSetting], Optional[str]]:
        """设置配置值"""
        # 获取默认配置
        default_config = self.DEFAULT_SETTINGS.get(key, {})
        
        value_type = kwargs.get('value_type', default_config.get('value_type', 'string'))
        category = kwargs.get('category', default_config.get('category', 'general'))
        description = kwargs.get('description', default_config.get('description'))
        is_public = kwargs.get('is_public', default_config.get('is_public', False))
        
        try:
            setting = SystemSetting.set_setting(
                key=key,
                value=value,
                value_type=value_type,
                category=category,
                description=description,
                is_public=is_public
            )
            return setting, None
        except Exception as e:
            return None, str(e)
    
    def get_settings_by_category(self, category: str, public_only: bool = False) -> List[dict]:
        """获取分类下的所有设置"""
        settings = SystemSetting.get_by_category(category, public_only)
        result = [s.to_dict() for s in settings]
        
        # 补充默认设置中存在但数据库中不存在的
        existing_keys = {s['key'] for s in result}
        for key, config in self.DEFAULT_SETTINGS.items():
            if config['category'] == category and key not in existing_keys:
                if not public_only or config.get('is_public', False):
                    result.append({
                        'key': key,
                        'value': config['value'],
                        'value_type': config['value_type'],
                        'category': config['category'],
                        'description': config.get('description'),
                        'is_public': config.get('is_public', False),
                        'is_default': True
                    })
        
        return result
    
    def get_all_settings(self, public_only: bool = False) -> Dict[str, List[dict]]:
        """获取所有设置，按分类分组"""
        result = {}
        for category in self.CATEGORIES.keys():
            settings = self.get_settings_by_category(category, public_only)
            if settings:
                result[category] = settings
        return result
    
    def get_public_settings(self) -> Dict[str, Any]:
        """获取所有公开设置（简化格式）"""
        settings = SystemSetting.get_all_public()
        result = {s.key: s.get_value() for s in settings}
        
        # 补充默认公开设置
        for key, config in self.DEFAULT_SETTINGS.items():
            if config.get('is_public', False) and key not in result:
                result[key] = config['value']
        
        return result
    
    def update_settings(self, settings: Dict[str, Any]) -> Tuple[int, List[dict]]:
        """批量更新设置"""
        updated = 0
        errors = []
        
        for key, value in settings.items():
            setting, error = self.set_setting(key, value)
            if error:
                errors.append({'key': key, 'error': error})
            else:
                updated += 1
        
        return updated, errors
    
    def delete_setting(self, key: str) -> Tuple[bool, str]:
        """删除设置"""
        setting = SystemSetting.get_by_key(key)
        if not setting:
            return False, '设置不存在'
        
        setting.delete()
        return True, '设置已删除'
    
    def reset_to_default(self, key: str) -> Tuple[bool, str]:
        """重置为默认值"""
        if key not in self.DEFAULT_SETTINGS:
            return False, '没有默认值'
        
        config = self.DEFAULT_SETTINGS[key]
        setting, error = self.set_setting(key, config['value'], **config)
        
        if error:
            return False, error
        return True, '已重置为默认值'
    
    def reset_category_to_default(self, category: str) -> int:
        """重置分类下所有设置为默认值"""
        count = 0
        for key, config in self.DEFAULT_SETTINGS.items():
            if config['category'] == category:
                success, _ = self.reset_to_default(key)
                if success:
                    count += 1
        return count


# 单例
settings_service = SettingsService()
