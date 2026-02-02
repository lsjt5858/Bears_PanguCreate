#!/usr/bin/env python3
"""
测试所有API端点是否正常工作
"""
import requests
import json

BASE_URL = "http://localhost:5001/api"

def test_health():
    """测试健康检查"""
    print("🔍 测试健康检查...")
    response = requests.get(f"{BASE_URL}/health")
    print(f"   状态码: {response.status_code}")
    print(f"   响应: {response.json()}")
    return response.status_code == 200

def test_login():
    """测试登录并获取token"""
    print("\n🔍 测试登录...")
    response = requests.post(
        f"{BASE_URL}/auth/login",
        json={"username": "admin", "password": "admin123"},
        headers={"Content-Type": "application/json"}
    )
    print(f"   状态码: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        token = data['data']['access_token']
        print(f"   ✅ 登录成功，获取到 token")
        return token
    else:
        print(f"   ❌ 登录失败: {response.text}")
        return None

def test_history(token):
    """测试历史记录API"""
    print("\n🔍 测试历史记录API...")
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{BASE_URL}/history", headers=headers)
    print(f"   状态码: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"   ✅ 历史记录数量: {data['pagination']['total']}")
        return True
    else:
        print(f"   ❌ 失败: {response.text}")
        return False

def test_datasources(token):
    """测试数据源API"""
    print("\n🔍 测试数据源API...")
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{BASE_URL}/datasources", headers=headers)
    print(f"   状态码: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"   ✅ 数据源数量: {len(data['data'])}")
        return True
    else:
        print(f"   ❌ 失败: {response.text}")
        return False

def test_relation(token):
    """测试关联数据生成API"""
    print("\n🔍 测试关联数据生成API...")
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    # 简单的测试数据
    test_data = {
        "tables": [
            {
                "id": "t1",
                "name": "users",
                "fields": [
                    {"id": "f1", "name": "id", "type": "uuid"},
                    {"id": "f2", "name": "name", "type": "chineseName"}
                ],
                "count": 5
            },
            {
                "id": "t2",
                "name": "orders",
                "fields": [
                    {"id": "f3", "name": "id", "type": "uuid"},
                    {"id": "f4", "name": "user_id", "type": "uuid"}
                ],
                "count": 10
            }
        ],
        "relations": [
            {
                "id": "r1",
                "sourceTable": "users",
                "sourceColumn": "id",
                "targetTable": "orders",
                "targetColumn": "user_id",
                "relationType": "one-to-many"
            }
        ]
    }
    
    response = requests.post(
        f"{BASE_URL}/relation/generate",
        headers=headers,
        json=test_data
    )
    print(f"   状态码: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"   ✅ 生成成功")
        print(f"   - users 表: {len(data['data']['users'])} 条")
        print(f"   - orders 表: {len(data['data']['orders'])} 条")
        return True
    else:
        print(f"   ❌ 失败: {response.text}")
        return False

def test_api_keys(token):
    """测试API密钥API"""
    print("\n🔍 测试API密钥API...")
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{BASE_URL}/api-keys", headers=headers)
    print(f"   状态码: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"   ✅ API密钥数量: {len(data['data'])}")
        return True
    else:
        print(f"   ❌ 失败: {response.text}")
        return False

def test_scheduled_tasks(token):
    """测试定时任务API"""
    print("\n🔍 测试定时任务API...")
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{BASE_URL}/scheduled-tasks", headers=headers)
    print(f"   状态码: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"   ✅ 定时任务数量: {len(data['data'])}")
        return True
    else:
        print(f"   ❌ 失败: {response.text}")
        return False

def main():
    print("=" * 60)
    print("🚀 Bears PanguCreate API 端点测试")
    print("=" * 60)
    
    results = {}
    
    # 1. 健康检查
    results['health'] = test_health()
    
    # 2. 登录获取token
    token = test_login()
    if not token:
        print("\n❌ 无法获取token，后续测试跳过")
        return
    
    # 3. 测试各个API
    results['history'] = test_history(token)
    results['datasources'] = test_datasources(token)
    results['relation'] = test_relation(token)
    results['api_keys'] = test_api_keys(token)
    results['scheduled_tasks'] = test_scheduled_tasks(token)
    
    # 总结
    print("\n" + "=" * 60)
    print("📊 测试结果总结")
    print("=" * 60)
    passed = sum(1 for v in results.values() if v)
    total = len(results)
    print(f"✅ 通过: {passed}/{total}")
    print(f"❌ 失败: {total - passed}/{total}")
    
    for name, result in results.items():
        status = "✅" if result else "❌"
        print(f"   {status} {name}")
    
    print("=" * 60)

if __name__ == "__main__":
    main()
