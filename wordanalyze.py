import jieba.posseg as pseg
import re

with open("text.txt") as fp:
	st = fp.read();
	ret = re.findall(r"\d+.年", st);
	ret = re.findall(r".{2}学期", st);
	ret = re.findall()
	print(ret);
	
	