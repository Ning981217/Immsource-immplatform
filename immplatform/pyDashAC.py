from traceback import format_exc
from time import sleep, time
from mmap import mmap
from os.path import getmtime
from pyAC import *
from psutil import pid_exists
import ctypes, sys, os, time, subprocess, io, re, configparser
from setting_define import *
import numpy as np

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


def get_steering_lock(path, car_id):
    FILE = path + car_id + '\\data.acd'
    NAME = car_id
    NAMESZ = len(NAME)
    if os.path.exists(FILE):
        NAMESZ = len(NAME)
        KEY1 = 0
        for i in range(NAMESZ):
            TMP = ord(NAME[i])
            KEY1 = KEY1 + TMP

        TMPSZ = NAMESZ - 1
        KEY2 = 0
        i = 0
        while i < TMPSZ:
            TMP = ord(NAME[i])
            KEY2 = KEY2 * TMP
            i = i + 1
            TMP2 = ord(NAME[i])
            KEY2 = KEY2 - TMP2
            i = i + 1

        TMPSZ = NAMESZ - 3
        KEY3 = 0
        i = 1
        while i < TMPSZ:
            TMP = ord(NAME[i])
            KEY3 = KEY3 * TMP
            i = i + 1
            TMP2 = ord(NAME[i])
            TMP2 = TMP2 + 27
            KEY3 = int(KEY3 / TMP2)
            i = i - 2
            TMP3 = ord(NAME[i])
            TMP = -27
            TMP = TMP - TMP3
            KEY3 = KEY3 + TMP
            i = i + 4

        KEY4 = 5763
        i = 1
        while i < NAMESZ:
            TMP = ord(NAME[i])
            KEY4 = KEY4 - TMP
            i = i + 1

        TMPSZ = NAMESZ - 4
        KEY5 = 66
        i = 1
        while i < TMPSZ:
            TMP = ord(NAME[i])
            TMP = TMP + 15
            TMP = TMP * KEY5
            i = i - 1
            TMP2 = ord(NAME[i])
            i = i + 1
            TMP2 = TMP2 + 15
            TMP2 = TMP2 * TMP
            TMP2 = TMP2 + 22
            KEY5 = TMP2
            i = i + 4

        TMPSZ = NAMESZ - 2
        KEY6 = 101
        i = 0
        while i < TMPSZ:
            TMP = ord(NAME[i])
            KEY6 = KEY6 - TMP
            i = i + 2

        TMPSZ = NAMESZ - 2
        KEY7 = 171
        i = 0
        while i < TMPSZ:
            TMP = ord(NAME[i])
            KEY7 = KEY7 % TMP
            i = i + 2

        TMPSZ = NAMESZ - 1
        KEY8 = 171
        i = 0
        while i < TMPSZ:
            TMP = ord(NAME[i])
            KEY8 = int(KEY8 / TMP)
            i = i + 1
            TMP2 = ord(NAME[i])
            KEY8 = KEY8 + TMP2
            i = i - 1
            i = i + 1

        KEY1 = KEY1 & 255
        KEY2 = KEY2 & 255
        KEY3 = KEY3 & 255
        KEY4 = KEY4 & 255
        KEY5 = KEY5 & 255
        KEY6 = KEY6 & 255
        KEY7 = KEY7 & 255
        KEY8 = KEY8 & 255
        TMP = str(KEY1) + '-' + str(KEY2) + '-' + str(KEY3) + '-' + str(KEY4) + '-'
        TMP2 = str(KEY5) + '-' + str(KEY6) + '-' + str(KEY7) + '-' + str(KEY8)
        KEY = TMP + TMP2
        ADC_SIZE = os.path.getsize(FILE)
        import struct
        ii = 0
        f = open(FILE, 'rb')
        while ii < ADC_SIZE:
            for i in range(10):
                NAMESZ = struct.unpack('i', f.read(4))[0]
                if NAMESZ >= 0:
                    if NAMESZ <= 100:
                        break
                else:
                    ADC_SIZE = ADC_SIZE - 4

            struct_fmt = '{}s'.format(NAMESZ)
            NAME = struct.unpack(struct_fmt, f.read(NAMESZ))[0].decode('utf-8')
            SIZE = struct.unpack('i', f.read(4))[0]
            MEMORY_FILE = struct.unpack('cccc' * SIZE, f.read(4 * SIZE))
            packed_content = MEMORY_FILE[::4]
            new_content = ''
            for i in range(SIZE):
                try:
                    new_content += chr(ord(packed_content[i]) - ord(KEY[(i % len(KEY))]))
                except:
                    pass

            if NAME == 'car.ini':
                s = io.StringIO(new_content)
                for line in s.readlines():
                    if 'STEER_LOCK' in line:
                        steering_lock = int(re.findall('\\d+', line)[0])
                        return steering_lock

            ii = ii + 4 * SIZE + 4 + NAMESZ + 4

    elif os.path.exists(path + car_id + '\\data\\car.ini'):
        with open((path + car_id + '\\data\\car.ini'), 'r', encoding='UTF-8') as (f):
            for line in f.readlines():
                if 'STEER_LOCK' in line:
                    steering_lock = int(re.findall('\\d+', line)[0])
                    return steering_lock

    else:
        return 900


def sign(val):
    return (0 < val) - (val < 0)


class highV1:

    def __init__(self, dPower=0.015):
        self.dPower = dPower
        self.hiLastData = 0
        self.HiLastVal = 0

    def run(self, val):
        iData = self.hiLastData * self.dPower + self.dPower * (val - self.HiLastVal)
        self.hiLastData = iData
        self.HiLastVal = val
        return iData


class lowV1:

    def __init__(self, dPower=0.15):
        self.dPower = dPower
        self.iLastData = 0

    def run(self, val):
        iData = val * self.dPower + (1.0 - self.dPower) * self.iLastData
        self.iLastData = iData
        return iData


def clamp(value, minvalue, maxvalue):
    return max(minvalue, min(value, maxvalue))


class pyDashAC:

    def __init__(self, ac_pid, dash, game_data, enable):
        self.ac_pid = ac_pid
        self.game_data = game_data[0]
        self.game_data_slow = game_data[1]
        self.enable = enable
        self.dash = dash
        self.last_steering_angle = 0
        self.iLastData = 0
        self.hiLastData = 0
        self.HiLastVal = 0
        self.low1 = lowV1(0.2)
        self.game_path = execute_cmd('wmic process where handle=' + str(ac_pid) + ' get ExecutablePath')
        self.game_path = self.game_path.replace('\r', '').replace('\n', '')
        self.game_path = ' '.join(self.game_path.split())
        self.game_path = self.game_path.split(' ')[1]
        if self.game_path:
            self.game_path, tempfilename = os.path.split(self.game_path)
            self.game_path = self.game_path + '\\content\\cars\\'
        self.status = False
        try:
            acMapHandle['physics'] = mmap(fileno=0, length=(sizeof(acPhysics)), tagname=(acMapTag['physics']))
            acMapHandle['graphics'] = mmap(fileno=0, length=(sizeof(acGraphics)), tagname=(acMapTag['graphics']))
            acMapHandle['static'] = mmap(fileno=0, length=(sizeof(acStatic)), tagname=(acMapTag['static']))
            if pid_exists(self.ac_pid):
                self.status = True
                self.game_data.t_game_id = game_id['ac']
        except:
            print('Unable to open shared memory map')

    def isRun(self):
        return self.status

    def __del__(self):
        pass

    def cosVector(self, x, y):
        if len(x) != len(y):
            print('error input,x and y is not in the same space')
            return
        result1 = 0.0
        result2 = 0.0
        result3 = 0.0
        for i in range(len(x)):
            result1 += x[i] * y[i]
            result2 += x[i] ** 2
            result3 += y[i] ** 2

        print('result is ' + str(result1 / (result2 * result3) ** 0.5))

    def lowV1(self, val):
        dPower = 0.15
        iData = val * dPower + (1.0 - dPower) * self.iLastData
        self.iLastData = iData
        return iData

    def highV1(self, val):
        dPower = 0.02
        iData = self.hiLastData * dPower + dPower * (val - self.HiLastVal)
        self.hiLastData = iData
        self.HiLastVal = val
        return iData

    def update(self):
        if pid_exists(self.ac_pid) and self.enable:
            try:
                acMapHandle['physics'].seek(0)
                acMapHandle['graphics'].seek(0)
                acMapHandle['static'].seek(0)
                physics_smm = acPhysics.from_buffer_copy(acMapHandle['physics'])
                graphics_smm = acGraphics.from_buffer_copy(acMapHandle['graphics'])
                static_smm = acStatic.from_buffer_copy(acMapHandle['static'])
                if graphics_smm.status == 2:
                    self.game_data.t_rpm = int(physics_smm.rpm)
                    self.game_data.t_ffb = int(-physics_smm.finalFF * 1000)
                    x1 = [
                     physics_smm.localVelocity[0], physics_smm.localVelocity[1]]
                    x2 = [physics_smm.tyreContactHeading[1][0], physics_smm.tyreContactHeading[1][1]]
                    x2 = [
                     1, 0]
                    x = np.array(x1)
                    y = np.array(x2)
                    Lx = np.sqrt(x.dot(x))
                    Ly = np.sqrt(y.dot(y))
                    if Lx * Ly != 0:
                        cos_angle = x.dot(y) / (Lx * Ly)
                        angle = np.arccos(cos_angle)
                        angle2 = angle * 360 / 2 / np.pi
                        slip_dir = angle2 - 90
                    else:
                        slip_dir = 0
                    self.dash.slip = (physics_smm.wheelSlip[0] + physics_smm.wheelSlip[1]) / 2
                    self.dash.rear_slip = (physics_smm.wheelSlip[2] + physics_smm.wheelSlip[3]) / 2
                    steering_angle = physics_smm.steerAngle
                    to_center = sign(steering_angle) * sign(self.last_steering_angle - steering_angle)
                    if self.dash.rear_slip >= 3.0:
                        if slip_dir > 0:
                            if to_center == 1:
                                if steering_angle > 0:
                                    self.dash.center_damper = abs(steering_angle) * physics_smm.speed / 1.5
                        elif slip_dir < 0:
                            if to_center == 1:
                                if steering_angle < 0:
                                    self.dash.center_damper = abs(steering_angle) * physics_smm.speed / 1.5
                        else:
                            self.dash.center_damper = 0
                    else:
                        self.dash.center_damper = 0
                        self.dash.load_diff = 0
                    if self.dash.rear_slip >= 0.7:
                        if physics_smm.localAngularVelocity[1] > 0 and steering_angle > 0 or physics_smm.localAngularVelocity[1] < 0 and steering_angle < 0:
                            steering_gain = 1 - abs(steering_angle)
                        else:
                            steering_gain = 1
                        rear_s = self.dash.rear_slip
                        if rear_s >= 3:
                            rear_s = 3
                        load_diff = 15 * rear_s * steering_gain * physics_smm.localAngularVelocity[1]
                    else:
                        load_diff = 0
                    load_diff = clamp(load_diff, -20, 20)
                    self.last_steering_angle = steering_angle
                    self.dash.accGx = physics_smm.accG[0]
                    self.dash.accGy = physics_smm.accG[1]
                    self.dash.accGz = physics_smm.accG[2]
                    self.dash.heading = physics_smm.heading
                    self.dash.pitch = physics_smm.pitch
                    self.dash.roll = physics_smm.roll
                    a = int(physics_smm.wheelLoad[0])
                    b = int(physics_smm.wheelLoad[1])
                    c = int(physics_smm.wheelLoad[2])
                    d = int(physics_smm.wheelLoad[3])
                else:
                    self.game_data.t_rpm = 0
                    self.game_data.t_ffb = 0
                self.game_data_slow.t_car_num = static_smm.numCars
                self.game_data_slow.t_max_rpm = static_smm.maxRPM
                performanceM = physics_smm.PerformanceMeter
                if performanceM >= 32.768:
                    performanceM = 32.768
                else:
                    if performanceM <= -32.768:
                        performanceM = -32.768
                    else:
                        self.game_data.t_performance = int(performanceM * 1000 + 32768)
                        current_time = graphics_smm.currentTime
                        if ':' in current_time:
                            if '-' not in current_time:
                                t_hour, t_min, t_sec = current_time.split(':')
                                self.game_data.t_current_time_hour = int(t_hour)
                                self.game_data.t_current_time_min = int(t_min)
                                self.game_data.t_current_time_sec = int(t_sec)
                            else:
                                self.game_data.t_current_time_hour = 0
                                self.game_data.t_current_time_min = 0
                                self.game_data.t_current_time_sec = 0
                        else:
                            last_time = graphics_smm.lastTime
                            if ':' in last_time:
                                if '-' not in last_time:
                                    t_hour, t_min, t_sec = last_time.split(':')
                                    self.game_data_slow.t_last_time_hour = int(t_hour)
                                    self.game_data_slow.t_last_time_min = int(t_min)
                                    self.game_data_slow.t_last_time_sec = int(t_sec)
                            self.game_data_slow.t_last_time_hour = 0
                            self.game_data_slow.t_last_time_min = 0
                            self.game_data_slow.t_last_time_sec = 0
                        best_time = graphics_smm.bestTime
                        if ':' in best_time and '-' not in best_time:
                            t_hour, t_min, t_sec = best_time.split(':')
                            self.game_data_slow.t_best_time_hour = int(t_hour)
                            self.game_data_slow.t_best_time_min = int(t_min)
                            self.game_data_slow.t_best_time_sec = int(t_sec)
                    self.game_data_slow.t_best_time_hour = 0
                    self.game_data_slow.t_best_time_min = 0
                    self.game_data_slow.t_best_time_sec = 0
                flag = graphics_smm.flag
                if flag == 0:
                    self.game_data.t_yellow_flag = 0
                    self.game_data.t_green_flag = 0
                    self.game_data.t_white_flag = 0
                    self.game_data.t_red_flag = 0
                    self.game_data.t_blue_flag = 0
                    self.game_data.t_black_flag = 0
                    self.game_data.t_black_orange_flag = 0
                    self.game_data.t_half_black_white_flag = 0
                    self.game_data.t_yellow_red_flag = 0
                    self.game_data.t_chequered_flag = 0
                    self.game_data.t_sc_board = 0
                else:
                    if flag == 1:
                        self.game_data.t_blue_flag = 1
                    else:
                        if flag == 2:
                            self.game_data.t_yellow_flag = 1
                        else:
                            if flag == 3:
                                self.game_data.t_black_flag = 1
                            else:
                                if flag == 4:
                                    self.game_data.t_white_flag = 1
                                else:
                                    if flag == 5:
                                        self.game_data.t_chequered_flag = 1
                                    else:
                                        if flag == 6:
                                            pass
                                self.game_data_slow.t_finish_lap = graphics_smm.completedLaps + 1
                                self.game_data_slow.t_lap_number = graphics_smm.numberOfLaps
                                self.game_data_slow.t_pos = graphics_smm.position
                                self.game_data.t_gas = int(physics_smm.gas)
                                self.game_data.t_brake = int(physics_smm.brake)
                                self.game_data.t_clutch = int(physics_smm.Clutch)
                                gear = physics_smm.gear
                                if gear == 0:
                                    self.game_data.t_gear = 30
                                else:
                                    if gear == 1:
                                        self.game_data.t_gear = 31
                                    else:
                                        self.game_data.t_gear = int(gear - 1)
                        self.game_data.t_speed = int(physics_smm.speed + 0.5)
                        self.game_data.t_fuel = int(physics_smm.fuel)
                        self.game_data_slow.t_tc = int(physics_smm.tc)
                        self.game_data_slow.t_abs = int(physics_smm.abs)
                        self.game_data_slow.t_fl_tire_wear = int(physics_smm.tireWear[0]) - 70
                        self.game_data_slow.t_fr_tire_wear = int(physics_smm.tireWear[1]) - 70
                        self.game_data_slow.t_rl_tire_wear = int(physics_smm.tireWear[2]) - 70
                        self.game_data_slow.t_rr_tire_wear = int(physics_smm.tireWear[3]) - 70
                        self.game_data.t_fl_tire_temp = int(physics_smm.TyreTempM[0])
                        self.game_data.t_fr_tire_temp = int(physics_smm.TyreTempM[1])
                        self.game_data.t_rl_tire_temp = int(physics_smm.TyreTempM[2])
                        self.game_data.t_rr_tire_temp = int(physics_smm.TyreTempM[3])
                        self.game_data.t_fl_brake_temp = int(physics_smm.BrakeTemp[0])
                        self.game_data.t_fr_brake_temp = int(physics_smm.BrakeTemp[1])
                        self.game_data.t_rl_brake_temp = int(physics_smm.BrakeTemp[2])
                        self.game_data.t_rr_brake_temp = int(physics_smm.BrakeTemp[3])
                        self.game_data.t_pit_limiter = physics_smm.pitLimiter
                        if static_smm.carModel:
                            try:
                                self.dash.syna_steering_lock = get_steering_lock(self.game_path, static_smm.carModel) * 2
                                preset_cfg = configparser.ConfigParser()
                                preset_cfg.optionxform = str
                                doc_path = os.path.expanduser('~\\Documents') + '\\Assetto Corsa\\cfg\\controls.ini'
                                if os.path.exists(doc_path):
                                    preset_cfg.read(doc_path)
                                    try:
                                        self.dash.max_steering_angle = int(preset_cfg.get('STEER', 'LOCK'))
                                    except:
                                        self.dash.max_steering_angle = 900

                                else:
                                    self.dash.max_steering_angle = 900
                            except Exception as e:
                                print('get_steering_lock error ', e)
                                self.dash.max_steering_angle = 900

                            if self.dash.max_steering_angle <= self.dash.syna_steering_lock:
                                self.dash.max_steering_angle = self.dash.syna_steering_lock
                self.status = True
                return self.game_data
            except Exception as e:
                print('ac updata error', e)
                self.status = False

        else:
            self.status = False
