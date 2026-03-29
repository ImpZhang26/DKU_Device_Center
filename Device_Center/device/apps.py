"""
设备选配应用配置
Django 4.2
"""
from django.apps import AppConfig


class DeviceConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'device'
    verbose_name = '设备选配'
    
    def ready(self):
        # 应用启动时执行的初始化操作
        pass