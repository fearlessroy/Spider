# -*- coding = utf-8 -*-

import logging
import requests
import time
import json
import html
from datetime import datetime

from weixincrawler.utils import headers_to_dict, sub_dict, str_to_dict
from weixincrawler.models import Post
from urllib.parse import urlsplit

requests.packages.urllib3.disable_warnings()
logging.basicConfig(level=logging.INFO)

logger = logging.getLogger(__name__)


class WeixinCrawler:
    def crawl(self, offset=0):
        """
        抓取更多文章
        :return:
        """
        url = "https://mp.weixin.qq.com/mp/profile_ext?action=getmsg&__biz=MjM5ODIyMTE0MA==&f=json&offset={offset}&count=10&is_ok=1&scene=124&uin=777&key=777&pass_ticket=zMERN05Nyw11W6aZCrtHj&wxtoken=&appmsg_token=938_ptkUwD7%TTtYug~~&x5=0&f=json".format(
            offset=offset)
        headers = """
            Host: mp.weixin.qq.com
            Accept-Encoding: br, gzip, deflate
            Cookie: devicetype=iOS11.2.1; lang=zh_CN; pass_ticket=zMERN051HHridaMCrtHj; version=16060124; wap_sid2=CLu+yYYBEnBaNXJa1jOHFDcwYTd4VGlJblhVV21BUExsYS1jUkZVNml5dG
            Accept: */*
            User-Agent: Mozilla/5.0 (iPhone; CPU iPhone OS 11_2_1 like Mac OS X) AppleWebKit/604.4.7 (KHTML, like Gecko) Mobile/15C153 MicroMessenger/6.6.1 NetType/WIFI Language/zh_CN
            Referer: https://mp.weixin.qq.com/mp/profile_ext?action=home&__biz=M==&scene=124&devicetype=iOS11.2.1&version=16060124&lang=zh_CN&nettype=WIFI&a8scene=3&fontScale=100&pass_ticket=zMERN05NywBiiXudj5x7o2q%2B8ZHa7FHARilreOrtHj&wx_header=1
            Accept-Language: zh-cn
            X-Requested-With: XMLHttpRequest"""
        headers = headers_to_dict(headers)
        response = requests.get(url, headers=headers, verify=False)
        result = response.json()
        if result.get("ret") == 0:
            msg_list = result.get("general_msg_list")
            offset = result.get("next_offset")
            logger.info("抓取数据: offset={},data={}".format(offset, msg_list))
            self.save(msg_list)
            # 递归调用
            has_next = result.get("can_msg_continue")
            if has_next == 1:
                next_offset = result.get("next_offset")
                time.sleep(2)
                self.crawl(next_offset)
            else:
                # 错误消息
                logger.error("无法正确获取内容，请重新从Fillder中获取请求参数")
                exit()

    @staticmethod
    def save(msg_list):
        msg_list = msg_list.replace("\/", "/")
        data = json.loads(msg_list)
        msg_list = data.get("list")
        for msg in msg_list:
            p_date = msg.get("comm_msg_info").get("datetime")
            msg_info = msg.get("app_msg_ext_info")  # 非图文消息没有此字段
            if msg_info:
                WeixinCrawler._insert(msg_info, p_date)
                multi_msg_info = msg_info.get("multi_app_msg_item_list")
                for msg_item in multi_msg_info:
                    WeixinCrawler._insert(msg_item, p_date)
            else:
                logger.warning(u"此消息不是图文推送，data=%s" % json.dumps(msg.get("comm_msg_info")))

    @staticmethod
    def _insert(item, p_date):
        keys = ('title', 'author', 'content_url', 'digest', 'cover', 'source_url')
        sub_data = sub_dict(item, keys)
        post = Post(**sub_data)
        p_date = datetime.fromtimestamp(p_date)
        post["p_date"] = p_date
        logger.info('save data %s ' % post.title)
        try:
            post.save()
        except Exception as e:
            logger.error("保存失败 data=%s" % post.to_json(), exc_info=True)

    @staticmethod
    def update_post(post):
        """
        post 参数是从mongodb读取出来的一条数据
        稍后就是对这个对象进行更新保存
        :param post:
        :return:
        """
        # 这个参数是我从Fiddler中拷贝出 URL，然后提取出查询参数部分再转换成字典对象
        # 稍后会作为参数传给request.post方法
        data_url_params = {'__biz': 'MjM5ODIyMTE0MA==',
                           'appmsg_type': '9',
                           'mid': '2650970509',
                           'sn': 'cae3bf171580e5b03ad910209c6d4881',
                           'idx': '1',
                           'scene': '38',
                           'title': '%E4%B8%AD%E5%9B%BD%E4%BA%92%E8%81%94%E7%BD%91%E5%8F%91%E5%B1%95%E5%8F%B2%E4%B8%8A%E6%9C%89%E8%BF%87%E9%BE%8C%E9%BE%8A%E7%9A%84%E7%AB%9E%E4%BA%89%E6%A1%88%E4%BE%8B&',
                           'ct': '1515141239',
                           'abtest_cookie': 'AwABAAoADAANAAcA/IgeAAyKHgCGih4Ai4oeAJCKHgCVih4An4oeAAAA',
                           'devicetype': 'iOS11.2.1',
                           'version': '/mmbizwap/zh_CN/htmledition/js/appmsg/index3af55a.js',
                           'f': 'json',
                           'r': '0.12955197160846676',
                           'is_need_ad': '1',
                           'comment_id': '3393728981',
                           'is_need_reward': '1',
                           'both_ad': '0',
                           'reward_uin_count': '30',
                           'msg_daily_idx': '1',
                           'is_original': '0',
                           'uin': '777',
                           'key': '777',
                           'pass_ticket': 'zMERNHHridaMCrtHj',
                           'wxtoken': '2040505533',
                           'devicetype': 'iOS11.2.1',
                           'clientversion': '16060124',
                           'appmsg_token': '938_aAOgTCf3Y5q4UDN',
                           'f': 'json'
                           }  # appmsg_token 记得用最新的

        # url转义处理
        content_url = html.unescape(post.content_url)
        # 截取content_url的查询参数部分
        content_url_params = urlsplit(content_url).query
        # 将参数转化为字典类型
        content_url_params = str_to_dict(content_url_params, "&", "=")
        # 更新到data_url
        data_url_params.update(content_url_params)
        body = "is_only_read=1&req_id=0720RNp6aZ3Wi3kZxY5Uu5Kf&pass_ticket=zMERN05Nyw11W6aZ1wY%252BkB%252BiiXudj5x7o2q%252B8ZHa7FHARilreO41HHridaMCrtHj&is_temp_url=0"
        data = str_to_dict(body, "&", "=")

        # 通过Fiddler 获取 最新的值
        headers = """
            Host: mp.weixin.qq.com
            Accept: */*
            X-Requested-With: XMLHttpRequest
            Accept-Language: zh-cn
            Accept-Encoding: br, gzip, deflate
            Content-Type: application/x-www-form-urlencoded; charset=UTF-8
            Origin: https://mp.weixin.qq.com
            User-Agent: Mozilla/5.0 (iPhone; CPU iPhone OS 11_2_1 like Mac OS X) AppleWebKit/604.4.7 (KHTML, like Gecko) Mobile/15C153 MicroMessenger/6.6.1 NetType/WIFI Language/zh_CN
            Connection: keep-alive
            Referer: https://mp.weixin.qq.com/s?__biz=MjM5ODIyMTE0MA==&mid=2650970509&idx=1&sn=cae3bf171580e5b03ad910209c6d4881&chksm=bd383db68a4fb4a02805d47f91990a6df95cc76a363c5782f651daa9666735217e1daaf2cfaa&scene=0&ascene=7&devicetype=iOS11.2.1&version=16060124&nettype=WIFI&abtest_cookie=AwABAAoADAANAAcA%2FIgeAAyKHgCGih4Ai4oeAJCKHgCVih4An4oeAAAA&lang=zh_CN&fontScale=100&pass_ticket=zMERN05Nyw11W6aZ1wY%2BkB%2BiiXudj5x7o2q%2B8ZHa7FHARilreO41HHridaMCrtHj&wx_header=1
            Content-Length: 155
            Cookie: rewardsn=ca237a91f29b; devicetype=iOS11.2.1; lang=zh_CN; pass_ticket=zMERN++8ZHa7FridaMCrtHj; version=16060124; wap_sid2=CLu+yYYBEnBaNXJaWng0U3dJQk1jOHFDcTBHd0N4eDNwSHJ0OTlzZXdqZlBNZzRwM3Exem5BcG8zNTV0bWxXWE85UU5qTDdka0tDUDJJeWJmR3h2X0VFNUU0eS1hUEdSTEIzVFlMQkdpU0FEYk5CNXEtU3FBd0FBMJO6yNIFOA1AAQ==; wxtokenkey=fa2e3a7d88d3d24d8ba5b90cafbe7a92839e80a3921676b635242479af7d8d86; wxuin=282222395; pgv_pvid=7554882136; sd_cookie_crttime=1507731239197; sd_userid=9961507731239197"""

        headers = str_to_dict(headers)

        data_url = "https://mp.weixin.qq.com/mp/getappmsgext"

        r = requests.post(data_url, data=data, verify=False, params=data_url_params, headers=headers)

        result = r.json()
        if result.get("appmsgstat"):
            post['read_num'] = result.get("appmsgstat").get("read_num")
            post['like_num'] = result.get("appmsgstat").get("like_num")
            post['reward_num'] = result.get("reward_total_count")
            post['u_date'] = datetime.now()
            logger.info("「{0}」read_num: {1} like_num: {2} reward_num: {3}".format
                        (post.title, post['read_num'], post['like_num'], post['reward_num']))
            post.save()
        else:
            logger.warning("没有获取的真实数据，请检查请求参数是否正确，返回的数据为：data=%s" % r.text)
            exit()


if __name__ == "__main__":
    crawler = WeixinCrawler()
    # crawler.crawl()
    for post in Post.objects(reward_num=0):
        crawler.update_post(post)
        time.sleep(2)
