"""
初始化测试数据脚本
用于快速填充数据库测试数据
"""
import sys
import os

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database import get_connection


def init_test_data():
    """初始化测试数据"""
    
    # ========== Apple 数据库测试数据 ==========
    print("正在初始化 Apple 数据库...")
    conn = get_connection('apple')
    cursor = conn.cursor()
    
    # 产品类型
    product_types = [
        ('Laptop', 'Laptop', 'MacBook Pro、MacBook Air'),
        ('Desktop', '台式机', 'iMac、Mac mini、Mac Studio、Mac Pro'),
        ('iPad', '平板电脑', 'iPad Pro、iPad Air、iPad、iPad mini'),
        ('Accessories', '配件', '键盘、鼠标、触控板等配件')
    ]
    cursor.executemany(
        'INSERT OR REPLACE INTO product_types (device_type, name, description) VALUES (?, ?, ?)',
        product_types
    )
    
    # 型号数据 - Laptop
    laptops = [
        ('MacBook Pro 14"', 'Laptop', 'M3 Pro/MaxCPU，14.2英寸Liquid Retina XDRDisplay'),
        ('MacBook Pro 16"', 'Laptop', 'M3 Pro/MaxCPU，16.2英寸Liquid Retina XDRDisplay'),
        ('MacBook Air 13"', 'Laptop', 'M3CPU，13.6英寸Liquid RetinaDisplay'),
        ('MacBook Air 15"', 'Laptop', 'M3CPU，15.3英寸Liquid RetinaDisplay'),
    ]
    for model, dtype, desc in laptops:
        cursor.execute('INSERT OR REPLACE INTO product_models (model_name, device_type, description) VALUES (?, ?, ?)',
                      (model, dtype, desc))
    
    # 型号数据 - 台式机
    desktops = [
        ('iMac 24"', 'Desktop', 'M3CPU，24英寸4.5K RetinaDisplay'),
        ('Mac mini', 'Desktop', 'M2/M2 ProCPU，小巧机身强劲性能'),
        ('Mac Studio', 'Desktop', 'M2 Max/UltraCPU，专业工作室级性能'),
        ('Mac Pro', 'Desktop', 'M2 UltraCPU，最强性能专业工作站'),
    ]
    for model, dtype, desc in desktops:
        cursor.execute('INSERT OR REPLACE INTO product_models (model_name, device_type, description) VALUES (?, ?, ?)',
                      (model, dtype, desc))
    
    # 型号数据 - iPad
    ipads = [
        ('iPad Pro 12.9"', 'iPad', 'M2CPU，12.9英寸Liquid Retina XDRDisplay'),
        ('iPad Pro 11"', 'iPad', 'M2CPU，11英寸Liquid RetinaDisplay'),
        ('iPad Air', 'iPad', 'M1CPU，10.9英寸Liquid RetinaDisplay'),
        ('iPad', 'iPad', 'A14CPU，10.9英寸RetinaDisplay'),
        ('iPad mini', 'iPad', 'A15CPU，8.3英寸Liquid RetinaDisplay'),
    ]
    for model, dtype, desc in ipads:
        cursor.execute('INSERT OR REPLACE INTO product_models (model_name, device_type, description) VALUES (?, ?, ?)',
                      (model, dtype, desc))
    
    conn.commit()
    
    # 获取型号ID映射
    cursor.execute('SELECT id, model_name, device_type FROM product_models')
    model_ids = {(row['model_name'], row['device_type']): row['id'] for row in cursor.fetchall()}
    
    # 配置数据 - MacBook Pro 14"
    mbp14_configs = [
        ('M3 Pro/18GB/512GB', model_ids[('MacBook Pro 14"', 'Laptop')], 'M3 Pro (11核CPU/14核GPU)', '18GB', '512GB SSD', '14核GPU', '14.2英寸Liquid Retina XDR', 14999, 17999, 0.15),
        ('M3 Pro/18GB/1TB', model_ids[('MacBook Pro 14"', 'Laptop')], 'M3 Pro (11核CPU/14核GPU)', '18GB', '1TB SSD', '14核GPU', '14.2英寸Liquid Retina XDR', 16999, 19999, 0.15),
        ('M3 Pro/36GB/1TB', model_ids[('MacBook Pro 14"', 'Laptop')], 'M3 Pro (12核CPU/18核GPU)', '36GB', '1TB SSD', '18核GPU', '14.2英寸Liquid Retina XDR', 22999, 26999, 0.15),
        ('M3 Max/36GB/1TB', model_ids[('MacBook Pro 14"', 'Laptop')], 'M3 Max (14核CPU/30核GPU)', '36GB', '1TB SSD', '30核GPU', '14.2英寸Liquid Retina XDR', 28999, 34999, 0.17),
    ]
    cursor.executemany(
        'INSERT OR REPLACE INTO product_configurations (configuration, model_id, cpu, memory, hard_disk, graphic_card, screen, original_price, discount_price, discount_rate) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',
        mbp14_configs
    )
    
    # 配置数据 - MacBook Pro 16"
    mbp16_configs = [
        ('M3 Pro/18GB/512GB', model_ids[('MacBook Pro 16"', 'Laptop')], 'M3 Pro (12核CPU/18核GPU)', '18GB', '512GB SSD', '18核GPU', '16.2英寸Liquid Retina XDR', 19999, 23999, 0.17),
        ('M3 Pro/36GB/1TB', model_ids[('MacBook Pro 16"', 'Laptop')], 'M3 Pro (12核CPU/18核GPU)', '36GB', '1TB SSD', '18核GPU', '16.2英寸Liquid Retina XDR', 24999, 28999, 0.14),
        ('M3 Max/36GB/1TB', model_ids[('MacBook Pro 16"', 'Laptop')], 'M3 Max (16核CPU/40核GPU)', '36GB', '1TB SSD', '40核GPU', '16.2英寸Liquid Retina XDR', 31999, 38999, 0.18),
        ('M3 Max/64GB/2TB', model_ids[('MacBook Pro 16"', 'Laptop')], 'M3 Max (16核CPU/40核GPU)', '64GB', '2TB SSD', '40核GPU', '16.2英寸Liquid Retina XDR', 41999, 49999, 0.16),
    ]
    cursor.executemany(
        'INSERT OR REPLACE INTO product_configurations (configuration, model_id, cpu, memory, hard_disk, graphic_card, screen, original_price, discount_price, discount_rate) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',
        mbp16_configs
    )
    
    # 配置数据 - MacBook Air 13"
    mba13_configs = [
        ('M3/8GB/256GB', model_ids[('MacBook Air 13"', 'Laptop')], 'M3 (8核CPU/8核GPU)', '8GB', '256GB SSD', '8核GPU', '13.6英寸Liquid Retina', 7999, 8999, 0.11),
        ('M3/16GB/512GB', model_ids[('MacBook Air 13"', 'Laptop')], 'M3 (8核CPU/8核GPU)', '16GB', '512GB SSD', '8核GPU', '13.6英寸Liquid Retina', 10999, 12499, 0.12),
    ]
    cursor.executemany(
        'INSERT OR REPLACE INTO product_configurations (configuration, model_id, cpu, memory, hard_disk, graphic_card, screen, original_price, discount_price, discount_rate) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',
        mba13_configs
    )
    
    # 配置数据 - iMac 24"
    imac_configs = [
        ('M3/8GB/256GB', model_ids[('iMac 24"', 'Desktop')], 'M3 (8核CPU/8核GPU)', '8GB', '256GB SSD', '集成GPU', '24英寸4.5K Retina', 10999, 12999, 0.15),
        ('M3/16GB/512GB', model_ids[('iMac 24"', 'Desktop')], 'M3 (8核CPU/10核GPU)', '16GB', '512GB SSD', '10核GPU', '24英寸4.5K Retina', 14999, 17499, 0.14),
    ]
    cursor.executemany(
        'INSERT OR REPLACE INTO product_configurations (configuration, model_id, cpu, memory, hard_disk, graphic_card, screen, original_price, discount_price, discount_rate) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',
        imac_configs
    )
    
    # 配置数据 - iPad
    ipad_configs = [
        ('256GB', model_ids[('iPad Pro 12.9"', 'iPad')], 'M2', '8GB', '256GB', '-', '12.9英寸XDR', 9299, 9999, 0.07),
        ('512GB', model_ids[('iPad Pro 12.9"', 'iPad')], 'M2', '8GB', '512GB', '-', '12.9英寸XDR', 10499, 11499, 0.09),
        ('256GB', model_ids[('iPad Air', 'iPad')], 'M1', '8GB', '256GB', '-', '10.9英寸Retina', 4799, 5399, 0.11),
        ('64GB', model_ids[('iPad', 'iPad')], 'A14', '4GB', '64GB', '-', '10.9英寸Retina', 3599, 3999, 0.10),
    ]
    cursor.executemany(
        'INSERT OR REPLACE INTO product_configurations (configuration, model_id, cpu, memory, hard_disk, graphic_card, screen, original_price, discount_price, discount_rate) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',
        ipad_configs
    )
    
    # 配件数据
    accessories = [
        ('Magic Keyboard', 'Keyboard', '带有Touch ID的妙控键盘', 749, 899, 0.17),
        ('Magic Mouse', 'Mouse', '妙控鼠标', 579, 699, 0.17),
        ('Magic Trackpad', 'Trackpad', '妙控触控板', 849, 999, 0.15),
        ('AirPods Pro', 'Audio', 'AirPods Pro (第二代) 带USB-C充电盒', 1799, 1899, 0.05),
        ('Apple Pencil Pro', 'Stylus', 'Apple Pencil Pro', 999, 999, 0.00),
        ('USB-C to Lightning', 'Cable', 'USB-C转闪电连接线 (1米)', 243, 289, 0.16),
    ]
    cursor.executemany(
        'INSERT OR REPLACE INTO accessories (model, device_type, description, discount_price, original_price, discount_rate) VALUES (?, ?, ?, ?, ?, ?)',
        accessories
    )
    
    conn.commit()
    conn.close()
    print("✓ Apple 数据库测试数据初始化完成")
    
    # ========== System 数据库测试数据 ==========
    print("正在初始化 System 数据库...")
    conn = get_connection('system')
    cursor = conn.cursor()
    
    # 创建测试用户
    cursor.execute('''CREATE TABLE IF NOT EXISTS test_users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        netid TEXT UNIQUE,
        name TEXT,
        email TEXT,
        department TEXT,
        role TEXT DEFAULT 'staff',
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP
    )''')
    
    # 添加一些测试用户
    test_users = [
        ('zhangsan', '张三', 'zhangsan@school.edu.cn', '计算机学院', 'staff'),
        ('lisi', '李四', 'lisi@school.edu.cn', '数学学院', 'staff'),
        ('wangwu', '王五', 'wangwu@school.edu.cn', '物理学院', 'staff'),
    ]
    cursor.executemany(
        'INSERT OR IGNORE INTO test_users (netid, name, email, department, role) VALUES (?, ?, ?, ?, ?)',
        test_users
    )
    
    conn.commit()
    conn.close()
    print("✓ System 数据库测试数据初始化完成")
    
    print("\n" + "="*50)
    print("测试数据初始化完成！")
    print("="*50)
    print("\n可使用以下测试账号登录：")
    print("  NETID登录: zhangsan, lisi, wangwu (任意输入即可)")
    print("  管理员登录: admin / admin123")


if __name__ == '__main__':
    init_test_data()