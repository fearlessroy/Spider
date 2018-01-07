# -*- coding:utf-8 -*-
import requests

header = """
Host: mp.weixin.qq.com
Cookie: devicetype=iOS11.2.1; lang=zh_CN; pass_ticket=zMERN05Nyw11W6aZ1wY+kB+iiXudj5x7o2q+8ZHa7FHARilreO41HHridaMCrtHj; version=16060124; wap_sid2=CLu+yYYBEnBaNXJaWng0U3dJQk1jOHFDcTBHd0M3VHB0b0NLQnVndTZjOUVsMGoxU2VfT1NfTVEzSzRzM3pOSnlnX1NQWlUyS2ZiMDdNWEU0UFAwX3lDX3F0akkwcFpMU0M4cWdWU0Ytc1RyaTNGUXdaS3FBd0FBMKTox9IFOA1AlU4=; wxuin=282222395; rewardsn=c7fccf086d2af56cc639; wxtokenkey=12faf9f6ddecd843a0bcdf6845a449afe1d2ffcf270770ce2e24c2bfdf787467; pgv_pvid=7554882136; sd_cookie_crttime=1507731239197; sd_userid=9961507731239197
X-WECHAT-KEY: b02e1976269c718361d1e6d2e1fc492a0a1928d01f7e1cde93ed33cea9f0113f870a62800bdb574c86ac6f61cfef45536ab2f54cfacf05a7b1c560455cc612b2132761b6455fa4343d63df619d241222
X-WECHAT-UIN: MjgyMjIyMzk1
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
User-Agent: Mozilla/5.0 (iPhone; CPU iPhone OS 11_2_1 like Mac OS X) AppleWebKit/604.4.7 (KHTML, like Gecko) Mobile/15C153 MicroMessenger/6.6.1 NetType/WIFI Language/zh_CN
Accept-Language: zh-cn
Accept-Encoding: br, gzip, deflate
Connection: keep-alive
"""





def crawl(header):
    url = "https://mp.weixin.qq.com/mp/profile_ext?action=home&__biz=MjM5ODIyMTE0MA==&scene=124&devicetype=iOS11.2.1&version=16060124&lang=zh_CN&nettype=WIFI&a8scene=3&fontScale=100&pass_ticket=zMERN05Nyw11W6aZ1wY%2BkB%2BiiXudj5x7o2q%2B8ZHa7FHARilreO41HHridaMCrtHj&wx_header=1"
    header = headers_to_dict(header)
    response = requests.get(url, headers=header, verify=False)
    print(response.text)
    with open("weixin_history.html", "w", encoding="utf-8") as f:
        f.write(response.text)


def extract_data():
    """
    从html页面提取历史文章数据
    :param html_content 页面源码
    :return: 历史文章列表
    """
    import re
    import html
    import json
    with open('weixin_history.html', 'r',encoding='utf-8') as f:
        html_content = f.read()
    rex = "msgList = '({.*?})'"
    pattern = re.compile(pattern=rex, flags=re.S)
    match = pattern.search(html_content)
    if match:
        data = match.group(1)
        data = html.unescape(data)
        data = json.loads(data)
        articles = data.get("list")
        for item in articles:
            print(item)
        print(articles)
        return articles


if __name__ == "__main__":
    # crawl(header=header)
    extract_data()
