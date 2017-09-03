# -*-encoding=utf-8 -*-

import matplotlib.pyplot as plt
from wordcloud import WordCloud
import jieba

'''
什么是词云呢？词云又叫文字云，是对文本数据中出现频率较高的“关键词”在视觉上的突出呈现，
形成关键词的渲染形成类似云一样的彩色图片，从而一眼就可以领略文本数据的主要表达意思

其实“词云”是对网络文本中出现频率较高的“关键词”予以视觉上的突出，形成“关键词云层”或“关键词渲染”，
从而过滤掉大量的无意义信息，使浏览者只要一眼扫过词云图片就可以领略文章或者网页内容的主旨。

生产词云的原理其实并不复杂，大体分成5步：
    1.对文本数据进行分词，也是众多NLP文本处理的第一步，对于wordcloud中的process_text（）方法，主要是停词的处理
    2.计算每个词在文本中出现的频率，生成一个哈希表。词频计算相当于各种分布式计算平台的第一案例wordcount， 和各种语言的hello world 程序具有相同的地位了，呵呵。
    3.根据词频的数值按比例生成一个图片的布局，类IntegralOccupancyMap 是该词云的算法所在，是词云的数据可视化方式的核心。
    4.将词按对应的词频在词云布局图上生成图片，核心方法是generate_from_frequencies,不论是generate（）还是generate_from_text（）都最终到generate_from_frequencies
    5.完成词云上各词的着色,默认是随机着色
'''

text_from_file_with_apath = open('test.txt', encoding='utf-8').read()

wordlist_after_jieba = jieba.cut(text_from_file_with_apath, cut_all=True)
wl_space_split = " ".join(wordlist_after_jieba)

my_wordcloud = WordCloud(font_path='MSYH.TTC').generate(wl_space_split)

plt.imshow(my_wordcloud)
plt.axis("off")
plt.show()
