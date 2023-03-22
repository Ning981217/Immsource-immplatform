import sys, os, logging, ctypes, sys, os, time
from cryptography.fernet import Fernet
import pyperclip

def execute_cmd(cmd):
    proc = subprocess.Popen(cmd,
      shell=True,
      stdout=(subprocess.PIPE),
      stderr=(subprocess.STDOUT),
      stdin=(subprocess.PIPE))
    proc.stdin.close()
    proc.wait()
    result = proc.stdout.read().decode('gbk')
    proc.stdout.close()
    return result


def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False


os.chdir(os.path.dirname(os.path.abspath(sys.argv[0])))
import webbrowser
from PyQt5 import QtCore, QtWidgets
import socket, uuid
from PyQt5.Qt import *
from PyQt5.QtGui import QIntValidator
from PyQt5.QtChart import QChartView
from PyQt5.QtCore import QTranslator
from PyQt5.QtWidgets import QDialog
from psutil import process_iter, Process
from PyQt5.QtGui import QTransform, QPixmap, QImage
from dynamicine import DynamicLine
from dynamicine import CurveChartView
from win32 import win32api, win32gui, win32print
from win32.win32api import GetSystemMetrics
from winreg import *
import re, requests, io, threading, subprocess, steering_ui, setting_ui, hid_ui, update_ui, hub_hid_ui, gforce_hid_ui, additional_ui, hub_additional_ui, pyDash, hub_rgb_led, hub_input, axis_ui
from update_ui import *
from setting_define import *
import configparser
from res.immbase import Ui_MainWindow as BaseUi
from res.immhub import Ui_MainWindow as HubUi
from res.immforce import Ui_MainWindow as GforceUi
from res.menu_bar import Ui_MainWindow as MenuUi
from res.preset import Ui_MainWindow as PresetUi
from res.colorpick import Ui_Dialog as ColorPickerUi
from res.menu_dialog import Ui_Dialog as MenuDialogUi
from res.cfg_new_rename import Ui_cfg_new_rename_Dialog as CfgDialog
from res.updatafw import Ui_update_fw_Dialog as UpdateFwDialogUi
from res.updatasw import Ui_update_sw_Dialog as UpdateSwDialogUi
from res.gear_calibrate import Ui_Dialog as GearCalibrateDialogUi
from res.connect_info import Ui_connect_info_Dialog as ConnectInfoDialogUi
from res.connect_info2 import Ui_connect_info_Dialog as ConnectInfoDialogUi2
from res.connect_info3 import Ui_MainWindow as ConnectInfoDialogUi
from res.help import Ui_help_info_Dialog as HelpInfoDialogUi
from res.error import Ui_Error_Dialog as ErrorDialogUi
from game_cfg import *
from game_et3_cfg import *
from immcore_cfg import *
from immcore_preset import *
from immcore_button_led import *
from immcore_rpm_led import *
import win32api, win32con, winreg, os, sys

def searchFile(key, startPath='.'):
    if not os.path.isdir(startPath):
        raise ValueError
    l = [os.path.join(startPath, x) for x in os.listdir(startPath)]
    filelist = [x for x in l if os.path.isfile(x) if key in os.path.splitext(os.path.basename(x))[0]]
    if not hasattr(searchFile, 'basePath'):
        searchFile.basePath = startPath
    outmap = map(lambda x: os.path.relpath(x, searchFile.basePath), filelist)
    outlist = list(outmap)
    dirlist = [x for x in l if os.path.isdir(x)]
    for dir in dirlist:
        outlist = outlist + searchFile(key, dir)

    return outlist


if not os.path.exists('sw'):
    os.makedirs('sw')
if not os.path.exists('cfg'):
    os.makedirs('cfg')
if not os.path.exists('./cfg/ui_setting.cfg'):
    with open('./cfg/ui_setting.cfg', 'w+') as (f):
        f.write(ui_setting_cfg)
if not os.path.exists('./cfg/clutch_setting.cfg'):
    with open('./cfg/clutch_setting.cfg', 'w+') as (f):
        f.write(clutch_setting_cfg)
if not os.path.exists('./fw/base'):
    os.makedirs('./fw/base')
if not os.path.exists('./fw/hub'):
    os.makedirs('./fw/hub')
if not os.path.exists('./hub_led/button_led'):
    os.makedirs('./hub_led/button_led')
if not searchFile('1_button_', './hub_led/button_led'):
    with open('./hub_led/button_led/1_button_GT.cfg', 'w+') as (f):
        f.write(led_1_button_GT)
if not searchFile('2_button_', './hub_led/button_led'):
    with open('./hub_led/button_led/2_button_F1.cfg', 'w+') as (f):
        f.write(led_2_button_F1)
if not searchFile('3_button_', './hub_led/button_led'):
    with open('./hub_led/button_led/3_button_STREET CAR.cfg', 'w+') as (f):
        f.write(led_3_button_STREET)
if not searchFile('4_button_', './hub_led/button_led'):
    with open('./hub_led/button_led/4_button_TRUCK.cfg', 'w+') as (f):
        f.write(led_4_button_TRUCK)
if not searchFile('5_button_', './hub_led/button_led'):
    with open('./hub_led/button_led/5_button_BLUE.cfg', 'w+') as (f):
        f.write(led_5_button_BLUE)
if not searchFile('6_button_', './hub_led/button_led'):
    with open('./hub_led/button_led/6_button_PINK.cfg', 'w+') as (f):
        f.write(led_6_button_PINK)
if not searchFile('7_button_', './hub_led/button_led'):
    with open('./hub_led/button_led/7_button_YELLOW.cfg', 'w+') as (f):
        f.write(led_7_button_YELLOW)
if not searchFile('8_button_', './hub_led/button_led'):
    with open('./hub_led/button_led/8_button_ORGANGE.cfg', 'w+') as (f):
        f.write(led_8_button_ORGANGE)
if not searchFile('9_button_', './hub_led/button_led'):
    with open('./hub_led/button_led/9_button_GREEN.cfg', 'w+') as (f):
        f.write(led_9_button_GREEN)
if not searchFile('10_button_', './hub_led/button_led'):
    with open('./hub_led/button_led/10_button_COLORFUL.cfg', 'w+') as (f):
        f.write(led_10_button_COLORFUL)
if not os.path.exists('hub_led/rpm_led'):
    os.makedirs('hub_led/rpm_led')
if not searchFile('1_rpm_', './hub_led/rpm_led'):
    with open('./hub_led/rpm_led/1_rpm_GT.cfg', 'w+') as (f):
        f.write(led_1_rpm_GT)
if not searchFile('2_rpm_', './hub_led/rpm_led'):
    with open('./hub_led/rpm_led/2_rpm_F1.cfg', 'w+') as (f):
        f.write(led_2_rpm_F1)
if not searchFile('3_rpm_', './hub_led/rpm_led'):
    with open('./hub_led/rpm_led/3_rpm_STREET CAR.cfg', 'w+') as (f):
        f.write(led_3_rpm_STREET)
if not searchFile('4_rpm_', './hub_led/rpm_led'):
    with open('./hub_led/rpm_led/4_rpm_TRUCK.cfg', 'w+') as (f):
        f.write(led_4_rpm_TRUCK)
if not searchFile('5_rpm_', './hub_led/rpm_led'):
    with open('./hub_led/rpm_led/5_rpm_DRIFT.cfg', 'w+') as (f):
        f.write(led_5_rpm_DRIFT)
if not searchFile('6_rpm_', './hub_led/rpm_led'):
    with open('./hub_led/rpm_led/6_rpm_RED.cfg', 'w+') as (f):
        f.write(led_6_rpm_RED)
if not searchFile('7_rpm_', './hub_led/rpm_led'):
    with open('./hub_led/rpm_led/7_rpm_GREEN.cfg', 'w+') as (f):
        f.write(led_7_rpm_GREEN)
if not searchFile('8_rpm_', './hub_led/rpm_led'):
    with open('./hub_led/rpm_led/8_rpm_WHITE.cfg', 'w+') as (f):
        f.write(led_8_rpm_WHITE)
if not searchFile('9_rpm_', './hub_led/rpm_led'):
    with open('./hub_led/rpm_led/9_rpm_YELLOW.cfg', 'w+') as (f):
        f.write(led_9_rpm_YELLOW)
if not searchFile('10_rpm_', './hub_led/rpm_led'):
    with open('./hub_led/rpm_led/10_rpm_CYAN BLUE.cfg', 'w+') as (f):
        f.write(led_10_rpm_CYAN_BLUE)
rpm_led_files = os.listdir('./hub_led/rpm_led')
button_led_files = os.listdir('./hub_led/button_led')
for rpm_setting, button_setting in zip(rpm_led_files, button_led_files):
    new_rpm_name = rpm_setting[6:]
    new_button_name = button_setting[0:9] + new_rpm_name
    os.rename('./hub_led/button_led/' + button_setting, './hub_led/button_led/' + new_button_name)

if not os.path.exists('preset'):
    os.makedirs('preset')
    with open('./preset/AC.cfg', 'w+') as (f):
        f.write(AC)
    with open('./preset/ACC.cfg', 'w+') as (f):
        f.write(ACC)
    with open('./preset/DiRT RALLY 2.0.cfg', 'w+') as (f):
        f.write(DR2)
    with open('./preset/DiRT RALLY.cfg', 'w+') as (f):
        f.write(DR)
    with open('./preset/DiRT 4.cfg', 'w+') as (f):
        f.write(DR4)
    with open('./preset/ETS 2.cfg', 'w+') as (f):
        f.write(ETS2)
    with open('./preset/F1 2018.cfg', 'w+') as (f):
        f.write(F12018)
    with open('./preset/F1 2019.cfg', 'w+') as (f):
        f.write(F12019)
    with open('./preset/F1 2020.cfg', 'w+') as (f):
        f.write(F12020)
    with open('./preset/F1 2021.cfg', 'w+') as (f):
        f.write(F12021)
    with open('./preset/FH4.cfg', 'w+') as (f):
        f.write(FH4)
    with open('./preset/FH4_DRIFT.cfg', 'w+') as (f):
        f.write(FH4_D)
    with open('./preset/iRacing.cfg', 'w+') as (f):
        f.write(IR)
    with open('./preset/LFS DRIFT.cfg', 'w+') as (f):
        f.write(LFSD)
    with open('./preset/LFS.cfg', 'w+') as (f):
        f.write(LFS)
    with open('./preset/PCARS 2.cfg', 'w+') as (f):
        f.write(PCARS2)
    with open('./preset/PCARS.cfg', 'w+') as (f):
        f.write(PCARS)
    with open('./preset/R3E.cfg', 'w+') as (f):
        f.write(R3E)
    with open('./preset/WRC 10.cfg', 'w+') as (f):
        f.write(WRC10)
    with open('./preset/AMS 2.cfg', 'w+') as (f):
        f.write(AMS2)
    with open('./preset/BeamNG.cfg', 'w+') as (f):
        f.write(BeamNG)

def Judge_Key(key_name=None, reg_root=win32con.HKEY_CURRENT_USER, reg_path='SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Run', abspath=None):
    """
        :param key_name: #  要查询的键名
        :param reg_root: # 根节点
                #win32con.HKEY_CURRENT_USER
                #win32con.HKEY_CLASSES_ROOT
                #win32con.HKEY_CURRENT_USER
                #win32con.HKEY_LOCAL_MACHINE
                #win32con.HKEY_USERS
                #win32con.HKEY_CURRENT_CONFIG
        :param reg_path: #  键的路径
        :return:feedback是（0/1/2/3：存在/不存在/权限不足/报错）
        """
    reg_flags = win32con.WRITE_OWNER | win32con.KEY_WOW64_64KEY | win32con.KEY_ALL_ACCESS
    try:
        key = winreg.OpenKey(reg_root, reg_path, 0, reg_flags)
        location, type = winreg.QueryValueEx(key, key_name)
        print('键存在1')
        feedback = 0
        if location != abspath:
            feedback = 1
            print('键存在2')
    except FileNotFoundError as e:
        print('FileNotFoundError')
        feedback = 1
    except PermissionError as e:
        print('PermissionError', e)
        feedback = 2
    except:
        print('JK Error')
        feedback = 3

    return feedback


def AutoRun(switch='open', key_name=None, abspath=os.path.abspath(sys.argv[0])):
    judge_key = Judge_Key(reg_root=(win32con.HKEY_CURRENT_USER), reg_path='Software\\Microsoft\\Windows\\CurrentVersion\\Run',
      key_name=key_name,
      abspath=abspath)
    KeyName = 'Software\\Microsoft\\Windows\\CurrentVersion\\Run'
    key = win32api.RegOpenKey(win32con.HKEY_CURRENT_USER, KeyName, 0, win32con.KEY_ALL_ACCESS)
    if switch == 'open':
        try:
            if judge_key == 0:
                print('已经开启了，无需再开启')
            else:
                if judge_key == 1:
                    win32api.RegSetValueEx(key, key_name, 0, win32con.REG_SZ, abspath)
                    win32api.RegCloseKey(key)
                    print('开机自启动添加成功！')
        except:
            print('添加失败')

    if switch == 'close':
        try:
            if judge_key == 0:
                win32api.RegDeleteValue(key, key_name)
                win32api.RegCloseKey(key)
                print('成功删除键！')
            else:
                if judge_key == 1:
                    print('键不存在')
                else:
                    if judge_key == 2:
                        print('权限不足')
                    else:
                        print('出现错误')
        except:
            print('删除失败')


class MyLabel(QLabel):

    def __init__(self, parent, pix):
        QLabel.__init__(self, parent)
        self.painter = QPainter()
        self.pix = pix
        self.angle = 0

    def setAngle(self, angle):
        self.angle = angle
        self.update()

    def paintEvent(self, event):
        super().paintEvent(event)
        self.painter.begin(self)
        self.painter.setRenderHint(QPainter.SmoothPixmapTransform)
        self.painter.translate(50, 50)
        self.painter.rotate(self.angle)
        self.painter.translate(-50, -50)
        self.painter.drawPixmap(0, 0, 100, 100, self.pix)
        self.painter.end()


ui_cfg = configparser.ConfigParser()
ui_cfg.read('./cfg/ui_setting.cfg')
ui_size = ui_cfg.get('menu', 'ui')
font_size = ui_cfg.get('menu', 'font')
if 'fh5' not in ui_cfg:
    ui_cfg.add_section('fh5')
    ui_cfg.set('fh5', 'tele_enable', 'True')
    ui_cfg.set('fh5', 't_ffb', 'True')
    ui_cfg.set('fh5', 'ip', '0.0.0.0')
    ui_cfg.set('fh5', 'port', '1111')
    with open('./cfg/ui_setting.cfg', 'w+') as (f):
        ui_cfg.write(f)
if 'ams2' not in ui_cfg:
    ui_cfg.add_section('ams2')
    ui_cfg.set('ams2', 'tele_enable', 'True')
    ui_cfg.set('ams2', 't_ffb', 'True')
    with open('./cfg/ui_setting.cfg', 'w+') as (f):
        ui_cfg.write(f)
if ui_size == 'S':
    ui_size = 1
else:
    if ui_size == 'M':
        ui_size = 1.333
    else:
        if ui_size == 'L':
            ui_size = 1.666
        if font_size == 'S':
            font_size = 1.15
        else:
            if font_size == 'M':
                font_size = 1.35
            elif font_size == 'L':
                font_size = 1.55
style_disconnect = 'QPushButton{\nbackground-color: rgb(255, 50, 50);\nborder-radius: 5px;\n}'
style_connected = 'QPushButton{\nbackground-color: rgb(50, 255, 50);\nborder-radius: 5px;\n}'
style_wireless_connected = 'QPushButton{\nbackground-color: rgb(0, 175, 255);\nborder-radius: 5px;\n}'
style_update = 'QPushButton{\nbackground-color: rgb(255, 255, 0);\nborder-radius: 5px;\n}'
style_ps4 = 'QPushButton{\nbackground-color: rgb(33, 65, 177);\nborder-radius: 5px;\n}'

class LanguageChooser(QObject):
    language_change = pyqtSignal(str)

    def __init__(self):
        super(LanguageChooser, self).__init__()
        self.language = ui_cfg.get('menu', 'language')

    def setLanguage(self, language_str):
        self.language = language_str
        self.language_change.emit(language_str)


language_chooser = LanguageChooser()
from enum import Enum

class Direction(Enum):
    Left = 0
    Right = 1
    Up = 2
    Down = 3


class Joystick(QWidget):

    def __init__(self, parent=None):
        super(Joystick, self).__init__(parent)
        self.setMinimumSize(110, 110)
        self.setMaximumSize(110, 110)
        self.movingOffset = QPointF(0, 0)
        self.grabCenter = True
        self._Joystick__maxDistance = 40
        self.setPos(55, 55)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        bounds = QRectF(-self._Joystick__maxDistance, -self._Joystick__maxDistance, self._Joystick__maxDistance * 2, self._Joystick__maxDistance * 2).translated(self._center())
        painter.setPen(QPen(QColor(130, 130, 130), 3))
        painter.drawEllipse(bounds)
        painter.setBrush(QColor(255, 187, 57))
        painter.setPen(QColor(255, 187, 57))
        painter.drawEllipse(self._centerEllipse())

    def _centerEllipse(self):
        if self.grabCenter:
            return QRectF(-10, -10, 20, 20).translated(self.movingOffset)
        else:
            return QRectF(-10, -10, 20, 20).translated(self._center())

    def _center(self):
        return QPointF(self.width() / 2, self.height() / 2)

    def _boundJoystick(self, point):
        limitLine = QLineF(self._center(), point)
        if limitLine.length() > self._Joystick__maxDistance:
            limitLine.setLength(self._Joystick__maxDistance)
        return limitLine.p2()

    def setPos(self, x, y):
        self.movingOffset = self._boundJoystick(QPointF(x, y))
        self.update()


class MainBaseUi(QMainWindow, BaseUi):
    addNewCfg = pyqtSignal(str)
    renameCfg = pyqtSignal(str)

    def __init__(self, mainWnd, hidchooser, hub_hidchooser, dashchooser):
        super(MainBaseUi, self).__init__()
        self.setupUi(self)
        self.reFontSize()
        self.type = 'base'
        self.x_mode_num = 0
        self.pc_mode_num = 0
        self.last_dev_key = ''
        for i in range(15):
            item = self.ch_comboBox.model().item(i)
            item.setForeground(QColor(255, 187, 57))

        self.changeLanguage(language_chooser.language)
        language_chooser.language_change.connect(lambda val: self.changeLanguage(val))
        self.mainWnd = mainWnd
        self.base_enc_align_pushButton.setVisible(False)
        self.lock_checkBox.setVisible(False)
        self.system_voltage_Label.setVisible(False)
        self.encrypted_checkBox.setVisible(False)
        self.ffb_strength_label.setVisible(False)
        self.FF_Global_strength_Slider.setVisible(False)
        self.FF_Global_strength_Value.setVisible(False)
        self.response_label.setVisible(False)
        self.FF_Response_Slider.setVisible(False)
        self.FF_Response_Value.setVisible(False)
        self.force_filter_label.setVisible(False)
        self.FF_Filter_Slider.setVisible(False)
        self.FF_Filter_Value.setVisible(False)
        self.base_test_torque_Slider.setVisible(False)
        self.base_test_torque_Value.setVisible(False)
        self.general_help_pushButton.setVisible(False)
        self.ffb_cfg_comboBox.wheelEvent = self.disWheel
        self.current_running_game = 'None'
        self.base_update_refresh_pushButton.clicked.connect(lambda : self.fw_path_lineEdit.setText(''))
        self.hidchooser = hidchooser
        self.hub_hidchooser = hub_hidchooser
        self.dashchooser = dashchooser
        self.settingchooser = setting_ui.SettingChooser(hidchooser=(self.hidchooser), main=self)
        self.setDefaultFromCfg()
        self.axisLineEditConnect()
        self.mode_checkBox.toggled.connect(lambda val: self.setBaseMode())
        self.fw_boot_path_lineEdit.setVisible(False)
        self.fw_boot_select_pushButton.setVisible(False)
        self.fw_path_lineEdit.setVisible(False)
        self.fw_select_pushButton.clicked.connect(lambda : self.selectDir('Please select the firmware', self.fw_path_lineEdit))
        self.fw_boot_select_pushButton.clicked.connect(lambda : self.selectBootDir('Please select the firmware', self.fw_boot_path_lineEdit))
        self.base_fw_desc_scrollArea.setVisible(False)
        self.base_add_cfg_pushButton.clicked.connect(lambda : self.openNewRenameDialog('new'))
        self.base_del_cfg_pushButton.clicked.connect(self.deleteFFBCfg)
        self.base_rename_cfg_pushButton.clicked.connect(lambda : self.openNewRenameDialog('rename'))
        self.base_copy_cfg_pushButton.clicked.connect(lambda : self.copyFFBCfg())
        self.base_paste_cfg_pushButton.clicked.connect(lambda : self.pasteFFBCfg())
        self.link_pushButton.clicked.connect(lambda : self.setAutoSetting(True))
        self.unlink_pushButton.clicked.connect(lambda : self.setAutoSetting(False))
        self.autosetting_checkBox.toggled.connect(lambda val: self.autosettingEnable(val))
        self.base_enc_align_pushButton.clicked.connect(lambda val: self.hidchooser.sent_handler(SETTING_ENCODER_ALIGN))
        self.ffb_cfg_comboBox.currentTextChanged.connect(lambda val: self.currentPresetchanged(val))
        self.addNewCfg.connect(lambda val: self.WritePresetToCfg(val, 'new'))
        self.base_angle_range_Slider.valueChanged.connect(lambda : self.WritePresetToCfg(self.ffb_cfg_comboBox.currentText(), 'modify'))
        self.FF_Global_strength_Slider.valueChanged.connect(lambda : self.WritePresetToCfg(self.ffb_cfg_comboBox.currentText(), 'modify'))
        self.FF_Response_Slider.valueChanged.connect(lambda : self.WritePresetToCfg(self.ffb_cfg_comboBox.currentText(), 'modify'))
        self.Detail_Enhancer_Slider.valueChanged.connect(lambda : self.WritePresetToCfg(self.ffb_cfg_comboBox.currentText(), 'modify'))
        self.Speed_Limit_Slider.valueChanged.connect(lambda : self.WritePresetToCfg(self.ffb_cfg_comboBox.currentText(), 'modify'))
        self.FF_Filter_Slider.valueChanged.connect(lambda : self.WritePresetToCfg(self.ffb_cfg_comboBox.currentText(), 'modify'))
        self.FF_Maxtorque_Slider.valueChanged.connect(lambda : self.WritePresetToCfg(self.ffb_cfg_comboBox.currentText(), 'modify'))
        self.Mech_Spring_Slider.valueChanged.connect(lambda : self.WritePresetToCfg(self.ffb_cfg_comboBox.currentText(), 'modify'))
        self.Mech_Friction_Slider.valueChanged.connect(lambda : self.WritePresetToCfg(self.ffb_cfg_comboBox.currentText(), 'modify'))
        self.Mech_Damping_Slider.valueChanged.connect(lambda : self.WritePresetToCfg(self.ffb_cfg_comboBox.currentText(), 'modify'))
        self.Mech_Inertia_Slider.valueChanged.connect(lambda : self.WritePresetToCfg(self.ffb_cfg_comboBox.currentText(), 'modify'))
        self.Dyna_Damping_Slider.valueChanged.connect(lambda : self.WritePresetToCfg(self.ffb_cfg_comboBox.currentText(), 'modify'))
        self.Understeer_Effect_Slider.valueChanged.connect(lambda : self.WritePresetToCfg(self.ffb_cfg_comboBox.currentText(), 'modify'))
        self.FF_Constant_Slider.valueChanged.connect(lambda : self.WritePresetToCfg(self.ffb_cfg_comboBox.currentText(), 'modify'))
        self.FF_Friction_Slider.valueChanged.connect(lambda : self.WritePresetToCfg(self.ffb_cfg_comboBox.currentText(), 'modify'))
        self.FF_Damping_Slider.valueChanged.connect(lambda : self.WritePresetToCfg(self.ffb_cfg_comboBox.currentText(), 'modify'))
        self.FF_Sine_Slider.valueChanged.connect(lambda : self.WritePresetToCfg(self.ffb_cfg_comboBox.currentText(), 'modify'))
        self.FF_Spring_Slider.valueChanged.connect(lambda : self.WritePresetToCfg(self.ffb_cfg_comboBox.currentText(), 'modify'))
        self.device_list = []
        self.dashchooser.gameStatusChange.connect(lambda val: self.AutoSetting(val))
        self.autosetting_checkBox.clicked.connect(lambda val: self.AutoSetting(self.current_running_game))
        self.hidchooser.connectStatusChange.connect(lambda val: self.updataStatus(val))
        self.hidchooser.usbHubStatusChange.connect(lambda device, port: self.usb_hub_updata(device, port))
        self.steeringchooser = steering_ui.SteeringChooser(hidchooser=(self.hidchooser), main=self, language_chooser=language_chooser)
        self.additionalchooser = additional_ui.AdditionalChooser(hidchooser=(self.hidchooser), main=self, language_chooser=language_chooser)
        self.axischooser = axis_ui.AxisChooser(hidchooser=(self.hidchooser), main=self)
        self.base_system_page_radioButton.clicked.connect(lambda val: self.base_stackedWidget.setCurrentIndex(0))
        self.base_ffb_page_radioButton.clicked.connect(lambda val: self.base_stackedWidget.setCurrentIndex(1))
        self.base_additional_page_radioButton.clicked.connect(lambda val: self.base_stackedWidget.setCurrentIndex(2))
        self.base_update_pushButton.clicked.connect(lambda : self.openUpdateFwDialog(1))
        self.base_update_boot_pushButton.clicked.connect(lambda : self.openUpdateFwDialog(2))
        self.autosetting_help_pushButton.clicked.connect(lambda val: self.openHelp('AUTOSETTING'))
        self.general_help_pushButton.clicked.connect(lambda val: self.openHelp('General'))
        self.ffb_help_pushButton.clicked.connect(lambda val: self.openHelp('FFB'))
        self.wireless_help_pushButton.clicked.connect(lambda val: self.openHelp('Wireless'))
        self.lock_checkBox.clicked.connect(lambda val: self.lock(val))
        chart = DynamicLine(self.hidchooser, self)
        chart.setBackgroundVisible(False)
        chart.setBackgroundBrush(QColor(0, 255, 255))
        chart.legend().hide()
        view = QChartView(chart)
        view.setRenderHint(QPainter.Antialiasing)
        self.torque_curve_gridLayout.addWidget(view)
        chart1 = DynamicLine(self.hidchooser, self)
        chart1.setBackgroundVisible(False)
        chart1.setBackgroundBrush(QColor(0, 255, 255))
        chart1.legend().hide()
        view1 = QChartView(chart1)
        view1.setDragMode(QGraphicsView.RubberBandDrag)
        view1.setMouseTracking(True)
        view1.setRenderHint(QPainter.Antialiasing)
        self.gridLayout_16.addWidget(view1)
        self.gridLayout_21.addWidget(view1)
        self.gridLayout_19.addWidget(view1)
        self.reset_mode_key_thread = Refresher(5)
        self.reset_mode_key_thread.sinOut.connect(self.reset_mode_key)
        self.reset_mode_key_thread.start()

    def lock(self, val):
        self.base_ffb_page_radioButton.setVisible(not val)

    def selectDir(self, str, lineEdit):
        filePath = QFileDialog.getOpenFileName(self, str, '', 'Bin files(*.bin)')[0]
        if filePath != '':
            lineEdit.setText(filePath)
            self.base_update_pushButton.setEnabled(True)
            self.fw_path_lineEdit.setVisible(True)

    def selectBootDir(self, str, lineEdit):
        filePath = QFileDialog.getOpenFileName(self, str, '', 'Bin files(*.bin)')[0]
        if filePath != '':
            lineEdit.setText(filePath)
            self.base_update_boot_pushButton.setEnabled(True)

    def copyFFBCfg(self):
        preset_name, _, _ = self.ffb_cfg_comboBox.currentText().partition(' - ')
        angle_range = self.base_angle_range_Slider2.value()
        angle_range_auto = self.range_auto_radioButton2.isChecked()
        max_torque = self.FF_Maxtorque_Slider.value()
        strength = self.FF_Global_strength_Slider.value()
        speed_limit = self.Speed_Limit_Slider.value()
        detail_enhance = self.Detail_Enhancer_Slider.value()
        center_spring = self.Mech_Spring_Slider.value()
        inh_friction = self.Mech_Friction_Slider.value()
        inh_damping = self.Mech_Damping_Slider.value()
        inh_inertia = self.Mech_Inertia_Slider.value()
        endstop_strength = self.Mech_Endstop_Slider.value()
        understeer = self.Understeer_Effect_Slider.value()
        dyna_damping = self.Dyna_Damping_Slider.value()
        ffb_constant = self.FF_Constant_Slider.value()
        ffb_friction = self.FF_Friction_Slider.value()
        ffb_damping = self.FF_Damping_Slider.value()
        ffb_sine = self.FF_Sine_Slider.value()
        ffb_spring = self.FF_Spring_Slider.value()
        text = [
         'IMMSOURCE_FFB_CFG', preset_name, angle_range, str(angle_range_auto), max_torque, strength, speed_limit, detail_enhance, center_spring, inh_friction, inh_damping, inh_inertia, endstop_strength, understeer,
         dyna_damping, ffb_constant, ffb_friction, ffb_damping, ffb_sine, ffb_spring]
        pyperclip.copy(str(text))

    def pasteFFBCfg(self):
        try:
            text = eval(pyperclip.paste())
            if isinstance(text, list) and len(text) == 20 and text[0] == 'IMMSOURCE_FFB_CFG':
                print(text)
                enter_name = text[1].strip()
                if self.ffb_cfg_comboBox.findText(enter_name, QtCore.Qt.MatchFixedString) != -1:
                    for i in range(1, 100):
                        enter_name = text[1].strip() + '_copy' + str(i)
                        if self.ffb_cfg_comboBox.findText(enter_name, QtCore.Qt.MatchFixedString) == -1:
                            break

                perset_dir = './preset/' + enter_name + '.cfg'
                with open(perset_dir, 'w+') as (f):
                    pass
                self.addNewCfg.emit(enter_name)
                self.base_angle_range_Slider2.setValue(text[2])
                self.range_auto_radioButton2.setChecked(eval(text[3]))
                self.FF_Maxtorque_Slider.setValue(text[4])
                self.FF_Global_strength_Slider.setValue(text[5])
                self.Speed_Limit_Slider.setValue(text[6])
                self.Detail_Enhancer_Slider.setValue(text[7])
                self.Mech_Spring_Slider.setValue(text[8])
                self.Mech_Friction_Slider.setValue(text[9])
                self.Mech_Damping_Slider.setValue(text[10])
                self.Mech_Inertia_Slider.setValue(text[11])
                self.Mech_Endstop_Slider.setValue(text[12])
                self.Understeer_Effect_Slider.setValue(text[13])
                self.Dyna_Damping_Slider.setValue(text[14])
                self.FF_Constant_Slider.setValue(text[15])
                self.FF_Friction_Slider.setValue(text[16])
                self.FF_Damping_Slider.setValue(text[17])
                self.FF_Sine_Slider.setValue(text[18])
                self.FF_Spring_Slider.setValue(text[19])
        except Exception as e:
            print('pasteFFBCfg ', e)

    def reset_mode_key(self):
        self.x_mode_num = 0
        self.f_mode_num = 0
        self.pc_mode_num = 0
        self.last_dev_key = ''
        self.mainWnd.titleBar.changeColor(15, 17, 20)

    def setBaseMode(self):
        if self.hidchooser.usbhidConnected() == CONNECT_STATUS_RUNNING:
            if ' F' in self.base_model_Label.text():
                self.hidchooser.sent_handler(SETTING_MODE, MODE_PC)
                if language_chooser.language == 'zh-cn' or language_chooser.language == 'zh-tc':
                    self.mode_checkBox.setText('正常模式')
                else:
                    self.mode_checkBox.setText('Normal Mode')
            else:
                self.hidchooser.sent_handler(SETTING_MODE, MODE_F)
                if language_chooser.language == 'zh-cn' or language_chooser.language == 'zh-tc':
                    self.mode_checkBox.setText('兼容模式')
                else:
                    self.mode_checkBox.setText('Comp Mode')

    def keyPressEvent(self, e):
        if e.key() == QtCore.Qt.Key_X:
            self.mainWnd.titleBar.changeColor(150, 17, 20)
        else:
            if e.key() == QtCore.Qt.Key_Z:
                self.mainWnd.titleBar.changeColor(150, 17, 20)
            elif e.key() == QtCore.Qt.Key_D:
                self.last_dev_key = 'D'
            else:
                if e.key() == QtCore.Qt.Key_E:
                    if self.last_dev_key == 'D':
                        self.last_dev_key = 'E'
                if e.key() == QtCore.Qt.Key_V:
                    if self.last_dev_key == 'E':
                        self.base_enc_align_pushButton.setVisible(True)
                        self.last_dev_key = ''
            if e.key() == QtCore.Qt.Key_L:
                self.base_ffb_page_radioButton.setVisible(not self.base_ffb_page_radioButton.isVisible())
                self.base_additional_page_radioButton.setVisible(not self.base_additional_page_radioButton.isVisible())

    def keyReleaseEvent(self, e):
        if e.key() == QtCore.Qt.Key_X:
            self.mainWnd.titleBar.changeColor(15, 17, 20)
            if self.hidchooser.usbhidConnected() == CONNECT_STATUS_RUNNING:
                self.x_mode_num = self.x_mode_num + 1
            if self.x_mode_num == 3:
                self.hidchooser.sent_handler(SETTING_MODE, MODE_X)
                self.x_mode_num = 0
        if e.key() == QtCore.Qt.Key_Z:
            self.mainWnd.titleBar.changeColor(15, 17, 20)
            if self.hidchooser.usbhidConnected() == CONNECT_STATUS_RUNNING:
                self.pc_mode_num = self.pc_mode_num + 1
            if self.pc_mode_num == 3:
                self.hidchooser.sent_handler(SETTING_MODE, MODE_PC)
                self.pc_mode_num = 0

    def disWheel(self, QWheelEvent):
        pass

    def changeLanguage(self, language):
        trans = QTranslator()
        trans.load('immbase_' + language + '.qm', ':/translations')
        app = QApplication.instance()
        app.installTranslator(trans)
        self.retranslateUi(self)
        all_w = self.findChildren(QWidget)
        scaleRate = font_size
        if ' F' not in self.base_model_Label.text():
            if language == 'zh-cn' or language == 'zh-tc':
                self.mode_checkBox.setText('正常模式')
            else:
                self.mode_checkBox.setText('Normal Mode')
        else:
            if language == 'zh-cn' or language == 'zh-tc':
                self.mode_checkBox.setText('兼容模式')
            else:
                self.mode_checkBox.setText('Comp Mode')
            if language == 'zh-cn':
                for _w in all_w:
                    if not _w == self.base_model_Label:
                        if _w == self.base_version_Label:
                            pass
                        else:
                            font = _w.font()
                            font.setFamily('Noto Sans SC Medium')
                            _w.setFont(font)

            else:
                if language == 'zh-tc':
                    for _w in all_w:
                        if not _w == self.base_model_Label:
                            if _w == self.base_version_Label:
                                pass
                            else:
                                font = _w.font()
                                font.setFamily('Noto Sans TC Medium')
                                _w.setFont(font)

                else:
                    if language == 'ko':
                        for _w in all_w:
                            if not _w == self.base_model_Label:
                                if _w == self.base_version_Label:
                                    pass
                                else:
                                    font = _w.font()
                                    font.setFamily('Noto Sans KR Medium')
                                    _w.setFont(font)

                    else:
                        if language == 'ja':
                            for _w in all_w:
                                if not _w == self.base_model_Label:
                                    if _w == self.base_version_Label:
                                        pass
                                    else:
                                        font = _w.font()
                                        font.setFamily('Noto Sans JP Medium')
                                        _w.setFont(font)

                        elif language == 'en':
                            for _w in all_w:
                                if not _w == self.base_model_Label:
                                    if _w == self.base_version_Label:
                                        pass
                                    else:
                                        font = _w.font()
                                        font.setFamily('Noto Sans SC Medium')
                                        _w.setFont(font)

    def usb_hub_updata(self, device, id):
        button = eval('self.device_' + str(id) + '_pushButton')
        label = eval('self.device_' + str(id) + '_label')
        device_style = 'QPushButton\n        {\n            border-image: url(:/icon/' + device + '.png);\n            border: 0px solid;\n        }'
        button.setStyleSheet(device_style)
        label.setText(device)

    def openUpdateFwDialog(self, type):
        if self.hidchooser.usbhidConnected() == CONNECT_STATUS_RUNNING or self.hidchooser.usbhidConnected() == CONNECT_STATUS_OTA:
            self.mainWnd.setBlack(True)
            self.updateFwDialog = UpdateFwDialog(self.mainWnd.m_pMask, self.mainWnd, self, self.hidchooser, type)
            self.updateFwDialog.show()

    def openHelp(self, val):
        self.mainWnd.setBlack(True)
        child_win = HelpInfoDialog(self.mainWnd.m_pMask, self.mainWnd, val)
        child_win.show()

    def AutoSetting(self, game):
        self.current_running_game = game
        if self.autosetting_checkBox.isChecked():
            count = self.ffb_cfg_comboBox.count()
            for i in range(count):
                preset_name = self.ffb_cfg_comboBox.itemText(i)
                head, sep, tail = preset_name.partition(' - ')
                preset_game_name = tail
                if game == preset_game_name:
                    self.ffb_cfg_comboBox.setCurrentIndex(i)
                    return

    def reFontSize(self):
        all_w = self.findChildren(QWidget)
        scaleRate = font_size
        for _w in all_w:
            font = _w.font()
            font.setPointSize(font.pointSize() * 1)
            point_size = font.pointSize()
            pixel_size = int(point_size * scaleRate)
            font.setPixelSize(pixel_size)
            if not _w.inherits('QToolBox'):
                _w.setFont(font)

    def autosettingEnable(self, enable):
        self.game_comboBox.setEnabled(enable)
        self.link_pushButton.setEnabled(enable)
        self.unlink_pushButton.setEnabled(enable)
        self.setCfg('menu', 'auto_setting_enable', str(enable))

    def setAutoSetting(self, enable):
        current_preset_name_index = self.ffb_cfg_comboBox.currentIndex()
        current_preset_name_name = self.ffb_cfg_comboBox.currentText()
        if not current_preset_name_name:
            return
        if ' - ' in current_preset_name_name:
            current_preset_name_name = current_preset_name_name[0:current_preset_name_name.find(' - ')]
        else:
            game_name = self.game_comboBox.currentText()
            preset_cfg = configparser.ConfigParser()
            perset_dir = './preset/' + current_preset_name_name + '.cfg'
            preset_cfg.read(perset_dir)
            preset_cfg.set('autosetting', 'enable', str(enable))
            if enable:
                count = self.ffb_cfg_comboBox.count()
                for i in range(count):
                    preset_name = self.ffb_cfg_comboBox.itemText(i)
                    head, sep, tail = preset_name.partition(' - ')
                    preset_name = head
                    preset_game_name = tail
                    if game_name == preset_game_name:
                        self.ffb_cfg_comboBox.setItemText(i, preset_name)
                        item_preset_cfg = configparser.ConfigParser()
                        item_perset_dir = './preset/' + preset_name + '.cfg'
                        print(item_perset_dir)
                        item_preset_cfg.read(item_perset_dir)
                        item_preset_cfg.set('autosetting', 'enable', 'False')
                        item_preset_cfg.set('autosetting', 'game', '')
                        with open(item_perset_dir, 'w+') as (f):
                            item_preset_cfg.write(f)

                preset_cfg.set('autosetting', 'game', game_name)
            with open(perset_dir, 'w+') as (f):
                preset_cfg.write(f)
            if enable:
                self.ffb_cfg_comboBox.setItemText(current_preset_name_index, current_preset_name_name + ' - ' + game_name)
            else:
                self.ffb_cfg_comboBox.setItemText(current_preset_name_index, current_preset_name_name)

    def currentPresetchanged(self, switch_text):
        if switch_text == '':
            return
        if ' - ' in switch_text:
            switch_text = switch_text[0:switch_text.find(' - ')]
        preset_name = switch_text
        self.setCfg('menu', 'current_setting', preset_name)
        perset_dir = './preset/' + preset_name + '.cfg'
        preset_cfg = configparser.ConfigParser()
        preset_cfg.read(perset_dir)
        self.base_angle_range_Slider2.setValue(int(preset_cfg.get('general', 'angle range')))
        self.base_angle_range_Value2.setText(preset_cfg.get('general', 'angle range') + '°')
        self.range_auto_radioButton2.setChecked(eval(preset_cfg.get('general', 'angle auto')))
        self.base_angle_range_Slider.setValue(int(preset_cfg.get('general', 'angle range')))
        self.base_angle_range_Value.setText(preset_cfg.get('general', 'angle range') + '°')
        self.range_auto_radioButton.setChecked(eval(preset_cfg.get('general', 'angle auto')))
        self.FF_Global_strength_Slider.setValue(int(preset_cfg.get('general', 'strenght')))
        self.FF_Response_Slider.setValue(int(preset_cfg.get('general', 'response')))
        self.Speed_Limit_Slider.setValue(int(preset_cfg.get('general', 'speed limit')))
        self.Detail_Enhancer_Slider.setValue(int(preset_cfg.get('general', 'detail enhance')))
        self.FF_Filter_Slider.setValue(int(preset_cfg.get('general', 'filter')))
        self.FF_Maxtorque_Slider.setValue(int(preset_cfg.get('general', 'maxtorque')))
        self.Mech_Spring_Slider.setValue(int(preset_cfg.get('inherent feature', 'spring')))
        self.Mech_Friction_Slider.setValue(int(preset_cfg.get('inherent feature', 'friction')))
        self.Mech_Damping_Slider.setValue(int(preset_cfg.get('inherent feature', 'damping')))
        self.Mech_Inertia_Slider.setValue(int(preset_cfg.get('inherent feature', 'inertia')))
        self.Dyna_Damping_Slider.setValue(int(preset_cfg.get('dynamic feature', 'damping')))
        self.Understeer_Effect_Slider.setValue(int(preset_cfg.get('dynamic feature', 'threshold')))
        self.FF_Constant_Slider.setValue(int(preset_cfg.get('force feedback signal', 'constant')))
        self.FF_Friction_Slider.setValue(int(preset_cfg.get('force feedback signal', 'friction')))
        self.FF_Damping_Slider.setValue(int(preset_cfg.get('force feedback signal', 'damping')))
        self.FF_Sine_Slider.setValue(int(preset_cfg.get('force feedback signal', 'sine')))
        self.FF_Spring_Slider.setValue(int(preset_cfg.get('force feedback signal', 'spring')))

    def WritePresetToCfg(self, preset_name, type):
        if ' - ' in preset_name:
            preset_name = preset_name[0:preset_name.find(' - ')]
        else:
            if not preset_name:
                return
            preset_cfg = configparser.ConfigParser()
            perset_dir = './preset/' + preset_name + '.cfg'
            preset_cfg.read(perset_dir)
            if type == 'new':
                preset_cfg.add_section('setting')
                preset_cfg.add_section('autosetting')
                preset_cfg.add_section('general')
                preset_cfg.add_section('inherent feature')
                preset_cfg.add_section('dynamic feature')
                preset_cfg.add_section('force feedback signal')
                preset_cfg.set('autosetting', 'enable', 'False')
                preset_cfg.set('autosetting', 'game', '')
            preset_cfg.set('general', 'angle range', str(self.base_angle_range_Slider2.value()))
            preset_cfg.set('general', 'angle auto', str(self.range_auto_radioButton2.isChecked()))
            preset_cfg.set('general', 'strenght', str(self.FF_Global_strength_Slider.value()))
            preset_cfg.set('general', 'response', str(self.FF_Response_Slider.value()))
            preset_cfg.set('general', 'speed limit', str(self.Speed_Limit_Slider.value()))
            preset_cfg.set('general', 'detail enhance', str(self.Detail_Enhancer_Slider.value()))
            preset_cfg.set('general', 'filter', str(self.FF_Filter_Slider.value()))
            preset_cfg.set('general', 'maxtorque', str(self.FF_Maxtorque_Slider.value()))
            preset_cfg.set('inherent feature', 'spring', str(self.Mech_Spring_Slider.value()))
            preset_cfg.set('inherent feature', 'friction', str(self.Mech_Friction_Slider.value()))
            preset_cfg.set('inherent feature', 'damping', str(self.Mech_Damping_Slider.value()))
            preset_cfg.set('inherent feature', 'inertia', str(self.Mech_Inertia_Slider.value()))
            preset_cfg.set('dynamic feature', 'damping', str(self.Dyna_Damping_Slider.value()))
            preset_cfg.set('dynamic feature', 'threshold', str(self.Understeer_Effect_Slider.value()))
            preset_cfg.set('force feedback signal', 'constant', str(self.FF_Constant_Slider.value()))
            preset_cfg.set('force feedback signal', 'friction', str(self.FF_Friction_Slider.value()))
            preset_cfg.set('force feedback signal', 'damping', str(self.FF_Damping_Slider.value()))
            preset_cfg.set('force feedback signal', 'sine', str(self.FF_Sine_Slider.value()))
            preset_cfg.set('force feedback signal', 'spring', str(self.FF_Spring_Slider.value()))
            with open(perset_dir, 'w+') as (f):
                preset_cfg.write(f)
            if type == 'new':
                self.ffb_cfg_comboBox.addItem(preset_name)
                self.ffb_cfg_comboBox.setCurrentText(preset_name)

    def openNewRenameDialog(self, type):
        self.mainWnd.setBlack(True)
        child_win = BaseNewRenameCfgDialog(self, self.mainWnd.m_pMask, self.ffb_cfg_comboBox, self.mainWnd, type)
        child_win.show()

    def deleteFFBCfg(self):
        current_index = self.ffb_cfg_comboBox.currentIndex()
        current_text = self.ffb_cfg_comboBox.currentText()
        if ' - ' in current_text:
            current_text = current_text[0:current_text.find(' - ')]
        self.ffb_cfg_comboBox.removeItem(current_index)
        perset_dir = './preset/' + current_text + '.cfg'
        os.remove(perset_dir)

    def axisLineEditConnect(self):
        self.A1_lineEdit.editingFinished.connect(lambda : self.setCfg('axis_name', 'axis1', self.A1_lineEdit.text()))
        self.A2_lineEdit.editingFinished.connect(lambda : self.setCfg('axis_name', 'axis2', self.A2_lineEdit.text()))
        self.A3_lineEdit.editingFinished.connect(lambda : self.setCfg('axis_name', 'axis3', self.A3_lineEdit.text()))
        self.A4_lineEdit.editingFinished.connect(lambda : self.setCfg('axis_name', 'axis4', self.A4_lineEdit.text()))
        self.A5_lineEdit.editingFinished.connect(lambda : self.setCfg('axis_name', 'axis5', self.A5_lineEdit.text()))
        self.A6_lineEdit.editingFinished.connect(lambda : self.setCfg('axis_name', 'axis6', self.A6_lineEdit.text()))
        self.A7_lineEdit.editingFinished.connect(lambda : self.setCfg('axis_name', 'axis7', self.A7_lineEdit.text()))

    def setCfg(self, sec, opt, val):
        ui_cfg.set(sec, opt, val)
        with open('./cfg/ui_setting.cfg', 'w+') as (f):
            ui_cfg.write(f)

    def setDefaultFromCfg(self):
        a1_name = ui_cfg.get('axis_name', 'axis1')
        a2_name = ui_cfg.get('axis_name', 'axis2')
        a3_name = ui_cfg.get('axis_name', 'axis3')
        a4_name = ui_cfg.get('axis_name', 'axis4')
        a5_name = ui_cfg.get('axis_name', 'axis5')
        a6_name = ui_cfg.get('axis_name', 'axis6')
        a7_name = ui_cfg.get('axis_name', 'axis7')
        self.A1_lineEdit.setText(a1_name)
        self.A2_lineEdit.setText(a2_name)
        self.A3_lineEdit.setText(a3_name)
        self.A4_lineEdit.setText(a4_name)
        self.A5_lineEdit.setText(a5_name)
        self.A6_lineEdit.setText(a6_name)
        self.A7_lineEdit.setText(a7_name)
        fileList = os.listdir('./preset')
        for file in fileList:
            try:
                preset_name, extension = os.path.splitext(file)
                if extension == '.cfg':
                    preset_cfg = configparser.ConfigParser()
                    perset_dir = './preset/' + preset_name + '.cfg'
                    preset_cfg.read(perset_dir)
                    autosetting_enable = preset_cfg.get('autosetting', 'enable')
                    game = preset_cfg.get('autosetting', 'game')
                    if autosetting_enable == 'True':
                        preset_name = preset_name + ' - ' + game
                    self.ffb_cfg_comboBox.addItem(preset_name)
                    if self.dyna_feature_checkBox.isChecked():
                        self.game_comboBox.setEnabled(True)
                        self.link_pushButton.setEnabled(True)
                        self.unlink_pushButton.setEnabled(True)
                    else:
                        self.game_comboBox.setEnabled(False)
                        self.link_pushButton.setEnabled(False)
                        self.unlink_pushButton.setEnabled(False)
            except:
                pass

        settinged_preset_name = ui_cfg.get('menu', 'current_setting')
        count = self.ffb_cfg_comboBox.count()
        for i in range(count):
            preset_name = self.ffb_cfg_comboBox.itemText(i)
            head, sep, tail = preset_name.partition(' - ')
            preset_game_name = tail
            if settinged_preset_name == head:
                self.ffb_cfg_comboBox.setCurrentIndex(i)
                self.currentPresetchanged(preset_name)
                break

        game_autosetting = ui_cfg.get('menu', 'auto_setting_enable')
        self.autosetting_checkBox.setChecked(eval(game_autosetting))
        self.game_comboBox.setEnabled(eval(game_autosetting))
        self.link_pushButton.setEnabled(eval(game_autosetting))
        self.unlink_pushButton.setEnabled(eval(game_autosetting))

    def refreshDPI(self):

        def get_real_resolution():
            """获取真实的分辨率"""
            hDC = win32gui.GetDC(0)
            w = win32print.GetDeviceCaps(hDC, win32con.DESKTOPHORZRES)
            h = win32print.GetDeviceCaps(hDC, win32con.DESKTOPVERTRES)
            return (w, h)

        def get_screen_size():
            """获取缩放后的分辨率"""
            w = GetSystemMetrics(0)
            h = GetSystemMetrics(1)
            return (w, h)

        real_resolution = get_real_resolution()
        screen_size = get_screen_size()
        screen_scale_rate = round(real_resolution[0] / screen_size[0], 2)

    def updataStatus(self, status):
        if status == CONNECT_STATUS_RUNNING:
            self.connect_status_Label.setStyleSheet(style_connected)
            product_name = self.hidchooser.getHIDProductName()
            release_number = self.hidchooser.getHIDReleaseNumber()
            vid = self.hidchooser.usb_hid.vendor_id
            pid = self.hidchooser.usb_hid.product_id
            base_boot_ver = release_number >> 8
            base_ver = release_number & 255
            base_ver_major = base_ver >> 6
            base_ver_minor = base_ver & 63
            base_boot_ver_major = base_boot_ver >> 6
            base_boot_ver_minor = base_boot_ver & 63
            ver = str(base_ver_major) + '.' + str(base_ver_minor)
            boot_ver = str(base_boot_ver_major) + '.' + str(base_boot_ver_minor)
            if vid == IMMS_BASE_VID:
                if pid == IMMS_BASE_PID:
                    mode = 'ET5'
            if vid == IMMS_BASE_ET3_VID:
                if pid == IMMS_BASE_ET3_PID:
                    mode = 'ET3'
            if vid == IMMS_BASE_X_VID:
                if pid == IMMS_BASE_X_PID:
                    if 'ET5' in product_name:
                        mode = 'ET5 X'
            if vid == IMMS_BASE_F_VID:
                if pid == IMMS_BASE_F_PID:
                    if 'ET5' in product_name:
                        mode = 'ET5 F'
            if vid == IMMS_BASE_X_VID:
                if pid == IMMS_BASE_X_PID:
                    if 'ET3' in product_name:
                        mode = 'ET3 X'
            if vid == IMMS_BASE_F_VID:
                if pid == IMMS_BASE_F_PID:
                    if 'ET3' in product_name:
                        mode = 'ET3 F'
                    else:
                        mode = 'N/A'
                else:
                    self.mode_checkBox.toggled.disconnect()
                    if ' F' in mode:
                        self.mode_checkBox.setChecked(True)
                        if language_chooser.language == 'zh-cn' or language_chooser.language == 'zh-tc':
                            self.mode_checkBox.setText('兼容模式')
                        else:
                            self.mode_checkBox.setText('Comp Mode')
                    else:
                        self.mode_checkBox.setChecked(False)
                        if language_chooser.language == 'zh-cn' or language_chooser.language == 'zh-tc':
                            self.mode_checkBox.setText('正常模式')
                        else:
                            self.mode_checkBox.setText('Normal Mode')
                self.mode_checkBox.toggled.connect(lambda val: self.setBaseMode())
            else:
                if status == CONNECT_STATUS_OTA:
                    self.connect_status_Label.setStyleSheet(style_update)
                    product_name = self.hidchooser.getHIDProductName()
                    release_number = self.hidchooser.usb_hid.release_number
                    vid = self.hidchooser.usb_hid.vendor_id
                    pid = self.hidchooser.usb_hid.product_id
                    base_boot_ver = release_number >> 8
                    base_ver = release_number & 255
                    base_ver_major = base_ver >> 6
                    base_ver_minor = base_ver & 63
                    base_boot_ver_major = base_boot_ver >> 6
                    base_boot_ver_minor = base_boot_ver & 63
                    ver = str(base_ver_major) + '.' + str(base_ver_minor)
                    boot_ver = str(base_boot_ver_major) + '.' + str(base_boot_ver_minor)
                    if vid == IMMS_BASE_UPDATA_VID:
                        if pid == IMMS_BASE_UPDATA_PID:
                            mode = 'ET5'
                    elif vid == IMMS_BASE_ET3_UPDATA_VID:
                        if pid == IMMS_BASE_ET3_UPDATA_PID:
                            mode = 'ET3'
                    else:
                        mode = 'N/A'
                elif status == CONNECT_STATUS_PS4:
                    self.connect_status_Label.setStyleSheet(style_ps4)
                    product_name = self.hidchooser.getHIDProductName()
                    release_number = self.hidchooser.usb_hid.release_number
                    vid = self.hidchooser.usb_hid.vendor_id
                    pid = self.hidchooser.usb_hid.product_id
                    base_boot_ver = release_number >> 8
                    base_ver = release_number & 255
                    base_ver_major = base_ver >> 6
                    base_ver_minor = base_ver & 63
                    base_boot_ver_major = base_boot_ver >> 6
                    base_boot_ver_minor = base_boot_ver & 63
                    ver = str(base_ver_major) + '.' + str(base_ver_minor)
                    boot_ver = str(base_boot_ver_major) + '.' + str(base_boot_ver_minor)
                    if vid == IMMS_BASE_PS4_VID:
                        if pid == IMMS_BASE_PS4_PID and 'ET5' in product_name:
                            mode = 'ET5 PS4'
                elif vid == IMMS_BASE_PS4_VID:
                    if pid == IMMS_BASE_PS4_PID:
                        if 'ET3' in product_name:
                            mode = 'ET3 PS4'
                else:
                    mode = 'N/A'
        else:
            if status == CONNECT_STATUS_FAULT:
                self.connect_status_Label.setStyleSheet(style_disconnect)
                ver = 'N/A'
                boot_ver = 'N/A'
                mode = 'N/A'
        if mode == 'ET3' or mode == 'ET3 X' or mode == 'ET3 F' or mode == 'ET3 PS4':
            self.FF_Maxtorque_Slider.setMaximum(100)
        else:
            if mode == 'ET5' or mode == 'ET5 X' or mode == 'ET5 X' or mode == 'ET5 PS4':
                self.FF_Maxtorque_Slider.setMaximum(170)
        self.base_model_Label.setText(mode)
        self.update_model_Label.setText(mode)
        self.base_version_Label.setText(ver)
        self.update_version_Label.setText(ver)
        self.update_boot_version_Label.setText(boot_ver)

    def tr_chinese(self):
        trans = QTranslator()
        trans.load('zh_CN.qm')
        app = QApplication.instance()
        app.installTranslator(trans)
        self.retranslateUi(self)
        self.action_chinese.setChecked(True)
        self.action_english.setChecked(False)
        self.cf.set('language', 'type', 'zh_CN')
        with open('./cfg/setting.cfg', 'w+') as (f):
            self.cf.write(f)

    def tr_english(self):
        trans = QTranslator()
        trans.load('en.qm')
        app = QApplication.instance()
        app.installTranslator(trans)
        self.retranslateUi(self)
        self.action_english.setChecked(True)
        self.action_chinese.setChecked(False)
        self.cf.set('language', 'type', 'en')
        with open('./cfg/setting.cfg', 'w+') as (f):
            self.cf.write(f)


class CalibrateGearDialog(QDialog, GearCalibrateDialogUi):

    def __init__(self, base_ui_class=None, parent=None, mainWnd=None, base_hidchooser=None, hub_hidchooser=None):
        super(CalibrateGearDialog, self).__init__(parent)
        self.setupUi(self)
        self.reFontSize()
        self.changeLanguage(language_chooser.language)
        language_chooser.language_change.connect(lambda val: self.changeLanguage(val))
        self.base_ui_class = base_ui_class
        self.parent = parent
        self.base_hidchooser = base_hidchooser
        self.hub_hidchooser = hub_hidchooser
        self.mainWnd = mainWnd
        self.setWindowFlags(QtCore.Qt.WindowCloseButtonHint | QtCore.Qt.FramelessWindowHint)
        self.cancel_pushButton.pressed.connect(self.closeDialog)
        animation = QPropertyAnimation(self, b'windowOpacity', self)
        animation.setDuration(200)
        animation.setStartValue(0)
        animation.setEndValue(1)
        animation2 = QPropertyAnimation(self.mainWnd.m_pMask, b'windowOpacity', self.mainWnd.m_pMask)
        animation2.setDuration(200)
        animation2.setStartValue(0)
        animation2.setEndValue(1)
        animation.start()
        animation2.start()
        parent_globalPos = self.parent.mapToGlobal(QPoint(0, 0))
        self_globalPos = self.mapToGlobal(QPoint(0, 0))
        x = parent_globalPos.x() - self_globalPos.x() + (self.parent.width() - self.width()) / 2
        y = parent_globalPos.y() - self_globalPos.y() + (self.parent.height() - self.height()) / 2
        self.move(x, y)
        self.paddle_pushButton.clicked.connect(self.calibrate_clutch_finish)
        self.joystick_pushButton.clicked.connect(self.calibrate_joy_finish)
        self.x_min = 65535
        self.y_min = 65535
        self.x_max = 0
        self.y_max = 0
        self.left_gear_min = 65535
        self.right_gear_min = 65535
        self.left_gear_max = 0
        self.right_gear_max = 0
        self.left_clutch_min = 65535
        self.right_clutch_min = 65535
        self.left_clutch_max = 0
        self.right_clutch_max = 0
        self.hub_hidchooser.sent_handler(SETTING_START_JOY_CALIBRATE, 0)
        self.hub_hidchooser.sent_handler(SETTING_START_PADDLE_CALIBRATE, 0)
        self.base_hidchooser.sent_handler(SETTING_START_JOY_CALIBRATE, 0)
        self.base_hidchooser.sent_handler(SETTING_START_PADDLE_CALIBRATE, 0)
        self.port_thread = Refresher(0.05)
        self.port_thread.sinOut.connect(self.calibrate)
        self.port_thread.start()

    def changeLanguage(self, language):
        trans = QTranslator()
        trans.load('gear_calibrate_' + language + '.qm', ':/translations')
        app = QApplication.instance()
        app.installTranslator(trans)
        self.retranslateUi(self)
        all_w = self.findChildren(QWidget)
        scaleRate = font_size
        if language == 'zh-cn':
            for _w in all_w:
                font = _w.font()
                font.setFamily('Noto Sans SC Medium')
                _w.setFont(font)

        else:
            if language == 'zh-tc':
                for _w in all_w:
                    font = _w.font()
                    font.setFamily('Noto Sans TC Medium')
                    _w.setFont(font)

            else:
                if language == 'ko':
                    for _w in all_w:
                        font = _w.font()
                        font.setFamily('Noto Sans KR Medium')
                        _w.setFont(font)

                else:
                    if language == 'ja':
                        for _w in all_w:
                            font = _w.font()
                            font.setFamily('Noto Sans JP Medium')
                            _w.setFont(font)

                    elif language == 'en':
                        for _w in all_w:
                            font = _w.font()
                            font.setFamily('Noto Sans SC Medium')
                            _w.setFont(font)

    def calibrate_clutch_finish(self):
        self.hub_hidchooser.sent_handler(SETTING_CLUTACH_CALIBRATE_X_MAX, self.left_clutch_min + 2000)
        self.hub_hidchooser.sent_handler(SETTING_CLUTACH_CALIBRATE_X_MIN, self.left_clutch_max - 2000)
        self.hub_hidchooser.sent_handler(SETTING_CLUTACH_CALIBRATE_Y_MAX, self.right_clutch_min + 2000)
        self.hub_hidchooser.sent_handler(SETTING_CLUTACH_CALIBRATE_Y_MIN, self.right_clutch_max - 2000)
        self.base_hidchooser.sent_handler(SETTING_CLUTACH_CALIBRATE_X_MAX, self.left_clutch_min + 2000)
        self.base_hidchooser.sent_handler(SETTING_CLUTACH_CALIBRATE_X_MIN, self.left_clutch_max - 2000)
        self.base_hidchooser.sent_handler(SETTING_CLUTACH_CALIBRATE_Y_MAX, self.right_clutch_min + 2000)
        self.base_hidchooser.sent_handler(SETTING_CLUTACH_CALIBRATE_Y_MIN, self.right_clutch_max - 2000)
        self.hub_hidchooser.sent_handler(SETTING_GEAR_CALIBRATE_X_MAX, self.left_gear_min + 2000)
        self.hub_hidchooser.sent_handler(SETTING_GEAR_CALIBRATE_X_MIN, self.left_gear_max - 2000)
        self.hub_hidchooser.sent_handler(SETTING_GEAR_CALIBRATE_Y_MAX, self.right_gear_min + 2000)
        self.hub_hidchooser.sent_handler(SETTING_GEAR_CALIBRATE_Y_MIN, self.right_gear_max - 2000)
        self.base_hidchooser.sent_handler(SETTING_GEAR_CALIBRATE_X_MAX, self.left_gear_min + 2000)
        self.base_hidchooser.sent_handler(SETTING_GEAR_CALIBRATE_X_MIN, self.left_gear_max - 2000)
        self.base_hidchooser.sent_handler(SETTING_GEAR_CALIBRATE_Y_MAX, self.right_gear_min + 2000)
        self.base_hidchooser.sent_handler(SETTING_GEAR_CALIBRATE_Y_MIN, self.right_gear_max - 2000)
        self.hub_hidchooser.sent_handler(SETTING_PADDLE_CALIBRATE_FINISH, 0)
        self.base_hidchooser.sent_handler(SETTING_PADDLE_CALIBRATE_FINISH, 0)

    def calibrate_joy_finish(self):
        self.hub_hidchooser.sent_handler(SETTING_JOY_CALIBRATE_X_MIN, self.x_min + 2000)
        self.hub_hidchooser.sent_handler(SETTING_JOY_CALIBRATE_X_MAX, self.x_max - 2000)
        self.hub_hidchooser.sent_handler(SETTING_JOY_CALIBRATE_Y_MIN, self.y_min + 2000)
        self.hub_hidchooser.sent_handler(SETTING_JOY_CALIBRATE_Y_MAX, self.y_max - 2000)
        self.hub_hidchooser.sent_handler(SETTING_JOY_CALIBRATE_FINISH, 0)
        self.base_hidchooser.sent_handler(SETTING_JOY_CALIBRATE_X_MIN, self.x_min + 2000)
        self.base_hidchooser.sent_handler(SETTING_JOY_CALIBRATE_X_MAX, self.x_max - 2000)
        self.base_hidchooser.sent_handler(SETTING_JOY_CALIBRATE_Y_MIN, self.y_min + 2000)
        self.base_hidchooser.sent_handler(SETTING_JOY_CALIBRATE_Y_MAX, self.y_max - 2000)
        self.base_hidchooser.sent_handler(SETTING_JOY_CALIBRATE_FINISH, 0)

    def calibrate(self):
        joy_x = self.hub_hidchooser.y_for_func + 32767
        joy_y = self.hub_hidchooser.x_for_func + 32767
        left_clutch = -(self.hub_hidchooser.rx_for_func - 32767)
        right_clutch = -(self.hub_hidchooser.z_for_func - 32767)
        left_gear = -(self.hub_hidchooser.slider_for_func - 32767)
        right_gear = -(self.hub_hidchooser.rz_for_func - 32767)
        if self.x_min > joy_x:
            self.x_min = joy_x
        if self.y_min > joy_y:
            self.y_min = joy_y
        if self.x_max < joy_x:
            self.x_max = joy_x
        if self.y_max < joy_y:
            self.y_max = joy_y
        self.x_min_label.setText(str(self.x_min))
        self.y_min_label.setText(str(self.y_min))
        self.x_max_label.setText(str(self.x_max))
        self.y_max_label.setText(str(self.y_max))
        if self.left_clutch_min > left_clutch:
            self.left_clutch_min = left_clutch
        if self.right_clutch_min > right_clutch:
            self.right_clutch_min = right_clutch
        if self.left_clutch_max < left_clutch:
            self.left_clutch_max = left_clutch
        if self.right_clutch_max < right_clutch:
            self.right_clutch_max = right_clutch
        self.left_clutch_min_label.setText(str(self.left_clutch_min))
        self.right_clutch_min_label.setText(str(self.right_clutch_min))
        self.left_clutch_max_label.setText(str(self.left_clutch_max))
        self.right_clutch_max_label.setText(str(self.right_clutch_max))
        if self.left_gear_min > left_gear:
            self.left_gear_min = left_gear
        if self.right_gear_min > right_gear:
            self.right_gear_min = right_gear
        if self.left_gear_max < left_gear:
            self.left_gear_max = left_gear
        if self.right_gear_max < right_gear:
            self.right_gear_max = right_gear
        self.left_gear_min_label.setText(str(self.left_gear_min))
        self.right_gear_min_label.setText(str(self.right_gear_min))
        self.left_gear_max_label.setText(str(self.left_gear_max))
        self.right_gear_max_label.setText(str(self.right_gear_max))

    def reFontSize(self):
        all_w = self.findChildren(QWidget)
        scaleRate = font_size
        for _w in all_w:
            font = _w.font()
            font.setPointSize(font.pointSize() * 1)
            point_size = font.pointSize()
            pixel_size = int(point_size * scaleRate)
            font.setPixelSize(pixel_size)
            if not _w.inherits('QToolBox'):
                _w.setFont(font)

    def mousePressEvent(self, event):
        pass

    def ok(self):
        pass

    def closeDialog(self):
        animation = QPropertyAnimation(self, b'windowOpacity', self)
        animation.setDuration(200)
        animation.setStartValue(1)
        animation.setEndValue(0)
        animation2 = QPropertyAnimation(self.mainWnd.m_pMask, b'windowOpacity', self.mainWnd.m_pMask)
        animation2.setDuration(200)
        animation2.setStartValue(1)
        animation2.setEndValue(0)
        animation.finished.connect(self.closeAndBlack)
        animation.start()
        animation2.start()
        self.port_thread.stop()

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Escape:
            pass

    def closeAndBlack(self):
        self.mainWnd.setBlack(False)
        self.close()


class MainHubUi(QMainWindow, HubUi):
    renameCfg = pyqtSignal(str)
    rpmLedChange = pyqtSignal(QObject, str)
    buttonLedChange = pyqtSignal(QObject, str)
    statusLedChange = pyqtSignal(QObject, str)

    def __init__(self, mainWnd, hidchooser, hub_hidchooser, dashchooser, base_ui):
        super(MainHubUi, self).__init__()
        self.setupUi(self)
        self.reFontSize()
        self.gear_calibrate_pushButton.setVisible(False)
        self.enc_zero_pushButton.setVisible(False)
        self.encrypted_checkBox.setVisible(False)
        self.clutch_left_label.setVisible(True)
        self.clutch_right_label.setVisible(True)
        self.hub_left_clutch_progressBar.setVisible(True)
        self.hub_right_clutch_progressBar.setVisible(True)
        self.clutch_label.setVisible(False)
        self.hub_clutch_point_progressBar.setVisible(False)
        self.bite_point_label.setVisible(False)
        self.hub_clutch_point_Slider.setVisible(False)
        self.hub_clutch_point_Value.setVisible(False)
        self.clutch_setting_pushButton_1.setVisible(False)
        self.clutch_setting_pushButton_2.setVisible(False)
        self.clutch_setting_pushButton_3.setVisible(False)
        self.clutch_setting_pushButton_4.setVisible(False)
        self.clutch_setting_pushButton_5.setVisible(False)
        self.clutch_rename_cfg_pushButton.setVisible(False)
        self.fw_boot_path_lineEdit.setVisible(False)
        self.fw_boot_select_pushButton.setVisible(False)
        self.fw_path_lineEdit.setVisible(False)
        self.button_texts = [
         'P', 'SUB', 'L', 'R', 'ADD', 'N', 'ERS', 'DRS', 'K1', 'K2', 'FL1', 'FL2', 'FL3', 'FR1', 'FR2', 'FR3']
        self.dir_up_pushButton.setAttribute(Qt.WA_TransparentForMouseEvents, True)
        self.dir_down_pushButton.setAttribute(Qt.WA_TransparentForMouseEvents, True)
        self.dir_left_pushButton.setAttribute(Qt.WA_TransparentForMouseEvents, True)
        self.dir_right_pushButton.setAttribute(Qt.WA_TransparentForMouseEvents, True)
        self.dir_push_pushButton.setAttribute(Qt.WA_TransparentForMouseEvents, True)
        self.dir_sub_pushButton.setAttribute(Qt.WA_TransparentForMouseEvents, True)
        self.dir_add_pushButton.setAttribute(Qt.WA_TransparentForMouseEvents, True)
        self.type = 'hub'
        self.changeLanguage(language_chooser.language)
        language_chooser.language_change.connect(lambda val: self.changeLanguage(val))
        self.hidchooser = hidchooser
        self.hub_hidchooser = hub_hidchooser
        self.dashchooser = dashchooser
        self.base_ui = base_ui
        self.clutch_axis_mode_radioButton.clicked.connect(lambda val: self.clutchModeChange(0))
        self.clutch_button_mode_radioButton.clicked.connect(lambda val: self.clutchModeChange(0))
        self.clutch_point_mode_radioButton.clicked.connect(lambda val: self.clutchModeChange(1))
        self.hub_clutch_point_Slider.valueChanged.connect(lambda : self.hub_clutch_point_Value.setText(str(self.hub_clutch_point_Slider.value())))
        self.hub_clutch_point_Slider.valueChanged.connect(lambda val: self.write_cfg_hub_clutch_point_Value(val))
        self.clutch_rename_cfg_pushButton.clicked.connect(lambda : self.openNewRenameDialog('clutch_point'))
        self.hub_hidchooser.connectStatusChange.connect(lambda val: self.updataStatus(val))
        self.hubrgbledchooser = hub_rgb_led.HubRgbLedChooser(hidchooser=(self.hub_hidchooser), base_hidchooser=(self.hidchooser), main=self, base_main=(self.base_ui), dash=(self.dashchooser))
        self.hubinputchooser = hub_input.HubInputChooser(hidchooser=(self.hub_hidchooser), base_hidchooser=(self.hidchooser), main=self)
        self.hubadditionalchooser = hub_additional_ui.HubAdditionalChooser(hub_hidchooser=(self.hub_hidchooser), base_hidchooser=(self.hidchooser), main=self, language_chooser=language_chooser)
        self.gear_calibrate_pushButton.clicked.connect(self.openCalibrateGear)
        self.hub_fw_desc_scrollArea.setVisible(False)
        self.fw_select_pushButton.clicked.connect(lambda : self.selectDir('Please select the firmware', self.fw_path_lineEdit))
        self.fw_boot_select_pushButton.clicked.connect(lambda : self.selectBootDir('Please select the firmware', self.fw_boot_path_lineEdit))
        self.mainWnd = mainWnd
        self.hub_system_page_radioButton.clicked.connect(lambda val: self.hub_stackedWidget.setCurrentIndex(0))
        self.hub_led_page_radioButton.clicked.connect(lambda val: self.hub_stackedWidget.setCurrentIndex(1))
        self.hub_additional_page_radioButton.clicked.connect(lambda val: self.hub_stackedWidget.setCurrentIndex(2))
        self.rpm_led_setting_buttonGroup.buttonToggled.connect(lambda val: self.changeRpmLedSetting(val))
        self.rpm_led_setting_buttonGroup.buttonToggled.connect(lambda val: self.changeButtonLedSetting(val))
        self.clutch_setting_buttonGroup.buttonToggled.connect(lambda val: self.changeClutchSetting(val))
        self.hub_rename_cfg_pushButton.clicked.connect(lambda : self.openNewRenameDialog('rpm_led'))
        self.hub_led_brightness_Slider.valueChanged.connect(lambda : self.hub_led_brightness_Value.setText(str(self.hub_led_brightness_Slider.value())))
        self.hub_update_pushButton.clicked.connect(lambda : self.openUpdateFwDialog(1))
        self.hub_update_boot_pushButton.clicked.connect(lambda : self.openUpdateFwDialog(2))
        self.rpmLedChange.connect(lambda val1, val2: self.changeCurrentRpmLedSettingColor(val1, val2))
        self.buttonLedChange.connect(lambda val1, val2: self.changeCurrentButtonLedSettingColor(val1, val2))
        self.Flush_pushButton.clicked.connect(self.changeCurrentRpmLedSetting)
        self.Slider_List = [
         self.L1_verticalSlider, self.L2_verticalSlider, self.L3_verticalSlider, self.L4_verticalSlider, self.L5_verticalSlider,
         self.L6_verticalSlider, self.L7_verticalSlider, self.L8_verticalSlider, self.L9_verticalSlider, self.L10_verticalSlider,
         self.flush_verticalSlider,
         self.hub_led_brightness_Slider]
        self.paddle_help_pushButton.clicked.connect(lambda val: self.openHelp('Paddle'))
        for Slider in self.Slider_List:
            Slider.valueChanged.connect(self.changeCurrentRpmLedSetting)

        self.rpm_led_type_buttonGroup.buttonToggled.connect(self.changeCurrentRpmLedSetting)

        def LambdaCallback1(button):
            return lambda : self.colorSelect(button)

        def LambdaCallback2(button):
            return lambda event: self.rpm_led_WheelEvent(button)

        for i in range(1, 11):
            led_button = eval('self.L' + str(i) + '_pushButton')
            led_button.clicked.connect(LambdaCallback1(led_button))
            led_button.colorIndex = 0
            led_button.wheelEvent = LambdaCallback2(led_button)

        def button_led_LambdaCallback3(button):
            return lambda : self.colorSelect(button, 1)

        def button_led_LambdaCallback4(button):
            return lambda event: self.button_led_WheelEvent(button)

        for button_text in self.button_texts:
            led_button = eval('self.' + button_text + '_pushButton')
            led_button.clicked.connect(button_led_LambdaCallback3(led_button))
            led_button.colorIndex = 0
            led_button.wheelEvent = button_led_LambdaCallback4(led_button)

        def button_led_LambdaCallback1(led_checkbox):
            return lambda val: self.updataEnableBrightnessSetting(led_checkbox)

        def button_led_LambdaCallback2(hub_led_brightness_slider):
            return lambda val: self.updataEnableBrightnessSetting(hub_led_brightness_slider)

        for led_index, button_text in enumerate(self.button_texts):
            led_checkbox = eval('self.' + button_text + '_led_en_checkBox')
            led_checkbox.toggled.connect(button_led_LambdaCallback1(led_checkbox))

        self.Button_led_brightness_Slider.valueChanged.connect(button_led_LambdaCallback2(self.Button_led_brightness_Slider))

        def status_led_LambdaCallback1(button):
            return lambda : self.colorSelect(button, 2)

        def status_led_LambdaCallback2(button):
            return lambda event: self.status_led_WheelEvent(button)

        def status_led_LambdaCallback3(led_en_checkbox):
            return lambda val: self.status_led_en_change_write_cfg(led_en_checkbox)

        status_texts = ['pitlimiter', 'drs', 'drsallowed', 'tc', 'abs', 'greenflag', 'redflag', 'yellowflag', 'blueflag', 'whiteflag', 'blackflag']
        for status_text in status_texts:
            for button_text in self.button_texts:
                led_button = eval('self.' + status_text + '_' + button_text + '_pushButton')
                led_en_checkbox = eval('self.' + status_text + '_en_checkBox')
                led_button.clicked.connect(status_led_LambdaCallback1(led_button))
                led_button.colorIndex = 0
                led_button.wheelEvent = status_led_LambdaCallback2(led_button)
                led_en_checkbox.toggled.connect(status_led_LambdaCallback3(led_en_checkbox))

        self.statusLedChange.connect(lambda val1, val2: self.changeCurrentStatusLedSettingColor(val1, val2))
        self.readClutchSetting()
        self.setDefaultFromCfg()
        self.reset_mode_key_thread = Refresher(5)
        self.reset_mode_key_thread.sinOut.connect(self.reset_mode_key)
        self.reset_mode_key_thread.start()
        self.joy = Joystick()
        self.gridLayout_3.addWidget(self.joy, 1, 0)

    def selectDir(self, str, lineEdit):
        filePath = QFileDialog.getOpenFileName(self, str, '', 'Bin files(*.bin)')[0]
        if filePath != '':
            lineEdit.setText(filePath)
            self.hub_update_pushButton.setEnabled(True)
            self.fw_path_lineEdit.setVisible(True)

    def selectBootDir(self, str, lineEdit):
        filePath = QFileDialog.getOpenFileName(self, str, '', 'Bin files(*.bin)')[0]
        if filePath != '':
            lineEdit.setText(filePath)
            self.hub_update_boot_pushButton.setEnabled(True)

    def reset_mode_key(self):
        self.last_dev_key = ''
        self.mainWnd.titleBar.changeColor(15, 17, 20)

    def keyPressEvent(self, e):
        if e.key() == QtCore.Qt.Key_D:
            self.last_dev_key = 'D'
        else:
            if e.key() == QtCore.Qt.Key_E:
                if self.last_dev_key == 'D':
                    self.last_dev_key = 'E'
            if e.key() == QtCore.Qt.Key_V:
                if self.last_dev_key == 'E':
                    self.paddle_calibrate_pushButton.setVisible(True)
                    self.joy_calibrate_pushButton.setVisible(True)
                    self.enc_zero_pushButton.setVisible(True)
                    self.last_dev_key = ''

    def keyReleaseEvent(self, e):
        if e.key() == QtCore.Qt.Key_D:
            self.mainWnd.titleBar.changeColor(15, 17, 20)
        else:
            if e.key() == QtCore.Qt.Key_E:
                self.mainWnd.titleBar.changeColor(15, 17, 20)
            if e.key() == QtCore.Qt.Key_V:
                self.mainWnd.titleBar.changeColor(15, 17, 20)

    def openHelp(self, val):
        self.mainWnd.setBlack(True)
        child_win = HelpInfoDialog(self.mainWnd.m_pMask, self.mainWnd, val)
        child_win.show()

    def clutchModeChange(self, val):
        if val == 0:
            self.clutch_left_label.setVisible(True)
            self.clutch_right_label.setVisible(True)
            self.hub_left_clutch_progressBar.setVisible(True)
            self.hub_right_clutch_progressBar.setVisible(True)
            self.clutch_label.setVisible(False)
            self.hub_clutch_point_progressBar.setVisible(False)
            self.bite_point_label.setVisible(False)
            self.hub_clutch_point_Slider.setVisible(False)
            self.hub_clutch_point_Value.setVisible(False)
            self.clutch_setting_pushButton_1.setVisible(False)
            self.clutch_setting_pushButton_2.setVisible(False)
            self.clutch_setting_pushButton_3.setVisible(False)
            self.clutch_setting_pushButton_4.setVisible(False)
            self.clutch_setting_pushButton_5.setVisible(False)
            self.clutch_rename_cfg_pushButton.setVisible(False)
        elif val == 1:
            self.clutch_left_label.setVisible(False)
            self.clutch_right_label.setVisible(False)
            self.hub_left_clutch_progressBar.setVisible(False)
            self.hub_right_clutch_progressBar.setVisible(False)
            self.clutch_label.setVisible(True)
            self.hub_clutch_point_progressBar.setVisible(True)
            self.bite_point_label.setVisible(True)
            self.hub_clutch_point_Slider.setVisible(True)
            self.hub_clutch_point_Value.setVisible(True)
            self.clutch_setting_pushButton_1.setVisible(True)
            self.clutch_setting_pushButton_2.setVisible(True)
            self.clutch_setting_pushButton_3.setVisible(True)
            self.clutch_setting_pushButton_4.setVisible(True)
            self.clutch_setting_pushButton_5.setVisible(True)
            self.clutch_rename_cfg_pushButton.setVisible(True)

    def reFontSize(self):
        all_w = self.findChildren(QWidget)
        scaleRate = font_size
        for _w in all_w:
            font = _w.font()
            font.setPointSize(font.pointSize() * 1)
            point_size = font.pointSize()
            pixel_size = int(point_size * scaleRate)
            font.setPixelSize(pixel_size)
            if not _w.inherits('QToolBox'):
                _w.setFont(font)

    def changeLanguage(self, language):
        trans = QTranslator()
        trans.load('immhub_' + language + '.qm', ':/translations')
        app = QApplication.instance()
        app.installTranslator(trans)
        self.retranslateUi(self)
        all_w = self.findChildren(QWidget)
        scaleRate = font_size
        if language == 'zh-cn':
            for _w in all_w:
                if not _w == self.hub_model_Label:
                    if _w == self.hub_version_Label:
                        pass
                    else:
                        font = _w.font()
                        font.setFamily('Noto Sans SC Medium')
                        _w.setFont(font)

        else:
            if language == 'zh-tc':
                for _w in all_w:
                    if not _w == self.hub_model_Label:
                        if _w == self.hub_version_Label:
                            pass
                        else:
                            font = _w.font()
                            font.setFamily('Noto Sans TC Medium')
                            _w.setFont(font)

            else:
                if language == 'ko':
                    for _w in all_w:
                        if not _w == self.hub_model_Label:
                            if _w == self.hub_version_Label:
                                continue
                            font = _w.font()
                            font.setFamily('Noto Sans KR Medium')
                            _w.setFont(font)

                else:
                    if language == 'ja':
                        for _w in all_w:
                            if not _w == self.hub_model_Label:
                                if _w == self.hub_version_Label:
                                    pass
                                else:
                                    font = _w.font()
                                    font.setFamily('Noto Sans JP Medium')
                                    _w.setFont(font)

                    elif language == 'en':
                        for _w in all_w:
                            if not _w == self.hub_model_Label:
                                if _w == self.hub_version_Label:
                                    pass
                                else:
                                    font = _w.font()
                                    font.setFamily('Noto Sans SC Medium')
                                    _w.setFont(font)

    def openUpdateFwDialog(self, type):
        if self.hub_hidchooser.usbhidConnected() == CONNECT_STATUS_RUNNING or self.hub_hidchooser.usbhidConnected() == CONNECT_STATUS_OTA:
            self.mainWnd.setBlack(True)
            self.updateFwDialog = UpdateFwDialog((self.mainWnd.m_pMask), (self.mainWnd), ui_class=self, hidchooser=(self.hub_hidchooser), type=type)
            self.updateFwDialog.show()
        else:
            self.hub_update_info_label.setStyleSheet('QLabel { \ncolor: rgb(255, 20, 20);\n}')
            self.hub_update_pushButton.setEnabled(False)
            if language_chooser.language == 'zh-cn':
                self.hub_update_info_label.setText('请通过USB连接后进行更新')
            else:
                self.hub_update_info_label.setText('Please update after connecting via USB')

    def openNewRenameDialog(self, type):
        self.mainWnd.setBlack(True)
        child_win = HubNewRenameCfgDialog(self, self.mainWnd.m_pMask, self.rpm_led_setting_buttonGroup.checkedButton(), self.mainWnd, type)
        child_win.show()

    def openCalibrateGear(self):
        self.mainWnd.setBlack(True)
        child_win = CalibrateGearDialog(self, self.mainWnd.m_pMask, self.mainWnd, self.hidchooser, self.hub_hidchooser)
        child_win.show()

    def changeCurrentRpmLedSettingColor(self, led_button, color_str):
        current_setting_button = self.rpm_led_setting_buttonGroup.checkedButton()
        rpm_setting_name = current_setting_button.text()[:-1]
        rpm_setting_index = current_setting_button.objectName()[current_setting_button.objectName().rfind('_') + 1:]
        led_index = led_button.objectName()[1:led_button.objectName().find('_')]
        preset_dir = './hub_led/rpm_led/' + str(rpm_setting_index) + '_rpm_' + rpm_setting_name + '.cfg'
        cf = configparser.ConfigParser()
        cf.read(preset_dir)
        cf.set('color', 'led' + str(led_index), color_str)
        with open(preset_dir, 'w+') as (f):
            cf.write(f)

    def changeCurrentStatusLedSettingColor(self, led_button, color_str):
        current_setting_button = self.rpm_led_setting_buttonGroup.checkedButton()
        rpm_setting_name = current_setting_button.text()[:-1]
        rpm_setting_index = current_setting_button.objectName()[current_setting_button.objectName().rfind('_') + 1:]
        status_type = led_button.objectName().split('_')[0]
        status_led = led_button.objectName().split('_')[1]
        preset_dir = './hub_led/button_led/' + str(rpm_setting_index) + '_button_' + rpm_setting_name + '.cfg'
        cf = configparser.ConfigParser()
        cf.read(preset_dir)
        cf.set(status_type, status_led, color_str)
        with open(preset_dir, 'w+') as (f):
            cf.write(f)

    def status_led_en_change_write_cfg(self, checkbox):
        current_setting_button = self.rpm_led_setting_buttonGroup.checkedButton()
        rpm_setting_name = current_setting_button.text()[:-1]
        rpm_setting_index = current_setting_button.objectName()[current_setting_button.objectName().rfind('_') + 1:]
        status_type = checkbox.objectName().split('_')[0]
        preset_dir = './hub_led/button_led/' + str(rpm_setting_index) + '_button_' + rpm_setting_name + '.cfg'
        cf = configparser.ConfigParser()
        cf.read(preset_dir)
        cf.set(status_type, 'enable', str(checkbox.isChecked()))
        with open(preset_dir, 'w+') as (f):
            cf.write(f)

    def changeCurrentButtonLedSettingColor(self, led_button, color_str):
        self.hubrgbledchooser.updataButtonRgbLed()
        current_setting_button = self.rpm_led_setting_buttonGroup.checkedButton()
        rpm_setting_name = current_setting_button.text()[:-1]
        rpm_setting_index = current_setting_button.objectName()[current_setting_button.objectName().rfind('_') + 1:]
        led_text = led_button.objectName()[0:led_button.objectName().find('_')]
        preset_dir = './hub_led/button_led/' + str(rpm_setting_index) + '_button_' + rpm_setting_name + '.cfg'
        cf = configparser.ConfigParser()
        cf.read(preset_dir)
        cf.set('color', led_text, color_str)
        with open(preset_dir, 'w+') as (f):
            cf.write(f)

    def updataEnableBrightnessSetting(self, checkbox_or_slider):
        self.hubrgbledchooser.updataButtonRgbLed()
        current_setting_button = self.rpm_led_setting_buttonGroup.checkedButton()
        rpm_setting_name = current_setting_button.text()[:-1]
        rpm_setting_index = current_setting_button.objectName()[current_setting_button.objectName().rfind('_') + 1:]
        led_text = checkbox_or_slider.objectName()[0:checkbox_or_slider.objectName().find('_')]
        preset_dir = './hub_led/button_led/' + str(rpm_setting_index) + '_button_' + rpm_setting_name + '.cfg'
        cf = configparser.ConfigParser()
        cf.read(preset_dir)
        if type(checkbox_or_slider) == 'QCheckbox':
            led_checkbox = eval('self.' + led_text + '_led_en_checkBox')
            cf.set('enable', led_text, str(led_checkbox.isChecked()))
        cf.set('brightness', 'button', str(self.Button_led_brightness_Slider.value()))
        with open(preset_dir, 'w+') as (f):
            cf.write(f)

    def changeCurrentRpmLedSetting(self):
        current_setting_button = self.rpm_led_setting_buttonGroup.checkedButton()
        rpm_setting_name = current_setting_button.text()[:-1]
        rpm_setting_index = current_setting_button.objectName()[current_setting_button.objectName().rfind('_') + 1:]
        preset_dir = './hub_led/rpm_led/' + str(rpm_setting_index) + '_rpm_' + rpm_setting_name + '.cfg'
        cf = configparser.ConfigParser()
        cf.read(preset_dir)
        cf.set('setting', 'brightness', str(self.hub_led_brightness_Slider.value()))
        type = -1
        if self.rpm_linear_radioButton.isChecked():
            type = '0'
        else:
            if self.rpm_twoway_radioButton.isChecked():
                type = '1'
            else:
                if self.rpm_customize_radioButton.isChecked():
                    type = '2'
        if type != -1:
            cf.set('setting', 'type', type)
        cf.set('setting', 'flush able', str(self.Flush_pushButton.isChecked()))
        cf.set('percentage', 'led1', str(self.L1_verticalSlider.value()))
        cf.set('percentage', 'led2', str(self.L2_verticalSlider.value()))
        cf.set('percentage', 'led3', str(self.L3_verticalSlider.value()))
        cf.set('percentage', 'led4', str(self.L4_verticalSlider.value()))
        cf.set('percentage', 'led5', str(self.L5_verticalSlider.value()))
        cf.set('percentage', 'led6', str(self.L6_verticalSlider.value()))
        cf.set('percentage', 'led7', str(self.L7_verticalSlider.value()))
        cf.set('percentage', 'led8', str(self.L8_verticalSlider.value()))
        cf.set('percentage', 'led9', str(self.L9_verticalSlider.value()))
        cf.set('percentage', 'led10', str(self.L10_verticalSlider.value()))
        cf.set('percentage', 'flush', str(self.flush_verticalSlider.value()))
        with open(preset_dir, 'w+') as (f):
            cf.write(f)

    def readClutchSetting(self):
        cf = configparser.ConfigParser()
        cf.read('./cfg/clutch_setting.cfg')
        index = cf.get('current', 'index')
        eval('self.clutch_setting_pushButton_' + str(index)).setChecked(True)
        for i in range(1, 6):
            name = cf.get('set' + str(i), 'name')
            eval('self.clutch_setting_pushButton_' + str(i)).setText(name)

    def changeClutchSetting(self, button):
        if button.isChecked() == False:
            return
        set_index = button.objectName().split('_')[(-1)]
        cf = configparser.ConfigParser()
        cf.read('./cfg/clutch_setting.cfg')
        point = cf.get('set' + str(set_index), 'point')
        self.hub_clutch_point_Slider.setValue(int(point))
        cf.set('current', 'index', str(set_index))
        with open('./cfg/clutch_setting.cfg', 'w+') as (f):
            cf.write(f)

    def write_cfg_hub_clutch_point_Value(self, val):
        current_set_button = self.clutch_setting_buttonGroup.checkedButton()
        if current_set_button == None:
            return
        set_index = current_set_button.objectName().split('_')[(-1)]
        cf = configparser.ConfigParser()
        cf.read('./cfg/clutch_setting.cfg')
        cf.set('set' + str(set_index), 'point', str(val))
        with open('./cfg/clutch_setting.cfg', 'w+') as (f):
            cf.write(f)

    def changeRpmLedSetting(self, button):
        if button.isChecked() == False:
            return
        else:
            rpm_setting_name = button.text()[:-1]
            setting_index = button.objectName()[button.objectName().rfind('_') + 1:]
            preset_dir = './hub_led/rpm_led/' + str(setting_index) + '_rpm_' + rpm_setting_name + '.cfg'
            self.setCfg('rpm_setting', 'index', str(setting_index))
            cf = configparser.ConfigParser()
            cf.read(preset_dir)
            self.hub_led_brightness_Slider.setValue(int(cf.get('setting', 'brightness')))
            type = cf.get('setting', 'type')
            if type == '0':
                self.rpm_linear_radioButton.setChecked(True)
            if type == '1':
                self.rpm_twoway_radioButton.setChecked(True)
            if type == '2':
                self.rpm_customize_radioButton.setChecked(True)
        self.Flush_pushButton.setChecked(eval(cf.get('setting', 'flush able')))

        def getColorString(color_str):
            font_color = '0, 0, 0'
            r, g, b = color_str.replace(' ', '').split(',')
            Y = 0.212671 * int(r) + 0.71516 * int(g) + 0.072169 * int(b)
            if Y <= 125:
                font_color = '255, 255, 255'
            color = '\n            QPushButton{\n            background-color: rgb(' + color_str + ');\n            border: 1px solid;\n            border-color: rgb(255,255,255);\n            border-radius: 10px;\n            color: rgb(' + font_color + ');\n            }\n            QPushButton:hover{\n            background-color: rgb(' + color_str + ');\n            border: 1px solid;\n            border-color: rgb(200,200,200);\n            }\n            QPushButton:pressed{\n            background-color: rgb(' + color_str + ');\n            border: 1px solid;\n            border-color: rgb(255,255,255);\n            }\n            '
            return color

        for index in range(1, 11):
            color_button = eval('self.L' + str(index) + '_pushButton')
            color_str = cf.get('color', 'led' + str(index))
            color_button.setStyleSheet(getColorString(color_str))

        for index in range(1, 11):
            color_slider = eval('self.L' + str(index) + '_verticalSlider')
            per_val = cf.get('percentage', 'led' + str(index))
            color_slider.setValue(int(per_val))

        self.flush_verticalSlider.setValue(int(cf.get('percentage', 'flush')))

    def changeButtonLedSetting(self, button):
        if button.isChecked() == False:
            return
        rpm_setting_name = button.text()[:-1]
        setting_index = button.objectName()[button.objectName().rfind('_') + 1:]
        preset_dir = './hub_led/button_led/' + str(setting_index) + '_button_' + rpm_setting_name + '.cfg'
        self.setCfg('button_led_setting', 'index', str(setting_index))
        cf = configparser.ConfigParser()
        cf.read(preset_dir)

        def getColorString(color_str):
            font_color = '0, 0, 0'
            r, g, b = color_str.replace(' ', '').split(',')
            Y = 0.212671 * int(r) + 0.71516 * int(g) + 0.072169 * int(b)
            if Y <= 125:
                font_color = '255, 255, 255'
            color = '\n            QPushButton{\n            background-color: rgb(' + color_str + ');\n            border: 1px solid;\n            border-color: rgb(255,255,255);\n            border-radius: 10px;\n            color: rgb(' + font_color + ');\n            }\n            QPushButton:hover{\n            background-color: rgb(' + color_str + ');\n            border: 1px solid;\n            border-color: rgb(200,200,200);\n            }\n            QPushButton:pressed{\n            background-color: rgb(' + color_str + ');\n            border: 1px solid;\n            border-color: rgb(255,255,255);\n            }\n            '
            return color

        def getStatusColorString(color_str):
            font_color = '0, 0, 0'
            r, g, b = color_str.replace(' ', '').split(',')
            Y = 0.212671 * int(r) + 0.71516 * int(g) + 0.072169 * int(b)
            if Y <= 125:
                font_color = '255, 255, 255'
            color = '\n            QPushButton{\n            background-color: rgb(' + color_str + ');\n            border: 1px solid;\n            border-color: rgb(255,255,255);\n            border-radius: 8px;\n            color: rgb(' + font_color + ');\n            }\n            QPushButton:hover{\n            background-color: rgb(' + color_str + ');\n            border: 1px solid;\n            border-color: rgb(200,200,200);\n            }\n            QPushButton:pressed{\n            background-color: rgb(' + color_str + ');\n            border: 1px solid;\n            border-color: rgb(255,255,255);\n            }\n            '
            return color

        for button_text in self.button_texts:
            led_checkbox = eval('self.' + button_text + '_led_en_checkBox')
            color_button = eval('self.' + button_text + '_pushButton')
            led_checkbox.setChecked(eval(cf.get('enable', button_text)))
            color_str = cf.get('color', button_text)
            color_button.setStyleSheet(getColorString(color_str))

        self.Button_led_brightness_Slider.setValue(int(cf.get('brightness', 'button')))
        self.hubrgbledchooser.updataButtonRgbLed()
        status_texts = [
         'pitlimiter', 'drs', 'drsallowed', 'tc', 'abs', 'greenflag', 'redflag', 'yellowflag', 'blueflag', 'whiteflag', 'blackflag']
        for status_text in status_texts:
            for button_text in self.button_texts:
                led_button = eval('self.' + status_text + '_' + button_text + '_pushButton')
                led_en_checkbox = eval('self.' + status_text + '_en_checkBox')
                color_str = cf.get(status_text, button_text)
                isable = cf.get(status_text, 'enable')
                led_button.setStyleSheet(getStatusColorString(color_str))
                led_en_checkbox.setChecked(eval(isable))

    def setCfg(self, sec, opt, val):
        ui_cfg.set(sec, opt, val)
        with open('./cfg/ui_setting.cfg', 'w+') as (f):
            ui_cfg.write(f)

    def setDefaultFromCfg(self):
        fileList = os.listdir('./hub_led/rpm_led')
        for file in fileList:
            file_name, extension = os.path.splitext(file)
            if extension == '.cfg':
                preset_name = file_name[file_name.find('_rpm') + 5:]
                button_index = file_name[:file_name.find('_')]
                button = eval('self.hub_led_setting_pushButton_' + str(button_index))
                button.setText(preset_name + ' ')

        index = ui_cfg.get('rpm_setting', 'index')
        button = eval('self.hub_led_setting_pushButton_' + str(index))
        button.setChecked(True)
        fileList = os.listdir('./hub_led/button_led')
        for file in fileList:
            file_name, extension = os.path.splitext(file)
            if extension == '.cfg':
                preset_name = file_name[file_name.find('_button') + 8:]
                button_index = file_name[:file_name.find('_')]
                button = eval('self.hub_button_led_setting_pushButton_' + str(button_index))
                button.setText(preset_name + ' ')

        index = ui_cfg.get('button_led_setting', 'index')
        button = eval('self.hub_button_led_setting_pushButton_' + str(index))
        button.setChecked(True)

    def rpm_led_WheelEvent(self, button):
        button.colorIndex = (button.colorIndex + 1) % 12
        color1 = ui_cfg.get('color_pick', 'color1')
        color2 = ui_cfg.get('color_pick', 'color2')
        color3 = ui_cfg.get('color_pick', 'color3')
        color4 = ui_cfg.get('color_pick', 'color4')
        color5 = ui_cfg.get('color_pick', 'color5')
        color6 = ui_cfg.get('color_pick', 'color6')
        color7 = ui_cfg.get('color_pick', 'color7')
        color8 = ui_cfg.get('color_pick', 'color8')
        color9 = ui_cfg.get('color_pick', 'color9')
        color10 = ui_cfg.get('color_pick', 'color10')
        color11 = ui_cfg.get('color_pick', 'color11')
        color12 = ui_cfg.get('color_pick', 'color12')
        color_str_list = [
         color1, color2, color3, color4, color5, color6,
         color7, color8, color9, color10, color11, color12]
        color_str = color_str_list[button.colorIndex]
        font_color = '0, 0, 0'
        r, g, b = color_str.replace(' ', '').split(',')
        Y = 0.212671 * int(r) + 0.71516 * int(g) + 0.072169 * int(b)
        if Y <= 125:
            font_color = '255, 255, 255'
        color = '\n        QPushButton{\n        background-color: rgb(' + color_str + ');\n        border: 1px solid;\n        border-color: rgb(255,255,255);\n        border-radius: 10px;\n        color: rgb(' + font_color + ');\n        }\n        QPushButton:hover{\n        background-color: rgb(' + color_str + ');\n        border: 1px solid;\n        border-color: rgb(200,200,200);\n        }\n        QPushButton:pressed{\n        background-color: rgb(' + color_str + ');\n        border: 1px solid;\n        border-color: rgb(255,255,255);\n        }\n        '
        button.setStyleSheet(color)
        self.rpmLedChange.emit(button, color_str)

    def button_led_WheelEvent(self, button):
        button.colorIndex = (button.colorIndex + 1) % 12
        color1 = ui_cfg.get('color_pick', 'color1')
        color2 = ui_cfg.get('color_pick', 'color2')
        color3 = ui_cfg.get('color_pick', 'color3')
        color4 = ui_cfg.get('color_pick', 'color4')
        color5 = ui_cfg.get('color_pick', 'color5')
        color6 = ui_cfg.get('color_pick', 'color6')
        color7 = ui_cfg.get('color_pick', 'color7')
        color8 = ui_cfg.get('color_pick', 'color8')
        color9 = ui_cfg.get('color_pick', 'color9')
        color10 = ui_cfg.get('color_pick', 'color10')
        color11 = ui_cfg.get('color_pick', 'color11')
        color12 = ui_cfg.get('color_pick', 'color12')
        color_str_list = [
         color1, color2, color3, color4, color5, color6,
         color7, color8, color9, color10, color11, color12]
        color_str = color_str_list[button.colorIndex]
        font_color = '0, 0, 0'
        r, g, b = color_str.replace(' ', '').split(',')
        Y = 0.212671 * int(r) + 0.71516 * int(g) + 0.072169 * int(b)
        if Y <= 125:
            font_color = '255, 255, 255'
        color = '\n        QPushButton{\n        background-color: rgb(' + color_str + ');\n        border: 1px solid;\n        border-color: rgb(255,255,255);\n        border-radius: 10px;\n        color: rgb(' + font_color + ');\n        }\n        QPushButton:hover{\n        background-color: rgb(' + color_str + ');\n        border: 1px solid;\n        border-color: rgb(200,200,200);\n        }\n        QPushButton:pressed{\n        background-color: rgb(' + color_str + ');\n        border: 1px solid;\n        border-color: rgb(255,255,255);\n        }\n        '
        button.setStyleSheet(color)
        self.buttonLedChange.emit(button, color_str)

    def status_led_WheelEvent(self, button):
        button.colorIndex = (button.colorIndex + 1) % 12
        color1 = ui_cfg.get('color_pick', 'color1')
        color2 = ui_cfg.get('color_pick', 'color2')
        color3 = ui_cfg.get('color_pick', 'color3')
        color4 = ui_cfg.get('color_pick', 'color4')
        color5 = ui_cfg.get('color_pick', 'color5')
        color6 = ui_cfg.get('color_pick', 'color6')
        color7 = ui_cfg.get('color_pick', 'color7')
        color8 = ui_cfg.get('color_pick', 'color8')
        color9 = ui_cfg.get('color_pick', 'color9')
        color10 = ui_cfg.get('color_pick', 'color10')
        color11 = ui_cfg.get('color_pick', 'color11')
        color12 = ui_cfg.get('color_pick', 'color12')
        color_str_list = [
         color1, color2, color3, color4, color5, color6,
         color7, color8, color9, color10, color11, color12]
        color_str = color_str_list[button.colorIndex]
        font_color = '0, 0, 0'
        r, g, b = color_str.replace(' ', '').split(',')
        Y = 0.212671 * int(r) + 0.71516 * int(g) + 0.072169 * int(b)
        if Y <= 125:
            font_color = '255, 255, 255'
        color = '\n        QPushButton{\n        background-color: rgb(' + color_str + ');\n        border: 1px solid;\n        border-color: rgb(255,255,255);\n        border-radius: 8px;\n        color: rgb(' + font_color + ');\n        }\n        QPushButton:hover{\n        background-color: rgb(' + color_str + ');\n        border: 1px solid;\n        border-color: rgb(200,200,200);\n        }\n        QPushButton:pressed{\n        background-color: rgb(' + color_str + ');\n        border: 1px solid;\n        border-color: rgb(255,255,255);\n        }\n        '
        button.setStyleSheet(color)
        self.statusLedChange.emit(button, color_str)

    def colorSelect(self, button, isbutton=0):
        self.mainWnd.setBlack(True)
        self.colorPick = ColorPickerDialog(self, mainWnd.m_pMask, button, mainWnd, isbutton)
        self.colorPick.show()

    def updataStatus(self, status):
        if status == CONNECT_STATUS_RUNNING:
            self.connect_status_Label.setStyleSheet(style_connected)
            product_name = self.hub_hidchooser.usb_hid.product_string
            release_number = self.hub_hidchooser.usb_hid.release_number
            vid = self.hub_hidchooser.usb_hid.vendor_id
            pid = self.hub_hidchooser.usb_hid.product_id
            hub_boot_ver = release_number >> 8
            hub_ver = release_number & 255
            hub_ver_major = hub_ver >> 6
            hub_ver_minor = hub_ver & 63
            hub_boot_ver_major = hub_boot_ver >> 6
            hub_boot_ver_minor = hub_boot_ver & 63
            ver = str(hub_ver_major) + '.' + str(hub_ver_minor)
            boot_ver = str(hub_boot_ver_major) + '.' + str(hub_boot_ver_minor)
            if vid == IMMS_HUB_VID:
                if pid == IMMS_HUB_PID:
                    mode = 'FD1'
            mode = 'N/A'
        else:
            if status == CONNECT_STATUS_WIRELESS_RUNNING:
                self.connect_status_Label.setStyleSheet(style_wireless_connected)
                mode = self.hub_hidchooser.getModel()
                ver_major = self.hub_hidchooser.hub_major_ver
                ver_minor = self.hub_hidchooser.hub_minor_ver
                ver = str(ver_major) + '.' + str(ver_minor)
                boot_ver = 'N/A'
            else:
                if status == CONNECT_STATUS_OTA:
                    self.connect_status_Label.setStyleSheet(style_update)
                    product_name = self.hub_hidchooser.usb_hid.product_string
                    release_number = self.hub_hidchooser.usb_hid.release_number
                    vid = self.hub_hidchooser.usb_hid.vendor_id
                    pid = self.hub_hidchooser.usb_hid.product_id
                    hub_boot_ver = release_number >> 8
                    hub_ver = release_number & 255
                    hub_ver_major = hub_ver >> 6
                    hub_ver_minor = hub_ver & 63
                    hub_boot_ver_major = hub_boot_ver >> 6
                    hub_boot_ver_minor = hub_boot_ver & 63
                    ver = str(hub_ver_major) + '.' + str(hub_ver_minor)
                    boot_ver = str(hub_boot_ver_major) + '.' + str(hub_boot_ver_minor)
                    if vid == IMMS_HUB_UPDATA_VID:
                        if pid == IMMS_HUB_UPDATA_PID:
                            mode = 'FD1'
                    else:
                        mode = 'N/A'
                else:
                    if status == CONNECT_STATUS_FAULT:
                        self.connect_status_Label.setStyleSheet(style_disconnect)
                        ver = 'N/A'
                        boot_ver = 'N/A'
                        mode = 'N/A'
                    status_texts = ['pitlimiter', 'drs', 'drsallowed', 'tc', 'abs', 'greenflag', 'redflag', 'yellowflag', 'blueflag', 'whiteflag', 'blackflag']
                    status_led_texts = [
                     'FL1', 'FL2', 'FL3', 'FR1', 'FR2', 'FR3']
                    if mode == 'FD1':
                        self.widget_2.setVisible(False)
                        self.widget_11.setVisible(False)
                        self.ERS_pushButton.setVisible(False)
                        self.ERS_led_en_checkBox.setVisible(False)
                        self.DRS_pushButton.setVisible(False)
                        self.DRS_led_en_checkBox.setVisible(False)
                        self.K1_pushButton.setVisible(False)
                        self.K1_led_en_checkBox.setVisible(False)
                        self.K2_pushButton.setVisible(False)
                        self.K2_led_en_checkBox.setVisible(False)
                        for status_type in status_texts:
                            for key in ('ERS', 'DRS', 'K1', 'K2'):
                                button = eval('self.' + status_type + '_' + key + '_pushButton')
                                button.setVisible(False)

                            for key in status_led_texts:
                                button = eval('self.' + status_type + '_' + key + '_pushButton')
                                button.setVisible(False)

                    elif mode == 'FD1S':
                        self.K1_pushButton.setVisible(False)
                        self.K1_led_en_checkBox.setVisible(False)
                        self.K2_pushButton.setVisible(False)
                        self.K2_led_en_checkBox.setVisible(False)
                        for status_type in status_texts:
                            for key in ('K1', 'K2'):
                                button = eval('self.' + status_type + '_' + key + '_pushButton')
                                button.setVisible(False)

                            for key in ('ERS', 'DRS'):
                                button = eval('self.' + status_type + '_' + key + '_pushButton')
                                button.setVisible(True)

                            for key in status_led_texts:
                                button = eval('self.' + status_type + '_' + key + '_pushButton')
                                button.setVisible(True)

            self.hub_model_Label.setText(mode)
            self.update_model_Label.setText(mode)
            self.hub_version_Label.setText(ver)
            self.update_version_Label.setText(ver)
            self.update_boot_version_Label.setText(boot_ver)


class MainGforceUi(QMainWindow, GforceUi):
    addNewCfg = pyqtSignal(str)
    renameCfg = pyqtSignal(str)

    def __init__(self, mainWnd, hidchooser, gforce_hidchooser, dashchooser):
        super(MainGforceUi, self).__init__()
        self.setupUi(self)
        self.gforce_hidchooser = gforce_hidchooser
        self.reFontSize()
        self.type = 'base'
        self.x_mode_num = 0
        self.pc_mode_num = 0
        self.last_dev_key = ''
        self.gforce_system_page_radioButton.clicked.connect(lambda val: self.gforce_stackedWidget.setCurrentIndex(0))
        self.gforce_additional_page_radioButton.clicked.connect(lambda val: self.gforce_stackedWidget.setCurrentIndex(1))
        self.gforce_hidchooser.connectStatusChange.connect(lambda val: self.updataStatus(val))
        self.changeLanguage(language_chooser.language)
        language_chooser.language_change.connect(lambda val: self.changeLanguage(val))
        self.mainWnd = mainWnd
        self.gx_mult_Slider.valueChanged.connect(lambda val: self.gx_mult_Value.setText(str(val)))
        self.gy_mult_Slider.valueChanged.connect(lambda val: self.gy_mult_Value.setText(str(val)))
        self.gz_mult_Slider.valueChanged.connect(lambda val: self.gz_mult_Value.setText(str(val)))
        self.pitch_mult_Slider.valueChanged.connect(lambda val: self.pitch_mult_Value.setText(str(val)))
        self.roll_mult_Slider.valueChanged.connect(lambda val: self.roll_mult_Value.setText(str(val)))
        self.gx_filter_Slider.valueChanged.connect(lambda val: self.gx_filter_Value.setText(str(val)))
        self.gy_filter_Slider.valueChanged.connect(lambda val: self.gy_filter_Value.setText(str(val)))
        self.gz_filter_Slider.valueChanged.connect(lambda val: self.gz_filter_Value.setText(str(val)))
        self.pitch_filter_Slider.valueChanged.connect(lambda val: self.pitch_filter_Value.setText(str(val)))
        self.roll_filter_Slider.valueChanged.connect(lambda val: self.roll_filter_Value.setText(str(val)))

    def updataStatus(self, status):
        if status == CONNECT_STATUS_RUNNING:
            self.connect_status_Label.setStyleSheet(style_connected)
            product_name = self.gforce_hidchooser.getHIDProductName()
            release_number = self.gforce_hidchooser.usb_hid.release_number
            vid = self.gforce_hidchooser.usb_hid.vendor_id
            pid = self.gforce_hidchooser.usb_hid.product_id
            gforce_boot_ver = release_number >> 8
            gforce_ver = release_number & 255
            gforce_ver_major = gforce_ver >> 6
            gforce_ver_minor = gforce_ver & 63
            gforce_boot_ver_major = gforce_boot_ver >> 6
            gforce_boot_ver_minor = gforce_boot_ver & 63
            ver = str(gforce_ver_major) + '.' + str(gforce_ver_minor)
            boot_ver = str(gforce_boot_ver_major) + '.' + str(gforce_boot_ver_minor)
            if vid == IMMS_GFORCE_VID:
                if pid == IMMS_GFORCE_PID:
                    mode = 'GFORCE'
            mode = 'N/A'
        elif status == CONNECT_STATUS_OTA:
            self.connect_status_Label.setStyleSheet(style_update)
            product_name = self.gforce_hidchooser.getHIDProductName()
            release_number = self.gforce_hidchooser.usb_hid.release_number
            vid = self.gforce_hidchooser.usb_hid.vendor_id
            pid = self.gforce_hidchooser.usb_hid.product_id
            gforce_boot_ver = release_number >> 8
            gforce_ver = release_number & 255
            gforce_ver_major = gforce_ver >> 6
            gforce_ver_minor = gforce_ver & 63
            gforce_boot_ver_major = gforce_boot_ver >> 6
            gforce_boot_ver_minor = gforce_boot_ver & 63
            ver = str(gforce_ver_major) + '.' + str(gforce_ver_minor)
            boot_ver = str(gforce_boot_ver_major) + '.' + str(gforce_boot_ver_minor)
            if vid == IMMS_GFORCE_UPDATA_VID:
                if pid == IMMS_GFORCE_UPDATA_PID:
                    mode = 'GFORCE'
            mode = 'N/A'
        else:
            if status == CONNECT_STATUS_FAULT:
                self.connect_status_Label.setStyleSheet(style_disconnect)
                ver = 'N/A'
                boot_ver = 'N/A'
                mode = 'N/A'
            self.gforce_model_Label.setText(mode)
            self.update_model_Label.setText(mode)
            self.gforce_version_Label.setText(ver)
            self.update_version_Label.setText(ver)
            self.update_boot_version_Label.setText(boot_ver)

    def reFontSize(self):
        all_w = self.findChildren(QWidget)
        scaleRate = font_size
        for _w in all_w:
            font = _w.font()
            font.setPointSize(font.pointSize() * 1)
            point_size = font.pointSize()
            pixel_size = int(point_size * scaleRate)
            font.setPixelSize(pixel_size)
            if not _w.inherits('QToolBox'):
                _w.setFont(font)

    def changeLanguage(self, language):
        trans = QTranslator()
        trans.load('immhub_' + language + '.qm', ':/translations')
        app = QApplication.instance()
        app.installTranslator(trans)
        self.retranslateUi(self)
        all_w = self.findChildren(QWidget)
        scaleRate = font_size
        if language == 'zh-cn':
            for _w in all_w:
                if not _w == self.gforce_model_Label:
                    if _w == self.gforce_version_Label:
                        pass
                    else:
                        font = _w.font()
                        font.setFamily('Noto Sans SC Medium')
                        _w.setFont(font)

        else:
            if language == 'zh-tc':
                for _w in all_w:
                    if not _w == self.gforce_model_Label:
                        if _w == self.gforce_version_Label:
                            pass
                        else:
                            font = _w.font()
                            font.setFamily('Noto Sans TC Medium')
                            _w.setFont(font)

            else:
                if language == 'ko':
                    for _w in all_w:
                        if not _w == self.gforce_model_Label:
                            if _w == self.gforce_version_Label:
                                continue
                            font = _w.font()
                            font.setFamily('Noto Sans KR Medium')
                            _w.setFont(font)

                else:
                    if language == 'ja':
                        for _w in all_w:
                            if not _w == self.gforce_model_Label:
                                if _w == self.gforce_version_Label:
                                    pass
                                else:
                                    font = _w.font()
                                    font.setFamily('Noto Sans JP Medium')
                                    _w.setFont(font)

                    elif language == 'en':
                        for _w in all_w:
                            if not _w == self.gforce_model_Label:
                                if _w == self.gforce_version_Label:
                                    pass
                                else:
                                    font = _w.font()
                                    font.setFamily('Noto Sans SC Medium')
                                    _w.setFont(font)


class MainMenuUi(QMainWindow, MenuUi):
    basePageClicked = pyqtSignal(str)
    hubPageClicked = pyqtSignal(str)
    presetPageClicked = pyqtSignal(str)

    def __init__(self, mainWnd, hidchooser, hub_hidchooser, gforce_hidchooser, dashchooser):
        super(MainMenuUi, self).__init__()
        self.setupUi(self)
        self.reFontSize()
        self.hidchooser = hidchooser
        self.hub_hidchooser = hub_hidchooser
        self.gforce_hidchooser = gforce_hidchooser
        self.dashchooser = dashchooser
        self.changeGameStatus('None')
        self.immgforce_radioButton.setVisible(False)
        self.changeLanguage(language_chooser.language)
        language_chooser.language_change.connect(lambda val: self.changeLanguage(val))
        self.preset_radioButton.setVisible(False)
        self.hidchooser.connectStatusChange.connect(lambda val: self.updataBaseStatus(val))
        self.hub_hidchooser.connectStatusChange.connect(lambda val: self.updataHubStatus(val))
        self.gforce_hidchooser.connectStatusChange.connect(lambda val: self.updataGforceStatus(val))
        self.immbase_radioButton.clicked.connect(lambda val: self.main_stackedWidget.setCurrentIndex(0))
        self.immhub_radioButton.clicked.connect(lambda val: self.main_stackedWidget.setCurrentIndex(1))
        self.preset_radioButton.clicked.connect(lambda val: self.main_stackedWidget.setCurrentIndex(2))
        self.immgforce_radioButton.clicked.connect(lambda val: self.main_stackedWidget.setCurrentIndex(3))
        self.immbase_radioButton.clicked.connect(lambda : self.basePageClicked.emit(''))
        self.immhub_radioButton.clicked.connect(lambda : self.hubPageClicked.emit(''))
        self.preset_radioButton.clicked.connect(lambda : self.presetPageClicked.emit(''))
        self.dashchooser.gameStatusChange.connect(lambda val: self.changeGameStatus(val))

    def changeGameStatus(self, game):
        if game == 'None':
            icon1 = QIcon()
            icon1.addPixmap(QPixmap(':/icon/connect_fail.png'), QIcon.Normal, QIcon.Off)
            self.preset_radioButton.setIcon(icon1)
            self.preset_radioButton.setIconSize(QtCore.QSize(5, 5))
        else:
            icon1 = QIcon()
            icon1.addPixmap(QPixmap(':/icon/connect_ok.png'), QIcon.Normal, QIcon.Off)
            self.preset_radioButton.setIcon(icon1)
            self.preset_radioButton.setIconSize(QtCore.QSize(5, 5))

    def changeLanguage(self, language):
        trans = QTranslator()
        trans.load('menu_bar_' + language + '.qm', ':/translations')
        app = QApplication.instance()
        app.installTranslator(trans)
        self.retranslateUi(self)
        all_w = self.findChildren(QWidget)
        scaleRate = font_size
        if language == 'zh-cn':
            for _w in all_w:
                if _w == self.menu_pushButton or _w == self.immbase_radioButton or _w == self.immhub_radioButton or _w == self.preset_radioButton:
                    font = _w.font()
                    font.setFamily('Noto Sans SC Medium')
                    _w.setFont(font)

        else:
            if language == 'zh-tc':
                for _w in all_w:
                    if _w == self.menu_pushButton or _w == self.immbase_radioButton or _w == self.immhub_radioButton or _w == self.preset_radioButton:
                        font = _w.font()
                        font.setFamily('Noto Sans TC Medium')
                        _w.setFont(font)

            else:
                if language == 'ko':
                    for _w in all_w:
                        if _w == self.menu_pushButton or _w == self.immbase_radioButton or _w == self.immhub_radioButton or _w == self.preset_radioButton:
                            font = _w.font()
                            font.setFamily('Noto Sans KR Medium')
                            _w.setFont(font)

                else:
                    if language == 'ja':
                        for _w in all_w:
                            if _w == self.menu_pushButton or _w == self.immbase_radioButton or _w == self.immhub_radioButton or _w == self.preset_radioButton:
                                font = _w.font()
                                font.setFamily('Noto Sans JP Medium')
                                _w.setFont(font)

                    elif language == 'en':
                        for _w in all_w:
                            if _w == self.menu_pushButton or _w == self.immbase_radioButton or _w == self.immhub_radioButton or _w == self.preset_radioButton:
                                font = _w.font()
                                font.setFamily('Noto Sans SC Medium')
                                _w.setFont(font)

    def updataBaseStatus(self, status):
        if status == CONNECT_STATUS_RUNNING:
            icon1 = QIcon()
            icon1.addPixmap(QPixmap(':/icon/connect_ok.png'), QIcon.Normal, QIcon.Off)
            self.immbase_radioButton.setIcon(icon1)
            self.immbase_radioButton.setIconSize(QtCore.QSize(5, 5))
        else:
            if status == CONNECT_STATUS_OTA:
                icon1 = QIcon()
                icon1.addPixmap(QPixmap(':/icon/connect_ota.png'), QIcon.Normal, QIcon.Off)
                self.immbase_radioButton.setIcon(icon1)
                self.immbase_radioButton.setIconSize(QtCore.QSize(5, 5))
            else:
                if status == CONNECT_STATUS_PS4:
                    icon1 = QIcon()
                    icon1.addPixmap(QPixmap(':/icon/connect_ps4.png'), QIcon.Normal, QIcon.Off)
                    self.immbase_radioButton.setIcon(icon1)
                    self.immbase_radioButton.setIconSize(QtCore.QSize(5, 5))
                elif status == CONNECT_STATUS_FAULT:
                    icon1 = QIcon()
                    icon1.addPixmap(QPixmap(':/icon/connect_fail.png'), QIcon.Normal, QIcon.Off)
                    self.immbase_radioButton.setIcon(icon1)
                    self.immbase_radioButton.setIconSize(QtCore.QSize(5, 5))
                    self.hub_hidchooser.isWireless = False

    def updataHubStatus(self, status):
        if status == CONNECT_STATUS_RUNNING:
            icon1 = QIcon()
            icon1.addPixmap(QPixmap(':/icon/connect_ok.png'), QIcon.Normal, QIcon.Off)
            self.immhub_radioButton.setIcon(icon1)
            self.immhub_radioButton.setIconSize(QtCore.QSize(5, 5))
        else:
            if status == CONNECT_STATUS_OTA:
                icon1 = QIcon()
                icon1.addPixmap(QPixmap(':/icon/connect_ota.png'), QIcon.Normal, QIcon.Off)
                self.immhub_radioButton.setIcon(icon1)
                self.immhub_radioButton.setIconSize(QtCore.QSize(5, 5))
            else:
                if status == CONNECT_STATUS_FAULT:
                    icon1 = QIcon()
                    icon1.addPixmap(QPixmap(':/icon/connect_fail.png'), QIcon.Normal, QIcon.Off)
                    self.immhub_radioButton.setIcon(icon1)
                    self.immhub_radioButton.setIconSize(QtCore.QSize(5, 5))
                elif status == CONNECT_STATUS_WIRELESS_RUNNING:
                    icon1 = QIcon()
                    icon1.addPixmap(QPixmap(':/icon/connect_wireless_ok.png'), QIcon.Normal, QIcon.Off)
                    self.immhub_radioButton.setIcon(icon1)
                    self.immhub_radioButton.setIconSize(QtCore.QSize(5, 5))

    def updataGforceStatus(self, status):
        if status == CONNECT_STATUS_RUNNING:
            icon1 = QIcon()
            icon1.addPixmap(QPixmap(':/icon/connect_ok.png'), QIcon.Normal, QIcon.Off)
            self.immgforce_radioButton.setIcon(icon1)
            self.immgforce_radioButton.setIconSize(QtCore.QSize(5, 5))
        else:
            if status == CONNECT_STATUS_OTA:
                icon1 = QIcon()
                icon1.addPixmap(QPixmap(':/icon/connect_ota.png'), QIcon.Normal, QIcon.Off)
                self.immgforce_radioButton.setIcon(icon1)
                self.immgforce_radioButton.setIconSize(QtCore.QSize(5, 5))
            elif status == CONNECT_STATUS_FAULT:
                icon1 = QIcon()
                icon1.addPixmap(QPixmap(':/icon/connect_fail.png'), QIcon.Normal, QIcon.Off)
                self.immgforce_radioButton.setIcon(icon1)
                self.immgforce_radioButton.setIconSize(QtCore.QSize(5, 5))

    def reFontSize(self):
        all_w = self.findChildren(QWidget)
        scaleRate = font_size
        for _w in all_w:
            font = _w.font()
            font.setPointSize(font.pointSize() * 1)
            point_size = font.pointSize()
            pixel_size = int(point_size * scaleRate)
            font.setPixelSize(pixel_size)
            if not _w.inherits('QToolBox'):
                _w.setFont(font)


class MainPresetUi(QMainWindow, PresetUi):

    def __init__(self, mainWnd, main_menu_ui, dashchooser):
        super(MainPresetUi, self).__init__()
        self.setupUi(self)
        self.reFontSize()
        self.changeLanguage(language_chooser.language)
        language_chooser.language_change.connect(lambda val: self.changeLanguage(val))
        self.main_menu_ui = main_menu_ui
        self.mainWnd = mainWnd
        self.dashchooser = dashchooser
        self.preset_injection_page_radioButton.clicked.connect(lambda val: self.setPage(0))
        self.preset_additional_page_radioButton.clicked.connect(lambda val: self.setPage(1))
        self.game_dir_select_pushButton.clicked.connect(lambda : self.selectDir('Please select the installation directory', self.game_path_lineEdit))
        self.injection_pushButton.clicked.connect(self.injection)
        self.game_buttonGroup.buttonToggled.connect(lambda val: self.chosseGame(val))
        self.telemetry_ffb_checkBox.toggled.connect(lambda : self.writePresetSetting())
        self.ac_page_radioButton.setChecked(True)
        self.udp_ip_label.setVisible(False)
        self.udp_port_label.setVisible(False)
        self.ip_lineEdit.setVisible(False)
        self.port_lineEdit.setVisible(False)
        self.telemetry_ffb_label.setVisible(False)
        self.telemetry_ffb_checkBox.setVisible(False)
        self.ip_lineEdit.editingFinished.connect(lambda : self.writePresetSetting())
        self.port_lineEdit.editingFinished.connect(lambda : self.writePresetSetting())
        self.telemetry_checkBox.stateChanged.connect(lambda : self.writePresetSetting())
        self.preset_help_pushButton.clicked.connect(lambda val: self.openHelp('Preset'))
        self.telemetry_help_pushButton.clicked.connect(lambda val: self.openHelp('Telemetry'))
        self.dashchooser.gameStatusChange.connect(lambda val: self.changeGameStatus(val))
        self.open_immp_import_setting()
        self.ac_page_radioButton.setChecked(True)

    def changeGameStatus(self, game):
        if game == 'None':
            self.game_status_label.setText('')
            self.game_status_label_2.setText('')
        else:
            if game == 'Assetto Corsa':
                self.ac_page_radioButton.setChecked(True)
            else:
                if game == 'Assetto Corsa Competizione':
                    self.acc_page_radioButton.setChecked(True)
                else:
                    if game == 'Project CARS':
                        self.pcar1_page_radioButton.setChecked(True)
                    else:
                        if game == 'iRacing':
                            self.ir_page_radioButton.setChecked(True)
                        else:
                            if game == 'DiRT 4':
                                self.dr4_page_radioButton.setChecked(True)
                            else:
                                if game == 'DiRT RALLY':
                                    self.drr_page_radioButton.setChecked(True)
                                else:
                                    if game == 'DiRT RALLY 2.0':
                                        self.drr2_page_radioButton.setChecked(True)
                                    else:
                                        if game == 'Forza Horizon4':
                                            self.fh4_page_radioButton.setChecked(True)
                                        else:
                                            if game == 'Forza Horizon5':
                                                self.fh5_page_radioButton.setChecked(True)
                                            else:
                                                if game == 'rFactor 2':
                                                    self.rf2_page_radioButton.setChecked(True)
                                                else:
                                                    if game == 'RaceRoom Racing Experience':
                                                        self.r3e_page_radioButton.setChecked(True)
                                                    else:
                                                        if game == 'F1 2018':
                                                            self.f12018_page_radioButton.setChecked(True)
                                                        else:
                                                            if game == 'F1 2019':
                                                                self.f12019_page_radioButton.setChecked(True)
                                                            else:
                                                                if game == 'F1 2020':
                                                                    self.f12020_page_radioButton.setChecked(True)
                                                                else:
                                                                    if game == 'F1 2021':
                                                                        self.f12021_page_radioButton.setChecked(True)
                                                                    else:
                                                                        if game == 'Euro Truck Simulator 2':
                                                                            self.ets2_page_radioButton.setChecked(True)
                        if language_chooser.language == 'zh-cn':
                            self.game_status_label.setText(game.upper() + ' 运行中')
                            self.game_status_label_2.setText(game.upper() + ' 运行中')
                        else:
                            if language_chooser.language == 'zh-tc':
                                self.game_status_label.setText(game.upper() + ' 運行中')
                                self.game_status_label_2.setText(game.upper() + ' 運行中')
                            else:
                                self.game_status_label.setText(game.upper() + ' RUNNING')
                                self.game_status_label_2.setText(game.upper() + ' RUNNING')

    def openHelp(self, val):
        self.mainWnd.setBlack(True)
        child_win = HelpInfoDialog(self.mainWnd.m_pMask, self.mainWnd, val)
        child_win.show()

    def setPage(self, val):
        self.preset_stackedWidget.setCurrentIndex(val)

    def changeLanguage(self, language):
        trans = QTranslator()
        trans.load('preset_' + language + '.qm', ':/translations')
        app = QApplication.instance()
        app.installTranslator(trans)
        self.retranslateUi(self)
        all_w = self.findChildren(QWidget)
        scaleRate = font_size
        if language == 'zh-cn':
            for _w in all_w:
                font = _w.font()
                font.setFamily('Noto Sans SC Medium')
                _w.setFont(font)

        else:
            if language == 'zh-tc':
                for _w in all_w:
                    font = _w.font()
                    font.setFamily('Noto Sans TC Medium')
                    _w.setFont(font)

            else:
                if language == 'ko':
                    for _w in all_w:
                        font = _w.font()
                        font.setFamily('Noto Sans KR Medium')
                        _w.setFont(font)

                else:
                    if language == 'ja':
                        for _w in all_w:
                            font = _w.font()
                            font.setFamily('Noto Sans JP Medium')
                            _w.setFont(font)

                    elif language == 'en':
                        for _w in all_w:
                            font = _w.font()
                            font.setFamily('Noto Sans SC Medium')
                            _w.setFont(font)

    def reFontSize(self):
        all_w = self.findChildren(QWidget)
        scaleRate = font_size
        for _w in all_w:
            font = _w.font()
            font.setPointSize(font.pointSize() * 1)
            point_size = font.pointSize()
            pixel_size = int(point_size * scaleRate)
            font.setPixelSize(pixel_size)
            if not _w.inherits('QToolBox'):
                _w.setFont(font)

    def writePresetSetting(self):
        seletc_game_button_objname = self.game_buttonGroup.checkedButton().objectName()
        game_name = seletc_game_button_objname[:seletc_game_button_objname.find('_')]
        ui_cfg.set(game_name, 't_ffb', str(self.telemetry_ffb_checkBox.isChecked()))
        ui_cfg.set(game_name, 'tele_enable', str(self.telemetry_checkBox.isChecked()))
        if ui_cfg.has_option(game_name, 'ip'):
            if ui_cfg.has_option(game_name, 'port'):
                ui_cfg.set(game_name, 'ip', self.ip_lineEdit.text())
                ui_cfg.set(game_name, 'port', self.port_lineEdit.text())
        with open('./cfg/ui_setting.cfg', 'w+') as (f):
            ui_cfg.write(f)

    def selectDir(self, str, lineEdit):
        filePath = QFileDialog.getExistingDirectory(self, str, '')
        if filePath != '':
            lineEdit.setText(filePath)

    def injection(self):
        seletc_game_button_objname = self.game_buttonGroup.checkedButton().objectName()
        game_name = seletc_game_button_objname[:seletc_game_button_objname.find('_')]
        game_path = self.game_path_lineEdit.text()
        if game_name == 'dr4' or game_name == 'drr2':
            if os.path.exists(game_path + '\\input\\devices\\device_defines.xml'):
                with open(game_path + '\\input\\devices\\device_defines.xml', 'r') as (lines):
                    lines = list(lines)
                    device_defines = False
                    for line in lines:
                        if '<device id="{C0010126-0000-0000-0000-504944564944}" name="immsource_et5" priority="100" type="wheel" />' in line:
                            device_defines = True
                            break

                    if device_defines == False:
                        for line_num, line in enumerate(lines):
                            if '</device_list>' in line:
                                lines[line_num] = line.replace('</device_list>', '  <device id="{C0010126-0000-0000-0000-504944564944}" name="immsource_et5" priority="100" type="wheel" />\n</device_list>')
                                break

                if device_defines == False:
                    with open(game_path + '\\input\\devices\\device_defines.xml', 'w+') as (f):
                        for line in lines:
                            f.write(line)

            else:
                if os.path.exists(game_path + '\\input\\devices\\device_defines.xml'):
                    with open(game_path + '\\input\\devices\\device_defines.xml', 'r') as (lines):
                        lines = list(lines)
                        device_defines = False
                        for line in lines:
                            if '<device id="{C0050126-0000-0000-0000-504944564944}" name="immsource_et3" priority="100" type="wheel" />' in line:
                                device_defines = True
                                break

                        if device_defines == False:
                            for line_num, line in enumerate(lines):
                                if '</device_list>' in line:
                                    lines[line_num] = line.replace('</device_list>', '  <device id="{C0050126-0000-0000-0000-504944564944}" name="immsource_et3" priority="100" type="wheel" />\n</device_list>')
                                    break

                    if device_defines == False:
                        with open(game_path + '\\input\\devices\\device_defines.xml', 'w+') as (f):
                            for line in lines:
                                f.write(line)

                if os.path.exists(game_path + '\\input\\actionmaps'):
                    with open(game_path + '\\input\\actionmaps\\immsource_et5.xml', 'w+') as (f):
                        if game_name == 'dr4':
                            f.write(dr4_cfg)
                        else:
                            if game_name == 'drr2':
                                f.write(drr2_cfg)
            if os.path.exists(game_path + '\\input\\actionmaps'):
                with open(game_path + '\\input\\actionmaps\\immsource_et3.xml', 'w+') as (f):
                    if game_name == 'dr4':
                        f.write(dr4_et3_cfg)
                    else:
                        if game_name == 'drr2':
                            f.write(drr2_et3_cfg)
        else:
            if game_name == 'drr':
                if os.path.exists(game_path + '\\input'):
                    with open(game_path + '\\input\\immsource_et5.xml', 'w+') as (f):
                        f.write(drr_cfg)
                    with open(game_path + '\\input\\immsource_et3.xml', 'w+') as (f):
                        f.write(drr_et3_cfg)
            else:
                if game_name == 'ac':
                    if os.path.exists(game_path + '\\cfg\\controllers\\presets'):
                        with open(game_path + '\\cfg\\controllers\\presets\\IMMSOURCE_ET5.ini', 'w+') as (f):
                            f.write(ac_cfg)
                        with open(game_path + '\\cfg\\controllers\\presets\\IMMSOURCE_ET3.ini', 'w+') as (f):
                            f.write(ac_et3_cfg)
                else:
                    if game_name == 'acc':
                        if os.path.exists(os.path.expanduser('~') + '\\Documents\\Assetto Corsa Competizione\\Customs\\Controls'):
                            with open(os.path.expanduser('~') + '\\Documents\\Assetto Corsa Competizione\\Customs\\Controls\\IMMSOURCE_ET5.json', 'w+') as (f):
                                f.write(acc_cfg)
                            with open(os.path.expanduser('~') + '\\Documents\\Assetto Corsa Competizione\\Customs\\Controls\\IMMSOURCE_ET3.json', 'w+') as (f):
                                f.write(acc_et3_cfg)
                    else:
                        if game_name == 'rf2':
                            if os.path.exists(game_path + '\\UserData\\Controller'):
                                with open(game_path + '\\UserData\\Controller\\IMMSOURCE ET5.JSON', 'w+') as (f):
                                    f.write(rf2_cfg)
                                with open(game_path + '\\UserData\\Controller\\IMMSOURCE ET3.JSON', 'w+') as (f):
                                    f.write(rf2_et3_cfg)
                        else:
                            if game_name == 'r3e':
                                if os.path.exists(game_path + '\\Game\\GameData\\ControlSet'):
                                    with open(game_path + '\\Game\\GameData\\ControlSet\\IMMSOURCE ET5.rcs', 'w+') as (f):
                                        f.write(r3e_cfg)
                                    with open(game_path + '\\Game\\GameData\\ControlSet\\IMMSOURCE ET3.rcs', 'w+') as (f):
                                        f.write(r3e_et3_cfg)
                                if os.path.exists(os.path.expanduser('~') + '\\Documents\\My Games\\SimBin\\RaceRoom Racing Experience\\UserData\\ControlSet'):
                                    with open(os.path.expanduser('~') + '\\Documents\\My Games\\SimBin\\RaceRoom Racing Experience\\UserData\\ControlSet\\IMMSOURCE ET5.rcs', 'w+') as (f):
                                        f.write(r3e_user_cfg)
                                    with open(os.path.expanduser('~') + '\\Documents\\My Games\\SimBin\\RaceRoom Racing Experience\\UserData\\ControlSet\\IMMSOURCE ET3.rcs', 'w+') as (f):
                                        f.write(r3e_user_et3_cfg)
                            elif game_name == 'f12018' or game_name == 'f12019' or game_name == 'f12020' or game_name == 'f12021':
                                if os.path.exists(game_path + '\\actionmaps'):
                                    with open(game_path + '\\actionmaps\\immsource_et5.xml', 'w+') as (f):
                                        f.write(f12020_cfg)
                                    with open(game_path + '\\actionmaps\\immsource_et3.xml', 'w+') as (f):
                                        f.write(f12020_et3_cfg)

    def loadAutosetPreset(self, switch_text):
        if switch_text == '':
            return
        preset_name = switch_text
        perset_dir = './preset/' + preset_name + '.cfg'
        preset_cfg = configparser.ConfigParser()
        preset_cfg.read(perset_dir)
        self.preset_ffb_mode_label.setText(preset_cfg.get('setting', 'mode'))
        self.preset_ffb_strength_label.setText(preset_cfg.get('general', 'strenght'))
        self.preset_ffb_response_label.setText(preset_cfg.get('general', 'response'))
        self.preset_ffb_detail_enhance_label.setText(preset_cfg.get('general', 'detail enhance'))
        self.preset_ffb_filter_label.setText(preset_cfg.get('general', 'filter'))
        self.preset_ffb_linearity_label.setText(preset_cfg.get('general', 'linearity'))
        self.preset_inhe_spring_label.setText(preset_cfg.get('inherent feature', 'spring'))
        self.preset_inhe_friction_label.setText(preset_cfg.get('inherent feature', 'friction'))
        self.preset_inhe_damping_label.setText(preset_cfg.get('inherent feature', 'damping'))
        self.preset_inhe_inertia_label.setText(preset_cfg.get('inherent feature', 'inertia'))
        if preset_cfg.get('dynamic feature', 'enable') == 'True':
            self.preset_dyna_status_label.setText('On')
        else:
            if preset_cfg.get('dynamic feature', 'enable') == 'False':
                self.preset_dyna_status_label.setText('Off')
        self.preset_dyna_damping_label.setText(preset_cfg.get('dynamic feature', 'damping'))
        self.preset_dyna_threshold_label.setText(preset_cfg.get('dynamic feature', 'threshold'))
        self.preset_dyna_range_label.setText(preset_cfg.get('dynamic feature', 'range'))
        self.preset_ffb_constant_label.setText(preset_cfg.get('force feedback signal', 'constant'))
        self.preset_ffb_friction_label.setText(preset_cfg.get('force feedback signal', 'friction'))
        self.preset_ffb_damping_label.setText(preset_cfg.get('force feedback signal', 'damping'))
        self.preset_ffb_inertia_label.setText(preset_cfg.get('force feedback signal', 'inertia'))
        self.preset_ffb_sine_label.setText(preset_cfg.get('force feedback signal', 'sine'))
        self.preset_ffb_spring_label.setText(preset_cfg.get('force feedback signal', 'spring'))
        self.preset_ffb_ramp_label.setText(preset_cfg.get('force feedback signal', 'ramp'))
        self.preset_ffb_square_label.setText(preset_cfg.get('force feedback signal', 'square'))
        self.preset_ffb_sawtooth_label.setText(preset_cfg.get('force feedback signal', 'sawtooth'))

    def injectEnable(self, enable):
        self.injection_pushButton.setEnabled(enable)
        self.game_dir_select_pushButton.setEnabled(enable)
        self.game_path_lineEdit.setEnabled(enable)

    def open_immp_import_setting(self):
        for button in self.game_buttonGroup.buttons():
            button.setChecked(True)
            self.injection()

    def chosseGame(self, button):
        if button.isChecked() == False:
            return
        else:
            game_name = button.objectName()[:button.objectName().find('_')]
            game_path = self.searchSteam(game_name)
            self.game_path_lineEdit.setText(game_path)
            self.injectEnable(True)
            if game_name == 'ac':
                self.game_label.setText('Assetto Corsa')
                self.game_label2.setText('Assetto Corsa')
            else:
                if game_name == 'acc':
                    self.game_label.setText('Assetto Corsa Competizione')
                    self.game_label2.setText('Assetto Corsa Competizione')
                else:
                    if game_name == 'pcar1':
                        self.game_label.setText('Project CARS')
                        self.game_label2.setText('Project CARS')
                        self.injectEnable(False)
                    else:
                        if game_name == 'ir':
                            self.game_label.setText('iRacing')
                            self.game_label2.setText('iRacing')
                            self.injectEnable(False)
                        else:
                            if game_name == 'ams2':
                                self.game_label.setText('Automobilista 2')
                                self.game_label2.setText('Automobilista 2')
                                self.injectEnable(False)
                            else:
                                if game_name == 'dr4':
                                    self.game_label.setText('DiRT 4')
                                    self.game_label2.setText('DiRT 4')
                                else:
                                    if game_name == 'drr':
                                        self.game_label.setText('DiRT RALLY')
                                        self.game_label2.setText('DiRT RALLY')
                                    else:
                                        if game_name == 'drr2':
                                            self.game_label.setText('DiRT RALLY 2.0')
                                            self.game_label2.setText('DiRT RALLY 2.0')
                                        else:
                                            if game_name == 'fh4':
                                                self.game_label.setText('Forza Horizon 4')
                                                self.game_label2.setText('Forza Horizon 4')
                                                self.injectEnable(False)
                                            else:
                                                if game_name == 'fh5':
                                                    self.game_label.setText('Forza Horizon 5')
                                                    self.game_label2.setText('Forza Horizon 5')
                                                    self.injectEnable(False)
                                                else:
                                                    if game_name == 'rf2':
                                                        self.game_label.setText('rFactor 2')
                                                        self.game_label2.setText('rFactor 2')
                                                    else:
                                                        if game_name == 'r3e':
                                                            self.game_label.setText('RaceRoom Racing Experience')
                                                            self.game_label2.setText('RaceRoom Racing Experience')
                                                        else:
                                                            if game_name == 'lfs':
                                                                self.game_label.setText('Live For Speed')
                                                                self.game_label2.setText('Live For Speed')
                                                                self.injectEnable(False)
                                                            else:
                                                                if game_name == 'f12018':
                                                                    self.game_label.setText('F1 2018')
                                                                    self.game_label2.setText('F1 2018')
                                                                else:
                                                                    if game_name == 'f12019':
                                                                        self.game_label.setText('F1 2019')
                                                                        self.game_label2.setText('F1 2019')
                                                                    else:
                                                                        if game_name == 'f12020':
                                                                            self.game_label.setText('F1 2020')
                                                                            self.game_label2.setText('F1 2020')
                                                                        else:
                                                                            if game_name == 'f12021':
                                                                                self.game_label.setText('F1 2021')
                                                                                self.game_label2.setText('F1 2021')
                                                                            else:
                                                                                if game_name == 'ets2':
                                                                                    self.game_label.setText('Euro Truck Simulator 2')
                                                                                    self.game_label2.setText('Euro Truck Simulator 2')
                                                                                    self.injectEnable(False)
                    if game_name == 'ir':
                        pass
                    else:
                        self.telemetry_ffb_label.setVisible(False)
                        self.telemetry_ffb_checkBox.setVisible(False)
                telemetry_ffb = eval(ui_cfg.get(game_name, 't_ffb'))
                telemetry_enable = eval(ui_cfg.get(game_name, 'tele_enable'))
                if ui_cfg.has_option(game_name, 'ip') and ui_cfg.has_option(game_name, 'port'):
                    self.udp_ip_label.setVisible(True)
                    self.udp_port_label.setVisible(True)
                    self.ip_lineEdit.setVisible(True)
                    self.port_lineEdit.setVisible(True)
                    self.ip_lineEdit.setText(ui_cfg.get(game_name, 'ip'))
                    self.port_lineEdit.setText(ui_cfg.get(game_name, 'port'))
                else:
                    self.udp_ip_label.setVisible(False)
                    self.udp_port_label.setVisible(False)
                    self.ip_lineEdit.setVisible(False)
                    self.port_lineEdit.setVisible(False)
            self.telemetry_ffb_checkBox.setChecked(telemetry_ffb)
            self.telemetry_checkBox.setChecked(telemetry_enable)
            width = 640
            image_path = ':/icon/' + game_name + '_setting.png'
            im = QImage(image_path)
            if im.width() == 0:
                image_path = ':/icon/default_setting.png'
                im = QImage(image_path)
            im_ratio = im.height() / im.width()
            sacle_height = width * im_ratio
            self.recommend_pushButton.setMinimumSize(width, sacle_height)
            self.recommend_pushButton.setMaximumSize(width, sacle_height)
            style = 'QPushButton{border-image:url(' + image_path + ');}'
            self.recommend_pushButton.setStyleSheet(style)
            image_udp_path = ':/icon/' + game_name + '_udp_setting.png'
            im = QImage(image_udp_path)
            if im.width() == 0:
                image_udp_path = ':/icon/default_setting.png'
                im = QImage(image_udp_path)
                self.udp_game_setting_label.setVisible(False)
                self.udp_game_setting_pushButton.setVisible(False)
            else:
                self.udp_game_setting_label.setVisible(True)
                self.udp_game_setting_pushButton.setVisible(True)
        im_ratio = im.height() / im.width()
        sacle_height = width * im_ratio
        self.udp_game_setting_pushButton.setMinimumSize(width, sacle_height)
        self.udp_game_setting_pushButton.setMaximumSize(width, sacle_height)
        style = 'QPushButton{border-image:url(' + image_udp_path + ');}'
        self.udp_game_setting_pushButton.setStyleSheet(style)

    def searchSteam(self, game_name):
        game_path = None
        try:
            regRoot = ConnectRegistry(None, HKEY_LOCAL_MACHINE)
            subDir = 'SOFTWARE\\Wow6432Node\\Valve\\Steam'
            keyHandle = OpenKey(regRoot, subDir)
            count = QueryInfoKey(keyHandle)[1]
            steam_install_path = ''
            for j in range(count):
                name, value, type = EnumValue(keyHandle, j)
                if 'InstallPath' in name:
                    steam_install_path = value + '\\steamapps\\libraryfolders.vdf'

            if game_name == 'ac':
                _game = 'assettocorsa'
            else:
                if game_name == 'acc':
                    _game = 'Assetto Corsa Competizione'
                else:
                    if game_name == 'dr4':
                        _game = 'DiRT 4'
                    else:
                        if game_name == 'drr':
                            _game = 'DiRT Rally'
                        else:
                            if game_name == 'drr2':
                                _game = 'DiRT Rally 2.0'
                            else:
                                if game_name == 'f12018':
                                    _game = 'F1 2018'
                                else:
                                    if game_name == 'f12019':
                                        _game = 'F1 2019'
                                    else:
                                        if game_name == 'f12020':
                                            _game = 'F1 2020'
                                        else:
                                            if game_name == 'f12021':
                                                _game = 'F1 2021'
                                            else:
                                                if game_name == 'grid':
                                                    _game = 'GRID (2019)'
                                                else:
                                                    if game_name == 'pcar1':
                                                        _game = 'pCars'
                                                    else:
                                                        if game_name == 'r3e':
                                                            _game = 'raceroom racing experience'
                                                        else:
                                                            if game_name == 'rf2':
                                                                _game = 'rFactor 2'
                                                            else:
                                                                if game_name == 'kk':
                                                                    _game = 'KartKraft'
                                                                else:
                                                                    if game_name == 'ets2':
                                                                        _game = 'Euro Truck Simulator 2'
                                                                    else:
                                                                        if game_name == 'ir':
                                                                            _game = 'iRacing'
                                                                        else:
                                                                            _game = None
            if _game:
                if os.path.exists(steam_install_path):
                    with open(steam_install_path, 'r', encoding='UTF-8') as (f):
                        for line in f.readlines():
                            line = line.replace('"', '').replace('\\\\', '/')
                            line = re.split('[\\t|\\n]', line)
                            line = [i for i in line if i != '']
                            if len(line) == 2 and os.path.isdir(line[1]):
                                path = line[1] + '/steamapps/common'
                                if not os.path.isdir(path):
                                    pass
                                else:
                                    dirs = os.listdir(path)
                                    for game in dirs:
                                        if game == _game:
                                            game_path = path.replace('/', '\\') + '\\' + game

            CloseKey(keyHandle)
            CloseKey(regRoot)
        except Exception as e:
            print('searchSteam ', e)

        return game_path


class BaseNewRenameCfgDialog(QDialog, CfgDialog):

    def __init__(self, base_ui_class=None, parent=None, combbox=None, mainWnd=None, type=None):
        super(BaseNewRenameCfgDialog, self).__init__(parent)
        self.setupUi(self)
        self.reFontSize()
        self.changeLanguage(language_chooser.language)
        language_chooser.language_change.connect(lambda val: self.changeLanguage(val))
        self.base_ui_class = base_ui_class
        self.parent = parent
        self.combbox = combbox
        self.mainWnd = mainWnd
        self.type = type
        self.setWindowFlags(QtCore.Qt.WindowCloseButtonHint | QtCore.Qt.FramelessWindowHint)
        self.cancel_pushButton.pressed.connect(self.closeDialog)
        self.ok_pushButton.pressed.connect(self.ok)
        animation = QPropertyAnimation(self, b'windowOpacity', self)
        animation.setDuration(200)
        animation.setStartValue(0)
        animation.setEndValue(1)
        animation2 = QPropertyAnimation(self.mainWnd.m_pMask, b'windowOpacity', self.mainWnd.m_pMask)
        animation2.setDuration(200)
        animation2.setStartValue(0)
        animation2.setEndValue(1)
        animation.finished.connect(lambda : self.parent.markMousePress.connect(self.closeDialog))
        animation.start()
        animation2.start()
        parent_globalPos = self.parent.mapToGlobal(QPoint(0, 0))
        self_globalPos = self.mapToGlobal(QPoint(0, 0))
        x = parent_globalPos.x() - self_globalPos.x() + (self.parent.width() - self.width()) / 2
        y = parent_globalPos.y() - self_globalPos.y() + (self.parent.height() - self.height()) / 2
        self.move(x, y)

    def changeLanguage(self, language):
        trans = QTranslator()
        trans.load('cfg_new_rename_' + language + '.qm', ':/translations')
        app = QApplication.instance()
        app.installTranslator(trans)
        self.retranslateUi(self)
        all_w = self.findChildren(QWidget)
        scaleRate = font_size
        if language == 'zh-cn':
            for _w in all_w:
                font = _w.font()
                font.setFamily('Noto Sans SC Medium')
                _w.setFont(font)

        else:
            if language == 'zh-tc':
                for _w in all_w:
                    font = _w.font()
                    font.setFamily('Noto Sans TC Medium')
                    _w.setFont(font)

            else:
                if language == 'ko':
                    for _w in all_w:
                        font = _w.font()
                        font.setFamily('Noto Sans KR Medium')
                        _w.setFont(font)

                else:
                    if language == 'ja':
                        for _w in all_w:
                            font = _w.font()
                            font.setFamily('Noto Sans JP Medium')
                            _w.setFont(font)

                    elif language == 'en':
                        for _w in all_w:
                            font = _w.font()
                            font.setFamily('Noto Sans SC Medium')
                            _w.setFont(font)

    def reFontSize(self):
        all_w = self.findChildren(QWidget)
        scaleRate = font_size
        for _w in all_w:
            font = _w.font()
            font.setPointSize(font.pointSize() * 1)
            point_size = font.pointSize()
            pixel_size = int(point_size * scaleRate)
            font.setPixelSize(pixel_size)
            if not _w.inherits('QToolBox'):
                _w.setFont(font)

    def mousePressEvent(self, event):
        pass

    def ok(self):
        if self.cfg_lineEdit.text() == '':
            self.cfg_lineEdit.setPlaceholderText('Please enter a new setting name.')
            return
        else:
            if '-' in self.cfg_lineEdit.text():
                self.cfg_lineEdit.setText('')
                self.cfg_lineEdit.setPlaceholderText("'-' cannot appear in the name.")
                return
            if self.type == 'new':
                enter_name = self.cfg_lineEdit.text().strip()
                if self.combbox.findText(enter_name, QtCore.Qt.MatchFixedString) == -1:
                    perset_dir = './preset/' + enter_name + '.cfg'
                    with open(perset_dir, 'w+') as (f):
                        pass
                    self.base_ui_class.addNewCfg.emit(enter_name)
                else:
                    self.cfg_lineEdit.setText('')
                    self.cfg_lineEdit.setPlaceholderText('Setting name already exists.')
                    return
                self.closeDialog()
            elif self.type == 'rename':
                enter_name = self.cfg_lineEdit.text().strip()
                new_perset_dir = './preset/' + enter_name + '.cfg'
                current_index = self.combbox.currentIndex()
                current_text = self.combbox.currentText()
                if ' - ' in current_text:
                    current_text, game_name = current_text.split(' - ')
                    enter_name = enter_name + ' - ' + game_name
                old_perset_dir = './preset/' + current_text + '.cfg'
                os.rename(old_perset_dir, new_perset_dir)
                self.combbox.setItemText(current_index, enter_name)
                self.closeDialog()

    def closeDialog(self):
        animation = QPropertyAnimation(self, b'windowOpacity', self)
        animation.setDuration(200)
        animation.setStartValue(1)
        animation.setEndValue(0)
        animation2 = QPropertyAnimation(self.mainWnd.m_pMask, b'windowOpacity', self.mainWnd.m_pMask)
        animation2.setDuration(200)
        animation2.setStartValue(1)
        animation2.setEndValue(0)
        animation.finished.connect(self.closeAndBlack)
        animation.start()
        animation2.start()

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Escape:
            pass

    def closeAndBlack(self):
        self.mainWnd.setBlack(False)
        self.close()


class HubNewRenameCfgDialog(QDialog, CfgDialog):

    def __init__(self, hub_ui_class=None, parent=None, button=None, mainWnd=None, type=None):
        QDialog.__init__(self, parent)
        super(HubNewRenameCfgDialog, self).__init__(parent)
        self.setupUi(self)
        self.reFontSize()
        self.changeLanguage(language_chooser.language)
        language_chooser.language_change.connect(lambda val: self.changeLanguage(val))
        self.hub_ui_class = hub_ui_class
        self.parent = parent
        self.button = button
        self.mainWnd = mainWnd
        self.type = type
        self.setWindowFlags(QtCore.Qt.WindowCloseButtonHint | QtCore.Qt.FramelessWindowHint)
        self.cancel_pushButton.pressed.connect(self.closeDialog)
        self.ok_pushButton.pressed.connect(self.ok)
        animation = QPropertyAnimation(self, b'windowOpacity', self)
        animation.setDuration(200)
        animation.setStartValue(0)
        animation.setEndValue(1)
        animation2 = QPropertyAnimation(self.mainWnd.m_pMask, b'windowOpacity', self.mainWnd.m_pMask)
        animation2.setDuration(200)
        animation2.setStartValue(0)
        animation2.setEndValue(1)
        animation.finished.connect(lambda : self.parent.markMousePress.connect(self.closeDialog))
        animation.start()
        animation2.start()
        parent_globalPos = self.parent.mapToGlobal(QPoint(0, 0))
        self_globalPos = self.mapToGlobal(QPoint(0, 0))
        x = parent_globalPos.x() - self_globalPos.x() + (self.parent.width() - self.width()) / 2
        y = parent_globalPos.y() - self_globalPos.y() + (self.parent.height() - self.height()) / 2
        self.move(x, y)

    def changeLanguage(self, language):
        trans = QTranslator()
        trans.load('cfg_new_rename_' + language + '.qm', ':/translations')
        app = QApplication.instance()
        app.installTranslator(trans)
        self.retranslateUi(self)
        all_w = self.findChildren(QWidget)
        scaleRate = font_size
        if language == 'zh-cn':
            for _w in all_w:
                font = _w.font()
                font.setFamily('Noto Sans SC Medium')
                _w.setFont(font)

        else:
            if language == 'zh-tc':
                for _w in all_w:
                    font = _w.font()
                    font.setFamily('Noto Sans TC Medium')
                    _w.setFont(font)

            else:
                if language == 'ko':
                    for _w in all_w:
                        font = _w.font()
                        font.setFamily('Noto Sans KR Medium')
                        _w.setFont(font)

                else:
                    if language == 'ja':
                        for _w in all_w:
                            font = _w.font()
                            font.setFamily('Noto Sans JP Medium')
                            _w.setFont(font)

                    elif language == 'en':
                        for _w in all_w:
                            font = _w.font()
                            font.setFamily('Noto Sans SC Medium')
                            _w.setFont(font)

    def reFontSize(self):
        all_w = self.findChildren(QWidget)
        scaleRate = font_size
        for _w in all_w:
            font = _w.font()
            font.setPointSize(font.pointSize() * 1)
            point_size = font.pointSize()
            pixel_size = int(point_size * scaleRate)
            font.setPixelSize(pixel_size)
            if not _w.inherits('QToolBox'):
                _w.setFont(font)

    def mousePressEvent(self, event):
        pass

    def ok(self):
        if self.cfg_lineEdit.text() != '':
            if self.button != None:
                enter_name = self.cfg_lineEdit.text()
                setting_index = self.button.objectName()[self.button.objectName().rfind('_') + 1:]
                if self.type == 'rpm_led':
                    new_perset_dir = './hub_led/rpm_led/' + str(setting_index) + '_rpm_' + enter_name + '.cfg'
                    current_text = self.button.text()[:-1]
                    old_perset_dir = './hub_led/rpm_led/' + str(setting_index) + '_rpm_' + current_text + '.cfg'
                    os.rename(old_perset_dir, new_perset_dir)
                    new_perset_dir = './hub_led/button_led/' + str(setting_index) + '_button_' + enter_name + '.cfg'
                    current_text = self.button.text()[:-1]
                    old_perset_dir = './hub_led/button_led/' + str(setting_index) + '_button_' + current_text + '.cfg'
                    os.rename(old_perset_dir, new_perset_dir)
                else:
                    if self.type == 'clutch_point':
                        current_set_button = self.hub_ui_class.clutch_setting_buttonGroup.checkedButton()
                        set_index = current_set_button.objectName().split('_')[(-1)]
                        cf = configparser.ConfigParser()
                        cf.read('./cfg/clutch_setting.cfg')
                        cf.set('set' + str(set_index), 'name', str(enter_name))
                        with open('./cfg/clutch_setting.cfg', 'w+') as (f):
                            cf.write(f)
                        current_set_button.setText(enter_name)
                self.button.setText(enter_name + ' ')
                self.closeDialog()
            else:
                self.cfg_lineEdit.setText('')
                self.cfg_lineEdit.setPlaceholderText('Please choose a setting.')
        else:
            self.cfg_lineEdit.setPlaceholderText('Please enter a new setting name.')

    def closeDialog(self):
        animation = QPropertyAnimation(self, b'windowOpacity', self)
        animation.setDuration(200)
        animation.setStartValue(1)
        animation.setEndValue(0)
        animation2 = QPropertyAnimation(self.mainWnd.m_pMask, b'windowOpacity', self.mainWnd.m_pMask)
        animation2.setDuration(200)
        animation2.setStartValue(1)
        animation2.setEndValue(0)
        animation.finished.connect(self.closeAndBlack)
        animation.start()
        animation2.start()

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Escape:
            pass

    def closeAndBlack(self):
        self.mainWnd.setBlack(False)
        self.close()


class ColorPickerDialog(QDialog, ColorPickerUi):

    def __init__(self, hub_ui_class=None, parent=None, button=None, mainWnd=None, isbutton=0):
        super(ColorPickerDialog, self).__init__(parent)
        self.setupUi(self)
        self.reFontSize()
        self.hub_ui_class = hub_ui_class
        self.parent = parent
        self.button = button
        self.mainWnd = mainWnd
        self.isbutton = isbutton
        self.setWindowFlags(QtCore.Qt.WindowCloseButtonHint | QtCore.Qt.FramelessWindowHint)
        self.selected = 0
        self.color1_pushButton.mouseDoubleClickEvent = lambda val: self.SetColor(self.color1_pushButton)
        self.color2_pushButton.mouseDoubleClickEvent = lambda val: self.SetColor(self.color2_pushButton)
        self.color3_pushButton.mouseDoubleClickEvent = lambda val: self.SetColor(self.color3_pushButton)
        self.color4_pushButton.mouseDoubleClickEvent = lambda val: self.SetColor(self.color4_pushButton)
        self.color5_pushButton.mouseDoubleClickEvent = lambda val: self.SetColor(self.color5_pushButton)
        self.color6_pushButton.mouseDoubleClickEvent = lambda val: self.SetColor(self.color6_pushButton)
        self.color7_pushButton.mouseDoubleClickEvent = lambda val: self.SetColor(self.color7_pushButton)
        self.color8_pushButton.mouseDoubleClickEvent = lambda val: self.SetColor(self.color8_pushButton)
        self.color9_pushButton.mouseDoubleClickEvent = lambda val: self.SetColor(self.color9_pushButton)
        self.color10_pushButton.mouseDoubleClickEvent = lambda val: self.SetColor(self.color10_pushButton)
        self.color11_pushButton.mouseDoubleClickEvent = lambda val: self.SetColor(self.color11_pushButton)
        self.color12_pushButton.mouseDoubleClickEvent = lambda val: self.SetColor(self.color12_pushButton)
        self.setSettingColor()
        self.color_buttonGroup.buttonToggled.connect(lambda val: self.changeSliderValue(val))
        self.color_r_lineEdit.setValidator(QIntValidator(0, 255))
        self.color_g_lineEdit.setValidator(QIntValidator(0, 255))
        self.color_b_lineEdit.setValidator(QIntValidator(0, 255))
        self.color_r_Slider.valueChanged.connect(lambda val: self.color_r_lineEdit.setText(str(val)))
        self.color_g_Slider.valueChanged.connect(lambda val: self.color_g_lineEdit.setText(str(val)))
        self.color_b_Slider.valueChanged.connect(lambda val: self.color_b_lineEdit.setText(str(val)))
        self.color_r_Slider.valueChanged.connect(self.changeSettingColor)
        self.color_g_Slider.valueChanged.connect(self.changeSettingColor)
        self.color_b_Slider.valueChanged.connect(self.changeSettingColor)
        self.color_r_lineEdit.editingFinished.connect(lambda : self.color_r_Slider.setValue(int(self.color_r_lineEdit.text())))
        self.color_g_lineEdit.editingFinished.connect(lambda : self.color_g_Slider.setValue(int(self.color_g_lineEdit.text())))
        self.color_b_lineEdit.editingFinished.connect(lambda : self.color_b_Slider.setValue(int(self.color_b_lineEdit.text())))
        self.color_r_Slider.valueChanged.connect(self.changeButtonColor)
        self.color_g_Slider.valueChanged.connect(self.changeButtonColor)
        self.color_b_Slider.valueChanged.connect(self.changeButtonColor)
        animation = QPropertyAnimation(self, b'windowOpacity', self)
        animation.setDuration(200)
        animation.setStartValue(0)
        animation.setEndValue(1)
        animation2 = QPropertyAnimation(self.mainWnd.m_pMask, b'windowOpacity', self.mainWnd.m_pMask)
        animation2.setDuration(200)
        animation2.setStartValue(0)
        animation2.setEndValue(1)
        animation.finished.connect(lambda : self.parent.markMousePress.connect(self.closeDialog))
        animation.start()
        animation2.start()
        button_globalPos = self.button.mapToGlobal(QPoint(0, 0))
        self_globalPos = self.mapToGlobal(QPoint(0, 0))
        x = button_globalPos.x() - self_globalPos.x() + (self.button.width() - self.width()) / 2
        y = button_globalPos.y() - self_globalPos.y() + (self.button.height() - self.height()) / 2
        if x >= 880:
            x = 880
        if y >= 400:
            y = 400
        self.move(x, y + 40)

    def SetColor(self, button):
        bgColor = button.palette().color(QPalette.Background)
        r, g, b, a = bgColor.getRgb()
        color_str = str(r) + ', ' + str(g) + ', ' + str(b)
        self.selectedColor(color_str)

    def changeSliderValue(self, select_color_button):
        if not select_color_button.isChecked():
            return
        bgColor = select_color_button.palette().color(QPalette.Background)
        r, g, b, a = bgColor.getRgb()
        self.color_r_Slider.setValue(r)
        self.color_g_Slider.setValue(g)
        self.color_b_Slider.setValue(b)

    def changeButtonColor(self):
        select_color_button = self.color_buttonGroup.checkedButton()
        if not select_color_button:
            return
        r = self.color_r_Slider.value()
        g = self.color_g_Slider.value()
        b = self.color_b_Slider.value()
        color_str = str(r) + ', ' + str(g) + ', ' + str(b)
        color = 'QPushButton{\n                background-color: rgb(' + color_str + ');\n                border-color: rgb(255,255,255);\n                border: 2px solid;\n                border-color: rgb(51,51,51);\n                border-radius: 4px;\n                }\n                \n                \n                QPushButton:checked{\n                background-color: rgb(' + color_str + ');\n                border: 2px solid;\n                border-color: rgb(' + color_str + ');\n                border-radius: 2px;\n                }'
        select_color_button.setStyleSheet(color)

    def changeSettingColor(self):
        select_color_button = self.color_buttonGroup.checkedButton()
        if not select_color_button:
            return
        index = select_color_button.objectName().split('_')[0].replace('color', '')
        r = self.color_r_Slider.value()
        g = self.color_g_Slider.value()
        b = self.color_b_Slider.value()
        color_str = str(r) + ', ' + str(g) + ', ' + str(b)
        self.setCfg('color_pick', 'color' + str(index), color_str)

    def setSettingColor(self):
        for i in range(1, 13):
            color_str = ui_cfg.get('color_pick', 'color' + str(i))
            color = 'QPushButton{\n                    background-color: rgb(' + color_str + ');\n                    border-color: rgb(255,255,255);\n                    border: 2px solid;\n                    border-color: rgb(51,51,51);\n                    border-radius: 4px;\n                    }\n    \n    \n                    QPushButton:checked{\n                    background-color: rgb(' + color_str + ');\n                    border: 2px solid;\n                    border-color: rgb(' + color_str + ');\n                    border-radius: 2px;\n                    }'
            eval('self.color' + str(i) + '_pushButton').setStyleSheet(color)

    def setCfg(self, sec, opt, val):
        ui_cfg.set(sec, opt, val)
        with open('./cfg/ui_setting.cfg', 'w+') as (f):
            ui_cfg.write(f)

    def mousePressEvent(self, event):
        pass

    def reFontSize(self):
        all_w = self.findChildren(QWidget)
        scaleRate = font_size
        for _w in all_w:
            font = _w.font()
            font.setPointSize(font.pointSize() * 1)
            point_size = font.pointSize()
            pixel_size = int(point_size * scaleRate)
            font.setPixelSize(pixel_size)
            if not _w.inherits('QToolBox'):
                _w.setFont(font)

    def selectedColor(self, color_str):
        font_color = '0, 0, 0'
        r, g, b = color_str.replace(' ', '').split(',')
        Y = 0.212671 * int(r) + 0.71516 * int(g) + 0.072169 * int(b)
        if Y <= 125:
            font_color = '255, 255, 255'
        else:
            if self.isbutton == 1:
                color = '\n            QPushButton{\n            background-color: rgb(' + color_str + ');\n            border: 1px solid;\n            border-color: rgb(255,255,255);\n            border-radius: 10px;\n            color: rgb(' + font_color + ');\n            }\n            QPushButton:hover{\n            background-color: rgb(' + color_str + ');\n            border: 1px solid;\n            border-color: rgb(200,200,200);\n            }\n            QPushButton:pressed{\n            background-color: rgb(' + color_str + ');\n            border: 1px solid;\n            border-color: rgb(255,255,255);\n            }\n            '
                self.button.setStyleSheet(color)
                self.hub_ui_class.buttonLedChange.emit(self.button, color_str)
            else:
                if self.isbutton == 2:
                    color = '\n            QPushButton{\n            background-color: rgb(' + color_str + ');\n            border: 1px solid;\n            border-color: rgb(255,255,255);\n            border-radius: 8px;\n            color: rgb(' + font_color + ');\n            }\n            QPushButton:hover{\n            background-color: rgb(' + color_str + ');\n            border: 1px solid;\n            border-color: rgb(200,200,200);\n            }\n            QPushButton:pressed{\n            background-color: rgb(' + color_str + ');\n            border: 1px solid;\n            border-color: rgb(255,255,255);\n            }\n            '
                    self.button.setStyleSheet(color)
                    self.hub_ui_class.statusLedChange.emit(self.button, color_str)
                else:
                    color = '\n            QPushButton{\n            background-color: rgb(' + color_str + ');\n            border: 1px solid;\n            border-color: rgb(255,255,255);\n            border-radius: 10px;\n            color: rgb(' + font_color + ');\n            }\n            QPushButton:hover{\n            background-color: rgb(' + color_str + ');\n            border: 1px solid;\n            border-color: rgb(200,200,200);\n            }\n            QPushButton:pressed{\n            background-color: rgb(' + color_str + ');\n            border: 1px solid;\n            border-color: rgb(255,255,255);\n            }\n            '
                    self.button.setStyleSheet(color)
                    self.hub_ui_class.rpmLedChange.emit(self.button, color_str)
        self.closeDialog()

    def getColor(self):
        return self.selected

    def closeDialog(self):
        animation = QPropertyAnimation(self, b'windowOpacity', self)
        animation.setDuration(200)
        animation.setStartValue(1)
        animation.setEndValue(0)
        animation2 = QPropertyAnimation(self.mainWnd.m_pMask, b'windowOpacity', self.mainWnd.m_pMask)
        animation2.setDuration(200)
        animation2.setStartValue(1)
        animation2.setEndValue(0)
        animation.finished.connect(self.closeAndBlack)
        animation.start()
        animation2.start()

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Escape:
            pass

    def closeAndBlack(self):
        self.mainWnd.setBlack(False)
        self.close()


class UpdateFwDialog(QDialog, UpdateFwDialogUi):

    def __init__(self, parent=None, mainWnd=None, ui_class=None, hidchooser=None, type=0):
        super(UpdateFwDialog, self).__init__(parent)
        self.setupUi(self)
        self.setWindowFlags(QtCore.Qt.WindowCloseButtonHint | QtCore.Qt.FramelessWindowHint)
        self.update_p_Label.setVisible(False)
        self.updatefw_finish_Label.setVisible(False)
        self.updatefw_info_Label.setVisible(True)
        self.update_exit_pushButton.setVisible(False)
        self.parent = parent
        self.mainWnd = mainWnd
        self.hidchooser = hidchooser
        self.ui_class = ui_class
        self.type = type
        self.changeLanguage(language_chooser.language)
        language_chooser.language_change.connect(lambda val: self.changeLanguage(val))
        self.update_cancel_pushButton.pressed.connect(self.closeDialog)
        self.update_exit_pushButton.pressed.connect(self.closeDialog)
        self.update_ok_pushButton.pressed.connect(self.ok)
        animation = QPropertyAnimation(self, b'windowOpacity', self)
        animation.setDuration(200)
        animation.setStartValue(0)
        animation.setEndValue(1)
        animation2 = QPropertyAnimation(self.mainWnd.m_pMask, b'windowOpacity', self.mainWnd.m_pMask)
        animation2.setDuration(200)
        animation2.setStartValue(0)
        animation2.setEndValue(1)
        animation.start()
        animation2.start()
        parent_globalPos = self.parent.mapToGlobal(QPoint(0, 0))
        self_globalPos = self.mapToGlobal(QPoint(0, 0))
        x = parent_globalPos.x() - self_globalPos.x() + (self.parent.width() - self.width()) / 2
        y = parent_globalPos.y() - self_globalPos.y() + (self.parent.height() - self.height()) / 2
        self.move(x, y)
        self.reFontSize()
        self.hidchooser.connectStatusChange.connect(lambda val: self.updateStatusChange(val))
        self.comThread = comthread.ComthreadChooser(self.hidchooser, self)
        self.comThread.updateFinish.connect(self.updateFinish)

    def updateStatusChange(self, status):
        if status == CONNECT_STATUS_FAULT:
            if self.comThread.start_ota == True:
                self.closeAndBlack()

    def reFontSize(self):
        all_w = self.findChildren(QWidget)
        scaleRate = font_size
        for _w in all_w:
            font = _w.font()
            font.setPointSize(font.pointSize() * 1)
            point_size = font.pointSize()
            pixel_size = int(point_size * scaleRate)
            font.setPixelSize(pixel_size)
            if not _w.inherits('QToolBox'):
                _w.setFont(font)

    def changeLanguage(self, language):
        trans = QTranslator()
        trans.load('updatafw_' + language + '.qm', ':/translations')
        app = QApplication.instance()
        app.installTranslator(trans)
        self.retranslateUi(self)
        all_w = self.findChildren(QWidget)
        scaleRate = font_size
        if language == 'zh-cn':
            for _w in all_w:
                font = _w.font()
                font.setFamily('Noto Sans SC Medium')
                _w.setFont(font)

        else:
            if language == 'zh-tc':
                for _w in all_w:
                    font = _w.font()
                    font.setFamily('Noto Sans TC Medium')
                    _w.setFont(font)

            else:
                if language == 'ko':
                    for _w in all_w:
                        font = _w.font()
                        font.setFamily('Noto Sans KR Medium')
                        _w.setFont(font)

                else:
                    if language == 'ja':
                        for _w in all_w:
                            font = _w.font()
                            font.setFamily('Noto Sans JP Medium')
                            _w.setFont(font)

                    elif language == 'en':
                        for _w in all_w:
                            font = _w.font()
                            font.setFamily('Noto Sans SC Medium')
                            _w.setFont(font)

    def mousePressEvent(self, event):
        pass

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Escape:
            pass

    def closeAndBlack(self):
        self.comThread.__del__()
        self.mainWnd.setBlack(False)
        self.close()
        del self

    def ok(self):
        model = self.ui_class.update_model_Label.text().lower()
        type = self.hidchooser.type
        if self.type == 1:
            debug_fw_path = self.ui_class.fw_path_lineEdit.text()
            debug_fw_file = ''
            if os.path.isfile(debug_fw_path):
                path, file = os.path.split(debug_fw_path)
                file_name, suffix = os.path.splitext(file)
                if suffix == '.bin':
                    debug_fw_file = file_name
            if debug_fw_file != '':
                update_bin_path = debug_fw_path
            else:
                update_ver = self.ui_class.update_ver_label.text().replace('V', '')
                update_bin_path = './fw/' + type + '/' + type + '_' + model + '_' + update_ver + '.bin'
        else:
            if self.type == 2:
                debug_fw_boot_path = self.ui_class.fw_boot_path_lineEdit.text()
                debug_fw_boot_file = ''
                if os.path.isfile(debug_fw_boot_path):
                    path, file = os.path.split(debug_fw_boot_path)
                    file_name, suffix = os.path.splitext(file)
                    if suffix == '.bin':
                        debug_fw_boot_file = file_name
                if debug_fw_boot_file != '':
                    update_bin_path = debug_fw_boot_path
                    self.hidchooser.updata_boot_flag = False
                else:
                    self.hidchooser.updata_boot_flag = False
                    update_ver = self.ui_class.boot_update_ver_label.text().replace('V', '')
                    update_bin_path = './fw/' + type + '/' + type + '_' + model + '_boot_' + update_ver + '.bin'
            self.update_p_Label.setVisible(True)
            self.update_ok_pushButton.setEnabled(False)
            try:
                bin_buf = []
                f = Fernet('8FLIhP2-4BnRuZNBUXrMoyZa1pBttnDK1iEi3-COsVQ=')
                with open(update_bin_path, 'rb') as (file):
                    encrypted_data = file.read()
                decrypted_data = f.decrypt(encrypted_data)
                for data in decrypted_data:
                    bin_buf.append(data)

                bin_index = bin_buf[0:10]
                bin_buf = bin_buf[10:]
                file_size = len(bin_buf)
                fw_model = bin_index[0]
                print('decrypt', file_size, bin_index, model, fw_model)
                if fw_model == 1 and model == 'et5':
                    print('update et5')
                elif fw_model == 2 and model == 'et3':
                    print('update et3')
                elif fw_model == 3 and model == 'fd1':
                    print('update fd1')
                else:
                    print('update error')
                if language_chooser.language == 'zh-cn':
                    self.ui_class.base_update_info_label.setText('固件不匹配')
                else:
                    if language_chooser.language == 'zh-tc':
                        self.ui_class.base_update_info_label.setText('固件不匹配')
                    else:
                        self.ui_class.base_update_info_label.setText('Firmware mismatch')
                    self.closeDialog()
                    return
            except Exception as e:
                print(e)
                file_size = os.path.getsize(update_bin_path)
                bin_buf = []
                with open(update_bin_path, 'rb') as (f):
                    while True:
                        strb = f.read(1)
                        if strb == b'':
                            break
                        hexstr = binascii.b2a_hex(strb)
                        bin_buf.append(int(str(hexstr, 'utf-8'), 16))

                print('source', file_size)

            if self.type == 1:
                self.hidchooser.sent_handler(SETTING_UPDATA_MODE)
            else:
                if self.type == 2:
                    self.hidchooser.sent_handler(SETTING_BOOT_UPDATA_MODE)
            if APP_MAX_SIZE < file_size:
                return
            self.comThread.fileSize = file_size
            self.comThread.fileHexBuf = bin_buf
            self.comThread.cmdId = CMD_SND_FILE_DATA

    def updateFinish(self):
        self.update_cancel_pushButton.setVisible(False)
        self.update_ok_pushButton.setVisible(False)
        self.update_exit_pushButton.setVisible(True)
        self.updatefw_info_Label.setVisible(False)
        self.updatefw_finish_Label.setVisible(True)

    def closeDialog(self):
        animation = QPropertyAnimation(self, b'windowOpacity', self)
        animation.setDuration(200)
        animation.setStartValue(1)
        animation.setEndValue(0)
        animation2 = QPropertyAnimation(self.mainWnd.m_pMask, b'windowOpacity', self.mainWnd.m_pMask)
        animation2.setDuration(200)
        animation2.setStartValue(1)
        animation2.setEndValue(0)
        animation.finished.connect(self.closeAndBlack)
        animation.start()
        animation2.start()


class ConnectInfoDialog2(QMainWindow, ConnectInfoDialogUi):

    def __init__(self, text1='', text2=''):
        super(ConnectInfoDialog2, self).__init__()
        self.setupUi(self)
        self.info_Label.setText(text1)
        self.info_Label_2.setText(text2)
        self.reFontSize()

    def reFontSize(self):
        all_w = self.findChildren(QWidget)
        scaleRate = font_size
        for _w in all_w:
            font = _w.font()
            font.setPointSize(font.pointSize() * 1)
            point_size = font.pointSize()
            pixel_size = int(point_size * scaleRate)
            font.setPixelSize(pixel_size)
            if not _w.inherits('QToolBox'):
                _w.setFont(font)


class HelpInfoDialog(QDialog, HelpInfoDialogUi):

    def __init__(self, parent=None, mainWnd=None, val=''):
        super(HelpInfoDialog, self).__init__(parent)
        self.setupUi(self)
        self.setWindowFlags(QtCore.Qt.WindowCloseButtonHint | QtCore.Qt.FramelessWindowHint)
        self.parent = parent
        self.mainWnd = mainWnd
        self.val = val
        self.exit_pushButton.pressed.connect(self.closeDialog)
        animation = QPropertyAnimation(self, b'windowOpacity', self)
        animation.setDuration(200)
        animation.setStartValue(0)
        animation.setEndValue(1)
        animation2 = QPropertyAnimation(self.mainWnd.m_pMask, b'windowOpacity', self.mainWnd.m_pMask)
        animation2.setDuration(200)
        animation2.setStartValue(0)
        animation2.setEndValue(1)
        animation.start()
        animation2.start()
        parent_globalPos = self.parent.mapToGlobal(QPoint(0, 0))
        self_globalPos = self.mapToGlobal(QPoint(0, 0))
        x = parent_globalPos.x() - self_globalPos.x() + (self.parent.width() - self.width()) / 2
        y = parent_globalPos.y() - self_globalPos.y() + (self.parent.height() - self.height()) / 2
        self.move(x, y)
        self.reFontSize()
        if val != '':
            self.help_label.setText(val)
            width = 720
            val = val.lower()
            if language_chooser.language == 'zh-cn' or language_chooser.language == 'zh-tc':
                image_path = ':/icon/help_' + val + '.png'
                self.exit_pushButton.setText('退出')
            else:
                image_path = ':/icon/help_' + val + '_en.png'
                self.exit_pushButton.setText('Exit')
            im = QImage(image_path)
            if im.width() == 0:
                return
            im_ratio = im.height() / im.width()
            sacle_height = width * im_ratio
            self.help_pushButton.setMinimumSize(width, sacle_height)
            self.help_pushButton.setMaximumSize(width, sacle_height)
            style = 'QPushButton{border-image:url(' + image_path + ');}'
            self.help_pushButton.setStyleSheet(style)

    def reFontSize(self):
        all_w = self.findChildren(QWidget)
        scaleRate = font_size
        for _w in all_w:
            font = _w.font()
            font.setPointSize(font.pointSize() * 1)
            point_size = font.pointSize()
            pixel_size = int(point_size * scaleRate)
            font.setPixelSize(pixel_size)
            if not _w.inherits('QToolBox'):
                _w.setFont(font)

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Escape:
            pass

    def mousePressEvent(self, event):
        pass

    def closeAndBlack(self):
        self.mainWnd.setBlack(False)
        self.close()

    def closeDialog(self):
        animation = QPropertyAnimation(self, b'windowOpacity', self)
        animation.setDuration(200)
        animation.setStartValue(1)
        animation.setEndValue(0)
        animation2 = QPropertyAnimation(self.mainWnd.m_pMask, b'windowOpacity', self.mainWnd.m_pMask)
        animation2.setDuration(200)
        animation2.setStartValue(1)
        animation2.setEndValue(0)
        animation.finished.connect(self.closeAndBlack)
        animation.start()
        animation2.start()


class UpdateSwDialog(QDialog, UpdateSwDialogUi):

    def __init__(self, parent=None, mainWnd=None, cfg=None):
        super(UpdateSwDialog, self).__init__(parent)
        self.setupUi(self)
        self.setWindowFlags(QtCore.Qt.WindowCloseButtonHint | QtCore.Qt.FramelessWindowHint)
        self.parent = parent
        self.mainWnd = mainWnd
        self.cfg = cfg
        self.cancel = False
        current_version = IMMPLATFROM_VER
        for file_name in self.cfg.sections():
            latest_version = self.cfg.get(file_name, 'sw_ver')
            if latest_version > current_version:
                local_path = './sw/' + file_name + '.exe'
                download_path = self.cfg.get(file_name, 'path')
                self.new_version_sw_name = file_name + '.exe'
                break

        descrition = self.cfg.get('immplatform', 'descrition')
        self.base_update_desc_Label.setText(descrition.replace('\\n', '\n'))
        self.update_info_label.setVisible(False)
        self.speed_label.setVisible(False)
        self.changeLanguage(language_chooser.language)
        language_chooser.language_change.connect(lambda val: self.changeLanguage(val))
        self.update_cancel_pushButton.pressed.connect(self.closeDialog)
        self.update_thread = threading.Timer(0.01, self.updateSoftware, None)
        self.update_ok_pushButton.clicked.connect(lambda : self.update_thread.start())
        animation = QPropertyAnimation(self, b'windowOpacity', self)
        animation.setDuration(200)
        animation.setStartValue(0)
        animation.setEndValue(1)
        animation2 = QPropertyAnimation(self.mainWnd.m_pMask, b'windowOpacity', self.mainWnd.m_pMask)
        animation2.setDuration(200)
        animation2.setStartValue(0)
        animation2.setEndValue(1)
        animation.start()
        animation2.start()
        parent_globalPos = self.parent.mapToGlobal(QPoint(0, 0))
        self_globalPos = self.mapToGlobal(QPoint(0, 0))
        x = parent_globalPos.x() - self_globalPos.x() + (self.parent.width() - self.width()) / 2
        y = parent_globalPos.y() - self_globalPos.y() + (self.parent.height() - self.height()) / 2
        self.move(x, y)
        self.reFontSize()

    def updateSoftware(self):
        self.update_ok_pushButton.setEnabled(False)
        self.update_info_label.setVisible(True)
        self.speed_label.setVisible(True)
        current_version = IMMPLATFROM_VER
        latest_version = self.cfg.get('immplatform', 'sw_ver')
        local_path = './sw/immplatform.exe'
        download_path = self.cfg.get('immplatform', 'path')
        print('download_path ', download_path)

        def get_local_file_exists_size(local_path):
            try:
                lsize = os.stat(local_path).st_size
            except:
                lsize = 0

            return lsize

        r = requests.get(download_path, stream=True)
        file_size = int(r.headers['content-length'])

        def down(start):
            if start == 0:
                if os.path.exists(local_path):
                    os.remove(local_path)
            else:
                headers = {'Range': 'bytes=%d-' % start}
                r = requests.get(download_path, stream=True, headers=headers)
                print('file_size', file_size)
                f = open(local_path, 'ab+')
                t0 = time.time()
                last_byte = 0
                for chunk in r.iter_content(chunk_size=1024):
                    t = time.time() - t0
                    if chunk:
                        f.write(chunk)
                        f.flush()
                    if t >= 1:
                        current_downloaded_byte = os.path.getsize(local_path) - start
                        self.sw_update_progressBar.setValue(int(os.path.getsize(local_path) / file_size * 1000))
                        t_byte = current_downloaded_byte - last_byte
                        last_byte = current_downloaded_byte
                        speed = int(t_byte / 1024 / t)
                        self.speed_label.setText(str(speed) + ' Kb/s')
                        t0 = time.time()
                    if self.cancel == True:
                        return

                f.close()
                if get_local_file_exists_size(local_path) < file_size:
                    print('restart', get_local_file_exists_size(local_path), file_size)
                    down(get_local_file_exists_size(local_path))
                if get_local_file_exists_size(local_path) == file_size:
                    self.sw_update_progressBar.setValue(1000)

        down(0)
        print(get_local_file_exists_size(local_path))
        if os.path.isfile('upgrade.bat'):
            os.remove('upgrade.bat')
        self.WriteRestartCmd('immplatform.exe')
        self.update_thread = threading.Timer(0.01, self.updateSoftware, None)

    def WriteRestartCmd(self, exe_name):
        b = open('upgrade.bat', 'w')
        imms_path = os.path.realpath(sys.argv[0])
        path, file = os.path.split(imms_path)
        TempList = '@echo off\n'
        TempList += 'if "%1" == "h" goto begin\n'
        TempList += 'mshta vbscript:createobject("wscript.shell").run("""%~nx0"" h",0)(window.close)&&exit \n'
        TempList += ':begin\n'
        TempList += 'taskkill /pid ' + str(os.getpid()) + ' -f \n'
        TempList += 'if not exist %~dp0sw\\' + exe_name + ' exit \n'
        TempList += 'ping -n 3 127.0.0.1>nul\n'
        TempList += 'del ' + imms_path + '\n'
        TempList += 'move ' + path + '\\sw\\immplatform.exe ' + path + '\n'
        TempList += 'start ' + exe_name + '\n'
        TempList += 'del %0'
        b.write(TempList)
        b.close()
        filename = sys.argv[0]
        print(filename)
        if '.py' not in filename:
            print('run upgrade.bat')
            subprocess.Popen('upgrade.bat')
            os.popen('taskkill.exe /pid:' + str(os.getpid()))

    def reFontSize(self):
        all_w = self.findChildren(QWidget)
        scaleRate = font_size
        for _w in all_w:
            font = _w.font()
            font.setPointSize(font.pointSize() * 1)
            point_size = font.pointSize()
            pixel_size = int(point_size * scaleRate)
            font.setPixelSize(pixel_size)
            if not _w.inherits('QToolBox'):
                _w.setFont(font)

    def changeLanguage(self, language):
        trans = QTranslator()
        trans.load('updatasw_' + language + '.qm', ':/translations')
        app = QApplication.instance()
        app.installTranslator(trans)
        self.retranslateUi(self)
        all_w = self.findChildren(QWidget)
        scaleRate = font_size
        if language == 'zh-cn':
            for _w in all_w:
                font = _w.font()
                font.setFamily('Noto Sans SC Medium')
                _w.setFont(font)

        else:
            if language == 'zh-tc':
                for _w in all_w:
                    font = _w.font()
                    font.setFamily('Noto Sans TC Medium')
                    _w.setFont(font)

            else:
                if language == 'ko':
                    for _w in all_w:
                        font = _w.font()
                        font.setFamily('Noto Sans KR Medium')
                        _w.setFont(font)

                else:
                    if language == 'ja':
                        for _w in all_w:
                            font = _w.font()
                            font.setFamily('Noto Sans JP Medium')
                            _w.setFont(font)

                    elif language == 'en':
                        for _w in all_w:
                            font = _w.font()
                            font.setFamily('Noto Sans SC Medium')
                            _w.setFont(font)

    def mousePressEvent(self, event):
        pass

    def closeAndBlack(self):
        self.cancel = True
        self.update_thread.cancel()
        self.mainWnd.setBlack(False)
        self.close()

    def closeDialog(self):
        animation = QPropertyAnimation(self, b'windowOpacity', self)
        animation.setDuration(200)
        animation.setStartValue(1)
        animation.setEndValue(0)
        animation2 = QPropertyAnimation(self.mainWnd.m_pMask, b'windowOpacity', self.mainWnd.m_pMask)
        animation2.setDuration(200)
        animation2.setStartValue(1)
        animation2.setEndValue(0)
        animation.finished.connect(self.closeAndBlack)
        animation.start()
        animation2.start()


class MenuDialog(QDialog, MenuDialogUi):

    def __init__(self, parent=None, mainWnd=None):
        super(MenuDialog, self).__init__(parent)
        self.setupUi(self)
        self.reFontSize()
        self.changeLanguage(language_chooser.language)
        language_chooser.language_change.connect(lambda val: self.changeLanguage(val))
        self.language_comboBox.removeItem(5)
        self.language_comboBox.removeItem(4)
        self.language_comboBox.removeItem(3)
        self.mainWnd = mainWnd
        self.parent = parent
        self.setWindowFlags(QtCore.Qt.WindowCloseButtonHint | QtCore.Qt.FramelessWindowHint)
        self.config = configparser.ConfigParser(allow_no_value=True)
        self.language_list = [
         'zh-cn', 'zh-tc', 'en', 'ko', 'ja', 'ge']
        self.software_download_path = ''
        self.setDefaultFromCfg()
        self.menu_close_pushButton.clicked.connect(self.closeDialog)
        self.language_comboBox.setView(QListView())
        self.language_comboBox.currentIndexChanged.connect(lambda val: self.setLanguage(val))
        self.autostart_checkBox.toggled.connect(lambda val: self.setAutostart(val))
        self.autostart_checkBox.toggled.connect(lambda val: self.setCfg('menu', 'autostart', str(val)))
        self.minitray_checkBox.toggled.connect(lambda val: self.setCfg('menu', 'minitray', str(val)))
        self.ui_size_buttonGroup.buttonPressed.connect(lambda button: self.app_info(button))
        self.font_size_buttonGroup.buttonPressed.connect(lambda button: self.app_info(button))
        self.platform_version_label.setText(IMMPLATFROM_VER)
        self.movie = QMovie(':/icon/refresh.gif')
        self.movie.frameChanged.connect(lambda : self.software_update_refresh_pushButton.setIcon(QIcon(self.movie.currentPixmap())))
        self.refresh_thread = threading.Timer(0.01, self.software_check_update, None)
        self.software_update_refresh_pushButton.clicked.connect(self.start_refresh_thread)
        self.software_update_refresh_pushButton.clicked.connect(self.refresh_movie_start)
        self.software_update_pushButton.clicked.connect(lambda val: self.closeDialog(update=True))
        self.contact_pushButton.clicked.connect(self.link_handler)
        if self.mainWnd.isMaximized():
            Margins = 0
        else:
            Margins = self.mainWnd.Margins
        rect = self.mainWnd.geometry()
        x, y, w, h = (rect.x(), rect.y(), rect.width(), rect.height())
        self.x = x + Margins
        self.y = y + Margins
        animation = QPropertyAnimation(self, b'geometry', self.parent)
        animation.setDuration(100)
        animation.setStartValue(QRect(0, 0, 84, rect.height() - Margins * 2))
        animation.setEndValue(QRect(0, 0, 230, rect.height() - Margins * 2))
        animation2 = QPropertyAnimation(self.parent, b'windowOpacity', self.parent)
        animation2.setDuration(100)
        animation2.setStartValue(0)
        animation2.setEndValue(1)
        animation.finished.connect(lambda : self.parent.markMousePress.connect(self.closeDialog))
        animation.start()
        animation2.start()

    def start_refresh_thread(self):
        if not self.refresh_thread.is_alive():
            self.refresh_thread = threading.Timer(0.01, self.software_check_update, None)
            self.refresh_thread.start()

    def setAutostart(self, val):
        if val == True:
            AutoRun(switch='open', key_name='immplatform')
        else:
            AutoRun(switch='close', key_name='immplatform')

    def app_info(self, button):
        if language_chooser.language == 'zh-cn':
            self.app_info_label.setText('请重启生效  ')
        else:
            self.app_info_label.setText('Please restart the software  ')
        button_name = button.objectName()
        type, _, size, _ = button_name.split('_')
        self.setCfg('menu', type, size)

    def link_handler(self):
        webbrowser.open_new_tab(self.contact_pushButton.text())

    def refresh_movie_start(self):
        self.movie.start()

    def software_check_update(self):
        time.sleep(0.5)
        current_version = IMMPLATFROM_VER
        self.version_info_label.setStyleSheet('QLabel { \nbackground-color: rgb(40, 40, 40);\ncolor: rgb(169, 255, 47);\n}')
        try:
            html = requests.get('http://47.119.165.12/immplatform/software/sw_desc')
            print(html.text)
            sw_desc = html.text
            self.config.readfp(io.StringIO(sw_desc))
            latest_version = self.config.get('immplatform', 'sw_ver')
            latest_release = self.config.get('immplatform', 'release')
            if latest_version == current_version:
                if language_chooser.language == 'zh-cn':
                    self.version_info_label.setText('已经是最新版本的软件  ')
                else:
                    self.version_info_label.setText('The software is already the latest version  ')
            else:
                if latest_release == 'True':
                    if language_chooser.language == 'zh-cn':
                        self.version_info_label.setText('发现新版本 V' + str(latest_version) + '    ')
                    else:
                        self.version_info_label.setText('Latest version V' + str(latest_version) + '    ')
                    self.software_update_pushButton.setEnabled(True)
        except Exception as e:
            print(e)
            if language_chooser.language == 'zh-cn':
                self.version_info_label.setText('无法连接到远程服务器  ')
            else:
                self.version_info_label.setText('Cannot connect to remote server  ')
            self.version_info_label.setStyleSheet('QLabel { \nbackground-color: rgb(40, 40, 40);\ncolor: rgb(255, 20, 20);\n}')

        self.movie.stop()

    def reFontSize(self):
        all_w = self.findChildren(QWidget)
        scaleRate = font_size
        for _w in all_w:
            font = _w.font()
            font.setPointSize(font.pointSize() * 1)
            point_size = font.pointSize()
            pixel_size = int(point_size * scaleRate)
            font.setPixelSize(pixel_size)
            if not _w.inherits('QToolBox'):
                _w.setFont(font)

    def setCfg(self, sec, opt, val):
        ui_cfg.set(sec, opt, val)
        with open('./cfg/ui_setting.cfg', 'w+') as (f):
            ui_cfg.write(f)

    def setDefaultFromCfg(self):
        language = ui_cfg.get('menu', 'language')
        language_index = self.language_list.index(language)
        self.language_comboBox.setCurrentIndex(language_index)
        autostart = ui_cfg.get('menu', 'autostart')
        minitray = ui_cfg.get('menu', 'minitray')
        self.autostart_checkBox.setChecked(eval(autostart))
        self.minitray_checkBox.setChecked(eval(minitray))
        ui_size = ui_cfg.get('menu', 'ui')
        font_size = ui_cfg.get('menu', 'font')
        if ui_size == 'S':
            self.ui_size_S_radioButton.setChecked(True)
        else:
            if ui_size == 'M':
                self.ui_size_M_radioButton.setChecked(True)
            else:
                if ui_size == 'L':
                    self.ui_size_L_radioButton.setChecked(True)
                if font_size == 'S':
                    self.font_size_S_radioButton.setChecked(True)
                else:
                    if font_size == 'M':
                        self.font_size_M_radioButton.setChecked(True)
                    elif font_size == 'L':
                        self.font_size_L_radioButton.setChecked(True)

    def setLanguage(self, val):
        language = self.language_list[val]
        ui_cfg.set('menu', 'language', language)
        with open('./cfg/ui_setting.cfg', 'w+') as (f):
            ui_cfg.write(f)
        language_chooser.setLanguage(language)

    def changeLanguage(self, language):
        trans = QTranslator()
        trans.load('menu_dialog_' + language + '.qm', ':/translations')
        app = QApplication.instance()
        app.installTranslator(trans)
        self.retranslateUi(self)
        all_w = self.findChildren(QWidget)
        scaleRate = font_size
        if language == 'zh-cn':
            for _w in all_w:
                font = _w.font()
                font.setFamily('Noto Sans SC Medium')
                _w.setFont(font)

        else:
            if language == 'zh-tc':
                for _w in all_w:
                    font = _w.font()
                    font.setFamily('Noto Sans TC Medium')
                    _w.setFont(font)

            else:
                if language == 'ko':
                    for _w in all_w:
                        font = _w.font()
                        font.setFamily('Noto Sans KR Medium')
                        _w.setFont(font)

                else:
                    if language == 'ja':
                        for _w in all_w:
                            font = _w.font()
                            font.setFamily('Noto Sans JP Medium')
                            _w.setFont(font)

                    elif language == 'en':
                        for _w in all_w:
                            font = _w.font()
                            font.setFamily('Noto Sans SC Medium')
                            _w.setFont(font)

    def mousePressEvent(self, event):
        pass

    def closeDialog(self, update=False):
        if self.mainWnd.isMaximized():
            Margins = 0
        else:
            Margins = self.mainWnd.Margins
        rect = self.mainWnd.geometry()
        x, y, w, h = (rect.x(), rect.y(), rect.width(), rect.height())
        self.x = x + Margins
        self.y = y + Margins
        animation = QPropertyAnimation(self, b'geometry', self.parent)
        animation.setDuration(100)
        animation.setStartValue(QRect(0, 0, 230, rect.height() - Margins * 2))
        animation.setEndValue(QRect(0, 0, 84, rect.height() - Margins * 2))
        animation2 = QPropertyAnimation(self.parent, b'windowOpacity', self.parent)
        animation2.setDuration(100)
        animation2.setStartValue(1)
        animation2.setEndValue(0)
        if update:
            animation.finished.connect(self.closeAndopenUpdateSwDialog)
        else:
            animation.finished.connect(self.closeAndBlack)
        animation.start()
        animation2.start()

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Escape:
            pass

    def closeAndBlack(self):
        self.close()
        self.mainWnd.setBlack(False)
        self.parent.markMousePress.disconnect(self.closeDialog)

    def closeAndopenUpdateSwDialog(self):
        self.closeAndBlack()
        self.mainWnd.setBlack(True)
        self.updateSwDialog = UpdateSwDialog(self.mainWnd.m_pMask, self.mainWnd, self.config)
        self.updateSwDialog.show()


import sys
from PyQt5.QtCore import QSize
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt, pyqtSignal, QPoint
from PyQt5.QtGui import QFont, QEnterEvent, QPainter, QColor, QPen
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QSpacerItem, QSizePolicy, QPushButton
from PyQt5.QtGui import QIcon, QScreen
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QTextEdit
StyleSheet = '\n/*标题栏*/\nTitleBar {\n    color: white;\n    background-color: rbg(15, 17, 20);\n}\n/*最小化最大化关闭按钮通用默认背景*/\n#buttonMinimum,#buttonMaximum,#buttonClose {\n    border: none;\n    color: white;\n    background-color: rbg(55, 171, 200);\n}\n/*悬停*/\n#buttonMinimum:hover,#buttonMaximum:hover {\n    background-color: rgb(55, 57, 60);\n    color: white;\n}\n#buttonClose:hover {\n    background-color: rgb(255, 0, 0);\n    color: white;\n}\n/*鼠标按下不放*/\n#buttonMinimum:pressed,#buttonMaximum:pressed {\n    color: white;\n    background-color: rgb(255, 100, 100);\n}\n#buttonClose:pressed {\n    color: white;\n    background-color: rgb(255, 100, 100);\n}\n'

class TitleBar(QWidget):
    windowMinimumed = pyqtSignal()
    windowMaximumed = pyqtSignal()
    windowNormaled = pyqtSignal()
    windowClosed = pyqtSignal()
    windowMoved = pyqtSignal(QPoint)

    def __init__(self, *args, **kwargs):
        (super(TitleBar, self).__init__)(*args, **kwargs)
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.mPos = None
        self.iconSize = 20
        self.setAutoFillBackground(True)
        self.palette = self.palette()
        self.palette.setColor(self.palette.Window, QColor(15, 17, 20))
        self.setPalette(self.palette)
        layout = QHBoxLayout(self, spacing=0)
        layout.setContentsMargins(5, 0, 0, 0)
        self.iconLabel = QLabel(self)
        layout.addWidget(self.iconLabel)
        self.titleLabel = QLabel(self)
        self.titleLabel.setMargin(2)
        title_font = self.font() or QFont()
        title_font.setFamily('Noto Sans SC Medium')
        title_font.setPointSize(8)
        self.titleLabel.setFont(title_font)
        self.titleLabel.setStyleSheet('QLabel { \ncolor: rgb(200, 200, 200);\n}')
        layout.addWidget(self.titleLabel)
        self.infoLabel = QLabel(self)
        self.infoLabel.setMargin(2)
        info_font = self.font() or QFont()
        info_font.setFamily('Noto Sans SC Medium')
        info_font.setPointSize(8)
        self.infoLabel.setFont(info_font)
        self.infoLabel.setStyleSheet('QLabel { \ncolor: rgb(50, 255, 50);\n}')
        layout.addWidget(self.infoLabel)
        layout.addSpacerItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))
        font = self.font() or QFont()
        font.setFamily('Webdings')
        self.buttonMinimum = QPushButton('0', self, clicked=(self.windowMinimumed.emit), font=font, objectName='buttonMinimum')
        layout.addWidget(self.buttonMinimum)
        self.buttonClose = QPushButton('r', self, clicked=(self.windowClosed.emit), font=font, objectName='buttonClose')
        layout.addWidget(self.buttonClose)
        self.setHeight()
        self.reFontSize()

    def changeColor(self, r, g, b):
        self.palette.setColor(self.palette.Window, QColor(r, g, b))
        self.setPalette(self.palette)

    def reFontSize(self):
        all_w = self.findChildren(QWidget)
        scaleRate = font_size
        for _w in all_w:
            font = _w.font()
            font.setPointSize(font.pointSize() * 1)
            point_size = font.pointSize()
            pixel_size = int(point_size * scaleRate)
            font.setPixelSize(pixel_size)
            if not _w.inherits('QToolBox'):
                _w.setFont(font)

    def showMaximized(self):
        if self.buttonMaximum.text() == '1':
            self.buttonMaximum.setText('2')
            self.windowMaximumed.emit()
        else:
            self.buttonMaximum.setText('1')
            self.windowNormaled.emit()

    def setHeight(self, height=22):
        """设置标题栏高度"""
        self.setMinimumHeight(height)
        self.setMaximumHeight(height)
        self.buttonMinimum.setMinimumSize(height, height)
        self.buttonMinimum.setMaximumSize(height, height)
        self.buttonClose.setMinimumSize(height, height)
        self.buttonClose.setMaximumSize(height, height)

    def setTitle(self, title):
        """设置标题"""
        self.titleLabel.setText(title)

    def setInfo(self, info):
        self.infoLabel.setText(info)

    def setIcon(self, icon):
        """设置图标"""
        self.iconLabel.setPixmap(icon.pixmap(self.iconSize, self.iconSize))

    def setIconSize(self, size):
        """设置图标大小"""
        self.iconSize = size

    def enterEvent(self, event):
        self.setCursor(Qt.ArrowCursor)
        super(TitleBar, self).enterEvent(event)

    def mouseDoubleClickEvent(self, event):
        super(TitleBar, self).mouseDoubleClickEvent(event)

    def mousePressEvent(self, event):
        """鼠标点击事件"""
        if event.button() == Qt.LeftButton:
            self.mPos = event.pos()
        event.accept()

    def mouseReleaseEvent(self, event):
        """鼠标弹起事件"""
        self.mPos = None
        event.accept()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton:
            if self.mPos:
                self.windowMoved.emit(self.mapToGlobal(event.pos() - self.mPos))
        event.accept()


Left, Top, Right, Bottom, LeftTop, RightTop, LeftBottom, RightBottom = range(8)

class WindowMark(QWidget):
    markMousePress = pyqtSignal(str)

    def __init__(self, *args, **kwargs):
        (super(WindowMark, self).__init__)(*args, **kwargs)
        self.setWindowFlags(Qt.Window | Qt.FramelessWindowHint | Qt.WindowSystemMenuHint | Qt.WindowMinimizeButtonHint | Qt.WindowMaximizeButtonHint)
        self.setAttribute(Qt.WA_TranslucentBackground, True)

    def paintEvent(self, event):
        super(WindowMark, self).paintEvent(event)
        painter = QPainter(self)
        painter.fillRect(self.rect(), QColor(0, 0, 0, 170))

    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            self.markMousePress.emit('')


class FramelessWindow(QWidget):
    Margins = 5
    screenChanged = QtCore.pyqtSignal(QScreen, QScreen)

    def __init__(self, *args, **kwargs):
        (super(FramelessWindow, self).__init__)(*args, **kwargs)
        self.border_width = 8
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Window)
        self._pressed = False
        self.Direction = None
        self.title_hight = 20
        self.black = False
        self.setMouseTracking(True)
        layout = QVBoxLayout(self, spacing=0)
        layout.setContentsMargins(self.Margins, self.Margins, self.Margins, self.Margins)
        self.titleBar = TitleBar(self)
        layout.addWidget(self.titleBar)
        self.titleBar.windowMinimumed.connect(self.Minimized)
        self.titleBar.windowNormaled.connect(self.showNormal)
        self.titleBar.windowClosed.connect(self.Close)
        self.titleBar.windowMoved.connect(self.move)
        self.windowTitleChanged.connect(self.titleBar.setTitle)
        self.windowIconChanged.connect(self.titleBar.setIcon)
        self.m_pMask = WindowMark(self)
        self.m_pMask.setStyleSheet("QComboBox\n{\nbackground-color: rgb(255, 255, 255);\nborder: 1px solid;\nborder-color: rgb(221, 221, 221);\nborder-radius: 2px;\ncolor: rgb(40, 40, 80);\ntext-align:center;\n}\n\n\n\nQComboBox::drop-down{border-style: none;}\n\n\nQComboBox QAbstractItemView{\nborder: 0px;\noutline:0px;\nselection-background-color: rgb(55,171,200);\nbackground: rgb(1,58,80);\ncolor: rgb(255, 255, 255);\nfont-size:9px;\nfont-weight:bold;\nfont-family:'Bahnschrift SemiLight';\n}\n\nQComboBox QAbstractItemView::item{\nmin-height: 20px;\nmax-height: 20px;\n}")
        self.titleBar.windowMinimumed.connect(self.setBlackUi)
        self.titleBar.windowMaximumed.connect(self.setBlackUi)
        self.titleBar.windowNormaled.connect(self.setBlackUi)
        self.titleBar.windowMoved.connect(self.setBlackUi)
        self.tray_icon = TrayIcon(self)
        self.tray_icon.show()

    def Close(self):
        self.tray_icon.quit()
        self.tray_icon = None
        self.close()
        print('tray Close')

    def Minimized(self):
        tray_flag = eval(ui_cfg.get('menu', 'minitray'))
        if tray_flag == True:
            self.hide()
            self.tray_icon.show()
        else:
            self.showMinimized()

    def setBlackUi(self):
        if self.isMaximized():
            Margins = 0
        else:
            Margins = self.Margins
        rect = self.geometry()
        x, y, w, h = (rect.x(), rect.y(), rect.width(), rect.height())
        self.m_pMask.setGeometry(x + Margins, y + Margins, self.width() - Margins * 2, self.height() - Margins * 2)
        if self.black == True:
            self.m_pMask.show()
        else:
            self.m_pMask.hide()

    def setBlack(self, flag):
        self.black = flag
        self.setBlackUi()

    def setTitleBarHeight(self, height=20):
        """设置标题栏高度"""
        self.titleBar.setHeight(height)
        self.title_hight = height

    def setIconSize(self, size):
        """设置图标的大小"""
        self.titleBar.setIconSize(size)

    def setWidget(self, widget):
        """设置自己的控件"""
        if hasattr(self, '_widget'):
            return
        self._widget = widget
        self._widget.setAutoFillBackground(True)
        palette = self._widget.palette()
        palette.setColor(palette.Window, QColor(20, 20, 20))
        self._widget.setPalette(palette)
        self._widget.installEventFilter(self)
        self.layout().addWidget(self._widget)

    def move(self, pos):
        if self.windowState() == Qt.WindowMaximized or self.windowState() == Qt.WindowFullScreen:
            return
        super(FramelessWindow, self).move(pos)
        desktop = QApplication.desktop()
        screen_count = desktop.screenCount()

    def showMaximized(self):
        super(FramelessWindow, self).showMaximized()
        self.layout().setContentsMargins(0, 0, 0, 0)

    def showNormal(self):
        super(FramelessWindow, self).showNormal()
        self.layout().setContentsMargins(self.Margins, self.Margins, self.Margins, self.Margins)

    def eventFilter(self, obj, event):
        if isinstance(event, QEnterEvent):
            self.setCursor(Qt.ArrowCursor)
        return super(FramelessWindow, self).eventFilter(obj, event)

    def paintEvent(self, event):
        super(FramelessWindow, self).paintEvent(event)
        painter = QPainter(self)
        painter.setPen(QPen(QColor(255, 255, 255, 1), 2 * self.Margins))
        painter.drawRect(self.rect())
        path = QPainterPath()
        path.setFillRule(Qt.WindingFill)
        pat = QPainter(self)
        pat.setRenderHint(pat.Antialiasing)
        pat.fillPath(path, QBrush(Qt.white))
        color = QColor(50, 50, 50, 50)
        for i in range(10):
            i_path = QPainterPath()
            i_path.setFillRule(Qt.WindingFill)
            ref = QRectF(10 - i, 10 - i, self.width() - (10 - i) * 2, self.height() - (10 - i) * 2)
            i_path.addRoundedRect(ref, self.border_width, self.border_width)
            color.setAlpha(150 - i ** 0.5 * 50)
            pat.setPen(color)
            pat.drawPath(i_path)

        pat2 = QPainter(self)
        pat2.setRenderHint(pat2.Antialiasing)
        pat2.setBrush(Qt.white)
        pat2.setPen(Qt.transparent)
        rect = self.rect()
        rect.setLeft(9)
        rect.setTop(9)
        rect.setWidth(rect.width() - 9)
        rect.setHeight(rect.height() - 9)
        pat2.drawRoundedRect(rect, 4, 4)

    def mousePressEvent(self, event):
        super(FramelessWindow, self).mousePressEvent(event)
        if event.button() == Qt.LeftButton:
            self._mpos = event.pos()
            self._pressed = True

    def mouseReleaseEvent(self, event):
        super(FramelessWindow, self).mouseReleaseEvent(event)
        self._pressed = False
        self.Direction = None

    def mouseMoveEvent(self, event):
        super(FramelessWindow, self).mouseMoveEvent(event)
        pos = event.pos()
        xPos, yPos = pos.x(), pos.y()
        wm, hm = self.width() - self.Margins, self.height() - self.Margins

    def _resizeWidget(self, pos):
        """调整窗口大小"""
        if self.Direction == None:
            return
        mpos = pos - self._mpos
        xPos, yPos = mpos.x(), mpos.y()
        geometry = self.geometry()
        x, y, w, h = (geometry.x(), geometry.y(), geometry.width(), geometry.height())
        if self.Direction == LeftTop:
            if w - xPos > self.minimumWidth():
                x += xPos
                w -= xPos
            if h - yPos > self.minimumHeight():
                y += yPos
                h -= yPos
        elif self.Direction == RightBottom:
            if w + xPos > self.minimumWidth():
                w += xPos
                self._mpos = pos
            if h + yPos > self.minimumHeight():
                h += yPos
                self._mpos = pos
        else:
            if self.Direction == RightTop:
                if h - yPos > self.minimumHeight():
                    y += yPos
                    h -= yPos
                if w + xPos > self.minimumWidth():
                    w += xPos
                    self._mpos.setX(pos.x())
            else:
                if self.Direction == LeftBottom:
                    if w - xPos > self.minimumWidth():
                        x += xPos
                        w -= xPos
                    if h + yPos > self.minimumHeight():
                        h += yPos
                        self._mpos.setY(pos.y())
                else:
                    if self.Direction == Left:
                        if w - xPos > self.minimumWidth():
                            x += xPos
                            w -= xPos
                        else:
                            return
                    else:
                        if self.Direction == Right:
                            if w + xPos > self.minimumWidth():
                                w += xPos
                                self._mpos = pos
                            else:
                                return
                        else:
                            if self.Direction == Top:
                                if h - yPos > self.minimumHeight():
                                    y += yPos
                                    h -= yPos
                                else:
                                    return
                            else:
                                if self.Direction == Bottom:
                                    if h + yPos > self.minimumHeight():
                                        h += yPos
                                        self._mpos = pos
                                    else:
                                        return
            self.setGeometry(x, y, w, h)
            self.setBlackUi()

    def closeEvent(self, event):
        self._widget.close()


class TrayIcon(QtWidgets.QSystemTrayIcon):

    def __init__(self, MainWindow, parent=None):
        super(TrayIcon, self).__init__(parent)
        self.ui = MainWindow
        self.createMenu()

    def createMenu(self):
        self.menu = QtWidgets.QMenu()
        font = self.menu.font()
        font.setPointSize(font.pointSize() * 1)
        point_size = font.pointSize()
        scaleRate = font_size
        pixel_size = int(point_size * scaleRate)
        font.setPixelSize(pixel_size)
        self.menu.setFont(font)
        self.quitAction = QtWidgets.QAction('Exit', self, triggered=(self.quit))
        self.menu.addAction(self.quitAction)
        self.setContextMenu(self.menu)
        self.setIcon(QIcon(':/icon/imms_b.png'))
        self.icon = self.MessageIcon()
        self.activated.connect(self.onIconClicked)

    def showMsg(self):
        self.showMessage('Message', 'skr at here', self.icon)

    def show_window(self):
        self.ui.showNormal()
        self.ui.activateWindow()

    def quit(self):
        QtWidgets.qApp.quit()
        self.ui.m_pMask.hide()
        self.ui.close()
        os.popen('taskkill.exe /pid:' + str(os.getpid()))

    def onIconClicked(self, reason):
        if language_chooser.language == 'zh-cn':
            self.quitAction.setText('退出')
        else:
            if language_chooser.language == 'en':
                self.quitAction.setText('Exit')
        if reason == 2 or reason == 3:
            if self.ui.isMinimized() or not self.ui.isVisible():
                self.ui.showNormal()
                self.ui.activateWindow()
                self.ui.setWindowFlags(QtCore.Qt.FramelessWindowHint)
                self.ui.show()


class MainWindow(QWidget):

    def __init__(self, *args, **kwargs):
        (super(MainWindow, self).__init__)(*args, **kwargs)
        self.mainWnd = args[0]
        self.gridLayout = QtWidgets.QGridLayout(self)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setSpacing(1)
        self.gridLayout.setObjectName('gridLayout')
        self.ConnectInfoDialog = None
        self.base_connect_ui = ConnectInfoDialog2('没有发现IMMBASE设备', 'No IMMBASE device found')
        self.hub_connect_ui = ConnectInfoDialog2('没有发现IMMHUB设备', 'No IMMHUB device found')
        self.gforce_connect_ui = ConnectInfoDialog2('没有发现IMMGFORCE设备', 'No IMMGFORCE device found')
        self.dashchooser = pyDash.DashChooser(main=self, ui_cfg=ui_cfg)
        self.hub_hidchooser = hub_hid_ui.HubHidChooser(usb_vid=IMMS_HUB_VID, usb_pid=IMMS_HUB_PID, dash=(self.dashchooser))
        self.hidchooser = hid_ui.HidChooser(dash=(self.dashchooser), usb_vid=IMMS_BASE_VID, usb_pid=IMMS_BASE_PID, hub_hidchooser=(self.hub_hidchooser))
        self.gforce_hidchooser = gforce_hid_ui.GForceHidChooser(usb_vid=IMMS_GFORCE_VID, usb_pid=IMMS_GFORCE_PID, dash=(self.dashchooser))
        self.main_ui = MainMenuUi(self.mainWnd, self.hidchooser, self.hub_hidchooser, self.gforce_hidchooser, self.dashchooser)
        self.base_ui = MainBaseUi(self.mainWnd, self.hidchooser, self.hub_hidchooser, self.dashchooser)
        self.hub_ui = MainHubUi(self.mainWnd, self.hidchooser, self.hub_hidchooser, self.dashchooser, self.base_ui)
        self.gofrce_ui = MainGforceUi(self.mainWnd, self.hidchooser, self.gforce_hidchooser, self.dashchooser)
        self.preset_ui = MainPresetUi(self.mainWnd, self.main_ui, self.dashchooser)
        self.gridLayout.addWidget(self.main_ui, 0, 0, 1, 1)
        self.main_ui.base_gridLayout.addWidget(self.base_connect_ui, 1, 0, 1, 1)
        self.main_ui.hub_gridLayout.addWidget(self.hub_connect_ui, 1, 0, 1, 1)
        self.main_ui.gforce_gridLayout.addWidget(self.gforce_connect_ui, 1, 0, 1, 1)
        self.main_ui.menu_pushButton.clicked.connect(self.openMenu)
        self.hidchooser.connectStatusChange.connect(lambda val: self.base_connect(val))
        self.hub_hidchooser.connectStatusChange.connect(lambda val: self.hub_connect(val))
        self.gforce_hidchooser.connectStatusChange.connect(lambda val: self.gforce_connect(val))

    def changeBasePage(self, status):
        if status == CONNECT_STATUS_RUNNING:
            self.main_ui.immbase_radioButton.setText('BASE - ' + self.hidchooser.getModel() + ' ')
        else:
            self.main_ui.immbase_radioButton.setText('BASE ')

    def changeHubPage(self, status):
        if status == CONNECT_STATUS_RUNNING:
            self.main_ui.immhub_radioButton.setText('HUB - ' + self.hub_hidchooser.getModel() + ' ')
        else:
            self.main_ui.immhub_radioButton.setText('HUB ')

    def changePresetPage(self, status):
        if status == 'None':
            self.main_ui.preset_radioButton.setText('PRESET ')
        else:
            self.main_ui.preset_radioButton.setText('PRESET - ' + status + ' ')

    def openMenu(self):
        self.mainWnd.setBlack(True)
        child_win = MenuDialog(self.mainWnd.m_pMask, self.mainWnd)
        child_win.show()

    def base_connect(self, status):
        if status != CONNECT_STATUS_FAULT:
            self.main_ui.base_gridLayout.removeWidget(self.base_connect_ui)
            self.base_ui.setParent(None)
            self.main_ui.base_gridLayout.addWidget(self.base_ui, 1, 0, 1, 1)
            self.main_ui.preset_radioButton.setVisible(True)
            if self.main_ui.preset_gridLayout.itemAt(0) == None:
                self.main_ui.preset_gridLayout.addWidget(self.preset_ui, 1, 0, 1, 1)
        else:
            self.base_ui.base_update_pushButton.setEnabled(False)
            self.base_ui.base_update_boot_pushButton.setEnabled(False)
            self.base_ui.base_boot_update_info_label.setText('')
            self.base_ui.boot_update_ver_label.setText('')
            self.base_ui.base_update_info_label.setText('')
            self.base_ui.update_ver_label.setText('')
            self.base_ui.base_desc_label.setVisible(False)
            self.base_ui.base_boot_desc_label.setVisible(False)
            self.base_ui.base_update_desc_Label.setText('')
            self.base_ui.base_boot_update_desc_Label.setText('')
            self.base_ui.fw_boot_path_lineEdit.setText('')
            self.base_ui.fw_path_lineEdit.setText('')

    def hub_connect(self, status):
        if status != CONNECT_STATUS_FAULT:
            self.main_ui.hub_gridLayout.removeWidget(self.hub_connect_ui)
            self.hub_ui.setParent(None)
            self.main_ui.hub_gridLayout.addWidget(self.hub_ui, 1, 0, 1, 1)
            self.main_ui.preset_radioButton.setVisible(True)
            if self.main_ui.preset_gridLayout.itemAt(0) == None:
                self.main_ui.preset_gridLayout.addWidget(self.preset_ui, 1, 0, 1, 1)
        else:
            self.hub_ui.hub_update_pushButton.setEnabled(False)
            self.hub_ui.hub_update_boot_pushButton.setEnabled(False)
            self.hub_ui.hub_boot_update_info_label.setText('')
            self.hub_ui.boot_update_ver_label.setText('')
            self.hub_ui.hub_update_info_label.setText('')
            self.hub_ui.update_ver_label.setText('')
            self.hub_ui.hub_desc_label.setVisible(False)
            self.hub_ui.hub_boot_desc_label.setVisible(False)
            self.hub_ui.hub_update_desc_Label.setText('')
            self.hub_ui.hub_boot_update_desc_Label.setText('')

    def gforce_connect(self, status):
        self.main_ui.gforce_gridLayout.removeWidget(self.gforce_connect_ui)
        self.gofrce_ui.setParent(None)
        self.main_ui.gforce_gridLayout.addWidget(self.gofrce_ui, 1, 0, 1, 1)

    def openConnectInofDialog(self, status):
        if status == CONNECT_STATUS_FAULT:
            self.ConnectInfoDialog = ConnectInfoDialog(self.mainWnd.m_pMask, self.mainWnd)
        else:
            self.mainWnd.setBlack(False)
        if self.ConnectInfoDialog:
            self.ConnectInfoDialog.hide()

    def closeEvent(self, event):
        self.main_ui.close()
        self.base_ui.close()
        self.hub_ui.close()
        self.preset_ui.close()
        self.dashchooser.__del__()
        self.hidchooser.__del__()
        self.hub_hidchooser.__del__()
        self.gforce_hidchooser.__del__()


class ErrorDialog(QDialog, ErrorDialogUi):

    def __init__(self, info=''):
        super(ErrorDialog, self).__init__()
        self.setupUi(self)
        self.info = info
        self.error_info_Label.setText(self.info)
        self.setWindowFlags(QtCore.Qt.WindowCloseButtonHint | QtCore.Qt.FramelessWindowHint)
        self.changeLanguage(language_chooser.language)
        language_chooser.language_change.connect(lambda val: self.changeLanguage(val))
        self.exit_pushButton.pressed.connect(self.close)
        self.reFontSize()

    def reFontSize(self):
        all_w = self.findChildren(QWidget)
        scaleRate = font_size
        for _w in all_w:
            font = _w.font()
            font.setPointSize(font.pointSize() * 1)
            point_size = font.pointSize()
            pixel_size = int(point_size * scaleRate)
            font.setPixelSize(pixel_size)
            if not _w.inherits('QToolBox'):
                _w.setFont(font)

    def changeLanguage(self, language):
        trans = QTranslator()
        trans.load('updatafw_' + language + '.qm', ':/translations')
        app = QApplication.instance()
        app.installTranslator(trans)
        self.retranslateUi(self)
        all_w = self.findChildren(QWidget)
        scaleRate = font_size
        if language == 'zh-cn':
            for _w in all_w:
                font = _w.font()
                font.setFamily('Noto Sans SC Medium')
                _w.setFont(font)

        else:
            if language == 'zh-tc':
                for _w in all_w:
                    font = _w.font()
                    font.setFamily('Noto Sans TC Medium')
                    _w.setFont(font)

            else:
                if language == 'ko':
                    for _w in all_w:
                        font = _w.font()
                        font.setFamily('Noto Sans KR Medium')
                        _w.setFont(font)

                else:
                    if language == 'ja':
                        for _w in all_w:
                            font = _w.font()
                            font.setFamily('Noto Sans JP Medium')
                            _w.setFont(font)

                    elif language == 'en':
                        for _w in all_w:
                            font = _w.font()
                            font.setFamily('Noto Sans SC Medium')
                            _w.setFont(font)


import math

def sign(val):
    return (0 < val) - (val < 0)


def lugref_ss(v, Fc, Fs, vs, sigma_2):
    r = -(v / vs) * (v / vs)
    Fss = Fc * sign(v) + (Fs - Fc) * math.exp(r) * sign(v) + sigma_2 * v
    return Fss


z = 0

def lugref(v, Fc, Fs, vs, sigma_0, sigma_1, sigma_2, ts):
    global z
    r = -(v / vs) ** 2
    g_v = Fc + (Fs - Fc) * math.exp(r)
    z_dot = v - sigma_0 * abs(v) * z / g_v
    z = z + z_dot * ts
    F = sigma_0 * z + sigma_1 * z_dot + sigma_2 * v
    return F


def Sigmoid(x):
    return 1 / (1 + math.exp(-x))


def Tanh(x, t):
    if t > 0:
        if x <= 0:
            x = 1
    else:
        if t < 0:
            if x >= 0:
                x = -1
    a = math.pow(x / t, -100) + 1
    if a >= 500:
        a = 500
    return a


import math

def setServoPosition(pitchAngle, rollAngle, offset):
    PI = 3.14159
    centerLength = 75
    pitchAngle = pitchAngle / 360 * 2 * PI
    rollAngle = rollAngle / 360 * 2 * PI
    P1setpoint = math.sqrt(3) * centerLength / 6.0 * math.sin(pitchAngle) * math.cos(rollAngle) + centerLength / 2.0 * math.sin(rollAngle) + offset
    P2setpoint = math.sqrt(3) * centerLength / 6.0 * math.sin(pitchAngle) * math.cos(rollAngle) - centerLength / 2.0 * math.sin(rollAngle) + offset
    P3setpoint = -math.sqrt(3) * centerLength / 3.0 * math.sin(pitchAngle) * math.cos(rollAngle) + offset
    P4setpoint = -(math.sqrt(3) * centerLength / 6.0) * math.sin(pitchAngle) * math.cos(rollAngle) + centerLength / 2.0 * math.sin(rollAngle) + offset
    P5setpoint = -math.sqrt(3) * centerLength / 6.0 * math.sin(pitchAngle) * math.cos(rollAngle) - centerLength / 2.0 * math.sin(rollAngle) + offset
    print(P1setpoint, P2setpoint, P3setpoint, P4setpoint, P5setpoint)


def write_key():
    """
    Generates a key and save it into a file
    """
    key = Fernet.generate_key()
    print(key)
    with open('key.key', 'wb') as (key_file):
        key_file.write(key)


def encrypt(filename, key):
    """
    Given a filename (str) and key (bytes), it encrypts the file and write it
    """
    f = Fernet(key)
    with open(filename, 'rb') as (file):
        file_data = file.read()
    encrypted_data = f.encrypt(file_data)
    with open(filename, 'wb') as (file):
        file.write(encrypted_data)


def adecrypt(filename, key):
    """
    Given a filename (str) and key (bytes), it decrypts the file and write it
    """
    bin_buf = []
    f = Fernet(key)
    with open(filename, 'rb') as (file):
        encrypted_data = file.read()
    decrypted_data = f.decrypt(encrypted_data)
    for data in decrypted_data:
        bin_buf.append(data)

    with open(filename, 'wb') as (file):
        file.write(decrypted_data)


if __name__ == '__main__':
    sigma_0 = 500000.0
    sigma_1 = math.sqrt(1000000.0)
    sigma_2 = 0.0
    Fc = 1.0
    Fs = 1.0
    vs = 0.001
    ts = 0.001
    import struct
    x = struct.pack('>Q', 149542137757696)
    try:
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, 'System\\CurrentControlSet\\Control\\MediaProperties\\PrivateProperties\\Joystick\\OEM\\VID_0126&PID_C005', 0, winreg.KEY_SET_VALUE)
        winreg.SetValueEx(key, 'OEMData', None, winreg.REG_BINARY, x)
    except Exception as e:
        print(e)

    try:
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, 'System\\CurrentControlSet\\Control\\MediaProperties\\PrivateProperties\\Joystick\\OEM\\VID_0126&PID_C001', 0, winreg.KEY_SET_VALUE)
        winreg.SetValueEx(key, 'OEMData', None, winreg.REG_BINARY, x)
    except Exception as e:
        print(e)

    try:
        key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, 'System\\CurrentControlSet\\Control\\MediaProperties\\PrivateProperties\\Joystick\\OEM\\VID_0126&PID_C005', 0, winreg.KEY_SET_VALUE)
        winreg.SetValueEx(key, 'OEMData', None, winreg.REG_BINARY, x)
    except Exception as e:
        print(e)

    try:
        key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, 'System\\CurrentControlSet\\Control\\MediaProperties\\PrivateProperties\\Joystick\\OEM\\VID_0126&PID_C001', 0, winreg.KEY_SET_VALUE)
        winreg.SetValueEx(key, 'OEMData', None, winreg.REG_BINARY, x)
    except Exception as e:
        print(e)

    try:
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, 'System\\CurrentControlSet\\Control\\MediaProperties\\PrivateProperties\\Joystick\\OEM\\VID_046D&PID_C24F', 0, winreg.KEY_SET_VALUE)
        winreg.SetValueEx(key, 'OEMData', None, winreg.REG_BINARY, x)
    except Exception as e:
        print(e)

    print('process 1')

    def admin_exe():
        forza_install = Judge_Key('DisplayName', win32con.HKEY_CURRENT_USER, 'SOFTWARE\\Classes\\Local Settings\\Software\\Microsoft\\Windows\\CurrentVersion\\AppContainer\\Mappings\\S-1-15-2-4229748693-3326341846-1495081741-1528692508-1131203849-336638721-4261848658', None)
        if forza_install == 1:
            s = execute_cmd('CheckNetIsolation.exe LoopbackExempt -s')
            fh4_uwp_udp_ok = ' microsoft.sunrisebasegame_8wekyb3d8bbwe' in s
            if not fh4_uwp_udp_ok:
                os.system('CheckNetIsolation.exe LoopbackExempt -a -n=Microsoft.SunriseBaseGame_8wekyb3d8bbwe')
        forza_install = Judge_Key('DisplayName', win32con.HKEY_CURRENT_USER, 'SOFTWARE\\Classes\\Local Settings\\Software\\Microsoft\\Windows\\CurrentVersion\\AppContainer\\Mappings\\S-1-15-2-456837355-4097594857-4023660634-3351830381-3037171157-549978347-723580371', None)
        if forza_install == 1:
            s = execute_cmd('CheckNetIsolation.exe LoopbackExempt -s')
            fh5_uwp_udp_ok = ' microsoft.624f8b84b80_8wekyb3d8bbwe' in s
            if not fh5_uwp_udp_ok:
                os.system('CheckNetIsolation.exe LoopbackExempt -a -p=S-1-15-2-456837355-4097594857-4023660634-3351830381-3037171157-549978347-723580371')


    try:
        admin_exe()
    except Exception as e:
        print('admin_exe error ', e)

    print('process 2')

    def get_real_resolution():
        """获取真实的分辨率"""
        hDC = win32gui.GetDC(0)
        w = win32print.GetDeviceCaps(hDC, win32con.DESKTOPHORZRES)
        h = win32print.GetDeviceCaps(hDC, win32con.DESKTOPVERTRES)
        return (w, h)


    def get_screen_size():
        """获取缩放后的分辨率"""
        w = GetSystemMetrics(0)
        h = GetSystemMetrics(1)
        return (w, h)


    print('process 3')
    hostname = socket.gethostname()
    ip = socket.gethostbyname(hostname)

    def get_mac_address():
        mac = uuid.UUID(int=(uuid.getnode())).hex[-12:]
        return ':'.join([mac[e:e + 2] for e in range(0, 11, 2)])


    print('process 4')
    real_resolution = get_real_resolution()
    screen_size = get_screen_size()
    screen_scale_rate = round(real_resolution[0] / screen_size[0] * ui_size, 2)
    QGuiApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)
    print('process 5')
    os.environ['QT_SCALE_FACTOR'] = str(screen_scale_rate)
    app = QApplication(sys.argv)
    _id = QFontDatabase.addApplicationFont(':/font/NotoSansSC-Medium.otf')
    _id = QFontDatabase.addApplicationFont(':/font/NotoSansTC-Medium.otf')
    _id = QFontDatabase.addApplicationFont(':/font/NotoSansKR-Medium.otf')
    _id = QFontDatabase.addApplicationFont(':/font/NotoSansJP-Medium.otf')
    _id = QFontDatabase.addApplicationFont(':/font/Formula1-Wide.otf')
    print('process 6')
    pid = None
    for p in process_iter():
        if p.pid in [Process().pid, Process().ppid()]:
            pass
        else:
            try:
                if p.cmdline() == Process().cmdline():
                    pid = p.pid
                    break
            except:
                pass

    print('process 7')
    if pid:
        a = ErrorDialog('Cannot open immplatform repeatedly !')
        a.show()
    else:
        app.setStyleSheet(StyleSheet)
        mainWnd = FramelessWindow()
        mainWnd.setWindowTitle('IMMPLATFORM')
        mainWnd.setIconSize(12)
        mainWnd.setWindowIcon(QIcon(':/icon/imms_b.png'))
        mainWnd.setWidget(MainWindow(mainWnd))
        mainWnd.setMinimumSize(1080, 580)
        mainWnd.setMaximumSize(1080, 580)
        mainWnd.resize(1080, 580)
        mainWnd.show()
    sys.exit(app.exec_())
