from bs4 import BeautifulSoup
import re
import urllib.request,urllib.error
import csv
import codecs
import pymysql
import MySQL_Class as mc
import mailClass as ml



re_url = re.compile(r'<a href="(.*htm)"')
re_title = re.compile(r'<h1 class="arti_title">(.*)</h1>')


def askURL(baseurl):
    headers={
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36"
    }
    req = urllib.request.Request(baseurl,headers=headers)
    html=""
    try:
        res = urllib.request.urlopen(req,timeout=3000)
        html = res.read().decode("utf-8")
        #print(html)
    except urllib.error.URLError as e:
        if hasattr(e,"code"):
            print(e,"code")
        if hasattr(e,"reason"):
            print(e,"reason")
    soup = BeautifulSoup(html,"html.parser")

    string = []
    for i in range(1,15):
        i = "news n" + str(i) +" clearfix"
        string.append(i)

    items = []
    for i in string:
        item = soup.find_all("li",class_=i)[0]
        item = str(item)
        items.append(item)

    dirurls = []
    for i in items:
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
    urls,htmls = zip(*zip_)
    datalist = []
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

if __name__ == '__main__':
    # final_result = []
    # for i in range(1,11):
    #     baseurl = "https://jw.nju.edu.cn/ggtz/list{}.htm".format(str(i))
    #     final_result = final_result+spider(baseurl)
    # for i in final_result:
    #     print(i)
    sql1 = mc.sql(mc.config1)
    # sql1.create_table()
    # sql1.lines_insert(final_result)


    # get = sql1.select_lines()
    # for i in get:
    #     print(i[0],i[1])


    # data = []
    # for i in range(1,21):
    #     data.append([1,i])
    # sql1.update(data)
    users = ['wsy13638318926@outlook.com','2574945327@qq.com']
    get = sql1.select_lines()
    
    mails = []
    for i in get:
        i = list(i)
        i[4] = str(i[4])
        print(i)
        mail = ml.mailmaker(i)
        a = ml.mail(mail,users)
        a.confirmToSend()
    