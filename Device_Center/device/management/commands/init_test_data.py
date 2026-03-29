"""
初始化测试数据管理命令
用法: python manage.py init_test_data
"""
import hashlib
from django.core.management.base import BaseCommand
from device.models import ProductType, ProductModel, ProductConfiguration, Accessory, Admin


class Command(BaseCommand):
    help = '初始化测试数据'

    def handle(self, *args, **options):
        self.stdout.write('正在初始化测试数据...\n')
        
        # 初始化产品类型
        self.init_product_types()
        
        # 初始化型号
        self.init_models()
        
        # 初始化配置
        self.init_configurations()
        
        # 初始化配件
        self.init_accessories()
        
        # 初始化管理员
        self.init_admin()
        
        self.stdout.write(self.style.SUCCESS('\n✓ 测试数据初始化完成！\n'))
        self.stdout.write('\n登录信息:\n')
        self.stdout.write('  NETID登录: 任意NETID（如 testuser）\n')
        self.stdout.write('  管理员登录: admin / admin123\n')

    def init_product_types(self):
        """初始化产品类型"""
        self.stdout.write('正在初始化产品类型...')
        
        types = [
            ('Laptop', '笔记本电脑', 'MacBook Pro、MacBook Air'),
            ('Desktop', '台式机', 'iMac、Mac mini、Mac Studio、Mac Pro'),
            ('iPad', '平板电脑', 'iPad Pro、iPad Air、iPad、iPad mini'),
            ('Accessories', '配件', '键盘、鼠标、触控板等配件')
        ]
        
        for device_type, name, description in types:
            ProductType.objects.update_or_create(
                device_type=device_type,
                defaults={'name': name, 'description': description}
            )
        
        self.stdout.write(self.style.SUCCESS(' OK'))

    def init_models(self):
        """初始化型号"""
        self.stdout.write('\n正在初始化产品型号...')
        
        laptop_type = ProductType.objects.get(device_type='Laptop')
        desktop_type = ProductType.objects.get(device_type='Desktop')
        ipad_type = ProductType.objects.get(device_type='iPad')
        
        models = [
            # 笔记本电脑
            ('MacBook Pro 14"', laptop_type, 'M3 Pro/Max芯片，14.2英寸Liquid Retina XDR显示屏'),
            ('MacBook Pro 16"', laptop_type, 'M3 Pro/Max芯片，16.2英寸Liquid Retina XDR显示屏'),
            ('MacBook Air 13"', laptop_type, 'M3芯片，13.6英寸Liquid Retina显示屏'),
            # 台式机
            ('iMac 24"', desktop_type, 'M3芯片，24英寸4.5K Retina显示屏'),
            ('Mac mini', desktop_type, 'M2/M2 Pro芯片，小巧机身强劲性能'),
            ('Mac Studio', desktop_type, 'M2 Max/Ultra芯片，专业工作室级性能'),
            ('Mac Pro', desktop_type, 'M2 Ultra芯片，最强性能专业工作站'),
            # iPad
            ('iPad Pro 12.9"', ipad_type, 'M2芯片，12.9英寸Liquid Retina XDR显示屏'),
            ('iPad Pro 11"', ipad_type, 'M2芯片，11英寸Liquid Retina显示屏'),
            ('iPad Air', ipad_type, 'M1芯片，10.9英寸Liquid Retina显示屏'),
            ('iPad', ipad_type, 'A14芯片，10.9英寸Retina显示屏'),
            ('iPad mini', ipad_type, 'A15芯片，8.3英寸Liquid Retina显示屏'),
        ]
        
        for model_name, device_type, description in models:
            ProductModel.objects.update_or_create(
                model_name=model_name,
                device_type=device_type,
                defaults={'description': description}
            )
        
        self.stdout.write(self.style.SUCCESS(' OK'))

    def init_configurations(self):
        """初始化配置"""
        self.stdout.write('\n正在初始化产品配置...')
        
        # 获取型号
        mbp14 = ProductModel.objects.get(model_name='MacBook Pro 14"')
        mbp16 = ProductModel.objects.get(model_name='MacBook Pro 16"')
        mba13 = ProductModel.objects.get(model_name='MacBook Air 13"')
        imac24 = ProductModel.objects.get(model_name='iMac 24"')
        ipad_pro_129 = ProductModel.objects.get(model_name='iPad Pro 12.9"')
        ipad_air = ProductModel.objects.get(model_name='iPad Air')
        
        configurations = [
            # MacBook Pro 14"
            {'model': mbp14, 'config': 'M3 Pro/18GB/512GB', 'cpu': 'M3 Pro (11核CPU/14核GPU)', 'memory': '18GB', 'hard_disk': '512GB SSD', 'graphic_card': '14核GPU', 'screen': '14.2英寸XDR', 'original': 17999, 'discount': 14999, 'rate': 0.17},
            {'model': mbp14, 'config': 'M3 Pro/18GB/1TB', 'cpu': 'M3 Pro (11核CPU/14核GPU)', 'memory': '18GB', 'hard_disk': '1TB SSD', 'graphic_card': '14核GPU', 'screen': '14.2英寸XDR', 'original': 19999, 'discount': 16999, 'rate': 0.15},
            {'model': mbp14, 'config': 'M3 Max/36GB/1TB', 'cpu': 'M3 Max (14核CPU/30核GPU)', 'memory': '36GB', 'hard_disk': '1TB SSD', 'graphic_card': '30核GPU', 'screen': '14.2英寸XDR', 'original': 34999, 'discount': 28999, 'rate': 0.17},
            # MacBook Pro 16"
            {'model': mbp16, 'config': 'M3 Pro/18GB/512GB', 'cpu': 'M3 Pro (12核CPU/18核GPU)', 'memory': '18GB', 'hard_disk': '512GB SSD', 'graphic_card': '18核GPU', 'screen': '16.2英寸XDR', 'original': 23999, 'discount': 19999, 'rate': 0.17},
            {'model': mbp16, 'config': 'M3 Max/36GB/1TB', 'cpu': 'M3 Max (16核CPU/40核GPU)', 'memory': '36GB', 'hard_disk': '1TB SSD', 'graphic_card': '40核GPU', 'screen': '16.2英寸XDR', 'original': 38999, 'discount': 31999, 'rate': 0.18},
            # MacBook Air 13"
            {'model': mba13, 'config': 'M3/8GB/256GB', 'cpu': 'M3 (8核CPU/8核GPU)', 'memory': '8GB', 'hard_disk': '256GB SSD', 'graphic_card': '8核GPU', 'screen': '13.6英寸Retina', 'original': 8999, 'discount': 7999, 'rate': 0.11},
            {'model': mba13, 'config': 'M3/16GB/512GB', 'cpu': 'M3 (8核CPU/8核GPU)', 'memory': '16GB', 'hard_disk': '512GB SSD', 'graphic_card': '8核GPU', 'screen': '13.6英寸Retina', 'original': 12499, 'discount': 10999, 'rate': 0.12},
            # iMac 24"
            {'model': imac24, 'config': 'M3/8GB/256GB', 'cpu': 'M3 (8核CPU/8核GPU)', 'memory': '8GB', 'hard_disk': '256GB SSD', 'graphic_card': '集成显卡', 'screen': '24英寸4.5K', 'original': 12999, 'discount': 10999, 'rate': 0.15},
            {'model': imac24, 'config': 'M3/16GB/512GB', 'cpu': 'M3 (8核CPU/10核GPU)', 'memory': '16GB', 'hard_disk': '512GB SSD', 'graphic_card': '10核GPU', 'screen': '24英寸4.5K', 'original': 17499, 'discount': 14999, 'rate': 0.14},
            # iPad
            {'model': ipad_pro_129, 'config': '256GB', 'cpu': 'M2', 'memory': '8GB', 'hard_disk': '256GB', 'graphic_card': '-', 'screen': '12.9英寸XDR', 'original': 9999, 'discount': 9299, 'rate': 0.07},
            {'model': ipad_pro_129, 'config': '512GB', 'cpu': 'M2', 'memory': '8GB', 'hard_disk': '512GB', 'graphic_card': '-', 'screen': '12.9英寸XDR', 'original': 11499, 'discount': 10499, 'rate': 0.09},
            {'model': ipad_air, 'config': '256GB', 'cpu': 'M1', 'memory': '8GB', 'hard_disk': '256GB', 'graphic_card': '-', 'screen': '10.9英寸Retina', 'original': 5399, 'discount': 4799, 'rate': 0.11},
        ]
        
        for c in configurations:
            ProductConfiguration.objects.update_or_create(
                model=c['model'],
                configuration=c['config'],
                defaults={
                    'cpu': c['cpu'],
                    'memory': c['memory'],
                    'hard_disk': c['hard_disk'],
                    'graphic_card': c['graphic_card'],
                    'screen': c['screen'],
                    'original_price': c['original'],
                    'discount_price': c['discount'],
                    'discount_rate': c['rate'],
                }
            )
        
        self.stdout.write(self.style.SUCCESS(' OK'))

    def init_accessories(self):
        """初始化配件"""
        self.stdout.write('\n正在初始化配件...')
        
        accessories = [
            ('Magic Keyboard', 'Keyboard', '带有Touch ID的妙控键盘', 899, 749, 0.17),
            ('Magic Mouse', 'Mouse', '妙控鼠标', 699, 579, 0.17),
            ('Magic Trackpad', 'Trackpad', '妙控触控板', 999, 849, 0.15),
            ('AirPods Pro', 'Audio', 'AirPods Pro (第二代) 带USB-C充电盒', 1899, 1799, 0.05),
            ('Apple Pencil Pro', 'Stylus', 'Apple Pencil Pro', 999, 999, 0.00),
            ('USB-C to Lightning', 'Cable', 'USB-C转闪电连接线 (1米)', 289, 243, 0.16),
        ]
        
        for model, device_type, description, original, discount, rate in accessories:
            Accessory.objects.update_or_create(
                model=model,
                defaults={
                    'device_type': device_type,
                    'description': description,
                    'original_price': original,
                    'discount_price': discount,
                    'discount_rate': rate,
                }
            )
        
        self.stdout.write(self.style.SUCCESS(' OK'))

    def init_admin(self):
        """初始化管理员"""
        self.stdout.write('\n正在初始化管理员账号...')
        
        password_hash = hashlib.sha256('admin123'.encode()).hexdigest()
        Admin.objects.update_or_create(
            username='admin',
            defaults={
                'password_hash': password_hash,
                'name': '系统管理员',
                'role': 'super_admin',
            }
        )
        
        self.stdout.write(self.style.SUCCESS(' OK'))