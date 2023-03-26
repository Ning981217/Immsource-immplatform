from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5 import QtCore
from PyQt5.QtCore import QTimer
from PyQt5.QtSerialPort import QSerialPort, QSerialPortInfo
from PyQt5.QtCore import QIODevice, pyqtSignal, QByteArray
from PyQt5.QtGui import QTransform, QPixmap
import os, time, main
from base_ui import WidgetUI
from setting_ui import SettingChooser
from setting_define import *
from crc import *
from uitl import Refresher
import threading, goto
from dominate.tags import label
from goto import with_goto

class ComthreadChooser(QObject):
    updateFinish = pyqtSignal(int)

    def __init__(self, hidchooser, main):
        super(ComthreadChooser, self).__init__()
        self.main = main
        self.hidchooser = hidchooser
        self.cmdId = CMD_NON
        self.fileSize = 0
        self.fileHexBuf = []
        self.uploaded_buff_num = 0
        self.HID_BUF_SIZE = 64
        self.close = False
        self.update_bar_thread = Refresher(0.1)
        self.update_bar_thread.sinOut.connect(self.getUploadPercent)
        self.update_bar_thread.start()
        self.first_run = True
        self.start_ota = False
        t1 = threading.Timer(0.1, self.update_run, None)
        t1.start()

    def __del__(self):
        self.close = True
        self.start_ota = False
        self.update_bar_thread.__del__()
        del self

    @with_goto
    def update_run(self):
        while not self.close:
            time.sleep(0.001)
            if self.hidchooser.usbhidConnected() == CONNECT_STATUS_OTA or self.hidchooser.usbhidConnected() == CONNECT_STATUS_RUNNING and self.hidchooser.updata_boot_flag == True:
                if self.hidchooser.usbhidConnected() == CONNECT_STATUS_OTA:
                    self.HID_BUF_SIZE = 64
                elif self.hidchooser.usbhidConnected() == CONNECT_STATUS_RUNNING:
                    if self.hidchooser.updata_boot_flag == True:
                        self.HID_BUF_SIZE = 63
                self.start_ota = True
                if self.first_run == True:
                    time.sleep(2)
                    self.first_run = False
                blk_cnt = 0
                re_send = 0
                if self.cmdId == CMD_START_APP:
                    self.cmdId = CMD_NON
                    re_send = 0
                    while self.cmdFileSndEnd() != True:
                        if RE_SEND_TOTAL > re_send:
                            if not self.close:
                                re_send = re_send + 1
                                print('重新发送', re_send)

                    self.hidchooser.updata_boot_flag = False
                elif self.cmdId == CMD_GET_VERSION:
                    self.cmdId = CMD_NON
                    re_send = 0
                    while self.cmdGetIapVer() != True:
                        if RE_SEND_TOTAL > re_send:
                            if not self.close:
                                re_send = re_send + 1
                                print('重新发送', re_send)

                elif self.cmdId == CMD_SND_FILE_DATA:
                    label.begin
                    self.cmdId = CMD_NON
                    self.uploaded_buff_num = 0
                    re_send = 0
                    print('数据传输准备')
                    while self.cmdFileInfo() != True:
                        if RE_SEND_TOTAL > re_send:
                            if not self.close:
                                re_send = re_send + 1
                                print('重新发送', re_send)

                    if re_send >= RE_SEND_TOTAL:
                        goto.begin
                    blk_cnt = 0
                    while blk_cnt < self.fileSize / BLK_SIZE - 1:
                        if not self.close:
                            re_send = 0
                            while self.cmdBlkSndStart(blk_cnt, BLK_SIZE) != True:
                                if RE_SEND_TOTAL > re_send:
                                    if not self.close:
                                        re_send = re_send + 1
                                        print('重新发送', re_send)

                            if re_send >= RE_SEND_TOTAL:
                                goto.begin
                            re_send = 0
                            while self.cmdBlkSndData(self.fileHexBuf[blk_cnt * BLK_SIZE:blk_cnt * BLK_SIZE + BLK_SIZE], BLK_SIZE) != True:
                                if RE_SEND_TOTAL > re_send:
                                    if not self.close:
                                        re_send = re_send + 1
                                        print('重新发送', re_send)

                            if re_send >= RE_SEND_TOTAL:
                                goto.begin
                            re_send = 0
                            while self.cmdBlkSndEnd(blk_cnt, BLK_SIZE) != True:
                                if RE_SEND_TOTAL > re_send:
                                    if not self.close:
                                        re_send = re_send + 1
                                        print('重新发送', re_send)

                            if re_send >= RE_SEND_TOTAL:
                                goto.begin
                            blk_cnt = blk_cnt + 1

                    if self.fileSize > blk_cnt * BLK_SIZE:
                        re_send = 0
                        while self.cmdBlkSndStart(blk_cnt, self.fileSize - blk_cnt * BLK_SIZE) != True:
                            if RE_SEND_TOTAL > re_send:
                                if not self.close:
                                    re_send = re_send + 1
                                    print('重新发送', re_send)

                        if re_send >= RE_SEND_TOTAL:
                            goto.begin
                        re_send = 0
                        while self.cmdBlkSndData(self.fileHexBuf[blk_cnt * BLK_SIZE:blk_cnt * BLK_SIZE + self.fileSize - blk_cnt * BLK_SIZE], self.fileSize - blk_cnt * BLK_SIZE) != True:
                            if RE_SEND_TOTAL > re_send:
                                if not self.close:
                                    re_send = re_send + 1
                                    print('重新发送', re_send)

                        if re_send >= RE_SEND_TOTAL:
                            goto.begin
                        re_send = 0
                        while self.cmdBlkSndEnd(blk_cnt, self.fileSize - blk_cnt * BLK_SIZE) != True:
                            if RE_SEND_TOTAL > re_send:
                                if not self.close:
                                    re_send = re_send + 1
                                    print('重新发送', re_send)

                        if re_send >= RE_SEND_TOTAL:
                            goto.begin
                    print(u'--------------- 所有数据发送完成 ---------------')
                    self.cmdId = CMD_START_APP
                    print('--------------- start app ---------------')
                    self.updateFinish.emit(1)
                else:
                    self.start_ota = False

    def cmdFileInfo(self):
        if self.hidchooser.usbhidConnected() == CONNECT_STATUS_OTA:
            data = [
             0] + [1]
        else:
            if self.hidchooser.usbhidConnected() == CONNECT_STATUS_RUNNING:
                data = [
                 20] + [49]
            else:
                return self.hidchooser.waitFunTransReady(READ_WAIT_TOUT, self.close)
            data.append(self.fileSize & 255)
            data.append(self.fileSize >> 8 & 255)
            data.append(self.fileSize >> 16 & 255)
            data.append(self.fileSize >> 24 & 255)
            data = data + [0] * (64 - len(data) + 1)
            self.hidchooser.sent_update_handler(data)
            return self.hidchooser.waitFunTransReady(READ_WAIT_TOUT, self.close)

    def cmdFileSndEnd(self):
        if self.hidchooser.usbhidConnected() == CONNECT_STATUS_OTA:
            data = [
             0] + [2]
        else:
            if self.hidchooser.usbhidConnected() == CONNECT_STATUS_RUNNING:
                data = [
                 20] + [50]
            else:
                return self.hidchooser.waitFunTransEnd(READ_WAIT_TOUT, self.close)
            data.append(1)
            data = data + [0] * (64 - len(data) + 1)
            self.hidchooser.sent_update_handler(data)
            return self.hidchooser.waitFunTransEnd(READ_WAIT_TOUT, self.close)

    def cmdBlkSndStart(self, blk_cnt, blk_size):
        if self.hidchooser.usbhidConnected() == CONNECT_STATUS_OTA:
            data = [
             0] + [16]
        else:
            if self.hidchooser.usbhidConnected() == CONNECT_STATUS_RUNNING:
                data = [
                 20] + [64]
            else:
                return self.hidchooser.waitFunBlockStart(2, self.close)
            data.append(blk_cnt & 255)
            data.append(blk_cnt >> 8 & 255)
            data.append(blk_size & 255)
            data.append(blk_size >> 8 & 255)
            data = data + [0] * (64 - len(data) + 1)
            self.hidchooser.sent_update_handler(data)
            return self.hidchooser.waitFunBlockStart(2, self.close)

    def cmdBlkSndEnd(self, blk_cnt, blk_size):
        blk_buf = self.fileHexBuf[blk_cnt * BLK_SIZE:blk_cnt * BLK_SIZE + blk_size]
        crc_val = CRC16(blk_buf, blk_size)
        if self.hidchooser.usbhidConnected() == CONNECT_STATUS_OTA:
            data = [
             0] + [17]
        else:
            if self.hidchooser.usbhidConnected() == CONNECT_STATUS_RUNNING:
                data = [
                 20] + [65]
            else:
                return self.hidchooser.waitFunBlockFinish(2, self.close)
            data.append(crc_val & 255)
            data.append(crc_val >> 8 & 255)
            data = data + [0] * (64 - len(data) + 1)
            self.hidchooser.sent_update_handler(data)
            return self.hidchooser.waitFunBlockFinish(2, self.close)

    def getUploadPercent(self):
        if self.fileSize != 0:
            p = int(self.uploaded_buff_num / self.fileSize * 100)
            self.main.update_progressBar.setValue(p)
            self.main.update_p_Label.setText(str(p) + ' %')
        else:
            self.main.update_progressBar.setValue(0)
            self.main.update_p_Label.setText('0 %')

    def cmdBlkSndData(self, blk_buf, blk_size):
        frame_cnt = 0
        while frame_cnt < blk_size / (self.HID_BUF_SIZE - 2) - 1 and not self.close:
            if self.hidchooser.usbhidConnected() == CONNECT_STATUS_OTA:
                data = [
                 0] + [32]
            else:
                if self.hidchooser.usbhidConnected() == CONNECT_STATUS_RUNNING:
                    data = [
                     20] + [80]
                else:
                    return False
                data.append(self.HID_BUF_SIZE - 2)
                data = data + blk_buf[frame_cnt * (self.HID_BUF_SIZE - 2):frame_cnt * (self.HID_BUF_SIZE - 2) + (self.HID_BUF_SIZE - 2)]
                self.uploaded_buff_num = self.uploaded_buff_num + len(data) - 3
                data = data + [0] * (64 - len(data) + 1)
                self.hidchooser.sent_update_handler(data)
                frame_cnt = frame_cnt + 1
            if self.hidchooser.usbhidConnected() == CONNECT_STATUS_OTA:
                time.sleep(0.001)
            elif self.hidchooser.usbhidConnected() == CONNECT_STATUS_RUNNING:
                time.sleep(0.01)

        if blk_size > frame_cnt * (self.HID_BUF_SIZE - 2):
            if self.hidchooser.usbhidConnected() == CONNECT_STATUS_OTA:
                data = [
                 0] + [32]
            else:
                if self.hidchooser.usbhidConnected() == CONNECT_STATUS_RUNNING:
                    data = [
                     20] + [80]
                else:
                    return False
                data.append(blk_size - frame_cnt * (self.HID_BUF_SIZE - 2))
                data = data + blk_buf[frame_cnt * (self.HID_BUF_SIZE - 2):frame_cnt * (self.HID_BUF_SIZE - 2) + (blk_size - frame_cnt * (self.HID_BUF_SIZE - 2))]
                self.uploaded_buff_num = self.uploaded_buff_num + len(data) - 3
                data = data + [0] * (64 - len(data) + 1)
                self.hidchooser.sent_update_handler(data)
                if self.hidchooser.usbhidConnected() == CONNECT_STATUS_OTA:
                    time.sleep(0.001)
                elif self.hidchooser.usbhidConnected() == CONNECT_STATUS_RUNNING:
                    time.sleep(0.01)
            return True

    def cmdGetIapVer(self):
        if self.hidchooser.usbhidConnected() == CONNECT_STATUS_OTA:
            data = [
             0] + [128] + [1]
        else:
            if self.hidchooser.usbhidConnected() == CONNECT_STATUS_RUNNING:
                data = [
                 20] + [96] + [1]
            else:
                return False
            data = data + [0] * (64 - len(data) + 1)
            self.hidchooser.sent_update_handler(data)
            return True