"""
设备选配应用
Django 4.2 数据模型
"""
from django.db import models
from django.contrib.auth.models import User


def product_image_path(instance, filename):
    """产品图片上传路径"""
    brand = getattr(instance, 'brand', 'common').lower()
    return f'products/{brand}/{filename}'


class ProductImage(models.Model):
    """产品图片（支持主图+多副图）"""
    BRAND_CHOICES = [
        ('apple', 'Apple'),
        ('dell', 'Dell'),
        ('lenovo', 'Lenovo'),
    ]
    
    IMAGE_TYPE_CHOICES = [
        ('main', '主图'),
        ('gallery', '副图'),
    ]
    
    brand = models.CharField(max_length=50, choices=BRAND_CHOICES, verbose_name='品牌')
    product_id = models.IntegerField(verbose_name='产品ID')  # 关联的产品ID（AppleModel/DellProduct/LenovoProduct）
    product_type = models.CharField(max_length=50, verbose_name='产品类型')  # apple_model/dell_product/lenovo_product
    image_type = models.CharField(max_length=20, choices=IMAGE_TYPE_CHOICES, default='gallery', verbose_name='图片类型')
    image = models.ImageField(upload_to=product_image_path, verbose_name='产品图片')
    title = models.CharField(max_length=100, blank=True, verbose_name='图片标题')
    sort_order = models.IntegerField(default=0, verbose_name='排序')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    class Meta:
        verbose_name = '产品图片'
        verbose_name_plural = '产品图片'
        db_table = 'product_images'
        ordering = ['sort_order', 'created_at']

    def __str__(self):
        return f"{self.brand} - {self.product_id} - {self.image.name}"


class ProductType(models.Model):
    """产品类型（如：Laptop、Desktop、平板、Accessories）"""
    device_type = models.CharField(max_length=50, unique=True, verbose_name='设备类型')
    name = models.CharField(max_length=100, verbose_name='名称')
    description = models.TextField(blank=True, verbose_name='描述')
    is_active = models.BooleanField(default=True, verbose_name='是否启用')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    class Meta:
        verbose_name = '产品类型'
        verbose_name_plural = '产品类型'
        db_table = 'product_types'

    def __str__(self):
        return self.name


class ProductModel(models.Model):
    """Model（如：MacBook Pro 14"、iPad Pro）"""
    model_name = models.CharField(max_length=200, verbose_name='型号名称')
    device_type = models.ForeignKey(ProductType, on_delete=models.CASCADE, verbose_name='设备类型')
    description = models.TextField(blank=True, verbose_name='描述')
    image_url = models.CharField(max_length=500, blank=True, verbose_name='图片URL')
    is_active = models.BooleanField(default=True, verbose_name='是否启用')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    class Meta:
        verbose_name = 'Model'
        verbose_name_plural = 'Model'
        unique_together = ['model_name', 'device_type']
        db_table = 'product_models'

    def __str__(self):
        return self.model_name


class ProductConfiguration(models.Model):
    """产品配置（如：M3 Pro/18GB/512GB）"""
    model = models.ForeignKey(ProductModel, on_delete=models.CASCADE, related_name='configurations', verbose_name='型号')
    configuration = models.CharField(max_length=200, verbose_name='配置名称')
    cpu = models.CharField(max_length=200, blank=True, verbose_name='CPU')
    memory = models.CharField(max_length=100, blank=True, verbose_name='Memory')
    hard_disk = models.CharField(max_length=100, blank=True, verbose_name='硬盘')
    graphic_card = models.CharField(max_length=200, blank=True, verbose_name='GPU')
    screen = models.CharField(max_length=200, blank=True, verbose_name='屏幕')
    original_price = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name='原价')
    discount_price = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name='优惠价')
    discount_rate = models.DecimalField(max_digits=5, decimal_places=2, default=0, verbose_name='折扣率')
    # 新增字段
    color_option = models.TextField(blank=True, verbose_name='颜色选项')
    configuration_parameters = models.TextField(blank=True, verbose_name='配置参数')
    changing_config_price = models.TextField(blank=True, verbose_name='配置价格变更')
    weight = models.CharField(max_length=50, blank=True, verbose_name='Weight')
    wifi = models.CharField(max_length=100, blank=True, verbose_name='Wi-Fi')
    product_link = models.CharField(max_length=500, blank=True, verbose_name='产品链接')
    is_active = models.BooleanField(default=True, verbose_name='是否启用')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    class Meta:
        verbose_name = '产品配置'
        verbose_name_plural = '产品配置'
        db_table = 'product_configurations'

    def __str__(self):
        return f"{self.model.model_name} - {self.configuration}"


class Accessory(models.Model):
    """Accessories"""
    DEVICE_TYPES = [
        ('Keyboard', '键盘'),
        ('Mouse', '鼠标'),
        ('Trackpad', '触控板'),
        ('Audio', '音频'),
        ('Cable', '线缆'),
        ('Stylus', '手写笔'),
        ('Other', '其他'),
    ]
    
    model = models.CharField(max_length=200, verbose_name='型号')
    device_type = models.CharField(max_length=50, choices=DEVICE_TYPES, verbose_name='类型')
    description = models.TextField(blank=True, verbose_name='描述')
    original_price = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name='原价')
    discount_price = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name='优惠价')
    discount_rate = models.DecimalField(max_digits=5, decimal_places=2, default=0, verbose_name='折扣率')
    is_active = models.BooleanField(default=True, verbose_name='是否启用')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    class Meta:
        verbose_name = 'Accessories'
        verbose_name_plural = 'Accessories'
        db_table = 'accessories'

    def __str__(self):
        return self.model


class CartItem(models.Model):
    """购物车"""
    BRAND_CHOICES = [
        ('apple', 'Apple'),
        ('dell', 'Dell'),
        ('lenovo', 'Lenovo'),
    ]
    
    user_id = models.CharField(max_length=100, verbose_name='用户ID')  # 使用session_id或netid
    brand = models.CharField(max_length=50, choices=BRAND_CHOICES, verbose_name='品牌')
    device_type = models.CharField(max_length=50, blank=True, verbose_name='设备类型')
    model_name = models.CharField(max_length=200, verbose_name='型号名称')
    configuration_id = models.IntegerField(null=True, blank=True, verbose_name='配置ID')
    selected_config = models.JSONField(null=True, blank=True, verbose_name='选中配置')
    quantity = models.IntegerField(default=1, verbose_name='数量')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    class Meta:
        verbose_name = '购物车'
        verbose_name_plural = '购物车'
        db_table = 'cart_items'

    def __str__(self):
        return f"{self.user_id} - {self.model_name}"


class Order(models.Model):
    """订单"""
    BRAND_CHOICES = [
        ('apple', 'Apple'),
        ('dell', 'Dell'),
        ('lenovo', 'Lenovo'),
    ]
    
    STATUS_CHOICES = [
        ('pending', '待处理'),
        ('processing', '处理中'),
        ('completed', '已完成'),
        ('cancelled', '已取消'),
    ]
    
    order_number = models.CharField(max_length=50, unique=True, verbose_name='订单号')
    user_id = models.CharField(max_length=100, verbose_name='用户ID')
    user_name = models.CharField(max_length=200, blank=True, verbose_name='用户名')
    user_email = models.CharField(max_length=200, blank=True, verbose_name='用户eMail')
    brand = models.CharField(max_length=50, choices=BRAND_CHOICES, verbose_name='品牌')
    device_type = models.CharField(max_length=50, blank=True, verbose_name='设备类型')
    model_name = models.CharField(max_length=200, verbose_name='型号名称')
    selected_cpu = models.CharField(max_length=200, blank=True, verbose_name='CPU')
    selected_memory = models.CharField(max_length=100, blank=True, verbose_name='Memory')
    selected_hard_disk = models.CharField(max_length=100, blank=True, verbose_name='硬盘')
    selected_graphic_card = models.CharField(max_length=200, blank=True, verbose_name='GPU')
    selected_screen = models.CharField(max_length=200, blank=True, verbose_name='屏幕')
    
    # 升级配置
    selected_upgrades = models.JSONField(null=True, blank=True, verbose_name='选中升级配置')
    upgrade_price = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name='升级费用')
    
    base_price = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name='基础价格')
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name='Total Price')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name='状态')
    remark = models.TextField(blank=True, verbose_name='Remark')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        verbose_name = '订单'
        verbose_name_plural = '订单'
        ordering = ['-created_at']
        db_table = 'orders'

    def __str__(self):
        return self.order_number


class Admin(models.Model):
    """管理员"""
    username = models.CharField(max_length=100, unique=True, verbose_name='用户名')
    password_hash = models.CharField(max_length=256, verbose_name='密码哈希')
    name = models.CharField(max_length=100, verbose_name='姓名')
    email = models.CharField(max_length=200, blank=True, verbose_name='eMail')
    role = models.CharField(max_length=50, default='admin', verbose_name='角色')
    is_active = models.BooleanField(default=True, verbose_name='是否启用')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    class Meta:
        verbose_name = '管理员'
        verbose_name_plural = '管理员'
        db_table = 'admins'

    def __str__(self):
        return self.username


class DellProduct(models.Model):
    """Dell 产品"""
    DEVICE_TYPE_CHOICES = [
        ('Notebook', 'Laptop'),
        ('Laptop', 'High-performance Laptop'),
        ('Desktop', 'Desktop'),
        ('Monitor', 'Monitor'),
        ('Docking', '扩展坞'),
    ]
    
    # 基本信息
    device_type = models.CharField(max_length=50, choices=DEVICE_TYPE_CHOICES, verbose_name='设备类型')
    brand = models.CharField(max_length=50, default='DELL', verbose_name='品牌')
    model = models.CharField(max_length=200, verbose_name='型号名称')
    basic_config = models.TextField(blank=True, verbose_name='Basic Configuration')
    
    # 硬件配置
    cpu = models.CharField(max_length=500, blank=True, verbose_name='CPU')
    memory = models.CharField(max_length=200, blank=True, verbose_name='Memory')
    hard_disk = models.CharField(max_length=200, blank=True, verbose_name='硬盘')
    graphic_card = models.CharField(max_length=500, blank=True, verbose_name='GPU')
    wifi = models.CharField(max_length=500, blank=True, verbose_name='Wi-Fi')
    
    # 详细配置
    configuration_parameters = models.TextField(blank=True, verbose_name='配置参数（接口/端口）')
    weight = models.TextField(blank=True, verbose_name='Weight/尺寸')
    official_link = models.CharField(max_length=500, blank=True, verbose_name='官方链接')
    
    # 价格信息
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name='售价')
    original_price = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name='原价')
    discount_rate = models.DecimalField(max_digits=5, decimal_places=2, default=0, verbose_name='折扣率')
    changing_config_price = models.TextField(blank=True, verbose_name='配置升级价格')
    
    # 图片
    image_url = models.CharField(max_length=500, blank=True, verbose_name='产品图片URL')
    
    # 其他
    remark = models.TextField(blank=True, verbose_name='Remark')
    is_active = models.BooleanField(default=True, verbose_name='是否启用')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        verbose_name = 'Dell 产品'
        verbose_name_plural = 'Dell 产品'
        db_table = 'dell_products'
        ordering = ['device_type', 'model']

    def __str__(self):
        return self.model


class LenovoProduct(models.Model):
    """Lenovo 产品（包含型号和配置信息）"""
    DEVICE_TYPE_CHOICES = [
        ('Laptop', 'Laptop'),
        ('Desktop', 'Desktop'),
    ]
    
    # 基本信息
    device_type = models.CharField(max_length=50, choices=DEVICE_TYPE_CHOICES, verbose_name='设备类型')
    brand = models.CharField(max_length=50, default='Lenovo', verbose_name='品牌')
    model = models.CharField(max_length=200, verbose_name='型号名称')
    
    # 配置名称
    configuration = models.CharField(max_length=200, blank=True, verbose_name='配置名称')
    
    # 硬件配置
    cpu = models.CharField(max_length=500, blank=True, verbose_name='CPU')
    memory = models.CharField(max_length=200, blank=True, verbose_name='Memory')
    hard_disk = models.CharField(max_length=200, blank=True, verbose_name='硬盘')
    graphic_card = models.CharField(max_length=500, blank=True, verbose_name='GPU')
    
    # 其他配置
    screen = models.CharField(max_length=200, blank=True, verbose_name='屏幕')
    wifi = models.CharField(max_length=500, blank=True, verbose_name='Wi-Fi')
    weight = models.CharField(max_length=100, blank=True, verbose_name='Weight')
    accessary = models.CharField(max_length=500, blank=True, verbose_name='Accessories')
    
    # 详细配置
    configuration_parameters = models.TextField(blank=True, verbose_name='配置参数（接口/端口）')
    changing_config_price = models.TextField(blank=True, verbose_name='配置升级价格')
    
    # 价格信息
    discount_price = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name='优惠价')
    original_price = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name='原价')
    discount_rate = models.DecimalField(max_digits=5, decimal_places=2, default=0, verbose_name='折扣率')
    
    # 图片
    image_url = models.CharField(max_length=500, blank=True, verbose_name='产品图片URL')
    
    # 链接
    product_link = models.CharField(max_length=500, blank=True, verbose_name='产品链接')
    
    is_active = models.BooleanField(default=True, verbose_name='是否启用')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        verbose_name = 'Lenovo 产品'
        verbose_name_plural = 'Lenovo 产品'
        db_table = 'lenovo_products'
        ordering = ['device_type', 'model']

    def __str__(self):
        return f"{self.model} - {self.configuration}" if self.configuration else self.model