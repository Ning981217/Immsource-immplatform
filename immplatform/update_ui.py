from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5 import QtCore
from PyQt5.QtCore import QTimer
from PyQt5.QtSerialPort import QSerialPort, QSerialPortInfo
from PyQt5.QtCore import QIODevice, pyqtSignal
from PyQt5.QtGui import QTransform, QPixmap
import os, time, main
from base_ui import WidgetUI
from setting_ui import SettingChooser
import pyDash, comthread
from PyQt5 import uic
from setting_define import *
from uitl import Utiliy
from uitl import Refresher
from helper import res_path
import binascii

class UpdateDialog(QDialog, Utiliy):

    def __init__(self, parent=None, main=None, base_hidchooser=None, hub_hidchooser=None):
        QDialog.__init__(self, parent)
        self.setWindowFlags(QtCore.Qt.WindowCloseButtonHint)
        uic.loadUi(res_path('update.ui'), self)
        self.main = main
        self.base_hidchooser = base_hidchooser
        self.hub_hidchooser = hub_hidchooser
        self.ver_path_dic = {}
        self.getDownloadedBin()
        self.comThread = comthread.ComthreadChooser(self.base_hidchooser, self)
        self.setConnect()

    def setConnect(self):
        self.base_update_pushButton.clicked.connect(lambda : self.on_pushButtonOpenFile_clicked())

    def getDownloadedBin(self):
        connected_base_model = 'UNKNOW'
        connected_hub_model = 'UNKNOW'
        base_model = self.base_hidchooser.getHIDProductName()
        hub_model = None
        if 'ET5' in base_model:
            connected_base_model = 'ET5'
        else:
            if 'ET3' in base_model:
                connected_base_model = 'ET3'
            else:
                print('connected_base_model', connected_base_model)
                if connected_base_model != 'UNKNOW':
                    self.base_model_label.setStyleSheet('color:green')
                else:
                    self.base_model_label.setStyleSheet('color:red')
            if connected_hub_model != 'UNKNOW':
                self.hub_model_label.setStyleSheet('color:green')
            else:
                self.hub_model_label.setStyleSheet('color:red')
        self.base_model_label.setText(connected_base_model)
        self.hub_model_label.setText(connected_hub_model)
        dir = './fw'
        files = os.listdir(dir)
        for file in files:
            file_name, file_ext = os.path.splitext(file)
            device_type, bin_model, version = file_name.split('_')
            if device_type.upper() == 'BASE' and bin_model.upper() == connected_base_model:
                self.base_bin_comboBox.addItem(version)
                self.ver_path_dic[version] = dir + '/' + file
            else:
                if device_type.upper() == 'HUB' and bin_model.upper() == connected_hub_model:
                    self.hub_bin_comboBox.addItem(version)

    def on_pushButtonSndFile_clicked(self):
        self.comThread.cmdId = CMD_SND_FILE_DATA

    def on_actionStartApp_triggered(self):
        self.comThread.cmdId = CMD_START_APP

    def on_actionGetVer_triggered(self):
        self.comThread.cmdId = CMD_GET_VERSION

    def on_pushButtonOpenFile_clicked(self):
        update_ver = self.base_bin_comboBox.currentText()
        update_bin_path = self.ver_path_dic[update_ver]
        file_size = os.path.getsize(update_bin_path)
        print(file_size)
        bin_buf = []
        with open(update_bin_path, 'rb') as (f):
            while True:
                strb = f.read(1)
                if strb == b'':
                    break
                hexstr = binascii.b2a_hex(strb)
                bin_buf.append(int(str(hexstr, 'utf-8'), 16))

        if APP_MAX_SIZE < file_size:
            return
        self.comThread.fileSize = file_size
        self.comThread.fileHexBuf = bin_buf
        f.close()
        self.on_pushButtonSndFile_clicked()
