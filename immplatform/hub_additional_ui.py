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
from setting_define import *

class HubAdditionalChooser(Utiliy):

    def __init__(self, hub_hidchooser, base_hidchooser, main, language_chooser):
        self.main = main
        self.hub_hidchooser = hub_hidchooser
        self.base_hidchooser = base_hidchooser
        self.language_chooser = language_chooser
        self.Value_List = [
         self.main.hub_sound_intensity_Value]
        self.Slider_List = [
         self.main.hub_sound_intensity_Slider]
        self.ver_path_dic = {}
        self.refresh_thread = threading.Timer(0.01, self.refreshFw, None)
        self.main.hub_desc_label.setVisible(False)
        self.main.hub_boot_desc_label.setVisible(False)
        self.config = configparser.ConfigParser(allow_no_value=True)
        self.setConnect()
        self.port_thread = Refresher(1)
        self.port_thread.sinOut.connect(self.readSetting)
        self.port_thread.start()
        self.movie = QMovie(':/icon/refresh.gif')
        self.movie.frameChanged.connect(lambda : self.main.hub_update_refresh_pushButton.setIcon(QIcon(self.movie.currentPixmap())))

    def setConnect(self):
        """ Slider -> Value """

        def LambdaCallback1(Slider, Value):
            return lambda : Value.setText(str(Slider.value()))

        for Slider, Value in zip(self.Slider_List, self.Value_List):
            Slider.valueChanged.connect(LambdaCallback1(Slider, Value))

        self.main.hub_buzzer_en_checkBox.clicked.connect(lambda val: self.hubSentHandler(SETTING_HUB_BUZZER_ENABLE, val))
        self.main.hub_sound_intensity_Slider.valueChanged.connect(lambda val: self.hubSentHandler(SETTING_HUB_BUZZER_SOUND_INTENSITY, val))
        self.main.buzzer_paly_pushButton.clicked.connect(lambda val: self.hubSentHandler(SETTING_HUB_BUZZER_PLAY, 0))
        self.main.hub_update_refresh_pushButton.clicked.connect(self.start_refresh_thread)
        self.main.hub_update_refresh_pushButton.clicked.connect(self.refresh_movie_start)

    def start_refresh_thread(self):
        if not self.refresh_thread.is_alive():
            self.refresh_thread = threading.Timer(0.01, self.refreshFw, None)
            self.refresh_thread.start()

    def hubSentHandler(self, cmd, val):
        print(cmd, val)
        self.hub_hidchooser.sent_handler(cmd, val)
        self.base_hidchooser.sent_handler(cmd, val)

    def reloadDescription(self):
        self.main.hub_fw_desc_scrollArea.setVisible(True)
        type = None
        if self.hub_hidchooser.hub_device_type == 'FD1':
            type = 'fd1'
        else:
            if self.hub_hidchooser.hub_device_type == 'FD1S':
                type = 'fd1s'
        if type:
            try:
                descrition = self.config.get('hub_' + type, 'descrition')
                print(descrition)
                self.main.hub_update_desc_Label.setText(descrition.replace('\\n', '\n'))
            except Exception as e:
                print('reloadDescription', e)

    def reloadBootDescription(self):
        self.main.hub_boot_fw_desc_scrollArea.setVisible(True)
        type = None
        if self.hub_hidchooser.hub_device_type == 'FD1':
            type = 'fd1'
        else:
            if self.hub_hidchooser.hub_device_type == 'FD1S':
                type = 'fd1s'
        if type:
            try:
                descrition = self.config.get('hub_' + type, 'boot_descrition')
                print(descrition)
                self.main.hub_boot_update_desc_Label.setText(descrition.replace('\\n', '\n'))
            except Exception as e:
                print('reloadDescription', e)

    def refresh_movie_start(self):
        self.movie.start()

    def refreshFw(self):
        self.main.hub_update_pushButton.setEnabled(False)
        self.main.hub_update_boot_pushButton.setEnabled(False)
        self.main.hub_desc_label.setVisible(False)
        self.main.hub_boot_desc_label.setVisible(False)
        self.main.hub_update_desc_Label.setText('')
        self.main.hub_boot_update_desc_Label.setText('')
        if self.hub_hidchooser.usbhidConnected() == CONNECT_STATUS_RUNNING or self.hub_hidchooser.usbhidConnected() == CONNECT_STATUS_OTA:
            current_version = self.main.update_version_Label.text()
            current_boot_version = self.main.update_boot_version_Label.text()
            current_model = self.main.update_model_Label.text()
            time.sleep(1)
            self.main.hub_update_info_label.setStyleSheet('QLabel { \ncolor: rgb(169, 255, 47);\n}')
            if current_model == 'N/A' or current_version == 'N/A':
                if self.language_chooser.language == 'zh-cn':
                    self.main.hub_update_info_label.setText('设备连接异常，请重启设备后再尝试')
                else:
                    self.main.hub_update_info_label.setText('The device is connected abnormally, please restart and try again')
                return
            try:
                html = requests.get('http://47.119.165.12/immplatform/firmware/fw_hub_desc')
                fw_desc = html.text
                self.config.readfp(io.StringIO(fw_desc))
                file_names = self.config.sections()
                file_name = None
                for _file_name in file_names:
                    fw_model_name = _file_name.split('_')[1]
                    if current_model.lower() == fw_model_name.lower():
                        file_name = _file_name
                        break

                if not file_name:
                    return
                latest_version = self.config.get(file_name, 'fw_ver')
                latest_boot_version = self.config.get(file_name, 'boot_ver')
                latest_release = self.config.get(file_name, 'release')
                latest_boot_release = self.config.get(file_name, 'boot_release')
                needed_sw_version = self.config.get(file_name, 'sw_ver')
                if float(needed_sw_version) == float(IMMPLATFROM_VER):
                    if latest_version != current_version:
                        if latest_release == 'True':
                            local_path = './fw/hub/' + file_name + '_' + latest_version + '.bin'
                            download_path = self.config.get(file_name, 'path')
                            print(local_path)
                            if os.path.exists(local_path):
                                os.remove(local_path)
                            urllib.request.urlretrieve(download_path, local_path)
                            self.main.hub_update_pushButton.setEnabled(True)
                            self.reloadDescription()
                            if self.language_chooser.language == 'zh-cn':
                                if self.hub_hidchooser.usbhidConnected() == CONNECT_STATUS_OTA:
                                    self.main.hub_update_info_label.setText(' 可更新固件')
                                    self.main.update_ver_label.setText('V' + latest_version)
                                else:
                                    self.main.hub_update_info_label.setText(' 发现新版本固件，建议立即升级')
                                    self.main.update_ver_label.setText('V' + latest_version)
                            else:
                                if self.hub_hidchooser.usbhidConnected() == CONNECT_STATUS_OTA:
                                    self.main.hub_update_info_label.setText(' Updatable firmware')
                                    self.main.update_ver_label.setText('V' + latest_version)
                                else:
                                    self.main.hub_update_info_label.setText(' New version of firmware has been found')
                                    self.main.update_ver_label.setText('V' + latest_version)
                                self.main.hub_desc_label.setVisible(True)
                        else:
                            if self.language_chooser.language == 'zh-cn':
                                self.main.hub_update_info_label.setText(' 已经是最新版本的固件')
                            else:
                                self.main.hub_update_info_label.setText('The firmware is already the latest version')
                        if self.hub_hidchooser.usbhidConnected() == CONNECT_STATUS_RUNNING:
                            if latest_boot_version == current_boot_version:
                                if latest_boot_release == 'True':
                                    local_path = './fw/hub/' + file_name + '_boot_' + latest_boot_version + '.bin'
                                    download_path = self.config.get(file_name, 'boot_path')
                                    print(local_path)
                                    if os.path.exists(local_path):
                                        os.remove(local_path)
                                    urllib.request.urlretrieve(download_path, local_path)
                                    self.main.hub_update_boot_pushButton.setEnabled(True)
                                    self.reloadBootDescription()
                                    if self.language_chooser.language == 'zh-cn':
                                        self.main.hub_boot_update_info_label.setText(' 发现新版本固件，建议立即升级')
                                        self.main.boot_update_ver_label.setText('V' + latest_boot_version)
                                    else:
                                        self.main.hub_boot_update_info_label.setText(' New version of firmware has been found')
                                        self.main.boot_update_ver_label.setText('V' + latest_boot_version)
                                    self.main.hub_boot_desc_label.setVisible(True)
                            else:
                                if self.language_chooser.language == 'zh-cn':
                                    self.main.boot_update_ver_label.setText('')
                                    self.main.hub_boot_update_info_label.setText(' 已经是最新版本的固件')
                                else:
                                    self.main.boot_update_ver_label.setText('')
                                    self.main.hub_boot_update_info_label.setText(' The firmware is already the latest version')
                else:
                    if self.language_chooser.language == 'zh-cn':
                        self.main.hub_update_info_label.setText(' 请先更新IMMPLATFORM软件后再进行设备升级')
                    else:
                        self.main.hub_update_info_label.setText(' Please update the software before upgrading')
            except Exception as e:
                print('refreshFw', e)
                if self.language_chooser.language == 'zh-cn':
                    self.main.hub_update_info_label.setText(' 无法连接到远程服务器')
                else:
                    self.main.hub_update_info_label.setText(' Cannot connect to remote server')
                self.main.hub_update_info_label.setStyleSheet('QLabel { \ncolor: rgb(255, 20, 20);\n}')

        else:
            if self.language_chooser.language == 'zh-cn':
                self.main.hub_update_info_label.setText(' 请通过USB线连接后更新')
            else:
                self.main.hub_update_info_label.setText(' Please update after connecting via USB cable')
            self.main.hub_update_info_label.setStyleSheet('QLabel { \ncolor: rgb(255, 20, 20);\n}')
        self.movie.stop()

    def readSetting(self):
        if self.hub_hidchooser.usbhidDataReady():
            buzzer_en = self.hub_hidchooser.getBuzzerEnable()
            buzzer_intensity = self.hub_hidchooser.buzzer_intensity
            if self.hub_hidchooser.cmd_sending == False:
                if buzzer_en:
                    self.main.hub_buzzer_en_checkBox.setChecked(True)
                    self.main.hub_sound_intensity_Value.setEnabled(True)
                    self.main.hub_sound_intensity_Slider.setEnabled(True)
                    self.main.buzzer_paly_pushButton.setEnabled(True)
                else:
                    self.main.hub_buzzer_en_checkBox.setChecked(False)
                    self.main.hub_sound_intensity_Value.setEnabled(False)
                    self.main.hub_sound_intensity_Slider.setEnabled(False)
                    self.main.buzzer_paly_pushButton.setEnabled(False)
                self.main.hub_sound_intensity_Slider.setValue(buzzer_intensity)
