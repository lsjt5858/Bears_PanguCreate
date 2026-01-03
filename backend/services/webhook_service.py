"""
Webhook 服务
处理 Webhook 的创建、管理和触发
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import hmac
import hashlib
import json
import requests
from typing import Optional, List, Tuple
from datetime import datetime
from models.webhook import Webhook
from extensions import db


class WebhookService:
    """Webhook 服务类"""
    
    # 支持的事件类型
    EVENTS = {
        'task_completed': '任务执行完成',
        'task_failed': '任务执行失败',
        'data_generated': '数据生成完成',
        'datasource_connected': '数据源连接成功',
        'datasource_failed': '数据源连接失败',
        'template_created': '模板创建',
        'api_key_created': 'API密钥创建',
        'api_key_used': 'API密钥使用'
    }
    
    def get_supported_events(self) -> dict:
        """获取支持的事件类型"""
        return self.EVENTS
    
    def create_webhook(
        self,
        user_id: int,
        name: str,
        url: str,
        events: list,
        description: str = None,
        method: str = 'POST',
        headers: dict = None,
        secret: str = None
    ) -> Tuple[Optional[Webhook], Optional[str]]:
        """创建 Webhook"""
        # 验证事件类型
        for event in events:
            if event not in self.EVENTS:
                return None, f'不支持的事件类型: {event}'
        
        # 验证 URL
        if not url.startswith(('http://', 'https://')):
            return None, 'URL 必须以 http:// 或 https:// 开头'
        
        webhook = Webhook(
            user_id=user_id,
            name=name,
            url=url,
            description=description,
            method=method.upper(),
            secret=secret
        )
        webhook.set_events(events)
        if headers:
            webhook.set_headers(headers)
        
        webhook.save()
        return webhook, None
    
    def get_webhooks(self, user_id: int, page: int = 1, page_size: int = 20) -> Tuple[List[Webhook], int]:
        """获取用户的 Webhook 列表"""
        query = Webhook.query.filter_by(user_id=user_id).order_by(Webhook.created_at.desc())
        total = query.count()
        webhooks = query.offset((page - 1) * page_size).limit(page_size).all()
        return webhooks, total
    
    def get_webhook(self, webhook_id: str, user_id: int) -> Optional[Webhook]:
        """获取单个 Webhook"""
        webhook = Webhook.find_by_uuid(webhook_id)
        if webhook and webhook.user_id == user_id:
            return webhook
        return None
    
    def update_webhook(
        self,
        webhook_id: str,
        user_id: int,
        **kwargs
    ) -> Tuple[Optional[Webhook], Optional[str]]:
        """更新 Webhook"""
        webhook = self.get_webhook(webhook_id, user_id)
        if not webhook:
            return None, 'Webhook 不存在'
        
        # 更新字段
        if 'name' in kwargs:
            webhook.name = kwargs['name']
        if 'url' in kwargs:
            url = kwargs['url']
            if not url.startswith(('http://', 'https://')):
                return None, 'URL 必须以 http:// 或 https:// 开头'
            webhook.url = url
        if 'description' in kwargs:
            webhook.description = kwargs['description']
        if 'events' in kwargs:
            events = kwargs['events']
            for event in events:
                if event not in self.EVENTS:
                    return None, f'不支持的事件类型: {event}'
            webhook.set_events(events)
        if 'method' in kwargs:
            webhook.method = kwargs['method'].upper()
        if 'headers' in kwargs:
            webhook.set_headers(kwargs['headers'])
        if 'secret' in kwargs:
            webhook.secret = kwargs['secret']
        if 'is_active' in kwargs:
            webhook.is_active = kwargs['is_active']
        
        webhook.updated_at = datetime.utcnow()
        db.session.commit()
        return webhook, None
    
    def delete_webhook(self, webhook_id: str, user_id: int) -> Tuple[bool, str]:
        """删除 Webhook"""
        webhook = self.get_webhook(webhook_id, user_id)
        if not webhook:
            return False, 'Webhook 不存在'
        
        webhook.delete()
        return True, 'Webhook 已删除'
    
    def toggle_webhook(self, webhook_id: str, user_id: int) -> Tuple[Optional[Webhook], Optional[str]]:
        """切换 Webhook 状态"""
        webhook = self.get_webhook(webhook_id, user_id)
        if not webhook:
            return None, 'Webhook 不存在'
        
        webhook.is_active = not webhook.is_active
        webhook.updated_at = datetime.utcnow()
        db.session.commit()
        return webhook, None
    
    def _generate_signature(self, payload: str, secret: str) -> str:
        """生成签名"""
        return hmac.new(
            secret.encode('utf-8'),
            payload.encode('utf-8'),
            hashlib.sha256
        ).hexdigest()
    
    def trigger_webhook(self, webhook: Webhook, payload: dict) -> Tuple[bool, str]:
        """触发单个 Webhook"""
        try:
            headers = webhook.get_headers()
            headers['Content-Type'] = 'application/json'
            
            payload_str = json.dumps(payload)
            
            # 添加签名
            if webhook.secret:
                signature = self._generate_signature(payload_str, webhook.secret)
                headers['X-Webhook-Signature'] = signature
            
            # 添加时间戳
            headers['X-Webhook-Timestamp'] = datetime.utcnow().isoformat()
            
            # 发送请求
            if webhook.method == 'GET':
                response = requests.get(webhook.url, headers=headers, params=payload, timeout=10)
            else:
                response = requests.post(webhook.url, headers=headers, data=payload_str, timeout=10)
            
            success = 200 <= response.status_code < 300
            webhook.record_trigger(success, None if success else f'HTTP {response.status_code}')
            
            return success, f'HTTP {response.status_code}'
        except requests.Timeout:
            webhook.record_trigger(False, '请求超时')
            return False, '请求超时'
        except requests.RequestException as e:
            error = str(e)
            webhook.record_trigger(False, error)
            return False, error
    
    def trigger_event(self, user_id: int, event: str, payload: dict) -> List[dict]:
        """触发事件，通知所有相关的 Webhook"""
        webhooks = Webhook.get_active_webhooks_for_event(user_id, event)
        results = []
        
        # 添加事件信息到 payload
        event_payload = {
            'event': event,
            'event_name': self.EVENTS.get(event, event),
            'timestamp': datetime.utcnow().isoformat(),
            'data': payload
        }
        
        for webhook in webhooks:
            success, message = self.trigger_webhook(webhook, event_payload)
            results.append({
                'webhook_id': webhook.uuid,
                'webhook_name': webhook.name,
                'success': success,
                'message': message
            })
        
        return results
    
    def test_webhook(self, webhook_id: str, user_id: int) -> Tuple[bool, str]:
        """测试 Webhook"""
        webhook = self.get_webhook(webhook_id, user_id)
        if not webhook:
            return False, 'Webhook 不存在'
        
        test_payload = {
            'event': 'test',
            'event_name': '测试事件',
            'timestamp': datetime.utcnow().isoformat(),
            'data': {
                'message': '这是一条测试消息',
                'webhook_name': webhook.name
            }
        }
        
        return self.trigger_webhook(webhook, test_payload)


# 单例
webhook_service = WebhookService()
