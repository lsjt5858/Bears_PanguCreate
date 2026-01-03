"""
数据生成路由
"""
import time
import json
from flask import Blueprint, jsonify, request, g

from services import data_generator_service
from services.history_service import history_service
from middleware import optional_auth

generate_bp = Blueprint('generate', __name__, url_prefix='/api')


@generate_bp.route('/generate', methods=['POST'])
@optional_auth
def generate():
    """
    生成测试数据
    ---
    tags:
      - 数据生成
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          required:
            - fields
          properties:
            fields:
              type: array
              description: 字段配置列表
              items:
                type: object
                properties:
                  id:
                    type: string
                  name:
                    type: string
                    description: 字段名
                  type:
                    type: string
                    description: 数据类型（如 uuid, chineseName, email 等）
              example:
                - id: "1"
                  name: "id"
                  type: "uuid"
                - id: "2"
                  name: "name"
                  type: "chineseName"
            count:
              type: integer
              description: 生成数量（1-10000）
              default: 10
              example: 100
            name:
              type: string
              description: 生成任务名称（可选）
            project_id:
              type: integer
              description: 项目ID（可选）
            template_id:
              type: string
              description: 模板ID（可选）
    responses:
      200:
        description: 生成成功
        schema:
          type: object
          properties:
            success:
              type: boolean
            data:
              type: array
              items:
                type: object
            count:
              type: integer
            execution_time_ms:
              type: integer
      400:
        description: 参数错误
    """
    start_time = time.time()
    
    data = request.get_json()
    fields = data.get("fields", [])
    count = data.get("count", 10)
    name = data.get("name")  # 可选的生成名称
    project_id = data.get("project_id")  # 可选的项目 ID
    template_id = data.get("template_id")  # 可选的模板 ID
    
    # 参数验证
    if count < 1 or count > 10000:
        return jsonify({
            "success": False, 
            "error": "count must be between 1 and 10000"
        }), 400
    
    if not fields:
        return jsonify({
            "success": False, 
            "error": "fields is required"
        }), 400
    
    # 生成数据
    result = data_generator_service.generate_data(fields, count)
    
    # 计算执行时间和数据大小
    execution_time_ms = int((time.time() - start_time) * 1000)
    data_size_bytes = len(json.dumps(result, ensure_ascii=False).encode('utf-8'))
    
    # 如果用户已登录，记录历史
    history_uuid = None
    if hasattr(g, 'current_user') and g.current_user:
        try:
            history = history_service.create_history(
                user_id=g.current_user.id,
                fields=fields,
                row_count=count,
                name=name,
                project_id=project_id,
                template_id=template_id,
                export_format='json',
                execution_time_ms=execution_time_ms,
                data_size_bytes=data_size_bytes
            )
            history_uuid = history.uuid
        except Exception as e:
            # 记录历史失败不影响数据生成
            print(f"Failed to create history: {e}")
    
    return jsonify({
        "success": True, 
        "data": result, 
        "count": len(result),
        "fields": fields,
        "history_uuid": history_uuid,
        "execution_time_ms": execution_time_ms
    })
