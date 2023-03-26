from os.path import getmtime
from psutil import pid_exists
import socket, struct, time, threading
from enum import Enum
import os
from setting_define import *

class Fields(Enum):
    run_time = 0
    lap_time = 1
    distance = 2
    progress = 3
    pos_x = 4
    pos_y = 5
    pos_z = 6
    speed_ms = 7
    vel_x = 8
    vel_y = 9
    vel_z = 10
    roll_x = 11
    roll_y = 12
    roll_z = 13
    pitch_x = 14
    pitch_y = 15
    pitch_z = 16
    susp_rl = 17
    susp_rr = 18
    susp_fl = 19
    susp_fr = 20
    susp_vel_rl = 21
    susp_vel_rr = 22
    susp_vel_fl = 23
    susp_vel_fr = 24
    wsp_rl = 25
    wsp_rr = 26
    wsp_fl = 27
    wsp_fr = 28
    throttle = 29
    steering = 30
    brakes = 31
    clutch = 32
    gear = 33
    g_force_lat = 34
    g_force_lon = 35
    current_lap = 36
    rpm = 37
    sli_pro_support = 38
    car_pos = 39
    kers_level = 40
    kers_max_level = 41
    drs = 42
    traction_control = 43
    anti_lock_brakes = 44
    fuel_in_tank = 45
    fuel_capacity = 46
    in_pit = 47
    sector = 48
    sector_1_time = 49
    sector_2_time = 50
    brakes_temp_rl = 51
    brakes_temp_rr = 52
    brakes_temp_fl = 53
    brakes_temp_fr = 54
    tyre_pressure_rl = 55
    tyre_pressure_rr = 56
    tyre_pressure_fl = 57
    tyre_pressure_fr = 58
    laps_completed = 59
    total_laps = 60
    track_length = 61
    last_lap_time = 62
    max_rpm = 63
    idle_rpm = 64
    max_gears = 65


num_fields = 66

def bit_stream_to_float32(data, pos):
    try:
        value = struct.unpack('f', data[pos:pos + 4])[0]
    except struct.error as _:
        value = 0
    except Exception as e:
        value = 0
        print('Failed to get data item at pos {}. Make sure to set extradata=3 in the hardware settings.'.format(pos))

    return value


class pyDashDRR2:

    def __init__(self, game_name, drr2_pid, dash, game_data, port, enable, name):
        self.drr2_pid = drr2_pid
        self.game_data = game_data[0]
        self.game_data_slow = game_data[1]
        self.port = int(port)
        self.game_name = game_name
        self.enable = enable
        self.dash = dash
        self.status = False
        self.server_socket = None
        self.close = False
        try:
            game_udp_setting_file = os.path.expanduser('~') + '\\Documents\\My Games\\' + game_name + '\\hardwaresettings\\hardware_settings_config.xml'
            if os.path.exists(game_udp_setting_file):
                with open(game_udp_setting_file, 'r') as (lines):
                    lines = list(lines)
                    udp_enable = False
                    for line in lines:
                        if 'udp enabled="true"' in line:
                            udp_enable = True
                            break

                    if udp_enable == False:
                        for line_num, line in enumerate(lines):
                            if 'udp enabled' in line:
                                lines[line_num] = '\t\t<udp enabled="true" extradata="3" ip="' + '127.0.0.1' + '" port="' + str(self.port) + '" delay="1" />' + '\n'
                                break

                if udp_enable == False:
                    with open(game_udp_setting_file, 'w+') as (f):
                        for line in lines:
                            f.write(line)

            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self.server_socket.bind(('', self.port))
            self.server_socket.setblocking(0)
            self.server_socket.settimeout(1)
            if pid_exists(self.drr2_pid):
                self.status = True
                self.game_data.t_game_id = game_id[name]
        except Exception as e:
            print('pyDashDRR2 error', e)
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
        if pid_exists(self.drr2_pid) and self.status == True and self.enable:
            try:
                while not self.close:
                    time.sleep(0.01)
                    try:
                        data = self.server_socket.recv(1024)
                    except Exception as e:
                        print('drr4 _update')
                        data = None

                    if data != None:
                        run_time = bit_stream_to_float32(data, 0)
                        lap_time = bit_stream_to_float32(data, 4)
                        distance = max(bit_stream_to_float32(data, 8), 0)
                        progress = bit_stream_to_float32(data, 12)
                        pos_x = bit_stream_to_float32(data, 16)
                        pos_y = bit_stream_to_float32(data, 20)
                        pos_z = bit_stream_to_float32(data, 24)
                        speed_ms = bit_stream_to_float32(data, 28)
                        vel_x = bit_stream_to_float32(data, 32)
                        vel_y = bit_stream_to_float32(data, 36)
                        vel_z = bit_stream_to_float32(data, 40)
                        roll_x = bit_stream_to_float32(data, 44)
                        roll_y = bit_stream_to_float32(data, 48)
                        roll_z = bit_stream_to_float32(data, 52)
                        pitch_x = bit_stream_to_float32(data, 56)
                        pitch_y = bit_stream_to_float32(data, 60)
                        pitch_z = bit_stream_to_float32(data, 64)
                        susp_rl = bit_stream_to_float32(data, 68)
                        susp_rr = bit_stream_to_float32(data, 72)
                        susp_fl = bit_stream_to_float32(data, 76)
                        susp_fr = bit_stream_to_float32(data, 80)
                        susp_vel_rl = bit_stream_to_float32(data, 84)
                        susp_vel_rr = bit_stream_to_float32(data, 88)
                        susp_vel_fl = bit_stream_to_float32(data, 92)
                        susp_vel_fr = bit_stream_to_float32(data, 96)
                        wsp_rl = bit_stream_to_float32(data, 100)
                        wsp_rr = bit_stream_to_float32(data, 104)
                        wsp_fl = bit_stream_to_float32(data, 108)
                        wsp_fr = bit_stream_to_float32(data, 112)
                        throttle = bit_stream_to_float32(data, 116)
                        steering = bit_stream_to_float32(data, 120)
                        brakes = bit_stream_to_float32(data, 124)
                        clutch = bit_stream_to_float32(data, 128)
                        gear = bit_stream_to_float32(data, 132)
                        g_force_lat = bit_stream_to_float32(data, 136)
                        g_force_lon = bit_stream_to_float32(data, 140)
                        current_lap = bit_stream_to_float32(data, 144)
                        rpm = bit_stream_to_float32(data, 148)
                        sli_pro_support = bit_stream_to_float32(data, 152)
                        car_pos = bit_stream_to_float32(data, 156)
                        kers_level = bit_stream_to_float32(data, 160)
                        kers_max_level = bit_stream_to_float32(data, 164)
                        drs = bit_stream_to_float32(data, 168)
                        traction_control = bit_stream_to_float32(data, 172)
                        anti_lock_brakes = bit_stream_to_float32(data, 176)
                        fuel_in_tank = bit_stream_to_float32(data, 180)
                        fuel_capacity = bit_stream_to_float32(data, 184)
                        in_pit = bit_stream_to_float32(data, 188)
                        sector = bit_stream_to_float32(data, 192)
                        sector_1_time = bit_stream_to_float32(data, 196)
                        sector_2_time = bit_stream_to_float32(data, 200)
                        brakes_temp_rl = bit_stream_to_float32(data, 204)
                        brakes_temp_rr = bit_stream_to_float32(data, 208)
                        brakes_temp_fl = bit_stream_to_float32(data, 212)
                        brakes_temp_fr = bit_stream_to_float32(data, 216)
                        tyre_pressure_rl = bit_stream_to_float32(data, 220)
                        tyre_pressure_rr = bit_stream_to_float32(data, 224)
                        tyre_pressure_fl = bit_stream_to_float32(data, 228)
                        tyre_pressure_fr = bit_stream_to_float32(data, 232)
                        laps_completed = bit_stream_to_float32(data, 236)
                        total_laps = bit_stream_to_float32(data, 240)
                        track_length = bit_stream_to_float32(data, 244)
                        last_lap_time = bit_stream_to_float32(data, 248)
                        max_rpm = bit_stream_to_float32(data, 252)
                        idle_rpm = bit_stream_to_float32(data, 256)
                        max_gears = bit_stream_to_float32(data, 260)
                        self.game_data.t_rpm = int(rpm * 10)
                        self.game_data_slow.t_max_rpm = int(max_rpm * 10)
                        self.game_data.t_speed = int(speed_ms * 3.6 + 0.5)
                        self.game_data.t_gas = int(throttle)
                        self.game_data.t_brake = int(brakes)
                        self.game_data.t_clutch = int(clutch)
                        if gear == 0:
                            self.game_data.t_gear = 30
                        else:
                            if gear == 1:
                                self.game_data.t_gear = 31
                            else:
                                self.game_data.t_gear = int(gear - 1)
                        self.game_data.t_fl_brake_temp = int(brakes_temp_fl)
                        self.game_data.t_fr_brake_temp = int(brakes_temp_fr)
                        self.game_data.t_rl_brake_temp = int(brakes_temp_rl)
                        self.game_data.t_rr_brake_temp = int(brakes_temp_rr)
                    self.dash.max_steering_angle = 540
                    if not pid_exists(self.drr2_pid):
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
                print('drr2 dash updata error', e)
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
