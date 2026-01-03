"""
数据源路由
处理数据源管理相关的 API 请求
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from flask import Blueprint, request, jsonify, g
from middleware.auth import login_required
from services.datasource_service import datasource_service

datasource_bp = Blueprint('datasource', __name__, url_prefix='/api/datasources')


@datasource_bp.route('', methods=['GET'])
@login_required
def list_datasources():
    """获取数据源列表
    ---
    tags:
      - 数据源管理
    security:
      - BearerAuth: []
    parameters:
      - name: project_id
        in: query
        type: integer
        required: false
        description: 项目ID
      - name: type
        in: query
        type: string
        required: false
        description: 数据源类型 (mysql/postgresql/mongodb)
      - name: status
        in: query
        type: string
        required: false
        description: 状态
      - name: page
        in: query
        type: integer
        required: false
        default: 1
        description: 页码
      - name: page_size
        in: query
        type: integer
        required: false
        default: 20
        description: 每页数量
    responses:
      200:
        description: 数据源列表
        schema:
          type: object
          properties:
            data:
              type: array
              items:
                type: object
            pagination:
              type: object
              properties:
                page:
                  type: integer
                page_size:
                  type: integer
                total:
                  type: integer
                total_pages:
                  type: integer
    """
    user_id = g.current_user.id
    
    # 获取查询参数
    project_id = request.args.get('project_id', type=int)
    ds_type = request.args.get('type')
    status = request.args.get('status')
    page = request.args.get('page', 1, type=int)
    page_size = request.args.get('page_size', 20, type=int)
    
    datasources, total = datasource_service.list_datasources(
        user_id=user_id,
        project_id=project_id,
        ds_type=ds_type,
        status=status,
        page=page,
        page_size=page_size
    )
    
    return jsonify({
        'data': [ds.to_dict() for ds in datasources],
        'pagination': {
            'page': page,
            'page_size': page_size,
            'total': total,
            'total_pages': (total + page_size - 1) // page_size
        }
    })


@datasource_bp.route('', methods=['POST'])
@login_required
def create_datasource():
    """创建数据源
    ---
    tags:
      - 数据源管理
    security:
      - BearerAuth: []
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          required:
            - name
            - type
            - host
            - port
          properties:
            name:
              type: string
              description: 数据源名称
            type:
              type: string
              description: 数据源类型 (mysql/postgresql/mongodb)
            host:
              type: string
              description: 主机地址
            port:
              type: integer
              description: 端口号
            database:
              type: string
              description: 数据库名
            username:
              type: string
              description: 用户名
            password:
              type: string
              description: 密码
            description:
              type: string
              description: 描述
            project_id:
              type: integer
              description: 项目ID
            use_ssl:
              type: boolean
              description: 是否使用SSL
            ssl_config:
              type: object
              description: SSL配置
            api_config:
              type: object
              description: API配置
    responses:
      201:
        description: 创建成功
        schema:
          type: object
          properties:
            message:
              type: string
            data:
              type: object
      400:
        description: 请求参数错误
    """
    user_id = g.current_user.id
    data = request.get_json()
    
    if not data:
        return jsonify({'error': '请求数据不能为空'}), 400
    
    # 验证必填字段
    required_fields = ['name', 'type', 'host', 'port']
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'缺少必填字段: {field}'}), 400
    
    datasource, error = datasource_service.create_datasource(
        user_id=user_id,
        name=data['name'],
        ds_type=data['type'],
        host=data['host'],
        port=data['port'],
        database=data.get('database'),
        username=data.get('username'),
        password=data.get('password'),
        description=data.get('description'),
        project_id=data.get('project_id'),
        use_ssl=data.get('use_ssl', False),
        ssl_config=data.get('ssl_config'),
        api_config=data.get('api_config')
    )
    
    if error:
        return jsonify({'error': error}), 400
    
    return jsonify({
        'message': '数据源创建成功',
        'data': datasource.to_dict()
    }), 201


@datasource_bp.route('/<datasource_id>', methods=['GET'])
@login_required
def get_datasource(datasource_id):
    """获取数据源详情
    ---
    tags:
      - 数据源管理
    security:
      - BearerAuth: []
    parameters:
      - name: datasource_id
        in: path
        type: string
        required: true
        description: 数据源ID
    responses:
      200:
        description: 数据源详情
        schema:
          type: object
          properties:
            data:
              type: object
      404:
        description: 数据源不存在
    """
    user_id = g.current_user.id
    
    datasource = datasource_service.get_datasource(datasource_id, user_id)
    if not datasource:
        return jsonify({'error': '数据源不存在'}), 404
    
    return jsonify({
        'data': datasource.to_dict()
    })


@datasource_bp.route('/<datasource_id>', methods=['PUT'])
@login_required
def update_datasource(datasource_id):
    """更新数据源
    ---
    tags:
      - 数据源管理
    security:
      - BearerAuth: []
    parameters:
      - name: datasource_id
        in: path
        type: string
        required: true
        description: 数据源ID
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            name:
              type: string
              description: 数据源名称
            host:
              type: string
              description: 主机地址
            port:
              type: integer
              description: 端口号
            database:
              type: string
              description: 数据库名
            username:
              type: string
              description: 用户名
            password:
              type: string
              description: 密码
            description:
              type: string
              description: 描述
            use_ssl:
              type: boolean
              description: 是否使用SSL
    responses:
      200:
        description: 更新成功
        schema:
          type: object
          properties:
            message:
              type: string
            data:
              type: object
      400:
        description: 请求参数错误
    """
    user_id = g.current_user.id
    data = request.get_json()
    
    if not data:
        return jsonify({'error': '请求数据不能为空'}), 400
    
    datasource, error = datasource_service.update_datasource(
        datasource_id=datasource_id,
        user_id=user_id,
        **data
    )
    
    if error:
        return jsonify({'error': error}), 400
    
    return jsonify({
        'message': '数据源更新成功',
        'data': datasource.to_dict()
    })


@datasource_bp.route('/<datasource_id>', methods=['DELETE'])
@login_required
def delete_datasource(datasource_id):
    """删除数据源
    ---
    tags:
      - 数据源管理
    security:
      - BearerAuth: []
    parameters:
      - name: datasource_id
        in: path
        type: string
        required: true
        description: 数据源ID
    responses:
      200:
        description: 删除成功
        schema:
          type: object
          properties:
            message:
              type: string
      400:
        description: 删除失败
    """
    user_id = g.current_user.id
    
    success, error = datasource_service.delete_datasource(datasource_id, user_id)
    
    if not success:
        return jsonify({'error': error}), 400
    
    return jsonify({
        'message': '数据源删除成功'
    })


@datasource_bp.route('/<datasource_id>/test', methods=['POST'])
@login_required
def test_datasource_connection(datasource_id):
    """测试数据源连接
    ---
    tags:
      - 数据源管理
    security:
      - BearerAuth: []
    parameters:
      - name: datasource_id
        in: path
        type: string
        required: true
        description: 数据源ID
    responses:
      200:
        description: 测试结果
        schema:
          type: object
          properties:
            success:
              type: boolean
            message:
              type: string
            info:
              type: object
    """
    user_id = g.current_user.id
    
    success, message, info = datasource_service.test_connection(datasource_id, user_id)
    
    return jsonify({
        'success': success,
        'message': message,
        'info': info
    })


@datasource_bp.route('/test', methods=['POST'])
@login_required
def test_connection_params():
    """测试连接参数（不保存）
    ---
    tags:
      - 数据源管理
    security:
      - BearerAuth: []
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          required:
            - type
            - host
            - port
          properties:
            type:
              type: string
              description: 数据源类型 (mysql/postgresql/mongodb)
            host:
              type: string
              description: 主机地址
            port:
              type: integer
              description: 端口号
            database:
              type: string
              description: 数据库名
            username:
              type: string
              description: 用户名
            password:
              type: string
              description: 密码
            use_ssl:
              type: boolean
              description: 是否使用SSL
            api_config:
              type: object
              description: API配置
    responses:
      200:
        description: 测试结果
        schema:
          type: object
          properties:
            success:
              type: boolean
            message:
              type: string
            info:
              type: object
      400:
        description: 请求参数错误
    """
    data = request.get_json()
    
    if not data:
        return jsonify({'error': '请求数据不能为空'}), 400
    
    # 验证必填字段
    required_fields = ['type', 'host', 'port']
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'缺少必填字段: {field}'}), 400
    
    success, message, info = datasource_service.test_connection_params(
        ds_type=data['type'],
        host=data['host'],
        port=data['port'],
        database=data.get('database'),
        username=data.get('username'),
        password=data.get('password'),
        use_ssl=data.get('use_ssl', False),
        api_config=data.get('api_config')
    )
    
    return jsonify({
        'success': success,
        'message': message,
        'info': info
    })


@datasource_bp.route('/<datasource_id>/tables', methods=['GET'])
@login_required
def get_datasource_tables(datasource_id):
    """获取数据源的表/集合列表
    ---
    tags:
      - 数据源管理
    security:
      - BearerAuth: []
    parameters:
      - name: datasource_id
        in: path
        type: string
        required: true
        description: 数据源ID
    responses:
      200:
        description: 表列表
        schema:
          type: object
          properties:
            data:
              type: array
              items:
                type: object
      400:
        description: 获取失败
    """
    user_id = g.current_user.id
    
    tables, error = datasource_service.get_tables(datasource_id, user_id)
    
    if error:
        return jsonify({'error': error}), 400
    
    return jsonify({
        'data': tables
    })


@datasource_bp.route('/<datasource_id>/tables/<table_name>', methods=['GET'])
@login_required
def get_table_schema(datasource_id, table_name):
    """获取表结构
    ---
    tags:
      - 数据源管理
    security:
      - BearerAuth: []
    parameters:
      - name: datasource_id
        in: path
        type: string
        required: true
        description: 数据源ID
      - name: table_name
        in: path
        type: string
        required: true
        description: 表名
    responses:
      200:
        description: 表结构
        schema:
          type: object
          properties:
            data:
              type: object
      404:
        description: 数据源不存在
      500:
        description: 服务器错误
    """
    user_id = g.current_user.id
    
    from models.datasource import DataSource
    
    datasource = DataSource.find_by_uuid(datasource_id)
    if not datasource or datasource.user_id != user_id:
        return jsonify({'error': '数据源不存在'}), 404
    
    # 根据类型选择连接器
    try:
        if datasource.type == 'mysql':
            from connectors.mysql_connector import MySQLConnector
            connector = MySQLConnector(
                host=datasource.host,
                port=datasource.port,
                database=datasource.database,
                username=datasource.username,
                password=datasource.get_password(),
                use_ssl=datasource.use_ssl
            )
        elif datasource.type == 'postgresql':
            from connectors.postgres_connector import PostgreSQLConnector
            connector = PostgreSQLConnector(
                host=datasource.host,
                port=datasource.port,
                database=datasource.database,
                username=datasource.username,
                password=datasource.get_password(),
                use_ssl=datasource.use_ssl
            )
        elif datasource.type == 'mongodb':
            from connectors.mongo_connector import MongoDBConnector
            connector = MongoDBConnector(
                host=datasource.host,
                port=datasource.port,
                database=datasource.database,
                username=datasource.username,
                password=datasource.get_password()
            )
        else:
            return jsonify({'error': f'不支持的数据源类型: {datasource.type}'}), 400
        
        with connector:
            schema = connector.get_table_schema(table_name)
        
        datasource.record_query()
        
        return jsonify({
            'data': schema
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@datasource_bp.route('/<datasource_id>/write', methods=['POST'])
@login_required
def write_to_datasource(datasource_id):
    """向数据源写入数据
    ---
    tags:
      - 数据源管理
    security:
      - BearerAuth: []
    parameters:
      - name: datasource_id
        in: path
        type: string
        required: true
        description: 数据源ID
      - name: body
        in: body
        required: true
        schema:
          type: object
          required:
            - table_name
            - data
          properties:
            table_name:
              type: string
              description: 表名
            data:
              type: array
              items:
                type: object
              description: 要写入的数据
            create_table:
              type: boolean
              description: 是否创建表
            columns:
              type: array
              items:
                type: object
              description: 列定义
    responses:
      200:
        description: 写入成功
        schema:
          type: object
          properties:
            message:
              type: string
            inserted:
              type: integer
      400:
        description: 请求参数错误
      404:
        description: 数据源不存在
      500:
        description: 写入失败
    """
    user_id = g.current_user.id
    data = request.get_json()
    
    if not data:
        return jsonify({'error': '请求数据不能为空'}), 400
    
    table_name = data.get('table_name')
    records = data.get('data', [])
    create_table = data.get('create_table', False)
    columns = data.get('columns', [])
    
    if not table_name:
        return jsonify({'error': '缺少表名'}), 400
    
    if not records:
        return jsonify({'error': '数据不能为空'}), 400
    
    from models.datasource import DataSource
    
    datasource = DataSource.find_by_uuid(datasource_id)
    if not datasource or datasource.user_id != user_id:
        return jsonify({'error': '数据源不存在'}), 404
    
    try:
        # 根据类型选择连接器
        if datasource.type == 'mysql':
            from connectors.mysql_connector import MySQLConnector
            connector = MySQLConnector(
                host=datasource.host,
                port=datasource.port,
                database=datasource.database,
                username=datasource.username,
                password=datasource.get_password(),
                use_ssl=datasource.use_ssl
            )
        elif datasource.type == 'postgresql':
            from connectors.postgres_connector import PostgreSQLConnector
            connector = PostgreSQLConnector(
                host=datasource.host,
                port=datasource.port,
                database=datasource.database,
                username=datasource.username,
                password=datasource.get_password(),
                use_ssl=datasource.use_ssl
            )
        elif datasource.type == 'mongodb':
            from connectors.mongo_connector import MongoDBConnector
            connector = MongoDBConnector(
                host=datasource.host,
                port=datasource.port,
                database=datasource.database,
                username=datasource.username,
                password=datasource.get_password()
            )
        else:
            return jsonify({'error': f'不支持的数据源类型: {datasource.type}'}), 400
        
        with connector:
            # 如果需要创建表
            if create_table and columns:
                if datasource.type in ['mysql', 'postgresql']:
                    success, error = connector.create_table(table_name, columns)
                    if not success:
                        return jsonify({'error': f'创建表失败: {error}'}), 500
                elif datasource.type == 'mongodb':
                    connector.create_collection(table_name)
            
            # 插入数据
            success, inserted, error = connector.insert_data(table_name, records)
        
        if not success:
            return jsonify({'error': f'写入失败: {error}'}), 500
        
        datasource.record_query()
        
        return jsonify({
            'message': '数据写入成功',
            'inserted': inserted
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500
