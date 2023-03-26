from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5 import QtCore
from PyQt5.QtCore import QTimer
from PyQt5.QtSerialPort import QSerialPort, QSerialPortInfo
from PyQt5.QtCore import QIODevice, pyqtSignal
from PyQt5.QtGui import QTransform, QPixmap
import time, main
from base_ui import WidgetUI
from setting_ui import SettingChooser
from setting_define import *
from uitl import Utiliy
from uitl import Refresher

class SteeringChooser(Utiliy):

    def __init__(self, hidchooser, main, language_chooser):
        self.main = main
        self.hidchooser = hidchooser
        self.language_chooser = language_chooser
        self.angle_deg = 0
        self.buttons = []
        for i in range(1, 129):
            exec('self.buttons.append(self.main.base_b_' + str(i) + ')')

        for b in self.buttons:
            b.setAttribute(Qt.WA_TransparentForMouseEvents, True)

        self.setConnect()
        self.main.base_angle_Slider.setAttribute(Qt.WA_TransparentForMouseEvents, True)
        self.high_freq_thread = Refresher(0.01)
        self.high_freq_thread.sinOut.connect(self.highFreqUpdata)
        self.high_freq_thread.start()
        self.low_freq_thread = Refresher(2)
        self.low_freq_thread.sinOut.connect(self.lowFreqUpdata)
        self.low_freq_thread.start()

    def setConnect(self):
        self.main.range_auto_radioButton.toggled.connect(lambda val: self.main.range_auto_radioButton2.setChecked(val))
        self.main.range_auto_radioButton2.toggled.connect(lambda val: self.main.range_auto_radioButton.setChecked(val))
        self.main.base_angle_range_Slider.valueChanged.connect(lambda val: self.main.base_angle_range_Slider2.setValue(val))
        self.main.base_angle_range_Slider2.valueChanged.connect(lambda val: self.main.base_angle_range_Slider.setValue(val))
        self.main.base_angle_range_Slider2.valueChanged.connect(lambda : self.main.base_angle_range_Value2.setText(str(self.main.base_angle_range_Slider2.value()) + '°'))
        self.main.base_angle_range_Slider.valueChanged.connect(lambda : self.main.base_angle_range_Value.setText(str(self.main.base_angle_range_Slider.value()) + '°'))
        self.main.base_angle_range_Slider.valueChanged.connect(self.changeAngleSelectStatus)
        self.main.base_test_torque_Slider.valueChanged.connect(lambda : self.main.base_test_torque_Value.setText(str(self.main.base_test_torque_Slider.value())))
        self.main.range_180_radioButton.pressed.connect(lambda : self.main.base_angle_range_Slider.setValue(180))
        self.main.range_360_radioButton.pressed.connect(lambda : self.main.base_angle_range_Slider.setValue(360))
        self.main.range_540_radioButton.pressed.connect(lambda : self.main.base_angle_range_Slider.setValue(540))
        self.main.range_720_radioButton.pressed.connect(lambda : self.main.base_angle_range_Slider.setValue(720))
        self.main.range_900_radioButton.pressed.connect(lambda : self.main.base_angle_range_Slider.setValue(900))
        self.main.range_1080_radioButton.pressed.connect(lambda : self.main.base_angle_range_Slider.setValue(1080))
        self.main.range_180_radioButton.pressed.connect(lambda : self.hidchooser.sent_handler(SETTING_SET_RANGE, 180))
        self.main.range_360_radioButton.pressed.connect(lambda : self.hidchooser.sent_handler(SETTING_SET_RANGE, 360))
        self.main.range_540_radioButton.pressed.connect(lambda : self.hidchooser.sent_handler(SETTING_SET_RANGE, 540))
        self.main.range_720_radioButton.pressed.connect(lambda : self.hidchooser.sent_handler(SETTING_SET_RANGE, 720))
        self.main.range_900_radioButton.pressed.connect(lambda : self.hidchooser.sent_handler(SETTING_SET_RANGE, 900))
        self.main.range_1080_radioButton.pressed.connect(lambda : self.hidchooser.sent_handler(SETTING_SET_RANGE, 1080))
        self.main.range_180_radioButton.pressed.connect(lambda : self.hidchooser.sent_handler(SETTING_SYNA_LOCK, 1))
        self.main.range_360_radioButton.pressed.connect(lambda : self.hidchooser.sent_handler(SETTING_SYNA_LOCK, 1))
        self.main.range_540_radioButton.pressed.connect(lambda : self.hidchooser.sent_handler(SETTING_SYNA_LOCK, 1))
        self.main.range_720_radioButton.pressed.connect(lambda : self.hidchooser.sent_handler(SETTING_SYNA_LOCK, 1))
        self.main.range_900_radioButton.pressed.connect(lambda : self.hidchooser.sent_handler(SETTING_SYNA_LOCK, 1))
        self.main.range_1080_radioButton.pressed.connect(lambda : self.hidchooser.sent_handler(SETTING_SYNA_LOCK, 1))
        self.main.range_auto_radioButton.toggled.connect(self.changeRangeAuto)
        self.main.base_test_torque_Slider.valueChanged.connect(lambda val: self.hidchooser.sent_handler(SETTING_TEST_TORQUE, val))
        self.main.base_center_pushButton_2.clicked.connect(lambda : self.hidchooser.sent_handler(SETTING_ZORE_CENTER))
        self.main.base_angle_range_Slider.valueChanged.connect(lambda val: self.hidchooser.sent_handler(SETTING_SET_RANGE, val))
        self.main.base_angle_range_Slider.valueChanged.connect(lambda val: self.hidchooser.sent_handler(SETTING_SYNA_LOCK, 1))
        self.main.A1_min.clicked.connect(lambda val: self.hidchooser.sent_handler(SETTING_A1_MIN))
        self.main.A1_max.clicked.connect(lambda val: self.hidchooser.sent_handler(SETTING_A1_MAX))
        self.main.A2_min.clicked.connect(lambda val: self.hidchooser.sent_handler(SETTING_A2_MIN))
        self.main.A2_max.clicked.connect(lambda val: self.hidchooser.sent_handler(SETTING_A2_MAX))
        self.main.A3_min.clicked.connect(lambda val: self.hidchooser.sent_handler(SETTING_A3_MIN))
        self.main.A3_max.clicked.connect(lambda val: self.hidchooser.sent_handler(SETTING_A3_MAX))
        self.main.A4_min.clicked.connect(lambda val: self.hidchooser.sent_handler(SETTING_A4_MIN))
        self.main.A4_max.clicked.connect(lambda val: self.hidchooser.sent_handler(SETTING_A4_MAX))
        self.main.A5_min.clicked.connect(lambda val: self.hidchooser.sent_handler(SETTING_A5_MIN))
        self.main.A5_max.clicked.connect(lambda val: self.hidchooser.sent_handler(SETTING_A5_MAX))
        self.main.A6_min.clicked.connect(lambda val: self.hidchooser.sent_handler(SETTING_A6_MIN))
        self.main.A6_max.clicked.connect(lambda val: self.hidchooser.sent_handler(SETTING_A6_MAX))
        self.main.A7_min.clicked.connect(lambda val: self.hidchooser.sent_handler(SETTING_A7_MIN))
        self.main.A7_max.clicked.connect(lambda val: self.hidchooser.sent_handler(SETTING_A7_MAX))
        self.main.A1_reset.clicked.connect(lambda val: self.hidchooser.sent_handler(SETTING_A1_RESET))
        self.main.A2_reset.clicked.connect(lambda val: self.hidchooser.sent_handler(SETTING_A2_RESET))
        self.main.A3_reset.clicked.connect(lambda val: self.hidchooser.sent_handler(SETTING_A3_RESET))
        self.main.A4_reset.clicked.connect(lambda val: self.hidchooser.sent_handler(SETTING_A4_RESET))
        self.main.A5_reset.clicked.connect(lambda val: self.hidchooser.sent_handler(SETTING_A5_RESET))
        self.main.A6_reset.clicked.connect(lambda val: self.hidchooser.sent_handler(SETTING_A6_RESET))
        self.main.A7_reset.clicked.connect(lambda val: self.hidchooser.sent_handler(SETTING_A7_RESET))
        self.changeRangeAuto()

    def modeSelectChange(self, mode):
        self.main.base_multi_platform_label.setText('')
        if mode == 'PC':
            if self.hidchooser.mode != MODE_PC:
                self.main.base_mode_pushButton.setEnabled(True)
            else:
                if self.language_chooser.language == 'zh-cn':
                    self.main.base_multi_platform_label.setText('已经是PC模式')
                else:
                    self.main.base_multi_platform_label.setText('Currently in PC mode')
        else:
            if mode == 'PlayStation 3':
                self.main.base_mode_pushButton.setEnabled(False)
            else:
                if mode == 'PlayStation 4':
                    if self.hidchooser.mode != MODE_PS4:
                        ds4_connected = False
                        for i in range(6):
                            label = eval('self.main.device_' + str(i + 1) + '_label')
                            if label.text() == 'DualShock 4':
                                self.main.base_mode_pushButton.setEnabled(True)
                                ds4_connected = True

                        if ds4_connected == False:
                            if self.language_chooser.language == 'zh-cn':
                                self.main.base_multi_platform_label.setText('没有检测到 DualShock 4')
                            else:
                                self.main.base_multi_platform_label.setText('DualShock 4 not detected')
                    else:
                        if self.language_chooser.language == 'zh-cn':
                            self.main.base_multi_platform_label.setText('已经是PS4模式')
                        else:
                            self.main.base_multi_platform_label.setText('Currently in PS4 mode')
                elif mode == 'Xbox':
                    self.main.base_mode_pushButton.setEnabled(False)

    def changeMode(self):
        mode = self.main.mode_comboBox.currentText()
        if mode == 'PC':
            self.hidchooser.sent_handler(SETTING_MODE, MODE_PC)
        elif mode == 'PlayStation 4':
            self.hidchooser.sent_handler(SETTING_MODE, MODE_PS4)

    def changeAngleSelectStatus(self):
        if self.main.base_angle_range_Slider.value() != 180:
            self.main.range_180_radioButton.group().setExclusive(False)
            self.main.range_180_radioButton.setChecked(False)
            self.main.range_180_radioButton.group().setExclusive(True)
        else:
            self.main.range_180_radioButton.setChecked(True)
        if self.main.base_angle_range_Slider.value() != 360:
            self.main.range_360_radioButton.group().setExclusive(False)
            self.main.range_360_radioButton.setChecked(False)
            self.main.range_360_radioButton.group().setExclusive(True)
        else:
            self.main.range_360_radioButton.setChecked(True)
        if self.main.base_angle_range_Slider.value() != 540:
            self.main.range_540_radioButton.group().setExclusive(False)
            self.main.range_540_radioButton.setChecked(False)
            self.main.range_540_radioButton.group().setExclusive(True)
        else:
            self.main.range_540_radioButton.setChecked(True)
        if self.main.base_angle_range_Slider.value() != 720:
            self.main.range_720_radioButton.group().setExclusive(False)
            self.main.range_720_radioButton.setChecked(False)
            self.main.range_720_radioButton.group().setExclusive(True)
        else:
            self.main.range_720_radioButton.setChecked(True)
        if self.main.base_angle_range_Slider.value() != 900:
            self.main.range_900_radioButton.group().setExclusive(False)
            self.main.range_900_radioButton.setChecked(False)
            self.main.range_900_radioButton.group().setExclusive(True)
        else:
            self.main.range_900_radioButton.setChecked(True)
        if self.main.base_angle_range_Slider.value() != 1080:
            self.main.range_1080_radioButton.group().setExclusive(False)
            self.main.range_1080_radioButton.setChecked(False)
            self.main.range_1080_radioButton.group().setExclusive(True)
        else:
            self.main.range_1080_radioButton.setChecked(True)

    def changeRangeAuto(self):
        if self.main.range_auto_radioButton.isChecked():
            self.main.base_angle_range_Slider.setEnabled(False)
            self.main.base_angle_range_Value.setEnabled(False)
            self.main.base_angle_range_Slider2.setEnabled(False)
            self.main.base_angle_range_Value2.setEnabled(False)
            self.main.range_180_radioButton.setEnabled(False)
            self.main.range_360_radioButton.setEnabled(False)
            self.main.range_540_radioButton.setEnabled(False)
            self.main.range_720_radioButton.setEnabled(False)
            self.main.range_900_radioButton.setEnabled(False)
            self.main.range_1080_radioButton.setEnabled(False)
            self.main.hidchooser.sent_handler(SETTING_SYNA_LOCK, self.main.base_angle_range_Slider.value())
            self.main.hidchooser.sent_handler(SETTING_RANGE_AUTO, 1)
        else:
            self.main.hidchooser.sent_handler(SETTING_SYNA_LOCK, 1)
        if self.angle_deg <= 20:
            self.main.base_angle_range_Slider.setEnabled(True)
            self.main.base_angle_range_Value.setEnabled(True)
            self.main.base_angle_range_Slider2.setEnabled(True)
            self.main.base_angle_range_Value2.setEnabled(True)
            self.main.range_180_radioButton.setEnabled(True)
            self.main.range_360_radioButton.setEnabled(True)
            self.main.range_540_radioButton.setEnabled(True)
            self.main.range_720_radioButton.setEnabled(True)
            self.main.range_900_radioButton.setEnabled(True)
            self.main.range_1080_radioButton.setEnabled(True)
            self.main.hidchooser.sent_handler(SETTING_RANGE_AUTO, 0)

    def lowFreqUpdata(self):
        if self.hidchooser.usbhidDataReady():
            device_id = {-1: 'Not Supported', 0: 'None', 1: 'DualShock 4', 10: 'HE PRO GRS3', 11: 'HPD SC V1', 12: 'F PEDALS V2', 13: 'F PEDALS V3', 14: 'F SHIFTER SQ', 15: 'AZ PEDALS', 
             16: 'TLCM PEDALS', 17: 'SIMJACK PEDALS', 18: 'CPP PEDALS'}
            for i in range(6):
                id = eval('self.hidchooser.hub' + str(i + 1))
                try:
                    device = device_id[id]
                except:
                    device = device_id[(-1)]

                self.hidchooser.usbHubStatusChange.emit(device, i + 1)

            if self.hidchooser.cmd_sending == False:
                angle_range = self.hidchooser.angle_range
                if angle_range == 180:
                    self.main.range_180_radioButton.setChecked(True)
                if angle_range == 360:
                    self.main.range_360_radioButton.setChecked(True)
                if angle_range == 540:
                    self.main.range_540_radioButton.setChecked(True)
                if angle_range == 720:
                    self.main.range_720_radioButton.setChecked(True)
                if angle_range == 900:
                    self.main.range_900_radioButton.setChecked(True)
                if angle_range == 1080:
                    self.main.range_1080_radioButton.setChecked(True)
                dead_zone = self.hidchooser.dead_band
                angle_range_auto = self.hidchooser.angle_range_auto
                self.main.range_auto_radioButton.setChecked(angle_range_auto)

    def highFreqUpdata(self):
        if self.hidchooser.usbhidDataReady():
            pos = self.hidchooser.x
            angle_range = self.hidchooser.angle_range
            per = angle_range / 65536
            angle_deg = per * pos
            self.angle_deg = round(angle_deg, 1)
            if self.angle_deg == -0.0:
                self.angle_deg = 0.0
            if self.main.range_auto_radioButton.isChecked() == False:
                if abs(angle_deg) <= 20:
                    self.main.base_angle_range_Slider.setEnabled(True)
                    self.main.base_angle_range_Value.setEnabled(True)
                    self.main.base_angle_range_Value.setEnabled(True)
                    self.main.range_180_radioButton.setEnabled(True)
                    self.main.range_360_radioButton.setEnabled(True)
                    self.main.range_540_radioButton.setEnabled(True)
                    self.main.range_720_radioButton.setEnabled(True)
                    self.main.range_900_radioButton.setEnabled(True)
                    self.main.range_1080_radioButton.setEnabled(True)
                else:
                    self.main.base_angle_range_Slider.setEnabled(False)
                    self.main.base_angle_range_Value.setEnabled(False)
                    self.main.base_angle_range_Value.setEnabled(False)
                    self.main.range_180_radioButton.setEnabled(False)
                    self.main.range_360_radioButton.setEnabled(False)
                    self.main.range_540_radioButton.setEnabled(False)
                    self.main.range_720_radioButton.setEnabled(False)
                    self.main.range_900_radioButton.setEnabled(False)
                    self.main.range_1080_radioButton.setEnabled(False)
            self.main.base_angle_Slider.setValue(pos)
            self.main.base_angle_value.setText(str(self.angle_deg))
            voltage = int(self.hidchooser.getSystemVoltage() + 0.5)
            self.main.system_voltage_Label.setText(str(voltage) + ' V')
            b = self.hidchooser.buttons + (self.hidchooser.buttons2 << 64)
            for i in range(128):
                self.buttons[i].setChecked(False)

            for i in range(128):
                if b >> i & 1 == 1:
                    self.buttons[i].setChecked(True)

        else:
            self.main.base_angle_Slider.setValue(0)
            self.main.base_angle_value.setText('-')
            for i in range(64):
                self.buttons[i].setChecked(False)
