# -*- coding=utf-8 -*-
import codecs
import re

import jieba.analyse
import matplotlib.pyplot as plt
import requests
from scipy.misc import imread
from wordcloud import WordCloud

headers = {
    'Host': 'm.weibo.cn',
    'Referer': 'https://m.weibo.cn/u/xxxxxxxxx',  # 个人uid
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.101 Safari/537.36'
}

'''
https://m.weibo.cn/api/container/getIndex?uid=2350042112&luicode=10000011&
lfid=100103type%3D3%26q%3D%E4%B8%8D%E7%9D%A1%E4%B8%8D%E7%9D%A1%E5%B0%B1%E4%B8%8D%E7%9D%A1l&type=uid&value=2350042112&
containerid=1076032350042112

uid=xxxxxxxxx
luicode=10000011&
lfid=100103type%3D3%26q%3D%E4%B8%8D%E7%9D%A1%E4%B8%8D%E7%9D%A1%E5%B0%B1%E4%B8%8D%E7%9D%A1l&
type=uid&
value=2350042112&
containerid=1076032350042112
'''


def clean_html(raw_html):
    pattern = re.compile(r'<.*?>|转发微博|//:|Repost|，|？|。|、|分享图片|回复@.*?:|//@.*')
    text = re.sub(pattern, '', raw_html)
    return text


url = 'https://m.weibo.cn/api/container/getIndex'

params = {
    'uid': '{uid}',
    'luicode': '10000011',
    # 'featurecode': '20000320',
    'type': 'uid',
    'value': '2350042112',
    'containerid': '{containerid}',
    'page': '{page}'
}


def fetch_data(uid=None, container_id=None):
    '''

    :param uid:
    :param container_id:
    :return: 抓取数据,并保存在csv文件
    '''
    page = 0
    total = 203  # 根据api total字段而来
    blogs = []
    for i in range(0, total // 10):
        params['uid'] = uid
        params['page'] = str(page)
        params['containerid'] = container_id
        res = requests.get(url, params=params, headers=headers)
        cards = res.json().get('cards')

        for card in cards:
            if card.get('card_type') == 9:
                text = card.get('mblog').get('text')
                text = clean_html(text)
                blogs.append(text)
        page += 1
        print('抓取第%d页，目前总共抓取了%d条微薄' % (page, len(blogs)))

        with codecs.open('weibo1.txt', 'w', encoding='utf-8') as f:
            f.write('\n'.join(blogs))


def grey_color_func(word, font_size, position, orientation, random_state=None, **kwargs):
    s = 'hsl(0, 0%%, %d%%)' % 0
    return s


def generate_image():
    data = []
    jieba.analyse.set_stop_words("stopwords.txt")

    with codecs.open('weibo1.txt', 'r', encoding="utf-8") as f:
        for text in f.readlines():
            data.extend(jieba.analyse.extract_tags(text, topK=20))  # 关键字提取
        data = ' '.join(data)
        mask_img = imread('xxxxx.jpg', flatten=True)  # imread接收图片的完整路径为参数，也可以是文件指针，返回numpy.ndarray类型的矩阵

        wordcloud = WordCloud(font_path='MSYH.TTC',  # 支持中文的字体，默认字体无法支持中文，导致生成词云全部为方框
                              background_color='white',  # Background color for the word cloud image
                              mask=mask_img).generate(data)  # mask : nd-array or None (default=None)

        plt.imshow(wordcloud.recolor(color_func=grey_color_func, random_state=3),
                   interpolation='bilinear')  # 双线性的
        plt.axis('off')
        plt.savefig('heart.jpg', dpi=1600)  # dpi 每英寸点数


if __name__ == "__main__":
    # fetch_data('2350042xxx', '1076032350042112')
    generate_image()
