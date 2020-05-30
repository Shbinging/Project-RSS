import jieba.posseg as pseg
import re
from timeAnalyze import timesplit;
with open("text.txt") as fp:
    st = fp.read();
    a = timesplit;
    a.analyze(st);
    seg_list = pseg.cut(st)
    for w in seg_list:
        print(w.word, w.flag, sep = '/' ,end = ' ');
    ret = re.findall("学期+", st);
    print(ret);