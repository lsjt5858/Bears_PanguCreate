"""
模板服务
管理数据模板的CRUD操作
"""
from typing import List, Dict, Any, Optional
from datetime import datetime
import uuid as uuid_lib


class TemplateService:
    """模板服务"""
    
    def __init__(self):
        # 内存存储模板（生产环境应使用数据库）
        self._templates: List[Dict[str, Any]] = self._init_default_templates()

    def _init_default_templates(self) -> List[Dict[str, Any]]:
        """初始化默认模板"""
        return [
            {
                "id": "default-1",
                "name": "用户注册数据",
                "description": "包含用户注册所需的基本信息字段",
                "category": "user",
                "fields": [
                    {"id": "d1-1", "name": "user_id", "type": "uuid"},
                    {"id": "d1-2", "name": "username", "type": "chineseName"},
                    {"id": "d1-3", "name": "email", "type": "email"},
                    {"id": "d1-4", "name": "phone", "type": "chinesePhone"},
                    {"id": "d1-5", "name": "password", "type": "string"},
                    {"id": "d1-6", "name": "created_at", "type": "datetime"},
                ],
                "createdAt": "2024-01-01T00:00:00.000Z",
                "updatedAt": "2024-01-01T00:00:00.000Z",
            },
            {
                "id": "default-2",
                "name": "电商订单数据",
                "description": "电商平台订单测试数据模板",
                "category": "order",
                "fields": [
                    {"id": "d2-1", "name": "order_id", "type": "uuid"},
                    {"id": "d2-2", "name": "customer_name", "type": "chineseName"},
                    {"id": "d2-3", "name": "total_amount", "type": "amount"},
                    {"id": "d2-4", "name": "shipping_address", "type": "chineseAddress"},
                    {"id": "d2-5", "name": "order_date", "type": "datetime"},
                    {"id": "d2-6", "name": "phone", "type": "chinesePhone"},
                ],
                "createdAt": "2024-01-01T00:00:00.000Z",
                "updatedAt": "2024-01-01T00:00:00.000Z",
            },
            {
                "id": "default-3",
                "name": "商品信息数据",
                "description": "商品基础信息测试数据",
                "category": "product",
                "fields": [
                    {"id": "d3-1", "name": "product_id", "type": "uuid"},
                    {"id": "d3-2", "name": "product_name", "type": "word"},
                    {"id": "d3-3", "name": "price", "type": "amount"},
                    {"id": "d3-4", "name": "description", "type": "sentence"},
                    {"id": "d3-5", "name": "created_at", "type": "datetime"},
                ],
                "createdAt": "2024-01-01T00:00:00.000Z",
                "updatedAt": "2024-01-01T00:00:00.000Z",
            },
            {
                "id": "default-4",
                "name": "财务流水数据",
                "description": "财务交易流水测试数据",
                "category": "finance",
                "fields": [
                    {"id": "d4-1", "name": "transaction_id", "type": "uuid"},
                    {"id": "d4-2", "name": "account_name", "type": "chineseName"},
                    {"id": "d4-3", "name": "bank_card", "type": "bankCard"},
                    {"id": "d4-4", "name": "amount", "type": "amount"},
                    {"id": "d4-5", "name": "transaction_time", "type": "datetime"},
                ],
                "createdAt": "2024-01-01T00:00:00.000Z",
                "updatedAt": "2024-01-01T00:00:00.000Z",
            },
        ]

    def get_all(self) -> List[Dict[str, Any]]:
        """获取所有模板"""
        return self._templates

    def get_by_id(self, template_id: str) -> Optional[Dict[str, Any]]:
        """根据ID获取模板"""
        return next((t for t in self._templates if t["id"] == template_id), None)

    def get_by_category(self, category: str) -> List[Dict[str, Any]]:
        """按分类获取模板"""
        return [t for t in self._templates if t["category"] == category]

    def create(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """创建模板"""
        now = datetime.now().isoformat()
        template = {
            "id": str(uuid_lib.uuid4()),
            "name": data.get("name", ""),
            "description": data.get("description", ""),
            "category": data.get("category", "other"),
            "fields": data.get("fields", []),
            "createdAt": now,
            "updatedAt": now,
        }
        self._templates.append(template)
        return template

    def update(self, template_id: str, data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """更新模板"""
        template = self.get_by_id(template_id)
        if not template:
            return None
        
        template["name"] = data.get("name", template["name"])
        template["description"] = data.get("description", template["description"])
        template["category"] = data.get("category", template["category"])
        template["fields"] = data.get("fields", template["fields"])
        template["updatedAt"] = datetime.now().isoformat()
        
        return template

    def delete(self, template_id: str) -> bool:
        """删除模板"""
        original_len = len(self._templates)
        self._templates = [t for t in self._templates if t["id"] != template_id]
        return len(self._templates) < original_len


# 单例实例
template_service = TemplateService()
