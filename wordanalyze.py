import jieba.posseg as pseg

with open("text.txt") as fp:
	st = fp.read();
	seg_list = pseg.cut(st)#
	for w in seg_list:
		print(w.word, w.flag, sep = '/' ,end = ' ');