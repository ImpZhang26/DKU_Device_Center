"""
数据库连接和初始化模块
支持多数据库：system（系统数据）、apple、dell、lenovo（各品牌数据）
使用SQLite数据库
"""
import os
import sqlite3
from pathlib import Path

# 数据库Storage目录
DATABASES_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'Device_Center', 'databases')

def ensure_databases_dir():
    """确保数据库目录存在"""
    Path(DATABASES_DIR).mkdir(parents=True, exist_ok=True)

def get_connection(db_name):
    """
    获取数据库连接
    
    Args:
        db_name: 数据库名称 (system, apple, dell, lenovo)
    
    Returns:
        sqlite3.Connection 对象
    """
    ensure_databases_dir()
    
    db_path = os.path.join(DATABASES_DIR, f'{db_name}.db')
    
    # 连接数据库，启用外键约束
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    conn.execute('PRAGMA foreign_keys = ON')
    
    # 初始化数据库表（如果不存在）
    init_db(db_name, conn)
    
    return conn

def init_db(db_name, conn=None):
    """初始化数据库表结构"""
    if conn is None:
        conn = get_connection(db_name)
    
    cursor = conn.cursor()
    
    if db_name == 'system':
        # 系统数据库
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                netid TEXT UNIQUE NOT NULL,
                name TEXT NOT NULL,
                email TEXT,
                department TEXT,
                role TEXT DEFAULT 'staff',
                is_active INTEGER DEFAULT 1,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS admins (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                name TEXT NOT NULL,
                email TEXT,
                role TEXT DEFAULT 'admin',
                is_active INTEGER DEFAULT 1,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS orders (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                order_number TEXT UNIQUE NOT NULL,
                user_id INTEGER NOT NULL,
                brand TEXT NOT NULL,
                device_type TEXT,
                model_name TEXT NOT NULL,
                selected_cpu TEXT,
                selected_memory TEXT,
                selected_hard_disk TEXT,
                selected_graphic_card TEXT,
                selected_screen TEXT,
                total_price REAL,
                status TEXT DEFAULT 'pending',
                remark TEXT,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id)
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS cart_items (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                brand TEXT NOT NULL,
                device_type TEXT,
                model_name TEXT NOT NULL,
                configuration_id INTEGER,
                selected_config TEXT,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id)
            )
        ''')
        
        # 创建默认管理员账号（admin / admin123）
        import hashlib
        password_hash = hashlib.sha256('admin123'.encode()).hexdigest()
        cursor.execute('''
            INSERT OR IGNORE INTO admins (username, password_hash, name, role)
            VALUES (?, ?, ?, ?)
        ''', ('admin', password_hash, '系统管理员', 'super_admin'))
        
        # 创建测试用户
        cursor.execute('''
            INSERT OR IGNORE INTO users (netid, name, department, role)
            VALUES (?, ?, ?, ?)
        ''', ('testuser', '测试用户', '测试部门', 'staff'))
        
    elif db_name == 'apple':
        # Apple产品数据库
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS product_types (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                device_type TEXT UNIQUE NOT NULL,
                name TEXT NOT NULL,
                description TEXT,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS product_models (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                model_name TEXT NOT NULL,
                device_type TEXT NOT NULL,
                description TEXT,
                image_url TEXT,
                is_active INTEGER DEFAULT 1,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                UNIQUE(model_name, device_type)
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS product_configurations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                model_id INTEGER NOT NULL,
                configuration TEXT,
                cpu TEXT,
                memory TEXT,
                hard_disk TEXT,
                graphic_card TEXT,
                screen TEXT,
                original_price REAL,
                discount_price REAL,
                discount_rate REAL DEFAULT 0,
                is_active INTEGER DEFAULT 1,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (model_id) REFERENCES product_models(id)
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS accessories (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                model TEXT NOT NULL,
                device_type TEXT NOT NULL,
                description TEXT,
                original_price REAL,
                discount_price REAL,
                discount_rate REAL DEFAULT 0,
                is_active INTEGER DEFAULT 1,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS color_options (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                model_id INTEGER,
                color_name TEXT NOT NULL,
                color_hex TEXT,
                is_active INTEGER DEFAULT 1,
                FOREIGN KEY (model_id) REFERENCES product_models(id)
            )
        ''')
    
    elif db_name == 'dell':
        # Dell产品数据库
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS product_types (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                device_type TEXT UNIQUE NOT NULL,
                name TEXT NOT NULL,
                description TEXT,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS product_models (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                model_name TEXT NOT NULL,
                device_type TEXT NOT NULL,
                description TEXT,
                image_url TEXT,
                is_active INTEGER DEFAULT 1,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                UNIQUE(model_name, device_type)
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS product_configurations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                model_id INTEGER NOT NULL,
                configuration TEXT,
                cpu TEXT,
                memory TEXT,
                hard_disk TEXT,
                graphic_card TEXT,
                screen TEXT,
                original_price REAL,
                discount_price REAL,
                discount_rate REAL DEFAULT 0,
                is_active INTEGER DEFAULT 1,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (model_id) REFERENCES product_models(id)
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS accessories (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                model TEXT NOT NULL,
                device_type TEXT NOT NULL,
                description TEXT,
                original_price REAL,
                discount_price REAL,
                discount_rate REAL DEFAULT 0,
                is_active INTEGER DEFAULT 1,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
    
    elif db_name == 'lenovo':
        # Lenovo产品数据库
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS product_types (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                device_type TEXT UNIQUE NOT NULL,
                name TEXT NOT NULL,
                description TEXT,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS product_models (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                model_name TEXT NOT NULL,
                device_type TEXT NOT NULL,
                description TEXT,
                image_url TEXT,
                is_active INTEGER DEFAULT 1,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                UNIQUE(model_name, device_type)
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS product_configurations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                model_id INTEGER NOT NULL,
                configuration TEXT,
                cpu TEXT,
                memory TEXT,
                hard_disk TEXT,
                graphic_card TEXT,
                screen TEXT,
                original_price REAL,
                discount_price REAL,
                discount_rate REAL DEFAULT 0,
                is_active INTEGER DEFAULT 1,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (model_id) REFERENCES product_models(id)
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS accessories (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                model TEXT NOT NULL,
                device_type TEXT NOT NULL,
                description TEXT,
                original_price REAL,
                discount_price REAL,
                discount_rate REAL DEFAULT 0,
                is_active INTEGER DEFAULT 1,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
    
    conn.commit()
    
    # 如果是apple数据库，插入一些初始数据
    if db_name == 'apple' and conn is not None:
        init_apple_data(cursor)
        conn.commit()

def init_apple_data(cursor):
    """初始化Apple产品数据（如果表为空）"""
    # 检查是否已有数据
    cursor.execute('SELECT COUNT(*) FROM product_types')
    if cursor.fetchone()[0] > 0:
        return
    
    # 插入产品类型
    product_types = [
        ('Laptop', 'Laptop', 'MacBook Pro、MacBook Air'),
        ('Desktop', 'Desktop', 'iMac、Mac mini、Mac Studio、Mac Pro'),
        ('iPad', '平板电脑', 'iPad Pro、iPad Air、iPad、iPad mini'),
        ('Accessories', 'Accessories', '键盘、鼠标、触控板等Accessories')
    ]
    cursor.executemany(
        'INSERT OR IGNORE INTO product_types (device_type, name, description) VALUES (?, ?, ?)',
        product_types
    )
    
    # 插入型号
    models = [
        ('MacBook Pro 14"', 'Laptop', 'M3 Pro/MaxCPU，14.2英寸Liquid Retina XDRDisplay'),
        ('MacBook Pro 16"', 'Laptop', 'M3 Pro/MaxCPU，16.2英寸Liquid Retina XDRDisplay'),
        ('MacBook Air 13"', 'Laptop', 'M3CPU，13.6英寸Liquid RetinaDisplay'),
        ('iMac 24"', 'Desktop', 'M3CPU，24英寸4.5K RetinaDisplay'),
        ('Mac mini', 'Desktop', 'M2/M2 ProCPU，小巧机身强劲性能'),
        ('iPad Pro 12.9"', 'iPad', 'M2CPU，12.9英寸Liquid Retina XDRDisplay'),
        ('iPad Air', 'iPad', 'M1CPU，10.9英寸Liquid RetinaDisplay'),
        ('iPad', 'iPad', 'A14CPU，10.9英寸RetinaDisplay'),
    ]
    cursor.executemany(
        'INSERT OR IGNORE INTO product_models (model_name, device_type, description) VALUES (?, ?, ?)',
        models
    )
    
    # 获取型号ID
    cursor.execute('SELECT id, model_name, device_type FROM product_models')
    model_ids = {(row['model_name'], row['device_type']): row['id'] for row in cursor.fetchall()}
    
    # 插入配置
    configs = [
        # MacBook Pro 14"
        ('M3 Pro/18GB/512GB', model_ids[('MacBook Pro 14"', 'Laptop')], 'M3 Pro (11核CPU/14核GPU)', '18GB', '512GB SSD', '14核GPU', '14.2英寸XDR', 17999, 14999, 0.17),
        ('M3 Max/36GB/1TB', model_ids[('MacBook Pro 14"', 'Laptop')], 'M3 Max (14核CPU/30核GPU)', '36GB', '1TB SSD', '30核GPU', '14.2英寸XDR', 34999, 28999, 0.17),
        # MacBook Pro 16"
        ('M3 Pro/18GB/512GB', model_ids[('MacBook Pro 16"', 'Laptop')], 'M3 Pro (12核CPU/18核GPU)', '18GB', '512GB SSD', '18核GPU', '16.2英寸XDR', 23999, 19999, 0.17),
        ('M3 Max/36GB/1TB', model_ids[('MacBook Pro 16"', 'Laptop')], 'M3 Max (16核CPU/40核GPU)', '36GB', '1TB SSD', '40核GPU', '16.2英寸XDR', 38999, 31999, 0.18),
        # MacBook Air 13"
        ('M3/8GB/256GB', model_ids[('MacBook Air 13"', 'Laptop')], 'M3 (8核CPU/8核GPU)', '8GB', '256GB SSD', '8核GPU', '13.6英寸Retina', 8999, 7999, 0.11),
        ('M3/16GB/512GB', model_ids[('MacBook Air 13"', 'Laptop')], 'M3 (8核CPU/8核GPU)', '16GB', '512GB SSD', '8核GPU', '13.6英寸Retina', 12499, 10999, 0.12),
        # iMac 24"
        ('M3/8GB/256GB', model_ids[('iMac 24"', 'Desktop')], 'M3 (8核CPU/8核GPU)', '8GB', '256GB SSD', '集成GPU', '24英寸4.5K', 12999, 10999, 0.15),
        ('M3/16GB/512GB', model_ids[('iMac 24"', 'Desktop')], 'M3 (8核CPU/10核GPU)', '16GB', '512GB SSD', '10核GPU', '24英寸4.5K', 17499, 14999, 0.14),
        # iPad
        ('256GB', model_ids[('iPad Pro 12.9"', 'iPad')], 'M2', '8GB', '256GB', '-', '12.9英寸XDR', 9999, 9299, 0.07),
        ('512GB', model_ids[('iPad Pro 12.9"', 'iPad')], 'M2', '8GB', '512GB', '-', '12.9英寸XDR', 11499, 10499, 0.09),
        ('256GB', model_ids[('iPad Air', 'iPad')], 'M1', '8GB', '256GB', '-', '10.9英寸Retina', 5399, 4799, 0.11),
    ]
    cursor.executemany(
        'INSERT OR IGNORE INTO product_configurations (configuration, model_id, cpu, memory, hard_disk, graphic_card, screen, original_price, discount_price, discount_rate) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',
        configs
    )
    
    # 插入Accessories
    accessories = [
        ('Magic Keyboard', 'Keyboard', '带有Touch ID的妙控键盘', 899, 749, 0.17),
        ('Magic Mouse', 'Mouse', '妙控鼠标', 699, 579, 0.17),
        ('Magic Trackpad', 'Trackpad', '妙控触控板', 999, 849, 0.15),
        ('AirPods Pro', 'Audio', 'AirPods Pro (第二代)', 1899, 1799, 0.05),
        ('Apple Pencil Pro', 'Stylus', 'Apple Pencil Pro', 999, 999, 0.00),
    ]
    cursor.executemany(
        'INSERT OR IGNORE INTO accessories (model, device_type, description, original_price, discount_price, discount_rate) VALUES (?, ?, ?, ?, ?, ?)',
        accessories
    )

def close_connection(conn):
    """关闭数据库连接"""
    if conn:
        conn.close()