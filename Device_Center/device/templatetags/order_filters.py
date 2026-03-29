"""
Django 模板标签
"""
import json
from django import template

register = template.Library()

@register.filter
def parse_upgrades(value):
    """解析订单的升级选项JSON，返回格式化的HTML字符串"""
    if not value:
        return ''
    
    try:
        if isinstance(value, str):
            upgrades = json.loads(value)
        else:
            upgrades = value
        
        if not upgrades:
            return ''
        
        # 格式化每个升级选项
        upgrade_html = '<div class="upgrade-tags">'
        for upgrade in upgrades:
            if isinstance(upgrade, dict):
                name = upgrade.get('name', str(upgrade))
                price = upgrade.get('price', 0)
            else:
                name = str(upgrade)
                price = 0
            
            upgrade_html += f'<span class="upgrade-tag">+{name}'
            if price:
                upgrade_html += f' (¥{price:.2f})'
            upgrade_html += '</span>'
        
        upgrade_html += '</div>'
        return upgrade_html
    except (json.JSONDecodeError, TypeError, ValueError):
        # 如果解析失败，返回原始字符串
        return str(value) if value else ''

@register.filter
def format_upgrades_text(value):
    """将升级选项JSON转换为文本格式"""
    if not value:
        return '无'
    
    try:
        if isinstance(value, str):
            upgrades = json.loads(value)
        else:
            upgrades = value
        
        if not upgrades:
            return '无'
        
        # 格式化每个升级选项
        upgrade_parts = []
        for upgrade in upgrades:
            if isinstance(upgrade, dict):
                name = upgrade.get('name', str(upgrade))
                price = upgrade.get('price', 0)
            else:
                name = str(upgrade)
                price = 0
            
            if price:
                upgrade_parts.append(f"{name}(+¥{price:.2f})")
            else:
                upgrade_parts.append(name)
        
        return '、'.join(upgrade_parts)
    except (json.JSONDecodeError, TypeError, ValueError):
        return str(value) if value else '无'