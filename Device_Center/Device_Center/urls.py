"""
URL configuration for Device_Center project.
Django 4.2 URL routing
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
import os

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('device.urls')),
]

# 静态文件服务（开发模式）
if settings.DEBUG:
    # 直接从 STATICFILES_DIRS 目录服务
    static_url = settings.STATIC_URL
    static_root = os.path.join(settings.BASE_DIR, 'static')
    urlpatterns += static(static_url, document_root=static_root)

# 媒体文件服务
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)