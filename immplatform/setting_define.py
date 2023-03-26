from ctypes import c_uint16, c_uint8, c_int16, c_uint32, string_at, addressof, sizeof, Structure, BigEndianStructure
import ctypes
IMMPLATFROM_VER = '0.17'
IMMS_BASE_VID = 294
IMMS_BASE_PID = 49153
IMMS_BASE_F_VID = 4660
IMMS_BASE_F_PID = 48813
IMMS_BASE_ET3_VID = 294
IMMS_BASE_ET3_PID = 49157
IMMS_BASE_X_VID = 1133
IMMS_BASE_X_PID = 49743
IMMS_BASE_UPDATA_VID = 294
IMMS_BASE_UPDATA_PID = 41217
IMMS_BASE_ET3_UPDATA_VID = 294
IMMS_BASE_ET3_UPDATA_PID = 41221
IMMS_GFORCE_VID = 567
IMMS_GFORCE_PID = 61441
IMMS_BASE_PS4_VID = 1133
IMMS_BASE_PS4_PID = 49760
IMMS_HUB_VID = 294
IMMS_HUB_PID = 45057
IMMS_HUB_UPDATA_VID = 294
IMMS_HUB_UPDATA_PID = 45313
CONNECT_STATUS_RUNNING = 1
CONNECT_STATUS_WIRELESS_RUNNING = 3
CONNECT_STATUS_FAULT = 0
CONNECT_STATUS_OTA = 2
CONNECT_STATUS_PS4 = 4
MODE_UNKNOW = 0
MODE_NORMAL = 1
MODE_HIGHTORQUE = 2
MODE_ZEROTORQUE = 3
SETTING_MODE = 0
SETTING_ZORE_CENTER = 1
SETTING_SET_RANGE = 2
SETTING_RANGE_AUTO = 3
SETTING_DEAD_BAND = 4
SETTING_ENDSTOP_STRENGTH = 5
SETTING_ENDSTOP_RANGE = 6
SETTING_ENDSTOP_DAMPING_STRENGTH = 7
SETTING_Encrypted = 8
SETTING_FFB_STRENGTH = 20
SETTING_FFB_RESPONSE = 21
SETTING_FFB_DETAIL_ENHANCER = 22
SETTING_FFB_FILTER = 23
SETTING_FFB_LINEARITY = 24
SETTING_AFFECTDEADBAND = 25
SETTING_MECH_SPRING_STRENGTH = 26
SETTING_MECH_FRICTION_STRENGTH = 27
SETTING_MECH_DAMPING_STRENGTH = 28
SETTING_MECH_INERTIA_STRENGTH = 29
SETTING_FFB_CONSTANT_STRENGTH = 31
SETTING_FFB_FRICTION_STRENGTH = 32
SETTING_FFB_DAMPING_STRENGTH = 33
SETTING_FFB_INERTIA_STRENGTH = 34
SETTING_FFB_SINE_STRENGTH = 35
SETTING_FFB_SPRING_STRENGTH = 36
SETTING_FFB_RAMP_STRENGTH = 37
SETTING_FFB_SQUARE_STRENGTH = 38
SETTING_FFB_SAWTOOTH_STRENGTH = 39
SETTING_FFB_TRIANGLE_STRENGTH = 19
SETTING_FFB_FRICTION_FILTER_STRENGTH = 40
SETTING_FFB_DAMPING_FILTER_STRENGTH = 41
SETTING_FFB_INERTIA_FILTER_STRENGTH = 42
SETTING_DYNA_DAMPING = 43
SETTING_DYNA_THRESHOLD = 44
SETTING_DYNA_RANGE = 45
SETTING_CAR_SPEED = 46
SETTING_A1_MIN = 47
SETTING_A1_MAX = 48
SETTING_A2_MIN = 49
SETTING_A2_MAX = 50
SETTING_A3_MIN = 51
SETTING_A3_MAX = 52
SETTING_A4_MIN = 53
SETTING_A4_MAX = 54
SETTING_A5_MIN = 55
SETTING_A5_MAX = 56
SETTING_A6_MIN = 57
SETTING_A6_MAX = 58
SETTING_A7_MIN = 59
SETTING_A7_MAX = 60
SETTING_A1_RESET = 61
SETTING_A2_RESET = 62
SETTING_A3_RESET = 63
SETTING_A4_RESET = 64
SETTING_A5_RESET = 65
SETTING_A6_RESET = 66
SETTING_A7_RESET = 67
SETTING_FRONT_LED_ENABLE = 70
SETTING_BACK_LED_ENABLE = 71
SETTING_FRONT_LED_BRIGHTNESS = 72
SETTING_BACK_LED_BRIGHTNESS = 73
SETTING_BUZZER_ENABLE = 74
SETTING_BUZZER_SOUND_INTENSITY = 75
SETTING_BUZZER_PLAY = 76
SETTING_COOLING_MODE = 77
SETTING_UPDATA_MODE = 78
SETTING_BOOT_UPDATA_MODE = 79
SETTING_RGB = 100
SETTING_SPEED = 101
SETTING_LEFT_ROTARY_SW_MODE = 102
SETTING_RIGHT_ROTARY_SW_MODE = 103
SETTING_CLUTCH_MODE = 104
SETTING_JOY_MODE = 105
SETTING_START_JOY_CALIBRATE = 106
SETTING_JOY_CALIBRATE_X_MIN = 107
SETTING_JOY_CALIBRATE_X_MAX = 108
SETTING_JOY_CALIBRATE_Y_MIN = 109
SETTING_JOY_CALIBRATE_Y_MAX = 110
SETTING_JOY_CALIBRATE_FINISH = 111
SETTING_START_PADDLE_CALIBRATE = 112
SETTING_CLUTACH_CALIBRATE_X_MIN = 113
SETTING_CLUTACH_CALIBRATE_X_MAX = 114
SETTING_CLUTACH_CALIBRATE_Y_MIN = 115
SETTING_CLUTACH_CALIBRATE_Y_MAX = 116
SETTING_GEAR_CALIBRATE_X_MIN = 117
SETTING_GEAR_CALIBRATE_X_MAX = 118
SETTING_GEAR_CALIBRATE_Y_MIN = 119
SETTING_GEAR_CALIBRATE_Y_MAX = 120
SETTING_PADDLE_CALIBRATE_FINISH = 121
SETTING_SET_CLUTCH_POINT = 122
SETTING_BUTTON_RGB = 123
SETTING_HUB_BUZZER_ENABLE = 124
SETTING_HUB_BUZZER_SOUND_INTENSITY = 125
SETTING_HUB_BUZZER_PLAY = 126
SETTING_ENCODER_ALIGN = 127
SETTING_SYNA_LOCK = 128
SETTING_HUB_PADDLE_CALIBRATE = 129
SETTING_HUB_JOY_CALIBRATE = 130
SETTING_HUB_ENC_ZERO = 131
SETTING_TEST_TORQUE = 200
SETTING_2G4_PAIRING = 201
SETTING_FFB_SPEED_LIMIT = 203
SETTING_FFB_SIMPLY_SETTING = 204
SETTING_RGB_1 = 206
SETTING_RGB_2 = 207
SETTING_GAME_INFO_FAST = 208
SETTING_GAME_INFO_SLOW = 209
SETTING_BUZZER_OVERROTATION_ENABLE = 223
SETTING_BUZZER_FFBCLIP_ENABLE = 224
K1_ID = 0
K2_ID = 1
K3_ID = 2
K4_ID = 3
K5_ID = 4
K6_ID = 5
K7_ID = 6
K8_ID = 7
K9_ID = 8
K10_ID = 9
K11_ID = 10
K12_ID = 11
K13_ID = 12
K14_ID = 13
K15_ID = 14
K16_ID = 15
K17_ID = 16
K18_ID = 17
L_GEAR_ID = 18
R_GEAR_ID = 19
L_CLATCH_ID = 20
R_CLATCH_ID = 21
L_PADDLE_ID = 22
R_PADDLE_ID = 23
JOY_PUSH_ID = 24
JOY_UP_ID = 25
JOY_DOWN_ID = 26
JOY_LEFT_ID = 27
JOY_RIGHT_ID = 28
DIR_PUSH_ID = 29
DIR_UP_ID = 30
DIR_DOWN_ID = 31
DIR_LEFT_ID = 32
DIR_RIGHT_ID = 33
DIR_ENC_LEFT_ID = 34
DIR_ENC_RIGHT_ID = 35
L_ENC_LEFT_ID = 36
L_ENC_RIGHT_ID = 37
R_ENC_LEFT_ID = 38
R_ENC_RIGHT_ID = 39
L_ENC_K1_ID = 40
L_ENC_K2_ID = 41
L_ENC_K3_ID = 42
L_ENC_K4_ID = 43
L_ENC_K5_ID = 44
L_ENC_K6_ID = 45
L_ENC_K7_ID = 46
L_ENC_K8_ID = 47
L_ENC_K9_ID = 48
L_ENC_K10_ID = 49
L_ENC_K11_ID = 50
L_ENC_K12_ID = 51
R_ENC_K1_ID = 52
R_ENC_K2_ID = 53
R_ENC_K3_ID = 54
R_ENC_K4_ID = 55
R_ENC_K5_ID = 56
R_ENC_K6_ID = 57
R_ENC_K7_ID = 58
R_ENC_K8_ID = 59
R_ENC_K9_ID = 60
R_ENC_K10_ID = 61
R_ENC_K11_ID = 62
R_ENC_K12_ID = 63
MODE_PC = 1
MODE_PC_OTA = 2
MODE_PS3 = 3
MODE_PS4 = 4
MODE_XBOX = 5
MODE_X = 6
MODE_F = 7
WHEEL_HUB_FD1 = 4
WHEEL_HUB_FD1S = 5
WHEEL_F1_FF1S = 6
CMD_NON = 0
CMD_SND_FILE_DATA = 1
CMD_START_APP = 2
CMD_GET_VERSION = 3
APP_MAX_SIZE = 458752
BLK_SIZE = 2048
WRITE_WAIT_TOUT = 10
READ_WAIT_TOUT = 10
DATA_LOG_LENGTH = 6
RE_SEND_TOTAL = 3
ch_list = [
 121, 122, 123, 124, 125, 119, 118, 117, 116, 115,
 114, 113, 112, 111, 110, 109, 108, 107, 106, 105,
 104, 103, 102, 101, 100, 99, 98, 97, 96, 95,
 94, 93, 92, 91, 90, 89, 88, 87, 86, 85,
 84, 83, 82, 81, 80, 79, 78, 77, 76, 75]
game_id = {'r3e':1, 
 'rf1':2, 
 'rf2':3, 
 'ac':4, 
 'ets2':5, 
 'acc':6, 
 'fh4':7, 
 'pcars1':8, 
 'pcars2':9, 
 'f12020':10, 
 'f12019':11, 
 'f12018':12, 
 'drr2':13, 
 'dr':14, 
 'dr4':15, 
 'ir':16, 
 'f12021':17, 
 'ams2':18}

class gameDataStructure(Structure):
    _pack_ = 1
    _fields_ = [
     (
      't_game_id', c_uint16, 5),
     (
      't_yellow_flag', c_uint16, 1),
     (
      't_green_flag', c_uint16, 1),
     (
      't_white_flag', c_uint16, 1),
     (
      't_red_flag', c_uint16, 1),
     (
      't_blue_flag', c_uint16, 1),
     (
      't_black_flag', c_uint16, 1),
     (
      't_black_orange_flag', c_uint16, 1),
     (
      't_half_black_white_flag', c_uint16, 1),
     (
      't_yellow_red_flag', c_uint16, 1),
     (
      't_chequered_flag', c_uint16, 1),
     (
      't_sc_board', c_uint16, 1),
     (
      't_gas', c_uint32, 7),
     (
      't_brake', c_uint32, 7),
     (
      't_clutch', c_uint32, 7),
     (
      't_speed', c_uint32, 11),
     (
      'x_gforce', c_uint32, 8),
     (
      'y_gforce', c_uint32, 8),
     (
      't_rpm', c_uint32, 14),
     (
      't_xxx', c_uint32, 1),
     (
      't_pit_limiter', c_uint32, 1),
     (
      't_slip_ratio_for_ffb', c_uint16, 8),
     (
      'xxxxx', c_uint16, 8),
     (
      't_current_time_hour', c_uint16, 7),
     (
      't_load_diff', c_uint16, 8),
     (
      't_dsdsd', c_uint16, 1),
     (
      't_current_time_min', c_uint16, 6),
     (
      't_current_time_sec', c_uint16, 10),
     (
      't_fuel', c_uint16, 16),
     (
      't_total_fuel', c_uint16, 16),
     (
      't_fuel_remaining_laps', c_uint16, 16),
     (
      't_fl_tire_damage', c_uint32, 7),
     (
      't_fr_tire_damage', c_uint32, 7),
     (
      't_rl_tire_damage', c_uint32, 7),
     (
      't_rr_tire_damage', c_uint32, 7),
     (
      't_tc_running', c_uint32, 1),
     (
      't_abs_running', c_uint32, 1),
     (
      't_drs_actived', c_uint32, 1),
     (
      't_drs_allowed', c_uint32, 1),
     (
      't_fl_tire_temp', c_uint16, 10),
     (
      't_gear', c_uint16, 6),
     (
      't_fr_tire_temp', c_uint16, 10),
     (
      't_rear_slip_ratio_for_ffb', c_uint16, 6),
     (
      't_rl_tire_temp', c_uint16, 10),
     (
      't_dyna_damping_for_ffb', c_uint16, 6),
     (
      't_rr_tire_temp', c_uint16, 10),
     (
      't_x5', c_uint16, 6),
     (
      't_fl_brake_temp', c_uint16, 11),
     (
      't_x6', c_uint16, 5),
     (
      't_fr_brake_temp', c_uint16, 11),
     (
      't_x7', c_uint16, 5),
     (
      't_rl_brake_temp', c_uint16, 11),
     (
      't_x8', c_uint16, 5),
     (
      't_rr_brake_temp', c_uint16, 11),
     (
      't_x9', c_uint16, 5),
     (
      't_performance', c_uint16, 16),
     (
      't_ffb', c_int16, 16),
     (
      't_fl_wing_damage', c_uint32, 7),
     (
      't_fr_wing_damage', c_uint32, 7),
     (
      't_rear_wing_damage', c_uint32, 7),
     (
      't_engine_damage', c_uint32, 7),
     (
      'x1', c_uint32, 4),
     (
      't_gear_box_damage', c_uint8, 7),
     (
      'x33', c_uint8, 1),
     (
      't_drs_active_distance', c_uint8, 8),
     (
      'x2', c_uint16, 16),
     (
      'x3', c_uint16, 16)]


class gameDataSlowStructure(Structure):
    _pack_ = 1
    _fields_ = [
     (
      't_car_brand', c_uint16, 6),
     (
      't_car_type', c_uint16, 5),
     (
      'xxx1', c_uint16, 5),
     (
      't_car_num', c_uint32, 7),
     (
      't_pos', c_uint32, 7),
     (
      't_finish_lap', c_uint32, 9),
     (
      't_lap_number', c_uint32, 9),
     (
      't_last_time_hour', c_uint8, 7),
     (
      'xx', c_uint8, 1),
     (
      't_last_time_min', c_uint16, 6),
     (
      't_last_time_sec', c_uint16, 10),
     (
      't_best_time_hour', c_uint8, 7),
     (
      'xx2', c_uint8, 1),
     (
      't_best_time_min', c_uint16, 6),
     (
      't_best_time_sec', c_uint16, 10),
     (
      't_fl_tire_wear', c_uint32, 5),
     (
      't_fr_tire_wear', c_uint32, 5),
     (
      't_rl_tire_wear', c_uint32, 5),
     (
      't_rr_tire_wear', c_uint32, 5),
     (
      't_engine_temp', c_uint32, 10),
     (
      't_x1', c_uint32, 2),
     (
      't_tc', c_uint32, 4),
     (
      't_abs', c_uint32, 4),
     (
      't_brake_bias', c_uint32, 7),
     (
      't_diff_bias', c_uint32, 7),
     (
      'x1', c_uint32, 10),
     (
      't_max_rpm', c_uint16, 14),
     (
      's1212', c_uint16, 2),
     (
      't_ers_energy', c_uint16, 7),
     (
      't_kers_energy', c_uint16, 7),
     (
      't_ers_mode', c_uint16, 2),
     (
      't_ers_deployed_lap', c_uint16, 7),
     (
      't_fuel_mix', c_uint16, 2),
     (
      'x1111', c_uint16, 7),
     (
      'x3', c_uint16, 16),
     (
      'x4', c_uint32, 32),
     (
      'x5', c_uint32, 32),
     (
      'x6', c_uint32, 32),
     (
      'x7', c_uint32, 32),
     (
      'x8', c_uint32, 32),
     (
      'x9', c_uint32, 32),
     (
      'x10', c_uint32, 32)]


class rpmRgb565(Structure):
    _fields_ = [
     (
      'r1', c_uint16, 5),
     (
      'g1', c_uint16, 6),
     (
      'b1', c_uint16, 5),
     (
      'r2', c_uint16, 5),
     (
      'g2', c_uint16, 6),
     (
      'b2', c_uint16, 5),
     (
      'r3', c_uint16, 5),
     (
      'g3', c_uint16, 6),
     (
      'b3', c_uint16, 5),
     (
      'r4', c_uint16, 5),
     (
      'g4', c_uint16, 6),
     (
      'b4', c_uint16, 5),
     (
      'r5', c_uint16, 5),
     (
      'g5', c_uint16, 6),
     (
      'b5', c_uint16, 5),
     (
      'r6', c_uint16, 5),
     (
      'g6', c_uint16, 6),
     (
      'b6', c_uint16, 5),
     (
      'r7', c_uint16, 5),
     (
      'g7', c_uint16, 6),
     (
      'b7', c_uint16, 5),
     (
      'r8', c_uint16, 5),
     (
      'g8', c_uint16, 6),
     (
      'b8', c_uint16, 5),
     (
      'r9', c_uint16, 5),
     (
      'g9', c_uint16, 6),
     (
      'b9', c_uint16, 5),
     (
      'r10', c_uint16, 5),
     (
      'g10', c_uint16, 6),
     (
      'b10', c_uint16, 5),
     (
      'r11', c_uint16, 5),
     (
      'g11', c_uint16, 6),
     (
      'b11', c_uint16, 5),
     (
      'r12', c_uint16, 5),
     (
      'g12', c_uint16, 6),
     (
      'b12', c_uint16, 5)]


class buttonRgb565(Structure):
    _fields_ = [
     (
      'r1', c_uint16, 5),
     (
      'g1', c_uint16, 6),
     (
      'b1', c_uint16, 5),
     (
      'r2', c_uint16, 5),
     (
      'g2', c_uint16, 6),
     (
      'b2', c_uint16, 5),
     (
      'r3', c_uint16, 5),
     (
      'g3', c_uint16, 6),
     (
      'b3', c_uint16, 5),
     (
      'r4', c_uint16, 5),
     (
      'g4', c_uint16, 6),
     (
      'b4', c_uint16, 5),
     (
      'r5', c_uint16, 5),
     (
      'g5', c_uint16, 6),
     (
      'b5', c_uint16, 5),
     (
      'r6', c_uint16, 5),
     (
      'g6', c_uint16, 6),
     (
      'b6', c_uint16, 5),
     (
      'r7', c_uint16, 5),
     (
      'g7', c_uint16, 6),
     (
      'b7', c_uint16, 5),
     (
      'r8', c_uint16, 5),
     (
      'g8', c_uint16, 6),
     (
      'b8', c_uint16, 5),
     (
      'r9', c_uint16, 5),
     (
      'g9', c_uint16, 6),
     (
      'b9', c_uint16, 5),
     (
      'r10', c_uint16, 5),
     (
      'g10', c_uint16, 6),
     (
      'b10', c_uint16, 5),
     (
      'r11', c_uint16, 5),
     (
      'g11', c_uint16, 6),
     (
      'b11', c_uint16, 5),
     (
      'r12', c_uint16, 5),
     (
      'g12', c_uint16, 6),
     (
      'b12', c_uint16, 5),
     (
      'r13', c_uint16, 5),
     (
      'g13', c_uint16, 6),
     (
      'b13', c_uint16, 5),
     (
      'r14', c_uint16, 5),
     (
      'g14', c_uint16, 6),
     (
      'b14', c_uint16, 5),
     (
      'r15', c_uint16, 5),
     (
      'g15', c_uint16, 6),
     (
      'b15', c_uint16, 5),
     (
      'r16', c_uint16, 5),
     (
      'g16', c_uint16, 6),
     (
      'b16', c_uint16, 5)]


gameData = gameDataStructure()
gameData_slow = gameDataSlowStructure()
print(sizeof(gameData), sizeof(gameData_slow))
