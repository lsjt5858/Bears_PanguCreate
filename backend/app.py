"""
DataForge Backend - Flask API
"""
from flask import Flask, jsonify, request
from flask_cors import CORS
from data_generator import generate_mock_data, DATA_TYPES
from datetime import datetime
import uuid

app = Flask(__name__)
CORS(app, origins=["http://localhost:5173", "http://localhost:3000"])

# 内存存储模板
templates = [
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


@app.route("/api/health", methods=["GET"])
def health():
    return jsonify({"status": "ok", "timestamp": datetime.now().isoformat()})


@app.route("/api/types", methods=["GET"])
def get_types():
    """获取所有支持的数据类型"""
    return jsonify({"success": True, "types": DATA_TYPES})


@app.route("/api/generate", methods=["POST"])
def generate():
    """生成测试数据"""
    data = request.get_json()
    fields = data.get("fields", [])
    count = data.get("count", 10)
    
    if count < 1 or count > 10000:
        return jsonify({"success": False, "error": "count must be between 1 and 10000"}), 400
    
    if not fields:
        return jsonify({"success": False, "error": "fields is required"}), 400
    
    result = generate_mock_data(fields, count)
    return jsonify({"success": True, "data": result, "count": len(result)})


@app.route("/api/templates", methods=["GET"])
def get_templates():
    """获取所有模板"""
    return jsonify({"success": True, "templates": templates})


@app.route("/api/templates/<template_id>", methods=["GET"])
def get_template(template_id):
    """获取单个模板"""
    template = next((t for t in templates if t["id"] == template_id), None)
    if not template:
        return jsonify({"success": False, "error": "Template not found"}), 404
    return jsonify({"success": True, "template": template})


@app.route("/api/templates", methods=["POST"])
def create_template():
    """创建模板"""
    data = request.get_json()
    now = datetime.now().isoformat()
    template = {
        "id": str(uuid.uuid4()),
        "name": data.get("name", ""),
        "description": data.get("description", ""),
        "category": data.get("category", "other"),
        "fields": data.get("fields", []),
        "createdAt": now,
        "updatedAt": now,
    }
    templates.append(template)
    return jsonify({"success": True, "template": template}), 201


@app.route("/api/templates/<template_id>", methods=["PUT"])
def update_template(template_id):
    """更新模板"""
    template = next((t for t in templates if t["id"] == template_id), None)
    if not template:
        return jsonify({"success": False, "error": "Template not found"}), 404
    
    data = request.get_json()
    template["name"] = data.get("name", template["name"])
    template["description"] = data.get("description", template["description"])
    template["category"] = data.get("category", template["category"])
    template["fields"] = data.get("fields", template["fields"])
    template["updatedAt"] = datetime.now().isoformat()
    
    return jsonify({"success": True, "template": template})


@app.route("/api/templates/<template_id>", methods=["DELETE"])
def delete_template(template_id):
    """删除模板"""
    global templates
    original_len = len(templates)
    templates = [t for t in templates if t["id"] != template_id]
    
    if len(templates) == original_len:
        return jsonify({"success": False, "error": "Template not found"}), 404
    
    return jsonify({"success": True, "message": "Template deleted"})


if __name__ == "__main__":
    app.run(debug=True, port=5000)
