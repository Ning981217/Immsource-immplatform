# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.7.9 (tags/v3.7.9:13c94747c7, Aug 17 2020, 18:58:18) [MSC v.1900 64 bit (AMD64)]
# Embedded file name: axis_ui.py
# Compiled at: 1995-09-28 00:18:56
# Size of source mod 2**32: 257 bytes
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import QTimer
from PyQt5.QtSerialPort import QSerialPort, QSerialPortInfo
from PyQt5.QtCore import QIODevice, pyqtSignal
from PyQt5 import QtGui
from PyQt5.QtGui import QRegExpValidator
import time, main
from base_ui import WidgetUI
from uitl import Utiliy
from uitl import Refresher
from setting_define import *

class AxisChooser(Utiliy):

    def __init__(self, hidchooser, main):
        self.main = main
        self.hidchooser = hidchooser
        self.port_thread = Refresher(0.033)
        self.port_thread.sinOut.connect(self.updata6AxisADCValue)
        self.port_thread.start()

    def updata6AxisADCValue(self):
        if self.hidchooser.usbhidConnected() == CONNECT_STATUS_RUNNING:
            y = self.hidchooser.y
            z = self.hidchooser.z
            rx = self.hidchooser.rx
            ry = self.hidchooser.ry
            rz = self.hidchooser.rz
            slider = self.hidchooser.slider
            slider2 = self.hidchooser.slider2
            self.main.A1_progressBar.setValue(y)
            self.main.A2_progressBar.setValue(z)
            self.main.A3_progressBar.setValue(rx)
            self.main.A4_progressBar.setValue(ry)
            self.main.A5_progressBar.setValue(rz)
            self.main.A6_progressBar.setValue(slider)
            self.main.A7_progressBar.setValue(slider2)
# okay decompiling C:\Users\10439\Desktop\pyinstxtractor-2023.02\axis_ui.pyc
