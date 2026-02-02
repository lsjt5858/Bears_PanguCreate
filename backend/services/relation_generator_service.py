"""
关系数据生成服务
负责生成具有关联关系的多表数据
"""
from services.data_generator_service import data_generator_service
import random
from typing import List, Dict, Any


class RelationGeneratorService:
    """关系数据生成服务"""
    
    def generate_relation_data(self, tables: List[Dict[str, Any]], relations: List[Dict[str, Any]]) -> Dict[str, List[Dict[str, Any]]]:
        """
        生成关联数据
        
        Args:
            tables: 表配置列表，每个表包含 {id, name, count, fields}
                - id: 表ID
                - name: 表名
                - count: 生成行数
                - fields: 字段列表 [{id, name, type}]
            relations: 关系配置列表 {sourceTable, sourceColumn, targetTable, targetColumn, relationType}
                - sourceTable: 源表名（主表）
                - sourceColumn: 源表关联列
                - targetTable: 目标表名（从表）
                - targetColumn: 目标表外键列
                - relationType: 关系类型 (one-to-one, one-to-many, many-to-many)
        
        Returns:
            dict: {tableName: [rows]} 每个表的生成数据
        """
        if not tables:
            return {}
        
        result_data = {}
        table_map = {t['name']: t for t in tables}
        
        # 1. 首先生成所有表的基础数据
        for table in tables:
            table_name = table.get('name')
            if not table_name:
                continue
            
            # 标记外键列（这些列的值将在后续步骤中被关系数据覆盖）
            fk_columns = set()
            for rel in relations:
                if rel.get('targetTable') == table_name:
                    fk_columns.add(rel.get('targetColumn'))
            
            # 转换字段格式以匹配 DataGeneratorService
            gen_fields = []
            for field in table.get('fields', []):
                field_name = field.get('name')
                field_type = field.get('type', 'string')
                
                if field_name:
                    gen_fields.append({
                        "name": field_name,
                        "type": field_type
                    })
            
            # 生成表数据
            if gen_fields:
                rows = data_generator_service.generate_data(gen_fields, table.get('count', 10))
                result_data[table_name] = rows
            else:
                result_data[table_name] = []
        
        # 2. 处理关系，填充外键数据
        for rel in relations:
            try:
                self._apply_relation(result_data, rel)
            except Exception as e:
                print(f"应用关系时出错: {e}")
                # 继续处理其他关系
        
        return result_data
    
    def _apply_relation(self, result_data: Dict[str, List[Dict[str, Any]]], relation: Dict[str, Any]) -> None:
        """
        应用单个关系到数据中
        
        Args:
            result_data: 已生成的表数据
            relation: 关系配置
        """
        source_table_name = relation.get('sourceTable')
        target_table_name = relation.get('targetTable')
        source_col = relation.get('sourceColumn')
        target_col = relation.get('targetColumn')
        rel_type = relation.get('relationType', 'one-to-many')
        
        # 验证表和列是否存在
        if source_table_name not in result_data or target_table_name not in result_data:
            print(f"警告: 表 {source_table_name} 或 {target_table_name} 不存在")
            return
        
        source_rows = result_data[source_table_name]
        target_rows = result_data[target_table_name]
        
        if not source_rows or not target_rows:
            print(f"警告: 表 {source_table_name} 或 {target_table_name} 没有数据")
            return
        
        # 获取源表的所有关联键值
        source_keys = []
        for row in source_rows:
            if source_col in row:
                source_keys.append(row[source_col])
        
        if not source_keys:
            print(f"警告: 源表 {source_table_name} 的列 {source_col} 没有数据")
            return
        
        # 根据关系类型填充外键
        if rel_type == 'one-to-one':
            # 一对一：目标表的每一行对应源表的一个唯一行
            shuffled_keys = source_keys.copy()
            random.shuffle(shuffled_keys)
            
            for i, row in enumerate(target_rows):
                key = shuffled_keys[i % len(shuffled_keys)]
                row[target_col] = key
        
        elif rel_type == 'one-to-many':
            # 一对多：目标表的每一行关联到源表的一个行（源表是"一"，目标表是"多"）
            # 例如 User(1) -> Orders(N)
            for row in target_rows:
                row[target_col] = random.choice(source_keys)
        
        elif rel_type == 'many-to-many':
            # 多对多：在物理实现上通常需要中间表
            # 这里简化处理为一对多（每个目标行随机关联一个源行）
            # 注意：真正的多对多关系需要额外的关联表
            for row in target_rows:
                row[target_col] = random.choice(source_keys)
        
        else:
            print(f"警告: 不支持的关系类型 {rel_type}")
    
    def validate_relations(self, tables: List[Dict[str, Any]], relations: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        验证关系配置的有效性
        
        Args:
            tables: 表配置列表
            relations: 关系配置列表
        
        Returns:
            dict: 验证结果 {valid: bool, errors: []}
        """
        errors = []
        table_names = {t.get('name') for t in tables if t.get('name')}
        
        # 构建表的字段映射
        table_fields = {}
        for table in tables:
            table_name = table.get('name')
            if table_name:
                table_fields[table_name] = {f.get('name') for f in table.get('fields', []) if f.get('name')}
        
        # 验证每个关系
        for i, rel in enumerate(relations):
            source_table = rel.get('sourceTable')
            target_table = rel.get('targetTable')
            source_col = rel.get('sourceColumn')
            target_col = rel.get('targetColumn')
            
            # 检查表是否存在
            if source_table not in table_names:
                errors.append(f"关系 {i+1}: 源表 '{source_table}' 不存在")
            
            if target_table not in table_names:
                errors.append(f"关系 {i+1}: 目标表 '{target_table}' 不存在")
            
            # 检查列是否存在
            if source_table in table_fields and source_col not in table_fields[source_table]:
                errors.append(f"关系 {i+1}: 源表 '{source_table}' 中不存在列 '{source_col}'")
            
            if target_table in table_fields and target_col not in table_fields[target_table]:
                errors.append(f"关系 {i+1}: 目标表 '{target_table}' 中不存在列 '{target_col}'")
        
        return {
            "valid": len(errors) == 0,
            "errors": errors
        }


# 单例实例
relation_generator_service = RelationGeneratorService()

