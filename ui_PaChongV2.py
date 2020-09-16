# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_PaChong.ui'
#
# Created by: PyQt5 UI code generator 5.12
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
from selenium import webdriver  # 导入Selenium
import requests
from bs4 import BeautifulSoup  # 导入BeautifulSoup 模块
import os  # 导入os模块
import time
import datetime
import re
import threading

staticUrl = 'https://image.baidu.com/search/index?tn=baiduimage&ipn=r&ct=201326592&cl=2&lm=-1&st=-1&fm' \
            '=result&fr=&sf=1&fmq=1599026437060_R&pv=&ic=&nc=1&z=&hd=&latest=&copyright=&se=1&showtab=0&fb' \
            '=0&width=&height=&face=0&istype=2&ie=utf-8&hs=2&sid=&word='
staticFolderPath = r'C:\D\BaiduPicture'

gBrowserTxt = ""
gLabelStr = ""

windowWidth = 800
windowHeight = 600
browserBorder = 5
browserHeightFactor = 0.8
picWidth = 80
picHeight = 80


def scroll_down(driver, times):
    global gLabelStr
    for i in range(times):
        gLabelStr = "开始执行第" + str(i + 1) + "次下拉操作"
        for j in range(5):
            driver.execute_script("window.scrollBy(0, 500);")  # 执行JavaScript实现网页下拉倒底部
            time.sleep(1)  # 等待2秒，页面加载出来再执行下拉操作

        gLabelStr = "第" + str(i + 1) + "次等待网页加载......"
        time.sleep(3)  # 等待3秒，页面加载出来再执行下拉操作


def mkdir(path):  # 这个函数创建文件夹
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


def get_time_str():
    curr = datetime.datetime.now()
    micors = curr.microsecond / 1000
    s1 = datetime.datetime.strftime(curr, '%H:%M:%S.') + '%03d' % micors + ':'
    return s1


def scratchNovel(book_url):
    global gBrowserTxt
    global gLabelStr
    gLabelStr = '开始网页get请求'
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
    midx = 0
    maxmidx = len(all_a)
    for cc in all_a:
        midx += 1
        a = cc.find_all('a')  # 获取网页中的的所有a标签
        idx = 0
        maxidx = len(a)
        for t in a:
            idx += 1
            gLabelStr = "处理 " + str(idx) + r"/" + str(maxidx) + r'   ' + str(midx) + '/' + str(maxmidx)
            title = t.contents
            url = t['href']
            page = driver.get(url)
            pageContent = BeautifulSoup(driver.page_source, 'lxml').find('div', class_='content')
            content += '\n' + title[0] + '\n'
            gBrowserTxt += title[0] + '\n'
            subcontent = ''
            for p in pageContent.contents[1:-1]:
                if p.contents:
                    subcontent += p.contents[0]
            subcontent = re.sub('<.>', '', subcontent)
            content += subcontent
            # print(content.encode('utf8'))
    with open('novel.txt', 'w', encoding='utf-8') as f:
        f.write(content)
    gLabelStr = '操作完成'


def scratchPic(keyWord):
    global gBrowserTxt
    global gLabelStr
    srb = keyWord.encode('utf8')
    web_url = staticUrl
    for b in srb:
        web_url += '%' + str(hex(b))[-2:].upper()
    folder_path = staticFolderPath + '\\' + keyWord

    gLabelStr = '开始网页get请求'
    opt = webdriver.ChromeOptions()
    # 把chrome设置成无界面模式，不论windows还是linux都可以，自动适配对应参数
    # opt.headless = True
    driver = webdriver.Chrome(options=opt)
    driver.get(web_url)
    scroll_down(driver=driver, times=1)  # 执行网页下拉到底部操作，执行3次
    gLabelStr = '开始获取所有a标签'
    all_a = BeautifulSoup(driver.page_source, 'lxml').find_all('li',
                                                               class_='imgitem')  # 获取网页中的class为cV68d的所有a标签
    gLabelStr = '开始创建文件夹'
    is_new_folder = mkdir(folder_path)  # 创建文件夹，并判断是否是新创建
    gLabelStr = '开始切换文件夹'
    os.chdir(folder_path)  # 切换路径至上面创建的文件夹

    gLabelStr = get_time_str() + "img标签的数量是：" + str(len(all_a))  # 这里添加一个查询图片标签的数量，来检查我们下拉操作是否有误
    file_names = os.listdir(folder_path)  # 获取文件家中的所有文件名，类型是list
    img_list = []  # 保存文件列表，防止重复
    idx = 1
    attrstr = 'data-objurl'
    for a in all_a:  # 循环每个标签，获取标签中图片的url并且进行网络请求，最后保存图片
        if a.has_attr(attrstr):
            img_str = a[attrstr]  # a标签中完整的style字符串
            print('图片url是：' + img_str)
        else:
            continue
        gLabelStr = get_time_str() + ' 处理第' + str(idx) + '/' + str(len(all_a)) + '张图片'
        idx += 1
        img_url = a[attrstr]
        if img_url in img_list:
            continue
        img_list.append(img_url)

        # 截取url中参数前面、网址后面的字符串为图片名
        img_names = re.findall('[^/]*\.jp[e]?g|[^/]*\.png|[^/]*\.gif', img_url)
        if len(img_names) > 0:
            img_name = img_names[0]
        else:
            print('文件信息不能识别')
            continue

        img_name = re.sub("[#!@$%?&*^]", '', img_name)  # 去除文件名中可能存在的乱码
        if is_new_folder:
            bl = save_url_file(img_url, img_name)  # 调用save_img方法来保存图片
            if bl:
                s = r'<img src=' + img_name + r' width = "' + str(picWidth) + \
                    r'" height="' + str(picHeight) + r'" border="15"> '
                gBrowserTxt += s
            time.sleep(1)  # 防止太频繁操作被服务器干掉
        else:
            if img_name not in file_names:
                bl = save_url_file(img_url, img_name)  # 调用save_img方法来保存图片
                if bl:
                    s = r'<img src=' + img_name + r' width = "' + str(picWidth) + \
                        r'" height="' + str(picHeight) + r'" border="15"> '
                    gBrowserTxt += s
                time.sleep(1)  # 防止太频繁操作被服务器干掉
            else:
                print("该图片已经存在：" + img_name + "，不再重新下载。")
                s = r'<img src=' + img_name + r' width = "' + str(picWidth) + \
                    r'" height="' + str(picHeight) + r'" border="15"> '
                gBrowserTxt += s

    gLabelStr = '操作完成'


def save_url_file(url, file_name):  # 保存图片
    print('开始请求图片地址，过程会有点长...')
    try:
        img = requests.get(url)
    except:
        print('请求该图片失败')
        return False
    print('开始保存图片' + file_name)
    f = open(file_name, 'ab')
    f.write(img.content)
    print(file_name + '图片保存成功！')
    f.close()
    return True


class Ui_MyPaChong(QtWidgets.QWidget):
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        self.setWindowTitle("爬虫小工具")
        self.resize(windowWidth, windowHeight)
        self.timer_id = 0
        self.task = 0
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        self.setFont(font)
        self.centralWidget = QtWidgets.QWidget(self)

        self.textBrowser = QtWidgets.QTextBrowser(self.centralWidget)
        browserHeight = int(windowHeight * browserHeightFactor)
        browserWidth = windowWidth - 2 * browserBorder
        browserBottom = browserBorder + browserHeight
        self.textBrowser.setGeometry(QtCore.QRect(browserBorder, browserBorder, browserWidth, browserHeight))
        self.label_tips = QtWidgets.QLabel(self.centralWidget)
        self.label_tips.setGeometry(QtCore.QRect(browserBorder, browserBottom, 300, 22))
        self.label_tips.setText('tips')
        self.browserClearButton = QtWidgets.QPushButton(self.centralWidget)
        self.browserClearButton.setGeometry(QtCore.QRect(windowWidth - browserBorder - 75, browserBottom, 75, 23))
        self.browserClearButton.setText("清除显示")
        # self.checkBox = QtWidgets.QCheckBox("自动下拉", self.centralWidget)
        # self.checkBox.setGeometry(QtCore.QRect(windowWidth - browserBorder - 75 - 80, browserBottom, 75, 23))

        self.keyWordEdit = QtWidgets.QLineEdit(self.centralWidget)
        keyWordEditWidth = 120
        self.keyWordEdit.setGeometry(QtCore.QRect(browserBorder, browserBottom + 50, keyWordEditWidth, 23))
        self.picButton = QtWidgets.QPushButton(self.centralWidget)
        self.picButton.setGeometry(QtCore.QRect(browserBorder + keyWordEditWidth + 10, browserBottom + 50, 81, 23))
        self.picButton.setText("爬取百度图片")
        self.label = QtWidgets.QLabel(self.centralWidget)
        self.label.setGeometry(QtCore.QRect(browserBorder, browserBottom + 30, 54, 12))
        self.label.setText("图片信息")
        self.picEditClearButton = QtWidgets.QPushButton(self.centralWidget)
        self.picEditClearButton.setGeometry(QtCore.QRect(browserBorder, browserBottom + 75, 75, 23))
        self.picEditClearButton.setText("清除输入")

        self.novelEdit = QtWidgets.QLineEdit(self.centralWidget)
        novelEditWidth = 150
        novelEditWidthLeft = windowWidth - browserBorder - 75 - novelEditWidth - 10
        self.novelEdit.setGeometry(QtCore.QRect(novelEditWidthLeft, browserBottom + 50, novelEditWidth, 23))
        self.novelButton = QtWidgets.QPushButton(self.centralWidget)
        self.novelButton.setGeometry(QtCore.QRect(novelEditWidthLeft + novelEditWidth + 10, browserBottom + 50, 75, 23))
        self.novelButton.setText("爬取小说")
        self.label_2 = QtWidgets.QLabel(self.centralWidget)
        self.label_2.setGeometry(QtCore.QRect(novelEditWidthLeft, browserBottom + 30, 54, 12))
        self.label_2.setText("小说网址")
        self.novelEditClearButton = QtWidgets.QPushButton(self.centralWidget)
        self.novelEditClearButton.setGeometry(QtCore.QRect(novelEditWidthLeft, browserBottom + 75, 75, 23))
        self.novelEditClearButton.setText("清除输入")

        self.picButton.clicked.connect(self.getPics)
        self.browserClearButton.clicked.connect(self.textBrowser.clear)
        self.novelButton.clicked.connect(self.getNovel)
        self.picEditClearButton.clicked.connect(self.keyWordEdit.clear)
        self.novelEditClearButton.clicked.connect(self.novelEdit.clear)

    def beforeTask(self):
        global gBrowserTxt
        global gLabelStr
        self.textBrowser.clear()
        self.label_tips.setText('tips')
        gBrowserTxt = ""
        gLabelStr = ""

    def afterTask(self):
        if self.timer_id:
            self.killTimer(self.timer_id)
            self.timer_id = 0
        self.task = 0

    def timerEvent(self, event):
        global gBrowserTxt
        global gLabelStr
        self.textBrowser.setText(gBrowserTxt)
        self.label_tips.setText(gLabelStr)
        self.textBrowser.moveCursor(self.textBrowser.textCursor().End)
        # if self.checkBox.checkState():
        #     self.textBrowser.moveCursor(self.textBrowser.textCursor().End)
        if not self.task.is_alive():
            self.afterTask()

    def getNovel(self):
        if self.task:
            return
        self.beforeTask()
        self.timer_id = self.startTimer(1000, timerType=QtCore.Qt.VeryCoarseTimer)
        self.task = threading.Thread(target=scratchNovel, args=(self.novelEdit.text(),))
        self.task.start()

    def getPics(self):
        if self.task:
            return
        self.beforeTask()
        self.timer_id = self.startTimer(1000, timerType=QtCore.Qt.VeryCoarseTimer)
        self.task = threading.Thread(target=scratchPic, args=(self.keyWordEdit.text(),))
        self.task.start()


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    window = Ui_MyPaChong()
    window.show()
    sys.exit(app.exec_())
