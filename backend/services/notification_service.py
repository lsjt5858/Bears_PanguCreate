"""
通知服务
处理通知的创建、查询和管理
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from typing import Optional, List, Tuple
from models.notification import Notification
from extensions import db


class NotificationService:
    """通知服务类"""
    
    # 通知类型常量
    TYPE_INFO = 'info'
    TYPE_SUCCESS = 'success'
    TYPE_WARNING = 'warning'
    TYPE_ERROR = 'error'
    TYPE_SYSTEM = 'system'
    
    def create_notification(
        self,
        user_id: int,
        title: str,
        message: str = None,
        notification_type: str = TYPE_INFO,
        resource_type: str = None,
        resource_id: str = None
    ) -> Notification:
        """创建通知"""
        notification = Notification(
            user_id=user_id,
            title=title,
            message=message,
            type=notification_type,
            resource_type=resource_type,
            resource_id=resource_id
        )
        notification.save()
        return notification
    
    def get_notifications(
        self,
        user_id: int,
        unread_only: bool = False,
        page: int = 1,
        page_size: int = 20
    ) -> Tuple[List[Notification], int]:
        """获取用户通知列表"""
        return Notification.get_user_notifications(
            user_id=user_id,
            unread_only=unread_only,
            page=page,
            page_size=page_size
        )
    
    def get_notification(self, notification_id: str, user_id: int) -> Optional[Notification]:
        """获取单个通知"""
        notification = Notification.find_by_uuid(notification_id)
        if notification and notification.user_id == user_id:
            return notification
        return None
    
    def mark_as_read(self, notification_id: str, user_id: int) -> Tuple[bool, str]:
        """标记通知为已读"""
        notification = self.get_notification(notification_id, user_id)
        if not notification:
            return False, '通知不存在'
        
        notification.mark_as_read()
        return True, '已标记为已读'
    
    def mark_all_as_read(self, user_id: int) -> int:
        """标记所有通知为已读，返回更新数量"""
        count = Notification.get_unread_count(user_id)
        Notification.mark_all_as_read(user_id)
        return count
    
    def get_unread_count(self, user_id: int) -> int:
        """获取未读通知数量"""
        return Notification.get_unread_count(user_id)
    
    def delete_notification(self, notification_id: str, user_id: int) -> Tuple[bool, str]:
        """删除通知"""
        notification = self.get_notification(notification_id, user_id)
        if not notification:
            return False, '通知不存在'
        
        notification.delete()
        return True, '通知已删除'
    
    def delete_all_read(self, user_id: int) -> int:
        """删除所有已读通知，返回删除数量"""
        count = Notification.query.filter_by(user_id=user_id, is_read=True).count()
        Notification.query.filter_by(user_id=user_id, is_read=True).delete()
        db.session.commit()
        return count
    
    # 便捷方法：发送不同类型的通知
    def notify_info(self, user_id: int, title: str, message: str = None, **kwargs):
        """发送信息通知"""
        return self.create_notification(user_id, title, message, self.TYPE_INFO, **kwargs)
    
    def notify_success(self, user_id: int, title: str, message: str = None, **kwargs):
        """发送成功通知"""
        return self.create_notification(user_id, title, message, self.TYPE_SUCCESS, **kwargs)
    
    def notify_warning(self, user_id: int, title: str, message: str = None, **kwargs):
        """发送警告通知"""
        return self.create_notification(user_id, title, message, self.TYPE_WARNING, **kwargs)
    
    def notify_error(self, user_id: int, title: str, message: str = None, **kwargs):
        """发送错误通知"""
        return self.create_notification(user_id, title, message, self.TYPE_ERROR, **kwargs)
    
    def notify_system(self, user_id: int, title: str, message: str = None, **kwargs):
        """发送系统通知"""
        return self.create_notification(user_id, title, message, self.TYPE_SYSTEM, **kwargs)
    
    # 业务场景通知
    def notify_task_completed(self, user_id: int, task_name: str, task_id: str):
        """通知任务完成"""
        return self.notify_success(
            user_id=user_id,
            title='任务执行完成',
            message=f'定时任务 "{task_name}" 已成功执行',
            resource_type='task',
            resource_id=task_id
        )
    
    def notify_task_failed(self, user_id: int, task_name: str, task_id: str, error: str):
        """通知任务失败"""
        return self.notify_error(
            user_id=user_id,
            title='任务执行失败',
            message=f'定时任务 "{task_name}" 执行失败: {error}',
            resource_type='task',
            resource_id=task_id
        )
    
    def notify_datasource_connected(self, user_id: int, ds_name: str, ds_id: str):
        """通知数据源连接成功"""
        return self.notify_success(
            user_id=user_id,
            title='数据源连接成功',
            message=f'数据源 "{ds_name}" 连接测试通过',
            resource_type='datasource',
            resource_id=ds_id
        )
    
    def notify_datasource_failed(self, user_id: int, ds_name: str, ds_id: str, error: str):
        """通知数据源连接失败"""
        return self.notify_error(
            user_id=user_id,
            title='数据源连接失败',
            message=f'数据源 "{ds_name}" 连接失败: {error}',
            resource_type='datasource',
            resource_id=ds_id
        )


# 单例
notification_service = NotificationService()
