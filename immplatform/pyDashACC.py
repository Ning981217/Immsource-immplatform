from traceback import format_exc
from time import sleep, time
from mmap import mmap
from os.path import getmtime
from pyACC import *
from psutil import pid_exists
import os, re
from setting_define import *
car_angle = {'alpine_a110_gt4':720, 
 'aston_martin_v8_vantage_gt4':640, 
 'amr_v8_vantage_gt4':640, 
 'audi_r8_lms_gt4':720, 
 'audi_r8_gt4':720, 
 'bmw_m4_gt4':500, 
 'bmw_m4_gt3':500, 
 'chevrolet_camaro_gt4.r':720, 
 'chevrolet_camaro_gt4r':720, 
 'ginetta_g55_gt4':720, 
 'ktm_xbow_gt4':580, 
 'ktm_x_bow_gt4':580, 
 'maserati_granturismo_mc_gt4':900, 
 'maserati_mc_gt4':900, 
 'mclaren_570s_gt4':480, 
 'mercedes_amg_gt4':500, 
 'porsche_718_cayman_gt4':800, 
 'porsche_718_cayman_gt4_mr':800, 
 'amr_v12_vantage_gt3':640, 
 'audi_r8_lms':720, 
 'bentley_continental_gt3_2015':640, 
 'bentley_continental_gt3_2016':640, 
 'bentley_continental_gt3_2018':640, 
 'bmw_m6_gt3':565, 
 'emil_frey_jaguar_gt3':720, 
 'jaguar_g3':720, 
 'ferrari_488_gt3':480, 
 'honda_nsx_gt3':620, 
 'lamborghini_huracan_gt3':620, 
 'lamborghini_huracan_st':620, 
 'lexus_rc_f_gt3':640, 
 'mclaren_650s_gt3':480, 
 'mercedes_amg_gt3':640, 
 'nissan_gt_r_gt3_2015':640, 
 'nissan_gt_r_gt3_2018':640, 
 'nissan_gt_r_gt3_2017':640, 
 'porsche_991_gt3_r':800, 
 'porsche_991ii_gt3_cup':800, 
 'reiter_engineering_r_ex_gt3':720, 
 'aston_martin_racing_v8_vantage_gt3':640, 
 'amr_v8_vantage_gt3':640, 
 'audi_r8_lms_evo':720, 
 'bentley_continental_gt3':640, 
 'bmw_m6_gt3':565, 
 'ferrari_488_gt3':480, 
 'ferrari_488_gt3_evo':480, 
 'honda_nsx_gt3_evo':620, 
 'lamborghini_huracan_gt3':620, 
 'lamborghini_huracan_gt3_evo':620, 
 'lamborghini_gallardo_rex':620, 
 'lexus_rc_f_gt3':640, 
 'mclaren_720s_gt3':480, 
 'mercedes_amg_gt3':640, 
 'mercedes_amg_gt3_evo':640, 
 'nissan_gt_r_gt3':640, 
 'porsche_991ii_gt3_r':800}

class pyDashACC:

    def __init__(self, acc_pid, dash, game_data, enable):
        self.acc_pid = acc_pid
        self.game_data = game_data[0]
        self.game_data_slow = game_data[1]
        self.enable = enable
        self.dash = dash
        self.status = False
        try:
            accMapHandle['physics'] = mmap(fileno=0, length=(sizeof(accPhysics)), tagname=(accMapTag['physics']))
            accMapHandle['graphics'] = mmap(fileno=0, length=(sizeof(accGraphics)), tagname=(accMapTag['graphics']))
            accMapHandle['static'] = mmap(fileno=0, length=(sizeof(accStatic)), tagname=(accMapTag['static']))
            if pid_exists(self.acc_pid):
                self.status = True
                self.game_data.t_game_id = game_id['acc']
        except Exception as e:
            print('Unable to open shared memory map', e)

    def isRun(self):
        return self.status

    def __del__(self):
        pass

    def update(self):
        if pid_exists(self.acc_pid) and self.enable:
            try:
                accMapHandle['physics'].seek(0)
                accMapHandle['graphics'].seek(0)
                accMapHandle['static'].seek(0)
                physics_smm = accPhysics.from_buffer_copy(accMapHandle['physics'])
                graphics_smm = accGraphics.from_buffer_copy(accMapHandle['graphics'])
                static_smm = accStatic.from_buffer_copy(accMapHandle['static'])
                status = graphics_smm.AC_STATUS
                if status == 2:
                    self.game_data.t_speed = int(physics_smm.speedKmh + 0.5)
                    self.game_data.t_rpm = physics_smm.rpm
                    self.game_data_slow.t_max_rpm = static_smm.maxRpm
                    self.dash.slip = (physics_smm.wheelSlip[0] + physics_smm.wheelSlip[1]) / 2
                    self.dash.rear_slip = (physics_smm.wheelSlip[2] + physics_smm.wheelSlip[3]) / 2
                    ave_load = (physics_smm.wheelLoad[0] + physics_smm.wheelLoad[1]) / 2
                    sub_load = physics_smm.wheelLoad[0] - physics_smm.wheelLoad[1]
                    try:
                        self.dash.load_diff = physics_smm.accG[0]
                    except Exception as e:
                        self.dash.load_diff = 0
                        print('e', e)

                    doc_path = os.path.expanduser('~\\Documents') + '\\Assetto Corsa Competizione\\Config\\controls.json'
                    if os.path.exists(doc_path):
                        with open(doc_path, 'r', encoding='UTF-8') as (f):
                            for line in f.readlines():
                                if 'steerLock' in line:
                                    self.dash.max_steering_angle = int(re.sub('\\D', '', line))
                                    break

                    else:
                        self.dash.max_steering_angle = 900
                    self.game_data.t_car_num = static_smm.numCars
                    performanceM = physics_smm.performanceMeter
                    if performanceM >= 32.768:
                        performanceM = 32.768
                    else:
                        if performanceM <= -32.768:
                            performanceM = -32.768
                        self.game_data.t_performance = int(performanceM * 1000 + 32768)
                        current_time = graphics_smm.currentTime
                        if ':' in current_time:
                            if '-' not in current_time:
                                t_hour, t_min, t_sec = current_time.split(':')
                                self.game_data.t_current_time_hour = int(t_hour)
                                self.game_data.t_current_time_min = int(t_min)
                                self.game_data.t_current_time_sec = int(t_sec)
                        self.game_data.t_current_time_hour = 0
                        self.game_data.t_current_time_min = 0
                        self.game_data.t_current_time_sec = 0
                    last_time = graphics_smm.lastTime
                    if ':' in last_time:
                        if '-' not in last_time:
                            t_hour, t_min, t_sec = last_time.split(':')
                            self.game_data.t_last_time_hour = int(t_hour)
                            self.game_data.t_last_time_min = int(t_min)
                            self.game_data.t_last_time_sec = int(t_sec)
                    self.game_data.t_last_time_hour = 0
                    self.game_data.t_last_time_min = 0
                    self.game_data.t_last_time_sec = 0
                else:
                    best_time = graphics_smm.bestTime
                    if ':' in best_time:
                        if '-' not in best_time:
                            t_hour, t_min, t_sec = best_time.split(':')
                            self.game_data.t_best_time_hour = int(t_hour)
                            self.game_data.t_best_time_min = int(t_min)
                            self.game_data.t_best_time_sec = int(t_sec)
                        else:
                            self.game_data.t_best_time_hour = 0
                            self.game_data.t_best_time_min = 0
                            self.game_data.t_best_time_sec = 0
                        self.game_data.t_yellow_flag = graphics_smm.GlobalYellow
                        self.game_data.t_red_flag = graphics_smm.GlobalRed
                        self.game_data.t_white_flag = graphics_smm.GlobalWhite
                        self.game_data.t_finish_lap = graphics_smm.completedLaps + 1
                        self.game_data.t_lap_number = graphics_smm.numberOfLaps
                        self.game_data.t_pos = graphics_smm.position
                        self.game_data.t_gas = int(physics_smm.gas)
                        self.game_data.t_brake = int(physics_smm.brake)
                        self.game_data.t_clutch = int(physics_smm.clutch)
                        gear = physics_smm.gear
                        if gear == 0:
                            self.game_data.t_gear = 30
                        else:
                            if gear == 1:
                                self.game_data.t_gear = 31
                            else:
                                self.game_data.t_gear = int(gear - 1)
                            self.game_data.t_fuel = int(physics_smm.fuel)
                            self.game_data.t_tc_running = int(physics_smm.tc)
                            self.game_data.t_abs_running = int(physics_smm.abs)
                            self.game_data.t_has_drs = int(physics_smm.drs)
                            self.game_data.t_fl_tire_wear = int(physics_smm.tyreWear[0]) - 70
                            self.game_data.t_fr_tire_wear = int(physics_smm.tyreWear[1]) - 70
                            self.game_data.t_rl_tire_wear = int(physics_smm.tyreWear[2]) - 70
                            self.game_data.t_rr_tire_wear = int(physics_smm.tyreWear[3]) - 70
                            self.game_data.t_fl_tire_temp = int(physics_smm.tyreTemp[0])
                            self.game_data.t_fr_tire_temp = int(physics_smm.tyreTemp[1])
                            self.game_data.t_rl_tire_temp = int(physics_smm.tyreTemp[2])
                            self.game_data.t_rr_tire_temp = int(physics_smm.tyreTemp[3])
                            self.game_data.t_fl_brake_temp = int(physics_smm.brakeTemp[0])
                            self.game_data.t_fr_brake_temp = int(physics_smm.brakeTemp[1])
                            self.game_data.t_rl_brake_temp = int(physics_smm.brakeTemp[2])
                            self.game_data.t_rr_brake_temp = int(physics_smm.brakeTemp[3])
                            self.game_data.t_pit_limiter = physics_smm.pitLimiterOn
                            try:
                                self.dash.syna_steering_lock = car_angle[static_smm.carModel]
                            except Exception as e:
                                self.dash.max_steering_angle = 900
                                print('acc ', e)

                    else:
                        self.game_data.t_speed = 0
                    self.game_data.t_rpm = 0
                self.status = True
                return self.game_data
            except Exception as e:
                print('updata error', e)
                self.status = False

        else:
            self.status = False