from adeq import makeConfig;
from adeq import adeqSql;

import jieba
import re
from timeAnalyze import timesplit;


class tagAnalyze:
    def __init__(self, fromData, fromDataTag, Config, trainName, wordbagName, isToNewSet):#原始数据表，读取的标签,训练数据库config，分析数据库,是否新建
        self.fromData  = fromData;
        self.fromDataTag = fromDataTag;
        self.trainName = trainName;
        self.wordBagName = wordbagName;
        self.wordBagData = adeqSql(Config, wordbagName);
        if (isToNewSet):
            self.trainData = adeqSql(Config, "train_"+trainName);
            self.trainData.createTable("train_"+trainName);
            self.analyzeData = adeqSql(Config, "analyze_"+trainName);
            self.trainData.createTable("analyze_"+trainName);
        else:
            self.trainData = adeqSql(Config, "train_"+trainName);
            self.analyzeData = adeqSql(Config, "analyze_"+trainName);

    def clearContextTable(self):
        self.trainData.clearTable();

    def clearAnalyzeTable(self):
        self.analyzeData.clearTable();

    def setContextTableNotAnalyze(self):
        n = self.trainData.getTableSize();
        for i in range(1, n):
            self.trainData.edit("id", i, "isAnalyze", 0);

    def prepareContextTable(self, isNew = 1):#isnew 1全部手工重建 0 改变已经训练标签为未训练 
        if (isNew):
            self.trainData.clearTable();
            self.trainData.createColumn("isAnalyze", "int DEFAULT 0");
            self.trainData.createColumn("title", "VARCHAR(200)");
            self.trainData.createColumn("tag", "VARCHAR(200)");
            self.trainData.createColumn("number", "int");
            #导入文本
            n = self.fromData.getTableSize();
            print(self.trainData.getTabletitle());
            for i in range(1, n):
                title = self.fromData.queryXY("id", i, self.fromDataTag)[0];
                self.trainData.insertKey("title", title);
                self.trainData.edit("id", i, "isAnalyze", 0);

    def getwordBag(self):
        a = self.wordBagData.queryXY("tag", self.trainName, "word")[0].split(',');
        return a;

    def getwordFilter(self):
        a = self.wordBagData.queryXY("tag", self.trainName, "filter")[0].split(',');
        return a;

    def analyzeByHand(self, l, r, isOverload = 0):#1 覆盖原来标签 0 不覆盖 从1开始
        for i in range(l, r):
            title = self.trainData.queryXY("id", i, "title")[0];
            status = self.trainData.queryXY("id", i, "tag")[0];
            if (status != None and isOverload == 0):#判断改标题是否处理过
               continue;
           #打印
            print(title);
            a = self.getwordBag();
            for j in range(0, len(a)):
                print(j, a[j], end = '   ');
            print();
            #记录
            id = int(input());
            self.trainData.edit("id", i ,"tag", a[id]);
            self.trainData.edit("id", i, "isAnalyze", 0);
        self.trainData.printTable();

    def prepareAnalyzeTable(self, isNew = 1):#1新建
        self.analyzeData.clearTable();
        self.analyzeData.createColumn("word", "VARCHAR(200)");
        a = self.getwordBag();
        for tagWord in a:
            self.analyzeData.createColumn(tagWord, "int default 0");
    
    def filterWord(self, title):
        a = self.getwordFilter();
        for word in a:
            tmpSt = '';
            while (tmpSt != title):
                tmpSt = title;
                title = title.replace(word, "");
        return title;

    def analyzeTrain(self):
        n = self.trainData.getTableSize();
        for i in range(1, n):
            title = self.trainData.queryXY("id", i, "title")[0];
            ##时间词过滤
            print(title);
            timer = timesplit();
            title = timer.analyze(title);
            ##语法、无效词过滤
            title = self.filterWord(title);
            ##词频统计
            print(title);
            seg_list = jieba.lcut(title);
            tmp = self.trainData.queryXY("id", i, "tag")[0];
            if (tmp == None): continue;
            if (tmp == "其他"):
                continue;
            for word in seg_list:
                if (self.analyzeData.hasKey("word", word)):#如果该词语存在就加1
                    s = self.analyzeData.queryXY("id", i, tmp);
                    s += 1;
                    self.analyzeData.edit("id", i, tmp, s);
                else:#否则增加该词语
                    self.analyzeData.insertKey("word", word);
                    self.analyzeData.edit("word", word, tmp, 1);
             
        print(self.analyzeData.printTable());

    def sum(self, b):
        s = 0;
        for i in b:
            s += i;
        return s;

    def sum1(self, b):
        s = 0;
        for i in b:
            s += i[0];
        return s;

    def f(self, word, pattern):
        a = self.getwordBag();
        d = self.analyzeData.queryH("word", word);
        if (not self.analyzeData.hasKey("word", word)):
            return 0;
        d = d[0][2:];
        ans = 0;
        e = 0;
        for i in range(0, len(a)): 
            if (a[i] == pattern):
                e = d[i];
                if (self.sum(d) != 0):
                    ans = d[i] / self.sum(d);
        d = self.analyzeData.queryL(pattern);
        if (self.sum1(d) != 0):
            ans = ans * e /self.sum1(d);
        return ans*100;

    def refind(self, title):
        a = self.getwordBag();
        timer = timesplit();
        title = timer.analyze(title);
        title = self.filterWord(title);
        seg_list = jieba.lcut(title);
        mx = -1;
        ans = '';
        for pattern in a:
            s = 0;
            for word in seg_list:
                s += self.f(word, pattern);
            print(pattern, s, sep = ' ');
            if (s > mx):
                mx = s;
                ans = pattern;
        return ans;

if (__name__ == "__main__"):
    config = makeConfig("test");
    fromData = adeqSql(config, "test");
    config1 = makeConfig("tag");
    fromData = adeqSql(config1, "wordbag");
    #fromData.createColumn("filter", "VARCHAR(200)");
    fromData.edit("tag", "column", "filter", "的,通知,公告,关于, ");
    a = tagAnalyze(fromData, "title", config1, "column", "wordbag", 0);
    print(a.refind("【学生】关于本学期本科生课程增加一次退课安排的通知"));
    #a.clearAnalyzeTable();
    #a.analyzeTrain();
    #a.analyzeTrain();
    #a.prepareAnalyzeTable();
    #a.prepareContext(0);
    #fromData.printTable();
    #fromData.createTable("wordbag");
    #fromData.createColumn("tag", "VARCHAR(200)");
    #fromData.createColumn("word", "VARCHAR(800)");
    #fromData.insertKey("tag", "column");
    #fromData.edit("tag", "column", "word", "课程,考试,毕业,交流,竞赛,其他");
    #fromData.printTable();
    
    