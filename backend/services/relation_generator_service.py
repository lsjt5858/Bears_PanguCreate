
from services.data_generator_service import data_generator_service
import random
import uuid

class RelationGeneratorService:
    def generate_relation_data(self, tables, relations):
        """
        生成关联数据
        :param tables: list of dict, 每个表的配置 {id, name, count, fields}
        :param relations: list of dict, 关系配置 {sourceTable, sourceColumn, targetTable, targetColumn, relationType}
        :return: dict, {tableName: [rows]}
        """
        result_data = {}
        
        # 1. 首先生成所有表的基础数据（不包含外键）
        table_map = {t['name']: t for t in tables}
        
        # 确定生成顺序（拓扑排序的简化版，这里先假设这里没有循环依赖且用户定义顺序合理，或者先生成所有主数据后再填补外键）
        # 更好的策略：先生成所有非外键数据，再处理外键关联
        
        for table in tables:
            # 过滤掉作为外键的目标列，这些列的数据需要后续根据关系生成
            # 但 DataGeneratorService 需要知道所有列。
            # 策略：先让 DataGeneratorService 生成所有数据，对于外键列，我们稍后覆盖它们。
            
            # 转换 fields 格式以匹配 DataGeneratorService
            # 前端 fields包含 id, name, type. 后端需要 type, name, options
            # 注意：前端 RelationPage 的 fields 只有简单的 id, name, type。需要适配。
            
            gen_fields = []
            fk_columns = set()
            
            # 找出该表作为目标表的所有关系，标记外键列
            for rel in relations:
                if rel['targetTable'] == table['name']:
                    fk_columns.add(rel['targetColumn'])
            
            for field in table['fields']:
                # 如果是外键列，暂时作为 string 生成，稍后覆盖
                # 或者可以传递特殊类型给 DataGenerator? 不，直接生成即可，反正要覆盖。
                gen_fields.append({
                    "name": field['name'],
                    "type": field['type'],
                    "options": {}
                })
            
            rows = data_generator_service.generate_data(gen_fields, table['count'])
            result_data[table['name']] = rows
            
        # 2. 处理关系，填充/覆盖外键数据
        for rel in relations:
            source_table_name = rel['sourceTable']
            target_table_name = rel['targetTable']
            source_col = rel['sourceColumn']
            target_col = rel['targetColumn']
            rel_type = rel['relationType']
            
            if source_table_name not in result_data or target_table_name not in result_data:
                continue
                
            source_rows = result_data[source_table_name]
            target_rows = result_data[target_table_name]
            
            # 获取源表的所有可用 ID (或其他关联键)
            source_keys = [row.get(source_col) for row in source_rows]
            
            if not source_keys:
                continue
                
            if rel_type == 'one-to-one':
                # 一对一：目标表的每一行对应源表的一个唯一行
                # 如果目标表行数 > 源表行数，则无法唯一，只能循环或报错。这里选择循环使用但尽量唯一。
                # 实际上 1:1 通常要求行数一致。我们这里打乱源key然后赋值。
                shuffled_keys = source_keys.copy()
                random.shuffle(shuffled_keys)
                
                for i, row in enumerate(target_rows):
                    key = shuffled_keys[i % len(shuffled_keys)]
                    row[target_col] = key
                    
            elif rel_type == 'one-to-many':
                # 一对多：目标表的每一行关联到源表的一个行（源表是"一"，目标表是"多"）
                # 例如 User(1) -> Orders(N)。Order 表中的 user_id 从 User 表 id 中随机选。
                for row in target_rows:
                    row[target_col] = random.choice(source_keys)
                    
            elif rel_type == 'many-to-many':
                # 多对多：通常不直接修改这两个表，而是应该有一个中间表。
                # 但如果用户的配置是直接连，这通常是不合逻辑的物理模型。
                # 假设用户想模拟的是：通过某种方式关联。
                # 对于标准的多对多，通常是生成第三张表。
                # 但此处的 UI 只有 "表" 和 "关系"。如果这是逻辑关系，生成数据时如何体现？
                # 如果用户定义了 T1 和 T2 多对多，且指定了 T1.id 和 T2.uid... 这在物理上通常意味着 T2 有个 uid 指向 T1，但这只是 1:N。
                # 如果是 T1 和 T2 多对多，通常意味着存在 T3 (T1_id, T2_id)。
                # 鉴于此工具的简单性，如果用户选择了多对多，我们是否应该自动生成中间表数据并返回？
                # 或者，暂不支持自动生成中间表，只支持 FK 填充。
                # 我们按照 1:N 处理 FK 填充。因为物理上必须是 1:N (外键在目标表)。
                for row in target_rows:
                    row[target_col] = random.choice(source_keys)

        return result_data

relation_generator_service = RelationGeneratorService()
