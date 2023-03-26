from os.path import getmtime
from psutil import pid_exists
import socket
from struct import unpack
import time, threading
from f1_2020_telemetry.packets import *
from setting_define import *
import datetime

class pyDashF1_2020:

    def __init__(self, f1_2020_pid, dash, game_data, port, enable):
        self.f1_2020_pid = f1_2020_pid
        self.game_data = game_data[0]
        self.game_data_slow = game_data[1]
        self.port = int(port)
        self.enable = enable
        self.dash = dash
        self.status = False
        self.server_socket = None
        self.close = False
        try:
            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self.server_socket.bind(('', self.port))
            print(self.server_socket)
            self.server_socket.setblocking(0)
            self.server_socket.settimeout(1)
            if pid_exists(self.f1_2020_pid):
                self.status = True
                self.game_data.t_game_id = game_id['f12020']
        except Exception as e:
            print('pyDashF1-2020 error', e)
            try:
                self.server_socket.shutdown(0)
                self.server_socket.shutdown(1)
                self.server_socket.shutdown(2)
                self.server_socket.close()
            except:
                pass

        t1 = threading.Timer(0.033, self._update, None)
        t1.start()

    def isRun(self):
        return self.status

    def __del__(self):
        self.close = True
        try:
            self.server_socket.shutdown(0)
            self.server_socket.shutdown(1)
            self.server_socket.shutdown(2)
            self.server_socket.close()
        except:
            pass

    def update(self):
        pass

    def _update(self):
        if pid_exists(self.f1_2020_pid) and self.status == True and self.enable:
            try:
                while not self.close:
                    try:
                        data = self.server_socket.recv(2048)
                        packet = unpack_udp_packet(data)
                    except Exception as e:
                        print('f1 2020 _update')
                        packet = []

                    if isinstance(packet, PacketCarTelemetryData_V1):
                        data_packet = packet.carTelemetryData[packet.header.playerCarIndex]
                        self.game_data.t_rpm = data_packet.engineRPM
                        self.game_data.t_speed = int(data_packet.speed + 0.5)
                        self.game_data.t_fl_tire_temp = int(data_packet.tyresSurfaceTemperature[2])
                        self.game_data.t_fr_tire_temp = int(data_packet.tyresSurfaceTemperature[3])
                        self.game_data.t_rl_tire_temp = int(data_packet.tyresSurfaceTemperature[0])
                        self.game_data.t_rr_tire_temp = int(data_packet.tyresSurfaceTemperature[1])
                        self.game_data.t_fl_brake_temp = int(data_packet.brakesTemperature[2])
                        self.game_data.t_fr_brake_temp = int(data_packet.brakesTemperature[3])
                        self.game_data.t_rl_brake_temp = int(data_packet.brakesTemperature[0])
                        self.game_data.t_rr_brake_temp = int(data_packet.brakesTemperature[1])
                        gear = data_packet.gear
                        if gear == -1:
                            self.game_data.t_gear = 30
                        else:
                            if gear == 0:
                                self.game_data.t_gear = 31
                            else:
                                self.game_data.t_gear = int(gear)
                        self.game_data_slow.t_engine_temp = int(data_packet.engineTemperature)
                        self.game_data.t_gas = int(data_packet.throttle)
                        self.game_data.t_brake = int(data_packet.brake)
                        self.game_data.t_clutch = int(data_packet.clutch)
                        self.game_data.t_drs_actived = int(data_packet.drs)
                    if isinstance(packet, PacketCarSetupData_V1):
                        data_packet = packet.carSetups[packet.header.playerCarIndex]
                        self.game_data_slow.t_brake_bias = int(data_packet.brakeBias)
                        self.game_data_slow.t_diff_bias = int(data_packet.onThrottle)
                    if isinstance(packet, PacketMotionData_V1):
                        data_packet = packet.carMotionData[packet.header.playerCarIndex]
                        raw_x = data_packet.gForceLateral
                        if raw_x >= 5:
                            raw_x = 5
                        else:
                            if raw_x <= -5:
                                raw_x = -5
                            raw_y = data_packet.gForceLongitudinal
                            if raw_y >= 5:
                                raw_y = 5
                            elif raw_y <= -5:
                                raw_y = -5
                        self.game_data.x_gforce = int(raw_x * 30 + 125)
                        self.game_data.y_gforce = int(raw_y * 30 + 125)
                    if isinstance(packet, PacketCarStatusData_V1):
                        data_packet = packet.carStatusData[packet.header.playerCarIndex]
                        self.game_data_slow.t_max_rpm = int(data_packet.maxRPM)
                        self.game_data_slow.t_tc = int(data_packet.tractionControl)
                        self.game_data_slow.t_abs = int(data_packet.antiLockBrakes)
                        self.game_data_slow.t_fuel_mix = int(data_packet.fuelMix)
                        self.game_data.t_pit_limiter = int(data_packet.pitLimiterStatus)
                        self.game_data.t_fuel = int(data_packet.fuelInTank * 100)
                        self.game_data.t_total_fuel = int(data_packet.fuelCapacity * 100)
                        self.game_data.t_fuel_remaining_laps = int(data_packet.fuelRemainingLaps * 100)
                        self.game_data.t_drs_allowed = int(data_packet.drsAllowed)
                        self.game_data.t_drs_active_distance = int(data_packet.drsActivationDistance)
                        self.game_data_slow.t_ers_energy = int(data_packet.ersStoreEnergy / 4000000 * 100)
                        self.game_data_slow.t_ers_mode = int(data_packet.ersDeployMode)
                        self.game_data_slow.t_kers_energy = int(data_packet.ersHarvestedThisLapMGUK / 2000000 * 100)
                        self.game_data_slow.t_ers_deployed_lap = 100 - int(data_packet.ersDeployedThisLap / 4000000 * 100)
                        self.game_data_slow.t_fl_tire_wear = int(100 - data_packet.tyresWear[2]) - 70
                        self.game_data_slow.t_fr_tire_wear = int(100 - data_packet.tyresWear[3]) - 70
                        self.game_data_slow.t_rl_tire_wear = int(100 - data_packet.tyresWear[0]) - 70
                        self.game_data_slow.t_rr_tire_wear = int(100 - data_packet.tyresWear[1]) - 70
                        flag = data_packet.vehicleFiaFlags
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
                        if flag == 1:
                            self.game_data.t_green_flag = 1
                        else:
                            if flag == 2:
                                self.game_data.t_blue_flag = 1
                            else:
                                if flag == 3:
                                    self.game_data.t_yellow_flag = 1
                                elif flag == 4:
                                    self.game_data.t_red_flag = 1
                    if isinstance(packet, PacketSessionData_V1):
                        data_packet = packet
                        self.game_data_slow.t_lap_number = int(data_packet.totalLaps)
                    if isinstance(packet, PacketParticipantsData_V1):
                        self.game_data_slow.t_car_num = int(packet.numActiveCars)
                    if isinstance(packet, PacketLapData_V1):
                        data_packet = packet.lapData[packet.header.playerCarIndex]
                        self.game_data_slow.t_finish_lap = int(data_packet.currentLapNum)
                        self.game_data_slow.t_pos = int(data_packet.carPosition)
                        current_time = data_packet.currentLapTime
                        t_msec = int((current_time - int(current_time)) * 1000)
                        current_time = str(datetime.timedelta(seconds=(int(current_time))))
                        if ':' in current_time:
                            if '-' not in current_time:
                                t_hour, t_min, t_sec = current_time.split(':')
                                self.game_data.t_current_time_hour = int(t_min)
                                self.game_data.t_current_time_min = int(t_sec)
                                self.game_data.t_current_time_sec = int(t_msec)
                        else:
                            self.game_data.t_current_time_hour = 0
                            self.game_data.t_current_time_min = 0
                            self.game_data.t_current_time_sec = 0
                        last_time = data_packet.lastLapTime
                        t_msec = int((last_time - int(last_time)) * 1000)
                        last_time = str(datetime.timedelta(seconds=(int(last_time))))
                        if ':' in last_time:
                            if '-' not in last_time:
                                t_hour, t_min, t_sec = last_time.split(':')
                                self.game_data_slow.t_last_time_hour = int(t_min)
                                self.game_data_slow.t_last_time_min = int(t_sec)
                                self.game_data_slow.t_last_time_sec = int(t_msec)
                            else:
                                self.game_data_slow.t_last_time_hour = 0
                                self.game_data_slow.t_last_time_min = 0
                                self.game_data_slow.t_last_time_sec = 0
                        else:
                            best_time = data_packet.bestLapTime
                            t_msec = int((best_time - int(best_time)) * 1000)
                            best_time = str(datetime.timedelta(seconds=(int(best_time))))
                            if ':' in best_time:
                                if '-' not in best_time:
                                    t_hour, t_min, t_sec = best_time.split(':')
                                    self.game_data_slow.t_best_time_hour = int(t_min)
                                    self.game_data_slow.t_best_time_min = int(t_sec)
                                    self.game_data_slow.t_best_time_sec = int(t_msec)
                            self.game_data_slow.t_best_time_hour = 0
                            self.game_data_slow.t_best_time_min = 0
                            self.game_data_slow.t_best_time_sec = 0
                    self.dash.max_steering_angle = 360
                    if not pid_exists(self.f1_2020_pid):
                        self.status = False
                        try:
                            self.server_socket.shutdown(0)
                            self.server_socket.shutdown(1)
                            self.server_socket.shutdown(2)
                            self.server_socket.close()
                        except Exception as e:
                            print('close udp ', e)
                            break

            except Exception as e:
                print('f1 2020 dash updata error', e)
                self.status = False
                try:
                    self.server_socket.shutdown(0)
                    self.server_socket.shutdown(1)
                    self.server_socket.shutdown(2)
                    self.server_socket.close()
                except:
                    pass

        else:
            self.status = False
