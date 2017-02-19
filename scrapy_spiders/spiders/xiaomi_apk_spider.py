# -*- coding: utf-8 -*-
# 使用requests获取网页源代码
import requests
import re

# from flask import redirect
# 目标页面
# html=requests.get('http://app.mi.com/topList')
# html.encoding='utf-8'
# print html.text

# 获取引用detail页面
# link=re.findall('</a><h5><a href="(.*?)"',html.text,re.S)
# for each in link:
#     print each
# print len(link) #应用页面首页共有排名前48的应用程序
# for i in range(2,5)


# 循环把48个apk爬取出来
# i=0
# url01='http://app.mi.com'+link[0]
# print url01
# # redirect(url)
# html02=requests.get(url01)
# html02.encoding='utf-8'
# #print html02.text
# download=re.findall('class="app-info-down"><a href="(.*?)" class="download">',html02.text,re.S)
# print download
# url02='http://app.mi.com'+download[0]
# print url02
# i=0
# load01=requests.get(url02)
# fp=open('load01\\'+str(i)+'.apk','wb')
# fp.write(load01.content)
# fp.close()

link = []
for i in range(1, 4):
    html = requests.get('http://app.mi.com/topList?page=' + str(i))
    html.encoding = 'utf-8'
    link.extend(re.findall('</a><h5><a href="(.*?)"', html.text, re.S))
    # if len(link)>100:#没有什么用，主要还是到第三页时还没到100
    #     break
print(len(link))
# for each in link:
#     print each


j = 0
for each in link:
    url01 = 'http://app.mi.com' + each
    html02 = requests.get(url01)
    html02.encoding = 'utf-8'
    download = re.findall('class="app-info-down"><a href="(.*?)" class="download">', html02.text, re.S)
    url02 = 'http://app.mi.com' + download[0]
    load01 = requests.get(url02)
    fp = open('load01\\' + str(j) + '.apk', 'wb')
    fp.write(load01.content)
    fp.close()
    j += 1
    if j >= 100:
        break
