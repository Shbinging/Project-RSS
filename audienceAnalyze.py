import re;
from timeAnalyze import timesplit;
class audiencesplit:
	def find(self, st, backTime):
		a = list(map(int, backTime.split('-')));
		sem = 0;
		if (8<= a[1] and a[1] <=12):
			sem = 1;
		if (1 <= a[1] and a[1] <= 7):
			sem = 2;
		if (sem == 2):
			freshman = a[0] - 1;
		else:
			freshman = a[0];
		ret = re.findall(r'\d+级', st);
		for i in range(0, len(ret)):
			if (len(ret[i]) == 3):
				ret[i] = "20" + ret[i];
		if (len(re.findall(r'毕业|大四|推免', st))):
			ret.append(str(freshman -3)+"级");
		if (len(re.findall(r'大一|新生|入学', st))):
			ret.append(str(freshman) + "级");
		if (len(re.findall(r'大二', st))):
			ret.append(str(freshman - 1) + "级");
		if (len(re.findall(r'大三', st))):
			ret.append(str(freshman - 2) + "级");
		ret = list(set(ret));
		if (len(ret) == 0):
			for i in range(0, 4):
				ret.append(str(freshman - i) + "级");
		ret = sorted(ret);
		return ','.join(ret);

if (__name__ == "__main__"):
	a = audiencesplit();
	print(a.find("【教师|学生】2019-2020学年第二学期停调课信息（实时更新）","2020-01-10"));