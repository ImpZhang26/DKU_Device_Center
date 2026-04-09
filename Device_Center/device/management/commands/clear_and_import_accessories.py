"""
清空 accessories 表并从 apple.json 重新导入
使用方式: python manage.py clear_and_import_accessories
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
from device.models import Accessory
from device.management.commands.import_apple_data import Command as ImportAppleCommand

class Command(BaseCommand):
    help = '清空 accessories 表并从 apple.json 重新导入数据'
    
    def handle(self, *args, **options):
        self.stdout.write("=" * 60)
        self.stdout.write("清空并重新导入 Accessories 数据")
        self.stdout.write("=" * 60)
        
        # 统计当前数据
        before_count = Accessory.objects.count()
        self.stdout.write(f"📊 清空前Accessories数量: {before_count}")
        
        if before_count > 0:
            deleted = Accessory.objects.all().delete()[0]
            self.stdout.write(f"🗑️  已删除 {deleted} 条Accessories记录")
        
        # 从 apple.json 读取数据
        json_path = '/Users/tz138/Desktop/DKU_Device_Center/Device_Center/jsonData/apple.json'
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        accessories_data = data.get('Accessories', [])
        self.stdout.write(f"📦 准备导入 {len(accessories_data)} 个Accessories")
        
        # 使用 import_apple_data 的逻辑导入（复用代码）
        importer = ImportAppleCommand()
        importer.import_accessories(accessories_data)
        
        # 统计导入后数据
        after_count = Accessory.objects.count()
        self.stdout.write(f"✅ 导入后Accessories数量: {after_count}")
        
        # 显示导入的Accessories列表
        self.stdout.write("\n📋 已导入Accessories列表:")
        for acc in Accessory.objects.all().order_by('device_type', 'model'):
            self.stdout.write(f"  • {acc.model} ({acc.device_type}) - ¥{acc.discount_price}")
        
        self.stdout.write("\n" + "=" * 60)
        self.stdout.write(self.style.SUCCESS("🎉 Accessories 表清理并重新导入完成！"))
        self.stdout.write("=" * 60)
        self.stdout.write("\n🔍 验证命令: python manage.py shell")
        self.stdout.write("   >>> from device.models import Accessory")
        self.stdout.write("   >>> Accessory.objects.count()  # 应显示 12")

