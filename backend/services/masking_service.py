"""
数据脱敏服务
提供多种数据脱敏策略
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import re
import hashlib
from typing import Any, Dict, List, Optional


class MaskingService:
    """数据脱敏服务类"""
    
    # 脱敏策略
    STRATEGIES = {
        'mask': '掩码替换',
        'hash': '哈希处理',
        'truncate': '截断处理',
        'replace': '固定值替换',
        'shuffle': '随机打乱',
        'null': '置空处理',
        'partial': '部分保留'
    }
    
    # 预定义的脱敏规则
    PRESET_RULES = {
        'phone': {
            'strategy': 'partial',
            'pattern': r'^(\d{3})\d{4}(\d{4})$',
            'replacement': r'\1****\2',
            'description': '手机号脱敏 (保留前3后4)'
        },
        'email': {
            'strategy': 'partial',
            'pattern': r'^(.{2}).*(@.*)$',
            'replacement': r'\1***\2',
            'description': '邮箱脱敏 (保留前2位和域名)'
        },
        'id_card': {
            'strategy': 'partial',
            'pattern': r'^(.{6}).*(.{4})$',
            'replacement': r'\1********\2',
            'description': '身份证脱敏 (保留前6后4)'
        },
        'bank_card': {
            'strategy': 'partial',
            'pattern': r'^(.{4}).*(.{4})$',
            'replacement': r'\1********\2',
            'description': '银行卡脱敏 (保留前4后4)'
        },
        'name': {
            'strategy': 'partial',
            'pattern': r'^(.).*$',
            'replacement': r'\1**',
            'description': '姓名脱敏 (保留首字)'
        },
        'address': {
            'strategy': 'truncate',
            'length': 10,
            'suffix': '***',
            'description': '地址脱敏 (截断)'
        },
        'password': {
            'strategy': 'replace',
            'value': '******',
            'description': '密码脱敏 (固定替换)'
        },
        'ip': {
            'strategy': 'partial',
            'pattern': r'^(\d+\.\d+)\.\d+\.\d+$',
            'replacement': r'\1.*.*',
            'description': 'IP地址脱敏 (保留前两段)'
        }
    }
    
    def get_strategies(self) -> dict:
        """获取支持的脱敏策略"""
        return self.STRATEGIES
    
    def get_preset_rules(self) -> dict:
        """获取预定义的脱敏规则"""
        return self.PRESET_RULES
    
    def mask_value(self, value: Any, strategy: str, **options) -> Any:
        """对单个值进行脱敏"""
        if value is None:
            return None
        
        value_str = str(value)
        
        if strategy == 'mask':
            return self._mask_strategy(value_str, **options)
        elif strategy == 'hash':
            return self._hash_strategy(value_str, **options)
        elif strategy == 'truncate':
            return self._truncate_strategy(value_str, **options)
        elif strategy == 'replace':
            return self._replace_strategy(value_str, **options)
        elif strategy == 'shuffle':
            return self._shuffle_strategy(value_str, **options)
        elif strategy == 'null':
            return self._null_strategy(**options)
        elif strategy == 'partial':
            return self._partial_strategy(value_str, **options)
        else:
            return value
    
    def _mask_strategy(self, value: str, mask_char: str = '*', 
                       start: int = 0, end: int = None, **kwargs) -> str:
        """掩码替换策略"""
        if end is None:
            end = len(value)
        
        masked = list(value)
        for i in range(start, min(end, len(value))):
            masked[i] = mask_char
        return ''.join(masked)
    
    def _hash_strategy(self, value: str, algorithm: str = 'md5', 
                       length: int = 8, **kwargs) -> str:
        """哈希处理策略"""
        if algorithm == 'md5':
            hashed = hashlib.md5(value.encode()).hexdigest()
        elif algorithm == 'sha256':
            hashed = hashlib.sha256(value.encode()).hexdigest()
        else:
            hashed = hashlib.md5(value.encode()).hexdigest()
        
        return hashed[:length] if length else hashed
    
    def _truncate_strategy(self, value: str, length: int = 5, 
                           suffix: str = '...', **kwargs) -> str:
        """截断处理策略"""
        if len(value) <= length:
            return value
        return value[:length] + suffix
    
    def _replace_strategy(self, value: str, replacement: str = '***', **kwargs) -> str:
        """固定值替换策略"""
        return replacement
    
    def _shuffle_strategy(self, value: str, **kwargs) -> str:
        """随机打乱策略"""
        import random
        chars = list(value)
        random.shuffle(chars)
        return ''.join(chars)
    
    def _null_strategy(self, null_value: Any = None, **kwargs) -> Any:
        """置空处理策略"""
        return null_value
    
    def _partial_strategy(self, value: str, pattern: str = None, 
                          replacement: str = None, **kwargs) -> str:
        """部分保留策略"""
        if pattern and replacement:
            try:
                return re.sub(pattern, replacement, value)
            except:
                return value
        return value
    
    def apply_preset_rule(self, value: Any, rule_name: str) -> Any:
        """应用预定义规则"""
        if rule_name not in self.PRESET_RULES:
            return value
        
        rule = self.PRESET_RULES[rule_name]
        return self.mask_value(value, rule['strategy'], **rule)
    
    def mask_record(self, record: dict, rules: Dict[str, dict]) -> dict:
        """对单条记录进行脱敏
        
        Args:
            record: 原始记录
            rules: 字段脱敏规则，格式: {field_name: {strategy: ..., ...}}
        
        Returns:
            脱敏后的记录
        """
        masked_record = record.copy()
        
        for field, rule in rules.items():
            if field in masked_record:
                if 'preset' in rule:
                    masked_record[field] = self.apply_preset_rule(
                        masked_record[field], 
                        rule['preset']
                    )
                else:
                    strategy = rule.get('strategy', 'mask')
                    masked_record[field] = self.mask_value(
                        masked_record[field],
                        strategy,
                        **rule
                    )
        
        return masked_record
    
    def mask_records(self, records: List[dict], rules: Dict[str, dict]) -> List[dict]:
        """对多条记录进行脱敏"""
        return [self.mask_record(record, rules) for record in records]
    
    def auto_detect_and_mask(self, value: str) -> tuple:
        """自动检测数据类型并脱敏
        
        Returns:
            (脱敏后的值, 检测到的类型)
        """
        # 手机号检测
        if re.match(r'^1[3-9]\d{9}$', value):
            return self.apply_preset_rule(value, 'phone'), 'phone'
        
        # 邮箱检测
        if re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', value):
            return self.apply_preset_rule(value, 'email'), 'email'
        
        # 身份证检测
        if re.match(r'^\d{17}[\dXx]$', value):
            return self.apply_preset_rule(value, 'id_card'), 'id_card'
        
        # 银行卡检测
        if re.match(r'^\d{16,19}$', value):
            return self.apply_preset_rule(value, 'bank_card'), 'bank_card'
        
        # IP地址检测
        if re.match(r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$', value):
            return self.apply_preset_rule(value, 'ip'), 'ip'
        
        return value, None


# 单例
masking_service = MaskingService()
