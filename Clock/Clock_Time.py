
from PyQt5.QtWidgets import QApplication,QMainWindow,QMessageBox,QWidget
from PyQt5.QtCore import *
from TimeClock.untitled import *
from PyQt5.Qt import Qt


class MyWidget(QWidget,Ui_Form):
    #电子表
    def __init__(self,parent = None):
        super(MyWidget,self).__init__(parent)
        self.setupUi(self)
        self.setStyleSheet('background-color')
        self.setWindowFlags(Qt.FramelessWindowHint)#无边框
        self.setAcceptDrops(True)
        self.lcdNumber.display('00:00:00')
        time_slot =QTimer(self)
        time_slot.timeout.connect(self.event_1)
        time_slot.start(1000)

    def event_1(self):
        time_format = QTime.currentTime()
        time_format = time_format.toString("hh:mm:ss")
        self.lcdNumber.display(time_format)
        QApplication.processEvents()

