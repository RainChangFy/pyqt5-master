from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

# from PyQt5.QtCore import Qt.QT
import math
from TimeClock.Clock_Time import MyWidget




class Clock_paint(QLabel):
    # 老式钟表
    def __init__(self,parent  =None):
        super(Clock_paint,self).__init__(parent)
        self.timer = QTimer()  # 定时器
        self.timer.timeout.connect(self.update)
        self.timer.start(1000)  # 每1s 更新一次

    def textRectF(self,radius,pointsize,angle):

        recf = QRectF()
        recf.setX(radius*math.cos(angle*math.pi/180.0)-pointsize*2)
        recf.setY(radius*math.sin(angle*math.pi/180.0)-pointsize/2.0)
        recf.setWidth(pointsize*4)#宽度、高度
        recf.setHeight(pointsize)
        return recf

    def paintEvent(self, event):

        hour_points = [QPoint(5,8),QPoint(-5,8),QPoint(0,-30)]
        minute_points = [QPoint(5,8),QPoint(-5,8),QPoint(0,-65)]
        second_points = [QPoint(5,8),QPoint(-5,8),QPoint(0,-80)]

        hour_color = QColor(200,100,0,200)
        minute_color = QColor(0,127,127,150)
        second_color = QColor(0,160,230,150)

        min_len = min(self.width(),self.height())
        time = QTime.currentTime() #获取当前时间
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.translate(self.width()/2,self.height()/2)#平移到窗口中心
        painter.scale(min_len/200.0,min_len/200.0) #进行尺度缩放

        #----------绘制时针------------
        painter.setPen(Qt.NoPen)
        painter.setBrush(hour_color)#颜色
        painter.save()
        # 根据 1小时时= 30°，水品方向逆时针旋转时针
        painter.rotate(30.0*((time.hour()+time.minute()/60.0)))
        painter.drawConvexPolygon(QPolygon(hour_points))
        painter.restore() # save 退出，可重新设置画笔

        painter.setPen(hour_color)
        #绘制小时线(360/12 = 30度)
        for i in range(12):
            painter.drawLine(88,0,96,0)#绘制水平线
            painter.rotate(30.0)# 原有旋转角度上进行旋转；

        radius = 100 # 半径
        font = painter.font()
        font.setBold(True)
        painter.setFont(font)
        pointSize = font.pointSize()#字体大小
        # print(pointSize)

        #绘制小时文本
        for i in range(12):
            nhour = i + 3 # 从水平 3 点进行绘制
            if(nhour>12):
                nhour -= 12
            painter.drawText(self.textRectF(radius*0.8,pointSize,i*30),Qt.AlignCenter,str(nhour))

        #绘制分针;
        painter.setPen(Qt.NoPen)
        painter.setBrush(minute_color)
        painter.save()

        # 1分钟为6°，
        painter.rotate(6.0*(time.minute()+time.second()/60.0))
        painter.drawConvexPolygon(QPolygon(minute_points))
        painter.restore()

        #绘制分针线
        painter.setPen(minute_color)
        for i in range(60):
            if(i%5 !=0):
                painter.drawLine(92,0,96,0)
            painter.rotate(6.0)

        #绘制秒针
        painter.setPen(Qt.NoPen)
        painter.setBrush(second_color)
        painter.save()
        #绘制秒线
        painter.rotate(6.0*time.second())
        painter.drawConvexPolygon(QPolygon(second_points))
        painter.restore()

        painter.setPen(second_color)
        for i in range(360):
            if(i%5!=0 or i%30!=0):#绘制
                painter.drawLine(94,0,96,0)
            painter.rotate(1.0)#旋转
class My_Widget(QWidget):

    def __init__(self,parent = None):
        super(My_Widget,self).__init__(parent)

        self.label1 = Clock_paint()
        self.label2 = MyWidget()
        self.horizon_layout = QHBoxLayout()
        self.horizon_layout.addWidget(self.label1)
        self.horizon_layout.addWidget(self.label2)
        self.setLayout(self.horizon_layout)
        self.setWindowTitle('时钟--《公号:小张Python》')
        self.setWindowIcon(QIcon('clock.jpg'))
if __name__ =='__main__':
    import sys
    app = QApplication(sys.argv)
    my_widget = My_Widget()
    my_widget.show()
    sys.exit(app.exec())


