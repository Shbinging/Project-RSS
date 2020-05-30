
import smtplib
from email.mime.text import MIMEText
from email.header import Header
import time

#---------------------------------------------
# mailmaker函数能直接将接到的数据库的邮件信息转化为mail函数需要的mail对象
# mail对象在进行初始化的时候就会进行连接判断
# mail对象唯一的函数是confirmToSend()没有任何参数，确认好信息后发送即可
#---------------------------------------------

mail_host="smtp.qq.com"  #设置服务器
mail_user="13638318926@qq.com"    #用户名
mail_pass="isqhryfduoxrbcej"   #口令
sender = '13638318926@qq.com'
 
#---------------------------------------------
def time_stamp():
    now = int(time.time())
    timeArray = time.localtime(now)
    otherStyleTime = time.strftime("%Y-%m-%d",timeArray)
    return otherStyleTime

def mailmaker(data):
    mail = '''------------------------------------------------------
项目仍在测试中，为了保证你不遗漏重要信息，请访问原文URL链接
------------------------------------------------------\n'''
    mail = mail + data[1]+"\n"+data[2]+"\n"
    mail = mail+'''------------------------------------------------------
感谢参加教务处RSS订阅测试计划
项目创建者：水兵、王颂言
------------------------------------------------------\n'''
    mail = mail + time_stamp()
    return mail

class mail:
    receivers = ['wsy13638318926@outlook.com']
    message = MIMEText('Project RSS 邮件测试', 'plain', 'utf-8')
    message['From'] = Header("RSS PROJECT", 'utf-8')
    message['To'] =  Header("测试用户", 'utf-8')
    message['Subject'] = Header('RSS订阅测试', 'utf-8')
    smtpObj = smtplib.SMTP() 
    def __init__(self,data,users):
        mail_content = mailmaker(data)
        self.receivers = users
        self.message = MIMEText(mail_content,'plain','utf-8')
        self.message['From'] = Header("RSS Project",'utf-8')
        self.message['To'] = Header("RSS用户",'utf-8')
        subject =data[0]
        self.message['Subject'] = Header(subject,'utf-8')
        try:
            self.smtpObj = smtplib.SMTP_SSL(host = mail_host) 
            self.smtpObj.connect(mail_host, 465)    # 25 为 SMTP 端口号
            self.smtpObj.login(mail_user,mail_pass)
        except self.smtplib.SMTPException:
            print("登陆失败")
    def confirmToSend(self):
        try:
            self.smtpObj.sendmail(sender, self.receivers, self.message.as_string())
            print("邮件发送成功")
        except self.smtplib.SMTPException:
            print("邮件发送失败")
            


if __name__ == "__main__":
    users = ['13638318926@qq.com']
    data = ['title','tag','url']
    send1 = mail(data,users)
    send1.confirmToSend()