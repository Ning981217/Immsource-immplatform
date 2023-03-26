from os.path import getmtime
from psutil import pid_exists
import socket
from struct import unpack
import time, threading
from setting_define import *
import datetime

class ForzaDataPacket:
    sled_format = '<iIfffffffffffffffffffffffffffffffffffffffffffffffffffiiiii'
    dash_format = '<iIfffffffffffffffffffffffffffffffffffffffffffffffffffiiiiifffffffffffffffffHBBBBBBbbb'
    sled_props = [
     'is_race_on', 'timestamp_ms',
     'engine_max_rpm', 'engine_idle_rpm', 'current_engine_rpm',
     'acceleration_x', 'acceleration_y', 'acceleration_z',
     'velocity_x', 'velocity_y', 'velocity_z',
     'angular_velocity_x', 'angular_velocity_y', 'angular_velocity_z',
     'yaw', 'pitch', 'roll',
     'norm_suspension_travel_FL', 'norm_suspension_travel_FR',
     'norm_suspension_travel_RL', 'norm_suspension_travel_RR',
     'tire_slip_ratio_FL', 'tire_slip_ratio_FR',
     'tire_slip_ratio_RL', 'tire_slip_ratio_RR',
     'wheel_rotation_speed_FL', 'wheel_rotation_speed_FR',
     'wheel_rotation_speed_RL', 'wheel_rotation_speed_RR',
     'wheel_on_rumble_strip_FL', 'wheel_on_rumble_strip_FR',
     'wheel_on_rumble_strip_RL', 'wheel_on_rumble_strip_RR',
     'wheel_in_puddle_FL', 'wheel_in_puddle_FR',
     'wheel_in_puddle_RL', 'wheel_in_puddle_RR',
     'surface_rumble_FL', 'surface_rumble_FR',
     'surface_rumble_RL', 'surface_rumble_RR',
     'tire_slip_angle_FL', 'tire_slip_angle_FR',
     'tire_slip_angle_RL', 'tire_slip_angle_RR',
     'tire_combined_slip_FL', 'tire_combined_slip_FR',
     'tire_combined_slip_RL', 'tire_combined_slip_RR',
     'suspension_travel_meters_FL', 'suspension_travel_meters_FR',
     'suspension_travel_meters_RL', 'suspension_travel_meters_RR',
     'car_ordinal', 'car_class', 'car_performance_index',
     'drivetrain_type', 'num_cylinders']
    dash_props = [
     'position_x', 'position_y', 'position_z',
     'speed', 'power', 'torque',
     'tire_temp_FL', 'tire_temp_FR',
     'tire_temp_RL', 'tire_temp_RR',
     'boost', 'fuel', 'dist_traveled',
     'best_lap_time', 'last_lap_time',
     'cur_lap_time', 'cur_race_time',
     'lap_no', 'race_pos',
     'accel', 'brake', 'clutch', 'handbrake',
     'gear', 'steer',
     'norm_driving_line', 'norm_ai_brake_diff']

    def __init__(self, data, packet_format='dash'):
        self.packet_format = packet_format
        if packet_format == 'sled':
            for prop_name, prop_value in zip(self.sled_props, unpack(self.sled_format, data)):
                setattr(self, prop_name, prop_value)

        else:
            if packet_format == 'fh4':
                patched_data = data[:232] + data[244:323]
                for prop_name, prop_value in zip(self.sled_props + self.dash_props, unpack(self.dash_format, patched_data)):
                    setattr(self, prop_name, prop_value)

            else:
                for prop_name, prop_value in zip(self.sled_props + self.dash_props, unpack(self.dash_format, data)):
                    setattr(self, prop_name, prop_value)

    @classmethod
    def get_props(cls, packet_format='dash'):
        """
        Return the list of properties in the data packet, in order.

        :param packet_format: which packet format to get properties for,
                              one of either 'sled' or 'dash'
        :type packet_format: str
        """
        if packet_format == 'sled':
            return cls.sled_props
        else:
            return cls.sled_props + cls.dash_props

    def to_list(self, attributes):
        """
        Return the values of this data packet, in order. If a list of 
        attributes are provided, only return those.

        :param attributes: the attributes to return
        :type attributes: list
        """
        if attributes:
            return [getattr(self, a) for a in attributes]
        else:
            if self.packet_format == 'sled':
                return [getattr(self, prop_name) for prop_name in self.sled_props]
            return [getattr(self, prop_name) for prop_name in self.sled_props + self.dash_props]


class pyDashFH4:

    def __init__(self, fh4_pid, dash, game_data, port, enable):
        self.fh4_pid = fh4_pid
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
            self.server_socket.setblocking(0)
            self.server_socket.settimeout(1)
            if pid_exists(self.fh4_pid):
                self.status = True
                self.game_data.t_game_id = game_id['fh4']
        except Exception as e:
            print('pyDashFH4 error', e)
            try:
                self.server_socket.shutdown(0)
                self.server_socket.shutdown(1)
                self.server_socket.shutdown(2)
                self.server_socket.close()
            except Exception as e:
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
        except Exception as e:
            pass

    def update(self):
        pass

    def _update(self):
        if pid_exists(self.fh4_pid) and self.enable:
            try:
                while not self.close:
                    time.sleep(0.01)
                    try:
                        data = self.server_socket.recv(512)
                        fdp = ForzaDataPacket(data, 'fh4')
                        self.game_data.t_rpm = int(fdp.current_engine_rpm)
                        self.game_data_slow.t_max_rpm = int(fdp.engine_max_rpm)
                        self.game_data.t_speed = int(fdp.speed + 0.5)
                        self.status = True
                        self.dash.max_steering_angle = 900
                        if not pid_exists(self.fh4_pid):
                            self.status = False
                            try:
                                self.server_socket.shutdown(0)
                                self.server_socket.shutdown(1)
                                self.server_socket.shutdown(2)
                                self.server_socket.close()
                                break
                            except:
                                break

                    except Exception as e:
                        print('fh4 _update')
                        fdp = []

            except Exception as e:
                print('fh4 dash updata error', e)
                self.status = False

        else:
            self.server_socket.shutdown(0)
            self.server_socket.shutdown(1)
            self.server_socket.shutdown(2)
            self.server_socket.close()
            self.status = False
