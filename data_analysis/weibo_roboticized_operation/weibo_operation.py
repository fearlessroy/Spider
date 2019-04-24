# -*- encoding=utf-8 -*-
from selenium import webdriver
import time

browser = webdriver.Chrome()


# 登录微博
def weibo_login(user_name, password):
    # 打开微博登录页面
    browser.get("https://passport.weibo.cn/signin/login")
    browser.implicitly_wait(5)
    time.sleep(1)
    # 填写登录信息：用户名、密码
    browser.find_element_by_id("loginName").send_keys(user_name)
    browser.find_element_by_id("loginPassword").send_keys(password)
    time.sleep(1)
    # 点击登录
    browser.find_element_by_id("loginAction").click()
    time.sleep(1)


# 设置用户名、密码
user_name = "xxxxxxx"
password = 'xxxxxxx'
weibo_login(user_name, password)


# 关注指定的用户
def add_follow(uid):
    browser.get('https://m.weibo.com/u/' + str(uid))
    time.sleep(1)
    # browser.find_element_by_id("follow").click()
    follow_buttion = browser.find_element_by_xpath('//div[@class="m-add-box m-followBtn"]')
    follow_buttion.click()
    time.sleep()
    # 选择分组
    group_button = browser.find_element_by_xpath('//div[@class="m-btn m-btn-white m-btn-text-black"]')
    group_button.click()
    time.sleep(1)


# 某个用户的 uid
uid = ''
add_follow(uid)


# 写评论
def add_comment(weibo_url, content):
    browser.get(weibo_url)
    browser.implicitly_wait(5)
    content_textarea = browser.find_element_by_css_selector('textarea.W_input').clear()
    content_textarea = browser.find_element_by_css_selector('textarea.W_input').send_keys(content)
    time.sleep(2)
    comment_button = browser.find_element_by_css_selector('.W_btn_a').click()
    time.sleep()


# 发文字微博
def post_weibo(content):
    # 跳转到用户的首页
    browser.get('https://weibo.com')
    browser.implicitly_wait(5)
    # 点击右上角的发布按钮
    post_button = browser.find_element_by_css_selector("[node-type='publish']").click()
    # 在弹出的文本框中输入内容
    content_text_area = browser.find_element_by_css_selector("textarea.W_input").send_keys(content)
    time.sleep(2)
    # 点击发布按钮
    post_button = browser.find_element_by_css_selector("[node-type='submit").click()
    time.sleep(1)


# 给指定的微博写评论
weibo_url = ''
content = 'Good Luck!'
# 自动发微博
content = 'xxx'
post_weibo(content)
