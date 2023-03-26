from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import QTimer
from PyQt5.QtSerialPort import QSerialPort, QSerialPortInfo
from PyQt5.QtCore import QObject, pyqtSlot, pyqtSignal
import time, main
from base_ui import WidgetUI
from uitl import Refresher
from setting_define import *
from queue import Queue
import threading
hub_q = Queue(maxsize=0)
hub_updata_q = Queue(maxsize=0)
from easyhid import Enumeration

def get_s16(value):
    if value < 32768:
        return value
    else:
        return value - 65536


class HubHidChooser(QObject):
    connectStatusChange = pyqtSignal(int)

    def __init__(self, usb_vid, usb_pid, dash):
        super(HubHidChooser, self).__init__()
        self.type = 'hub'
        self.base_device_type = 'None'
        self.main = main
        self.usb_hid = None
        self.usb_hid_close = False
        self.cmd_sending = False
        self.first_system_status_rec = False
        self.usb_last_connect_status = -1
        self.last_rgb_data = [
         0] * 64
        self.last_game_data = [0] * 64
        self.last_game_data_slow = [0] * 64
        self.rpmRgb = rpmRgb565()
        self.buttonRgb = buttonRgb565()
        self.isWireless = False
        self.dash = dash
        self.usb_status_running = False
        self.usb_status_ota = False
        self.try_connect_success = False
        self.updata_boot_flag = False
        self.usb_vid = usb_vid
        self.usb_pid = usb_pid
        self.FunTransReady_flag = False
        self.FunTransEnd = False
        self.FunBlockStart = False
        self.FunBlockFinish = False
        self.FunFrameData = False
        self.FunControl = False
        self.wireless_data = []
        self.buttons = self.buttons2 = 0
        self.x = self.y = self.z = self.rx = self.ry = self.rz = self.slider = self.slider2 = -32767
        self.x_for_func = self.y_for_func = self.z_for_func = self.rx_for_func = self.ry_for_func = self.rz_for_func = self.slider_for_func = self.slider2_for_func = 0
        self.left_enc = self.right_enc = 0
        self.system_status = self.mode = self.model = self.hub_major_ver = self.hub_minor_ver = 0
        self.left_rot_sw_mode = self.right_rot_sw_mode = self.clutch_mode = self.joy_mode = self.buzzer_enable = self.buzzer_intensity = self.clutch_point = 0
        self.find_devices()
        self.connect_status = False
        self.find_hid_thread = Refresher(0.03333333333333333)
        self.find_hid_thread.sinOut.connect(self.refreshHidAndTryConnect)
        self.find_hid_thread.start()
        t1 = threading.Timer(1, self.receive_handler, None)
        t1.start()
        self.find_device_thread = threading.Timer(1, self.find_device, None)

    def __del__(self):
        if self.usb_hid != None:
            self.usb_hid.close()
        self.usb_hid_close = True

    def find_devices(self):
        self.devlist = Enumeration().find(vid=(self.usb_vid), pid=(self.usb_pid))
        self.devlist_for_update = Enumeration().find(vid=(self.usb_vid), pid=45313)
        if self.devlist != []:
            self.usb_hid = self.devlist[0]
            if not self.usb_hid.is_open():
                self.usb_hid.open()
        elif self.devlist_for_update != []:
            self.usb_hid = self.devlist_for_update[0]
            if not self.usb_hid.is_open():
                self.usb_hid.open()

    def sent_handler(self, cmd=0, value=0):
        if self.usbhidConnected() == CONNECT_STATUS_RUNNING:
            data = [
             20] + [cmd] + [value & 255] + [value >> 8 & 255]
            data = data + [0] * (64 - len(data) + 1)
            hub_q.put(data)

    def sent_RGB_handler(self, cmd, ws2812_rgb, ws2812_button_rgb, force=True):
        if self.usbhidConnected() == CONNECT_STATUS_RUNNING and self.updata_boot_flag == False:
            for i, (field, _type, size) in enumerate(self.rpmRgb._fields_):
                setattr(self.rpmRgb, field, ws2812_rgb[i] >> 3)

            ws2812_rgb_list = string_at(addressof(self.rpmRgb), sizeof(self.rpmRgb))
            for i, (field, _type, size) in enumerate(self.buttonRgb._fields_):
                setattr(self.buttonRgb, field, ws2812_button_rgb[i] >> 3)

            ws2812_button_rgb_list = string_at(addressof(self.buttonRgb), sizeof(self.buttonRgb))
            data = [
             20] + [SETTING_RGB] + list(ws2812_rgb_list) + list(ws2812_button_rgb_list)
            data = data + [0] * (64 - len(data) + 1)
            try:
                if self.last_rgb_data != data or force == True:
                    hub_q.put(data)
                self.last_rgb_data = data
            except Exception as e:
                print('hub sent_RGB_handler ', e)

    def hid_write(self, data):
        try:
            self.usb_hid.write(bytearray(data[1:]), data[0])
        except Exception as e:
            self.usb_hid = None
            self.devlist = []
            self.devlist_for_update = []
            self.find_hid_thread.setTime(1)
            self.usb_status_running = False
            self.usb_status_ota = False
            self.first_system_status_rec = False
            self.model = MODE_UNKNOW
            print(e)

    def sent_update_handler(self, data):
        if self.usbhidConnected() == CONNECT_STATUS_OTA or self.usbhidConnected() == CONNECT_STATUS_RUNNING and self.updata_boot_flag == True:
            hub_updata_q.put(data)

    def set_Wirless_data(self, data):
        if data != []:
            self.isWireless = True
            self.wireless_data = data

    def receive_handler(self):
        last_data = []
        while self.usb_hid_close != True:
            time.sleep(0.001)
            try:
                if self.isWireless:
                    data = self.wireless_data
                else:
                    if self.usb_hid != None:
                        if self.usb_hid.is_open():
                            data = list(self.usb_hid.read())
                        else:
                            data = None
                    elif not data:
                        continue
                    report_id = data[0]
                    cmd = data[1]
                    if self.usbhidConnected() == CONNECT_STATUS_OTA:
                        cmd = data[0]
                        if cmd == 1:
                            self.FunTransReady_flag = True
                        else:
                            if cmd == 2:
                                self.FunTransEnd = True
                            else:
                                if cmd == 16:
                                    self.FunBlockStart = True
                                else:
                                    if cmd == 17:
                                        self.FunBlockFinish = True
                                    else:
                                        if cmd == 32:
                                            self.FunFrameData = True
                                        else:
                                            if cmd == 128:
                                                self.FunControl = True
                                                version = ''
                                                for i in data[2:]:
                                                    if i:
                                                        version = version + str(chr(i))

                                                print(version)
                    elif self.usbhidConnected() == CONNECT_STATUS_RUNNING or self.isWireless == True:
                        if report_id == 22:
                            cmd = data[1]
                            if cmd == 49:
                                if data[2] == 0:
                                    self.FunTransReady_flag = True
                            else:
                                if cmd == 50:
                                    if data[2] == 0:
                                        self.FunTransEnd = True
                                else:
                                    if cmd == 64:
                                        self.FunBlockStart = True
                                    else:
                                        if cmd == 65:
                                            if data[4] == 0:
                                                self.FunBlockFinish = True
                                        else:
                                            if cmd == 80:
                                                self.FunFrameData = True
                                            elif cmd == 96:
                                                self.FunControl = True
                                                version = ''
                                                for i in data[2:]:
                                                    if i:
                                                        version = version + str(chr(i))

                                                print(version)
                        if report_id == 3:
                            self.model = data[1]
                            self.system_status = data[2]
                            self.hub_major_ver = str(data[3])
                            self.hub_minor_ver = str(data[4])
                            self.info_reserved_1 = data[5]
                            self.info_reserved_2 = data[6]
                            self.info_reserved_3 = data[7]
                            self.info_reserved_4 = data[8]
                            self.left_rot_sw_mode = data[9]
                            self.right_rot_sw_mode = data[10]
                            self.clutch_mode = data[11]
                            self.joy_mode = data[12]
                            self.buzzer_enable = data[13]
                            self.buzzer_intensity = data[14]
                            self.clutch_point = data[15] + (data[16] << 8)
                            self.left_enc = data[17]
                            self.right_enc = data[18]
                            self.first_system_status_rec = True
                        if self.usbhidConnected() == CONNECT_STATUS_RUNNING:
                            if report_id == 1:
                                self.buttons = data[1] + (data[2] << 8) + (data[3] << 16) + (data[4] << 24) + (data[5] << 32) + (data[6] << 40) + (data[7] << 48) + (data[8] << 56)
                                self.buttons2 = data[9] + (data[10] << 8) + (data[11] << 16) + (data[12] << 24) + (data[13] << 32) + (data[14] << 40) + (data[15] << 48) + (data[16] << 56)
                                self.x = get_s16(data[17] + (data[18] << 8))
                                self.y = get_s16(data[19] + (data[20] << 8))
                                self.z = get_s16(data[21] + (data[22] << 8))
                                self.rx = get_s16(data[23] + (data[24] << 8))
                                self.ry = get_s16(data[25] + (data[26] << 8))
                                self.rz = get_s16(data[27] + (data[28] << 8))
                                self.slider = get_s16(data[29] + (data[30] << 8))
                                self.slider2 = get_s16(data[31] + (data[32] << 8))
            except Exception as e:
                self.usb_hid = None
                self.devlist = []
                self.devlist_for_update = []
                self.find_hid_thread.setTime(1)
                self.usb_status_running = False
                self.usb_status_ota = False
                self.first_system_status_rec = False
                self.model = MODE_UNKNOW
                print(e)

    def waitFunTransReady(self, timeout, close_flag):
        time_num = int(timeout / 0.1)
        while time_num > 0 and not close_flag:
            if self.FunTransReady_flag == True:
                self.FunTransReady_flag = False
                return True
            time.sleep(0.1)
            time_num = time_num - 1

        return False

    def waitFunTransEnd(self, timeout, close_flag):
        time_num = int(timeout / 0.1)
        while time_num > 0 and not close_flag:
            if self.FunTransEnd == True:
                self.FunTransEnd = False
                return True
            time.sleep(0.1)
            time_num = time_num - 1

        return False

    def waitFunBlockStart(self, timeout, close_flag):
        time_num = int(timeout / 0.1)
        while time_num > 0 and not close_flag:
            if self.FunBlockStart == True:
                self.FunBlockStart = False
                return True
            time.sleep(0.1)
            time_num = time_num - 1

        return False

    def waitFunBlockFinish(self, timeout, close_flag):
        time_num = int(timeout / 0.1)
        while time_num > 0 and not close_flag:
            if self.FunBlockFinish == True:
                self.FunBlockFinish = False
                return True
            time.sleep(0.1)
            time_num = time_num - 1

        return False

    def waitFunFrameData(self, timeout, close_flag):
        time_num = int(timeout / 0.1)
        while time_num > 0 and not close_flag:
            if self.FunFrameData == True:
                self.FunFrameData = False
                return True
            time.sleep(0.1)
            time_num = time_num - 1

        return False

    def waitFunControl(self, timeout, close_flag):
        time_num = int(timeout / 0.1)
        while time_num > 0 and not close_flag:
            if self.FunControl == True:
                self.FunControl = False
                return True
            time.sleep(0.1)
            time_num = time_num - 1

        return False

    def start(self):
        self.find_hid_thread.start()

    def usbhidConnected(self):
        if self.usb_hid != None:
            if self.usb_hid.is_connected():
                if self.usb_status_running:
                    return CONNECT_STATUS_RUNNING
            if self.isWireless == True:
                if self.model != MODE_UNKNOW:
                    return CONNECT_STATUS_WIRELESS_RUNNING
        else:
            if self.usb_hid != None:
                if self.usb_hid.is_connected():
                    if self.usb_status_ota:
                        return CONNECT_STATUS_OTA
        self.usb_status_running = False
        self.usb_status_ota = False
        return CONNECT_STATUS_FAULT

    def usbhidDataReady(self):
        if self.usbhidConnected() == CONNECT_STATUS_RUNNING or self.usbhidConnected() == CONNECT_STATUS_WIRELESS_RUNNING:
            if self.first_system_status_rec:
                return True
        return False

    def find_device(self):
        self.devlist = Enumeration().find(vid=(self.usb_vid), pid=(self.usb_pid))
        self.devlist_for_update = Enumeration().find(vid=(self.usb_vid), pid=45313)

    def refreshHidAndTryConnect(self):
        current_connect_status = self.usbhidConnected()
        if current_connect_status != self.usb_last_connect_status:
            self.connectStatusChange.emit(current_connect_status)
        if current_connect_status == CONNECT_STATUS_RUNNING and self.try_connect_success:
            if self.updata_boot_flag == False:
                self.find_hid_thread.setTime(0.02)
                if not hub_q.empty():
                    data = hub_q.get()
                    self.hid_write(data)
                    self.cmd_sending = True
                    if data[1] == SETTING_BOOT_UPDATA_MODE:
                        self.updata_boot_flag = True
                else:
                    self.cmd_sending = False
        if (current_connect_status == CONNECT_STATUS_OTA or self.usbhidConnected() == CONNECT_STATUS_RUNNING and self.updata_boot_flag == True) and self.try_connect_success:
            self.find_hid_thread.setTime(0.001)
            if not hub_updata_q.empty():
                data = hub_updata_q.get()
                if len(data) == 65:
                    self.hid_write(data)
        else:
            self.try_connect_success = False
            self.find_hid_thread.setTime(1)
            if not self.find_device_thread.is_alive():
                self.find_device_thread = threading.Timer(1, self.find_device, None)
                self.find_device_thread.start()
            try:
                if self.devlist != []:
                    self.usb_hid = self.devlist[0]
                    print(self.usb_hid)
                    if not self.usb_hid.is_open():
                        self.usb_hid.open()
                    self.try_connect_success = True
                    self.usb_status_running = True
                else:
                    if self.devlist_for_update != []:
                        self.usb_hid = self.devlist_for_update[0]
                        print(self.usb_hid)
                        if not self.usb_hid.is_open():
                            self.usb_hid.open()
                        self.try_connect_success = True
                        self.usb_status_ota = True
                    else:
                        self.usb_hid = None
                        self.devlist = []
                        self.devlist_for_update = []
                        self.usb_status_running = False
                        self.usb_status_ota = False
                        self.first_system_status_rec = False
                        self.model = MODE_UNKNOW
            except Exception as e:
                self.usb_hid = None
                self.devlist = []
                self.devlist_for_update = []
                self.find_hid_thread.setTime(1)
                self.usb_status_running = False
                self.usb_status_ota = False
                self.first_system_status_rec = False
                self.model = MODE_UNKNOW
                print('hub hid refreshHidAndTryConnect', e)

        hub_model = self.getHIDProductName()
        if hub_model != None:
            if 'FD1' in hub_model:
                if 'FD1S' not in hub_model:
                    self.hub_device_type = 'FD1'
            if 'FD1S' in hub_model:
                self.hub_device_type = 'FD1S'
        self.usb_last_connect_status = current_connect_status

    def getHIDProductName(self):
        if self.usbhidConnected() != CONNECT_STATUS_FAULT:
            try:
                return self.usb_hid.product_string
            except:
                return 'None'

        else:
            return 'None'

    def getModel(self):
        if self.model == 0:
            return 'Unknow'
        else:
            if self.model == WHEEL_HUB_FD1:
                return 'FD1'
            if self.model == WHEEL_HUB_FD1S:
                return 'FD1S'

    def getWireUSBModel(self):
        if self.usbhidConnected() == CONNECT_STATUS_OTA or self.usbhidConnected() == CONNECT_STATUS_RUNNING:
            product_name = self.usb_hid.get_product_string()
            if product_name == '':
                return 'Unknow'
            if product_name == 'IMMSOURCE DYAGONFLY' or product_name == 'IMMBASE DYAGONFLY UPDATE MODE':
                return 'Dyagonfly'

    def getSystemStatus(self):
        if self.system_status == 0:
            return 'Unknow'
        else:
            if self.system_status == 1:
                return 'Uninit'
            if self.system_status == 2:
                return 'Initing'
            if self.system_status == 3:
                return 'Running'

    def getBuzzerEnable(self):
        if self.buzzer_enable == 1:
            return True
        else:
            return False
