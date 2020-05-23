from MySQL_Class import sql;
from MySQL_Class import config1;
from MySQL_Class import config2;
from MySQL_Class import config2;
import jieba
import re
from timeAnalyze import timesplit;
config = {
        'host': 'localhost',
        'port': 3306,
        'database': 'test',
        'user': 'root',
        'password': 'abc@123',
        'charset': 'utf8',
        'use_unicode': True,
        'get_warnings': True,
    }
dataf = sql(config2);



a = '线下课、网课、阅读经典、研读课、通识课、网络考试、口语考试、计算机等级考试、补考、缓考、期末考试、毕业准备、转专业及分流、其他、重修、竞赛、四六级、交换'.split("、");

def sum(b):
    s = 0;
    for i in b:
        s += i;
    return s;

def sum1(b):
    s = 0;
    for i in b:
        s += i[0];
    return s;
def f(word, pattern):
    opt1 = "select * from f where word = "+"'"+word+"'";
    opt2 = "select %s from f"%pattern;
    if (not dataf.isExsist(opt1)):
        return 0;
    if (not dataf.isExsist(opt2)):
        return 0;
    d = dataf.select_lines(opt1);
    d = d[0][2:];
    ans = 0;
    e = 0;
    for i in range(0, len(a)): 
        if (a[i] == pattern):
            e = d[i];
            if (sum(d) != 0):
                ans = d[i] / sum(d);
    d = dataf.select_lines(opt2);
    if (sum1(d) != 0):
        ans = ans * e /sum1(d);
    return ans*100;

def refind(title):
    timer = timesplit();
    title = timer.analyze(title);
    print(title);
    title = title.replace("关于", "");
    title = title.replace("通知", "");
    title = title.replace("公告", "");
    title = title.replace("的", "");
    seg_list = jieba.lcut(title);
    mx = -1;
    ans = '';
    for pattern in a:
        s = 0;
        for word in seg_list:
            #if (pattern == "线下课"):
              #  print(word, '@',f(word, pattern), sep = '');
            s += f(word, pattern);
        print(pattern, s, sep = ' ');
        if (s > mx):
            mx = s;
            ans = pattern;
    return ans;

print(refind("2019年华东五校共享共建暑期课程-华为大数据创新训练营报名通知"));
"""
insert_order = "INSERT INTO test (time, title, info, url) VALUES (%s, %s, %s ,%s)"
#在这里输入插入语句，注意格式第一个括号里面是对应的栏目，后一个括号全部是%s

select_order = "SELECT title FROM test WHERE id IN (1,2,3,4,5,6)"
#在这里输入MySQL的SELECT语句

update_order = "UPDATE test SET status = %s WHERE id = %s"

delete_order = "DELETE from test WHERE id = %s "
"""




"""
i = 0;
for item in a:
    print(i, item ,sep = ' ');
    i += 1;
"""
"""
#人工对数据打标签

data = sql(config1);
data.create_table("ALTER TABLE test ADD COLUMN act VARCHAR(200)");
list1 = data.select_lines("SELECT act FROM test");
list2 = data.select_lines("SELECT title FROM test");
print(list1);
for i in range(0, 155):
    try:
        if (list1[i][0] != None):
            continue;
        else:
            print(list2[i]);
            tmp = int(input());
            st = "UPDATE test SET"+ " act = '"+ a[tmp] + "' WHERE id = " + str(i+1);
            data.update(st);
    except:
        print(i);

"""
"""
dataf = sql(config2);
#新建数据库
#word\活动

a = '线下课、网课、阅读经典、研读课、通识课、网络考试、口语考试、计算机等级考试、补考、缓考、期末考试、毕业准备、转专业及分流、其他、重修、竞赛、四六级、交换'.split("、");

for i in range(14,18):
    st = "alter table f add column %s int default 0"%a[i];
    dataf.update(st);


data = sql(config1);
list2 = data.select_lines("SELECT title FROM test");
for i in range(0, 130):
    title = list2[i][0];
    timer = timesplit();
    title = timer.analyze(title);
    print(title);
    title = title.replace("关于", "");
    title = title.replace("通知", "");
    title = title.replace("公告", "");
    seg_list = jieba.lcut(title);
    try:
        tmp = data.select_lines("select act from test where id = %s"%(i+1))[0][0];
        if (tmp == "其他"):
            continue;
    except:
        print(-2);
    tmp1 = dataf.select_lines("select word from f");
    for word in seg_list:
        opt = "select word from f where word =" + "'"+ word+ "'";
        print(opt);
        if (dataf.isExsist(opt)):
            dataf.update("update f set %s = %s +1 where word ="%(tmp, tmp) + "'" + word + "'");
        else:
            st = "insert into f (word, %s)"%tmp+ " values(" + "'"+ word + "'" + "," + "1)";
            print('new');
            dataf.update(st);
    

list3 = dataf.select_lines("select * from f");
print(list3);



"""
