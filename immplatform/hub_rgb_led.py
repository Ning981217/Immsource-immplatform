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
from PyQt5.Qt import *
from setting_define import *
from uitl import Utiliy
from uitl import Refresher
import configparser, threading

class HubRgbLedChooser(Utiliy):

    def __init__(self, hidchooser, base_hidchooser, main, base_main, dash):
        self.main = main
        self.hidchooser = hidchooser
        self.base_hidchooser = base_hidchooser
        self.dash = dash
        self.base_main = base_main
        self.car_speed = 0
        self.flush_time = 0
        self.led_reset = False
        self.static_updata_gap = 0
        self.graphics_updata_gap = 0
        self.physics_1_updata_gap = 0
        self.physics_2_updata_gap = 0
        self.main.hub_led_test_pushButton.clicked.connect(self.RgbTestStart)
        self.button_texts = [
         'P', 'SUB', 'L', 'R', 'ADD', 'N', 'ERS', 'DRS', 'K1', 'K2', 'FL1', 'FL2', 'FL3', 'FR1', 'FR2', 'FR3']
        self.Value_List = [
         self.main.L1_Value, self.main.L2_Value, self.main.L3_Value, self.main.L4_Value, self.main.L5_Value,
         self.main.L6_Value, self.main.L7_Value, self.main.L8_Value, self.main.L9_Value, self.main.L10_Value,
         self.main.flush_Value]
        self.Slider_List = [
         self.main.L1_verticalSlider, self.main.L2_verticalSlider, self.main.L3_verticalSlider, self.main.L4_verticalSlider, self.main.L5_verticalSlider,
         self.main.L6_verticalSlider, self.main.L7_verticalSlider, self.main.L8_verticalSlider, self.main.L9_verticalSlider, self.main.L10_verticalSlider,
         self.main.flush_verticalSlider]
        self.main.Button_led_brightness_Slider.valueChanged.connect(lambda val: self.main.Button_led_brightness_Value.setText(str(val)))

        def LambdaCallback1(Slider, Value):
            return lambda : Value.setText(str(Slider.value()))

        for Slider, Value in zip(self.Slider_List, self.Value_List):
            Slider.valueChanged.connect(LambdaCallback1(Slider, Value))
            Slider.valueChanged.connect(self.rpmModeSetting)

        self.main.rpm_linear_radioButton.clicked.connect(lambda val: self.rpmModeSetting(1))
        self.main.rpm_twoway_radioButton.clicked.connect(lambda val: self.rpmModeSetting(1))
        self.main.rpm_customize_radioButton.clicked.connect(lambda val: self.rpmModeSetting(1))
        self.main.Flush_pushButton.clicked.connect(lambda val: self.flushSetEnable(val))

        def test_LambdaCallback(flag, status):
            return lambda : self.set_test(flag, status)

        status_texts = [
         'pitlimiter', 'drs', 'drsallowed', 'tc', 'abs', 'greenflag', 'redflag', 'yellowflag', 'blueflag', 'whiteflag', 'blackflag']
        for status_text in status_texts:
            exec('self.' + status_text + '_test=False')
            exec('self.main.' + status_text + "_test_pushButton.pressed.connect(test_LambdaCallback('" + status_text + "_test', True))")
            exec('self.main.' + status_text + "_test_pushButton.released.connect(test_LambdaCallback('" + status_text + "_test', False))")

        self.ws2812_rgb = [
         0] * 36
        self.ws2812_button_rgb = [0] * 48
        self.test_p = 0
        self.last_flush_status = False
        self.last_button_flush_status = True
        self.port_thread = Refresher(0.03333333333333333)
        self.port_thread.sinOut.connect(self.updataRgbLed)
        self.port_thread.start()
        self.button_led_thread = Refresher(0.03333333333333333)
        self.button_led_thread.sinOut.connect(self.updataButtonLed)
        self.button_led_thread.start()
        self.rgb_test_thread = Refresher(0.05)
        self.rgb_test_thread.sinOut.connect(self.RgbTestRunning)

    def set_test(self, flag, status):
        exec('self.' + flag + '=' + str(status))

    def flushSetEnable(self, status):
        self.main.flush_verticalSlider.setEnabled(status)
        self.main.flush_Value.setEnabled(status)

    def rpmModeSetting(self, radioButton_check):
        if self.main.rpm_linear_radioButton.isChecked():
            if radioButton_check == 1:
                self.main.L10_verticalSlider.setValue(self.main.flush_verticalSlider.value())
            self.main.L1_verticalSlider.setEnabled(True)
            self.main.L10_verticalSlider.setEnabled(True)
            self.main.L2_verticalSlider.setEnabled(False)
            self.main.L3_verticalSlider.setEnabled(False)
            self.main.L4_verticalSlider.setEnabled(False)
            self.main.L5_verticalSlider.setEnabled(False)
            self.main.L6_verticalSlider.setEnabled(False)
            self.main.L7_verticalSlider.setEnabled(False)
            self.main.L8_verticalSlider.setEnabled(False)
            self.main.L9_verticalSlider.setEnabled(False)
            min_val = self.main.L1_verticalSlider.value()
            max_val = self.main.L10_verticalSlider.value()
            gap = (max_val - min_val) / 9
            for index, Slider in enumerate(self.Slider_List[:-1]):
                Slider.setValue(min_val + index * gap)

        else:
            if self.main.rpm_twoway_radioButton.isChecked():
                if radioButton_check == 1:
                    self.main.L5_verticalSlider.setValue(self.main.flush_verticalSlider.value())
                self.main.L1_verticalSlider.setEnabled(True)
                self.main.L5_verticalSlider.setEnabled(True)
                self.main.L2_verticalSlider.setEnabled(False)
                self.main.L3_verticalSlider.setEnabled(False)
                self.main.L4_verticalSlider.setEnabled(False)
                self.main.L6_verticalSlider.setEnabled(False)
                self.main.L7_verticalSlider.setEnabled(False)
                self.main.L8_verticalSlider.setEnabled(False)
                self.main.L9_verticalSlider.setEnabled(False)
                self.main.L10_verticalSlider.setEnabled(False)
                min_val = self.main.L1_verticalSlider.value()
                max_val = self.main.L5_verticalSlider.value()
                gap = (max_val - min_val) / 4
                for index, Slider in enumerate(self.Slider_List[:-6]):
                    Slider.setValue(min_val + index * gap)

                for index, Slider in enumerate(self.Slider_List[5:-1]):
                    Slider.setValue(max_val - index * gap)

            if self.main.rpm_customize_radioButton.isChecked():
                self.main.L1_verticalSlider.setEnabled(True)
                self.main.L2_verticalSlider.setEnabled(True)
                self.main.L3_verticalSlider.setEnabled(True)
                self.main.L4_verticalSlider.setEnabled(True)
                self.main.L5_verticalSlider.setEnabled(True)
                self.main.L6_verticalSlider.setEnabled(True)
                self.main.L7_verticalSlider.setEnabled(True)
                self.main.L8_verticalSlider.setEnabled(True)
                self.main.L9_verticalSlider.setEnabled(True)
                self.main.L10_verticalSlider.setEnabled(True)
            value_list = []
            for Slider in self.Slider_List:
                value_list.append(Slider.value())

            if self.main.flush_verticalSlider.value() < max(value_list):
                self.main.flush_verticalSlider.setValue(max(value_list))

    def setOnIndexLed(self, led_index):
        brightness = float(self.main.hub_led_brightness_Slider.value()) / 30
        led_button = eval('self.main.L' + str(led_index + 1) + '_pushButton')
        bgColor = led_button.palette().color(QPalette.Background)
        r, g, b, a = bgColor.getRgb()
        r = min(r * brightness, 255)
        g = min(g * brightness, 255)
        b = min(b * brightness, 255)
        self.ws2812_rgb[led_index * 3] = int(r * 1)
        self.ws2812_rgb[led_index * 3 + 1] = int(g * 1)
        self.ws2812_rgb[led_index * 3 + 2] = int(b * 1)

    def setOffIndexLed(self, led_index):
        self.ws2812_rgb[led_index * 3] = 0
        self.ws2812_rgb[led_index * 3 + 1] = 0
        self.ws2812_rgb[led_index * 3 + 2] = 0

    def RgbTestStart(self):
        self.port_thread.stop()
        self.test_p = 0
        self.rgb_test_thread.start()
        self.rgb_test_thread.pcontinue()

    def RgbTestRunning(self):
        self.updataRgbLedForTest(self.test_p)
        self.test_p = round(self.test_p + 0.1, 2)
        self.hidchooser.sent_RGB_handler(SETTING_RGB, self.ws2812_rgb, self.ws2812_button_rgb)
        self.base_hidchooser.sent_RGB_handler(SETTING_RGB, self.ws2812_rgb, self.ws2812_button_rgb)
        if self.main.Flush_pushButton.isChecked():
            test_t = 1.8
        else:
            test_t = 1.2
        if self.test_p >= test_t:
            for i in range(3):
                self.ws2812_rgb = [
                 0] * 64
                self.hidchooser.sent_RGB_handler(SETTING_RGB, self.ws2812_rgb, self.ws2812_button_rgb, True)
                self.base_hidchooser.sent_RGB_handler(SETTING_RGB, self.ws2812_rgb, self.ws2812_button_rgb, True)

            self.rgb_test_thread.stop()
            self.port_thread.start()
            self.port_thread.pcontinue()

    def updataButtonRgbLed(self):
        for led_index, button_text in enumerate(self.button_texts):
            led_checkbox = eval('self.main.' + button_text + '_led_en_checkBox')
            if led_checkbox.isChecked():
                if led_index <= 9:
                    brightness = self.main.Button_led_brightness_Slider.value() / 30
                else:
                    brightness = self.main.hub_led_brightness_Slider.value() / 30
            else:
                brightness = 0
            led_button = eval('self.main.' + button_text + '_pushButton')
            bgColor = led_button.palette().color(QPalette.Background)
            r, g, b, a = bgColor.getRgb()
            r = min(r * brightness, 255)
            g = min(g * brightness, 255)
            b = min(b * brightness, 255)
            self.ws2812_button_rgb[led_index * 3] = int(r * 1)
            self.ws2812_button_rgb[led_index * 3 + 1] = int(g * 1)
            self.ws2812_button_rgb[led_index * 3 + 2] = int(b * 1)

        self.hidchooser.sent_RGB_handler(SETTING_BUTTON_RGB, self.ws2812_rgb, self.ws2812_button_rgb)
        self.base_hidchooser.sent_RGB_handler(SETTING_BUTTON_RGB, self.ws2812_rgb, self.ws2812_button_rgb)

    def updataButtonLed(self):
        pitlimiter = self.pitlimiter_test | gameData.t_pit_limiter
        drs = self.drs_test | gameData.t_drs_actived
        blackflag = self.blackflag_test | gameData.t_black_flag
        greenflag = self.greenflag_test | gameData.t_green_flag
        redflag = self.redflag_test | gameData.t_red_flag
        yellowflag = self.yellowflag_test | gameData.t_yellow_flag
        blueflag = self.blueflag_test | gameData.t_blue_flag
        whiteflag = self.whiteflag_test | gameData.t_white_flag
        tc = self.tc_test | gameData.t_tc_running
        abs = self.abs_test | gameData.t_abs_running
        drsallowed = self.drsallowed_test | gameData.t_drs_allowed
        active_status = None
        if pitlimiter:
            active_status = 'pitlimiter'
        if drs:
            active_status = 'drs'
        if blackflag:
            active_status = 'blackflag'
        if greenflag:
            active_status = 'greenflag'
        if redflag:
            active_status = 'redflag'
        if yellowflag:
            active_status = 'yellowflag'
        if blueflag:
            active_status = 'blueflag'
        if whiteflag:
            active_status = 'whiteflag'
        if tc:
            active_status = 'tc'
        if abs:
            active_status = 'abs'
        if drsallowed:
            active_status = 'drsallowed'
        if active_status == None:
            self.updataButtonRgbLed()
            return
        else:
            status_led_checkbox = eval('self.main.' + active_status + '_en_checkBox')
            if not status_led_checkbox.isChecked():
                self.updataButtonRgbLed()
                return
            if self.last_button_flush_status == True:
                for led_index, button_text in enumerate(self.button_texts):
                    led_checkbox = eval('self.main.' + button_text + '_led_en_checkBox')
                    if led_checkbox.isChecked():
                        if led_index <= 9:
                            brightness = self.main.Button_led_brightness_Slider.value() / 30
                        else:
                            brightness = self.main.hub_led_brightness_Slider.value() / 30
                    else:
                        brightness = 0
                    status_led_button = eval('self.main.' + active_status + '_' + button_text + '_pushButton')
                    bgColor = status_led_button.palette().color(QPalette.Background)
                    r, g, b, a = bgColor.getRgb()
                    if not (r == 0 and g == 0 and b == 0):
                        r = min(r * brightness, 255)
                        g = min(g * brightness, 255)
                        b = min(b * brightness, 255)
                        self.ws2812_button_rgb[led_index * 3] = int(r * 1)
                        self.ws2812_button_rgb[led_index * 3 + 1] = int(g * 1)
                        self.ws2812_button_rgb[led_index * 3 + 2] = int(b * 1)

                self.hidchooser.sent_RGB_handler(SETTING_BUTTON_RGB, self.ws2812_rgb, self.ws2812_button_rgb)
                self.base_hidchooser.sent_RGB_handler(SETTING_BUTTON_RGB, self.ws2812_rgb, self.ws2812_button_rgb)
            else:
                for led_index, button_text in enumerate(self.button_texts):
                    led_checkbox = eval('self.main.' + button_text + '_led_en_checkBox')
                    if led_checkbox.isChecked():
                        if led_index <= 9:
                            brightness = self.main.Button_led_brightness_Slider.value() / 30
                        else:
                            brightness = self.main.hub_led_brightness_Slider.value() / 30
                    else:
                        brightness = 0
                    status_led_button = eval('self.main.' + active_status + '_' + button_text + '_pushButton')
                    bgColor = status_led_button.palette().color(QPalette.Background)
                    r, g, b, a = bgColor.getRgb()
                    if not (r == 0 and g == 0 and b == 0):
                        if not active_status == 'drs':
                            if not active_status == 'tc':
                                if active_status == 'abs' or active_status == 'drsallowed':
                                    pass
                        else:
                            self.ws2812_button_rgb[led_index * 3] = 0
                            self.ws2812_button_rgb[led_index * 3 + 1] = 0
                            self.ws2812_button_rgb[led_index * 3 + 2] = 0
                    else:
                        led_button = eval('self.main.' + button_text + '_pushButton')
                        bgColor = led_button.palette().color(QPalette.Background)
                        r, g, b, a = bgColor.getRgb()
                        r = min(r * brightness, 255)
                        g = min(g * brightness, 255)
                        b = min(b * brightness, 255)
                        self.ws2812_button_rgb[led_index * 3] = int(r * 1)
                        self.ws2812_button_rgb[led_index * 3 + 1] = int(g * 1)
                        self.ws2812_button_rgb[led_index * 3 + 2] = int(b * 1)

                self.hidchooser.sent_RGB_handler(SETTING_BUTTON_RGB, self.ws2812_rgb, self.ws2812_button_rgb)
                self.base_hidchooser.sent_RGB_handler(SETTING_BUTTON_RGB, self.ws2812_rgb, self.ws2812_button_rgb)
            self.flush_time = self.flush_time + 1
            speed = 5
            if self.flush_time <= speed:
                self.last_button_flush_status = True
            else:
                self.last_button_flush_status = False
        if self.flush_time >= 2 * speed:
            self.flush_time = 0

    def updataRgbLed(self):
        p = self.dash.getRpmPercentage()
        if p == None:
            if self.led_reset == True:
                self.ws2812_rgb = [
                 0] * 64
                self.hidchooser.sent_RGB_handler(SETTING_RGB, self.ws2812_rgb, self.ws2812_button_rgb, True)
                self.base_hidchooser.sent_RGB_handler(SETTING_RGB, self.ws2812_rgb, self.ws2812_button_rgb, True)
                self.led_reset = False
            return
        else:
            self.led_reset = True
            if self.main.Flush_pushButton.isChecked():
                if p >= self.main.flush_verticalSlider.value() / 100:
                    if self.last_flush_status == True:
                        for i in range(10):
                            self.setOffIndexLed(i)

                        self.last_flush_status = False
                    else:
                        for i in range(10):
                            self.setOnIndexLed(i)

                        self.last_flush_status = True
                    self.hidchooser.sent_RGB_handler(SETTING_RGB, self.ws2812_rgb, self.ws2812_button_rgb)
                    self.base_hidchooser.sent_RGB_handler(SETTING_RGB, self.ws2812_rgb, self.ws2812_button_rgb)
                    return
        for i in range(10):
            current_led_rpm_per_slider = eval('self.main.L' + str(i + 1) + '_verticalSlider')
            if p > float(current_led_rpm_per_slider.value()) / 100:
                self.setOnIndexLed(i)
            else:
                self.setOffIndexLed(i)

        self.hidchooser.sent_RGB_handler(SETTING_RGB, self.ws2812_rgb, self.ws2812_button_rgb)
        self.base_hidchooser.sent_RGB_handler(SETTING_RGB, self.ws2812_rgb, self.ws2812_button_rgb)

    def updataRgbLedForTest(self, p):
        if self.main.Flush_pushButton.isChecked():
            if p >= self.main.flush_verticalSlider.value() / 100:
                if self.last_flush_status == True:
                    for i in range(10):
                        self.setOffIndexLed(i)

                    self.last_flush_status = False
                else:
                    for i in range(10):
                        self.setOnIndexLed(i)

                    self.last_flush_status = True
                return
        for i in range(10):
            current_led_rpm_per_slider = eval('self.main.L' + str(i + 1) + '_verticalSlider')
            if p > float(current_led_rpm_per_slider.value()) / 100:
                self.setOnIndexLed(i)
            else:
                self.setOffIndexLed(i)
