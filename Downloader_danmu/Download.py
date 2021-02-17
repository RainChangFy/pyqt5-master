'''
@author:zeroing
@wx公众号：小张Python

'''
import requests
from pyquery import PyQuery as pq
import re
from PyQt5.QtWidgets import *
from PyQt5 import QtCore
from PyQt5.QtGui import *
from PyQt5.QtCore import QThread, pyqtSignal
import time
from bs4 import BeautifulSoup


class Ui_From(QWidget):
    '''UI 界面'''

    def __init__(self, parent=None):
        super(Ui_From, self).__init__(parent=parent)
        self.setWindowTitle("B站弹幕采集")
        self.setWindowIcon(QIcon('pic.jpg'))  # 图标
        self.top_label = QLabel("作者：小张\n 微信公号：小张Python")
        self.top_label.setAlignment(QtCore.Qt.AlignHCenter)
        self.top_label.setStyleSheet('color:red;font-weight:bold;')
        self.label = QLabel("B站视频url")
        self.label.setAlignment(QtCore.Qt.AlignHCenter)
        self.editline1 = QLineEdit()
        self.pushButton = QPushButton("开始下载")
        self.pushButton.setEnabled(False)  # 关闭启动
        self.Console = QListWidget()
        self.saveButton = QPushButton("保存至")
        self.layout = QGridLayout()
        self.layout.addWidget(self.top_label, 0, 0, 1, 2)
        self.layout.addWidget(self.label, 1, 0)
        self.layout.addWidget(self.editline1, 1, 1)
        self.layout.addWidget(self.pushButton, 2, 0)
        self.layout.addWidget(self.saveButton, 3, 0)
        self.layout.addWidget(self.Console, 2, 1, 3, 1)
        self.setLayout(self.layout)
        self.savepath = None

        self.pushButton.clicked.connect(self.downButton)
        self.saveButton.clicked.connect(self.savePushbutton)

        self.editline1.textChanged.connect(self.syns_lineEdit)

    def syns_lineEdit(self):
        if self.editline1.text():
            self.pushButton.setEnabled(True)  # 打开按钮

    def savePushbutton(self):
        savePath = QFileDialog.getSaveFileName(self, 'Save Path', '/', 'txt(*.txt)')
        if savePath[0]:  # 选中 txt 文件路径
            self.savepath = str(savePath[0])  # 进行赋值

    def downButton(self):
        if not self.label.text():
            QMessageBox.warning(self, 'error', '未提供下载的 url 链接，请重新尝试!', QMessageBox.Ok)
            return
        if not self.savepath:
            QMessageBox.warning(self, 'error', '保存路径为空，请重新尝试', QMessageBox.Ok)
            return

        url = str(self.editline1.text())
        item = QListWidgetItem()
        item.setText("已经获取链接:{}".format(url))
        self.Console.addItem(item)
        QApplication.processEvents()  # 刷新界面
        res = requests.get(url).text
        item1 = QListWidgetItem()
        item1.setText("正在解析中....")
        self.Console.addItem(item1)
        QApplication.processEvents()

        # result_url  =re.findall('.*?"baseUrl":"(.*?)","base_url".*?',res)[0]
        self.Work(res)
        if self.result_url:
            cid = str(self.result_url).split('/')[6]
            item2 = QListWidgetItem()
            item2.setText("获取到 cid 编号{}".format(cid))
            self.download_danmu(cid)  # 弹幕下载
        else:
            item2 = QListWidgetItem()
            item2.setText("文本解析错误，请重试\n")

        self.Console.addItem(item2)
        item3 = QListWidgetItem()
        item3.setText("弹幕保存至 {} 完毕".format(self.savepath))
        self.Console.addItem(item3)
        QApplication.processEvents()

    def download_danmu(self, cid):
        '''弹幕下载并存储'''

        url = 'http://comment.bilibili.com/{}.xml'.format(cid)

        f = open(self.savepath, 'w+', encoding='utf-8')  # 打开 txt 文件
        res = requests.get(url)
        res.encoding = 'utf-8'
        soup = BeautifulSoup(res.text, 'lxml')
        items = soup.find_all('d')  # 找到 d 标签

        for item in items:
            text = item.text
            f.write(text)
            f.write('\n')
        f.close()

    def Work(self, text):
        self.parse_text = Parsetext(text)
        self.parse_text.trigger.connect(self.signal_parse)
        self.parse_text.run()

    def signal_parse(self, value):
        if value:
            self.result_url = value


class Parsetext(QThread):
    trigger = pyqtSignal(str)  # 信号发射；

    def __init__(self, text, parent=None):
        super(Parsetext, self).__init__()
        self.text = text

    def __del__(self):
        self.wait()

    def run(self):
        print('解析 -----------{}'.format(self.text))
        result_url = re.findall('.*?"baseUrl":"(.*?)","base_url".*?', self.text)[0]
        self.trigger.emit(result_url)


if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    Ui_Widget = Ui_From()
    Ui_Widget.show()
    sys.exit(app.exec())
