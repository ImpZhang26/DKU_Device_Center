"""
设备选配应用 - URL配置
Django 4.2 URL routing
"""
from django.urls import path
from . import views

urlpatterns = [
    # 首页
    path('', views.index, name='index'),
    
    # 认证
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    
    # Apple 选配中心
    path('apple/', views.apple_index, name='apple_index'),
    path('apple/laptop/', views.apple_laptop, name='apple_laptop'),
    path('apple/desktop/', views.apple_desktop, name='apple_desktop'),
    path('apple/ipad/', views.apple_ipad, name='apple_ipad'),
    path('apple/accessories/', views.apple_accessories, name='apple_accessories'),
    path('apple/detail/<int:config_id>/', views.apple_detail, name='apple_detail'),
    
    # Dell 选配中心
    path('dell/', views.dell_index, name='dell_index'),
    path('dell/notebook/', views.dell_notebook, name='dell_notebook'),
    path('dell/laptop/', views.dell_laptop, name='dell_laptop'),
    path('dell/desktop/', views.dell_desktop, name='dell_desktop'),
    path('dell/monitor/', views.dell_monitor, name='dell_monitor'),
    path('dell/accessories/', views.dell_accessories, name='dell_accessories'),
    path('dell/detail/<str:model_name>/', views.dell_detail, name='dell_detail'),
    
    # Lenovo 选配中心
    path('lenovo/', views.lenovo_index, name='lenovo_index'),
    path('lenovo/laptop/', views.lenovo_laptop, name='lenovo_laptop'),
    path('lenovo/desktop/', views.lenovo_desktop, name='lenovo_desktop'),
    path('lenovo/detail/<int:config_id>/', views.lenovo_detail, name='lenovo_detail'),
    
    # API - Apple
    path('api/apple/types/', views.api_product_types, {'brand': 'apple'}, name='api_apple_types'),
    path('api/apple/models/<str:device_type>/', views.api_models, {'brand': 'apple'}, name='api_apple_models'),
    path('api/apple/configs/<int:model_id>/', views.api_configurations, {'brand': 'apple'}, name='api_apple_configs'),
    path('api/apple/accessories/', views.api_accessories, {'brand': 'apple'}, name='api_apple_accessories'),
    
    # 购物车 API
    path('api/<str:brand>/cart/add/', views.api_cart_add, name='api_cart_add'),
    path('api/<str:brand>/cart/<int:cart_id>/remove/', views.api_cart_remove, name='api_cart_remove'),
    path('api/<str:brand>/cart/', views.api_cart_list, name='api_cart_list'),
    
    # 订单 API
    path('api/<str:brand>/order/create/', views.api_order_create, name='api_order_create'),
    path('api/<str:brand>/orders/', views.api_orders, name='api_orders'),
    
    # 我的订单
    path('orders/', views.my_orders, name='my_orders'),
    path('api/order/cancel/', views.api_order_cancel, name='api_order_cancel'),
    
    # 管理后台 (避免与 Django Admin 冲突，使用 /manage/ 前缀)
    path('manage/', views.admin_dashboard, name='manage'),
    path('api/admin/export/orders/', views.export_orders_excel, name='export_orders_excel'),
    path('api/admin/orders/', views.api_admin_orders, name='api_admin_orders'),
    path('api/admin/order/<int:order_id>/', views.api_admin_order_detail, name='api_admin_order_detail'),
    path('api/admin/order/<int:order_id>/status/', views.api_admin_order_status, name='api_admin_order_status'),
    path('api/admin/stats/', views.api_admin_stats, name='api_admin_stats'),
    
    # 产品管理
    path('api/admin/apple/models/', views.api_admin_apple_models, name='api_admin_apple_models'),
    path('api/admin/apple/model/<int:model_id>/', views.api_admin_apple_model, name='api_admin_apple_model'),
    path('api/admin/apple/configs/', views.api_admin_apple_configs, name='api_admin_apple_configs'),
    path('api/admin/apple/config/<int:config_id>/', views.api_admin_apple_config, name='api_admin_apple_config'),
    path('api/admin/dell/products/', views.api_admin_dell_products, name='api_admin_dell_products'),
    path('api/admin/dell/product/<int:product_id>/', views.api_admin_dell_product, name='api_admin_dell_product'),
    path('api/admin/lenovo/products/', views.api_admin_lenovo_products, name='api_admin_lenovo_products'),
    path('api/admin/lenovo/product/<int:product_id>/', views.api_admin_lenovo_product, name='api_admin_lenovo_product'),
    
    # 产品图片管理
    path('api/admin/<str:brand>/<str:product_type>/<int:product_id>/images/', views.api_admin_product_images, name='api_admin_product_images'),
    path('api/admin/<str:brand>/upload/image/', views.api_admin_upload_image, name='api_admin_upload_image'),
    path('api/admin/image/<int:image_id>/', views.api_admin_delete_image, name='api_admin_delete_image'),
    path('api/admin/image/<int:image_id>/set-main/', views.api_admin_set_main_image, name='api_admin_set_main_image'),
    path('api/admin/images/reorder/', views.api_admin_reorder_images, name='api_admin_reorder_images'),

    # 产品特定图片管理（根据brand和product_id）
    path('api/admin/<str:brand>/<int:product_id>/images/', views.api_admin_product_images, name='api_admin_product_images'),
    path('api/admin/<str:brand>/<int:product_id>/upload-image/', views.api_admin_product_upload_image, name='api_admin_product_upload_image'),
    path('api/admin/<str:brand>/<int:product_id>/set-main-image/', views.api_admin_product_set_main_image, name='api_admin_product_set_main_image'),
    path('api/admin/<str:brand>/<int:product_id>/delete-image/', views.api_admin_product_delete_image, name='api_admin_product_delete_image'),
    path('api/admin/<str:brand>/<int:product_id>/delete-main-image/', views.api_admin_product_delete_main_image, name='api_admin_product_delete_main_image'),

    # Apple Model 图片管理
    path('api/admin/apple/model/<int:model_id>/images/', views.api_admin_apple_model_images, name='api_admin_apple_model_images'),
    path('api/admin/apple/model/<int:model_id>/upload-image/', views.api_admin_apple_model_upload_image, name='api_admin_apple_model_upload_image'),
    path('api/admin/apple/model/<int:model_id>/set-main-image/', views.api_admin_apple_model_set_main_image, name='api_admin_apple_model_set_main_image'),
    path('api/admin/apple/model/<int:model_id>/delete-image/<int:image_id>/', views.api_admin_apple_model_delete_image, name='api_admin_apple_model_delete_image'),
    path('api/admin/apple/model/<int:model_id>/delete-main-image/', views.api_admin_apple_model_delete_main_image, name='api_admin_apple_model_delete_main_image'),

    # Apple Config 图片管理
    path('api/admin/apple/config/<int:config_id>/images/', views.api_admin_apple_config_images, name='api_admin_apple_config_images'),
    path('api/admin/apple/config/<int:config_id>/upload-image/', views.api_admin_apple_config_upload_image, name='api_admin_apple_config_upload_image'),
    path('api/admin/apple/config/<int:config_id>/set-main-image/', views.api_admin_apple_config_set_main_image, name='api_admin_apple_config_set_main_image'),
    path('api/admin/apple/config/<int:config_id>/delete-image/<int:image_id>/', views.api_admin_apple_config_delete_image, name='api_admin_apple_config_delete_image'),
    path('api/admin/apple/config/<int:config_id>/delete-main-image/', views.api_admin_apple_config_delete_main_image, name='api_admin_apple_config_delete_main_image'),

    # Dell Product 图片管理
    path('api/admin/dell/product/<int:product_id>/images/', views.api_admin_dell_product_images, name='api_admin_dell_product_images'),
    path('api/admin/dell/product/<int:product_id>/upload-image/', views.api_admin_dell_product_upload_image, name='api_admin_dell_product_upload_image'),
    path('api/admin/dell/product/<int:product_id>/set-main-image/', views.api_admin_dell_product_set_main_image, name='api_admin_dell_product_set_main_image'),
    path('api/admin/dell/product/<int:product_id>/delete-image/<int:image_id>/', views.api_admin_dell_product_delete_image, name='api_admin_dell_product_delete_image'),
    path('api/admin/dell/product/<int:product_id>/delete-main-image/', views.api_admin_dell_product_delete_main_image, name='api_admin_dell_product_delete_main_image'),

    # Lenovo Product 图片管理
    path('api/admin/lenovo/product/<int:product_id>/images/', views.api_admin_lenovo_product_images, name='api_admin_lenovo_product_images'),
    path('api/admin/lenovo/product/<int:product_id>/upload-image/', views.api_admin_lenovo_product_upload_image, name='api_admin_lenovo_product_upload_image'),
    path('api/admin/lenovo/product/<int:product_id>/set-main-image/', views.api_admin_lenovo_product_set_main_image, name='api_admin_lenovo_product_set_main_image'),
    path('api/admin/lenovo/product/<int:product_id>/delete-image/<int:image_id>/', views.api_admin_lenovo_product_delete_image, name='api_admin_lenovo_product_delete_image'),
    path('api/admin/lenovo/product/<int:product_id>/delete-main-image/', views.api_admin_lenovo_product_delete_main_image, name='api_admin_lenovo_product_delete_main_image'),
]