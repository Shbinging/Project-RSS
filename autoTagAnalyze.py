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
            self.sumData = adeqSql(Config, "sum_"+ trainName);
            self.sumData.createTable("sum_"+trainName);
            self.prepareContextTable();
            self.prepareAnalyzeTable();
            self.prepareSumTable();
        else:
            self.trainData = adeqSql(Config, "train_"+trainName);
            self.analyzeData = adeqSql(Config, "analyze_"+trainName);
            self.sumData = adeqSql(Config, "sum_"+ trainName);

    def clearContextTable(self):
        self.trainData.clearTable();

    def clearAnalyzeTable(self):
        self.analyzeData.clearTable();

    def clearSumTable(self):
        self.sumData.clearTable();

    def setContextTableNotAnalyze(self):
        n = self.trainData.getTableSize();
        for i in range(1, n):
            self.trainData.edit("id", i, "isAnalyze", 0);

    def prepareContextTable(self, tagName = "@", value = ""):#isnew 1全部手工重建 0 改变已经训练标签为未训练 
        isNew = 0;
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

    def prepareSumTable(self):
        a = self.getwordBag();
        print(a);
        self.sumData.insertKey(a[0], 0);
        for tagWord in a:
            self.sumData.createColumn(tagWord, "int default 0");
            self.sumData.edit(id, 1, tagWord, 0);

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
        ss = 0;
        for i in range(1, n):
            
            title = self.trainData.queryXY("id", i, "title")[0];
            ##时间词过滤
            timer = timesplit();
            title = timer.analyze(title);
            ##语法、无效词过滤
            title = self.filterWord(title);
            ##词频统计
            seg_list = jieba.lcut(title);

            tmp = self.trainData.queryXY("id", i, "tag")[0];
            if (tmp == None): continue;
            
            #if (tmp == "其他"):
             #   continue;
            if (tmp == "课程"):
                ss += 1;
            s1 = self.sumData.queryXY("id", 1, tmp)[0];
            s1 += 1;
            self.sumData.edit("id",1, tmp, s1);
            seg_list = list(set(seg_list));
            for word in seg_list:

                if (self.analyzeData.hasKey("word", word)):#如果该词语存在就加1

                    s = self.analyzeData.queryXY("word", word, tmp)[0];
                    s += 1;
                    self.analyzeData.edit("word", word, tmp, s);
                else:#否则增加该词语
                    self.analyzeData.insertKey("word", word);
                    self.analyzeData.edit("word", word, tmp, 1);
        print(ss);  
           
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

    def fBayes(self, segList,pattern):#朴素贝叶斯+拉普拉斯修正进行标签权重计算
        a = self.getwordBag();
       # d = self.analyzeData.queryH("word", word);
        b = self.sumData.queryH("id", 1);
        tagSum = len(b[0][1:]);#标签的种类数
        s1 = self.sum(b[0][1:]);##计算所有标签出现的次数;
        s2 = 0;##计算所有单词出现总次数
        s5 = self.sumData.queryXY("id", 1, pattern)[0];
        for word in segList:
            if (not self.analyzeData.hasKey("word", word)):
                continue;
            s2 += self.sum(self.analyzeData.queryH("word", word)[0][2:]);
        #for word in segList:
        pPattern = (self.sumData.queryXY("id", 1, pattern)[0]+1) / (s1+2);#统计改标签的概率
        ss = pPattern;#贝叶斯概率
        tmp = self.analyzeData.queryL(pattern);
        s3 = self.sum1(tmp);#某标签下所有单词出现的次数
        wordSum = len(tmp);
        for word in segList:
            if (not self.analyzeData.hasKey("word", word)):
                continue;
                ss = ss*1/(s5+2);
                ss = ss/(1/(wordSum));
                #ss = ss/(1/(s1+2));
            else:
                tmp1 = self.analyzeData.queryXY("word", word, pattern)[0];
                s4 = self.sum(self.analyzeData.queryH("word", word)[0][2:]);##某个单词出现总次数;
                #if (tmp1 == 0 or s4 == 0):continue;
                ss = ss*(tmp1+1)/(s5+2);
                #ss = ss/((s4+1)/(s1 + 2));
                ss = ss/((s4+1)/(s3 + wordSum));
                #print(word, tmp1, s3, (tmp1+1)/(s3+2));
                #print(word, 1/((tmp1+1)/(s4 + tagSum)));
        return ss;


    
    def refind1(self, title):
        a = self.getwordBag();
        timer = timesplit();
        title = timer.analyze(title);
        title = self.filterWord(title);
        seg_list = jieba.lcut(title);
        mx = -1;
        ans = '';
        for pattern in a:
            #s = 1;
            #for word in seg_list:
             #   s *= self.f(word, pattern);
                #if (pattern == "交流"):
                #print(pattern , word, self.f(word, pattern));
            s = self.fBayes(seg_list, pattern);
            if (s > mx):
                mx = s;
                ans = pattern;
        list = [];
        list.append(ans);
        list.append(1);
        return list;

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
        ans1 = self.refind1(title)[0];
        if (ans1 == ans):
            list.append(0);
        else:
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
    name = "column";
    a = tagAnalyze(name, fromData, "title", config1, "wordbag", 0);
    st = "关于“悦读经典计划”悦读学分认定的说明（2019-2020学年第一学期）";
    print(a.refind(st));
    print(a.refind1(st));
    #print(a.analyzeData.queryXY("id", 1, "网络考试"));
######################################################
#增加对标签的分类统计
"""
    name = "课程_activity";
    a = tagAnalyze(name, fromData, "title", config1, "wordbag", 0);
    a.clearSumTable();
    a.clearAnalyzeTable();
    a.prepareSumTable();
    a.analyzeTrain();
    a.sumData.printTable();
    a.analyzeData.printTable();
   """
######################################################
    