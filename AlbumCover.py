from selenium import webdriver
from bs4 import BeautifulSoup
import requests
import os

class AlbumCover():
    """
    从网易抓取专辑封面图片
    参考 https://www.cnblogs.com/Albert-Lee/p/6276847.html
    """
    def __init__(self):
        self.init_url = "https://music.163.com/#/search/m/?s=LinkinPark&type=10" #请求网址
        self.folder_path = "C:\D\LinkinPark" #想要存放的文件目录

    def save_img(self, url, file_name):  ##保存图片
        print('开始请求图片地址，过程会有点长...')
        img = self.request(url)
        print('开始保存图片')
        f = open(file_name, 'ab')
        f.write(img.content)
        print(file_name, '图片保存成功！')
        f.close()

    def request(self, url):  # 封装的requests 请求
        r = requests.get(url)  # 像目标url地址发送get请求，返回一个response对象。有没有headers参数都可以。
        return r

    def mkdir(self, path):  ##这个函数创建文件夹
        path = path.strip()
        isExists = os.path.exists(path)
        if not isExists:
            print('创建名字叫做', path, '的文件夹')
            os.makedirs(path)
            print('创建成功！')
            return True
        else:
            print(path, '文件夹已经存在了，不再创建')
            return False

    def get_files(self, path):  # 获取文件夹中的文件名称列表
        pic_names = os.listdir(path)
        return pic_names

    def spider(self):
        print("Start!")
        driver = webdriver.Chrome()
        driver.get(self.init_url)
        driver.switch_to.frame("g_iframe")
        html = driver.page_source

        self.mkdir(self.folder_path)  # 创建文件夹
        print('开始切换文件夹')
        os.chdir(self.folder_path)  # 切换路径至上面创建的文件夹

        file_names = self.get_files(self.folder_path)  # 获取文件夹中的所有文件名，类型是list

        all_li = BeautifulSoup(html, 'lxml').find('div', class_='ztag j-flag').find_all('a')
        # print(type(all_li))

        for li in all_li:
            if not li.find('img'):
                continue
            print(li)
            album_img = li.find('img')['src']
            album_name = li.find('span', class_='msk')['title']
            end_pos = album_img.index('?')
            album_img_url = album_img[:end_pos]

            photo_name = album_name.replace('/', '').replace(':', ',') + '.jpg'
            print(album_img_url, photo_name)

            if photo_name in file_names:
                print('图片已经存在，不再重新下载')
            else:
                self.save_img(album_img_url, photo_name)

album_cover = AlbumCover()
album_cover.spider()