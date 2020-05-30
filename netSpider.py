from bs4 import BeautifulSoup
import re
import urllib.request,urllib.error
import csv
import codecs
import mailClass as ml
import mysqlClass as mc


re_url = re.compile(r'<a href="(.*htm)"')
re_title = re.compile(r'<h1 class="arti_title">(.*)</h1>')


def askURL(baseurl):
    headers={
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36"
    }
    req = urllib.request.Request(baseurl,headers=headers)
    html=""
    try:
        res = urllib.request.urlopen(req,timeout=10000)
        html = res.read().decode("utf-8")
        #print(html)
    except urllib.error.URLError as e:
        if hasattr(e,"code"):
            print(e,"code")
        if hasattr(e,"reason"):
            print(e,"reason")
    soup = BeautifulSoup(html,"html.parser")
    string = []
    for i in range(1,6):
        i = "news n" + str(i) +" clearfix"
        string.append(i)

    items = []
    for i in string:
        item = soup.find_all("li",class_=i)[0]
        item = str(item)
        items.append(item)

    dirurls = []

    for i in items:
        if re.findall(re_url,i) == []:
            continue
        dirurl = 'https://jw.nju.edu.cn/'+re.findall(re_url,i)[0]
        dirurls.append(dirurl)
 
    # print(dirurl)


    finalhtmls=[]

    for i in dirurls:
        req2 = urllib.request.Request(i,headers=headers)
        try:
            res2 = urllib.request.urlopen(req2)
            finalhtml = res2.read().decode("utf-8")
            finalhtmls.append(finalhtml)
        except urllib.error.URLError as e:
            if hasattr(e,"code"):
                print(e,"code")
            if hasattr(e,"reason"):
                print(e,"reason")
    result = zip(dirurls,finalhtmls)
    return result



def getData(zip_):
    datalist = []
    urls,htmls = zip(*zip_)
    NUM = 1
    for html in htmls:
        data =[]
        soup = BeautifulSoup(html,"html.parser")
        temp = soup.find_all('div',class_="article")
        if temp == []:
            continue
        item = soup.find_all('div',class_="article")[0]
        strings_=item.stripped_strings
        strings = []
        for i in strings_:
            strings.append(i)
        time = strings[2]
        data.append(time)
        title = strings[0]
        data.append(title)
        for i in range(0,5):
            strings.remove(strings[0])
        content = ""
        for i in strings:
            content = content + i
        data.append(content)
        datalist.append(data)
        print(NUM)
        NUM = NUM+1
    for i in range(0,len(datalist)):
         datalist[i].append(urls[i])
    return datalist


def spider(a):
     pack_ = askURL(a)
     result = getData(pack_)
     return result

def netSpider():
    bad_url = []
    sql1 = mc.sql(mc.config3)
    sql1.create_table(1)
    final_result = []
    baseurl = "https://jw.nju.edu.cn/ggtz/list1.htm"
    a = spider(baseurl)
    compare_ = []
    to_sql = []
    b = sql1.select_lines(2)
    for i in b :
        # print(i[1])
        compare_.append(i)
    for i in a:
        if i not in compare_:
            to_sql.append(i)
    print("YSES")
    for i in to_sql:
        print(i[1])
    if to_sql == []:
        return 0
    else :
        sql1.lines_insert(1,to_sql)
        return 1
   

    
    
    
       



    # for i in range(13,16):
    #     baseurl = "https://jw.nju.edu.cn/ggtz/list{}.html".format(str(i))
    #     print(baseurl)
    #     try:
    #         sql1.lines_insert(1,spider(baseurl))
    #     except:
    #         bad_url.append(i)
    #         continue
    # for i in final_result:
    #     print(i)
    # print(bad_url)
    # get = sql1.select_lines(1)
    # k = 1
    # for i in get:
    #     print(i[0],i[1])
    #     print(k)
    #     k = k+1


#----------------------------------
#邮件测试
    # data = []
    # for i in range(1,21):
    #     data.append([1,i])
    # sql1.update(data)
    # users = ['1065254539@qq.com']
    # get = sql1.select_lines()
    

    # mails = []
    # for i in get:
    #     i = list(i)
    #     i[4] = str(i[4])
    #     print(i)
    #     mail = ml.mailmaker(i)
    #     a = ml.mail(mail,users)
    #     a.confirmToSend()

#--------------------------------
#内容识别测试

    # a = ta.timesplit()
    
    # for i in get:
    #     a.analyze(str(i))
   