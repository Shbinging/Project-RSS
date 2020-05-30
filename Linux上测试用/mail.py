# -*- coding: UTF-8 -*-
import os
import re
import smtplib
from email.header import Header
from email.mime.text import MIMEText

def send_email():
    """Centos7系统使用Python发邮件"""
    mail_host = "smtp.qq.com"  # 设置服务器
    mail_user = "13638318926@qq.com"  # 用户名
    mail_pass = "isqhryfduoxrbcej"  # 使用自己的口令
    sender = '13638318926@qq.com'
    receivers = ['1322675190@qq.com']  # 接收邮件(可设置多个)
    message = MIMEText('预警：toutiao_spider文件未完全运行！', 'plain', 'utf-8')
    message['From'] = Header("120.79.220.109", 'utf-8')
    message['To'] = Header("测试", 'utf-8')
    subject = 'toutiao_spider预警'
    message['Subject'] = Header(subject, 'utf-8')
    try:
        smtpObj = smtplib.SMTP_SSL(host = mail_host)
        smtpObj.connect(mail_host, 465)
        smtpObj.login(mail_user, mail_pass)
        smtpObj.sendmail(sender, receivers, message.as_string())
        print('发送成功')
    except smtplib.SMTPException:
        print("ERROR")


send_email()