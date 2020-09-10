from selenium import webdriver  # 导入Selenium
import requests
from bs4 import BeautifulSoup  # 导入BeautifulSoup 模块
import os  # 导入os模块
import time
import re
import datetime

web_url = "http://www.zongheng.com/"
search_url = "http://search.zongheng.com/s?keyword="
book_url = "http://book.zongheng.com/showchapter/903436.html"

print('开始网页get请求')
# 使用selenium通过PhantomJS来进行网络请求
# driver = webdriver.PhantomJS()
opt = webdriver.ChromeOptions()

# 把chrome设置成无界面模式，不论windows还是linux都可以，自动适配对应参数
# opt.set_headless()
opt.headless = True
driver = webdriver.Chrome(options=opt)
driver.get(book_url)
all_a = BeautifulSoup(driver.page_source, 'lxml').find_all('ul', class_='chapter-list clearfix')
content = ''
for cc in all_a:
    a = cc.find_all('a')  # 获取网页中的的所有a标签
    for t in a:
        title = t.contents
        url = t['href']
        page = driver.get(url)
        pageContent = BeautifulSoup(driver.page_source, 'lxml').find('div', class_='content')
        content += '\n' + title[0] + '\n'
        print(title[0])
        subcontent = ''
        for p in pageContent.contents[1:-1]:
            if p.contents:
                subcontent += p.contents[0]
        subcontent = re.sub('<.>', '', subcontent)
        content += subcontent
        # print(content.encode('utf8'))
with open('novel.txt', 'w', encoding='utf-8') as f:
    f.write(content)
