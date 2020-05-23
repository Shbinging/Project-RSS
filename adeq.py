import mysql.connector;
from MySQL_Class_Use import sql;




def makeConfig(databaseName):
	config = {
        'host': 'localhost',
        'port': 3306,
        'database': 'adeqtest',
        'user': 'root',
        'password': 'abc@123',
        'charset': 'utf8',
        'use_unicode': True,
        'get_warnings': True,
    }
	config['database'] = databaseName;
	return config;

class adeqSql(sql):
	def __init__(self, config, tableName):
		sql.__init__(self, config);
		self.tableName = tableName;

	def zy(self, ch):
		if (type(ch) == type(1)):
			return str(ch);
		if (type(ch) == type("ab")):
			st = "'" + ch + "'";
			return st;

	def createColumn(self, name, typeName):#-1 fail 0 not need to add 1 add
		try:
			result = self.getTabletitle();
			for colName in result:
				if (name in colName):
					print("列已经存在");
					return 0;
			opt = "alter table %s add column %s %s"%(self.tableName, name, typeName);
			self.update(opt);
		except:
			print("发生错误createColumn");
			return -1;

	def createTable(self, name):
		try:
			opt = "create table %s (id INT not null auto_increment, primary key (id))"%(name);
			self.tableName = name;
			self.update(opt);
		except:
			print("发生错误createTable");
			return -1;
	def createTable(self, name):
		try:
			opt = "create table %s (id INT not null auto_increment, primary key (id))"%(name);
			self.tableName = name;
			self.update(opt);
		except:
			print("发生错误createTable");
			return -1;

	def clearTable(self):
		try:
			opt = "truncate "+self.tableName;
			self.update(opt);
		except:
			print("发生错误createTable");
			return -1;

	def hasKey(self, tagName, name):#某一列是否有某个值
		try:
			opt = "select %s from %s where %s ="%(tagName, self.tableName, tagName) + self.zy(name);
			return self.isExsist(opt);
		except:
			print("发生错误hasKey");
			return -1;

	def insertKey(self, tagName, name):
		try:
			opt = "insert into %s (%s)"%(self.tableName, tagName)+ " values("+ self.zy(name) + ")";
			self.update(opt);
		except:
			print("发生错误insertKey");
			return -1;

	def getTableStr(self):#获取整张表格
		opt = "select * from %s"%self.tableName;
		a = self.select_lines(opt);
		return a;

	def getTableSize(self):#获取表格行数
		result = self.getTableStr();
		return len(result);

	def getTabletitle(self):#获取所有标签名称
		opt = "SELECT column_name FROM information_schema.columns WHERE table_name =  " + self.zy(self.tableName) + " and TABLE_SCHEMA=" + self.zy(self.config["database"]);
		c = self.select_lines(opt);
		return c;

	def printTable(self):
		#a = self.getTabletitle();
		b = self.getTableStr();
		#for tag in a:
		#	print(tag[0], '\t', end = '');
		#print();
		for line in b:
			for word in line:
				print(word, '\t', end = '');
			print();

	def queryL(self, tagName):
		try:
			opt = "select %s from %s"%(tagName, self.tableName);
			tmp = self.select_lines(opt);
			return tmp;
		except:
			print("发生错误queryL");
			return -1;

	def queryH(self, tagName, name):
		try:
			opt = "select * from %s where %s ="%(self.tableName, tagName) + self.zy(name);
			tmp = self.select_lines(opt);
			return tmp;
		except:
			print("发生错误queryH");
			return -1;

	def queryXY(self, tagName1, name, tagName2):#先行后列, select tagName2 from table where tagName1 = name 
		try:
			opt = "select %s from %s where %s ="%(tagName2, self.tableName, tagName1) + self.zy(name);
			tmp = self.select_lines(opt);
			if (len(tmp) == 0):
				tmp = [];
			else:
				tmp = tmp[0];
			return tmp;
		except:
			print("发生错误queryXY");
			return -1;

	def edit(self, tagName1, name, tagName2, newKey):#修改某行某列的值
		try:
			opt = "UPDATE %s"%self.tableName+" SET %s = "%tagName2 + self.zy(newKey)+" WHERE %s = "%tagName1 + self.zy(name);
			self.update(opt);
		except:
			print("发生错误edit");
			return -1;

if (__name__ == "__main__"):
	c = makeConfig("123");
	print(c);