"""
邮件发送工具模块
用于发送订单通知邮件
"""
import smtplib
import json
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formataddr
from email.header import Header

# ==================== SMTP 配置 ====================
SMTP_SERVER = "smtp.163.com"
SMTP_PORT = 25
FROM_ADDR = "ip_pingfail_alert@163.com"
FROM_PASSWORD = "EHJNGRYACAODBKMS"
FROM_DISPLAY_NAME = "Device Center Support System"

# 邮件收件人配置
CC_RECIPIENTS = ["tz138@duke.edu"]
RECIPIENTS = ["tz138@duke.edu"]  # 主收件人


def _format_addr(name, email):
    """格式化发件人/收件人显示名称"""
    if name:
        return formataddr((Header(name, 'utf-8').encode(), email))
    return email


def send_order_email(order_data):
    """
    发送订单确认邮件
    
    Args:
        order_data: 订单数据字典，包含以下字段:
            - order_number: 订单号
            - user_id: 用户ID
            - user_name: 用户姓名
            - user_email: 用户邮箱
            - brand: 品牌 (apple/dell/lenovo)
            - model_name: 型号名称
            - cpu: CPU配置
            - memory: 内存配置
            - hard_disk: 硬盘配置
            - graphic_card: 显卡配置
            - screen: 屏幕配置
            - base_price: 基础价格
            - upgrade_price: 升级价格
            - total_price: 总价
            - selected_upgrades: 升级选项列表 (可选)
            - status: 订单状态
            - created_at: 创建时间
    
    Returns:
        bool: 发送是否成功
    """
    try:
        # 构建邮件主题
        subject = 'Device Center Orders Info'
        
        # 构建邮件正文
        html_body = _build_order_email_html(order_data)
        
        # 创建邮件对象
        msg = MIMEMultipart('alternative')
        msg['Subject'] = subject
        msg['From'] = _format_addr(FROM_DISPLAY_NAME, FROM_ADDR)
        msg['To'] = ', '.join(RECIPIENTS)
        msg['Cc'] = ', '.join(CC_RECIPIENTS)
        
        # 添加HTML正文
        msg.attach(MIMEText(html_body, 'html', 'utf-8'))
        
        # 准备收件人列表（To + Cc）
        all_recipients = RECIPIENTS + CC_RECIPIENTS
        
        # 发送邮件
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.set_debuglevel(0)  # 0 for production, 1 for debugging
        server.login(FROM_ADDR, FROM_PASSWORD)
        server.sendmail(FROM_ADDR, all_recipients, msg.as_string())
        server.quit()
        
        print(f"订单邮件发送成功: {order_data.get('order_number', 'Unknown')}")
        return True
        
    except Exception as e:
        print(f"订单邮件发送失败: {str(e)}")
        return False


def _build_order_email_html(order_data):
    """
    构建订单邮件的HTML内容
    
    Args:
        order_data: 订单数据字典
    
    Returns:
        str: HTML格式的邮件内容
    """
    # 解析升级选项
    selected_upgrades = order_data.get('selected_upgrades', [])
    if isinstance(selected_upgrades, str):
        try:
            selected_upgrades = json.loads(selected_upgrades)
        except (json.JSONDecodeError, TypeError):
            selected_upgrades = []
    
    # 格式化升级选项列表
    upgrades_html = ''
    if selected_upgrades:
        upgrades_html = '<ul>'
        for upgrade in selected_upgrades:
            if isinstance(upgrade, dict):
                name = upgrade.get('name', str(upgrade))
                price = upgrade.get('price', '')
            else:
                name = str(upgrade)
                price = ''
            upgrades_html += f'<li>{name} {price}</li>'
        upgrades_html += '</ul>'
    else:
        upgrades_html = '<p>无</p>'
    
    # 格式化价格
    base_price = order_data.get('base_price', 0)
    upgrade_price = order_data.get('upgrade_price', 0)
    total_price = order_data.get('total_price', 0)
    
    # 格式化时间
    created_at = order_data.get('created_at', '')
    if hasattr(created_at, 'strftime'):
        created_at = created_at.strftime('%Y-%m-%d %H:%M:%S')
    
    # 状态映射
    status_map = {
        'pending': '待处理',
        'processing': '处理中',
        'completed': '已完成',
        'cancelled': '已终止',
    }
    status = order_data.get('status', 'pending')
    status_text = status_map.get(status, status)
    
    # 品牌显示名称
    brand_display = {
        'apple': 'Apple',
        'dell': 'Dell',
        'lenovo': 'Lenovo',
    }.get(order_data.get('brand', ''), order_data.get('brand', '')).upper()
    
    html = f'''<!DOCTYPE html>
<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
<style type="text/css">
    body {{ text-align: left; margin: 0px auto; padding: 20px; font: 13px 'Lucida Grande', 'Lucida Sans Unicode', Helvetica, Arial, sans-serif; }}
    p, table, tr, th, td {{ margin: 0; padding: 0; font-weight: normal; }}
    table {{ border-collapse: collapse; margin-bottom: 15px; width: 100%; }}
    th, td {{ padding: 8px; border: 1px solid #ddd; text-align: left; }}
    th {{ background-color: #f5f5f5; font-weight: bold; }}
    .header {{ background-color: #0070C0; color: white; }}
    .section-title {{ background-color: #E6F2FF; font-weight: bold; }}
    .price-row td {{ font-weight: bold; }}
    .total-row {{ background-color: #FFF2CC; }}
    .total-row td {{ font-weight: bold; font-size: 14px; }}
    .status {{ padding: 4px 8px; border-radius: 4px; background-color: #28a745; color: white; }}
</style>
</head>
<body>
    <p>Dear Team:</p>
    <br/>
    <p>&nbsp;&nbsp;&nbsp;&nbsp;Device Center 收到新订单，请查看详细信息。</p>
    <br/>
    
    <table border="1">
        <tr>
            <th colspan="2" class="header" align="center">订单信息</th>
        </tr>
        <tr>
            <th width="25%">订单号</th>
            <td><strong>{order_data.get('order_number', 'N/A')}</strong></td>
        </tr>
        <tr>
            <th>创建时间</th>
            <td>{created_at}</td>
        </tr>
        <tr>
            <th>订单状态</th>
            <td><span class="status">{status_text}</span></td>
        </tr>
        <tr>
            <th>品牌</th>
            <td>{brand_display}</td>
        </tr>
    </table>
    
    <br/>
    
    <table border="1">
        <tr>
            <th colspan="2" class="section-title" align="center">用户信息</th>
        </tr>
        <tr>
            <th width="25%">用户ID</th>
            <td>{order_data.get('user_id', 'N/A')}</td>
        </tr>
        <tr>
            <th>用户姓名</th>
            <td>{order_data.get('user_name', 'N/A')}</td>
        </tr>
        <tr>
            <th>用户邮箱</th>
            <td>{order_data.get('user_email', 'N/A')}</td>
        </tr>
    </table>
    
    <br/>
    
    <table border="1">
        <tr>
            <th colspan="2" class="section-title" align="center">产品配置</th>
        </tr>
        <tr>
            <th width="25%">型号名称</th>
            <td><strong>{order_data.get('model_name', 'N/A')}</strong></td>
        </tr>
        <tr>
            <th>CPU</th>
            <td>{order_data.get('cpu', 'N/A')}</td>
        </tr>
        <tr>
            <th>内存</th>
            <td>{order_data.get('memory', 'N/A')}</td>
        </tr>
        <tr>
            <th>硬盘</th>
            <td>{order_data.get('hard_disk', 'N/A')}</td>
        </tr>
        <tr>
            <th>显卡</th>
            <td>{order_data.get('graphic_card', 'N/A')}</td>
        </tr>
        <tr>
            <th>屏幕</th>
            <td>{order_data.get('screen', 'N/A')}</td>
        </tr>
    </table>
    
    <br/>
    
    <table border="1">
        <tr>
            <th colspan="2" class="section-title" align="center">升级选项</th>
        </tr>
        <tr>
            <th width="25%">已选升级</th>
            <td>{upgrades_html}</td>
        </tr>
    </table>
    
    <br/>
    
    <table border="1">
        <tr>
            <th colspan="2" class="section-title" align="center">价格明细</th>
        </tr>
        <tr>
            <th width="25%">基础价格</th>
            <td>¥{base_price}</td>
        </tr>
        <tr>
            <th>升级费用</th>
            <td>¥{upgrade_price}</td>
        </tr>
        <tr class="total-row">
            <th>总价</th>
            <td>¥{total_price}</td>
        </tr>
    </table>
    
    <br/>
    
    <p>--</p>
    <p>Device Center 自动发送</p>
</body>
</html>'''
    
    return html