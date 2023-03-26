from traceback import format_exc
from time import sleep, time
from mmap import mmap
from os.path import getmtime
from pyPCARS import *
from psutil import pid_exists
from setting_define import *
import datetime

class pyDashPCARS:

    def __init__(self, pcars_pid, dash, game_data, enable, ver):
        self.pcars_pid = pcars_pid
        self.game_data = game_data[0]
        self.game_data_slow = game_data[1]
        self.enable = enable
        self.dash = dash
        self.status = False
        try:
            self.pcarsMapHandle = mmap(fileno=0, length=(sizeof(pcarsPhysics)), tagname=pcarsMapTag)
            if pid_exists(self.pcars_pid):
                self.status = True
                self.game_data.t_game_id = game_id[('pcar' + str(ver))]
        except Exception as e:
            print('Unable to open shared memory map', e)

    def isRun(self):
        return self.status

    def __del__(self):
        pass

    def update(self):
        if pid_exists(self.pcars_pid) and self.enable:
            try:
                self.pcarsMapHandle.seek(0)
                physics_smm = pcarsPhysics.from_buffer_copy(self.pcarsMapHandle)
                self.game_data.t_speed = int(physics_smm.mSpeed + 0.5)
                self.game_data.t_rpm = int(physics_smm.mRpm)
                self.game_data_slow.t_max_rpm = int(physics_smm.mMaxRPM)
                ParticipantInfo = physics_smm.mParticipantInfo[0]
                self.game_data.t_finish_lap = int(ParticipantInfo.mLapsCompleted)
                self.game_data.t_lap_number = int(ParticipantInfo.mCurrentLap)
                self.game_data.t_pos = int(ParticipantInfo.mRacePosition)
                self.game_data.t_car_num = int(physics_smm.mNumParticipants)
                current_time = physics_smm.mCurrentTime
                t_msec = int((current_time - int(current_time)) * 1000)
                current_time = str(datetime.timedelta(seconds=current_time))
                if ':' in current_time and '-' not in current_time:
                    t_hour, t_min, t_sec = current_time.split(':')
                    self.game_data.t_current_time_hour = int(t_min)
                    self.game_data.t_current_time_min = int(t_sec)
                    self.game_data.t_current_time_sec = int(t_msec)
                else:
                    self.game_data.t_current_time_hour = 0
                    self.game_data.t_current_time_min = 0
                    self.game_data.t_current_time_sec = 0
                last_time = physics_smm.mLastLapTime
                t_msec = int((last_time - int(last_time)) * 1000)
                last_time = str(datetime.timedelta(seconds=last_time))
                if ':' in last_time:
                    if '-' not in last_time:
                        t_hour, t_min, t_sec = last_time.split(':')
                        self.game_data.t_last_time_hour = int(t_min)
                        self.game_data.t_last_time_min = int(t_sec)
                        self.game_data.t_last_time_sec = int(t_msec)
                    else:
                        self.game_data.t_last_time_hour = 0
                        self.game_data.t_last_time_min = 0
                        self.game_data.t_last_time_sec = 0
                else:
                    best_time = physics_smm.mBestLapTime
                    t_msec = int((best_time - int(best_time)) * 1000)
                    best_time = str(datetime.timedelta(seconds=best_time))
                    if ':' in best_time:
                        if '-' not in best_time:
                            t_hour, t_min, t_sec = best_time.split(':')
                            self.game_data.t_best_time_hour = int(t_min)
                            self.game_data.t_best_time_min = int(t_sec)
                            self.game_data.t_best_time_sec = int(t_msec)
                    self.game_data.t_best_time_hour = 0
                    self.game_data.t_best_time_min = 0
                    self.game_data.t_best_time_sec = 0
                if physics_smm.mPitMode == 2:
                    self.game_data.t_pit_limiter = 1
                else:
                    self.game_data.t_pit_limiter = 0
                flag = physics_smm.mHighestFlagColour
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
                    if flag == 2:
                        self.game_data.t_blue_flag = 1
                    else:
                        if flag == 4:
                            self.game_data.t_yellow_flag = 1
                        else:
                            if flag == 6:
                                self.game_data.t_black_flag = 1
                            else:
                                if flag == 3:
                                    self.game_data.t_white_flag = 1
                                else:
                                    if flag == 7:
                                        self.game_data.t_chequered_flag = 1
                                    else:
                                        if flag == 6:
                                            pass
                self.game_data.t_gas = int(physics_smm.mThrottle)
                self.game_data.t_brake = int(physics_smm.mBrake)
                self.game_data.t_clutch = int(physics_smm.mClutch)
                self.game_data.t_fl_tire_wear = int(physics_smm.mTyreWear[0]) - 70
                self.game_data.t_fr_tire_wear = int(physics_smm.mTyreWear[1]) - 70
                self.game_data.t_rl_tire_wear = int(physics_smm.mTyreWear[2]) - 70
                self.game_data.t_rr_tire_wear = int(physics_smm.mTyreWear[3]) - 70
                self.game_data.t_fl_tire_temp = int(physics_smm.mTyreTemp[0])
                self.game_data.t_fr_tire_temp = int(physics_smm.mTyreTemp[1])
                self.game_data.t_rl_tire_temp = int(physics_smm.mTyreTemp[2])
                self.game_data.t_rr_tire_temp = int(physics_smm.mTyreTemp[3])
                self.game_data.t_fl_brake_temp = int(physics_smm.mBrakeTempCelsius[0])
                self.game_data.t_fr_brake_temp = int(physics_smm.mBrakeTempCelsius[1])
                self.game_data.t_rl_brake_temp = int(physics_smm.mBrakeTempCelsius[2])
                self.game_data.t_rr_brake_temp = int(physics_smm.mBrakeTempCelsius[3])
                self.status = True
                return self.game_data
            except Exception as e:
                print('pacrs shared memory updata error ', e)
                self.status = False

        else:
            self.status = False
