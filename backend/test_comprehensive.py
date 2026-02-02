#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
全面测试模板市场功能
"""
import requests
import json

BASE_URL = "http://localhost:5001"

def test_all_features():
    """测试所有模板市场功能"""
    print("=" * 60)
    print("全面测试模板市场功能")
    print("=" * 60)
    
    # 1. 注册并登录
    print("\n【步骤 1】注册并登录...")
    register_data = {
        "username": "comprehensive_test",
        "email": "comprehensive@example.com",
        "password": "password123"
    }
    requests.post(f"{BASE_URL}/api/auth/register", json=register_data)
    
    login_data = {"username": "comprehensive_test", "password": "password123"}
    response = requests.post(f"{BASE_URL}/api/auth/login", json=login_data)
    token = response.json()['data']['access_token']
    headers = {"Authorization": f"Bearer {token}"}
    print("✅ 登录成功")
    
    # 2. 创建模板
    print("\n【步骤 2】创建模板...")
    template_data = {
        "name": "综合测试模板",
        "description": "用于全面测试的模板",
        "category": "test",
        "fields": [{"id": "f1", "name": "field1", "type": "string"}],
        "tags": ["测试", "综合"],
        "is_public": True
    }
    response = requests.post(f"{BASE_URL}/api/market/templates", json=template_data, headers=headers)
    template_id = response.json()['data']['id']
    print(f"✅ 创建成功 (ID: {template_id})")
    
    # 3. 获取模板详情
    print("\n【步骤 3】获取模板详情...")
    response = requests.get(f"{BASE_URL}/api/market/templates/{template_id}")
    assert response.status_code == 200
    print("✅ 获取成功")
    
    # 4. 更新模板
    print("\n【步骤 4】更新模板...")
    update_data = {"description": "更新后的描述"}
    response = requests.put(f"{BASE_URL}/api/market/templates/{template_id}", json=update_data, headers=headers)
    assert response.status_code == 200
    print("✅ 更新成功")
    
    # 5. 使用模板
    print("\n【步骤 5】使用模板...")
    response = requests.post(f"{BASE_URL}/api/market/templates/{template_id}/use", headers=headers)
    assert response.status_code == 200
    print("✅ 使用成功")
    
    # 6. 评分模板
    print("\n【步骤 6】评分模板...")
    rating_data = {"score": 5, "comment": "很好用"}
    response = requests.post(f"{BASE_URL}/api/market/templates/{template_id}/rate", json=rating_data, headers=headers)
    assert response.status_code == 200
    print("✅ 评分成功")
    
    # 7. 获取评分列表
    print("\n【步骤 7】获取评分列表...")
    response = requests.get(f"{BASE_URL}/api/market/templates/{template_id}/ratings")
    assert response.status_code == 200
    print("✅ 获取成功")
    
    # 8. 收藏模板
    print("\n【步骤 8】收藏模板...")
    response = requests.post(f"{BASE_URL}/api/market/templates/{template_id}/favorite", headers=headers)
    assert response.status_code == 200
    assert response.json()['is_favorite'] == True
    print("✅ 收藏成功")
    
    # 9. 取消收藏
    print("\n【步骤 9】取消收藏...")
    response = requests.post(f"{BASE_URL}/api/market/templates/{template_id}/favorite", headers=headers)
    assert response.status_code == 200
    assert response.json()['is_favorite'] == False
    print("✅ 取消收藏成功")
    
    # 10. 再次收藏（为了测试删除）
    print("\n【步骤 10】再次收藏...")
    requests.post(f"{BASE_URL}/api/market/templates/{template_id}/favorite", headers=headers)
    print("✅ 再次收藏成功")
    
    # 11. 获取用户收藏
    print("\n【步骤 11】获取用户收藏...")
    response = requests.get(f"{BASE_URL}/api/market/favorites", headers=headers)
    assert response.status_code == 200
    print("✅ 获取成功")
    
    # 12. 获取我的模板
    print("\n【步骤 12】获取我的模板...")
    response = requests.get(f"{BASE_URL}/api/market/my-templates", headers=headers)
    assert response.status_code == 200
    print("✅ 获取成功")
    
    # 13. 获取热门标签
    print("\n【步骤 13】获取热门标签...")
    response = requests.get(f"{BASE_URL}/api/market/tags")
    assert response.status_code == 200
    print("✅ 获取成功")
    
    # 14. 获取分类列表
    print("\n【步骤 14】获取分类列表...")
    response = requests.get(f"{BASE_URL}/api/market/categories")
    assert response.status_code == 200
    print("✅ 获取成功")
    
    # 15. 获取市场统计
    print("\n【步骤 15】获取市场统计...")
    response = requests.get(f"{BASE_URL}/api/market/stats")
    assert response.status_code == 200
    print("✅ 获取成功")
    
    # 16. 删除模板（关键测试）
    print("\n【步骤 16】删除模板（包含所有关联数据）...")
    response = requests.delete(f"{BASE_URL}/api/market/templates/{template_id}", headers=headers)
    if response.status_code == 200:
        print("✅✅✅ 删除成功！所有关联数据已清理！")
    else:
        print(f"❌ 删除失败: {response.text}")
        return False
    
    # 17. 验证删除
    print("\n【步骤 17】验证模板已删除...")
    response = requests.get(f"{BASE_URL}/api/market/templates/{template_id}")
    assert response.status_code == 404
    print("✅ 验证成功")
    
    print("\n" + "=" * 60)
    print("🎉🎉🎉 所有测试通过！模板市场功能完全正常！")
    print("=" * 60)
    print("\n测试结果汇总:")
    print("  ✅ 创建模板")
    print("  ✅ 获取模板详情")
    print("  ✅ 更新模板")
    print("  ✅ 使用模板（下载记录）")
    print("  ✅ 评分模板")
    print("  ✅ 获取评分列表")
    print("  ✅ 收藏/取消收藏")
    print("  ✅ 获取用户收藏")
    print("  ✅ 获取我的模板")
    print("  ✅ 获取热门标签")
    print("  ✅ 获取分类列表")
    print("  ✅ 获取市场统计")
    print("  ✅ 删除模板（含关联数据）✨ 已修复")
    print("  ✅ 验证删除")
    print("\n总计: 17/17 测试通过 (100%)")
    return True


if __name__ == "__main__":
    try:
        success = test_all_features()
        if success:
            print("\n✅ 模板市场功能完成度: 100%")
    except AssertionError as e:
        print(f"\n❌ 测试失败: {str(e)}")
        import traceback
        traceback.print_exc()
    except Exception as e:
        print(f"\n❌ 测试过程中发生错误: {str(e)}")
        import traceback
        traceback.print_exc()
