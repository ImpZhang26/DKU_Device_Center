"""
从 apple.json 导入数据到 Django 数据库
使用方式: python manage.py import_apple_data
"""
import json
import os
import sys

# 设置Django环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Device_Center.settings')
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

import django
django.setup()

from django.core.management.base import BaseCommand
from device.models import ProductType, ProductModel, ProductConfiguration, Accessory


class Command(BaseCommand):
    help = '从 apple.json 导入数据到 Django 数据库'
    
    def handle(self, *args, **options):
        # 从 /Device_Center/jsonData/ 读取 apple.json
        json_path = '/Users/tz138/Desktop/DKU_Device_Center/Device_Center/jsonData/apple.json'
        
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        self.stdout.write("=" * 60)
        self.stdout.write("开始导入 Apple 产品数据...")
        self.stdout.write("=" * 60)
        
        # 导入 Laptop
        self.stdout.write("\n📦 正在导入 Laptop...")
        self.import_category(data.get('Laptop', []), 'Laptop')
        
        # 导入 Desktop
        self.stdout.write("\n📦 正在导入 Desktop...")
        self.import_category(data.get('Desktop', []), 'Desktop')
        
        # 导入 iPad
        self.stdout.write("\n📦 正在导入 iPad...")
        self.import_category(data.get('iPad', []), 'iPad')
        
        # 导入 Accessories
        self.stdout.write("\n📦 正在导入 Accessories...")
        self.import_accessories(data.get('Accessories', []))
        
        self.stdout.write("\n" + "=" * 60)
        self.stdout.write(self.style.SUCCESS("✅ 数据导入完成！"))
        self.stdout.write("=" * 60)
        
        # 显示统计
        self.stdout.write(f"\n📊 数据库统计：")
        self.stdout.write(f"  - 产品类型: {ProductType.objects.count()}")
        self.stdout.write(f"  - Model: {ProductModel.objects.count()}")
        self.stdout.write(f"  - 产品配置: {ProductConfiguration.objects.count()}")
        self.stdout.write(f"  - Accessories: {Accessory.objects.count()}")
    
    def import_category(self, products, device_type_name):
        """导入产品分类数据"""

        device_type_map = {
            'Laptop': ('Laptop', 'Laptop'),
            'Desktop': ('Desktop', 'Desktop'),
            'iPad': ('iPad', 'iPad'),
        }

        device_type_code, device_type_cn = device_type_map.get(device_type_name, (device_type_name, device_type_name))

        ptype, created = ProductType.objects.get_or_create(
            device_type=device_type_code,
            defaults={'name': device_type_cn}
        )
        if created:
            self.stdout.write(f"  ✓ 创建产品类型: {device_type_cn}")

        # 导入每个Model
        for product in products:
            model_name = product.get('model', '')
            description = f"{product.get('brand', 'Apple')} {model_name}"

            # 创建Model
            model, created = ProductModel.objects.get_or_create(
                model_name=model_name,
                device_type=ptype,
                defaults={
                    'description': description,
                    'is_active': True
                }
            )
            if created:
                self.stdout.write(f"  ✓ 创建型号: {model_name}")

            # 导入配置
            configs = product.get('configurations', [])
            new_config_count = 0
            skip_config_count = 0

            for config in configs:
                try:
                    original_price = config.get('original_price') or 0
                    discount_price = config.get('discount_price') or 0
                    discount_rate = config.get('discount_rate') or 0

                    cpu = config.get('cpu', '') or ''
                    memory = config.get('memory', '') or ''
                    hard_disk = config.get('hard_disk', '') or ''
                    graphic_card = config.get('graphic_card', '') or ''
                    screen = config.get('screen', '') or ''  # 处理null值，确保不为None

                    # 检查是否已存在完全相同的配置
                    existing = ProductConfiguration.objects.filter(
                        model=model,
                        cpu=cpu,
                        memory=memory,
                        hard_disk=hard_disk,
                        graphic_card=graphic_card,
                        screen=screen,
                        configuration=config.get('configuration', '')
                    ).first()

                    if existing:
                        # 更新折扣价格等可能变化的字段
                        existing.discount_price = discount_price
                        existing.original_price = original_price
                        existing.discount_rate = discount_rate
                        # 更新新字段
                        existing.color_option = config.get('color_option', '') or ''
                        existing.configuration_parameters = config.get('configuration_parameters', '') or ''
                        existing.changing_config_price = config.get('changing_config_price', '') or ''
                        existing.weight = config.get('weight', '') or ''
                        existing.wifi = config.get('wifi', '') or ''
                        existing.product_link = config.get('product_link', '') or ''
                        existing.is_active = True
                        existing.save()
                        skip_config_count += 1
                    else:
                        # 创建新配置
                        ProductConfiguration.objects.create(
                            model=model,
                            configuration=config.get('configuration', ''),
                            cpu=cpu,
                            memory=memory,
                            hard_disk=hard_disk,
                            graphic_card=graphic_card,
                            screen=screen,
                            original_price=original_price,
                            discount_price=discount_price,
                            discount_rate=discount_rate,
                            color_option=config.get('color_option', '') or '',
                            configuration_parameters=config.get('configuration_parameters', '') or '',
                            changing_config_price=config.get('changing_config_price', '') or '',
                            weight=config.get('weight', '') or '',
                            wifi=config.get('wifi', '') or '',
                            product_link=config.get('product_link', '') or '',
                            is_active=True
                        )
                        new_config_count += 1

                except Exception as e:
                    self.stdout.write(self.style.WARNING(f"    ✗ 配置导入失败: {config.get('configuration')}"))
                    self.stdout.write(self.style.WARNING(f"      错误详情: {str(e)}"))
                    import traceback
                    self.stdout.write(self.style.WARNING(f"      错误位置: {traceback.format_exc()}"))

            self.stdout.write(f"    → {model_name}: {new_config_count} 个新配置, {skip_config_count} 个已存在")
    
    def import_accessories(self, accessories):
        """导入Accessories数据"""
        
        for acc in accessories:
            device_type_map = {
                'Keyboard': 'Keyboard',
                'Mouse': 'Mouse',
                'Trackpad': 'Trackpad',
                'Audio': 'Audio',
                'Cable': 'Cable',
                'Stylus': 'Stylus',
            }
            
            model_name = acc.get('model', '')
            device_type = 'Other'
            
            for key in device_type_map:
                if key.lower() in model_name.lower():
                    device_type = device_type_map[key]
                    break
            
            try:
                original_price = acc.get('original_price') or 0
                discount_price = acc.get('discount_price') or 0
                discount_rate = acc.get('discount_rate') or 0
                
                Accessory.objects.get_or_create(
                    model=model_name,
                    device_type=device_type,
                    defaults={
                        'description': '',
                        'original_price': original_price,
                        'discount_price': discount_price,
                        'discount_rate': discount_rate,
                        'is_active': True
                    }
                )
                display_name = model_name[:50] + '...' if len(model_name) > 50 else model_name
                self.stdout.write(f"  ✓ Accessories: {display_name}")
            except Exception as e:
                self.stdout.write(self.style.WARNING(f"  ✗ Accessories导入失败"))
        
        self.stdout.write(f"  → 共导入 {len(accessories)} 个Accessories")