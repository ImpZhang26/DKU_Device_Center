"""
Django management command to import Lenovo products from JSON file
"""
import json
import os
from django.core.management.base import BaseCommand
from django.db import models
from device.models import LenovoProduct


class Command(BaseCommand):
    help = 'Import Lenovo products from JSON data file'

    def add_arguments(self, parser):
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Clear existing Lenovo products before import',
        )

    def handle(self, *args, **options):
        # 获取JSON文件路径 - 项目根目录下的 jsonData 文件夹
        json_file = os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),  # device/
            '..', '..',  # 项目根目录
            'jsonData', 'lenovo.json'
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
            product_count = LenovoProduct.objects.count()
            LenovoProduct.objects.all().delete()
            self.stdout.write(self.style.SUCCESS(f'Cleared {product_count} Lenovo products'))
        
        # 导入数据
        total_products = 0
        
        for device_type, products in data.items():
            if not isinstance(products, list):
                continue
            
            for product_data in products:
                try:
                    # 获取型号名称
                    model_name = product_data.get('model', '')
                    if not model_name:
                        continue
                    
                    # 获取配置信息
                    configurations = product_data.get('configurations', [])
                    
                    # 如果有配置，逐一创建；否则创建一条记录
                    if isinstance(configurations, list) and len(configurations) > 0:
                        for idx, config_data in enumerate(configurations):
                            try:
                                # 使用 product_link 作为唯一标识，如果没有则使用索引
                                product_link = config_data.get('product_link', '').strip()
                                if product_link:
                                    # 通过 product_link 查找
                                    lookup_kwargs = {
                                        'device_type': device_type,
                                        'model': model_name,
                                        'product_link': product_link,
                                    }
                                else:
                                    # 没有 product_link 时，使用 (device_type, model) + CPU/Memory/硬盘 组合
                                    lookup_kwargs = {
                                        'device_type': device_type,
                                        'model': model_name,
                                        'cpu': config_data.get('cpu', '') or '',
                                        'memory': config_data.get('memory', '') or '',
                                        'hard_disk': config_data.get('hard_disk', '') or '',
                                    }
                                
                                product, created = LenovoProduct.objects.update_or_create(
                                    **lookup_kwargs,
                                    defaults={
                                        'brand': product_data.get('brand', 'Lenovo'),
                                        'configuration': config_data.get('configuration', 'Standard'),
                                        'cpu': config_data.get('cpu', ''),
                                        'memory': config_data.get('memory', ''),
                                        'hard_disk': config_data.get('hard_disk', ''),
                                        'screen': config_data.get('screen', ''),
                                        'wifi': config_data.get('wifi', ''),
                                        'weight': config_data.get('weight', ''),
                                        'accessary': config_data.get('accessary', ''),
                                        'configuration_parameters': config_data.get('configuration_parameters', ''),
                                        'changing_config_price': config_data.get('changing_config_price', ''),
                                        'discount_price': config_data.get('discount_price', 0),
                                        'original_price': config_data.get('original_price', 0),
                                        'discount_rate': config_data.get('discount_rate', 0) or 0,
                                        'graphic_card': config_data.get('graphic_card', ''),
                                    }
                                )
                                if created:
                                    total_products += 1
                                    self.stdout.write(f'  Created: {model_name} - {config_data.get("cpu", "Standard")} ({config_data.get("memory", "")})')
                                else:
                                    self.stdout.write(f'  Updated: {model_name} - {config_data.get("cpu", "Standard")} ({config_data.get("memory", "")})')
                            except Exception as e:
                                self.stderr.write(self.style.ERROR(f'Error importing {model_name} config {idx}: {e}'))
                    else:
                        # 无配置信息的情况
                        product, created = LenovoProduct.objects.update_or_create(
                            device_type=device_type,
                            model=model_name,
                            configuration='Standard',
                            defaults={
                                'brand': product_data.get('brand', 'Lenovo'),
                                'cpu': product_data.get('cpu', ''),
                                'memory': product_data.get('memory', ''),
                                'hard_disk': product_data.get('hard_disk', ''),
                                'graphic_card': product_data.get('graphic_card', ''),
                                'screen': product_data.get('screen', ''),
                                'wifi': product_data.get('wifi', ''),
                                'weight': product_data.get('weight', ''),
                                'accessary': product_data.get('accessary', ''),
                                'configuration_parameters': product_data.get('configuration_parameters', ''),
                                'changing_config_price': product_data.get('changing_config_price', ''),
                                'discount_price': product_data.get('discount_price', 0),
                                'original_price': product_data.get('original_price', 0),
                                'discount_rate': product_data.get('discount_rate', 0) or 0,
                                'product_link': product_data.get('product_link', ''),
                            }
                        )
                        if created:
                            total_products += 1
                            self.stdout.write(f'  Created: {model_name}')
                        
                except Exception as e:
                    self.stderr.write(self.style.ERROR(f'Error importing {product_data.get("model")}: {e}'))
        
        self.stdout.write(self.style.SUCCESS(f'\nSuccessfully imported {total_products} Lenovo products'))
        
        # 显示统计信息
        product_stats = LenovoProduct.objects.values('device_type').annotate(
            count=models.Count('id')
        ).order_by('device_type')
        
        self.stdout.write('\nProduct counts by type:')
        for stat in product_stats:
            self.stdout.write(f'  {stat["device_type"]}: {stat["count"]} products')