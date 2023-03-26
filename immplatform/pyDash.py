from pyDashR3E import pyDashR3E
from pyDashRF1 import pyDashRF1
from pyDashAC import pyDashAC
from pyDashACC import pyDashACC
from pyDashFH4 import pyDashFH4
from pyDashPCARS import pyDashPCARS
from pyDashF1_2021 import pyDashF1_2021
from pyDashF1_2020 import pyDashF1_2020
from pyDashF1_2019 import pyDashF1_2019
from pyDashF1_2018 import pyDashF1_2018
from pyDashDRR2 import pyDashDRR2
from pyDashETS2 import pyDashETS2
from pyDashIRACING import pyDashIRACING
from pyDashAMS2 import pyDashAMS2
from sys import exit
from distutils.util import strtobool
import json
from datetime import datetime
from uitl import Utiliy
from uitl import Refresher
from psutil import process_iter, Process
import os, re, threading
from PyQt5.QtCore import QObject, pyqtSlot, pyqtSignal
from setting_define import *
import configparser
from ctypes import c_uint16, string_at, addressof, sizeof, Structure, memmove
import subprocess
from psutil import process_iter, Process
ui_cfg = configparser.ConfigParser()
ui_cfg.read('./cfg/ui_setting.cfg', encoding='UTF-8')

def execute_cmd(cmd, mode='r', buffering=-1):
    proc = subprocess.Popen(cmd,
      shell=True,
      stdout=(subprocess.PIPE),
      stderr=(subprocess.STDOUT),
      stdin=(subprocess.PIPE))
    proc.stdin.close()
    result = proc.stdout.read().decode('gbk', 'ignore')
    proc.stdout.close()
    return result


def clamp(value, minvalue, maxvalue):
    return max(minvalue, min(value, maxvalue))


class DashChooser(QObject):
    gameStatusChange = pyqtSignal(str)

    def __init__(self, main, ui_cfg):
        super(DashChooser, self).__init__()
        self.clearAllData()
        self.main = main
        self.game_proc = None
        self.dash_close = False
        self.ui_cfg = ui_cfg
        self.slip = 128
        self.rear_slip = 0
        self.load_diff = 128
        self.center_damper = 0
        self.accGx = self.accGy = self.accGz = 0
        self.heading = self.pitch = self.roll = 0
        self.load_time = 0
        self.data_slow_time = 0
        self.game_data_thread = Refresher(2)
        self.game_data_thread.sinOut.connect(self.updateGameData)
        self.game_data_thread.start()

    def __del__(self):
        self.dash_close = True
        if self.game_proc:
            self.game_proc.__del__()

    def clearAllData(self):
        for field, _type, size in gameData._fields_:
            setattr(gameData, field, 0)

        for field, _type, size in gameData_slow._fields_:
            setattr(gameData_slow, field, 0)

        self.max_steering_angle = 720
        self.syna_steering_lock = 720
        gameData.t_load_diff = 128
        gameData.t_slip_ratio_for_ffb = 128
        try:
            game_data = string_at(addressof(gameData), sizeof(gameData))
            game_data = list(game_data)
            self.main.hidchooser.sent_game_info_handler(SETTING_GAME_INFO_FAST, game_data)
            game_data_slow = string_at(addressof(gameData_slow), sizeof(gameData_slow))
            game_data_slow = list(game_data_slow)
            self.main.hidchooser.sent_game_info_handler(SETTING_GAME_INFO_SLOW, game_data_slow)
        except Exception as e:
            print('clearAllData ', e)

    def findGameRunning(self):
        if self.game_proc == None:
            self.gameStatusChange.emit('None')
            try:
                f = execute_cmd('tasklist').split('\n')
                for eachLine in f:
                    info = re.split('[ ]+', eachLine)
                    p_name = info[0].lower()
                    if p_name == 'rrre.exe' or p_name == 'rrre64.exe':
                        p_pid = int(info[1])
                        self.game_proc = pyDashR3E(p_pid, self, [gameData, gameData_slow], eval(ui_cfg.get('r3e', 'tele_enable')))
                        self.gameStatusChange.emit('RaceRoom Racing Experience')
                        break
                    elif p_name == 'ams2avx.exe':
                        p_pid = int(info[1])
                        self.game_proc = pyDashAMS2(p_pid, self, [gameData, gameData_slow], eval(ui_cfg.get('ams2', 'tele_enable')))
                        self.gameStatusChange.emit('Automobillsta 2')
                        break
                    elif p_name == 'rfactor2.exe':
                        break
                    elif p_name == 'acs.exe' or p_name == 'assettocorsa.exe':
                        p_pid = int(info[1])
                        self.game_proc = pyDashAC(p_pid, self, [gameData, gameData_slow], eval(ui_cfg.get('ac', 'tele_enable')))
                        self.gameStatusChange.emit('Assetto Corsa')
                        break
                    elif p_name == 'eurotrucks2.exe':
                        break
                    elif p_name == 'acc.exe':
                        p_pid = int(info[1])
                        self.game_proc = pyDashACC(p_pid, self, [gameData, gameData_slow], eval(ui_cfg.get('acc', 'tele_enable')))
                        self.gameStatusChange.emit('Assetto Corsa Competizione')
                        break
                    elif p_name == 'forzahorizon5.exe':
                        p_pid = int(info[1])
                        ip = self.ui_cfg.get('fh5', 'ip')
                        port = self.ui_cfg.get('fh5', 'port')
                        if self.game_proc == None:
                            self.game_proc = pyDashFH4(p_pid, self, [gameData, gameData_slow], port, eval(ui_cfg.get('fh5', 'tele_enable')))
                            self.gameStatusChange.emit('Forza Horizon5')
                        break
                    elif p_name == 'forzahorizon4.exe':
                        p_pid = int(info[1])
                        ip = self.ui_cfg.get('fh4', 'ip')
                        port = self.ui_cfg.get('fh4', 'port')
                        if self.game_proc == None:
                            self.game_proc = pyDashFH4(p_pid, self, [gameData, gameData_slow], port, eval(ui_cfg.get('fh4', 'tele_enable')))
                            self.gameStatusChange.emit('Forza Horizon4')
                        break
                    elif p_name == 'pcars.exe' or p_name == 'pcars64.exe':
                        p_pid = int(info[1])
                        self.game_proc = pyDashPCARS(p_pid, self, [gameData, gameData_slow], eval(ui_cfg.get('pcar1', 'tele_enable')), 1)
                        self.gameStatusChange.emit('Project CARS')
                        print('pcars')
                        break
                    elif p_name == 'pcars2.exe' or p_name == 'pcars2avx.exe':
                        p_pid = int(info[1])
                        self.game_proc = pyDashPCARS(p_pid, self, [gameData, gameData_slow], eval(ui_cfg.get('pcar2', 'tele_enable')), 2)
                        self.gameStatusChange.emit('Project CARS 2')
                        print('pcars2')
                        break
                    elif p_name == 'f1_2020_dx12.exe' or p_name == 'f1_2020.exe':
                        ip = self.ui_cfg.get('f12020', 'ip')
                        port = self.ui_cfg.get('f12020', 'port')
                        if self.game_proc == None:
                            p_pid = int(info[1])
                            self.game_proc = pyDashF1_2020(p_pid, self, [gameData, gameData_slow], port, eval(ui_cfg.get('f12020', 'tele_enable')))
                            self.gameStatusChange.emit('F1 2020')
                        break
                    elif p_name == 'f1_2021_dx12.exe' or p_name == 'f1_2021.exe':
                        ip = self.ui_cfg.get('f12021', 'ip')
                        port = self.ui_cfg.get('f12021', 'port')
                        if self.game_proc == None:
                            p_pid = int(info[1])
                            self.game_proc = pyDashF1_2021(p_pid, self, [gameData, gameData_slow], port, eval(ui_cfg.get('f12021', 'tele_enable')))
                            self.gameStatusChange.emit('F1 2021')
                        break
                    elif p_name == 'f1_2019_dx12.exe' or p_name == 'f1_2019.exe':
                        ip = self.ui_cfg.get('f12019', 'ip')
                        port = self.ui_cfg.get('f12019', 'port')
                        if self.game_proc == None:
                            p_pid = int(info[1])
                            self.game_proc = pyDashF1_2019(p_pid, self, [gameData, gameData_slow], port, eval(ui_cfg.get('f12019', 'tele_enable')))
                            self.gameStatusChange.emit('F1 2019')
                        break
                    elif p_name == 'f1_2018.exe':
                        ip = self.ui_cfg.get('f12018', 'ip')
                        port = self.ui_cfg.get('f12018', 'port')
                        if self.game_proc == None:
                            p_pid = int(info[1])
                            self.game_proc = pyDashF1_2018(p_pid, self, [gameData, gameData_slow], port, eval(ui_cfg.get('f12018', 'tele_enable')))
                            self.gameStatusChange.emit('F1 2018')
                        break
                    elif p_name == 'dirtrally2.exe':
                        ip = self.ui_cfg.get('drr2', 'ip')
                        port = self.ui_cfg.get('drr2', 'port')
                        if self.game_proc == None:
                            p_pid = int(info[1])
                            self.game_proc = pyDashDRR2('DiRT Rally 2.0', p_pid, self, [gameData, gameData_slow], port, eval(ui_cfg.get('drr2', 'tele_enable')), 'drr2')
                            self.gameStatusChange.emit('DiRT Rally 2.0')
                        print(1)
                        break
                    else:
                        if p_name == 'drt.exe':
                            ip = self.ui_cfg.get('drr', 'ip')
                            port = self.ui_cfg.get('drr', 'port')
                            if self.game_proc == None:
                                p_pid = int(info[1])
                                self.game_proc = pyDashDRR2('DiRT Rally', p_pid, self, [gameData, gameData_slow], port, eval(ui_cfg.get('drr', 'tele_enable')), 'dr')
                                self.gameStatusChange.emit('DiRT Rally')
                            print(2)
                            break
                        else:
                            if p_name == 'dirt4.exe':
                                ip = self.ui_cfg.get('dr4', 'ip')
                                port = self.ui_cfg.get('dr4', 'port')
                                if self.game_proc == None:
                                    p_pid = int(info[1])
                                    self.game_proc = pyDashDRR2('DiRT 4', p_pid, self, [gameData, gameData_slow], port, eval(ui_cfg.get('dr4', 'tele_enable')), 'dr4')
                                    self.gameStatusChange.emit('DiRT 4')
                                break
                            elif p_name == 'iracingsim64dx11.exe':
                                p_pid = int(info[1])
                                self.game_proc = pyDashIRACING(p_pid, self, [gameData, gameData_slow], eval(ui_cfg.get('ir', 'tele_enable')))
                                self.gameStatusChange.emit('iRacing')
                                break

            except Exception as e:
                self.slip = 128
                self.rear_slip = 0
                self.load_diff = 128
                self.center_damper = 0
                print('Unhandled exception, ', e)
                for i in ui_cfg.sections():
                    print(i)

    def updateGameData(self):
        if self.game_proc != None and self.game_proc.isRun():
            self.game_data_thread.setTime(0.016666666666666666)
            self.game_proc.update()
            self.data_slow_time = self.data_slow_time + 1
            if self.max_steering_angle != 0:
                if self.main.base_ui.range_auto_radioButton.isChecked():
                    if self.max_steering_angle != self.main.base_ui.base_angle_range_Slider.value():
                        self.main.base_ui.base_angle_range_Slider.setValue(self.max_steering_angle)
                    if self.main.hidchooser.ffb_sync_steering_lock != self.syna_steering_lock:
                        self.main.hidchooser.sent_handler(SETTING_SYNA_LOCK, self.syna_steering_lock)
            if gameData.t_game_id != 0:
                slip = self.slip
                understeer_effect = self.main.base_ui.Understeer_Effect_Slider.value()
                slip_inc_effect_point = 0.7
                slip_dec_effect_point = 1.0
                slip_inc_effect_mult = 110 + understeer_effect * 5
                slip_dec_effect_mult = 120 + understeer_effect * 5
                slip_dec_effect_amp = 100 - understeer_effect * 4
                slip_max_inc_effect = int(128 + (slip_dec_effect_point - slip_inc_effect_point) * slip_inc_effect_mult)
                slip_max_inc_effect = clamp(slip_max_inc_effect, 0, 255)
                if self.rear_slip > 0.5:
                    t_rear_slip_ratio_for_ffb = int((self.rear_slip - 0.5) * 60)
                    gameData.t_rear_slip_ratio_for_ffb = clamp(t_rear_slip_ratio_for_ffb, 0, 60)
                else:
                    gameData.t_rear_slip_ratio_for_ffb = 0
                if self.rear_slip < 1.0:
                    if understeer_effect > 0:
                        if slip >= slip_inc_effect_point:
                            if slip < slip_dec_effect_point:
                                t_slip_ratio_for_ffb = int(128 + (slip - slip_inc_effect_point) * slip_inc_effect_mult)
                                gameData.t_slip_ratio_for_ffb = clamp(t_slip_ratio_for_ffb, 128, 255)
                        else:
                            if slip >= slip_dec_effect_point:
                                t_slip_ratio_for_ffb = int((slip - slip_dec_effect_point) * slip_dec_effect_mult)
                                aa = slip_max_inc_effect - slip_dec_effect_amp
                                if aa < 0:
                                    aa = 0
                                else:
                                    if aa > slip_max_inc_effect:
                                        aa = slip_max_inc_effect
                                gameData.t_slip_ratio_for_ffb = slip_max_inc_effect - clamp(t_slip_ratio_for_ffb, 0, aa)
                            else:
                                gameData.t_slip_ratio_for_ffb = 128
                else:
                    gameData.t_slip_ratio_for_ffb = 128
                car_speed = gameData.t_speed
                t_dyna_damping_for_ffb = int(car_speed * self.main.base_ui.Dyna_Damping_Slider.value() / 200)
                gameData.t_dyna_damping_for_ffb = clamp(t_dyna_damping_for_ffb, 0, 63)
                t_load_diff = int(128 + self.load_diff)
                gameData.t_load_diff = clamp(t_load_diff, 0, 255)
                slip = round(slip, 2)
                game_data = string_at(addressof(gameData), sizeof(gameData))
                game_data = list(game_data)
                self.main.hidchooser.sent_game_info_handler(SETTING_GAME_INFO_FAST, game_data)
                if self.data_slow_time % 6 == 0:
                    game_data_slow = string_at(addressof(gameData_slow), sizeof(gameData_slow))
                    game_data_slow = list(game_data_slow)
                    self.main.hidchooser.sent_game_info_handler(SETTING_GAME_INFO_SLOW, game_data_slow)
                _accGx = int(self.accGx * 1000) + 32768
                _accGy = int(self.accGy * 1000) + 32768
                _accGz = int(self.accGz * 1000) + 32768
                _heading = int(self.heading * 1000) + 32768
                _pitch = int(self.pitch * 1000) + 32768
                _roll = int(self.roll * 1000) + 32768
                self.main.gforce_hidchooser.sent_gforce_handler(SETTING_GAME_INFO_FAST, [
                 _accGx & 255, _accGx >> 8 & 255,
                 _accGy & 255, _accGy >> 8 & 255,
                 _accGz & 255, _accGz >> 8 & 255,
                 _heading & 255, _heading >> 8 & 255,
                 _pitch & 255, _pitch >> 8 & 255,
                 _roll & 255, _roll >> 8 & 255])
        else:
            self.game_data_thread.setTime(2)
            self.clearAllData()
            t1 = threading.Timer(1, self.findGameRunning, None)
            t1.start()
            if self.game_proc:
                self.game_proc.__del__()
            self.game_proc = None
            self.game_id = 0
            self.data_slow_time = 0

    def getRpmPercentage(self):
        if self.game_proc != None and self.game_proc.isRun():
            if gameData_slow.t_max_rpm == 0:
                return
            return float(gameData.t_rpm) / gameData_slow.t_max_rpm
        else:
            return

    def getSpeed(self):
        return self.speed

    def getSlip(self):
        return self.slip
