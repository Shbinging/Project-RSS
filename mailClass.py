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
    mail = ''
    for i in data:
        mail = mail + i +"\n"
    mail = mail+'''
    #-------------------------------------------------
    感谢参加教务处RSS订阅测试计划
    项目创建者：水兵、王颂言\n
    '''
    mail = mail + time_stamp()
    return mail

class mail:
    receivers = ['wsy13638318926@outlook.com']
    message = MIMEText('Project RSS 邮件测试', 'plain', 'utf-8')
    message['From'] = Header("RSS PROJECT", 'utf-8')
    message['To'] =  Header("测试用户", 'utf-8')
    message['Subject'] = Header('RSS订阅测试', 'utf-8')
    smtpObj = smtplib.SMTP() 
    def __init__(self,mail,users):
        self.receivers = users
        self.message = MIMEText(mail,'plain','utf-8')
        self.message['From'] = Header("RSS Project",'utf-8')
        self.message['To'] = Header("RSS用户",'utf-8')
        subject = time_stamp() + "南京大学教务处 RSS 订阅"
        self.message['Subject'] = Header(subject,'utf-8')
        try:
            self.smtpObj = smtplib.SMTP() 
            self.smtpObj.connect(mail_host, 25)    # 25 为 SMTP 端口号
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
    users = ['wsy13638318926@outlook.com','1436775971@qq.com','1322675190@qq.com']
    data = ['titel','time','content','url','lable']
    mail1 = mailmaker(data)
    send1 = mail(mail1,users)
    send1.confirmToSend()
