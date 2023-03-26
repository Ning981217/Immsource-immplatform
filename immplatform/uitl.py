from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import QTimer
from PyQt5.QtSerialPort import QSerialPort, QSerialPortInfo
from PyQt5.QtCore import QIODevice, pyqtSignal
import time

class Utiliy:

    def __init__(self):
        pass

    def updataSlider(self, value_object, slider_object):
        new_value = int(value_object.value())
        new_value = slider_object.maximum() if new_value > slider_object.maximum() else new_value
        new_value = slider_object.minimum() if new_value < slider_object.minimum() else new_value
        slider_object.setValue(new_value)

    def updataSliderAngle(self, value_object, slider_object, f):
        if f == 1:
            new_value = int(value_object.value())
        else:
            if f >= 2:
                new_value = float(value_object.value())
        new_value = slider_object.maximum() if new_value * f > slider_object.maximum() else new_value
        new_value = slider_object.minimum() if new_value * f < slider_object.minimum() else new_value
        slider_object.setValue(int(new_value * f))


class Refresher(QThread):
    sinOut = pyqtSignal(str)

    def __init__(self, t, parent=None):
        super(Refresher, self).__init__(parent)
        self.working = True
        self.t = t

    def __del__(self):
        self.working = False
        self.wait()

    def stop(self):
        self.working = False

    def pcontinue(self):
        self.working = True

    def run(self):
        while self.working == True:
            self.sinOut.emit('')
            time.sleep(self.t)

    def setTime(self, t):
        self.t = t
