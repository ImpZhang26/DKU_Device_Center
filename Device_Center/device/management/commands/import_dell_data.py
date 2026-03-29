"""
Django management command to import Dell products from JSON file
"""
import json
import os
from django.core.management.base import BaseCommand
from django.db import models
from device.models import DellProduct


class Command(BaseCommand):
    help = 'Import Dell products from JSON data file'

    def add_arguments(self, parser):
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Clear existing Dell products before import',
        )

    def handle(self, *args, **options):
        # 获取JSON文件路径 - 项目根目录下的 jsonData 文件夹
        json_file = os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),  # device/
            '..', '..',  # 项目根目录
            'jsonData', 'dell.json'
        )
        
        if not os.path.exists(json_file):
            self.stderr.write(self.style.ERROR(f'JSON file not found: {json_file}'))
            return
        
        # 读取JSON数据
        try:
            with open(json_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except Exception as e:
            self.stderr.write(self.style.ERROR(f'Failed to read JSON file: {e}'))
            return
        
        # 清空现有数据
        if options['clear']:
            count = DellProduct.objects.count()
            DellProduct.objects.all().delete()
            self.stdout.write(self.style.SUCCESS(f'Cleared {count} existing products'))
        
        # 导入数据
        total_imported = 0
        
        for category, products in data.items():
            if not isinstance(products, list):
                continue
                
            for product_data in products:
                try:
                    # 创建产品记录
                    product, created = DellProduct.objects.update_or_create(
                        model=product_data.get('model', ''),
                        defaults={
                            'device_type': product_data.get('device_type', category),
                            'brand': product_data.get('brand', 'DELL'),
                            'basic_config': product_data.get('basic_config', ''),
                            'cpu': product_data.get('cpu', ''),
                            'memory': product_data.get('memory', ''),
                            'hard_disk': product_data.get('hard_disk', ''),
                            'graphic_card': product_data.get('graphic_card', ''),
                            'wifi': product_data.get('wifi', ''),
                            'configuration_parameters': product_data.get('configuration_parameters', ''),
                            'weight': product_data.get('weight', ''),
                            'official_link': product_data.get('official_link', ''),
                            'price': product_data.get('price', 0),
                            'original_price': product_data.get('original_price', 0),
                            'discount_rate': product_data.get('discount_rate', 0) or 0,
                            'changing_config_price': product_data.get('changing_config_price', ''),
                            'remark': product_data.get('remark', ''),
                        }
                    )
                    
                    if created:
                        total_imported += 1
                        self.stdout.write(f'  Created: {product.model}')
                    else:
                        self.stdout.write(f'  Updated: {product.model}')
                        
                except Exception as e:
                    self.stderr.write(self.style.ERROR(f'Error importing {product_data.get("model")}: {e}'))
        
        self.stdout.write(self.style.SUCCESS(f'\nSuccessfully imported {total_imported} Dell products'))
        
        # 显示统计信息
        stats = DellProduct.objects.values('device_type').annotate(
            count=models.Count('id')
        ).order_by('device_type')
        
        self.stdout.write('\nProduct counts by type:')
        for stat in stats:
            self.stdout.write(f'  {stat["device_type"]}: {stat["count"]} products')