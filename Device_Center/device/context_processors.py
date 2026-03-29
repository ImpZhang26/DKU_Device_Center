"""
Django 上下文处理器
为所有模板提供全局变量
"""
from django.conf import settings
from datetime import datetime


def global_settings(request):
    """全局设置上下文"""
    return {
        'BRAND': 'Device Center',
        'CURRENT_YEAR': datetime.now().year,
        'DEBUG': settings.DEBUG,
        # 用户信息
        'user_id': request.session.get('user_id'),
        'user_name': request.session.get('user_name'),
        'is_admin': request.session.get('is_admin', False),
        'admin_name': request.session.get('admin_name'),
    }