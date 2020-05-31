#-----------------------------
#projectRss 主程序
#powered by Shbing wsy
#V1.0
#-----------------------------
from autoTagAPI import autoTag;
from adeq import adeqSql;
from adeq import makeConfig;
from mailClass import mail;
from netSpider import netSpider;
RSS = adeqSql(makeConfig("RSS"), "test2");
b = ["column", "object", "activity", "audience"];
WordBag = adeqSql(makeConfig("tag"),"wordbag");
User = adeqSql(makeConfig("user"),"user");

column ={"课程":"1","考试":"2","毕业":"3","交流":"4","竞赛":"5","专业分流":"6","其他":"7"};

grade = {"1":"2016级","2":"2017级","3":"2018级","4":"2019级"};

administrator = ["1436775971@qq.com"];

def printList(a):
	for item in a:
		print(item, end = '\t');
	print();

def getNewInfo():## title time url
	ans = [];
	n = RSS.getTableSize();
	for i in range(1, n+1):
		if (RSS.queryXY("id", i, "status")[0] == 1):
			continue;
		item = [];
		item.append(RSS.queryXY("id", i, "title")[0]);
		item.append(RSS.queryXY("id", i, "time")[0]);
		item.append(RSS.queryXY("id", i, "url")[0]);
		ans.append(item);
	return ans;

def getList(a):
	ans = [];
	for item in a:
		ans.append(item[0]);
	return ans;

def getStrTag(a):
	list = [];
	c = ["time","column","object","activity"];
	for ch in c:
		if (a[ch] != None):
			list.append(a[ch]);
	return ",".join(list);

while(1):
	##########################################
	#debug
	ff = 1;
	if (ff):
		User.edit("username", "1436775971@qq.com", "topics", "13");
		#User.edit("username", "1436775971@qq.com", "grade", "4");
	##########################################
	print("######################################################################");
	#netSpider();
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
	if (flag):
		sendMail = mail(["有新消息","标签确认",""], administrator);
		sendMail.confirmToSend();
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
	userList = getList(User.queryL("username"));
	option = getList(User.queryL("topics"));
	gradeList = getList(User.queryL("grade"));
	n = len(userList);
	for i in range(0, len(confirmList)):
		confirm = confirmList[i];
		sendList = [];
		for j in range(0, n):
			if (column[confirm[0]["column"]] in option[j]):
				isIN = 0;
				for ch in gradeList[j]:
					if (grade[ch] in confirm[0]["audience"]):
						isIN = 1;
				if (isIN or confirm[0]["column"] != "课程"):
					sendList.append(userList[j]);
		strTag = getStrTag(confirm[0]);
		print(sendList);
		if (len(sendList) > 0):
			sendMail = mail([titleList[i][0], strTag, titleList[i][2]],sendList);
			sendMail.confirmToSend();
		RSS.edit("url",titleList[i][2],"status", 1);
	break;