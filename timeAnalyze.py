#dateutil
import re
import time
import jieba
class timesplit:
    def ini(self, st):
        self.st = st;
        self.lyear = -1;
        self.lmonth = -1;
        self.lday = -1;
        self.lh = -1;
        self.lmin = -1;
        self.ryear = -1;
        self.rmonth = -1;
        self.rday = -1;
        self.rh = -1;
        self.rmin = -1;
        self.sem = -1;
        self.isinter = 0;
    def analyze(self, st):
        self.ini(st);
        d = self.extractsem();
        isinter = self.extractLR();
        self.extractYMDHM();
        return self.st;
    
    def getTime(self, st):
        self.ini(st);
        d = self.extractsem();
        isinter = self.extractLR();
        self.extractYMDHM();
        return [self.isinter,self.sem,(self.lyear, self.lmonth, self.lday, self.lh, self.lmin),(self.ryear, self.rmonth, self.rday, self.rh, self.rmin)];

    def extractsem(self):
        dw = [('1学期',1), ('上学期',1), ('秋季学期:',1), ('秋季', 1), ('第一学期',1), ('一学期',1), ('下半年',1), ('2学期',2), ('下学期',2), ('春季学期',2), ('春季',2), ('第二学期',2), ('二学期',2), ('上半年',2)];
        for w in dw:
            try:
                ret1 = re.findall(w[0], self.st);
                if (len(ret1) == 0):
                    continue;
                self.sem = w[1];
                self.st = self.st.replace(ret1[0], '');
                break;
            except:
                c = 1;
            
    def extractLR(self):#时间区间提取
        self.st = re.sub(r"到|至",'-', self.st);
        tmp = [-1] * 12;
        dw = ['年', '月', '日', '时|点'];
        isFind = 0;
        for i in range(0, 8, 2):
            try:
                st1 = "\d+-+\d+.*"+dw[i//2];
                ret = re.findall(st1, self.st);
                tmplist = re.findall(r"\d+", ret[0]);
                tmp[i] = int(tmplist[0]);
                tmp[i+1] = int(tmplist[1]);
                self.st = self.st.replace(ret[0], '');
                if (not(dw[i//2] == '年' and "学年" in ret[0])):
                    isFind = 1;
            except:
                c = 1;
        try:
            st1 = "\d+:\d+-+\d+:\d+";
            ret = re.findall(st1, self.st);
            tmplist = re.findall(r"\d+", ret[0]);
            self.st = self.st.replace(ret[0], '');
            tmp[6] = int(tmplist[0]);
            tmp[8] = int(tmplist[1]);
            tmp[7] = int(tmplist[2]);
            tmp[9] = int(tmplist[3]);
            isfind = 1;
        except:
            c = 1;
        self.lyear = max(self.lyear, tmp[0]);
        self.ryear = max(self.ryear, tmp[1]);
        self.lmonth = max(self.lmonth, tmp[2]);
        self.rmonth = max(self.rmonth, tmp[3]);
        self.lday = max(self.lday, tmp[4]);
        self.rday = max(self.rday, tmp[5]);
        self.lh = max(self.lh, tmp[6]);
        self.rh = max(self.rh, tmp[7]);
        self.lmin = max(self.lmin, tmp[8]);
        self.rmin = max(self.rmin, tmp[9]);
        return isFind;
    
    def extractYMDHM(self):#年月日时分提取
        tmp = [-1] * 12;
        dw = ['年', '月', '日', '时|点'];
        isFind = 0;
        for i in range(0, 8, 2):
            try:
                st1 = "\d+学*"+dw[i//2];
                ret = re.findall(st1, self.st);
                tmp[i] = int(re.findall(r"\d+", ret[0])[0]);
                self.st = self.st.replace(ret[0], '');
                isFind = 1;
                tmp[i+1] = int(re.findall(r"\d+", ret[1])[0]);
                self.st = self.st.replace(ret[1], '');
            except:
                c = 1;
        
        try:
            st1 = "\d+:\d+";
            ret = re.findall(st1, self.st);
            tmplist = re.findall(r"\d+", ret[0]);
            self.st = self.st.replace(ret[0], '');
            tmp[6] = int(tmplist[0]);
            tmp[8] = int(tmplist[1]);
            tmplist = re.findall(r"\d+", ret[1]);
            tmp[7] = int(tmplist[0]);
            tmp[9] = int(tmplist[1]);
            self.st = self.st.replace(ret[1], '');
        except:
            c = 1;
        self.lyear = max(self.lyear, tmp[0]);
        self.ryear = max(self.ryear, tmp[1]);
        self.lmonth = max(self.lmonth, tmp[2]);
        self.rmonth = max(self.rmonth, tmp[3]);
        self.lday = max(self.lday, tmp[4]);
        self.rday = max(self.rday, tmp[5]);
        self.lh = max(self.lh, tmp[6]);
        self.rh = max(self.rh, tmp[7]);
        self.lmin = max(self.lmin, tmp[8]);
        self.rmin = max(self.rmin, tmp[9]);
        
    def debug(self):
        print(self.isinter);
        print(self.sem, self.lyear, self.lmonth, self.lday, self.lh, self.lmin, sep = ' ');
        print(self.sem, self.ryear, self.rmonth, self.rday, self.rh, self.rmin, sep = ' ');
        print(self.st)

if (__name__ == "__main__"):
    with open("text.txt", encoding='utf-8') as fp:
        st = fp.read();
        #print(re.findall("第二学期", st));
        a = timesplit();
        a.analyze("【教师|学生】2019-2020学年第二学期停调课信息（实时更新）");

    
