#-----------------------------
#projectRss 主程序
#powered by Shbing wsy
#V1.0
#-----------------------------
from autoTagAPI import autoTag;
from adeq import adeqSql;
from adeq import makeConfig;
from mailClass import mail;

RSS = adeqSql(makeConfig("RSS"), "test2");
b = ["column", "object", "activity", "audience"];
WordBag = adeqSql(makeConfig("tag"),"wordbag");
User = adeqSql(makeConfig("user"),"user");

column = ["1", "课程","考试","毕业","交流","竞赛","专业分流","其他"];
administrator = ["1436775971@qq.com"];

def printList(a):
	for item in a:
		print(item, end = '\t');
	print();

def getNewInfo():## title time url
	ans = [];
	for i in range(1, 5):
		item = [];
		item.append(RSS.queryXY("id", i, "title")[0]);
		item.append(RSS.queryXY("id", i, "time")[0]);
		item.append(RSS.queryXY("id", i, "url")[0]);
		ans.append(item);
	return ans;

while(1):
	ff = 1;
	if (ff):
		
	print("######################################################################");
	#updateSpider();
	titleList = getNewInfo();
	confirmList= [];#手工确认
	###########################################
	#取出要发送的消息
	flag = 0;
	for title in titleList:
		aTag = autoTag();
		tmp = aTag.analyze(title[0], title[1]);
		confirmList.append(aTag.analyze(title[0], title[1]));
		if (tmp[1] == 1):
			flag = 1;
	#if (flag):
	#	sendMail = mail(["有新消息","标签确认",""], administrator);
	#	sendMail.confirmToSend();
	###########################################
	#标签确认
	print("-----------------------------------------------------------------------------");
	print("标签确认");
	print("-----------------------------------------------------------------------------");
	print("-----------------------------------------------------------------------------");
	tags = WordBag.queryL("word");
	print("标签：");
	for tag in tags:
		print(tag);
	print("-----------------------------------------------------------------------------");
	print("确认输入Yes，否则输入正确的标签,空格隔开");
	print("-----------------------------------------------------------------------------");
	for i in range(0, len(confirmList)):
		if (confirmList[i][1] == 0):
			continue;
		print("-----------------------------------------------------------------------------");
		print(titleList[i][0]);
		printList(b);
		for j in b:
			print(confirmList[i][0][j], end = '\t');
		print();
		opt = input("输入:");
		if (opt == "Yes"):
			continue;
		while(1):
			a = opt.split();
			k = -1;
			try:
				for item in a:
					k += 1;
					confirmList[i][0][b[k]] = item;
			except:
				print("输入错误！");

			for j in b:
				print(confirmList[i][0][j], end = '\t');
			print();
			opt = input("是否确认:");
			if (opt == "Yes"):
				break;
			opt = input("输入");
	print("确认完毕");
	############################################
	#发送邮件
