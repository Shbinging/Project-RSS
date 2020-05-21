from bs4 import BeautifulSoup
import re
import urllib.request,urllib.error
import csv
import codecs
import pymysql

baseurl = "https://jw.nju.edu.cn/ggtz/list1.htm"
re_url = re.compile(r'<a href="(.*htm)"')
art_title = re.compile(r'<h1 class="arti_title">(.*)</h1>')
art_time = re.compile(r'<span class="arti_update">发布时间：(.*)</span><span class="arti_views"')
art_contents = re.compile(r'style="font-size:18px;line-height:1.5em;">(.*)</span>')

def askURL():
    headers={
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36"
    }
    req = urllib.request.Request(baseurl,headers=headers)
    html=""
    try:
        res = urllib.request.urlopen(req)
        html = res.read().decode("utf-8")
        #print(html)
    except urllib.error.URLError as e:
        if hasattr(e,"code"):
            print(e,"code")
        if hasattr(e,"reason"):
            print(e,"reason")
    soup = BeautifulSoup(html,"html.parser")
    item = soup.find_all("li",class_="news n1 clearfix")[0]
    item = str(item)
    dirurl = 'https://jw.nju.edu.cn/'+re.findall(re_url,item)[0]
    # print(dirurl)
    req2 = urllib.request.Request(dirurl,headers=headers)
    finalhtml=""
    try:
        res2 = urllib.request.urlopen(req2)
        finalhtml = res2.read().decode("utf-8")
        #print(html)
    except urllib.error.URLError as e:
        if hasattr(e,"code"):
            print(e,"code")
        if hasattr(e,"reason"):
            print(e,"reason")
    return finalhtml


def getData():
    html = askURL()
    soup = BeautifulSoup(html,"html.parser")
    item = soup.find_all("div",class_="article")[0]
    item_temp = str(item)
    title = re.findall(art_title,item_temp)[0]
    time = re.findall(art_time,item_temp)[0]
    print(time,title,sep=" ")
    contents = soup.find("div",class_="wp_articlecontent")
    # for i in contents.children:
    #     print(i.string)
    content = ""
    for i in contents.stripped_strings:
        content = content+i
    print(content)








if __name__ == '__main__':
    askURL()
    getData()