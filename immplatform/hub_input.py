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
import ctypes, time
from PyQt5 import uic
from helper import res_path
from setting_define import *
SendInput = ctypes.windll.user32.SendInput
PUL = ctypes.POINTER(ctypes.c_ulong)

class KeyBdInput(ctypes.Structure):
    _fields_ = [
     (
      'wVk', ctypes.c_ushort),
     (
      'wScan', ctypes.c_ushort),
     (
      'dwFlags', ctypes.c_ulong),
     (
      'time', ctypes.c_ulong),
     (
      'dwExtraInfo', PUL)]


class HardwareInput(ctypes.Structure):
    _fields_ = [
     (
      'uMsg', ctypes.c_ulong),
     (
      'wParamL', ctypes.c_short),
     (
      'wParamH', ctypes.c_ushort)]


class MouseInput(ctypes.Structure):
    _fields_ = [
     (
      'dx', ctypes.c_long),
     (
      'dy', ctypes.c_long),
     (
      'mouseData', ctypes.c_ulong),
     (
      'dwFlags', ctypes.c_ulong),
     (
      'time', ctypes.c_ulong),
     (
      'dwExtraInfo', PUL)]


class Input_I(ctypes.Union):
    _fields_ = [
     (
      'ki', KeyBdInput),
     (
      'mi', MouseInput),
     (
      'hi', HardwareInput)]


class Input(ctypes.Structure):
    _fields_ = [
     (
      'type', ctypes.c_ulong),
     (
      'ii', Input_I)]


def PressKey(hexKeyCode):
    extra = ctypes.c_ulong(0)
    ii_ = Input_I()
    ii_.ki = KeyBdInput(0, hexKeyCode, 8, 0, ctypes.pointer(extra))
    x = Input(ctypes.c_ulong(1), ii_)
    ctypes.windll.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))


def ReleaseKey(hexKeyCode):
    extra = ctypes.c_ulong(0)
    ii_ = Input_I()
    ii_.ki = KeyBdInput(0, hexKeyCode, 10, 0, ctypes.pointer(extra))
    x = Input(ctypes.c_ulong(1), ii_)
    ctypes.windll.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))


class CalibrateDialog(QDialog):

    def __init__(self, hub_hidchooser):
        QDialog.__init__(self)
        self.setWindowFlags(QtCore.Qt.WindowCloseButtonHint)
        uic.loadUi(res_path('calibrate.ui'), self)
        self.hidchooser = hub_hidchooser
        self.num = 220.0
        self.port_thread = Refresher(0.05)
        self.port_thread.sinOut.connect(self.calibrate)
        self.port_thread.start()
        self.x_min = 65535
        self.y_min = 65535
        self.x_max = 0
        self.y_max = 0
        self.hidchooser.sent_handler(SETTING_START_JOY_CALIBRATE, 0)

    def calibrate(self):
        self.num = self.num - 1
        sec = int(self.num / 20.0)
        if sec == 0:
            self.port_thread.stop()
            self.hidchooser.sent_handler(SETTING_JOY_CALIBRATE_X_MIN, self.x_min + 2000)
            self.hidchooser.sent_handler(SETTING_JOY_CALIBRATE_X_MAX, self.x_max - 2000)
            self.hidchooser.sent_handler(SETTING_JOY_CALIBRATE_Y_MIN, self.y_min + 2000)
            self.hidchooser.sent_handler(SETTING_JOY_CALIBRATE_Y_MAX, self.y_max - 2000)
            self.hidchooser.sent_handler(SETTING_JOY_CALIBRATE_FINISH, 0)
            self.num_label.setText('Calibration is complete.')
            return
        self.num_label.setText(str(sec))
        x = self.hidchooser.getX() + 32767
        y = self.hidchooser.getY() + 32767
        if self.x_min > x:
            self.x_min = x
        if self.y_min > y:
            self.y_min = y
        if self.x_max < x:
            self.x_max = x
        if self.y_max < y:
            self.y_max = y
        self.x_min_label.setText(str(self.x_min))
        self.y_min_label.setText(str(self.y_min))
        self.x_max_label.setText(str(self.x_max))
        self.y_max_label.setText(str(self.y_max))


class CalibratePaddleDialog(QDialog):

    def __init__(self, hub_hidchooser):
        QDialog.__init__(self)
        self.setWindowFlags(QtCore.Qt.WindowCloseButtonHint)
        uic.loadUi(res_path('calibrate2.ui'), self)
        self.hidchooser = hub_hidchooser
        self.num = 220.0
        self.port_thread = Refresher(0.05)
        self.port_thread.sinOut.connect(self.calibrate)
        self.port_thread.start()
        self.left_clutch_min = 65535
        self.right_clutch_min = 65535
        self.left_clutch_max = 0
        self.right_clutch_max = 0
        self.hidchooser.sent_handler(SETTING_START_PADDLE_CALIBRATE, 0)

    def calibrate(self):
        self.num = self.num - 1
        sec = int(self.num / 20.0)
        if sec == 0:
            self.port_thread.stop()
            self.hidchooser.sent_handler(SETTING_CLUTACH_CALIBRATE_X_MIN, self.left_clutch_min + 2000)
            self.hidchooser.sent_handler(SETTING_CLUTACH_CALIBRATE_X_MAX, self.left_clutch_max - 2000)
            self.hidchooser.sent_handler(SETTING_CLUTACH_CALIBRATE_Y_MIN, self.right_clutch_min + 2000)
            self.hidchooser.sent_handler(SETTING_CLUTACH_CALIBRATE_Y_MAX, self.right_clutch_max - 2000)
            self.hidchooser.sent_handler(SETTING_PADDLE_CALIBRATE_FINISH, 0)
            self.num_label.setText('Calibration is complete.')
            return
        self.num_label.setText(str(sec))
        x = -(self.hidchooser.getZ() - 32767)
        y = -(self.hidchooser.getRx() - 32767)
        if self.left_clutch_min > x:
            self.left_clutch_min = x
        if self.right_clutch_min > y:
            self.right_clutch_min = y
        if self.left_clutch_max < x:
            self.left_clutch_max = x
        if self.right_clutch_max < y:
            self.right_clutch_max = y
        self.x_min_label.setText(str(self.left_clutch_min))
        self.y_min_label.setText(str(self.right_clutch_min))
        self.x_max_label.setText(str(self.left_clutch_max))
        self.y_max_label.setText(str(self.right_clutch_max))


class HubInputChooser(Utiliy):

    def __init__(self, hidchooser, base_hidchooser, main):
        self.main = main
        self.hidchooser = hidchooser
        self.base_hidchooser = base_hidchooser
        self.buttons = []
        for i in range(1, 65):
            exec('self.buttons.append(self.main.k' + str(i) + '_pushButton)')

        for b in self.buttons:
            b.setAttribute(Qt.WA_TransparentForMouseEvents, True)

        self.main.left_enc_sub_pushButton.setAttribute(Qt.WA_TransparentForMouseEvents, True)
        self.main.left_enc_add_pushButton.setAttribute(Qt.WA_TransparentForMouseEvents, True)
        self.main.right_enc_sub_pushButton.setAttribute(Qt.WA_TransparentForMouseEvents, True)
        self.main.right_enc_add_pushButton.setAttribute(Qt.WA_TransparentForMouseEvents, True)
        self.main.hub_left_encoder_dia.setAttribute(Qt.WA_TransparentForMouseEvents, True)
        self.main.hub_right_encoder_dia.setAttribute(Qt.WA_TransparentForMouseEvents, True)
        self.setConnect()
        self.last_dir4_enc_left_flag = False
        self.last_dir4_enc_right_flag = False
        self.last_left_enc_left_flag = False
        self.last_left_enc_right_flag = False
        self.last_right_enc_left_flag = False
        self.last_right_enc_right_flag = False
        self.last_left_rot_sw_mode = 0
        self.last_right_rot_sw_mode = 0
        self.last_clutch_mode = 0
        self.last_joy_mode = 0
        self.port_thread = Refresher(0.01)
        self.port_thread.sinOut.connect(self.updataValue)
        self.port_thread.start()
        self.read_setting_thread = Refresher(1)
        self.read_setting_thread.sinOut.connect(self.readSetting)
        self.read_setting_thread.start()

    def setConnect(self):
        self.main.left_bandswitch_radioButton.clicked.connect(lambda val: self.hubSentHandler(SETTING_LEFT_ROTARY_SW_MODE, 1, True))
        self.main.left_encoder_radioButton.clicked.connect(lambda val: self.hubSentHandler(SETTING_LEFT_ROTARY_SW_MODE, 2, True))
        self.main.left_mult_encoder_radioButton.clicked.connect(lambda val: self.hubSentHandler(SETTING_LEFT_ROTARY_SW_MODE, 3, True))
        self.main.right_bandswitch_radioButton.clicked.connect(lambda val: self.hubSentHandler(SETTING_RIGHT_ROTARY_SW_MODE, 1, True))
        self.main.right_encoder_radioButton.clicked.connect(lambda val: self.hubSentHandler(SETTING_RIGHT_ROTARY_SW_MODE, 2, True))
        self.main.right_mult_encoder_radioButton.clicked.connect(lambda val: self.hubSentHandler(SETTING_RIGHT_ROTARY_SW_MODE, 3, True))
        self.main.clutch_axis_mode_radioButton.clicked.connect(lambda val: self.hubSentHandler(SETTING_CLUTCH_MODE, 1, True))
        self.main.clutch_button_mode_radioButton.clicked.connect(lambda val: self.hubSentHandler(SETTING_CLUTCH_MODE, 2, True))
        self.main.clutch_point_mode_radioButton.clicked.connect(lambda val: self.hubSentHandler(SETTING_CLUTCH_MODE, 3, True))
        self.main.joy_axis_mode_radioButton.clicked.connect(lambda val: self.hubSentHandler(SETTING_JOY_MODE, 1, True))
        self.main.joy_button_mode_radioButton.clicked.connect(lambda val: self.hubSentHandler(SETTING_JOY_MODE, 2, True))
        self.slider_conn = self.main.hub_clutch_point_Slider.valueChanged.connect(lambda val: self.hubSentHandler(SETTING_SET_CLUTCH_POINT, val, True))
        self.main.paddle_calibrate_pushButton.clicked.connect(lambda val: self.hubSentHandler(SETTING_HUB_PADDLE_CALIBRATE, True))
        self.main.joy_calibrate_pushButton.clicked.connect(lambda val: self.hubSentHandler(SETTING_HUB_JOY_CALIBRATE, True))
        self.main.enc_zero_pushButton.clicked.connect(lambda val: self.hubSentHandler(SETTING_HUB_ENC_ZERO, True))

    def hubSentHandler(self, cmd, val=0, for_wireless=False):
        self.hidchooser.sent_handler(cmd, val)
        if for_wireless == True:
            self.base_hidchooser.sent_handler(cmd, val, for_wireless)
        self.base_hidchooser.sent_handler(cmd, val, for_wireless)

    def openCalibrateJoy(self):
        child_win = CalibrateDialog(self.hidchooser)
        child_win.exec_()

    def openCalibratePaddle(self):
        child_win = CalibratePaddleDialog(self.hidchooser)
        child_win.exec_()

    def setPushButtonStatus(self, id, qbutton):
        button = self.hidchooser.buttons
        print(bin(button))
        if button >> id & 1 == 1:
            qbutton.setDown(True)
        else:
            qbutton.setDown(False)

    def ParaButton(self):
        pass

    def updataValue(self):
        x = y = z = rx = ry = rz = slider = slider2 = left_clutch = right_clutch = clutch_point = -32767
        left_x = left_y = 0
        if self.hidchooser.usbhidConnected() == CONNECT_STATUS_WIRELESS_RUNNING:
            x = self.hidchooser.x
            y = self.hidchooser.y
            clutch_point = self.hidchooser.z
            rx = self.hidchooser.rx
            left_clutch = self.hidchooser.ry
            right_clutch = self.hidchooser.rz
            left_x = self.hidchooser.slider
            slider2 = self.hidchooser.slider2
        else:
            if self.hidchooser.usbhidConnected() == CONNECT_STATUS_RUNNING:
                left_x = self.hidchooser.x
                left_y = self.hidchooser.y
                right_clutch = self.hidchooser.z
                left_clutch = self.hidchooser.rx
                clutch_point = self.hidchooser.ry
                rz = self.hidchooser.rz
                slider = self.hidchooser.slider
                slider2 = self.hidchooser.slider2
            if self.main.clutch_axis_mode_radioButton.isChecked():
                self.main.hub_left_clutch_progressBar.setValue(left_clutch)
                self.main.hub_right_clutch_progressBar.setValue(right_clutch)
            elif self.main.clutch_point_mode_radioButton.isChecked():
                self.main.hub_clutch_point_progressBar.setValue(clutch_point)
                self.main.hub_clutch_point_progressBar.setFormat(str(int((clutch_point + 32767) / 65.535 + 0.5)))
        if self.main.joy_axis_mode_radioButton.isChecked():
            if self.hidchooser.isWireless:
                y = 55
            else:
                y = left_y / 32767 * 40 + 55
            x = left_x / 32767 * 40 + 55
            self.main.hub_joy_x_label.setText('X : ' + str(int(left_x / 32767 * 50)))
            if self.hidchooser.isWireless:
                self.main.hub_joy_y_label.setText('Y : Invalid')
            else:
                self.main.hub_joy_y_label.setText('Y : ' + str(int(-left_y / 32767 * 50)))
            self.main.joy.setPos(x, y)
        else:
            if self.main.joy_button_mode_radioButton.isChecked():
                self.main.joy.setPos(55, 55)
                self.main.hub_joy_x_label.setText('X : 0')
                self.main.hub_joy_y_label.setText('Y : 0')
            else:
                b = self.hidchooser.buttons
                for i in range(64):
                    self.buttons[i].setDown(False)

                self.main.dir_up_pushButton.setDown(False)
                self.main.dir_down_pushButton.setDown(False)
                self.main.dir_left_pushButton.setDown(False)
                self.main.dir_right_pushButton.setDown(False)
                self.main.dir_push_pushButton.setDown(False)
                self.main.dir_sub_pushButton.setDown(False)
                self.main.dir_add_pushButton.setDown(False)
                self.main.right_enc_sub_pushButton.setDown(False)
                self.main.right_enc_add_pushButton.setDown(False)
                self.main.left_enc_sub_pushButton.setDown(False)
                self.main.left_enc_add_pushButton.setDown(False)
                l_gear = 0
                r_gear = 0
                l_clutch = 0
                r_clutch = 0
                for i in range(64):
                    if b >> i & 1 == 1:
                        self.buttons[i].setDown(True)
                        if i == DIR_UP_ID:
                            self.main.dir_up_pushButton.setDown(True)
                        else:
                            if i == DIR_DOWN_ID:
                                self.main.dir_down_pushButton.setDown(True)
                            else:
                                if i == DIR_LEFT_ID:
                                    self.main.dir_left_pushButton.setDown(True)
                                else:
                                    if i == DIR_RIGHT_ID:
                                        self.main.dir_right_pushButton.setDown(True)
                                    else:
                                        if i == DIR_PUSH_ID:
                                            self.main.dir_push_pushButton.setDown(True)
                                if i == DIR_ENC_LEFT_ID:
                                    self.main.dir_sub_pushButton.setDown(True)
                                elif i == DIR_ENC_RIGHT_ID:
                                    self.main.dir_add_pushButton.setDown(True)
                        if i == L_ENC_RIGHT_ID:
                            self.main.left_enc_sub_pushButton.setDown(True)
                        else:
                            if i == L_ENC_LEFT_ID:
                                self.main.left_enc_add_pushButton.setDown(True)
                            if i == R_ENC_RIGHT_ID:
                                self.main.right_enc_sub_pushButton.setDown(True)
                            elif i == R_ENC_LEFT_ID:
                                self.main.right_enc_add_pushButton.setDown(True)
                        if self.main.joy_button_mode_radioButton.isChecked():
                            if i == JOY_DOWN_ID:
                                x = 110
                                y = 55
                                self.main.hub_joy_x_label.setText('X : 1')
                                self.main.hub_joy_y_label.setText('Y : 0')
                                self.main.joy.setPos(x, y)
                            else:
                                if i == JOY_UP_ID:
                                    x = 0
                                    y = 55
                                    self.main.hub_joy_x_label.setText('X : -1')
                                    self.main.hub_joy_y_label.setText('Y : 0')
                                    self.main.joy.setPos(x, y)
                                if i == JOY_RIGHT_ID:
                                    x = 55
                                    y = 110
                                    self.main.hub_joy_x_label.setText('X : 0')
                                    self.main.hub_joy_y_label.setText('Y : -1')
                                    self.main.joy.setPos(x, y)
                                elif i == JOY_LEFT_ID:
                                    x = 55
                                    y = 0
                                    self.main.hub_joy_x_label.setText('X : 0')
                                    self.main.hub_joy_y_label.setText('Y : 1')
                                    self.main.joy.setPos(x, y)
                        if i == L_GEAR_ID:
                            l_gear = 1
                        if i == R_GEAR_ID:
                            r_gear = 1
                        if i == R_CLATCH_ID:
                            l_clutch = 1
                        if i == L_CLATCH_ID:
                            r_clutch = 1

                if l_gear == 1:
                    self.main.hub_left_gear_progressBar.setValue(32767)
                else:
                    self.main.hub_left_gear_progressBar.setValue(-32767)
            if r_gear == 1:
                self.main.hub_right_gear_progressBar.setValue(32767)
            else:
                self.main.hub_right_gear_progressBar.setValue(-32767)
        if self.main.clutch_button_mode_radioButton.isChecked():
            if l_clutch == 1:
                self.main.hub_left_clutch_progressBar.setValue(32767)
            else:
                self.main.hub_left_clutch_progressBar.setValue(-32767)
            if r_clutch == 1:
                self.main.hub_right_clutch_progressBar.setValue(32767)
            else:
                self.main.hub_right_clutch_progressBar.setValue(-32767)
        self.main.hub_left_encoder_dia.setValue(12 - self.hidchooser.left_enc + 1)
        self.main.hub_right_encoder_dia.setValue(12 - self.hidchooser.right_enc + 1)

    def readSetting(self):
        if self.hidchooser.usbhidConnected() == CONNECT_STATUS_RUNNING or self.hidchooser.usbhidConnected() == CONNECT_STATUS_WIRELESS_RUNNING:
            if self.hidchooser.cmd_sending == False and self.base_hidchooser.cmd_sending == False:
                left_rot_sw_mode = self.hidchooser.left_rot_sw_mode
                right_rot_sw_mode = self.hidchooser.right_rot_sw_mode
                clutch_mode = self.hidchooser.clutch_mode
                joy_mode = self.hidchooser.joy_mode
                clutch_point = self.hidchooser.clutch_point
                if clutch_point != self.main.hub_clutch_point_Slider.value():
                    pass
                if self.last_left_rot_sw_mode != left_rot_sw_mode:
                    if left_rot_sw_mode == 1:
                        self.main.left_bandswitch_radioButton.setChecked(True)
                    else:
                        if left_rot_sw_mode == 2:
                            self.main.left_encoder_radioButton.setChecked(True)
                        elif left_rot_sw_mode == 3:
                            self.main.left_mult_encoder_radioButton.setChecked(True)
                if self.last_right_rot_sw_mode != right_rot_sw_mode:
                    if right_rot_sw_mode == 1:
                        self.main.right_bandswitch_radioButton.setChecked(True)
                    else:
                        if right_rot_sw_mode == 2:
                            self.main.right_encoder_radioButton.setChecked(True)
                        elif right_rot_sw_mode == 3:
                            self.main.right_mult_encoder_radioButton.setChecked(True)
                if self.last_clutch_mode != clutch_mode:
                    if clutch_mode == 1:
                        self.main.clutch_axis_mode_radioButton.setChecked(True)
                        self.main.clutchModeChange(0)
                    else:
                        if clutch_mode == 2:
                            self.main.clutch_button_mode_radioButton.setChecked(True)
                            self.main.clutchModeChange(0)
                        elif clutch_mode == 3:
                            self.main.clutch_point_mode_radioButton.setChecked(True)
                            self.main.clutchModeChange(1)
                if self.last_joy_mode != joy_mode:
                    if joy_mode == 1:
                        self.main.joy_axis_mode_radioButton.setChecked(True)
                    elif joy_mode == 2:
                        self.main.joy_button_mode_radioButton.setChecked(True)
                self.last_left_rot_sw_mode = left_rot_sw_mode
                self.last_right_rot_sw_mode = right_rot_sw_mode
                self.last_clutch_mode = clutch_mode
                self.last_joy_mode = joy_mode
