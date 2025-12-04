"""
导出服务
负责将生成的数据导出为不同格式
"""
from typing import List, Dict, Any
from collections import OrderedDict
import json
import csv
import io


class ExportService:
    """导出服务"""

    def to_json(self, data: List[Dict[str, Any]], fields: List[Dict[str, Any]]) -> str:
        """导出为JSON格式"""
        # 确保字段顺序
        ordered_data = self._ensure_field_order(data, fields)
        return json.dumps(ordered_data, ensure_ascii=False, indent=2)

    def to_csv(self, data: List[Dict[str, Any]], fields: List[Dict[str, Any]]) -> str:
        """导出为CSV格式"""
        if not data or not fields:
            return ""
        
        output = io.StringIO()
        field_names = [f["name"] for f in fields]
        
        writer = csv.DictWriter(output, fieldnames=field_names, extrasaction='ignore')
        writer.writeheader()
        
        for row in data:
            # 按字段顺序写入
            ordered_row = {name: row.get(name, "") for name in field_names}
            writer.writerow(ordered_row)
        
        return output.getvalue()

    def to_sql(self, data: List[Dict[str, Any]], fields: List[Dict[str, Any]], table_name: str = "test_data") -> str:
        """导出为SQL INSERT语句"""
        if not data or not fields:
            return ""
        
        field_names = [f["name"] for f in fields]
        columns = ", ".join(field_names)
        
        values_list = []
        for row in data:
            values = []
            for name in field_names:
                val = row.get(name, "")
                # 转义单引号
                if isinstance(val, str):
                    val = val.replace("'", "''")
                    values.append(f"'{val}'")
                elif isinstance(val, bool):
                    values.append("1" if val else "0")
                elif val is None:
                    values.append("NULL")
                else:
                    values.append(str(val))
            values_list.append(f"({', '.join(values)})")
        
        return f"INSERT INTO {table_name} ({columns}) VALUES\n" + ",\n".join(values_list) + ";"

    def _ensure_field_order(self, data: List[Dict[str, Any]], fields: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """确保数据字段顺序与配置一致"""
        if not fields:
            return data
        
        field_names = [f["name"] for f in fields]
        ordered_data = []
        
        for row in data:
            ordered_row = OrderedDict()
            for name in field_names:
                if name in row:
                    ordered_row[name] = row[name]
            ordered_data.append(dict(ordered_row))
        
        return ordered_data


# 单例实例
export_service = ExportService()
