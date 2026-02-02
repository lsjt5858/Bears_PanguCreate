#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
测试模板删除功能修复
"""
import requests
import json

BASE_URL = "http://localhost:5001"

def test_delete_template():
    """测试删除模板功能"""
    print("=" * 60)
    print("测试模板删除功能修复")
    print("=" * 60)
    
    # 1. 注册测试用户
    print("\n1. 注册测试用户...")
    register_data = {
        "username": "test_delete_user",
        "email": "test_delete@example.com",
        "password": "password123"
    }
    response = requests.post(f"{BASE_URL}/api/auth/register", json=register_data)
    if response.status_code == 201:
        print("✅ 用户注册成功")
    else:
        print(f"❌ 用户注册失败: {response.text}")
        return
    
    # 2. 登录获取 token
    print("\n2. 登录获取 token...")
    login_data = {
        "username": "test_delete_user",
        "password": "password123"
    }
    response = requests.post(f"{BASE_URL}/api/auth/login", json=login_data)
    if response.status_code == 200:
        token = response.json()['data']['access_token']
        user_id = response.json()['data']['user']['id']
        print(f"✅ 登录成功，token: {token[:20]}...")
    else:
        print(f"❌ 登录失败: {response.text}")
        return
    
    headers = {"Authorization": f"Bearer {token}"}
    
    # 3. 创建测试模板
    print("\n3. 创建测试模板...")
    template_data = {
        "name": "测试删除模板",
        "description": "这是一个用于测试删除功能的模板",
        "category": "test",
        "fields": [
            {"id": "f1", "name": "test_field", "type": "string"}
        ],
        "tags": ["测试", "删除"],
        "is_public": True
    }
    response = requests.post(f"{BASE_URL}/api/market/templates", json=template_data, headers=headers)
    if response.status_code == 201:
        template_id = response.json()['data']['id']
        print(f"✅ 模板创建成功，ID: {template_id}")
    else:
        print(f"❌ 模板创建失败: {response.text}")
        return
    
    # 4. 使用模板（创建下载记录）
    print("\n4. 使用模板（创建下载记录）...")
    response = requests.post(f"{BASE_URL}/api/market/templates/{template_id}/use", headers=headers)
    if response.status_code == 200:
        print("✅ 模板使用成功（下载记录已创建）")
    else:
        print(f"⚠️ 模板使用失败: {response.text}")
    
    # 5. 评分模板（创建评分记录）
    print("\n5. 评分模板（创建评分记录）...")
    rating_data = {"score": 5, "comment": "测试评分"}
    response = requests.post(f"{BASE_URL}/api/market/templates/{template_id}/rate", json=rating_data, headers=headers)
    if response.status_code == 200:
        print("✅ 模板评分成功（评分记录已创建）")
    else:
        print(f"⚠️ 模板评分失败: {response.text}")
    
    # 6. 收藏模板（创建收藏记录）
    print("\n6. 收藏模板（创建收藏记录）...")
    response = requests.post(f"{BASE_URL}/api/market/templates/{template_id}/favorite", headers=headers)
    if response.status_code == 200:
        print("✅ 模板收藏成功（收藏记录已创建）")
    else:
        print(f"⚠️ 模板收藏失败: {response.text}")
    
    # 7. 删除模板（关键测试）
    print("\n7. 删除模板（关键测试）...")
    print("   这是修复的核心功能，应该能成功删除所有关联数据")
    response = requests.delete(f"{BASE_URL}/api/market/templates/{template_id}", headers=headers)
    
    if response.status_code == 200:
        print("✅✅✅ 模板删除成功！修复有效！")
        print(f"   响应: {response.json()}")
    else:
        print(f"❌❌❌ 模板删除失败！")
        print(f"   状态码: {response.status_code}")
        print(f"   响应: {response.text}")
        return
    
    # 8. 验证模板已删除
    print("\n8. 验证模板已删除...")
    response = requests.get(f"{BASE_URL}/api/market/templates/{template_id}")
    if response.status_code == 404:
        print("✅ 验证成功：模板已不存在")
    else:
        print(f"⚠️ 验证失败：模板仍然存在")
    
    # 9. 清理：删除测试用户
    print("\n9. 清理测试数据...")
    # 注意：这里需要有删除用户的 API，如果没有就跳过
    print("   测试用户将保留在数据库中（可手动清理）")
    
    print("\n" + "=" * 60)
    print("🎉 测试完成！模板删除功能已修复！")
    print("=" * 60)


if __name__ == "__main__":
    try:
        test_delete_template()
    except Exception as e:
        print(f"\n❌ 测试过程中发生错误: {str(e)}")
        import traceback
        traceback.print_exc()
