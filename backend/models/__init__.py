"""
数据模型定义
"""
from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional
from datetime import datetime
import uuid as uuid_lib

# 数据库模型
from .base import BaseModel
from .user import User
from .project import Project, project_members
from .history import GenerationHistory
from .template import Template as TemplateModel, Tag, TemplateRating, TemplateFavorite, TemplateDownload
from .datasource import DataSource


@dataclass
class DataField:
    """数据字段模型"""
    id: str
    name: str
    type: str
    options: Optional[Dict[str, Any]] = None

    def to_dict(self) -> Dict[str, Any]:
        result = {"id": self.id, "name": self.name, "type": self.type}
        if self.options:
            result["options"] = self.options
        return result

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "DataField":
        return cls(
            id=data.get("id", str(uuid_lib.uuid4())),
            name=data.get("name", ""),
            type=data.get("type", "string"),
            options=data.get("options")
        )


@dataclass
class Template:
    """模板模型（旧版，保持兼容）"""
    id: str
    name: str
    description: str
    category: str
    fields: List[DataField]
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    updated_at: str = field(default_factory=lambda: datetime.now().isoformat())

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "category": self.category,
            "fields": [f.to_dict() for f in self.fields],
            "createdAt": self.created_at,
            "updatedAt": self.updated_at,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Template":
        return cls(
            id=data.get("id", str(uuid_lib.uuid4())),
            name=data.get("name", ""),
            description=data.get("description", ""),
            category=data.get("category", "other"),
            fields=[DataField.from_dict(f) for f in data.get("fields", [])],
            created_at=data.get("createdAt", datetime.now().isoformat()),
            updated_at=data.get("updatedAt", datetime.now().isoformat()),
        )


@dataclass
class DataType:
    """数据类型定义"""
    id: str
    name: str
    icon: str
    category: str

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "icon": self.icon,
            "category": self.category,
        }
