from traceback import format_exc
from time import sleep, time
from mmap import mmap
from os.path import getmtime
from psutil import pid_exists
import irsdk, math
from setting_define import *
import datetime

class pyDashIRACING:

    def __init__(self, iracing_pid, dash, game_data, enable):
        self.iracing_pid = iracing_pid
        self.game_data = game_data[0]
        self.game_data_slow = game_data[1]
        self.dash = dash
        self.enable = enable
        self.status = False
        try:
            self.ir = irsdk.IRSDK()
            if pid_exists(self.iracing_pid):
                self.status = True
                self.game_data.t_game_id = game_id['ir']
        except Exception as e:
            print('Unable to open shared memory map', e)

    def isRun(self):
        return self.status

    def __del__(self):
        pass

    def update(self):
        if pid_exists(self.iracing_pid) and self.enable:
            try:
                self.ir.startup()
                if self.ir['DriverInfo']:
                    rpm_max = int(self.ir['DriverInfo']['DriverCarRedLine'])
                self.game_data.t_speed = int(self.ir['Speed'] + 0.5)
                self.game_data.t_rpm = int(self.ir['RPM'])
                self.game_data_slow.t_max_rpm = rpm_max
                flag = self.ir['SessionFlags']
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
                    if flag == 32:
                        self.game_data.t_blue_flag = 1
                    else:
                        if flag == 8:
                            self.game_data.t_yellow_flag = 1
                        else:
                            if flag == 65536:
                                self.game_data.t_black_flag = 1
                            else:
                                if flag == 2:
                                    self.game_data.t_white_flag = 1
                                else:
                                    if flag == 1:
                                        self.game_data.t_chequered_flag = 1
                                    current_time = self.ir['LapCurrentLapTime']
                                    current_time = str(datetime.timedelta(seconds=(int(current_time))))
                                    if ':' in current_time:
                                        if '-' not in current_time:
                                            t_hour, t_min, t_sec = current_time.split(':')
                                            self.game_data.t_current_time_hour = int(t_hour)
                                            self.game_data.t_current_time_min = int(t_min)
                                            self.game_data.t_current_time_sec = int(t_sec)
                                    self.game_data.t_current_time_hour = 0
                                    self.game_data.t_current_time_min = 0
                                    self.game_data.t_current_time_sec = 0
                                last_time = self.ir['LapLastLapTime']
                                last_time = str(datetime.timedelta(seconds=(int(last_time))))
                                if ':' in last_time:
                                    if '-' not in last_time:
                                        t_hour, t_min, t_sec = last_time.split(':')
                                        self.game_data.t_last_time_hour = int(t_hour)
                                        self.game_data.t_last_time_min = int(t_min)
                                        self.game_data.t_last_time_sec = int(t_sec)
                                self.game_data.t_last_time_hour = 0
                                self.game_data.t_last_time_min = 0
                                self.game_data.t_last_time_sec = 0
                            best_time = self.ir['LapBestLapTime']
                            best_time = str(datetime.timedelta(seconds=(int(best_time))))
                            if ':' in best_time:
                                if '-' not in best_time:
                                    t_hour, t_min, t_sec = best_time.split(':')
                                    self.game_data.t_best_time_hour = int(t_hour)
                                    self.game_data.t_best_time_min = int(t_min)
                                    self.game_data.t_best_time_sec = int(t_sec)
                            self.game_data.t_best_time_hour = 0
                            self.game_data.t_best_time_min = 0
                            self.game_data.t_best_time_sec = 0
                        self.game_data.t_finish_lap = self.ir['LapCompleted']
                        self.game_data.t_pos = self.ir['PlayerCarPosition']
                        self.game_data.t_car_num = self.ir['DCDriversSoFar']
                        gear = self.ir['Gear']
                        if gear == -1:
                            self.game_data.t_gear = 30
                        else:
                            if gear == 0:
                                self.game_data.t_gear = 31
                            else:
                                self.game_data.t_gear = int(gear)
                self.game_data.t_fuel = int(self.ir['FuelLevelPct'])
                self.game_data.t_fl_tire_wear = int(self.ir['LFwearM']) - 70
                self.game_data.t_fr_tire_wear = int(self.ir['RFwearM']) - 70
                self.game_data.t_rl_tire_wear = int(self.ir['LRwearM']) - 70
                self.game_data.t_rr_tire_wear = int(self.ir['RRwearM']) - 70
                self.game_data.t_fl_tire_temp = int(self.ir['LFtempCM'])
                self.game_data.t_fr_tire_temp = int(self.ir['RFtempCM'])
                self.game_data.t_rl_tire_temp = int(self.ir['LRtempCM'])
                self.game_data.t_rr_tire_temp = int(self.ir['RRtempCM'])
                self.game_data.t_fl_brake_temp = int(self.ir['FuelLevelPct'])
                self.game_data.t_fr_brake_temp = int(self.ir['FuelLevelPct'])
                self.game_data.t_rl_brake_temp = int(self.ir['FuelLevelPct'])
                self.game_data.t_rr_brake_temp = int(self.ir['FuelLevelPct'])
                self.game_data.t_gas = int(self.ir['Throttle'])
                self.game_data.t_brake = int(self.ir['Brake'])
                self.game_data.t_clutch = int(self.ir['Clutch'])
                if self.game_data.t_speed < 0:
                    self.game_data.t_speed = 0
                if self.game_data.t_rpm < 0:
                    self.game_data.t_rpm = 0
                if self.game_data_slow.t_max_rpm < 0:
                    self.game_data_slow.t_max_rpm = 0
                self.dash.max_steering_angle = math.degrees(self.ir['SteeringWheelAngleMax'])
                self.status = True
                return self.game_data
            except Exception as e:
                print('updata error', e)
                self.status = False

        else:
            self.status = False
