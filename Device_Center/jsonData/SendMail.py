import smtplib
from email.mime.multipart import MIMEMultipart 
from email import encoders
from email.header import Header
from email.mime.text import MIMEText
from email.utils import parseaddr, formataddr
from email.mime.application import MIMEApplication
import os
import argparse

TDTXT = '''
<tr><th bgcolor='CCCCCC' >Server Location</th>
            <th bgcolor='CCCCCC' >Server IP Address</th>
            <th bgcolor='CCCCCC' >Server Name</th>
            <th bgcolor='CCCCCC' >Server Label</th>
            <th bgcolor='FF4500' >Server Status</th>
</tr>
'''


def send_email(receivers,servermsg):
    #发件人eMail
    asender="ip_pingfail_alert@163.com"
    #收件人eMail
    areceiver=receivers
    #抄送人eMail
    acc = 'tz138@duke.edu'
    #邮件主题
    asubject = 'Server Offline Warning'  

    #发件人地址
    from_addr = "ip_pingfail_alert@163.com"
    #eMail密码（授权码）
    password="EHJNGRYACAODBKMS"
    #邮件设置
    msg = MIMEMultipart()
    msg['Subject'] = asubject  
    msg['to'] = areceiver  
    msg['Cc'] = acc 
    msg['from'] =  "IT Server Monitor"

    #邮件正文   

    

    body = '''
<html>
<head>
<meta http-equiv='Content-Type' content='text/html;charset=UTF-8'>
<style type='text/css'>
    body{text-align:left;margin:0px auto;padding:20px;font:13px 'Lucida Grande', 'Lucida Sans Unicode', Helvetica, Arial, sans-serif;}
    p,table,tr,th{margin:0;padding:0;font-weight:normal;}
    table{border-collapse:collapse;margin-bottom:15px;}
    table, table th {padding:5px; border:1px solid #000;border-width:0px 0px 0px 0px;}
</style>
</head>
<body>
    <p>Dear Team:</p>
    <br/>
    <p>&nbsp;&nbsp;&nbsp;&nbsp;Alert!</p>
    <br/>
    <p>&nbsp;&nbsp;&nbsp;&nbsp;Below servers are OFFLINE. Please check~</p>

<br/>
<br/>
    <table border='1'>
        <tr>
            <th colspan='6' align='center' bgcolor='CCCCCC'>Server Offline List</th>
        </tr>
        <tr><th bgcolor='CCCCCC' >Server Location</th>
            <th bgcolor='CCCCCC' >Server IP Address</th>
            <th bgcolor='CCCCCC' >Server Name</th>
            <th bgcolor='CCCCCC' >Server Label</th>
            <th bgcolor='CCCCCC' >Server Status</th>
        </tr>
        SERVER_LIST_TEXT
    </table>
</body>
</html>
    '''

    #添加邮件正文:
    ServerBody = getMailBody(servermsg)

    # print(body.replace('SERVER_LIST_TEXT',ServerBody))
    msg.attach(MIMEText(body.replace('SERVER_LIST_TEXT',ServerBody), 'html', 'utf-8'))

    #生成excel
    FilePath = os.environ['HOME'] + '/ServerList.html'

    with open(FilePath,'w+') as file_write:
        file_write.write(body.replace('SERVER_LIST_TEXT',ServerBody))
        file_write.close()

    # 添加附件
    # 注意这里的文件路径是斜杠
    xlsxpart = MIMEApplication(open(FilePath, 'rb').read())
    xlsxpart.add_header('Content-Disposition', 'attachment', filename='ServerList.html')
    msg.attach(xlsxpart)    

    # 设置eMail服务器地址以及端口
    smtp_server ="smtp.163.com"
    server = smtplib.SMTP(smtp_server, 25)
    server.set_debuglevel(1)

    #登陆eMail
    server.login(from_addr, password)

    #发送邮件
    server.sendmail(from_addr, areceiver.split(',')+acc.split(','), msg.as_string())

    #断开服务器链接
    server.quit()   

def getMailBody(Servermsg):
    mailBody = ''
    # server_list_txt = 'AB3106,10.200.4.177,DKU-DDS-001,2010102-202012-00001,OFFLINE;AB3107,10.200.4.155,DKU-DDS-002,2010102-202012-00002,OFFLINE'
    serverArr = Servermsg.split(';')
    for index in range(0,len(serverArr)):
        oneServer = serverArr[index].split(',')
        mailBody = mailBody + TDTXT.replace('Server Location',oneServer[0]).replace('Server IP Address',oneServer[3]).replace('Server Name',oneServer[1]).replace('Server Label',oneServer[2]).replace('Server Status',oneServer[5])

    return mailBody



if __name__ =='__main__':
    parser = argparse.ArgumentParser(description='for Email')
    parser.add_argument('-re', '--receivers', help='receivers for e-mail', type=str, default=False, required=True)
    parser.add_argument('-msg', '--servermsg', help='server message', type=str, default=False, required=True)
    args = parser.parse_args()
    receivers = args.receivers
    servermsg = args.servermsg
    # receivers = 'tz138@duke.edu'
    # servermsg = "IB2001,DKU-DDS-003,2010102-202012-00003,10.200.21.134,1,OFFLINE"
    send_email(receivers,servermsg)
