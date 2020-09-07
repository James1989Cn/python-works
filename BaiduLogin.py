from selenium import webdriver  # 导入Selenium
import requests
from bs4 import BeautifulSoup  # 导入BeautifulSoup 模块
import os  # 导入os模块
import time
import re
import datetime
web_url = "https://www.baidu.com/"
# wd = webdriver.Chrome()
# wd.get(web_url)
# cookieBefore = wd.get_cookies()
# print(cookieBefore)
# wd.find_element_by_xpath('//*[@id="u1"]/a').click() #点击登陆
# time.sleep(3)  # 等待界面弹出 #
# wd.find_element_by_xpath('//*[@id="TANGRAM__PSP_11__footerULoginBtn"]').click() #点击用户名登陆
# time.sleep(3)  # 等待界面弹出 #
# wd.find_element_by_xpath('//*[@id="TANGRAM__PSP_11__userName"]').send_keys('17608117975') #填写对话框
# wd.find_element_by_xpath('//*[@id="TANGRAM__PSP_11__password"]').send_keys('wsfghaha123') #填写对话框
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
cookiesAfter = [{'domain': '.baidu.com', 'httpOnly': False, 'name': 'H_PS_PSSID', 'path': '/', 'secure': False, 'value': '32643_32606_1462_32572_7544_32328_31253_32046_7552_32676_32117_31709_32581'},
{'domain': '.baidu.com', 'expiry': 1858389526, 'httpOnly': True, 'name': 'BDUSS_BFESS', 'path': '/', 'sameSite': 'None', 'secure': True, 'value': 'E0zZWNwbGNHUDdRM05MMFdXZjdFZG5QTktDLTdiaFZJbUVKLTh0cnJ2Z1dQM2xmRVFBQUFBJCQAAAAAAAAAAAEAAAAmn7oHxKfHuc7atvsAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAABayUV8WslFfT'},
{'domain': '.baidu.com', 'expiry': 1858389526, 'httpOnly': True, 'name': 'BDUSS', 'path': '/', 'secure': False, 'value': 'E0zZWNwbGNHUDdRM05MMFdXZjdFZG5QTktDLTdiaFZJbUVKLTh0cnJ2Z1dQM2xmRVFBQUFBJCQAAAAAAAAAAAEAAAAmn7oHxKfHuc7atvsAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAABayUV8WslFfT'},
{'domain': '.baidu.com', 'expiry': 1630725506, 'httpOnly': False, 'name': 'BAIDUID', 'path': '/', 'secure': False, 'value': '9D2E55EFCC777675997F46B500770BD1:FG=1'},
{'domain': '.baidu.com', 'expiry': 3746673153, 'httpOnly': False, 'name': 'BIDUPSID', 'path': '/', 'secure': False, 'value': '9D2E55EFCC777675CA4CB5E0ECF23D7E'},
{'domain': '.baidu.com', 'expiry': 3746673153, 'httpOnly': False, 'name': 'PSTM', 'path': '/', 'secure': False, 'value': '1599189506'},
{'domain': 'www.baidu.com', 'expiry': 1600053528, 'httpOnly': False, 'name': 'BD_UPN', 'path': '/', 'secure': False, 'value': '12314753'},
{'domain': 'www.baidu.com', 'httpOnly': False, 'name': 'BD_HOME', 'path': '/', 'secure': False, 'value': '1'}]
for c in cookiesAfter:
    wd.add_cookie(c)
# 刷新页面，可以看到已经是登录状态了，至此完成的使用cookie 的登录。
wd.refresh()
