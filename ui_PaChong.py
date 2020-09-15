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


def scroll_down(driver, times, browser):
    for i in range(times):
        browser.setText("开始执行第" + str(i + 1) + "次下拉操作")
        for j in range(5):
            driver.execute_script("window.scrollBy(0, 500);")  # 执行JavaScript实现网页下拉倒底部
            time.sleep(1)  # 等待2秒，页面加载出来再执行下拉操作

        browser.setText("第" + str(i + 1) + "次下拉操作执行完毕")
        browser.setText("第" + str(i + 1) + "次等待网页加载......")
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


def scratchNovel(book_url, Browser, label):
    label.setText('开始网页get请求')
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
            idx +=1
            label.setText("处理 " + str(idx) + r"/" + str(maxidx) + r'   ' + str(midx) + '/' + str(maxmidx))
            title = t.contents
            url = t['href']
            page = driver.get(url)
            pageContent = BeautifulSoup(driver.page_source, 'lxml').find('div', class_='content')
            content += '\n' + title[0] + '\n'
            Browser.append(title[0])
            subcontent = ''
            for p in pageContent.contents[1:-1]:
                if p.contents:
                    subcontent += p.contents[0]
            subcontent = re.sub('<.>', '', subcontent)
            content += subcontent
            Browser.moveCursor(Browser.textCursor().End)
            time.sleep(0.3)  # 切换任务给GUI进行刷新
            # print(content.encode('utf8'))
    with open('novel.txt', 'w', encoding='utf-8') as f:
        f.write(content)
    label.setText('操作完成')


def scratchPic(keyWord, Browser, label):
    srb = keyWord.encode('utf8')
    web_url = staticUrl
    #
    lb = QtWidgets.QLabel(Browser)
    lb.setPixmap(QtGui.QBitmap('music.png'))
    lb.setFixedSize(100, 150)
    lb.move(100, 100)
    for b in srb:
        web_url += '%' + str(hex(b))[-2:].upper()
    folder_path = staticFolderPath + '\\' + keyWord
    label.setText('开始网页get请求')

    time.sleep(0.01)  # 等待3秒，页面加载出来再执行下拉操作
    MainWindow.show()
    opt = webdriver.ChromeOptions()
    # 把chrome设置成无界面模式，不论windows还是linux都可以，自动适配对应参数
    opt.headless = True
    driver = webdriver.Chrome(options=opt)
    driver.get(web_url)
    scroll_down(driver=driver, times=1, browser=label)  # 执行网页下拉到底部操作，执行3次
    label.setText('开始获取所有a标签')
    time.sleep(0.01)  # 等待3秒，页面加载出来再执行下拉操作
    all_a = BeautifulSoup(driver.page_source, 'lxml').find_all('li',
                                                               class_='imgitem')  # 获取网页中的class为cV68d的所有a标签
    label.setText('开始创建文件夹')
    time.sleep(0.01)  # 等待3秒，页面加载出来再执行下拉操作
    is_new_folder = mkdir(folder_path)  # 创建文件夹，并判断是否是新创建
    label.setText('开始切换文件夹')
    time.sleep(0.01)  # 等待3秒，页面加载出来再执行下拉操作
    os.chdir(folder_path)  # 切换路径至上面创建的文件夹

    label.setText(get_time_str() + "img标签的数量是：" + str(len(all_a)))  # 这里添加一个查询图片标签的数量，来检查我们下拉操作是否有误
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
        label.setText(get_time_str() + ' 处理第' + str(idx) + '/' + str(len(all_a)) + '张图片')
        time.sleep(0.01)  # 等待3秒，页面加载出来再执行下拉操作
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
            time.sleep(0.01)  # 等待3秒，页面加载出来再执行下拉操作
            continue

        picWidth = 150
        picHeight = 150
        img_name = re.sub("[#!@$%?&*^]", '', img_name)  # 去除文件名中可能存在的乱码
        if is_new_folder:
            bl = save_url_file(img_url, img_name, label)  # 调用save_img方法来保存图片
            if bl:
                s = r'<img src=' + img_name + r' width = "' + str(picWidth) + \
                    r'" height="' + str(picHeight) + r'" border="15"> '
                Browser.insertHtml(s)
            time.sleep(1)  # 防止太频繁操作被服务器干掉
        else:
            if img_name not in file_names:
                bl = save_url_file(img_url, img_name, label)  # 调用save_img方法来保存图片
                if bl:
                    s = r'<img src=' + img_name + r' width = "' + str(picWidth) + \
                        r'" height="' + str(picHeight) + r'" border="15"> '
                    Browser.insertHtml(s)
                time.sleep(1)  # 防止太频繁操作被服务器干掉
            else:
                print("该图片已经存在：" + img_name + "，不再重新下载。")
                s = r'<img src=' + img_name + r' width = "' + str(picWidth) + \
                    r'" height="' + str(picHeight) + r'" border="15"> '
                Browser.insertHtml(s)
                time.sleep(0.3)  # 等待3秒，页面加载出来再执行下拉操作
        Browser.moveCursor(Browser.textCursor().End)
        time.sleep(0.3)  # 切换任务给GUI进行刷新

    label.setText('操作完成')


def save_url_file(url, file_name, browser):  # 保存图片
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


class Ui_MyPaChong(object):
    def setupUi(self, MyPaChong):
        MyPaChong.setObjectName("MyPaChong")
        MyPaChong.setWindowModality(QtCore.Qt.ApplicationModal)
        MyPaChong.setEnabled(True)
        MyPaChong.resize(800, 600)
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        MyPaChong.setFont(font)
        MyPaChong.setToolTip("")
        MyPaChong.setToolTipDuration(5)
        MyPaChong.setWhatsThis("")
        self.centralwidget = QtWidgets.QWidget(MyPaChong)
        self.centralwidget.setObjectName("centralwidget")
        self.lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit.setGeometry(QtCore.QRect(80, 420, 113, 20))
        self.lineEdit.setObjectName("lineEdit")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(200, 420, 81, 23))
        self.pushButton.setToolTip("")
        self.pushButton.setObjectName("pushButton")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(80, 400, 54, 12))
        self.label.setObjectName("label")
        self.textBrowser = QtWidgets.QTextBrowser(self.centralwidget)
        self.textBrowser.setGeometry(QtCore.QRect(100, 40, 531, 271))
        self.textBrowser.setObjectName("textBrowser")
        self.label_tips = QtWidgets.QLabel(self.centralwidget)
        self.label_tips.setGeometry(QtCore.QRect(100, 320, 300, 22))
        self.label_tips.setObjectName("label_tips")
        self.label_tips.setText('tips')

        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(560, 320, 75, 23))
        self.pushButton_2.setObjectName("pushButton_2")
        self.lineEdit_2 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_2.setGeometry(QtCore.QRect(420, 420, 151, 20))
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.pushButton_3 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_3.setGeometry(QtCore.QRect(590, 420, 75, 23))
        self.pushButton_3.setObjectName("pushButton_3")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(420, 400, 54, 12))
        self.label_2.setObjectName("label_2")
        self.pushButton_4 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_4.setGeometry(QtCore.QRect(80, 450, 75, 23))
        self.pushButton_4.setObjectName("pushButton_4")
        self.pushButton_5 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_5.setGeometry(QtCore.QRect(420, 450, 75, 23))
        self.pushButton_5.setObjectName("pushButton_5")
        MyPaChong.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MyPaChong)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 23))
        self.menubar.setObjectName("menubar")
        MyPaChong.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MyPaChong)
        self.statusbar.setObjectName("statusbar")
        MyPaChong.setStatusBar(self.statusbar)

        self.retranslateUi(MyPaChong)
        self.pushButton.clicked.connect(self.getPics)
        self.pushButton_2.clicked.connect(self.textBrowser.clear)
        self.pushButton_3.clicked.connect(self.getNovle)
        self.pushButton_4.clicked.connect(self.lineEdit.clear)
        self.pushButton_5.clicked.connect(self.lineEdit_2.clear)
        QtCore.QMetaObject.connectSlotsByName(MyPaChong)

    def retranslateUi(self, MyPaChong):
        _translate = QtCore.QCoreApplication.translate
        MyPaChong.setWindowTitle(_translate("MyPaChong", "爬虫小工具"))
        self.lineEdit.setToolTip(_translate("MyPaChong", "图片关键词"))
        self.pushButton.setText(_translate("MyPaChong", "爬取百度图片"))
        self.label.setText(_translate("MyPaChong", "图片信息"))
        self.pushButton_2.setText(_translate("MyPaChong", "清除窗口"))
        self.pushButton_3.setText(_translate("MyPaChong", "爬取小说"))
        self.label_2.setText(_translate("MyPaChong", "小说网址"))
        self.pushButton_4.setText(_translate("MyPaChong", "清除输入"))
        self.pushButton_5.setText(_translate("MyPaChong", "清除输入"))
        # scratchPic(self.lineEdit.text(), self.textBrowser)

    def getNovle(self):
        self.textBrowser.clear()
        t1 = threading.Thread(target=scratchNovel, args=(self.lineEdit_2.text(), self.textBrowser, self.label_tips))
        t1.start()

    def getPics(self):
        self.textBrowser.clear()
        t1 = threading.Thread(target=scratchPic, args=(self.lineEdit.text(), self.textBrowser, self.label_tips))
        t1.start()

    def testTask(self, browser):
        browser.append('testTask')
        QtWidgets.QApplication.processEvents()


if __name__ == "__main__":
    import sys

    App = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MyPaChong()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(App.exec_())
