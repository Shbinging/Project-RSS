import jieba.posseg as pseg
from timeAnalyze import timesplit;
jieba.load_userdict('dict.txt');
with open("text.txt",  encoding='utf-8') as fp:
    st = fp.read();
    a = timesplit();
    st = a.analyze(st);
    seg_list = pseg.cut(st)
    for w in seg_list:
        print(w.word, w.flag, sep = '/' ,end = ' ');

	