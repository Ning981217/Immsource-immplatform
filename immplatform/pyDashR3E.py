from traceback import format_exc
from time import sleep, time
from mmap import mmap
from os.path import getmtime
from pyR3E import *
from psutil import pid_exists
from setting_define import *
import datetime

class pyDashR3E:

    def __init__(self, r3e_pid, dash, game_data, enable):
        self.r3e_pid = r3e_pid
        self.game_data = game_data[0]
        self.game_data_slow = game_data[1]
        self.enable = enable
        self.status = False
        self.dash = dash
        try:
            self.r3e_smm_handle = mmap(fileno=0, length=(sizeof(r3e_shared)), tagname=r3e_smm_tag)
            if pid_exists(self.r3e_pid):
                self.status = True
                self.game_data.t_game_id = game_id['r3e']
        except Exception as e:
            print('Unable to open shared memory map', e)

    def isRun(self):
        return self.status

    def __del__(self):
        pass

    def update(self):
        if pid_exists(self.r3e_pid) and self.enable:
            try:
                self.r3e_smm_handle.seek(0)
                smm = r3e_shared.from_buffer_copy(self.r3e_smm_handle)
                if smm.game_in_replay == 0:
                    self.game_data.t_speed = int(mps_to_kph(smm.car_speed) + 0.5)
                    self.game_data.t_rpm = int(rps_to_rpm(smm.engine_rps))
                    self.game_data_slow.t_max_rpm = int(rps_to_rpm(smm.max_engine_rps))
                    self.game_data.t_finish_lap = smm.completed_laps
                    self.game_data.t_lap_number = smm.number_of_laps
                    self.game_data.t_pos = smm.position
                    self.game_data.t_gas = int(smm.throttle)
                    self.game_data.t_brake = int(smm.brake)
                    self.game_data.t_clutch = int(smm.clutch)
                    gear = smm.gear
                    if gear == 0:
                        self.game_data.t_gear = 30
                    else:
                        if gear == 1:
                            self.game_data.t_gear = 31
                        else:
                            self.game_data.t_gear = int(gear - 1)
                            current_time = smm.lap_time_current_self
                            current_time = str(datetime.timedelta(seconds=(int(current_time))))
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
                            last_time = smm.lap_time_previous_self
                            last_time = str(datetime.timedelta(seconds=(int(last_time))))
                            if ':' in last_time:
                                if '-' not in last_time:
                                    t_hour, t_min, t_sec = last_time.split(':')
                                    self.game_data.t_last_time_hour = int(t_hour)
                                    self.game_data.t_last_time_min = int(t_min)
                                    self.game_data.t_last_time_sec = int(t_sec)
                                else:
                                    self.game_data.t_last_time_hour = 0
                                    self.game_data.t_last_time_min = 0
                                    self.game_data.t_last_time_sec = 0
                                best_time = smm.lap_time_best_self
                                best_time = str(datetime.timedelta(seconds=(int(best_time))))
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
                            else:
                                self.game_data.t_fl_tire_wear = int(smm.tire_wear[0]) - 70
                                self.game_data.t_fr_tire_wear = int(smm.tire_wear[1]) - 70
                                self.game_data.t_rl_tire_wear = int(smm.tire_wear[2]) - 70
                                self.game_data.t_rr_tire_wear = int(smm.tire_wear[3]) - 70
                                self.game_data.t_fl_tire_temp = int(smm.tire_temp[0].current_temp[0])
                                self.game_data.t_fr_tire_temp = int(smm.tire_temp[1].current_temp[0])
                                self.game_data.t_rl_tire_temp = int(smm.tire_temp[2].current_temp[0])
                                self.game_data.t_rr_tire_temp = int(smm.tire_temp[3].current_temp[0])
                                self.game_data.t_fl_brake_temp = int(smm.brake_temp[0].current_temp)
                                self.game_data.t_fr_brake_temp = int(smm.brake_temp[1].current_temp)
                                self.game_data.t_rl_brake_temp = int(smm.brake_temp[2].current_temp)
                                self.game_data.t_rr_brake_temp = int(smm.brake_temp[3].current_temp)
                                if smm.flags.blue == 1:
                                    self.game_data.t_blue_flag = 1
                                else:
                                    self.game_data.t_blue_flag = 0
                            if smm.flags.yellow == 1:
                                self.game_data.t_yellow_flag = 1
                            else:
                                self.game_data.t_yellow_flag = 0
                            if smm.flags.black == 1:
                                self.game_data.t_black_flag = 1
                            else:
                                self.game_data.t_black_flag = 0
                            if smm.flags.white == 1:
                                self.game_data.t_white_flag = 1
                            else:
                                self.game_data.t_white_flag = 0
                            if smm.flags.green == 1:
                                self.game_data.t_green_flag = 1
                            else:
                                self.game_data.t_green_flag = 0
                            print(smm.flags.green)
                            if smm.flags.checkered != -1:
                                self.game_data.t_chequered_flag = 1
                            else:
                                self.game_data.t_chequered_flag = 0
                            if self.game_data.t_speed < 0:
                                self.game_data.t_speed = 0
                            if self.game_data.t_rpm < 0:
                                self.game_data.t_rpm = 0
                            if self.game_data_slow.t_max_rpm < 0:
                                self.game_data_slow.t_max_rpm = 0
                        self.dash.max_steering_angle = smm.steer_wheel_range_degrees
                        self.dash.syna_steering_lock = smm.steer_wheel_range_degrees
                self.status = True
                return self.game_data
            except Exception as e:
                print('updata error', e)
                self.status = False

        else:
            self.status = False
