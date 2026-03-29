"""
设备选配应用 - Django后台管理配置
"""
from django.contrib import admin
from .models import ProductType, ProductModel, ProductConfiguration, Accessory, CartItem, Order, Admin


@admin.register(ProductType)
class ProductTypeAdmin(admin.ModelAdmin):
    list_display = ['device_type', 'name', 'description', 'is_active']
    search_fields = ['device_type', 'name']
    list_filter = ['is_active']


@admin.register(ProductModel)
class ProductModelAdmin(admin.ModelAdmin):
    list_display = ['model_name', 'device_type', 'is_active']
    search_fields = ['model_name', 'description']
    list_filter = ['device_type', 'is_active']


@admin.register(ProductConfiguration)
class ProductConfigurationAdmin(admin.ModelAdmin):
    list_display = ['model', 'configuration', 'cpu', 'memory', 'discount_price', 'is_active']
    search_fields = ['configuration', 'cpu']
    list_filter = ['model', 'is_active']


@admin.register(Accessory)
class AccessoryAdmin(admin.ModelAdmin):
    list_display = ['model', 'device_type', 'discount_price', 'is_active']
    search_fields = ['model', 'description']
    list_filter = ['device_type', 'is_active']


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ['user_id', 'brand', 'model_name', 'created_at']
    search_fields = ['user_id', 'model_name']
    list_filter = ['brand', 'created_at']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['order_number', 'user_id', 'brand', 'model_name', 'total_price', 'status', 'created_at']
    search_fields = ['order_number', 'user_id', 'model_name']
    list_filter = ['brand', 'status', 'created_at']
    readonly_fields = ['order_number', 'created_at', 'updated_at']
    fieldsets = (
        ('基本信息', {'fields': ('order_number', 'user_id', 'user_name', 'brand')}),
        ('产品信息', {'fields': ('device_type', 'model_name')}),
        ('配置信息', {'fields': ('selected_cpu', 'selected_memory', 'selected_hard_disk', 'selected_graphic_card', 'selected_screen')}),
        ('订单信息', {'fields': ('total_price', 'status', 'remark')}),
        ('时间信息', {'fields': ('created_at', 'updated_at')}),
    )


@admin.register(Admin)
class AdminAdmin(admin.ModelAdmin):
    list_display = ['username', 'name', 'email', 'role', 'is_active']
    search_fields = ['username', 'name']
    list_filter = ['role', 'is_active']
    readonly_fields = ['password_hash']