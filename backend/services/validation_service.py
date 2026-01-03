"""
数据验证服务
提供多种数据验证规则
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import re
from typing import Any, Dict, List, Optional, Tuple
from datetime import datetime


class ValidationService:
    """数据验证服务类"""
    
    # 验证规则类型
    RULE_TYPES = {
        'required': '必填验证',
        'type': '类型验证',
        'length': '长度验证',
        'range': '范围验证',
        'pattern': '正则验证',
        'enum': '枚举验证',
        'unique': '唯一性验证',
        'custom': '自定义验证'
    }
    
    # 预定义的验证规则
    PRESET_RULES = {
        'email': {
            'pattern': r'^[\w\.-]+@[\w\.-]+\.\w+$',
            'message': '邮箱格式不正确'
        },
        'phone': {
            'pattern': r'^1[3-9]\d{9}$',
            'message': '手机号格式不正确'
        },
        'id_card': {
            'pattern': r'^\d{17}[\dXx]$',
            'message': '身份证号格式不正确'
        },
        'url': {
            'pattern': r'^https?://[\w\.-]+',
            'message': 'URL格式不正确'
        },
        'ip': {
            'pattern': r'^(\d{1,3}\.){3}\d{1,3}$',
            'message': 'IP地址格式不正确'
        },
        'date': {
            'pattern': r'^\d{4}-\d{2}-\d{2}$',
            'message': '日期格式不正确 (YYYY-MM-DD)'
        },
        'datetime': {
            'pattern': r'^\d{4}-\d{2}-\d{2}[T ]\d{2}:\d{2}:\d{2}',
            'message': '日期时间格式不正确'
        },
        'chinese': {
            'pattern': r'^[\u4e00-\u9fa5]+$',
            'message': '必须为中文字符'
        },
        'alphanumeric': {
            'pattern': r'^[a-zA-Z0-9]+$',
            'message': '只能包含字母和数字'
        },
        'username': {
            'pattern': r'^[a-zA-Z][a-zA-Z0-9_]{2,19}$',
            'message': '用户名必须以字母开头，3-20位字母数字下划线'
        },
        'password': {
            'pattern': r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).{8,}$',
            'message': '密码至少8位，包含大小写字母和数字'
        },
        'positive_integer': {
            'pattern': r'^[1-9]\d*$',
            'message': '必须为正整数'
        },
        'decimal': {
            'pattern': r'^-?\d+(\.\d+)?$',
            'message': '必须为数字'
        }
    }
    
    def get_rule_types(self) -> dict:
        """获取支持的验证规则类型"""
        return self.RULE_TYPES
    
    def get_preset_rules(self) -> dict:
        """获取预定义的验证规则"""
        return self.PRESET_RULES
    
    def validate_required(self, value: Any, **kwargs) -> Tuple[bool, Optional[str]]:
        """必填验证"""
        if value is None or value == '' or (isinstance(value, (list, dict)) and len(value) == 0):
            return False, kwargs.get('message', '此字段为必填项')
        return True, None
    
    def validate_type(self, value: Any, expected_type: str, **kwargs) -> Tuple[bool, Optional[str]]:
        """类型验证"""
        type_map = {
            'string': str,
            'integer': int,
            'float': (int, float),
            'boolean': bool,
            'list': list,
            'dict': dict
        }
        
        if expected_type not in type_map:
            return True, None
        
        expected = type_map[expected_type]
        if not isinstance(value, expected):
            return False, kwargs.get('message', f'类型必须为 {expected_type}')
        return True, None
    
    def validate_length(self, value: Any, min_len: int = None, max_len: int = None, 
                        exact_len: int = None, **kwargs) -> Tuple[bool, Optional[str]]:
        """长度验证"""
        if value is None:
            return True, None
        
        length = len(str(value)) if not isinstance(value, (list, dict)) else len(value)
        
        if exact_len is not None and length != exact_len:
            return False, kwargs.get('message', f'长度必须为 {exact_len}')
        
        if min_len is not None and length < min_len:
            return False, kwargs.get('message', f'长度不能小于 {min_len}')
        
        if max_len is not None and length > max_len:
            return False, kwargs.get('message', f'长度不能大于 {max_len}')
        
        return True, None
    
    def validate_range(self, value: Any, min_val: Any = None, max_val: Any = None, 
                       **kwargs) -> Tuple[bool, Optional[str]]:
        """范围验证"""
        if value is None:
            return True, None
        
        try:
            num_value = float(value)
            
            if min_val is not None and num_value < min_val:
                return False, kwargs.get('message', f'值不能小于 {min_val}')
            
            if max_val is not None and num_value > max_val:
                return False, kwargs.get('message', f'值不能大于 {max_val}')
            
            return True, None
        except (ValueError, TypeError):
            return False, kwargs.get('message', '值必须为数字')
    
    def validate_pattern(self, value: Any, pattern: str, **kwargs) -> Tuple[bool, Optional[str]]:
        """正则验证"""
        if value is None or value == '':
            return True, None
        
        try:
            if not re.match(pattern, str(value)):
                return False, kwargs.get('message', '格式不正确')
            return True, None
        except re.error:
            return False, '正则表达式无效'
    
    def validate_enum(self, value: Any, allowed_values: list, **kwargs) -> Tuple[bool, Optional[str]]:
        """枚举验证"""
        if value is None:
            return True, None
        
        if value not in allowed_values:
            return False, kwargs.get('message', f'值必须是以下之一: {", ".join(map(str, allowed_values))}')
        return True, None
    
    def validate_unique(self, value: Any, existing_values: list, **kwargs) -> Tuple[bool, Optional[str]]:
        """唯一性验证"""
        if value is None:
            return True, None
        
        if value in existing_values:
            return False, kwargs.get('message', '值已存在，必须唯一')
        return True, None
    
    def validate_preset(self, value: Any, preset_name: str, **kwargs) -> Tuple[bool, Optional[str]]:
        """使用预定义规则验证"""
        if preset_name not in self.PRESET_RULES:
            return True, None
        
        preset = self.PRESET_RULES[preset_name]
        return self.validate_pattern(value, preset['pattern'], message=preset['message'])
    
    def validate_field(self, value: Any, rules: List[dict]) -> List[str]:
        """验证单个字段
        
        Args:
            value: 字段值
            rules: 验证规则列表
        
        Returns:
            错误消息列表
        """
        errors = []
        
        for rule in rules:
            rule_type = rule.get('type')
            
            if rule_type == 'required':
                valid, error = self.validate_required(value, **rule)
            elif rule_type == 'type':
                valid, error = self.validate_type(value, rule.get('expected_type'), **rule)
            elif rule_type == 'length':
                valid, error = self.validate_length(value, **rule)
            elif rule_type == 'range':
                valid, error = self.validate_range(value, **rule)
            elif rule_type == 'pattern':
                valid, error = self.validate_pattern(value, rule.get('pattern', ''), **rule)
            elif rule_type == 'enum':
                valid, error = self.validate_enum(value, rule.get('allowed_values', []), **rule)
            elif rule_type == 'unique':
                valid, error = self.validate_unique(value, rule.get('existing_values', []), **rule)
            elif rule_type == 'preset':
                valid, error = self.validate_preset(value, rule.get('preset_name', ''), **rule)
            else:
                continue
            
            if not valid and error:
                errors.append(error)
        
        return errors
    
    def validate_record(self, record: dict, field_rules: Dict[str, List[dict]]) -> Dict[str, List[str]]:
        """验证单条记录
        
        Args:
            record: 数据记录
            field_rules: 字段验证规则，格式: {field_name: [rules]}
        
        Returns:
            字段错误映射，格式: {field_name: [errors]}
        """
        errors = {}
        
        for field, rules in field_rules.items():
            value = record.get(field)
            field_errors = self.validate_field(value, rules)
            if field_errors:
                errors[field] = field_errors
        
        return errors
    
    def validate_records(self, records: List[dict], field_rules: Dict[str, List[dict]], 
                         check_unique: bool = False) -> List[dict]:
        """验证多条记录
        
        Args:
            records: 数据记录列表
            field_rules: 字段验证规则
            check_unique: 是否检查记录间的唯一性
        
        Returns:
            验证结果列表
        """
        results = []
        seen_values = {}  # 用于唯一性检查
        
        for i, record in enumerate(records):
            # 如果需要检查唯一性，更新 existing_values
            if check_unique:
                for field, rules in field_rules.items():
                    for rule in rules:
                        if rule.get('type') == 'unique':
                            if field not in seen_values:
                                seen_values[field] = []
                            rule['existing_values'] = seen_values[field]
            
            errors = self.validate_record(record, field_rules)
            
            # 记录已见值
            if check_unique:
                for field in field_rules.keys():
                    if field in record and record[field] is not None:
                        if field not in seen_values:
                            seen_values[field] = []
                        seen_values[field].append(record[field])
            
            results.append({
                'index': i,
                'valid': len(errors) == 0,
                'errors': errors
            })
        
        return results
    
    def get_validation_summary(self, validation_results: List[dict]) -> dict:
        """获取验证结果摘要"""
        total = len(validation_results)
        valid_count = sum(1 for r in validation_results if r['valid'])
        invalid_count = total - valid_count
        
        # 统计各字段的错误数
        field_error_counts = {}
        for result in validation_results:
            for field, errors in result.get('errors', {}).items():
                if field not in field_error_counts:
                    field_error_counts[field] = 0
                field_error_counts[field] += len(errors)
        
        return {
            'total': total,
            'valid_count': valid_count,
            'invalid_count': invalid_count,
            'valid_rate': round(valid_count / total * 100, 2) if total > 0 else 0,
            'field_error_counts': field_error_counts
        }


# 单例
validation_service = ValidationService()
