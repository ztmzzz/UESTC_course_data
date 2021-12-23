#!/usr/bin/python
# -*- coding: UTF-8 -*-
# Filename: if_name_main.py

from bs4 import BeautifulSoup     #网页解析，获取数据
import re       #正则表达式，进行文字匹配
import urllib.request,urllib.error      #制定URL，获取网页数据
import xlwt     #进行excel操作
import sqlite3  #进行SQLite数据库操作



def main():
    baseurl = "https://movie.douban.com/top250?start="
    #爬取网页
    datalist = getData(baseurl)
    savepath = "豆瓣电影Top250.xls"
    dbpath = "movie.db"
    #保存数据
    # savepath='G:/war/douban/豆瓣电影Top250-3.xls'
    saveData(datalist,savepath)
    #saveData2DB(datalist,dbpath)

    # askURL("https://movie.douban.com/top250?start=")

#影片详情链接的规则
findLink = re.compile(r'<a href="(.*?)">')     #创建正则表达式对象，表示规则（字符串的模式）
#影片图片
findImgSrc = re.compile(r'<img.*src="(.*?)"',re.S)   #re.S 让换行符包含在字符中
#影片片名
findTitle = re.compile(r'<span class="title">(.*)</span>')
#影片评分
findRating = re.compile(r'<span class="rating_num" property="v:average">(.*)</span>')
#找到评价人数
findJudge = re.compile(r'<span>(\d*)人评价</span>')
#找到概况
findInq = re.compile(r'<span class="inq">(.*)</span>')
#找到影片的相关内容
findBd = re.compile(r'<p class="">(.*?)</p>',re.S)


#一个功能对应一个函数
#爬取网页
def getData(baseurl):
    datalist = []
    for i in range(0,10):       #调用获取页面信息的函数，10次
        url = baseurl + str(i*25)
        html = askURL(url)      #保存获取到的网页源码

         # 2.逐一解析数据
        soup = BeautifulSoup(html,"html.parser")
        for item in soup.find_all('div',class_="item"):     #查找符合要求的字符串，形成列表
            #print(item)   #测试：查看电影item全部信息
            data = []    #保存一部电影的所有信息
            item = str(item)

            #影片详情的链接
            link = re.findall(findLink,item)[0]     #re库用来通过正则表达式查找指定的字符串
            data.append(link)                       #添加链接

            imgSrc = re.findall(findImgSrc,item)[0]
            data.append(imgSrc)                     #添加图片

            titles = re.findall(findTitle,item)     #片名可能只有一个中文名，没有外国名
            if len(titles) == 2:
                ctitle = titles[0]                  #添加中文名
                data.append(ctitle)
                otitle = titles[1].replace("/","")  #去掉无关的符号
                data.append(otitle)                 #添加外国名
            else:
                data.append(titles[0])
                data.append(' ')        #外国名字留空

            rating = re.findall(findRating,item)[0]
            data.append(rating)                        #添加评分

            judgeNum = re.findall(findJudge,item)[0]
            data.append(judgeNum)                       #提加评价人数

            inq = re.findall(findInq,item)
            if len(inq) != 0:
                inq = inq[0].replace("。","")    #去掉句号
                data.append(inq)                # 添加概述
            else:
                data.append(" ")                #留空

            bd = re.findall(findBd,item)[0]
            bd = re.sub('<br(\s+)?/>(\s+)?'," ",bd)   #去掉<br/>
            bd = re.sub('/'," ",bd)     #替换/
            data.append(bd.strip())     #去掉前后的空格

            datalist.append(data)       #把处理好的一部电影信息放入datalist

    return datalist



#得到指定一个URL的网页内容
def askURL(url):
    head = {                #模拟浏览器头部信息，向豆瓣服务器发送消息
        "User-Agent": "Mozilla / 5.0(Windows NT 10.0; Win64; x64) AppleWebKit / 537.36(KHTML, like Gecko) Chrome / 80.0.3987.122  Safari / 537.36"
    }
                            #用户代理，表示告诉豆瓣服务器，我们是什么类型的机器、浏览器（本质上是告诉浏览器，我们可以接收什么水平的文件内容）

    request = urllib.request.Request(url,headers=head)  #使用request封装url和头部信息
    html = ""
    #异常处理
    try:
        response = urllib.request.urlopen(request)
        html = response.read().decode("utf-8")
        #print(html)
    except urllib.error.URLError as e:
        if hasattr(e,"code"):
            print(e.code)
        if hasattr(e,"reason"):
            print(e.reason)
    return html




#保存数据
def saveData(datalist,savepath):
    print("save....")
    book = xlwt.Workbook(encoding="utf-8",style_compression=0)  #创建workbook对象
    sheet = book.add_sheet('豆瓣电影Top250',cell_overwrite_ok=True)    #创建工作表
    col = ("电影详情链接","图片链接","影片中文名","影片外国名","评分","评价数","概况","相关信息")
    for i in range(0,8):
        sheet.write(0,i,col[i]) #列名
    for i in range(0,250):
        print("第%d条" %(i+1))
        data = datalist[i]
        for j in range(0,8):
            sheet.write(i+1,j,data[j])      #数据

    book.save(savepath)       #保存


# def saveData2DB(datalist,dbpath):
#     init_db(dbpath)
#     conn = sqlite3.connect(dbpath)
#     cur = conn.cursor()
#
#     for data in datalist:
#         for index in range(len(data)):
#             if index == 4 or index == 5:
#                 continue
#             data[index] = '"'+data[index]+'"'
#         sql = '''
#                 insert into movie250 (
#                 info_link,pic_link,cname,ename,score,rated,instroduction,info)
#                 values(%s)'''%",".join(data)
#         print(sql)
#         cur.execute(sql)
#         conn.commit()
#     cur.close()
#     conn.close()
#
#
#
# def init_db(dbpath):
#     sql = '''
#         create table movie250
#         (
#         id integer primary key autoincrement,
#         info_link text,
#         pic_link text,
#         cname varchar,
#         ename varchar,
#         score numeric ,
#         rated numeric ,
#         instroduction text,
#         info text
#         )
#
#     '''  #创建数据表
#     conn = sqlite3.connect(dbpath)
#     cursor = conn.cursor()
#     cursor.execute(sql)
#     conn.commit()
#     conn.close()



if __name__ == "__main__":          #当程序执行时
#调用函数
    main()
    #init_db("movietest.db")
    print("爬取完毕！")