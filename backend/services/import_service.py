"""
批量导入服务
支持从 JSON、CSV、Excel 导入配置和数据
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import json
import csv
import io
from typing import Any, Dict, List, Optional, Tuple
from datetime import datetime


class ImportService:
    """批量导入服务类"""
    
    # 支持的导入格式
    SUPPORTED_FORMATS = {
        'json': 'JSON 格式',
        'csv': 'CSV 格式',
        'jsonl': 'JSON Lines 格式'
    }
    
    # 支持的导入类型
    IMPORT_TYPES = {
        'template': '模板配置',
        'fields': '字段配置',
        'datasource': '数据源配置',
        'data': '原始数据'
    }
    
    def get_supported_formats(self) -> dict:
        """获取支持的导入格式"""
        return self.SUPPORTED_FORMATS
    
    def get_import_types(self) -> dict:
        """获取支持的导入类型"""
        return self.IMPORT_TYPES
    
    def parse_json(self, content: str) -> Tuple[Optional[List[dict]], Optional[str]]:
        """解析 JSON 内容"""
        try:
            data = json.loads(content)
            if isinstance(data, dict):
                data = [data]
            elif not isinstance(data, list):
                return None, '数据格式错误，需要数组或对象'
            return data, None
        except json.JSONDecodeError as e:
            return None, f'JSON 解析错误: {str(e)}'
    
    def parse_jsonl(self, content: str) -> Tuple[Optional[List[dict]], Optional[str]]:
        """解析 JSON Lines 内容"""
        try:
            data = []
            for line_num, line in enumerate(content.strip().split('\n'), 1):
                line = line.strip()
                if line:
                    try:
                        data.append(json.loads(line))
                    except json.JSONDecodeError as e:
                        return None, f'第 {line_num} 行 JSON 解析错误: {str(e)}'
            return data, None
        except Exception as e:
            return None, f'解析错误: {str(e)}'
    
    def parse_csv(self, content: str, delimiter: str = ',', 
                  has_header: bool = True) -> Tuple[Optional[List[dict]], Optional[str]]:
        """解析 CSV 内容"""
        try:
            reader = csv.reader(io.StringIO(content), delimiter=delimiter)
            rows = list(reader)
            
            if not rows:
                return None, 'CSV 文件为空'
            
            if has_header:
                headers = rows[0]
                data = []
                for row in rows[1:]:
                    if len(row) == len(headers):
                        data.append(dict(zip(headers, row)))
                    elif len(row) > 0:
                        # 补齐或截断
                        row_data = {}
                        for i, header in enumerate(headers):
                            row_data[header] = row[i] if i < len(row) else ''
                        data.append(row_data)
            else:
                # 无表头，使用列索引作为键
                data = []
                for row in rows:
                    data.append({f'col_{i}': val for i, val in enumerate(row)})
            
            return data, None
        except Exception as e:
            return None, f'CSV 解析错误: {str(e)}'
    
    def parse_content(self, content: str, format: str, **options) -> Tuple[Optional[List[dict]], Optional[str]]:
        """根据格式解析内容"""
        if format == 'json':
            return self.parse_json(content)
        elif format == 'jsonl':
            return self.parse_jsonl(content)
        elif format == 'csv':
            return self.parse_csv(
                content, 
                delimiter=options.get('delimiter', ','),
                has_header=options.get('has_header', True)
            )
        else:
            return None, f'不支持的格式: {format}'
    
    def validate_template_config(self, data: List[dict]) -> Tuple[List[dict], List[dict]]:
        """验证模板配置"""
        valid = []
        errors = []
        
        for i, item in enumerate(data):
            item_errors = []
            
            if not item.get('name'):
                item_errors.append('缺少模板名称')
            
            if not item.get('fields') or not isinstance(item.get('fields'), list):
                item_errors.append('缺少字段配置或格式错误')
            else:
                for j, field in enumerate(item['fields']):
                    if not field.get('name'):
                        item_errors.append(f'字段 {j+1} 缺少名称')
                    if not field.get('type'):
                        item_errors.append(f'字段 {j+1} 缺少类型')
            
            if item_errors:
                errors.append({'index': i, 'data': item, 'errors': item_errors})
            else:
                valid.append(item)
        
        return valid, errors
    
    def validate_fields_config(self, data: List[dict]) -> Tuple[List[dict], List[dict]]:
        """验证字段配置"""
        valid = []
        errors = []
        
        for i, item in enumerate(data):
            item_errors = []
            
            if not item.get('name'):
                item_errors.append('缺少字段名称')
            if not item.get('type'):
                item_errors.append('缺少字段类型')
            
            if item_errors:
                errors.append({'index': i, 'data': item, 'errors': item_errors})
            else:
                valid.append(item)
        
        return valid, errors
    
    def validate_datasource_config(self, data: List[dict]) -> Tuple[List[dict], List[dict]]:
        """验证数据源配置"""
        valid = []
        errors = []
        
        required_fields = ['name', 'type', 'host', 'port']
        valid_types = ['mysql', 'postgresql', 'mongodb']
        
        for i, item in enumerate(data):
            item_errors = []
            
            for field in required_fields:
                if not item.get(field):
                    item_errors.append(f'缺少必填字段: {field}')
            
            if item.get('type') and item['type'] not in valid_types:
                item_errors.append(f'不支持的数据源类型: {item["type"]}')
            
            if item_errors:
                errors.append({'index': i, 'data': item, 'errors': item_errors})
            else:
                valid.append(item)
        
        return valid, errors
    
    def validate_import_data(self, data: List[dict], import_type: str) -> Tuple[List[dict], List[dict]]:
        """验证导入数据"""
        if import_type == 'template':
            return self.validate_template_config(data)
        elif import_type == 'fields':
            return self.validate_fields_config(data)
        elif import_type == 'datasource':
            return self.validate_datasource_config(data)
        elif import_type == 'data':
            # 原始数据不做特殊验证
            return data, []
        else:
            return [], [{'error': f'不支持的导入类型: {import_type}'}]
    
    def import_templates(self, user_id: int, templates: List[dict]) -> Tuple[int, List[dict]]:
        """导入模板配置"""
        from models.template import Template
        from extensions import db
        
        imported = 0
        errors = []
        
        for i, tpl in enumerate(templates):
            try:
                template = Template(
                    user_id=user_id,
                    name=tpl['name'],
                    description=tpl.get('description', ''),
                    category=tpl.get('category', 'other'),
                    fields=tpl['fields'],
                    is_public=tpl.get('is_public', False)
                )
                template.save()
                imported += 1
            except Exception as e:
                errors.append({'index': i, 'name': tpl.get('name'), 'error': str(e)})
        
        return imported, errors
    
    def import_datasources(self, user_id: int, datasources: List[dict]) -> Tuple[int, List[dict]]:
        """导入数据源配置"""
        from services.datasource_service import datasource_service
        
        imported = 0
        errors = []
        
        for i, ds in enumerate(datasources):
            try:
                datasource, error = datasource_service.create_datasource(
                    user_id=user_id,
                    name=ds['name'],
                    ds_type=ds['type'],
                    host=ds['host'],
                    port=ds['port'],
                    database=ds.get('database'),
                    username=ds.get('username'),
                    password=ds.get('password'),
                    description=ds.get('description')
                )
                if error:
                    errors.append({'index': i, 'name': ds.get('name'), 'error': error})
                else:
                    imported += 1
            except Exception as e:
                errors.append({'index': i, 'name': ds.get('name'), 'error': str(e)})
        
        return imported, errors
    
    def process_import(self, user_id: int, content: str, format: str, 
                       import_type: str, **options) -> dict:
        """处理导入请求"""
        # 解析内容
        data, parse_error = self.parse_content(content, format, **options)
        if parse_error:
            return {
                'success': False,
                'error': parse_error,
                'stage': 'parse'
            }
        
        # 验证数据
        valid_data, validation_errors = self.validate_import_data(data, import_type)
        
        if not valid_data:
            return {
                'success': False,
                'error': '没有有效的数据可导入',
                'validation_errors': validation_errors,
                'stage': 'validate'
            }
        
        # 执行导入
        if import_type == 'template':
            imported, import_errors = self.import_templates(user_id, valid_data)
        elif import_type == 'datasource':
            imported, import_errors = self.import_datasources(user_id, valid_data)
        else:
            # 其他类型返回解析后的数据
            return {
                'success': True,
                'data': valid_data,
                'total': len(data),
                'valid_count': len(valid_data),
                'validation_errors': validation_errors,
                'stage': 'complete'
            }
        
        return {
            'success': True,
            'imported': imported,
            'total': len(data),
            'valid_count': len(valid_data),
            'validation_errors': validation_errors,
            'import_errors': import_errors,
            'stage': 'complete'
        }


# 单例
import_service = ImportService()
