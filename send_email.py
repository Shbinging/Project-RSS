import smtplib
from email.mime.text import MIMEText
from email.header import Header

#---------------------------------------------

mail_host="smtp.qq.com"  #设置服务器
mail_user="13638318926@qq.com"    #用户名
mail_pass="isqhryfduoxrbcej"   #口令 
 
#---------------------------------------------


sender = '13638318926@qq.com'
receivers = ['wsy13638318926@outlook.com']
message = MIMEText('Project RSS 邮件测试', 'plain', 'utf-8')
message['From'] = Header("RSS PROJECT", 'utf-8')
message['To'] =  Header("测试", 'utf-8')
subject = 'Python SMTP 邮件测试'
message['Subject'] = Header(subject, 'utf-8')

try:
    smtpObj = smtplib.SMTP() 
    smtpObj.connect(mail_host, 25)    # 25 为 SMTP 端口号
    smtpObj.login(mail_user,mail_pass)
    smtpObj.sendmail(sender, receivers, message.as_string())
    print ("邮件发送成功")
except smtplib.SMTPException:
    print ("Error: 无法发送邮件")