"""
pyR3E.py - Defines the shared memory map structures for RaceRoom Racing Experience 
        as outlined by Sector3 Studios (https://github.com/sector3studios/r3e-api)
by Dan Allongo (daniel.s.allongo@gmail.com)

Release History:
2016-05-06: Split off into separate file
2016-05-04: Updated per https://github.com/mrbelowski/CrewChiefV4/blob/master/CrewChiefV4/R3E/RaceRoomData.cs
2016-05-04: Initial release
"""
from ctypes import *

class r3e_struct(Structure):
    _pack_ = 1


class r3e_session_enum(r3e_struct):
    _fields_ = [
     (
      'R3E_SESSION_UNAVAILABLE', c_int),
     (
      'R3E_SESSION_PRACTICE', c_int),
     (
      'R3E_SESSION_QUALIFY', c_int),
     (
      'R3E_SESSION_RACE', c_int)]


r3e_session = r3e_session_enum(-1, 0, 1, 2)

class r3e_session_length_enum(r3e_struct):
    _fields_ = [
     (
      'R3E_SESSION_LENGTH_UNAVAILABLE', c_int),
     (
      'R3E_SESSION_LENGTH_TIME_BASED', c_int),
     (
      'R3E_SESSION_LENGTH_LAP_BASED', c_int),
     (
      'R3E_SESSION_LENGTH_TIME_AND_LAP_BASED', c_int)]


r3e_session_length = r3e_session_length_enum(-1, 0, 1, 2)

class r3e_session_phase_enum(r3e_struct):
    _fields_ = [
     (
      'R3E_SESSION_PHASE_UNAVAILABLE', c_int),
     (
      'R3E_SESSION_PHASE_GARAGE', c_int),
     (
      'R3E_SESSION_PHASE_GRIDWALK', c_int),
     (
      'R3E_SESSION_PHASE_FORMATION', c_int),
     (
      'R3E_SESSION_PHASE_COUNTDOWN', c_int),
     (
      'R3E_SESSION_PHASE_GREEN', c_int),
     (
      'R3E_SESSION_PHASE_CHECKERED', c_int),
     (
      'R3E_SESSION_PHASE_TERMINATED', c_int)]


r3e_session_phase = r3e_session_phase_enum(-1, 0, 2, 3, 4, 5, 6, 7)

class r3e_control_enum(r3e_struct):
    _fields_ = [
     (
      'R3E_CONTROL_UNAVAILABLE', c_int),
     (
      'R3E_CONTROL_PLAYER', c_int),
     (
      'R3E_CONTROL_AI', c_int),
     (
      'R3E_CONTROL_REMOTE', c_int),
     (
      'R3E_CONTROL_REPLAY', c_int)]


r3e_control = r3e_control_enum(-1, 0, 1, 2, 3)

class r3e_pit_window_enum(r3e_struct):
    _fields_ = [
     (
      'R3E_PIT_WINDOW_UNAVAILABLE', c_int),
     (
      'R3E_PIT_WINDOW_DISABLED', c_int),
     (
      'R3E_PIT_WINDOW_CLOSED', c_int),
     (
      'R3E_PIT_WINDOW_OPEN', c_int),
     (
      'R3E_PIT_WINDOW_STOPPED', c_int),
     (
      'R3E_PIT_WINDOW_COMPLETED', c_int)]


r3e_pit_window = r3e_pit_window_enum(-1, 0, 1, 2, 3, 4)

class r3e_tire_type_enum(r3e_struct):
    _fields_ = [
     (
      'R3E_TIRE_TYPE_UNAVAILABLE', c_int),
     (
      'R3E_TIRE_TYPE_OPTION', c_int),
     (
      'R3E_TIRE_TYPE_PRIME', c_int)]


r3e_tire_type = r3e_tire_type_enum(-1, 0, 1)

class r3e_pitstop_status_enum(r3e_struct):
    _fields_ = [
     (
      'R3E_PITSTOP_STATUS_UNAVAILABLE', c_int),
     (
      'R3E_PITSTOP_STATUS_UNSERVED', c_int),
     (
      'R3E_PITSTOP_STATUS_SERVED', c_int)]


r3e_pitstop_status = r3e_pitstop_status_enum(-1, 0, 1)

class r3e_finish_status_enum(r3e_struct):
    _fields_ = [
     (
      'R3E_FINISH_STATUS_UNAVAILABLE', c_int),
     (
      'R3E_FINISH_STATUS_NONE', c_int),
     (
      'R3E_FINISH_STATUS_FINISHED', c_int),
     (
      'R3E_FINISH_STATUS_DNF', c_int),
     (
      'R3E_FINISH_STATUS_DNQ', c_int),
     (
      'R3E_FINISH_STATUS_DNS', c_int),
     (
      'R3E_FINISH_STATUS_DQ', c_int)]


r3e_finish_status = r3e_finish_status_enum(-1, 0, 1, 2, 3, 4, 5)

class r3e_vec3_f32(r3e_struct):
    _fields_ = [
     (
      'x', c_float),
     (
      'y', c_float),
     (
      'z', c_float)]


class r3e_vec3_f64(r3e_struct):
    _fields_ = [
     (
      'x', c_double),
     (
      'y', c_double),
     (
      'z', c_double)]


class r3e_ori_f32(r3e_struct):
    _fields_ = [
     (
      'pitch', c_float),
     (
      'yaw', c_float),
     (
      'roll', c_float)]


class r3e_aid_settings(r3e_struct):
    _fields_ = [
     (
      'abs', c_int),
     (
      'tc', c_int),
     (
      'esp', c_int),
     (
      'countersteer', c_int),
     (
      'cornering', c_int)]


class r3e_drs(r3e_struct):
    _fields_ = [
     (
      'equipped', c_int),
     (
      'available', c_int),
     (
      'numActivationsLeft', c_int),
     (
      'engaged', c_int)]


class r3e_tire_temps(r3e_struct):
    _fields_ = [
     (
      'frontleft_left', c_float),
     (
      'frontleft_center', c_float),
     (
      'frontleft_right', c_float),
     (
      'frontright_left', c_float),
     (
      'frontright_center', c_float),
     (
      'frontright_right', c_float),
     (
      'rearleft_left', c_float),
     (
      'rearleft_center', c_float),
     (
      'rearleft_right', c_float),
     (
      'rearright_left', c_float),
     (
      'rearright_center', c_float),
     (
      'rearright_right', c_float)]


class r3e_tire_temp(r3e_struct):
    _fields_ = [
     (
      'current_temp', c_float * 4),
     (
      'optimal_temp', c_float),
     (
      'cold_temp', c_float),
     (
      'hot_temp', c_float)]


class r3e_playerdata(r3e_struct):
    _fields_ = [
     (
      'game_simulation_ticks', c_int),
     (
      'game_simulation_time', c_double),
     (
      'position', r3e_vec3_f64),
     (
      'velocity', r3e_vec3_f64),
     (
      'local_velocity', r3e_vec3_f64),
     (
      'acceleration', r3e_vec3_f64),
     (
      'local_acceleration', r3e_vec3_f64),
     (
      'orientation', r3e_vec3_f64),
     (
      'rotation', r3e_vec3_f64),
     (
      'angular_acceleration', r3e_vec3_f64),
     (
      'angular_velocity', r3e_vec3_f64),
     (
      'local_angular_velocity', r3e_vec3_f64),
     (
      'local_g_force', r3e_vec3_f64),
     (
      'steering_force', c_double),
     (
      'steering_force_percentage', c_double),
     (
      'engine_torque', c_double),
     (
      'current_downforce', c_double),
     (
      'voltage', c_double),
     (
      'ers_level', c_double),
     (
      'power_mgu_h', c_double),
     (
      'power_mgu_k', c_double),
     (
      'torque_mgu_k', c_double),
     (
      'suspension_deflection', c_double * 4),
     (
      'suspension_velocity', c_double * 4),
     (
      'camber', c_double * 4),
     (
      'ride_height', c_double * 4),
     (
      'front_wing_height', c_double),
     (
      'front_roll_angle', c_double),
     (
      'rear_roll_angle', c_double),
     (
      'third_spring_suspension_deflection_front', c_double),
     (
      'third_spring_suspension_velocity_front', c_double),
     (
      'third_spring_suspension_deflection_rear', c_double),
     (
      'third_spring_suspension_velocity_rear', c_double),
     (
      'unused1', c_double)]


class r3e_flags(r3e_struct):
    _fields_ = [
     (
      'yellow', c_int),
     (
      'yellowCausedIt', c_int),
     (
      'yellowOvertake', c_int),
     (
      'yellowPositionsGained', c_int),
     (
      'sector_yellow', c_int * 3),
     (
      'closest_yellow_distance_into_track', c_float),
     (
      'blue', c_int),
     (
      'black', c_int),
     (
      'green', c_int),
     (
      'checkered', c_int),
     (
      'white', c_int),
     (
      'black_and_white', c_int)]


class r3e_car_damage(r3e_struct):
    _fields_ = [
     (
      'engine', c_float),
     (
      'transmission', c_float),
     (
      'aerodynamics', c_float),
     (
      'suspension', c_float),
     (
      'unused1', c_float),
     (
      'unused2', c_float)]


class r3e_tire_pressure(r3e_struct):
    _fields_ = [
     (
      'front_left', c_float),
     (
      'front_right', c_float),
     (
      'rear_left', c_float),
     (
      'rear_right', c_float)]


class r3e_brake_temps(r3e_struct):
    _fields_ = [
     (
      'front_left', c_float),
     (
      'front_right', c_float),
     (
      'rear_left', c_float),
     (
      'rear_right', c_float)]


class r3e_brake_temp(r3e_struct):
    _fields_ = [
     (
      'current_temp', c_float),
     (
      'optimal_temp', c_float),
     (
      'cold_temp', c_float),
     (
      'hot_temp', c_float)]


class r3e_cut_track_penalties(r3e_struct):
    _fields_ = [
     (
      'drive_through', c_int),
     (
      'stop_and_go', c_int),
     (
      'pit_stop', c_int),
     (
      'time_deduction', c_int),
     (
      'slow_down', c_int)]


class r3e_tyre_dirt(r3e_struct):
    _fields_ = [
     (
      'front_left', c_float),
     (
      'front_right', c_float),
     (
      'rear_left', c_float),
     (
      'rear_right', c_float)]


class r3e_wheel_speed(r3e_struct):
    _fields_ = [
     (
      'front_left', c_float),
     (
      'front_right', c_float),
     (
      'rear_left', c_float),
     (
      'rear_right', c_float)]


class r3e_track_info(r3e_struct):
    _fields_ = [
     (
      'track_id', c_int),
     (
      'layout_id', c_int),
     (
      'length', c_float)]


class r3e_push_to_pass(r3e_struct):
    _fields_ = [
     (
      'available', c_int),
     (
      'engaged', c_int),
     (
      'amount_left', c_int),
     (
      'engaged_time_left', c_float),
     (
      'wait_time_left', c_float)]


class r3e_driver_info(r3e_struct):
    _fields_ = [
     (
      'name', c_char * 64),
     (
      'car_number', c_int),
     (
      'class_id', c_int),
     (
      'model_id', c_int),
     (
      'team_id', c_int),
     (
      'livery_id', c_int),
     (
      'manufacturer_id', c_int),
     (
      'user_id', c_int),
     (
      'slot_id', c_int),
     (
      'class_performance_index', c_int),
     (
      'engine_type', c_int),
     (
      'unused1', c_int),
     (
      'unused2', c_int)]


class r3e_driver_data_1(r3e_struct):
    _fields_ = [
     (
      'driver_info', r3e_driver_info),
     (
      'finish_status', c_int),
     (
      'place', c_int),
     (
      'place_class', c_int),
     (
      'lap_distance', c_float),
     (
      'position', r3e_vec3_f32),
     (
      'track_sector', c_int),
     (
      'completed_laps', c_int),
     (
      'current_lap_valid', c_int),
     (
      'lap_time_current_self', c_float),
     (
      'sector_time_current_self', c_float * 3),
     (
      'sector_time_previous_self', c_float * 3),
     (
      'sector_time_best_self', c_float * 3),
     (
      'time_delta_front', c_float),
     (
      'time_delta_behind', c_float),
     (
      'pitstop_status', c_int),
     (
      'in_pitlane', c_int),
     (
      'num_pitstops', c_int),
     (
      'penalties', r3e_cut_track_penalties),
     (
      'car_speed', c_float),
     (
      'tire_type_front', c_int),
     (
      'tire_type_rear', c_int),
     (
      'tire_subtype_front', c_int),
     (
      'tire_subtype_rear', c_int),
     (
      'base_penalty_weight', c_float),
     (
      'aid_penalty_weight', c_float),
     (
      'drs_state', c_int),
     (
      'ptp_state', c_int),
     (
      'penaltyType', c_int),
     (
      'penaltyReason', c_int),
     (
      'unused1', c_int),
     (
      'unused2', c_int),
     (
      'unused3', c_float),
     (
      'unused4;', c_float)]


class r3e_sectorStarts(r3e_struct):
    _fields_ = [
     (
      'sector1', c_float),
     (
      'sector2', c_float),
     (
      'sector3', c_float)]


class r3e_shared(r3e_struct):
    _fields_ = [
     (
      'version_major', c_int),
     (
      'version_minor', c_int),
     (
      'all_drivers_offset', c_int),
     (
      'driver_data_size', c_int),
     (
      'game_paused', c_int),
     (
      'game_in_menus', c_int),
     (
      'game_in_replay', c_int),
     (
      'game_using_vr', c_int),
     (
      'game_unused1', c_int),
     (
      'player', r3e_playerdata),
     (
      'track_name', c_char * 64),
     (
      'layout_name', c_char * 64),
     (
      'track_id', c_int),
     (
      'layout_id', c_int),
     (
      'layout_length', c_float),
     (
      'sector_start_factors', r3e_sectorStarts),
     (
      'race_session_laps', c_int * 3),
     (
      'race_session_minutes', c_int * 3),
     (
      'event_index', c_int),
     (
      'session_type', c_int),
     (
      'session_iteration', c_int),
     (
      'session_length_format', c_int),
     (
      'session_pit_speed_limit', c_float),
     (
      'session_phase', c_int),
     (
      'start_lights', c_int),
     (
      'tire_wear_active', c_int),
     (
      'fuel_use_active', c_int),
     (
      'number_of_laps', c_int),
     (
      'session_time_duration', c_float),
     (
      'session_time_remaining', c_float),
     (
      'max_incident_points', c_int),
     (
      'event_unused2', c_float),
     (
      'pit_window_status', c_int),
     (
      'pit_window_start', c_int),
     (
      'pit_window_end', c_int),
     (
      'in_pitlane', c_int),
     (
      'pit_menu_selection', c_int),
     (
      'pit_menu_state', c_int * 11),
     (
      'pit_state', c_int),
     (
      'pit_total_duration', c_float),
     (
      'pit_elapsed_time', c_float),
     (
      'pit_action', c_int),
     (
      'num_pitstops', c_int),
     (
      'pit_min_duration_total', c_float),
     (
      'pit_min_duration_left', c_float),
     (
      'flags', r3e_flags),
     (
      'position', c_int),
     (
      'position_class', c_int),
     (
      'finish_status', c_int),
     (
      'cut_track_warnings', c_int),
     (
      'penalties', r3e_cut_track_penalties),
     (
      'num_penalties', c_int),
     (
      'completed_laps', c_int),
     (
      'current_lap_valid', c_int),
     (
      'track_sector', c_int),
     (
      'lap_distance', c_float),
     (
      'lap_distance_fraction', c_float),
     (
      'lap_time_best_leader', c_float),
     (
      'lap_time_best_leader_class', c_float),
     (
      'session_best_lap_sector_times', c_float * 3),
     (
      'lap_time_best_self', c_float),
     (
      'sector_time_best_self', c_float * 3),
     (
      'lap_time_previous_self', c_float),
     (
      'sector_time_previous_self', c_float * 3),
     (
      'lap_time_current_self', c_float),
     (
      'sector_time_current_self', c_float * 3),
     (
      'lap_time_delta_leader', c_float),
     (
      'lap_time_delta_leader_class', c_float),
     (
      'time_delta_front', c_float),
     (
      'time_delta_behind', c_float),
     (
      'time_delta_best_self', c_float),
     (
      'best_individual_sector_time_self', c_float * 3),
     (
      'best_individual_sector_time_leader', c_float * 3),
     (
      'best_individual_sector_time_leader_class', c_float * 3),
     (
      'incident_points', c_int),
     (
      'score_unused1', c_int),
     (
      'score_unused3', c_float),
     (
      'score_unused4', c_float),
     (
      'vehicle_info', r3e_driver_info),
     (
      'player_name', c_char * 64),
     (
      'control_type', c_int),
     (
      'car_speed', c_float),
     (
      'engine_rps', c_float),
     (
      'max_engine_rps', c_float),
     (
      'upshift_rps', c_float),
     (
      'gear', c_int),
     (
      'num_gears', c_int),
     (
      'car_cg_location', r3e_vec3_f32),
     (
      'car_orientation', r3e_ori_f32),
     (
      'local_acceleration', r3e_vec3_f32),
     (
      'total_mass', c_float),
     (
      'fuel_left', c_float),
     (
      'fuel_capacity', c_float),
     (
      'fuel_per_lap', c_float),
     (
      'engine_water_temp', c_float),
     (
      'engine_oil_temp', c_float),
     (
      'fuel_pressure', c_float),
     (
      'engine_oil_pressure', c_float),
     (
      'turbo_pressure', c_float),
     (
      'throttle', c_float),
     (
      'throttle_raw', c_float),
     (
      'brake', c_float),
     (
      'brake_raw', c_float),
     (
      'clutch', c_float),
     (
      'clutch_raw', c_float),
     (
      'steer_input_raw', c_float),
     (
      'steer_lock_degrees', c_int),
     (
      'steer_wheel_range_degrees', c_int),
     (
      'aid_settings', r3e_aid_settings),
     (
      'drs', r3e_drs),
     (
      'pit_limiter', c_int),
     (
      'push_to_pass', r3e_push_to_pass),
     (
      'brake_bias', c_float),
     (
      'drs_numActivationsTotal', c_int),
     (
      'ptp_numActivationsTotal', c_int),
     (
      'vehicle_unused1', c_float),
     (
      'vehicle_unused2', c_float),
     (
      'vehicle_unused3', r3e_ori_f32),
     (
      'tire_type', c_int),
     (
      'tire_rps', c_float * 4),
     (
      'tire_speed', c_float * 4),
     (
      'tire_grip', c_float * 4),
     (
      'tire_wear', c_float * 4),
     (
      'tire_flatspot', c_int * 4),
     (
      'tire_pressure', c_float * 4),
     (
      'tire_dirt', c_float * 4),
     (
      'tire_temp', r3e_tire_temp * 4),
     (
      'tire_type_front', c_int),
     (
      'tire_type_rear', c_int),
     (
      'tire_subtype_front', c_int),
     (
      'tire_subtype_rear', c_int),
     (
      'brake_temp', r3e_brake_temp * 4),
     (
      'brake_pressure', c_float * 4),
     (
      'traction_control_setting', c_int),
     (
      'engine_map_setting', c_int),
     (
      'engine_brake_setting', c_int),
     (
      'tire_unused1', c_float),
     (
      'tire_unused2', c_float * 4),
     (
      'tire_load', c_float * 4),
     (
      'car_damage', r3e_car_damage),
     (
      'num_cars', c_int),
     (
      'all_drivers_data_1', r3e_driver_data_1 * 128)]


def rps_to_rpm(r):
    return r * 9.549296596


def mps_to_mph(m):
    return m * 2.23694


def mps_to_kph(m):
    return m * 3.6


def kpa_to_psi(k):
    return k * 0.145038


def c_to_f(c):
    return c * 1.8 + 32


def l_to_g(l):
    return l * 0.264172


r3e_smm_tag = '$R3E'
r3e_smm_handle = None
