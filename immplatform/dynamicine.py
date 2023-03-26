import sys
from PyQt5.QtChart import QChartView, QChart, QSplineSeries, QValueAxis, QLineSeries, QScatterSeries
from PyQt5.QtCore import Qt, QTimer, QRandomGenerator, QPointF, QMargins
from PyQt5.QtGui import QPainter, QPen, QFont, QColor, QBrush
from PyQt5.QtWidgets import QApplication, QGraphicsView
from uitl import Refresher
import time, random
from setting_define import *

class CurveChartView(QChart):

    def __init__(self, hidchooser, main):
        super().__init__()
        self.hidchooser = hidchooser
        self.main = main
        self.forceCorrectnessFlag = False
        self.dragPointFlag = False
        self.seriesIndex = 0
        self.pointIndex = 0
        self.minValue = 0
        self.maxValue = 0
        self.minX = 0
        self.maxX = 10
        self.minY = 0
        self.maxY = 100
        self.curveIndex = 0
        self.map = [6908265, 2003199]
        self.color_map = self.map
        self.scatter1 = QScatterSeries()
        self.spline1 = QSplineSeries()
        for i in range(6):
            self.scatter1.append(i, 5 * i)
            self.spline1.append(i, 5 * i)

        self.scatter2 = QScatterSeries()
        self.spline2 = QSplineSeries()
        for i in range(6):
            self.scatter2.append(i, i * i)
            self.spline2.append(i, i * i)

        self.scatterList = []
        self.splineList = []
        self.scatterList.append(self.scatter2)
        self.splineList.append(self.spline2)
        for i, _ in enumerate(self.scatterList):
            self.scatter = self.scatterList[i]
            self.spline = self.splineList[i]
            pen = QPen()
            pen.setWidth(1)
            self.spline.setPen(pen)
            self.scatter.setMarkerShape(QScatterSeries.MarkerShapeCircle)
            self.scatter.setBorderColor(QColor(255, 0, 0))
            self.scatter.setBrush(QColor(255, 0, 0))
            self.scatter.setMarkerSize(8)
            self.addSeries(self.spline)
            self.addSeries(self.scatter)
            self.legend().hide()
            self.createDefaultAxes()
            self.axisY().setRange(self.minY, self.maxY)
            self.axisY().setTitleText('y')
            self.axisX().setRange(self.minX, self.maxX)
            self.axisX().setTitleText('x')
            self.setMargins(QMargins(1, 1, 1, 1))

    def __del__(self):
        self.chart_close = True


class DynamicLine(QChart):

    def __init__(self, hidchooser, main):
        super().__init__()
        self.hidchooser = hidchooser
        self.main = main
        self.chart_close = False
        self.layout().setContentsMargins(0, 0, 0, 0)
        self.setMargins(QMargins(0, 0, 0, 0))
        self.setBackgroundRoundness(0)
        self.x_min = 0
        self.x_max = 100
        self.y_min = -20
        self.y_max = 20
        self.point_count = 2500
        self.m_x = self.x_max
        self.m_y = self.y_min
        self.point_data = []
        self.point_data2 = []
        self.series = QLineSeries(self)
        self.series2 = QLineSeries(self)
        pen = QPen()
        pen.setWidth(1)
        self.series.setPen(pen)
        self.series2.setPen(pen)
        self.series.setColor(QColor(55, 171, 200))
        self.series2.setColor(QColor(255, 0, 0))
        self.axisX = QValueAxis()
        self.axisY = QValueAxis()
        Lfont = QFont('Alatsi')
        Lfont.setPixelSize(8)
        Lfont.setBold(False)
        self.axisX.setLabelsFont(Lfont)
        self.axisY.setLabelsFont(Lfont)
        self.axisX.setLabelsColor(QColor(255, 255, 255))
        self.axisY.setLabelsColor(QColor(255, 255, 255))
        self.axisX.setGridLineColor(QColor(51, 51, 51))
        self.axisY.setGridLineColor(QColor(51, 51, 51))
        self.series.append(self.m_x, self.m_y)
        self.series2.append(self.m_x, self.m_y * 2)
        self.axisX.setVisible(False)
        self.addSeries(self.series)
        self.addSeries(self.series2)
        self.addAxis(self.axisX, Qt.AlignBottom)
        self.addAxis(self.axisY, Qt.AlignLeft)
        self.series.attachAxis(self.axisX)
        self.series.attachAxis(self.axisY)
        self.series2.attachAxis(self.axisX)
        self.series2.attachAxis(self.axisY)
        self.axisX.setTickCount(self.point_count)
        self.axisX.setRange(self.x_min, self.x_max)
        self.axisY.setRange(self.y_min, self.y_max)
        self.timer = QTimer(self)
        self.timer.setInterval(5)
        self.timer.timeout.connect(self.handleTimeout)
        self.timer.start()
        self.main.chart_peak_torque_label.pressed.connect(lambda : self.main.chart_peak_torque_label.setText('0.0 Nm'))

    def __del__(self):
        self.chart_close = True

    def handleTimeout(self):
        x = self.plotArea().width() / self.axisX.tickCount()
        y = (self.axisX.max() - self.axisX.min()) / self.axisX.tickCount()
        self.m_x += y
        self.m_y = self.hidchooser.getTorque()
        point = QPointF(self.m_x, self.m_y)
        self.point_data.append(point)
        if len(self.point_data) > self.point_count:
            self.point_data.remove(self.point_data[0])
        self.series.replace(self.point_data)
        self.scroll(x, 0)
        angle = self.hidchooser.getCurrentAngle()
        angle_range = self.hidchooser.angle_range
        self.main.chart_angle_label.setText(str(angle) + u'\xb0')
        peak_torque_str = self.main.chart_peak_torque_label.text().replace(' Nm', '')
        if abs(self.hidchooser.getTorque()) > float(peak_torque_str):
            self.main.chart_peak_torque_label.setText(str(abs(self.hidchooser.getTorque())) + ' Nm')
        self.main.chart_current_torque_label.setText(str(abs(self.hidchooser.getTorque())) + ' Nm')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    chart = Dynamicine()
    chart.legend().hide()
    view = QChartView(chart)
    view.setRenderHint(QPainter.Antialiasing)
    view.show()
    sys.exit(app.exec_())