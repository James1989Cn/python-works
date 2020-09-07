from selenium import webdriver  # 导入Selenium
import requests
from bs4 import BeautifulSoup  # 导入BeautifulSoup 模块
import os  # 导入os模块
import time
import re
import datetime
web_url = "https://www.baidu.com/"
USERNAME = '你的用户名'
PWD = '你的用户密码'
# wd = webdriver.Chrome()
# wd.get(web_url)
# cookieBefore = wd.get_cookies()
# print(cookieBefore)
# wd.find_element_by_xpath('//*[@id="u1"]/a').click() #点击登陆
# time.sleep(3)  # 等待界面弹出 #
# wd.find_element_by_xpath('//*[@id="TANGRAM__PSP_11__footerULoginBtn"]').click() #点击用户名登陆
# time.sleep(3)  # 等待界面弹出 #
# wd.find_element_by_xpath('//*[@id="TANGRAM__PSP_11__userName"]').send_keys(USERNAME) #填写对话框
# wd.find_element_by_xpath('//*[@id="TANGRAM__PSP_11__password"]').send_keys(PWD) #填写对话框
# wd.find_element_by_xpath('//*[@id="TANGRAM__PSP_11__submit"]').click() #点击用户名登陆
# # 加一个休眠，这样得到的cookie 才是登录后的cookie,否则可能打印的还是登录前的cookie
# time.sleep(25)
# print("登录后！")
# cookiesAfter = wd.get_cookies()
# print("cookiesAfter:")
# print(cookiesAfter)
# wd.quit()

print("+++++++++++++++++++++++++")
print("cookieLogin")
wd = webdriver.Chrome()
# 清除一下cookie
wd.delete_all_cookies()
time.sleep(3)
wd.get(web_url)
# 打开浏览器后添加访问地址后，添加cookie
cookiesAfter = []# 跑一遍程序后可以直接给出cookies，跳过上面一半的步骤
for c in cookiesAfter:
    wd.add_cookie(c)
# 刷新页面，可以看到已经是登录状态了，至此完成的使用cookie 的登录。
wd.refresh()
