"""
Django 上下文CPU
为所有模板提供全局变量
"""
from django.conf import settings
from datetime import datetime


def global_settings(request):
    """全局设置上下文"""
    user_id = request.session.get('user_id')
    is_admin = request.session.get('is_admin', False)
    is_logged_in = bool(user_id or is_admin)
    user_display = request.session.get('admin_name') or request.session.get('user_name', '') or ''
    return {
        'BRAND': 'Device Center',
        'CURRENT_YEAR': datetime.now().year,
        'DEBUG': settings.DEBUG,
        'is_logged_in': is_logged_in,
        'user_display': user_display,
        'is_admin': is_admin,
        'user_id': user_id,
        'user_name': request.session.get('user_name'),
        'admin_name': request.session.get('admin_name'),
    }
