from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import QTimer
from PyQt5.QtSerialPort import QSerialPort, QSerialPortInfo
from PyQt5.QtCore import QIODevice, pyqtSignal
from PyQt5.QtCore import QObject, pyqtSlot, pyqtSignal
import time
from base_ui import WidgetUI
from uitl import Refresher
from pywinusb import hid
from setting_define import *
import threading
from queue import Queue
from easyhid import Enumeration
import usb.core
from crc import *
q = Queue(maxsize=0)
updata_q = Queue(maxsize=0)
from ctypes import c_uint16, string_at, addressof, sizeof, Structure, memmove
import ctypes

def get_s16(value):
    if value < 32768:
        return value
    else:
        return value - 65536


class HidChooser(QObject):
    connectStatusChange = pyqtSignal(int)
    usbHubStatusChange = pyqtSignal(str, int)

    def __init__(self, dash, usb_vid, usb_pid, hub_hidchooser):
        super(HidChooser, self).__init__()
        self.usb_hid = None
        self.usb_hid_close = False
        self.dash = dash
        self.hub_hidchooser = hub_hidchooser
        self.en = Enumeration()
        self.type = 'base'
        self.base_device_type = 'None'
        self.last_time = 0
        self.usb_last_connect_status = -1
        self.usb_status_running = False
        self.usb_status_ota = False
        self.usb_mode = 0
        self.last_rgb_data = [
         0] * 64
        self.last_game_data = [0] * 64
        self.last_game_data_slow = [0] * 64
        self.usb_vid = usb_vid
        self.usb_pid = usb_pid
        self.FunTransReady_flag = False
        self.FunTransEnd = False
        self.FunBlockStart = False
        self.FunBlockFinish = False
        self.FunFrameData = False
        self.FunControl = False
        self.try_connect_success = False
        self.first_system_status_rec = False
        self.first_ffb_setting_rec = False
        self.init_base = False
        self.rgb_send_stop = False
        self.cmd_sending = False
        self.rgb_sending = False
        self.hub_wireless_connect_time = 0
        self.rpmRgb = rpmRgb565()
        self.buttonRgb = buttonRgb565()
        self.buttons = self.buttons2 = 0
        self.x = self.y = self.z = self.rx = self.ry = self.rz = self.slider = self.slider2 = -32767
        self.mode = self.system_status = self.model = self.system_voltage = self.torque = self.motor_temp = self.drive_temp = self.base_ver = 0
        self.angle_range = self.angle_range_auto = self.dead_band = 0
        self.gear = 0
        self.front_led_enable = self.back_led_enable = self.front_led_brightness = self.back_led_brightness = 0
        self.buzzer_enable = self.buzzer_intensity = 0
        self.updata_boot_flag = False
        self.ffb_global_strength = 0
        self.ffb_response = 0
        self.speed_limit = 0
        self.ffb_detail_enhancer = 0
        self.ffb_filter = 0
        self.ffb_maxtorque = 0
        self.affect_deadband = 0
        self.mech_spring_strength = 0
        self.mech_friction_strength = 0
        self.mech_damping_strength = 0
        self.mech_inertia_strength = 0
        self.mech_endstop_strength = 0
        self.dyna_damping_strength = 0
        self.dyna_threshold = 0
        self.dyna_range = 0
        self.wireless_ch = 0
        self.ffb_constant_strength = 0
        self.ffb_friction_strength = 0
        self.ffb_damping_strength = 0
        self.ffb_inertia_strength = 0
        self.ffb_sine_strength = 0
        self.ffb_spring_strength = 0
        self.ffb_ramp_strength = 0
        self.ffb_square_strength = 0
        self.ffb_sawtooth_strength = 0
        self.ffb_triangle_strength = 0
        self.ffb_friction_filter_strength = 0
        self.ffb_damping_filter_strength = 0
        self.ffb_inertia_filter_strength = 0
        self.ffb_sync_steering_lock = 0
        self.device_type = 0
        self.device_status = 0
        self.led_last_time = 0
        self.devlist = []
        self.devlist_for_update = []
        self.find_devices()
        self.find_hid_thread = Refresher(0.03333333333333333)
        self.find_hid_thread.sinOut.connect(self.refreshHidAndTryConnect)
        self.find_hid_thread.start()
        t1 = threading.Timer(0.033, self.receive_handler, None)
        t1.start()
        t2 = threading.Timer(1, self.sendsharememory, None)
        t2.start()
        self.find_device_thread = threading.Timer(1, self.find_device, None)

    def find_devices(self):
        self.devlist = Enumeration().find(vid=IMMS_BASE_VID, pid=IMMS_BASE_PID)
        if self.devlist == []:
            self.devlist = Enumeration().find(vid=IMMS_BASE_ET3_VID, pid=IMMS_BASE_ET3_PID)
        elif self.devlist == []:
            self.devlist = Enumeration().find(vid=IMMS_BASE_X_VID, pid=IMMS_BASE_X_PID)
        else:
            if self.devlist == []:
                self.devlist = Enumeration().find(vid=IMMS_BASE_F_VID, pid=IMMS_BASE_F_PID)
                if self.devlist != []:
                    self.devlist_copy = self.devlist
                    self.devlist = []
                    for dev in self.devlist_copy:
                        if 'IMMS' in dev.product_string:
                            self.devlist = [
                             dev]

            self.devlist_for_update = Enumeration().find(vid=IMMS_BASE_UPDATA_VID, pid=IMMS_BASE_UPDATA_PID)
            if self.devlist_for_update == []:
                self.devlist_for_update = Enumeration().find(vid=IMMS_BASE_ET3_UPDATA_VID, pid=IMMS_BASE_ET3_UPDATA_PID)
            if self.devlist != []:
                self.usb_hid = self.devlist[0]
                if not self.usb_hid.is_open():
                    self.usb_hid.open()
                self.mode = MODE_PC
            else:
                if self.devlist_for_update != []:
                    self.usb_hid = self.devlist_for_update[0]
                    if not self.usb_hid.is_open():
                        self.usb_hid.open()
                    self.mode = MODE_PC_OTA
                else:
                    self.mode = 0

    def __del__(self):
        if self.usb_hid != None:
            self.usb_hid.close()
        self.usb_hid_close = True

    def sent_list_handler(self, cmd=0, value=[]):
        if self.usbhidConnected() == CONNECT_STATUS_RUNNING:
            data = [
             20] + [cmd] + value
            data = data + [0] * (64 - len(data) + 1)
            crc_val = CRC16(data, 30)
            data[30] = crc_val & 255
            data[31] = crc_val >> 8 & 255
            q.put(data)

    def sent_handler(self, cmd=0, value=0, for_wireless=False):
        if self.usbhidConnected() == CONNECT_STATUS_RUNNING:
            data = [
             20] + [cmd] + [value & 255] + [value >> 8 & 255]
            data = data + [0] * (64 - len(data) + 1)
            crc_val = CRC16(data, 30)
            data[30] = crc_val & 255
            data[31] = crc_val >> 8 & 255
            if cmd == SETTING_Encrypted:
                data[2] = 12
                data[3] = 23
                data[4] = 34
                data[5] = 45
                data[6] = 56
            q.put(data)
            if for_wireless == True:
                q.put(data)
                q.put(data)
                q.put(data)
        elif self.usbhidConnected() == CONNECT_STATUS_PS4:
            data = [
             5] + [2, 3, 5, 7, 11] + [cmd] + [value & 255] + [value >> 8 & 255]
            data = data + [0] * (32 - len(data) + 1)
            q.put(data)

    def hid_write(self, data):
        try:
            self.usb_hid.write(bytearray(data[1:]), data[0])
        except Exception as e:
            self.usb_hid = None
            self.find_hid_thread.setTime(1)
            self.usb_status_running = False
            self.usb_status_ota = False
            self.first_ffb_setting_rec = False
            self.first_system_status_rec = False
            self.init_base = False
            self.mode = 0
            print(e)

    def sent_update_handler(self, data):
        if self.usbhidConnected() == CONNECT_STATUS_OTA or self.usbhidConnected() == CONNECT_STATUS_RUNNING and self.updata_boot_flag == True:
            updata_q.put(data)

    def sent_RGB_handler(self, cmd, ws2812_rgb, ws2812_button_rgb, force=False):
        t_gas = time.time() - self.led_last_time
        if t_gas >= 2:
            force = True
            self.led_last_time = time.time()
        if self.usbhidConnected() == CONNECT_STATUS_RUNNING and self.cmd_sending == False:
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
                    self.usb_hid.write(data[1:], data[0])
                self.last_rgb_data = data
            except:
                pass

    def sent_Speed_handler(self, cmd, speed):
        if self.usbhidConnected() == CONNECT_STATUS_RUNNING:
            if self.cmd_sending == False:
                data = [
                 20] + [cmd] + [speed & 255] + [speed >> 8 & 255]
                data = data + [0] * (64 - len(data) + 1)
                crc_val = CRC16(data, 30)
                data[30] = crc_val & 255
                data[31] = crc_val >> 8 & 255
                self.hid_write(data)

    def sent_game_info_handler(self, cmd, data):
        if self.usbhidConnected() == CONNECT_STATUS_RUNNING:
            if self.cmd_sending == False:
                data = [
                 20] + [cmd] + data
                data = data + [0] * (64 - len(data) + 1)
                try:
                    if cmd == SETTING_GAME_INFO_FAST:
                        if self.last_game_data != data:
                            self.hid_write(data)
                        self.last_game_data = data
                    else:
                        if cmd == SETTING_GAME_INFO_SLOW:
                            if self.last_game_data_slow != data:
                                self.hid_write(data)
                            self.last_game_data_slow = data
                except:
                    pass

    def receive_handler_test(self, data):
        print('rec2', data, len(data))

    def receive_handler(self):
        while self.usb_hid_close != True:
            time.sleep(0.001)
            try:
                if self.usb_hid != None and self.usb_hid.is_open():
                    data = list(self.usb_hid.read())
                    if not data:
                        continue
                    report_id = data[0]
                    if self.usbhidConnected() == CONNECT_STATUS_OTA:
                        cmd = data[0]
                        if cmd == 1:
                            if data[1] == 0:
                                self.FunTransReady_flag = True
                        else:
                            if cmd == 2:
                                if data[1] == 0:
                                    self.FunTransEnd = True
                            else:
                                if cmd == 16:
                                    self.FunBlockStart = True
                                else:
                                    if cmd == 17:
                                        if data[3] == 0:
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
                    elif self.usbhidConnected() == CONNECT_STATUS_RUNNING:
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
                            if self.hub_hidchooser.isWireless:
                                self.hub_hidchooser.buttons = self.buttons
                                self.hub_hidchooser.x = self.y
                                self.hub_hidchooser.y = self.z
                                self.hub_hidchooser.z = self.rx
                                self.hub_hidchooser.rx = self.ry
                                self.hub_hidchooser.ry = self.rz
                                self.hub_hidchooser.rz = self.slider
                                self.hub_hidchooser.slider = self.slider2
                        else:
                            if report_id == 16:
                                self.model = data[1]
                                self.system_status = data[2]
                                self.base_ver = str(data[3]) + '.' + str(data[4])
                                self.base_mode = data[5]
                                self.system_voltage = data[6] + (data[7] << 8)
                                self.torque = get_s16(data[8] + (data[9] << 8))
                                self.hub1 = data[10]
                                self.hub2 = data[11]
                                self.hub3 = data[12]
                                self.hub4 = data[13]
                                self.hub5 = data[14]
                                self.hub6 = data[15]
                                self.angle_range = data[16] + (data[17] << 8)
                                self.angle_range_auto = data[18]
                                self.gear = data[19]
                                self.front_led_enable = data[20]
                                self.back_led_enable = data[21]
                                self.front_led_brightness = data[22]
                                self.back_led_brightness = data[23]
                                self.buzzer_enable = data[24]
                                self.buzzer_intensity = data[25]
                                self.wireless_ch = data[26]
                                self.buzzer_over_rotation_enable = data[27] >> 0 & 1
                                self.buzzer_ffb_clip_enable = data[27] >> 1 & 1
                                self.first_system_status_rec = True
                            else:
                                if report_id == 17:
                                    self.ffb_global_strength = data[1]
                                    self.ffb_response = data[2]
                                    self.ffb_detail_enhancer = data[3]
                                    self.ffb_filter = data[4]
                                    self.ffb_maxtorque = data[5]
                                    self.speed_limit = data[6]
                                    self.mech_spring_strength = data[7]
                                    self.mech_friction_strength = data[8]
                                    self.mech_damping_strength = data[9]
                                    self.mech_inertia_strength = data[10]
                                    self.ffb_constant_strength = data[11]
                                    self.ffb_friction_strength = data[12]
                                    self.ffb_damping_strength = data[13]
                                    self.ffb_inertia_strength = data[14]
                                    self.ffb_sine_strength = data[15]
                                    self.ffb_spring_strength = data[16]
                                    self.ffb_ramp_strength = data[17]
                                    self.ffb_square_strength = data[18]
                                    self.ffb_sawtooth_strength = data[19]
                                    self.ffb_triangle_strength = data[20]
                                    self.dyna_damping_strength = data[21]
                                    self.dyna_threshold = data[22]
                                    self.dyna_range = data[23]
                                    self.ffb_sync_steering_lock = data[24] + (data[25] << 8)
                                    self.ffb_constant_active = data[26] >> 0 & 1
                                    self.ffb_friction_active = data[26] >> 1 & 1
                                    self.ffb_damping_active = data[26] >> 2 & 1
                                    self.ffb_inertia_active = data[26] >> 3 & 1
                                    self.ffb_sine_active = data[26] >> 4 & 1
                                    self.ffb_spring_active = data[26] >> 5 & 1
                                    self.ffb_ramp_active = data[26] >> 6 & 1
                                    self.ffb_square_active = data[26] >> 7 & 1
                                    self.ffb_sawtooth_active = data[27] >> 0 & 1
                                    self.ffb_triangle_active = data[27] >> 1 & 1
                                    self.mech_endstop_strength = data[27] >> 2 & 63
                                    self.first_ffb_setting_rec = True
                                elif report_id == 18:
                                    data = data[1:]
                                    self.hub_wireless_connect_time = 0
                                    self.hub_hidchooser.isWireless = True
                                    self.hub_hidchooser.set_Wirless_data(data)
            except Exception as e:
                self.usb_hid = None
                self.find_hid_thread.setTime(1)
                self.usb_status_running = False
                self.usb_status_ota = False
                self.first_ffb_setting_rec = False
                self.first_system_status_rec = False
                self.init_base = False
                self.mode = 0
                print('receive_handler', e)

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
            if self.usb_hid != None:
                if self.usb_hid.is_connected():
                    if self.usb_status_ota:
                        return CONNECT_STATUS_OTA
        else:
            if self.usb_hid != None:
                if self.usb_hid.is_connected():
                    if self.mode == MODE_PS4:
                        return CONNECT_STATUS_PS4
        self.usb_status_running = False
        self.usb_status_ota = False
        return CONNECT_STATUS_FAULT

    def usbhidDataReady(self):
        if self.usbhidConnected() == CONNECT_STATUS_RUNNING:
            if self.first_system_status_rec:
                if self.first_ffb_setting_rec:
                    return True
        return False

    def getHIDProductName(self):
        if self.usbhidConnected() != CONNECT_STATUS_FAULT:
            try:
                return self.usb_hid.product_string
            except:
                return 'None'

        else:
            return 'None'

    def getHIDReleaseNumber(self):
        if self.usbhidConnected() != CONNECT_STATUS_FAULT:
            try:
                return self.usb_hid.release_number
            except:
                return 'None'

        else:
            return 'None'

    def find_device(self):
        self.devlist = Enumeration().find(vid=IMMS_BASE_VID, pid=IMMS_BASE_PID)
        if self.devlist == []:
            self.devlist = Enumeration().find(vid=IMMS_BASE_ET3_VID, pid=IMMS_BASE_ET3_PID)
        if self.devlist == []:
            self.devlist = Enumeration().find(vid=IMMS_BASE_X_VID, pid=IMMS_BASE_X_PID)
        if self.devlist == []:
            self.devlist = Enumeration().find(vid=IMMS_BASE_F_VID, pid=IMMS_BASE_F_PID)
            if self.devlist != []:
                self.devlist_copy = self.devlist
                self.devlist = []
                for dev in self.devlist_copy:
                    if 'IMMS' in dev.product_string:
                        self.devlist = [
                         dev]

        self.devlist_for_update = Enumeration().find(vid=IMMS_BASE_UPDATA_VID, pid=IMMS_BASE_UPDATA_PID)
        if self.devlist_for_update == []:
            self.devlist_for_update = Enumeration().find(vid=IMMS_BASE_ET3_UPDATA_VID, pid=IMMS_BASE_ET3_UPDATA_PID)

    def refreshHidAndTryConnect(self):
        status = self.usbhidConnected()
        if status != self.usb_last_connect_status:
            self.connectStatusChange.emit(status)
        if self.hub_wireless_connect_time >= 200:
            self.hub_hidchooser.isWireless = False
        current_connect_status = self.usbhidConnected()
        if current_connect_status == CONNECT_STATUS_RUNNING:
            if self.try_connect_success and self.updata_boot_flag == False:
                self.find_hid_thread.setTime(0.01)
                data = q.empty() or q.get()
                self.hid_write(data)
                self.cmd_sending = True
                if data[1] == SETTING_BOOT_UPDATA_MODE:
                    self.updata_boot_flag = True
            else:
                self.cmd_sending = False
            self.hub_wireless_connect_time = self.hub_wireless_connect_time + 1
        else:
            if (self.usbhidConnected() == CONNECT_STATUS_OTA or self.usbhidConnected() == CONNECT_STATUS_RUNNING and self.updata_boot_flag == True) and self.try_connect_success:
                self.find_hid_thread.setTime(0.001)
                if not updata_q.empty():
                    data = updata_q.get()
                    self.hid_write(data)
            else:
                if self.usbhidConnected() == CONNECT_STATUS_PS4:
                    self.find_hid_thread.setTime(0.03333333333333333)
                    if not q.empty():
                        data = q.get()
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
                if not self.usb_hid.is_open():
                    self.usb_hid.open()
                self.try_connect_success = True
                self.usb_status_running = True
                self.mode = MODE_PC
            else:
                if self.devlist_for_update != []:
                    self.usb_hid = self.devlist_for_update[0]
                    if not self.usb_hid.is_open():
                        self.usb_hid.open()
                    self.try_connect_success = True
                    self.usb_status_ota = True
                    self.mode = MODE_PC_OTA
                else:
                    self.usb_hid = None
                    self.usb_status_running = False
                    self.usb_status_ota = False
                    self.first_ffb_setting_rec = False
                    self.first_system_status_rec = False
                    self.init_base = False
                    self.mode = 0
        except Exception as e:
            self.usb_hid = None
            self.find_hid_thread.setTime(1)
            self.usb_status_running = False
            self.usb_status_ota = False
            self.first_ffb_setting_rec = False
            self.first_system_status_rec = False
            self.init_base = False
            self.mode = 0

        base_model = self.getHIDProductName()
        if base_model != None:
            if 'ET5' in base_model:
                self.base_device_type = 'ET5'
            elif 'ET3' in base_model:
                self.base_device_type = 'ET3'
        self.usb_last_connect_status = current_connect_status

    def getSystemVoltage(self):
        system_voltage = round(self.system_voltage / 10, 1)
        return system_voltage

    def getTorque(self):
        torque = round(float(self.torque) / 100, 2)
        return torque

    def getSystemStatus(self):
        if self.system_status == 0:
            return 'Unknow'
        else:
            if self.system_status == 1:
                return 'Uninit'
            else:
                if self.system_status == 2:
                    return 'Initing'
                else:
                    if self.system_status == 3:
                        return 'Normal idle'
                    if self.system_status == 4:
                        return 'Ffb running'
                    if self.system_status == 5:
                        return 'Low voltage'
                if self.system_status == 6:
                    return 'Over voltage'
            if self.system_status == 7:
                return 'Over temp'

    def getMotorTemp(self):
        return self.motor_temp / 10

    def getDriverTemp(self):
        return self.drive_temp / 10

    def getBaseVersion(self):
        return self.base_ver

    def getHubVersion(self):
        return 0

    def getPedalVersion(self):
        return 0

    def getGearVersion(self):
        return 0

    def getHandbrakeVersion(self):
        return 0

    def getDashboardVersion(self):
        return 0

    def getGear(self):
        return 0

    def getButton(self):
        return self.buttons

    def getX(self):
        return self.x

    def getY(self):
        return self.y

    def getZ(self):
        return self.z

    def getRx(self):
        return self.rx

    def getRy(self):
        return self.ry

    def getRz(self):
        return self.rz

    def getSlider(self):
        return self.slider

    def getCurrentAngle(self):
        angle_range = self.angle_range
        per = angle_range / 65536
        new_angle = per * self.getX()
        new_angle = round(new_angle, 1)
        if new_angle == -0.0:
            new_angle = 0.0
        return new_angle

    def getFrontLedEnable(self):
        if self.front_led_enable == 1:
            return True
        else:
            return False

    def getBackLedEnable(self):
        if self.back_led_enable == 1:
            return True
        else:
            return False

    def getBuzzerEnable(self):
        if self.buzzer_enable == 1:
            return True
        else:
            return False

    def sendsharememory(self):
        while not self.usb_hid_close:
            if not self.usbhidConnected():
                time.sleep(1)
            if self.usbhidConnected():
                pass
            time.sleep(0.033)
