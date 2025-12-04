"""
数据类型服务
管理所有支持的数据类型
"""
from typing import List, Dict, Any, Optional


class DataTypeService:
    """数据类型服务"""
    
    # 所有支持的数据类型
    DATA_TYPES = [
        {"id": "uuid", "name": "UUID", "icon": "🔑", "category": "identifier"},
        {"id": "number", "name": "数字", "icon": "🔢", "category": "identifier"},
        {"id": "string", "name": "随机字符串", "icon": "📝", "category": "identifier"},
        {"id": "boolean", "name": "布尔值", "icon": "✓", "category": "identifier"},
        {"id": "chineseName", "name": "中文姓名", "icon": "👤", "category": "personal"},
        {"id": "englishName", "name": "英文姓名", "icon": "👤", "category": "personal"},
        {"id": "email", "name": "邮箱", "icon": "📧", "category": "personal"},
        {"id": "chinesePhone", "name": "中国手机号", "icon": "📱", "category": "personal"},
        {"id": "phone", "name": "国际手机号", "icon": "📞", "category": "personal"},
        {"id": "chineseIdCard", "name": "身份证号", "icon": "🪪", "category": "personal"},
        {"id": "age", "name": "年龄", "icon": "🎂", "category": "personal"},
        {"id": "gender", "name": "性别", "icon": "⚧", "category": "personal"},
        {"id": "chineseAddress", "name": "中国地址", "icon": "📍", "category": "address"},
        {"id": "province", "name": "省份", "icon": "🗺️", "category": "address"},
        {"id": "city", "name": "城市", "icon": "🏙️", "category": "address"},
        {"id": "zipcode", "name": "邮编", "icon": "📮", "category": "address"},
        {"id": "date", "name": "日期", "icon": "📅", "category": "datetime"},
        {"id": "datetime", "name": "日期时间", "icon": "🕐", "category": "datetime"},
        {"id": "timestamp", "name": "时间戳", "icon": "⏱️", "category": "datetime"},
        {"id": "bankCard", "name": "银行卡号", "icon": "💳", "category": "finance"},
        {"id": "amount", "name": "金额", "icon": "💰", "category": "finance"},
        {"id": "url", "name": "URL", "icon": "🔗", "category": "internet"},
        {"id": "ip", "name": "IPv4", "icon": "🌐", "category": "internet"},
        {"id": "ipv6", "name": "IPv6", "icon": "🌐", "category": "internet"},
        {"id": "mac", "name": "MAC地址", "icon": "📶", "category": "internet"},
        {"id": "domain", "name": "域名", "icon": "🌍", "category": "internet"},
        {"id": "company", "name": "公司名称", "icon": "🏢", "category": "company"},
        {"id": "jobTitle", "name": "职位", "icon": "💼", "category": "company"},
        {"id": "paragraph", "name": "段落", "icon": "📄", "category": "text"},
        {"id": "sentence", "name": "句子", "icon": "💬", "category": "text"},
        {"id": "word", "name": "词语", "icon": "📝", "category": "text"},
    ]

    def get_all_types(self) -> List[Dict[str, Any]]:
        """获取所有数据类型"""
        return self.DATA_TYPES

    def get_types_by_category(self, category: str) -> List[Dict[str, Any]]:
        """按分类获取数据类型"""
        return [t for t in self.DATA_TYPES if t["category"] == category]

    def get_type_by_id(self, type_id: str) -> Optional[Dict[str, Any]]:
        """根据ID获取数据类型"""
        return next((t for t in self.DATA_TYPES if t["id"] == type_id), None)

    def get_categories(self) -> List[str]:
        """获取所有分类"""
        return list(set(t["category"] for t in self.DATA_TYPES))


# 单例实例
data_type_service = DataTypeService()
