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
ADMIN_RECIPIENTS = ["tz138@duke.edu"]  # Admin CC


def _format_addr(name, email):
    """格式化发件人/收件人显示名称"""
    if name:
        return formataddr((Header(name, 'utf-8').encode(), email))
    return email


def send_order_email(order_data):
    """
    发送订单确认邮件: 用户友好版 + 管理员通知版
    
    Args:
        order_data: 订单数据字典
    Returns:
        bool: 发送是否成功
    """
    try:
        user_email = order_data.get('user_email', '').strip()
        success = True
        
        # 1. 发送用户邮件 (友好版)
        if user_email:
            user_result = _send_user_email(order_data)
            success = success and user_result
            print(f"用户邮件: {'成功' if user_result else '失败'}")
        else:
            print("No user_email, skipping user email")
        
        # 2. 发送管理员邮件 (通知版)
        admin_result = _send_admin_email(order_data)
        success = success and admin_result
        print(f"管理员邮件: {'成功' if admin_result else '失败'}")
        
        return success
        
    except Exception as e:
        print(f"订单邮件发送失败: {str(e)}")
        return False


def _build_user_email_html(order_data):
    """
    构建用户订单确认邮件 (友好版本)
    """
    # 解析升级选项 (unchanged - keep existing logic)
    selected_upgrades = order_data.get('selected_upgrades', [])
    if isinstance(selected_upgrades, str):
        try:
            selected_upgrades = json.loads(selected_upgrades)
        except:
            selected_upgrades = []
    
    upgrades_html = ''
    upgrade_price = order_data.get('upgrade_price', 0)
    if selected_upgrades and upgrade_price > 0:
        upgrades_html = '<ul>'
        for upgrade in selected_upgrades:
            name = upgrade.get('name', str(upgrade)) if isinstance(upgrade, dict) else str(upgrade)
            upgrades_html += f'<li>{name}</li>'
        upgrades_html += '</ul>'
    
    base_price = order_data.get('base_price', 0)
    total_price = order_data.get('total_price', 0)
    created_at = order_data.get('created_at', '')
    if hasattr(created_at, 'strftime'):
        created_at = created_at.strftime('%Y-%m-%d %H:%M')
    
    brand_display = {
        'apple': 'Apple', 'dell': 'Dell', 'lenovo': 'Lenovo'
    }.get(order_data.get('brand', ''), 'Device Center')
    
    html = f'''
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <style>
            body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; line-height: 1.6; color: #333; max-width: 600px; margin: 0 auto; padding: 20px; }}
            .header {{ background: linear-gradient(135deg, #007AFF, #5856D6); color: white; padding: 30px; text-align: center; border-radius: 12px 12px 0 0; }}
            .content {{ background: #f8f9fa; padding: 30px; border-radius: 0 0 12px 12px; }}
            .order-number {{ font-size: 24px; font-weight: bold; color: #007AFF; }}
            .status {{ padding: 8px 16px; background: #E8F5E9; color: #2E7D32; border-radius: 20px; font-weight: 500; }}
            table {{ width: 100%; border-collapse: collapse; margin: 20px 0; background: white; border-radius: 8px; overflow: hidden; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }}
            th, td {{ padding: 12px 16px; text-align: left; border-bottom: 1px solid #eee; }}
            th {{ background: #f8f9fa; font-weight: 600; }}
            .price {{ font-size: 28px; font-weight: bold; color: #2E7D32; text-align: right; }}
            .upgrades {{ background: #e3f2fd; padding: 16px; border-radius: 8px; margin: 16px 0; }}
            .footer {{ text-align: center; color: #666; margin-top: 30px; font-size: 14px; }}
            @media (max-width: 600px) {{ body {{ padding: 10px; }} th, td {{ padding: 10px; font-size: 14px; }} }}
        </style>
    </head>
    <body>
        <div class="header">
            <h1>Configuration Info>
            <p>Hello, we have received your configuration request!</p>
        </div>
        <div class="content">
            <h2>Configurationtion Summary>
            <p><strong>No.:</strong> <span class="order-number">{order_data.get("order_number", "N/A")}</span></p>
            <p><strong>Time:</strong> {created_at}</p>
            
            
            <h3>Product Info</h3>
            <table>
                <tr><th>Brand</th><td>{brand_display}</td></tr>
                <tr><th>Model</th><td><strong>{order_data.get("model_name", "N/A")}</strong></td></tr>
                <tr><th>CPU</th><td>{order_data.get("cpu", "-")}</td></tr>
                <tr><th>Memory</th><td>{order_data.get("memory", "-")}</td></tr>
                <tr><th>Storage</th><td>{order_data.get("hard_disk", "-")}</td></tr>
                <tr><th>GPU</th><td>{order_data.get("graphic_card", "-")}</td></tr>
            </table>
            
            {upgrades_html or '<p>No upgrade options</p>'}
            
            <h3>Reference Price</h3>
            <table>
                {f'<tr><th>Upgrade Price</th><td>¥{upgrade_price:,.0f} </td></tr>' if upgrade_price > 0 else ''}
                <tr><th style="font-size: 20px;">Total Price</th><td class="price">¥{int(total_price):,}</td></tr>
            </table>
            
            {f'<h4>Remark</h4><p>{order_data.get("remark")}</p>' if order_data.get("remark") else ''}
            
            <div style="background: #fff3cd; padding: 20px; border-radius: 8px; margin: 20px 0;">
                <p><strong>We will process your configuration request as soon as possible!</strong></p>
            </div>
        </div>
        <div class="footer">
            <p>© Device Center • Duke Kunshan University</p>
        </div>
    </body>
    </html>'''
    return html


def _build_admin_email_html(order_data):
    """
    构建管理员新订单通知邮件 (简洁信息版)
    """
    created_at = order_data.get('created_at', '')
    if hasattr(created_at, 'strftime'):
        created_at = created_at.strftime('%Y-%m-%d %H:%M:%S')
    
    upgrade_price = order_data.get('upgrade_price', 0)
    base_price = order_data.get('base_price', 0)
    total_price = order_data.get('total_price', 0)
    
    html = f'''
    <!DOCTYPE html>
    <html>
    <head><meta charset="UTF-8"></head>
    <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333; max-width: 800px; margin: 0 auto; padding: 20px;">
        <h2 style="color: #d32f2f;">Device Center 收到新订单</h2>
        <p><strong>订单号:</strong> {order_data.get("order_number")}</p>
        <p><strong>用户:</strong> {order_data.get("user_id")} / {order_data.get("user_name")} ({order_data.get("user_email")})</p>
        <p><strong>时间:</strong> {created_at}</p>
        <p><strong>品牌:</strong> {order_data.get("brand", "N/A").upper()}</p>
        <p><strong>型号:</strong> {order_data.get("model_name")}</p>
        <p><strong>配置:</strong> CPU:{order_data.get("cpu", "-")} | Memory:{order_data.get("memory", "-")} | Storage:{order_data.get("hard_disk", "-")}</p>
    <p><strong>升级费用:</strong> ¥{f"{upgrade_price:,.0f}" if upgrade_price else 0} | <strong>Total Price:</strong> ¥{f"{total_price:,.0f}" if total_price else 0}</p>
        {f'<p><strong>Remark:</strong> {order_data.get("remark")}</p>' if order_data.get("remark") else ''}
        <hr style="margin: 30px 0;">
        <p style="color: #666; font-size: 14px;">请登录管理后台查看完整订单详情并处理。</p>
    </body>
    </html>'''
    return html


def _send_user_email(order_data):
    """发送用户友好版邮件"""
    user_email = order_data.get('user_email', '').strip()
    if not user_email:
        return False
    
    subject = f'Configuration Info - {order_data.get("order_number", "N/A")}'
    html_body = _build_user_email_html(order_data)
    
    msg = MIMEMultipart('alternative')
    msg['Subject'] = subject
    msg['From'] = _format_addr(FROM_DISPLAY_NAME, FROM_ADDR)
    msg['To'] = user_email
    
    msg.attach(MIMEText(html_body, 'html', 'utf-8'))
    
    server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
    server.login(FROM_ADDR, FROM_PASSWORD)
    server.sendmail(FROM_ADDR, [user_email], msg.as_string())
    server.quit()
    
    return True


def _send_admin_email(order_data):
    """发送管理员通知版邮件"""
    subject = f'[新订单] {order_data.get("order_number", "N/A")}'
    
    html_body = _build_admin_email_html(order_data)
    
    msg = MIMEMultipart('alternative')
    msg['Subject'] = subject
    msg['From'] = _format_addr(FROM_DISPLAY_NAME, FROM_ADDR)
    msg['To'] = ', '.join(ADMIN_RECIPIENTS)
    
    msg.attach(MIMEText(html_body, 'html', 'utf-8'))
    
    server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
    server.login(FROM_ADDR, FROM_PASSWORD)
    server.sendmail(FROM_ADDR, ADMIN_RECIPIENTS, msg.as_string())
    server.quit()
    
    return True
