from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import QTimer
from PyQt5.QtSerialPort import QSerialPort, QSerialPortInfo
from PyQt5.QtCore import QIODevice, pyqtSignal
import time, main
from base_ui import WidgetUI
from setting_define import *
from uitl import Utiliy
from uitl import Refresher
import os, requests, io, configparser, threading, urllib
from PyQt5.QtGui import QIcon, QMovie
import random
from setting_define import *

class AdditionalChooser(Utiliy):

    def __init__(self, hidchooser, main, language_chooser):
        self.main = main
        self.hidchooser = hidchooser
        self.language_chooser = language_chooser
        self.Value_List = [
         self.main.base_front_rgb_brightness_Value, self.main.base_back_rgb_brightness_Value,
         self.main.base_sound_intensity_Value]
        self.Slider_List = [
         self.main.base_front_rgb_brightness_Slider, self.main.base_back_rgb_brightness_Slider,
         self.main.base_sound_intensity_Slider]
        self.ver_path_dic = {}
        self.main.base_desc_label.setVisible(False)
        self.main.base_boot_desc_label.setVisible(False)
        self.refresh_thread = threading.Timer(0.01, self.refreshFw, None)
        self.config = configparser.ConfigParser(allow_no_value=True)
        self.setConnect()
        self.port_thread = Refresher(1)
        self.port_thread.sinOut.connect(self.readSetting)
        self.port_thread.start()
        self.movie = QMovie(':/icon/refresh.gif')
        self.movie.frameChanged.connect(lambda : self.main.base_update_refresh_pushButton.setIcon(QIcon(self.movie.currentPixmap())))

    def setConnect(self):
        """ Slider -> Value """

        def LambdaCallback1(Slider, Value):
            return lambda : Value.setText(str(Slider.value()))

        for Slider, Value in zip(self.Slider_List, self.Value_List):
            Slider.valueChanged.connect(LambdaCallback1(Slider, Value))

        self.main.base_front_rgb_brightness_Slider.valueChanged.connect(lambda val: self.hidchooser.sent_handler(SETTING_FRONT_LED_BRIGHTNESS, val))
        self.main.base_back_rgb_brightness_Slider.valueChanged.connect(lambda val: self.hidchooser.sent_handler(SETTING_BACK_LED_BRIGHTNESS, val))
        self.main.base_front_rgb_en_checkBox.clicked.connect(lambda val: self.hidchooser.sent_handler(SETTING_FRONT_LED_ENABLE, val))
        self.main.base_back_rgb_en_checkBox.clicked.connect(lambda val: self.hidchooser.sent_handler(SETTING_BACK_LED_ENABLE, val))
        self.main.base_buzzer_ffb_clipping_checkBox.clicked.connect(lambda val: self.hidchooser.sent_handler(SETTING_BUZZER_FFBCLIP_ENABLE, val))
        self.main.base_buzzer_over_rotation_checkBox.clicked.connect(lambda val: self.hidchooser.sent_handler(SETTING_BUZZER_OVERROTATION_ENABLE, val))
        self.main.base_buzzer_en_checkBox.clicked.connect(lambda val: self.hidchooser.sent_handler(SETTING_BUZZER_ENABLE, val))
        self.main.base_sound_intensity_Slider.valueChanged.connect(lambda val: self.hidchooser.sent_handler(SETTING_BUZZER_SOUND_INTENSITY, val))
        self.main.buzzer_paly_pushButton.clicked.connect(lambda : self.hidchooser.sent_handler(SETTING_BUZZER_PLAY))
        self.main.base_update_refresh_pushButton.clicked.connect(self.start_refresh_thread)
        self.main.base_update_refresh_pushButton.clicked.connect(self.refresh_movie_start)
        self.main.pairing_pushButton.clicked.connect(lambda val: self.setChannel())

    def start_refresh_thread(self):
        if not self.refresh_thread.is_alive():
            self.refresh_thread = threading.Timer(0.01, self.refreshFw, None)
            self.refresh_thread.start()

    def setChannel(self):
        ch = ch_list[(int(self.main.ch_comboBox.currentText()) - 1)]
        self.hidchooser.sent_handler(SETTING_2G4_PAIRING, ch)

    def reloadDescription(self):
        self.main.base_fw_desc_scrollArea.setVisible(True)
        type = None
        if self.hidchooser.base_device_type == 'ET5':
            type = 'et5'
        else:
            if self.hidchooser.base_device_type == 'ET3':
                type = 'et3'
        if type:
            try:
                descrition = self.config.get('base_' + type, 'descrition')
                self.main.base_update_desc_Label.setText(descrition.replace('\\n', '\n'))
            except Exception as e:
                print('reloadDescription', e)

    def reloadBootDescription(self):
        self.main.base_boot_fw_desc_scrollArea.setVisible(True)
        type = None
        if self.hidchooser.base_device_type == 'ET5':
            type = 'et5'
        else:
            if self.hidchooser.base_device_type == 'ET3':
                type = 'et3'
        if type:
            try:
                descrition = self.config.get('base_' + type, 'boot_descrition')
                print(descrition)
                self.main.base_boot_update_desc_Label.setText(descrition.replace('\\n', '\n'))
            except Exception as e:
                print('reloadDescription', e)

    def refresh_movie_start(self):
        self.movie.start()

    def refreshFw(self):
        self.main.base_update_pushButton.setEnabled(False)
        self.main.base_update_boot_pushButton.setEnabled(False)
        self.main.base_desc_label.setVisible(False)
        self.main.base_boot_desc_label.setVisible(False)
        self.main.base_update_desc_Label.setText('')
        self.main.base_boot_update_desc_Label.setText('')
        if self.hidchooser.usbhidConnected() == CONNECT_STATUS_RUNNING or self.hidchooser.usbhidConnected() == CONNECT_STATUS_OTA:
            current_version = self.main.update_version_Label.text()
            current_boot_version = self.main.update_boot_version_Label.text()
            current_model = self.main.update_model_Label.text()
            time.sleep(1)
            self.main.base_update_info_label.setStyleSheet('QLabel { \ncolor: rgb(169, 255, 47);\n}')
            if current_model == 'N/A' or current_version == 'N/A' or current_boot_version == 'N/A':
                if self.language_chooser.language == 'zh-cn':
                    self.main.base_update_info_label.setText('设备连接异常，请重启设备后再尝试')
                else:
                    self.main.base_update_info_label.setText('The device is connected abnormally, please restart and try again')
                self.movie.stop()
                return
            try:
                html = requests.get('http://47.119.165.12/immplatform/firmware/fw_base_desc')
                fw_desc = html.text
                print(fw_desc)
                self.config.readfp(io.StringIO(fw_desc))
                file_names = self.config.sections()
                file_name = None
                for _file_name in file_names:
                    fw_model_name = _file_name.split('_')[1]
                    if current_model.lower() == fw_model_name.lower():
                        file_name = _file_name
                        break

                if not file_name:
                    self.movie.stop()
                    return
                latest_version = self.config.get(file_name, 'fw_ver')
                latest_boot_version = self.config.get(file_name, 'boot_ver')
                latest_release = self.config.get(file_name, 'release')
                latest_boot_release = self.config.get(file_name, 'boot_release')
                needed_sw_version = self.config.get(file_name, 'sw_ver')
                if float(needed_sw_version) == float(IMMPLATFROM_VER):
                    if latest_version != current_version and latest_release == 'True' or self.hidchooser.usbhidConnected() == CONNECT_STATUS_OTA:
                        local_path = './fw/base/' + file_name + '_' + latest_version + '.bin'
                        download_path = self.config.get(file_name, 'path')
                        print(local_path, download_path)
                        if os.path.exists(local_path):
                            os.remove(local_path)
                        urllib.request.urlretrieve(download_path, local_path)
                        self.main.base_update_pushButton.setEnabled(True)
                        self.reloadDescription()
                        if self.language_chooser.language == 'zh-cn':
                            if self.hidchooser.usbhidConnected() == CONNECT_STATUS_OTA:
                                self.main.base_update_info_label.setText(' 可更新固件')
                                self.main.update_ver_label.setText('V' + latest_version)
                            else:
                                self.main.base_update_info_label.setText(' 发现新版本固件，建议立即升级')
                                self.main.update_ver_label.setText('V' + latest_version)
                        else:
                            if self.hidchooser.usbhidConnected() == CONNECT_STATUS_OTA:
                                self.main.base_update_info_label.setText(' Updatable firmware')
                                self.main.update_ver_label.setText('V' + latest_version)
                            else:
                                self.main.base_update_info_label.setText(' New version of firmware has been found')
                                self.main.update_ver_label.setText('V' + latest_version)
                            self.main.base_desc_label.setVisible(True)
                    else:
                        if self.language_chooser.language == 'zh-cn':
                            self.main.base_update_info_label.setText(' 已经是最新版本的固件')
                        else:
                            self.main.base_update_info_label.setText(' The firmware is already the latest version')
                    if self.hidchooser.usbhidConnected() == CONNECT_STATUS_RUNNING:
                        if latest_boot_version != current_boot_version:
                            if latest_boot_release == 'True':
                                local_path = './fw/base/' + file_name + '_boot_' + latest_boot_version + '.bin'
                                download_path = self.config.get(file_name, 'boot_path')
                                print(local_path, download_path)
                                if os.path.exists(local_path):
                                    os.remove(local_path)
                                urllib.request.urlretrieve(download_path, local_path)
                                self.main.base_update_boot_pushButton.setEnabled(True)
                                self.reloadBootDescription()
                                if self.language_chooser.language == 'zh-cn':
                                    self.main.base_boot_update_info_label.setText(' 发现新版本固件，建议立即升级')
                                    self.main.boot_update_ver_label.setText('V' + latest_boot_version)
                                else:
                                    self.main.base_boot_update_info_label.setText(' New version of firmware has been found')
                                    self.main.boot_update_ver_label.setText('V' + latest_boot_version)
                                self.main.base_boot_desc_label.setVisible(True)
                        else:
                            if self.language_chooser.language == 'zh-cn':
                                self.main.boot_update_ver_label.setText('')
                                self.main.base_boot_update_info_label.setText(' 已经是最新版本的固件')
                            else:
                                self.main.boot_update_ver_label.setText('')
                                self.main.base_boot_update_info_label.setText(' The firmware is already the latest version')
                else:
                    if self.language_chooser.language == 'zh-cn':
                        self.main.base_update_info_label.setText(' 请先更新IMMPLATFORM软件后再进行设备升级')
                    else:
                        self.main.base_update_info_label.setText(' Please update the software before upgrading')
            except Exception as e:
                print('refreshFw', e)
                if self.language_chooser.language == 'zh-cn':
                    self.main.base_update_info_label.setText(' 无法连接到远程服务器')
                else:
                    self.main.base_update_info_label.setText(' Cannot connect to remote server')
                self.main.base_update_info_label.setStyleSheet('QLabel { \ncolor: rgb(255, 20, 20);\n}')

        self.movie.stop()

    def readSetting(self):
        if self.hidchooser.usbhidDataReady():
            front_en = self.hidchooser.getFrontLedEnable()
            back_en = self.hidchooser.getBackLedEnable()
            front_brightness = self.hidchooser.front_led_brightness
            back_brightness = self.hidchooser.back_led_brightness
            buzzer_en = self.hidchooser.getBuzzerEnable()
            buzzer_intensity = self.hidchooser.buzzer_intensity
            buzzer_over_rotation_enable = self.hidchooser.buzzer_over_rotation_enable
            buzzer_ffb_clip_enable = self.hidchooser.buzzer_ffb_clip_enable
            if self.hidchooser.cmd_sending == False:
                if front_en:
                    self.main.base_front_rgb_en_checkBox.setChecked(True)
                    self.main.base_front_rgb_brightness_Value.setEnabled(True)
                    self.main.base_front_rgb_brightness_Slider.setEnabled(True)
                else:
                    self.main.base_front_rgb_en_checkBox.setChecked(False)
                    self.main.base_front_rgb_brightness_Value.setEnabled(False)
                    self.main.base_front_rgb_brightness_Slider.setEnabled(False)
                if back_en:
                    self.main.base_back_rgb_en_checkBox.setChecked(True)
                    self.main.base_back_rgb_brightness_Value.setEnabled(True)
                    self.main.base_back_rgb_brightness_Slider.setEnabled(True)
                else:
                    self.main.base_back_rgb_en_checkBox.setChecked(False)
                    self.main.base_back_rgb_brightness_Value.setEnabled(False)
                    self.main.base_back_rgb_brightness_Slider.setEnabled(False)
                self.main.base_front_rgb_brightness_Slider.setValue(front_brightness)
                self.main.base_back_rgb_brightness_Slider.setValue(back_brightness)
                if buzzer_en:
                    self.main.base_buzzer_en_checkBox.setChecked(True)
                    self.main.base_sound_intensity_Value.setEnabled(True)
                    self.main.base_sound_intensity_Slider.setEnabled(True)
                    self.main.buzzer_paly_pushButton.setEnabled(True)
                else:
                    self.main.base_buzzer_en_checkBox.setChecked(False)
                    self.main.base_sound_intensity_Value.setEnabled(False)
                    self.main.base_sound_intensity_Slider.setEnabled(False)
                    self.main.buzzer_paly_pushButton.setEnabled(False)
                if buzzer_over_rotation_enable:
                    self.main.base_buzzer_over_rotation_checkBox.setChecked(True)
                else:
                    self.main.base_buzzer_over_rotation_checkBox.setChecked(False)
                if buzzer_ffb_clip_enable:
                    self.main.base_buzzer_ffb_clipping_checkBox.setChecked(True)
                else:
                    self.main.base_buzzer_ffb_clipping_checkBox.setChecked(False)
                self.main.base_sound_intensity_Slider.setValue(buzzer_intensity)
