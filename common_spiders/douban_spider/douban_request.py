# -*- encoding=utf-8 -*-
import requests
import re


# url='https://movie.douban.com/top250'
# tag_page=requests.get(url)
# # print tag_page.text
# tag_page.encoding='utf-8'
# moviename=[]
# movie=re.findall(r'<span class="title">(.*?)</span>',tag_page.text,re.S)
# num=1
# for index,item in enumerate(movie):
#     if item.find("&nbsp")==-1:
#         moviename.append("Top"+str(num)+" "+item)
#         num+=1
# # print movie[47]
# for items in moviename:
#     print items

class DoubanSpider(object):
    def __init__(self):
        self.page = 1
        self.cur_url = 'https://movie.douban.com/top250?start={page}&&filter='
        self.movie_data = []
        self.top_num = 1
        print("...准备爬去豆瓣电影数据...")

    # 获取网页信息
    def get_page(self, cur_page):
        url = self.cur_url
        try:
            tag_page = requests.get(url.format(page=(cur_page - 1) * 25))

        except:
            print('exception')

        return tag_page

    def find_title(self, tag_page):
        moviename = []
        # 在Python的正则表达式中，有一个参数为re.S。它表示“.”（不包含外侧双引号，下同）的作用扩展到整个字符串，包括“\n”。
        movie = re.findall(r'<span class="title">(.*?)</span>', tag_page.text, re.S)
        for index, item in enumerate(movie):
            if item.find("&nbsp") == -1:
                moviename.append("Top" + str(self.top_num) + " " + item)
                self.top_num += 1
        self.movie_data.append(moviename)

    def start_spider(self):
        '''
        爬虫入口
        '''
        while self.page <= 4:
            tag_page = self.get_page(self.page)
            self.find_title(tag_page)
            self.page += 1


def domain():
    my_spider = DoubanSpider()
    my_spider.start_spider()
    for item1 in my_spider.movie_data:
        for item2 in item1:
            print(item2)
    print('...豆瓣爬虫爬取结束...')


if __name__ == "__main__":
    domain()
