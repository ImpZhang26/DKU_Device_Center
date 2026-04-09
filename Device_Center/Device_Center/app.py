"""
学校电脑设备管理系统 - Flask主应用程序
"""
from flask import Flask, render_template, request, jsonify, session, redirect, url_for
import os
import json
import hashlib
from datetime import datetime

from database import get_connection

app = Flask(__name__)
app.secret_key = 'device_center_secret_key_2024'

# 配置
JSON_DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'jsonData')
TEMPLATE_DIR = os.path.join(os.path.dirname(__file__), 'templates')
STATIC_DIR = os.path.join(os.path.dirname(__file__), 'static')

app.template_folder = TEMPLATE_DIR
app.static_folder = STATIC_DIR

# ==================== 首页 ====================

@app.route('/')
def index():
    """首页 - 品牌选择"""
    return render_template('index.html')

# ==================== 登录页面 ====================

@app.route('/login')
def login():
    """登录页面"""
    return render_template('login.html')

@app.route('/api/netid-login', methods=['POST'])
def netid_login():
    """
    NETID一键登录
    教职工凭借学校NETID一键登录，无需注册
    """
    netid = request.json.get('netid', '').strip().lower()
    
    if not netid:
        return jsonify({'success': False, 'message': '请输入NETID'})
    
    # 连接系统数据库
    conn = get_connection('system')
    cursor = conn.cursor()
    
    # 查找用户
    cursor.execute('SELECT * FROM users WHERE netid = ? AND is_active = 1', (netid,))
    user = cursor.fetchone()
    
    if not user:
        # 新用户，自动创建账户
        cursor.execute('''
            INSERT INTO users (netid, name, department, role)
            VALUES (?, ?, ?, ?)
        ''', (netid, netid, '', 'staff'))
        conn.commit()
        cursor.execute('SELECT * FROM users WHERE netid = ?', (netid,))
        user = cursor.fetchone()
    
    conn.close()
    
    # 设置session
    session['user_id'] = dict(user)['id']
    session['netid'] = dict(user)['netid']
    session['name'] = dict(user)['name']
    session['role'] = dict(user)['role']
    session['login_type'] = 'netid'
    
    return jsonify({
        'success': True, 
        'message': '登录成功',
        'user': {
            'netid': dict(user)['netid'],
            'name': dict(user)['name']
        }
    })

@app.route('/api/admin-login', methods=['POST'])
def admin_login():
    """
    管理员登录
    """
    username = request.json.get('username', '').strip()
    password = request.json.get('password', '')
    
    if not username or not password:
        return jsonify({'success': False, 'message': '请输入用户名和密码'})
    
    # 连接系统数据库
    conn = get_connection('system')
    cursor = conn.cursor()
    
    # 查找管理员
    password_hash = hashlib.sha256(password.encode()).hexdigest()
    cursor.execute('''
        SELECT * FROM admins WHERE username = ? AND password_hash = ? AND is_active = 1
    ''', (username, password_hash))
    admin = cursor.fetchone()
    
    conn.close()
    
    if not admin:
        return jsonify({'success': False, 'message': '用户名或密码错误'})
    
    # 设置session
    session['user_id'] = dict(admin)['id']
    session['username'] = dict(admin)['username']
    session['name'] = dict(admin)['name']
    session['role'] = dict(admin)['role']
    session['login_type'] = 'admin'
    
    return jsonify({
        'success': True, 
        'message': '登录成功',
        'user': {
            'username': dict(admin)['username'],
            'name': dict(admin)['name']
        }
    })

@app.route('/api/logout', methods=['POST'])
def logout():
    """退出登录"""
    session.clear()
    return jsonify({'success': True, 'message': '已退出登录'})

@app.route('/api/check-login')
def check_login():
    """检查登录状态"""
    if 'user_id' in session:
        return jsonify({
            'logged_in': True,
            'login_type': session.get('login_type'),
            'user': {
                'netid': session.get('netid'),
                'username': session.get('username'),
                'name': session.get('name'),
                'role': session.get('role')
            }
        })
    return jsonify({'logged_in': False})

# ==================== Apple选配中心 ====================

@app.route('/apple')
def apple_center():
    """Apple选配中心首页"""
    return render_template('apple/index.html')

@app.route('/apple/laptop')
def apple_laptop():
    """AppleLaptop选配"""
    return render_template('apple/laptop.html')

@app.route('/apple/desktop')
def apple_desktop():
    """AppleDesktop选配"""
    return render_template('apple/desktop.html')

@app.route('/apple/ipad')
def apple_ipad():
    """Apple iPad选配"""
    return render_template('apple/ipad.html')

@app.route('/apple/accessories')
def apple_accessories():
    """AppleAccessories"""
    return render_template('apple/accessories.html')

# ==================== Apple API接口 ====================

@app.route('/api/apple/product-types')
def apple_product_types():
    """获取Apple产品类型"""
    conn = get_connection('apple')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM product_types ORDER BY id')
    types = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return jsonify({'success': True, 'data': types})

@app.route('/api/apple/models/<device_type>')
def apple_models(device_type):
    """获取指定产品类型的型号列表"""
    conn = get_connection('apple')
    cursor = conn.cursor()
    cursor.execute('''
        SELECT DISTINCT model_name FROM product_models 
        WHERE device_type = ? ORDER BY model_name
    ''', (device_type,))
    models = [row['model_name'] for row in cursor.fetchall()]
    conn.close()
    return jsonify({'success': True, 'data': models})

@app.route('/api/apple/model-info')
def apple_model_info():
    """获取型号详细信息"""
    model_name = request.args.get('model_name')
    device_type = request.args.get('device_type')
    
    if not model_name or not device_type:
        return jsonify({'success': False, 'message': '参数不完整'})
    
    conn = get_connection('apple')
    cursor = conn.cursor()
    cursor.execute('''
        SELECT * FROM product_models 
        WHERE model_name = ? AND device_type = ?
    ''', (model_name, device_type))
    model = cursor.fetchone()
    conn.close()
    
    if model:
        return jsonify({'success': True, 'data': dict(model)})
    return jsonify({'success': False, 'message': '型号不存在'})

@app.route('/api/apple/configurations')
def apple_configurations():
    """获取型号的配置列表"""
    model_name = request.args.get('model_name')
    device_type = request.args.get('device_type')
    
    if not model_name or not device_type:
        return jsonify({'success': False, 'message': '参数不完整'})
    
    conn = get_connection('apple')
    cursor = conn.cursor()
    cursor.execute('''
        SELECT pc.* FROM product_configurations pc
        JOIN product_models pm ON pc.model_id = pm.id
        WHERE pm.model_name = ? AND pm.device_type = ?
    ''', (model_name, device_type))
    configs = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return jsonify({'success': True, 'data': configs})

@app.route('/api/apple/accessories')
def apple_accessories_list():
    """获取Accessories列表"""
    conn = get_connection('apple')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM accessories ORDER BY model')
    accessories = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return jsonify({'success': True, 'data': accessories})

@app.route('/api/apple/selection-options')
def apple_selection_options():
    """
    获取选配参数选项
    用于前端构建选配下拉框
    """
    model_name = request.args.get('model_name')
    device_type = request.args.get('device_type')
    
    if not model_name or not device_type:
        return jsonify({'success': False, 'message': '参数不完整'})
    
    conn = get_connection('apple')
    cursor = conn.cursor()
    cursor.execute('''
        SELECT DISTINCT cpu, memory, hard_disk, graphic_card, screen 
        FROM product_configurations pc
        JOIN product_models pm ON pc.model_id = pm.id
        WHERE pm.model_name = ? AND pm.device_type = ?
    ''', (model_name, device_type))
    
    options = {
        'cpus': set(),
        'memories': set(),
        'hard_disks': set(),
        'graphic_cards': set(),
        'screens': set()
    }
    
    for row in cursor.fetchall():
        if row['cpu']:
            options['cpus'].add(row['cpu'])
        if row['memory']:
            options['memories'].add(row['memory'])
        if row['hard_disk']:
            options['hard_disks'].add(row['hard_disk'])
        if row['graphic_card']:
            options['graphic_cards'].add(row['graphic_card'])
        if row['screen']:
            options['screens'].add(row['screen'])
    
    conn.close()
    
    # 转换为排序后的列表
    result = {
        'cpu': sorted(list(options['cpus'])),
        'memory': sorted(list(options['memories']), key=lambda x: (len(x.split()), x)),
        'hard_disk': sorted(list(options['hard_disks'])),
        'graphic_card': sorted(list(options['graphic_cards'])),
        'screen': sorted(list(options['screens']))
    }
    
    return jsonify({'success': True, 'data': result})

# ==================== 购物车相关 ====================

@app.route('/api/cart/add', methods=['POST'])
def cart_add():
    """添加购物车"""
    if 'user_id' not in session:
        return jsonify({'success': False, 'message': '请先登录'})
    
    data = request.json
    conn = get_connection('system')
    cursor = conn.cursor()
    
    cursor.execute('''
        INSERT INTO cart_items (user_id, brand, device_type, model_name, 
                               configuration_id, selected_config)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (
        session['user_id'],
        data.get('brand'),
        data.get('device_type'),
        data.get('model_name'),
        data.get('configuration_id'),
        json.dumps(data.get('selected_config', {}))
    ))
    
    conn.commit()
    conn.close()
    
    return jsonify({'success': True, 'message': '已加入购物车'})

@app.route('/api/cart/list')
def cart_list():
    """获取购物车列表"""
    if 'user_id' not in session:
        return jsonify({'success': False, 'message': '请先登录', 'data': []})
    
    conn = get_connection('system')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM cart_items WHERE user_id = ?', (session['user_id'],))
    items = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return jsonify({'success': True, 'data': items})

@app.route('/api/cart/remove/<int:item_id>', methods=['DELETE'])
def cart_remove(item_id):
    """删除购物车项"""
    if 'user_id' not in session:
        return jsonify({'success': False, 'message': '请先登录'})
    
    conn = get_connection('system')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM cart_items WHERE id = ? AND user_id = ?', 
                  (item_id, session['user_id']))
    conn.commit()
    conn.close()
    return jsonify({'success': True, 'message': '已删除'})

# ==================== 订单相关 ====================

@app.route('/api/order/create', methods=['POST'])
def order_create():
    """创建订单"""
    if 'user_id' not in session:
        return jsonify({'success': False, 'message': '请先登录'})
    
    from uuid import uuid4
    
    data = request.json
    order_number = f"DC{datetime.now().strftime('%Y%m%d%H%M%S')}{str(uuid4())[:4].upper()}"
    
    conn = get_connection('system')
    cursor = conn.cursor()
    
    cursor.execute('''
        INSERT INTO orders (order_number, user_id, brand, device_type, model_name,
                          selected_cpu, selected_memory, selected_hard_disk,
                          selected_graphic_card, selected_screen, total_price, remark)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        order_number,
        session['user_id'],
        data.get('brand'),
        data.get('device_type'),
        data.get('model_name'),
        data.get('cpu'),
        data.get('memory'),
        data.get('hard_disk'),
        data.get('graphic_card'),
        data.get('screen'),
        data.get('total_price'),
        data.get('remark')
    ))
    
    conn.commit()
    conn.close()
    
    return jsonify({'success': True, 'message': '订单创建成功', 'order_number': order_number})

@app.route('/api/orders')
def order_list():
    """获取订单列表"""
    if 'user_id' not in session:
        return jsonify({'success': False, 'message': '请先登录', 'data': []})
    
    conn = get_connection('system')
    cursor = conn.cursor()
    
    # 管理员可以看到所有订单
    if session.get('role') in ['admin', 'super_admin']:
        cursor.execute('SELECT * FROM orders ORDER BY created_at DESC')
    else:
        cursor.execute('SELECT * FROM orders WHERE user_id = ? ORDER BY created_at DESC', 
                      (session['user_id'],))
    
    orders = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return jsonify({'success': True, 'data': orders})

# ==================== 管理页面 ====================

@app.route('/admin')
def admin_dashboard():
    """管理后台首页"""
    if session.get('role') not in ['admin', 'super_admin']:
        return redirect(url_for('login'))
    return render_template('admin/dashboard.html')

@app.route('/admin/orders')
def admin_orders():
    """订单管理"""
    if session.get('role') not in ['admin', 'super_admin']:
        return redirect(url_for('login'))
    return render_template('admin/orders.html')

@app.route('/admin/products')
def admin_products():
    """产品管理"""
    if session.get('role') not in ['admin', 'super_admin']:
        return redirect(url_for('login'))
    return render_template('admin/products.html')

@app.route('/admin/users')
def admin_users():
    """用户管理"""
    if session.get('role') not in ['admin', 'super_admin']:
        return redirect(url_for('login'))
    return render_template('admin/users.html')

# ==================== 错误处理 ====================

@app.errorhandler(404)
def page_not_found(e):
    return render_template('error.html', error='页面不存在'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('error.html', error='服务器错误'), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)