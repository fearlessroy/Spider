# -*-encoding=utf-8 -*-

import matplotlib.pyplot as plt
from wordcloud import WordCloud
import jieba

'''
什么是词云呢？词云又叫文字云，是对文本数据中出现频率较高的“关键词”在视觉上的突出呈现，
形成关键词的渲染形成类似云一样的彩色图片，从而一眼就可以领略文本数据的主要表达意思。
'''

text_from_file_with_apath = open('test.txt', encoding='utf-8').read()

wordlist_after_jieba = jieba.cut(text_from_file_with_apath, cut_all=True)
wl_space_split = " ".join(wordlist_after_jieba)

my_wordcloud = WordCloud(font_path='MSYH.TTC').generate(wl_space_split)

plt.imshow(my_wordcloud)
plt.axis("off")
plt.show()
