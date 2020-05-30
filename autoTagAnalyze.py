from adeq import makeConfig;
from adeq import adeqSql;

import jieba
import re
from timeAnalyze import timesplit;
from audienceAnalyze import audiencesplit;

class tagAnalyze:
    def __init__(self,trainName, fromData=0, fromDataTag=0, Config=0, wordbagName=0, isToNewSet=0):#原始数据表，读取的标签,训练数据库config，分析数据库,是否新建
        if (trainName == "time" or trainName == "audience"):
            return;
        self.fromData  = fromData;
        self.fromDataTag = fromDataTag;
        self.trainName = trainName;
        self.wordBagName = wordbagName;
        self.wordBagData = adeqSql(Config, wordbagName);
        if (isToNewSet):
            self.trainData = adeqSql(Config, "train_"+trainName);
            self.trainData.createTable("train_"+trainName);
            self.analyzeData = adeqSql(Config, "analyze_"+trainName);
            self.analyzeData.createTable("analyze_"+trainName);
            self.prepareContextTable();
            self.prepareAnalyzeTable();
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

    def prepareContextTable(self, tagName = "@", value = ""):#isnew 1全部手工重建 0 改变已经训练标签为未训练 
        isNew = 1;
        if (isNew):
            self.trainData.clearTable();
            self.trainData.createColumn("isAnalyze", "int DEFAULT 0");
            self.trainData.createColumn("title", "VARCHAR(200)");
            self.trainData.createColumn("tag", "VARCHAR(200)");
            self.trainData.createColumn("number", "int");
            #导入文本
            n = self.fromData.getTableSize();
            for i in range(1, n):
                if (tagName != "@"):
                    tag = self.fromData.queryXY("id", i, tagName)[0];
                    if (tag != value):
                        continue;
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
            if (old.refind(title) != "考试"):
                continue;
            print(title);
            a = self.getwordBag();
            for j in range(0, len(a)):
                print(j, a[j], end = '   ');
            print();
            #记录
            id = int(input());
            if (id == -1):
                continue;
            self.trainData.edit("id", i ,"tag", a[id]);
            self.trainData.edit("id", i, "isAnalyze", 0);
        #self.trainData.printTable();

    def prepareAnalyzeTable(self, isNew = 1):#1新建
        self.analyzeData.clearTable();
        self.analyzeData.createColumn("word", "VARCHAR(200)");
        a = self.getwordBag();
        print(a);
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
            timer = timesplit();
            title = timer.analyze(title);
            ##语法、无效词过滤
            title = self.filterWord(title);
            ##词频统计
            seg_list = jieba.lcut_for_search(title);

            tmp = self.trainData.queryXY("id", i, "tag")[0];
            if (tmp == None): continue;
            #if (tmp == "其他"):
             #   continue;
            for word in seg_list:

                if (self.analyzeData.hasKey("word", word)):#如果该词语存在就加1

                    s = self.analyzeData.queryXY("word", word, tmp)[0];
                    s += 1;
                    self.analyzeData.edit("word", word, tmp, s);
                else:#否则增加该词语
                    self.analyzeData.insertKey("word", word);
                    self.analyzeData.edit("word", word, tmp, 1);
             

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
        e = self.analyzeData.queryXY("word", word, pattern)[0];
        if (self.sum(d) < 2): 
            return 0;
        if (self.sum(d) != 0):
            ans = e/ self.sum(d);
        d = self.analyzeData.queryL(pattern);
        if (self.sum1(d) != 0):
            ans = ans * e /self.sum1(d);
        return ans*100;

    def refind(self, title):
        a = self.getwordBag();
        timer = timesplit();
        title = timer.analyze(title);
        title = self.filterWord(title);
        seg_list = jieba.lcut_for_search(title);
        mx = -1;
        ans = '';
        for pattern in a:
            s = 0;
            for word in seg_list:
                s += self.f(word, pattern);
                #if (pattern == "交流"):
                #print(pattern , word, self.f(word, pattern));
            #print(pattern, s, sep = ' ');
            if (s > mx):
                mx = s;
                ans = pattern;
        list = [];
        list.append(ans);
        list.append(1);
        return list;

    def rfindTime(self, rst, backTime):#2012-12-11
        timeana = timesplit();
        timer = timeana.getTime(rst);
        if (timer[1] != -1):
            st = '';
            year = 0;

            if (timer[1] == 1):

                st = "秋季学期";
                year = timer[2][0];
            if (timer[1] == 2):
                st = "春季学期";
                year = timer[2][0] - 1;
            return str(year)+"-"+str(year+1)+"学年"+st;
        st = '';
        if ("暑假" in rst):
            st = "暑假";
        if ("寒假" in rst):
            st = "寒假";
        a = list(map(int, backTime.split('-')));
        if (7 <=a[1] and a[1] <=8 and st ==''):
            st = "暑假";
        if (9 <= a[1] and a[1] <=12 or a[1] == 1):
            st = "秋季学期";
        if (2 <= a[1] and a[1] <= 6):
            st = "春季学期";
        year = 0;
        if (timer[2][0] != -1):
            year = timer[2][0];
        else:
            year = a[0];
        if (st == '暑假' or st == '寒假'):
            return str(year) + st;
        if (st == "秋季学期"):
            return str(year) + "-" + str(year+1) + "学年"  +st;
        if (st == "春季学期"):
            return str(year-1) + "-" + str(year) + "学年" + st;
    def rfindAudience(self, rst, backTime):
        a = audiencesplit();
        return a.find(rst, backTime);

if (__name__ == "__main__"):
    config = makeConfig("notification");
    fromData = adeqSql(config, "test2");
    config1 = makeConfig("tag");
    
    backTime = fromData.queryXY("id", 10, "time")[0].split('：')[1];
    st = fromData.queryXY("id", 10, "title")[0];
    a = tagAnalyze("audience");
    print(st);
    print(backTime);
    print(a.rfindTime("江苏省计算机等级考试二级Python语言模拟试点考试报名通知 ", "2016-11-10"));
    """
    name = "考试_object";
    a = tagAnalyze(name,fromData, "title", config1, "wordbag", 0);
    a.analyzeData.printTable();
    """
    """
    name = "课程_activity";
    a = tagAnalyze(name,fromData, "title", config1, "wordbag", 0);
    old = tagAnalyze("column",fromData, "title", config1,  "wordbag", 0);
    a.analyzeTrain();
    a.analyzeData.printTable();

    """
    """
    !!!!!!

    !!!!!!!
    warning:
    tagAnalyze 参数顺序改变了

    new = 0;
    name = "考试_object";


    if (new):
        dataBag = adeqSql(config1, "wordbag");
        dataBag.insertKey("tag", name);
        dataBag.edit("tag", name,"word", "网络考试,英语口语考试,计算机等级考试,四六级及学位英语考试,期中考试,期末考试,其他考试,起始考试,补考,缓考");
        dataBag.edit("tag", name, "filter", "的,通知,公告,公示,关于,【,】, ,(,),0,1,2,3,4,5,6,7,8,9,（,）,《,》,[,],南京大学,本科生,学校");
        dataBag.printTable();
    a = tagAnalyze(fromData, "title", config1, name, "wordbag", new);
    old = tagAnalyze(fromData, "title", config1, "column", "wordbag", 0);
    print(" ----");
    ana = 0;
    if (ana):
        a.analyzeByHand(1,200);
        a.analyzeTrain();
    if (not ana and not new):
        dataBag = adeqSql(config1, "wordbag");
        dataBag.printTable();
        print(a.refind("2020年春季学期超星尔雅在线课程考试提醒"));
    """
   