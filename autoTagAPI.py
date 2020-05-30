from autoTagAnalyze import tagAnalyze;
from adeq import makeConfig;
from adeq import adeqSql;
class autoTag:
	def __init__(self):
		self.ans = {"time":None,"column":None,"object":None,"activity":None,"audience":None}

	def analyze(self, st, backTime):
		backTime = backTime.split("：")[1];
		a = tagAnalyze("time");
		self.ans["time"] = a.rfindTime(st, backTime);
		a = tagAnalyze("audience");
		self.ans["audience"] = a.rfindAudience(st, backTime);
		config = makeConfig("tag");
		a = tagAnalyze("column", 0, 0, config,"wordbag",0);
		self.ans["column"] = a.refind(st);
		
		if (self.ans["column"] == "课程"):
			a = tagAnalyze("课程_object",0,0,config,"wordbag",0);
			self.ans["object"] = a.refind(st);
			a = tagAnalyze("课程_activity",0,0,config,"wordbag",0);
			self.ans["activity"] = a.refind(st);
		if (self.ans["column"] == "考试"):
			a = tagAnalyze("考试_object",0,0,config,"wordbag",0);
			self.ans["object"] = a.refind(st);
		
		"""
		a = tagAnalyze("课程_object",0,0,config,"wordbag",0);
		a.refind(st);
		a = tagAnalyze("考试_object",0,0,config,"wordbag",0);
		a.refind(st);
		"""
		b = ["time", "column", "object", "activity", "audience"];
		for word in b:
			print(word, end = '\t             ');
		print();
		for word in b:
			print(self.ans[word], end = '\t');
		print();

if (__name__ == "__main__"):
	config = makeConfig("notification");
	fromData = adeqSql(config, "test2");
	for i in range(700, 740):
		st = fromData.queryXY("id", i, "title")[0];
		backTime = fromData.queryXY("id", i, "time")[0];
		print(st, end = ' ');
		print(backTime);
		a = autoTag();
		a.analyze(st, backTime);

