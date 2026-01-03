"""
调度服务
管理定时任务的创建、执行、调度
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import json
import time
from typing import Optional, List, Tuple, Dict, Any
from datetime import datetime, timedelta
from croniter import croniter

from extensions import db
from models.scheduled_task import ScheduledTask, TaskExecutionLog


class SchedulerService:
    """调度服务"""
    
    def __init__(self):
        self._scheduler = None
    
    def init_scheduler(self, app):
        """初始化调度器"""
        # 防止 Flask 在 Debug 模式下启动两个调度器实例
        if app.debug and os.environ.get('WERKZEUG_RUN_MAIN') != 'true':
            return

        if self._scheduler and self._scheduler.running:
            return

        from apscheduler.schedulers.background import BackgroundScheduler
        from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
        from apscheduler.executors.pool import ThreadPoolExecutor
        
        print("Initializing Scheduler...")
        jobstores = {
            'default': SQLAlchemyJobStore(url=app.config['SQLALCHEMY_DATABASE_URI'])
        }
        executors = {
            'default': ThreadPoolExecutor(10)
        }
        job_defaults = {
            'coalesce': True,
            'max_instances': 1,
            'misfire_grace_time': 60
        }
        
        self._scheduler = BackgroundScheduler(
            jobstores=jobstores,
            executors=executors,
            job_defaults=job_defaults,
            timezone='Asia/Shanghai'
        )
        
        # 启动调度器
        self._scheduler.start()
        print("Scheduler started successfully.")
        
        # 加载已有任务
        with app.app_context():
            self._load_existing_tasks(app)
    
    def _load_existing_tasks(self, app):
        """加载已有的活跃任务"""
        tasks = ScheduledTask.find_active_tasks()
        print(f"Found {len(tasks)} active tasks to schedule.")
        for task in tasks:
            self._add_job(task, app)
    
    def _add_job(self, task: ScheduledTask, app=None):
        """添加任务到调度器"""
        if not self._scheduler:
            return
        
        from apscheduler.triggers.cron import CronTrigger
        
        try:
            # 解析 cron 表达式
            trigger = CronTrigger.from_crontab(task.cron_expression, timezone=task.timezone)
            
            # 添加任务
            self._scheduler.add_job(
                func=self._execute_task,
                trigger=trigger,
                id=f'task_{task.uuid}',
                args=[task.uuid, app],
                replace_existing=True
            )
            
            # 更新下次执行时间
            task.next_run_at = trigger.get_next_fire_time(None, datetime.now())
            db.session.commit()
            
        except Exception as e:
            print(f"Failed to add job {task.uuid}: {e}")
    
    def _remove_job(self, task_uuid: str):
        """从调度器移除任务"""
        if not self._scheduler:
            return
        
        job_id = f'task_{task_uuid}'
        try:
            self._scheduler.remove_job(job_id)
        except:
            pass
    
    def _execute_task(self, task_uuid: str, app=None):
        """执行任务"""
        print(f"Executing task {task_uuid}...")
        if app:
            with app.app_context():
                self._do_execute_task(task_uuid)
        else:
            self._do_execute_task(task_uuid)
    
    def _do_execute_task(self, task_uuid: str):
        """实际执行任务"""
        from services.data_generator_service import data_generator_service
        
        task = ScheduledTask.find_by_uuid(task_uuid)
        if not task:
            print(f"Task {task_uuid} not found.")
            return
        if not task.is_active:
            print(f"Task {task_uuid} is not active (status: {task.status}).")
            return
        
        # 创建执行日志
        log = TaskExecutionLog(
            task_id=task.id,
            started_at=datetime.utcnow(),
            status='running'
        )
        log.save()
        
        start_time = time.time()
        
        try:
            # 生成数据
            fields = task.fields
            count = task.row_count
            
            result = data_generator_service.generate_data(fields, count)
            
            # 计算统计
            duration_ms = int((time.time() - start_time) * 1000)
            data_size = len(json.dumps(result, ensure_ascii=False).encode('utf-8'))
            
            # 处理输出
            output_status, output_message = self._handle_output(task, result)
            
            # 更新日志
            log.finished_at = datetime.utcnow()
            log.duration_ms = duration_ms
            log.status = 'success'
            log.rows_generated = len(result)
            log.data_size_bytes = data_size
            log.output_status = output_status
            log.output_message = output_message
            log.save()
            
            # 更新任务状态
            task.record_run(success=True)
            
            # 更新下次执行时间
            self._update_next_run(task)
            
        except Exception as e:
            # 记录错误
            log.finished_at = datetime.utcnow()
            log.duration_ms = int((time.time() - start_time) * 1000)
            log.status = 'failed'
            log.error_message = str(e)
            log.save()
            
            task.record_run(success=False, error=str(e))
    
    def _handle_output(self, task: ScheduledTask, data: list) -> Tuple[str, str]:
        """处理任务输出"""
        output_type = task.output_type
        output_config = task.output_settings
        
        if output_type == 'none':
            return 'skipped', '无输出配置'
        
        if output_type == 'webhook':
            return self._send_webhook(output_config, data, task)
        
        # 其他输出类型可以后续扩展
        return 'skipped', f'不支持的输出类型: {output_type}'
    
    def _send_webhook(self, config: dict, data: list, task: ScheduledTask) -> Tuple[str, str]:
        """发送 Webhook"""
        import requests
        
        url = config.get('url')
        if not url:
            return 'failed', 'Webhook URL 未配置'
        
        try:
            headers = config.get('headers', {})
            headers['Content-Type'] = 'application/json'
            
            payload = {
                'task_id': task.uuid,
                'task_name': task.name,
                'data': data,
                'count': len(data),
                'timestamp': datetime.utcnow().isoformat()
            }
            
            response = requests.post(url, json=payload, headers=headers, timeout=30)
            
            if response.status_code < 400:
                return 'success', f'Webhook 发送成功: {response.status_code}'
            else:
                return 'failed', f'Webhook 返回错误: {response.status_code}'
                
        except Exception as e:
            return 'failed', f'Webhook 发送失败: {str(e)}'
    
    def _update_next_run(self, task: ScheduledTask):
        """更新下次执行时间"""
        try:
            cron = croniter(task.cron_expression, datetime.now())
            task.next_run_at = cron.get_next(datetime)
            db.session.commit()
        except:
            pass
    
    def create_task(
        self,
        user_id: int,
        name: str,
        cron_expression: str,
        fields: list,
        row_count: int = 100,
        description: str = None,
        project_id: int = None,
        template_id: str = None,
        export_format: str = 'json',
        table_name: str = None,
        output_type: str = 'none',
        output_config: dict = None,
        timezone: str = 'Asia/Shanghai',
        max_runs: int = None,
        expires_at: datetime = None,
        app=None
    ) -> Tuple[Optional[ScheduledTask], Optional[str]]:
        """创建定时任务"""
        # 验证 cron 表达式
        if not self._validate_cron(cron_expression):
            return None, "无效的 Cron 表达式"
        
        # 创建任务
        task = ScheduledTask(
            user_id=user_id,
            project_id=project_id,
            template_id=template_id,
            name=name,
            description=description,
            cron_expression=cron_expression,
            timezone=timezone,
            row_count=row_count,
            export_format=export_format,
            table_name=table_name,
            output_type=output_type,
            max_runs=max_runs,
            expires_at=expires_at,
            status='active',
            is_enabled=True
        )
        task.fields = fields
        if output_config:
            task.output_settings = output_config
        
        # 计算下次执行时间
        try:
            cron = croniter(cron_expression, datetime.now())
            task.next_run_at = cron.get_next(datetime)
        except:
            pass
        
        task.save()
        
        # 添加到调度器
        if app:
            self._add_job(task, app)
        
        return task, None
    
    def _validate_cron(self, expression: str) -> bool:
        """验证 Cron 表达式"""
        try:
            croniter(expression)
            return True
        except:
            return False
    
    def update_task(
        self,
        task_id: str,
        user_id: int,
        app=None,
        **kwargs
    ) -> Tuple[Optional[ScheduledTask], Optional[str]]:
        """更新任务"""
        task = ScheduledTask.find_by_uuid(task_id)
        if not task:
            return None, "任务不存在"
        
        if task.user_id != user_id:
            return None, "无权修改此任务"
        
        # 更新字段
        if 'name' in kwargs:
            task.name = kwargs['name']
        if 'description' in kwargs:
            task.description = kwargs['description']
        if 'cron_expression' in kwargs:
            if not self._validate_cron(kwargs['cron_expression']):
                return None, "无效的 Cron 表达式"
            task.cron_expression = kwargs['cron_expression']
        if 'timezone' in kwargs:
            task.timezone = kwargs['timezone']
        if 'fields' in kwargs:
            task.fields = kwargs['fields']
        if 'row_count' in kwargs:
            task.row_count = kwargs['row_count']
        if 'export_format' in kwargs:
            task.export_format = kwargs['export_format']
        if 'table_name' in kwargs:
            task.table_name = kwargs['table_name']
        if 'output_type' in kwargs:
            task.output_type = kwargs['output_type']
        if 'output_config' in kwargs:
            task.output_settings = kwargs['output_config']
        if 'max_runs' in kwargs:
            task.max_runs = kwargs['max_runs']
        if 'expires_at' in kwargs:
            task.expires_at = kwargs['expires_at']
        
        # 更新下次执行时间
        try:
            cron = croniter(task.cron_expression, datetime.now())
            task.next_run_at = cron.get_next(datetime)
        except:
            pass
        
        task.save()
        
        # 更新调度器中的任务
        if task.is_active and app:
            self._add_job(task, app)
        else:
            self._remove_job(task.uuid)
        
        return task, None
    
    def delete_task(self, task_id: str, user_id: int) -> Tuple[bool, Optional[str]]:
        """删除任务"""
        task = ScheduledTask.find_by_uuid(task_id)
        if not task:
            return False, "任务不存在"
        
        if task.user_id != user_id:
            return False, "无权删除此任务"
        
        # 从调度器移除
        self._remove_job(task.uuid)
        
        # 删除执行日志
        TaskExecutionLog.query.filter_by(task_id=task.id).delete()
        
        task.delete()
        return True, None
    
    def pause_task(self, task_id: str, user_id: int) -> Tuple[bool, Optional[str]]:
        """暂停任务"""
        task = ScheduledTask.find_by_uuid(task_id)
        if not task:
            return False, "任务不存在"
        
        if task.user_id != user_id:
            return False, "无权操作此任务"
        
        task.status = 'paused'
        task.is_enabled = False
        task.save()
        
        self._remove_job(task.uuid)
        return True, None
    
    def resume_task(self, task_id: str, user_id: int, app=None) -> Tuple[bool, Optional[str]]:
        """恢复任务"""
        task = ScheduledTask.find_by_uuid(task_id)
        if not task:
            return False, "任务不存在"
        
        if task.user_id != user_id:
            return False, "无权操作此任务"
        
        task.status = 'active'
        task.is_enabled = True
        
        # 更新下次执行时间
        try:
            cron = croniter(task.cron_expression, datetime.now())
            task.next_run_at = cron.get_next(datetime)
        except:
            pass
        
        task.save()
        
        if app:
            self._add_job(task, app)
        
        return True, None
    
    def run_task_now(self, task_id: str, user_id: int) -> Tuple[bool, Optional[str]]:
        """立即执行任务"""
        task = ScheduledTask.find_by_uuid(task_id)
        if not task:
            return False, "任务不存在"
        
        if task.user_id != user_id:
            return False, "无权操作此任务"
        
        # 直接执行
        self._do_execute_task(task.uuid)
        return True, None
    
    def get_task(self, task_id: str, user_id: int) -> Optional[ScheduledTask]:
        """获取任务详情"""
        task = ScheduledTask.find_by_uuid(task_id)
        if not task or task.user_id != user_id:
            return None
        return task
    
    def list_tasks(
        self,
        user_id: int,
        project_id: int = None,
        status: str = None,
        page: int = 1,
        page_size: int = 20
    ) -> Tuple[List[ScheduledTask], int]:
        """获取任务列表"""
        query = ScheduledTask.query.filter_by(user_id=user_id)
        
        if project_id:
            query = query.filter_by(project_id=project_id)
        
        if status:
            query = query.filter_by(status=status)
        
        total = query.count()
        
        offset = (page - 1) * page_size
        tasks = query.order_by(ScheduledTask.created_at.desc())\
            .limit(page_size).offset(offset).all()
        
        return tasks, total
    
    def get_execution_logs(
        self,
        task_id: str,
        user_id: int,
        page: int = 1,
        page_size: int = 20
    ) -> Tuple[List[Dict], int]:
        """获取执行日志"""
        task = ScheduledTask.find_by_uuid(task_id)
        if not task or task.user_id != user_id:
            return [], 0
        
        query = TaskExecutionLog.query.filter_by(task_id=task.id)
        total = query.count()
        
        offset = (page - 1) * page_size
        logs = query.order_by(TaskExecutionLog.created_at.desc())\
            .limit(page_size).offset(offset).all()
        
        return [log.to_dict() for log in logs], total
    
    def get_task_stats(self, user_id: int) -> Dict[str, Any]:
        """获取任务统计"""
        tasks = ScheduledTask.query.filter_by(user_id=user_id).all()
        
        total = len(tasks)
        active = sum(1 for t in tasks if t.status == 'active' and t.is_enabled)
        paused = sum(1 for t in tasks if t.status == 'paused' or not t.is_enabled)
        error = sum(1 for t in tasks if t.status == 'error')
        
        total_runs = sum(t.run_count for t in tasks)
        total_success = sum(t.success_count for t in tasks)
        total_fail = sum(t.fail_count for t in tasks)
        
        return {
            'total_tasks': total,
            'active_tasks': active,
            'paused_tasks': paused,
            'error_tasks': error,
            'total_runs': total_runs,
            'total_success': total_success,
            'total_fail': total_fail,
            'success_rate': round(total_success / total_runs * 100, 1) if total_runs > 0 else 0
        }
    
    def parse_cron_description(self, expression: str) -> str:
        """解析 Cron 表达式为人类可读描述"""
        common_patterns = {
            '* * * * *': '每分钟',
            '0 * * * *': '每小时',
            '0 0 * * *': '每天 00:00',
            '0 8 * * *': '每天 08:00',
            '0 0 * * 0': '每周日 00:00',
            '0 0 * * 1': '每周一 00:00',
            '0 0 1 * *': '每月 1 日 00:00',
            '0 0 1 1 *': '每年 1 月 1 日 00:00',
        }
        
        if expression in common_patterns:
            return common_patterns[expression]
        
        return f'Cron: {expression}'
    
    def get_next_runs(self, expression: str, count: int = 5) -> List[str]:
        """获取接下来的执行时间"""
        try:
            cron = croniter(expression, datetime.now())
            runs = []
            for _ in range(count):
                next_run = cron.get_next(datetime)
                runs.append(next_run.isoformat())
            return runs
        except:
            return []


# 单例实例
scheduler_service = SchedulerService()
