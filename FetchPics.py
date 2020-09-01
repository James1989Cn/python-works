from selenium import webdriver  #导入Selenium
import requests
from bs4 import BeautifulSoup  #导入BeautifulSoup 模块
import os  #导入os模块
import time
import re

class BeautifulPicture():
    """
    从unsplash抓取图片
    参考 https://www.cnblogs.com/Albert-Lee/p/6276847.html
    """
    def __init__(self):  #类的初始化操作
        self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1'}  #给请求指定一个请求头来模拟chrome浏览器
        self.web_url = 'https://unsplash.com/t/travel'  #要访问的网页地址
        self.folder_path = 'C:\D\BeautifulPicture\Travel'  #设置图片要存放的文件目录

    def save_file_info(self):
        with open(self.folder_path+r'\rec.txt', 'a') as f:
            for ll in self.img_list:
                f.write(ll+' \n')

    def get_pic(self):
        print('开始网页get请求')
        # 使用selenium通过PhantomJS来进行网络请求
        # driver = webdriver.PhantomJS()
        driver = webdriver.Chrome()
        driver.get(self.web_url)
        self.scroll_down(driver=driver, times=3)  #执行网页下拉到底部操作，执行3次
        print('开始获取所有a标签')
        all_a = BeautifulSoup(driver.page_source, 'lxml').find_all('img', class_='_2VWD4 _2zEKz')  #获取网页中的class为cV68d的所有a标签
        print('开始创建文件夹')
        is_new_folder = self.mkdir(self.folder_path)  #创建文件夹，并判断是否是新创建
        print('开始切换文件夹')
        os.chdir(self.folder_path)   #切换路径至上面创建的文件夹

        print("img标签的数量是：", len(all_a))   #这里添加一个查询图片标签的数量，来检查我们下拉操作是否有误
        file_names = self.get_files(self.folder_path)  #获取文件家中的所有文件名，类型是list
        self.img_list = [] #保存文件列表，防止重复
        idx = 1
        for a in all_a: #循环每个标签，获取标签中图片的url并且进行网络请求，最后保存图片
            img_str = a['src'] #a标签中完整的style字符串
            print('处理第'+str(idx)+'张图片')
            idx += 1
            print('img标签的src内容是：', img_str)
            img_url = a['src']
            if img_url in self.img_list:
                continue
            self.img_list.append(img_url)
            # 注：为了尽快看到下拉加载的效果，截取高度和宽度部分暂时注释掉，因为图片较大，请求时间较长。
            #获取高度和宽度的字符在字符串中的位置
            # width_pos = img_url.index('&w=')
            # height_pos = img_url.index('&q=')
            # width_height_str = img_url[width_pos : height_pos] #使用切片功能截取高度和宽度参数，后面用来将该参数替换掉
            # print('高度和宽度数据字符串是：', width_height_str)
            # img_url_final = img_url.replace(width_height_str, '')  #把高度和宽度的字符串替换成空字符
            # print('截取后的图片的url是：', img_url_final)

            #截取url中参数前面、网址后面的字符串为图片名
            img_names = re.findall('photo-[0-9]*', img_url)
            img_name = img_names[0]+'.jpg'

            if is_new_folder:
                self.save_img(img_url, img_name)  # 调用save_img方法来保存图片
            else:
                if img_name not in file_names:
                    self.save_img(img_url, img_name)  # 调用save_img方法来保存图片
                else:
                    print("该图片已经存在：", img_name, "，不再重新下载。")
        self.save_file_info()

    def save_img(self, url, file_name): ##保存图片
        print('开始请求图片地址，过程会有点长...')
        img = self.request(url)
        print('开始保存图片'+file_name)
        f = open(file_name, 'ab')
        f.write(img.content)
        print(file_name,'图片保存成功！')
        f.close()

    def request(self, url):  #返回网页的response
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

    def scroll_down(self, driver, times):
        for i in range(times):
            print("开始执行第", str(i + 1),"次下拉操作")
            # driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")  #执行JavaScript实现网页下拉倒底部
            # time.sleep(3)  # 等待30秒，页面加载出来再执行下拉操作
            # driver.execute_script("window.scrollBy(0, -100);")  #执行JavaScript实现网页下拉倒底部
            for j in range(10):
                driver.execute_script("window.scrollBy(0, 500);")  #执行JavaScript实现网页下拉倒底部
                time.sleep(5)  # 等待30秒，页面加载出来再执行下拉操作

            print("第", str(i + 1), "次下拉操作执行完毕")
            print("第", str(i + 1), "次等待网页加载......")
            time.sleep(3)  # 等待30秒，页面加载出来再执行下拉操作

    def get_files(self, path):
        pic_names = os.listdir(path)
        return pic_names

beauty = BeautifulPicture()  #创建类的实例
beauty.get_pic()  #执行类中的方法