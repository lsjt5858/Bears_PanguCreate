#!/usr/bin/env python3
"""
模板市场功能测试脚本
"""
import requests
import json
import sys

BASE_URL = "http://localhost:5001/api"

# 测试数据
test_user = {
    "username": "test_user_market",
    "email": "test_market@example.com",
    "password": "Test@123456"
}

test_template = {
    "name": "测试模板 - 用户数据",
    "description": "这是一个测试模板，用于测试模板市场功能",
    "category": "user",
    "fields": [
        {"id": "1", "name": "用户名", "type": "string"},
        {"id": "2", "name": "邮箱", "type": "email"},
        {"id": "3", "name": "年龄", "type": "integer"}
    ],
    "tags": ["测试", "用户"],
    "is_public": True
}

class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    END = '\033[0m'

def print_test(name):
    print(f"\n{Colors.BLUE}{'='*60}")
    print(f"测试: {name}")
    print(f"{'='*60}{Colors.END}")

def print_success(msg):
    print(f"{Colors.GREEN}✓ {msg}{Colors.END}")

def print_error(msg):
    print(f"{Colors.RED}✗ {msg}{Colors.END}")

def print_info(msg):
    print(f"{Colors.YELLOW}ℹ {msg}{Colors.END}")

# 1. 注册用户
print_test("1. 用户注册")
try:
    resp = requests.post(f"{BASE_URL}/auth/register", json=test_user)
    if resp.status_code == 201:
        data = resp.json()
        token = data['data']['access_token']
        user_id = data['data']['user']['id']
        print_success(f"注册成功，用户ID: {user_id}")
    else:
        print_error(f"注册失败: {resp.status_code} - {resp.text}")
        sys.exit(1)
except Exception as e:
    print_error(f"注册异常: {e}")
    sys.exit(1)

# 2. 获取仪表盘统计
print_test("2. 获取仪表盘统计数据")
try:
    headers = {"Authorization": f"Bearer {token}"}
    resp = requests.get(f"{BASE_URL}/stats/dashboard", headers=headers)
    if resp.status_code == 200:
        data = resp.json()['data']
        print_success("获取仪表盘统计成功")
        print_info(f"  - 数据生成总量: {data['total_generated']}")
        print_info(f"  - 模板数量: {data['total_templates']}")
        print_info(f"  - 团队成员: {data['total_members']}")
        print_info(f"  - API调用次数: {data['api_calls']}")
    else:
        print_error(f"获取统计失败: {resp.status_code}")
except Exception as e:
    print_error(f"获取统计异常: {e}")

# 3. 获取生成趋势数据
print_test("3. 获取生成趋势数据")
try:
    resp = requests.get(f"{BASE_URL}/stats/trend?days=30", headers=headers)
    if resp.status_code == 200:
        data = resp.json()['data']
        print_success(f"获取趋势数据成功，共 {len(data)} 条记录")
        if data:
            print_info(f"  - 最早日期: {data[0]['date']}")
            print_info(f"  - 最新日期: {data[-1]['date']}")
    else:
        print_error(f"获取趋势失败: {resp.status_code}")
except Exception as e:
    print_error(f"获取趋势异常: {e}")

# 4. 获取最近活动
print_test("4. 获取最近活动")
try:
    resp = requests.get(f"{BASE_URL}/stats/activities?limit=10", headers=headers)
    if resp.status_code == 200:
        data = resp.json()['data']
        print_success(f"获取最近活动成功，共 {len(data)} 条记录")
        if data:
            print_info(f"  - 最新活动: {data[0]['action']} - {data[0]['target']}")
    else:
        print_error(f"获取活动失败: {resp.status_code}")
except Exception as e:
    print_error(f"获取活动异常: {e}")

# 5. 获取模板市场列表
print_test("5. 获取模板市场列表")
try:
    resp = requests.get(f"{BASE_URL}/market/templates?page=1&page_size=10", headers=headers)
    if resp.status_code == 200:
        data = resp.json()
        templates = data['data']
        pagination = data['pagination']
        print_success(f"获取模板列表成功")
        print_info(f"  - 当前页: {pagination['page']}")
        print_info(f"  - 总数: {pagination['total']}")
        print_info(f"  - 总页数: {pagination['total_pages']}")
        if templates:
            print_info(f"  - 第一个模板: {templates[0]['name']}")
    else:
        print_error(f"获取模板列表失败: {resp.status_code}")
except Exception as e:
    print_error(f"获取模板列表异常: {e}")

# 6. 创建模板
print_test("6. 创建模板")
try:
    resp = requests.post(f"{BASE_URL}/market/templates", json=test_template, headers=headers)
    if resp.status_code == 201:
        data = resp.json()['data']
        template_id = data['uuid'] or data['id']
        print_success(f"创建模板成功，模板ID: {template_id}")
        print_info(f"  - 模板名称: {data['name']}")
        print_info(f"  - 分类: {data['category']}")
    else:
        print_error(f"创建模板失败: {resp.status_code} - {resp.text}")
        template_id = None
except Exception as e:
    print_error(f"创建模板异常: {e}")
    template_id = None

# 7. 获取模板详情
if template_id:
    print_test("7. 获取模板详情")
    try:
        resp = requests.get(f"{BASE_URL}/market/templates/{template_id}", headers=headers)
        if resp.status_code == 200:
            data = resp.json()['data']
            print_success(f"获取模板详情成功")
            print_info(f"  - 模板名称: {data['name']}")
            print_info(f"  - 描述: {data['description']}")
            print_info(f"  - 字段数: {len(data['fields'])}")
        else:
            print_error(f"获取模板详情失败: {resp.status_code}")
    except Exception as e:
        print_error(f"获取模板详情异常: {e}")

    # 8. 使用模板（记录下载）
    print_test("8. 使用模板（记录下载）")
    try:
        resp = requests.post(f"{BASE_URL}/market/templates/{template_id}/use", headers=headers)
        if resp.status_code == 200:
            print_success("使用模板成功")
        else:
            print_error(f"使用模板失败: {resp.status_code}")
    except Exception as e:
        print_error(f"使用模板异常: {e}")

    # 9. 评分模板
    print_test("9. 评分模板")
    try:
        rating_data = {"score": 5, "comment": "很好的模板！"}
        resp = requests.post(f"{BASE_URL}/market/templates/{template_id}/rate", json=rating_data, headers=headers)
        if resp.status_code == 200:
            print_success("评分模板成功")
        else:
            print_error(f"评分模板失败: {resp.status_code}")
    except Exception as e:
        print_error(f"评分模板异常: {e}")

    # 10. 获取模板评分列表
    print_test("10. 获取模板评分列表")
    try:
        resp = requests.get(f"{BASE_URL}/market/templates/{template_id}/ratings?page=1&page_size=10", headers=headers)
        if resp.status_code == 200:
            data = resp.json()
            ratings = data['data']
            print_success(f"获取评分列表成功，共 {len(ratings)} 条评分")
        else:
            print_error(f"获取评分列表失败: {resp.status_code}")
    except Exception as e:
        print_error(f"获取评分列表异常: {e}")

    # 11. 收藏模板
    print_test("11. 收藏模板")
    try:
        resp = requests.post(f"{BASE_URL}/market/templates/{template_id}/favorite", headers=headers)
        if resp.status_code == 200:
            data = resp.json()
            print_success(f"收藏模板成功，收藏状态: {data['is_favorite']}")
        else:
            print_error(f"收藏模板失败: {resp.status_code}")
    except Exception as e:
        print_error(f"收藏模板异常: {e}")

    # 12. 获取用户收藏列表
    print_test("12. 获取用户收藏列表")
    try:
        resp = requests.get(f"{BASE_URL}/market/favorites?page=1&page_size=10", headers=headers)
        if resp.status_code == 200:
            data = resp.json()
            favorites = data['data']
            print_success(f"获取收藏列表成功，共 {len(favorites)} 个收藏")
        else:
            print_error(f"获取收藏列表失败: {resp.status_code}")
    except Exception as e:
        print_error(f"获取收藏列表异常: {e}")

    # 13. 获取我创建的模板
    print_test("13. 获取我创建的模板")
    try:
        resp = requests.get(f"{BASE_URL}/market/my-templates?page=1&page_size=10", headers=headers)
        if resp.status_code == 200:
            data = resp.json()
            my_templates = data['data']
            print_success(f"获取我的模板成功，共 {len(my_templates)} 个模板")
        else:
            print_error(f"获取我的模板失败: {resp.status_code}")
    except Exception as e:
        print_error(f"获取我的模板异常: {e}")

# 14. 获取热门标签
print_test("14. 获取热门标签")
try:
    resp = requests.get(f"{BASE_URL}/market/tags?limit=20", headers=headers)
    if resp.status_code == 200:
        data = resp.json()['data']
        print_success(f"获取热门标签成功，共 {len(data)} 个标签")
        if data:
            print_info(f"  - 前3个标签: {', '.join([t['name'] for t in data[:3]])}")
    else:
        print_error(f"获取热门标签失败: {resp.status_code}")
except Exception as e:
    print_error(f"获取热门标签异常: {e}")

# 15. 获取分类列表
print_test("15. 获取分类列表")
try:
    resp = requests.get(f"{BASE_URL}/market/categories", headers=headers)
    if resp.status_code == 200:
        data = resp.json()['data']
        print_success(f"获取分类列表成功，共 {len(data)} 个分类")
        for cat in data[:3]:
            print_info(f"  - {cat['name']}: {cat['count']} 个模板")
    else:
        print_error(f"获取分类列表失败: {resp.status_code}")
except Exception as e:
    print_error(f"获取分类列表异常: {e}")

# 16. 获取市场统计
print_test("16. 获取市场统计")
try:
    resp = requests.get(f"{BASE_URL}/market/stats", headers=headers)
    if resp.status_code == 200:
        data = resp.json()['data']
        print_success("获取市场统计成功")
        print_info(f"  - 总模板数: {data.get('total_templates', 'N/A')}")
        print_info(f"  - 总下载数: {data.get('total_downloads', 'N/A')}")
        print_info(f"  - 本周新增: {data.get('new_this_week', 'N/A')}")
    else:
        print_error(f"获取市场统计失败: {resp.status_code}")
except Exception as e:
    print_error(f"获取市场统计异常: {e}")

# 17. 按分类搜索模板
print_test("17. 按分类搜索模板")
try:
    resp = requests.get(f"{BASE_URL}/market/templates?category=user&page=1&page_size=5", headers=headers)
    if resp.status_code == 200:
        data = resp.json()
        templates = data['data']
        print_success(f"按分类搜索成功，找到 {len(templates)} 个模板")
    else:
        print_error(f"按分类搜索失败: {resp.status_code}")
except Exception as e:
    print_error(f"按分类搜索异常: {e}")

# 18. 按关键词搜索模板
print_test("18. 按关键词搜索模板")
try:
    resp = requests.get(f"{BASE_URL}/market/templates?search=测试&page=1&page_size=5", headers=headers)
    if resp.status_code == 200:
        data = resp.json()
        templates = data['data']
        print_success(f"按关键词搜索成功，找到 {len(templates)} 个模板")
    else:
        print_error(f"按关键词搜索失败: {resp.status_code}")
except Exception as e:
    print_error(f"按关键词搜索异常: {e}")

# 19. 按下载量排序
print_test("19. 按下载量排序模板")
try:
    resp = requests.get(f"{BASE_URL}/market/templates?sort_by=downloads&page=1&page_size=5", headers=headers)
    if resp.status_code == 200:
        data = resp.json()
        templates = data['data']
        print_success(f"按下载量排序成功，获得 {len(templates)} 个模板")
        if templates:
            print_info(f"  - 第一个模板下载量: {templates[0].get('downloads', 0)}")
    else:
        print_error(f"按下载量排序失败: {resp.status_code}")
except Exception as e:
    print_error(f"按下载量排序异常: {e}")

# 20. 按评分排序
print_test("20. 按评分排序模板")
try:
    resp = requests.get(f"{BASE_URL}/market/templates?sort_by=rating&page=1&page_size=5", headers=headers)
    if resp.status_code == 200:
        data = resp.json()
        templates = data['data']
        print_success(f"按评分排序成功，获得 {len(templates)} 个模板")
        if templates:
            print_info(f"  - 第一个模板评分: {templates[0].get('rating', 0)}")
    else:
        print_error(f"按评分排序失败: {resp.status_code}")
except Exception as e:
    print_error(f"按评分排序异常: {e}")

print(f"\n{Colors.BLUE}{'='*60}")
print("测试完成！")
print(f"{'='*60}{Colors.END}")

# 保存测试数据ID用于清理
if template_id:
    with open('test_data_ids.json', 'w') as f:
        json.dump({
            'user_id': user_id,
            'template_id': template_id,
            'username': test_user['username'],
            'email': test_user['email']
        }, f)
    print_info(f"测试数据已保存到 test_data_ids.json")
