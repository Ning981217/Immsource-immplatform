import ctypes, enum
from typing import Dict

class PackedLittleEndianStructure(ctypes.LittleEndianStructure):
    """'The base packet class for API version 2021'"""
    _pack_ = 1

    def __repr__(self):
        fstr_list = []
        for field in self._fields_:
            fname = field[0]
            value = getattr(self, fname)
            if isinstance(value, (PackedLittleEndianStructure, int, float, bytes)):
                vstr = repr(value)
            elif isinstance(value, ctypes.Array):
                vstr = '[{}]'.format(', '.join(repr(e) for e in value))
            else:
                raise RuntimeError('Bad value {!r} of type {!r}'.format(value, type(value)))
            fstr = f"{fname}={vstr}"
            fstr_list.append(fstr)

        return '{}({})'.format(self.__class__.__name__, ', '.join(fstr_list))


class PacketHeader(PackedLittleEndianStructure):
    _fields_ = [
     (
      'packetFormat', ctypes.c_uint16),
     (
      'gameMajorVersion', ctypes.c_uint8),
     (
      'gameMinorVersion', ctypes.c_uint8),
     (
      'packetVersion', ctypes.c_uint8),
     (
      'packetId', ctypes.c_uint8),
     (
      'sessionUID', ctypes.c_uint64),
     (
      'sessionTime', ctypes.c_float),
     (
      'frameIdentifier', ctypes.c_uint32),
     (
      'playerCarIndex', ctypes.c_uint8),
     (
      'secondary_player_car_index', ctypes.c_uint8)]


class CarMotionData(PackedLittleEndianStructure):
    _fields_ = [
     (
      'worldPositionX', ctypes.c_float),
     (
      'worldPositionY', ctypes.c_float),
     (
      'worldPositionZ', ctypes.c_float),
     (
      'worldVelocityX', ctypes.c_float),
     (
      'worldVelocityY', ctypes.c_float),
     (
      'worldVelocityZ', ctypes.c_float),
     (
      'worldForwardDirX', ctypes.c_int16),
     (
      'worldForwardDirY', ctypes.c_int16),
     (
      'worldForwardDirZ', ctypes.c_int16),
     (
      'worldRightDirX', ctypes.c_int16),
     (
      'worldRightDirY', ctypes.c_int16),
     (
      'worldRightDirZ', ctypes.c_int16),
     (
      'gForceLateral', ctypes.c_float),
     (
      'gForceLongitudinal', ctypes.c_float),
     (
      'gForceVertical', ctypes.c_float),
     (
      'yaw', ctypes.c_float),
     (
      'pitch', ctypes.c_float),
     (
      'roll', ctypes.c_float)]


class PacketMotionData(PackedLittleEndianStructure):
    _fields_ = [
     (
      'header', PacketHeader),
     (
      'carMotionData', CarMotionData * 22),
     (
      'suspensionPosition', ctypes.c_float * 4),
     (
      'suspensionVelocity', ctypes.c_float * 4),
     (
      'suspensionAcceleration', ctypes.c_float * 4),
     (
      'wheelSpeed', ctypes.c_float * 4),
     (
      'wheelSlip', ctypes.c_float * 4),
     (
      'localVelocityX', ctypes.c_float),
     (
      'localVelocityY', ctypes.c_float),
     (
      'localVelocityZ', ctypes.c_float),
     (
      'angularVelocityX', ctypes.c_float),
     (
      'angularVelocityY', ctypes.c_float),
     (
      'angularVelocityZ', ctypes.c_float),
     (
      'angularAccelerationX', ctypes.c_float),
     (
      'angularAccelerationY', ctypes.c_float),
     (
      'angularAccelerationZ', ctypes.c_float),
     (
      'frontWheelsAngle', ctypes.c_float)]


class MarshalZone(PackedLittleEndianStructure):
    _fields_ = [
     (
      'zoneStart', ctypes.c_float),
     (
      'zoneFlag', ctypes.c_int8)]


class WeatherForecastSample(PackedLittleEndianStructure):
    _fields_ = [
     (
      'session_type', ctypes.c_uint8),
     (
      'time_offset', ctypes.c_uint8),
     (
      'weather', ctypes.c_uint8),
     (
      'track_temperature', ctypes.c_int8),
     (
      'track_temperature_change', ctypes.c_int8),
     (
      'air_temperature', ctypes.c_int8),
     (
      'air_temperature_change', ctypes.c_int8),
     (
      'rain_percentage', ctypes.c_uint8)]


class PacketSessionData(PackedLittleEndianStructure):
    _fields_ = [
     (
      'header', PacketHeader),
     (
      'weather', ctypes.c_uint8),
     (
      'trackTemperature', ctypes.c_int8),
     (
      'airTemperature', ctypes.c_int8),
     (
      'totalLaps', ctypes.c_uint8),
     (
      'trackLength', ctypes.c_uint16),
     (
      'sessionType', ctypes.c_uint8),
     (
      'trackId', ctypes.c_int8),
     (
      'm_formula', ctypes.c_uint8),
     (
      'sessionTimeLeft', ctypes.c_uint16),
     (
      'sessionDuration', ctypes.c_uint16),
     (
      'pitSpeedLimit', ctypes.c_uint8),
     (
      'gamePaused', ctypes.c_uint8),
     (
      'isSpectating', ctypes.c_uint8),
     (
      'spectatorCarIndex', ctypes.c_uint8),
     (
      'sliProNativeSupport', ctypes.c_uint8),
     (
      'numMarshalZones', ctypes.c_uint8),
     (
      'marshalZones', MarshalZone * 21),
     (
      'safetyCarStatus', ctypes.c_uint8),
     (
      'networkGame', ctypes.c_uint8),
     (
      'num_weather_forecast_samples', ctypes.c_uint8),
     (
      'weather_forecast_samples', WeatherForecastSample * 56),
     (
      'forecast_accuracy', ctypes.c_uint8),
     (
      'ai_difficulty', ctypes.c_uint8),
     (
      'season_link_identifier', ctypes.c_uint32),
     (
      'weekend_link_identifier', ctypes.c_uint32),
     (
      'session_link_identifier', ctypes.c_uint32),
     (
      'pit_stop_window_ideal_lap', ctypes.c_uint8),
     (
      'pit_stop_window_latest_lap', ctypes.c_uint8),
     (
      'pit_stop_rejoin_position', ctypes.c_uint8),
     (
      'steering_assist', ctypes.c_uint8),
     (
      'braking_assist', ctypes.c_uint8),
     (
      'gearbox_assist', ctypes.c_uint8),
     (
      'pit_assist', ctypes.c_uint8),
     (
      'pit_release_assist', ctypes.c_uint8),
     (
      'ersassist', ctypes.c_uint8),
     (
      'drsassist', ctypes.c_uint8),
     (
      'dynamic_racing_line', ctypes.c_uint8),
     (
      'dynamic_racing_line_type', ctypes.c_uint8)]


class LapData(PackedLittleEndianStructure):
    _fields_ = [
     (
      'lastLapTime', ctypes.c_uint32),
     (
      'currentLapTime', ctypes.c_uint32),
     (
      'sector1_time_in_ms', ctypes.c_uint16),
     (
      'sector2_time_in_ms', ctypes.c_uint16),
     (
      'lap_distance', ctypes.c_float),
     (
      'total_distance', ctypes.c_float),
     (
      'safety_car_delta', ctypes.c_float),
     (
      'carPosition', ctypes.c_uint8),
     (
      'currentLapNum', ctypes.c_uint8),
     (
      'pit_status', ctypes.c_uint8),
     (
      'num_pit_stops', ctypes.c_uint8),
     (
      'sector', ctypes.c_uint8),
     (
      'current_lap_invalid', ctypes.c_uint8),
     (
      'penalties', ctypes.c_uint8),
     (
      'warnings', ctypes.c_uint8),
     (
      'num_unserved_drive_through_pens', ctypes.c_uint8),
     (
      'num_unserved_stop_go_pens', ctypes.c_uint8),
     (
      'grid_position', ctypes.c_uint8),
     (
      'driver_status', ctypes.c_uint8),
     (
      'result_status', ctypes.c_uint8),
     (
      'pit_lane_timer_active', ctypes.c_uint8),
     (
      'pit_lane_time_in_lane_in_ms', ctypes.c_uint16),
     (
      'pit_stop_timer_in_ms', ctypes.c_uint16),
     (
      'pit_stop_should_serve_pen', ctypes.c_uint8)]


class PacketLapData(PackedLittleEndianStructure):
    _fields_ = [
     (
      'header', PacketHeader),
     (
      'lapData', LapData * 22)]


class FastestLap(PackedLittleEndianStructure):
    _fields_ = [
     (
      'vehicle_idx', ctypes.c_uint8),
     (
      'lap_time', ctypes.c_float)]


class Retirement(PackedLittleEndianStructure):
    _fields_ = [
     (
      'vehicle_idx', ctypes.c_uint8)]


class TeamMateInPits(PackedLittleEndianStructure):
    _fields_ = [
     (
      'vehicle_idx', ctypes.c_uint8)]


class RaceWinner(PackedLittleEndianStructure):
    _fields_ = [
     (
      'vehicle_idx', ctypes.c_uint8)]


class Penalty(PackedLittleEndianStructure):
    _fields_ = [
     (
      'penalty_type', ctypes.c_uint8),
     (
      'infringement_type', ctypes.c_uint8),
     (
      'vehicle_idx', ctypes.c_uint8),
     (
      'other_vehicle_idx', ctypes.c_uint8),
     (
      'time', ctypes.c_uint8),
     (
      'lap_num', ctypes.c_uint8),
     (
      'places_gained', ctypes.c_uint8)]


class SpeedTrap(PackedLittleEndianStructure):
    _fields_ = [
     (
      'vehicle_idx', ctypes.c_uint8),
     (
      'speed', ctypes.c_float),
     (
      'overall_fastest_in_session', ctypes.c_uint8),
     (
      'driver_fastest_in_session', ctypes.c_uint8)]


class StartLights(PackedLittleEndianStructure):
    _fields_ = [
     (
      'num_lights', ctypes.c_uint8)]


class DriveThroughPenaltyServed(PackedLittleEndianStructure):
    _fields_ = [
     (
      'vehicle_idx', ctypes.c_uint8)]


class StopGoPenaltyServed(PackedLittleEndianStructure):
    _fields_ = [
     (
      'vehicle_idx', ctypes.c_uint8)]


class Flashback(PackedLittleEndianStructure):
    _fields_ = [
     (
      'flashback_frame_identifier', ctypes.c_uint32),
     (
      'flashback_session_time', ctypes.c_float)]


class Buttons(PackedLittleEndianStructure):
    _fields_ = [
     (
      'button_status', ctypes.c_uint32)]


class EventDataDetails(ctypes.Union):
    _fields_ = [
     (
      'fastest_lap', FastestLap),
     (
      'retirement', Retirement),
     (
      'team_mate_in_pits', TeamMateInPits),
     (
      'race_winner', RaceWinner),
     (
      'penalty', Penalty),
     (
      'speed_trap', SpeedTrap),
     (
      'start_lights', StartLights),
     (
      'drive_through_penalty_served', DriveThroughPenaltyServed),
     (
      'stop_go_penalty_served', StopGoPenaltyServed),
     (
      'flashback', Flashback),
     (
      'buttons', Buttons)]


class PacketEventData(PackedLittleEndianStructure):
    _fields_ = [
     (
      'header', PacketHeader),
     (
      'event_string_code', ctypes.c_uint8 * 4),
     (
      'event_details', EventDataDetails)]


class ParticipantData(PackedLittleEndianStructure):
    _fields_ = [
     (
      'ai_controlled', ctypes.c_uint8),
     (
      'driver_id', ctypes.c_uint8),
     (
      'network_id', ctypes.c_uint8),
     (
      'team_id', ctypes.c_uint8),
     (
      'my_team', ctypes.c_uint8),
     (
      'race_number', ctypes.c_uint8),
     (
      'nationality', ctypes.c_uint8),
     (
      'name', ctypes.c_char * 48),
     (
      'your_telemetry', ctypes.c_uint8)]


class PacketParticipantsData(PackedLittleEndianStructure):
    _fields_ = [
     (
      'header', PacketHeader),
     (
      'numActiveCars', ctypes.c_uint8),
     (
      'participants', ParticipantData * 22)]


class CarSetupData(PackedLittleEndianStructure):
    _fields_ = [
     (
      'frontWing', ctypes.c_uint8),
     (
      'rearWing', ctypes.c_uint8),
     (
      'onThrottle', ctypes.c_uint8),
     (
      'offThrottle', ctypes.c_uint8),
     (
      'frontCamber', ctypes.c_float),
     (
      'rearCamber', ctypes.c_float),
     (
      'frontToe', ctypes.c_float),
     (
      'rearToe', ctypes.c_float),
     (
      'frontSuspension', ctypes.c_uint8),
     (
      'rearSuspension', ctypes.c_uint8),
     (
      'frontAntiRollBar', ctypes.c_uint8),
     (
      'rearAntiRollBar', ctypes.c_uint8),
     (
      'frontSuspensionHeight', ctypes.c_uint8),
     (
      'rearSuspensionHeight', ctypes.c_uint8),
     (
      'brakePressure', ctypes.c_uint8),
     (
      'brakeBias', ctypes.c_uint8),
     (
      'm_rear_left_tyre_pressure', ctypes.c_float),
     (
      'm_rear_right_tyre_pressure', ctypes.c_float),
     (
      'm_front_left_tyre_pressure', ctypes.c_float),
     (
      'm_front_right_tyre_pressure', ctypes.c_float),
     (
      'ballast', ctypes.c_uint8),
     (
      'fuelLoad', ctypes.c_float)]


class PacketCarSetupData(PackedLittleEndianStructure):
    _fields_ = [
     (
      'header', PacketHeader),
     (
      'carSetups', CarSetupData * 22)]


class CarTelemetryData(PackedLittleEndianStructure):
    _fields_ = [
     (
      'speed', ctypes.c_uint16),
     (
      'throttle', ctypes.c_float),
     (
      'steer', ctypes.c_float),
     (
      'brake', ctypes.c_float),
     (
      'clutch', ctypes.c_uint8),
     (
      'gear', ctypes.c_int8),
     (
      'engineRPM', ctypes.c_uint16),
     (
      'drs', ctypes.c_uint8),
     (
      'revLightsPercent', ctypes.c_uint8),
     (
      'm_rev_lights_bit_value', ctypes.c_uint16),
     (
      'brakesTemperature', ctypes.c_uint16 * 4),
     (
      'tyresSurfaceTemperature', ctypes.c_uint8 * 4),
     (
      'tyresInnerTemperature', ctypes.c_uint8 * 4),
     (
      'engineTemperature', ctypes.c_uint16),
     (
      'tyresPressure', ctypes.c_float * 4),
     (
      'surfaceType', ctypes.c_uint8 * 4)]


class PacketCarTelemetryData(PackedLittleEndianStructure):
    _fields_ = [
     (
      'header', PacketHeader),
     (
      'carTelemetryData', CarTelemetryData * 22),
     (
      'mfd_panel_index', ctypes.c_uint8),
     (
      'mfd_panel_index_secondary_player', ctypes.c_uint8),
     (
      'suggested_gear', ctypes.c_int8)]


class CarStatusData(PackedLittleEndianStructure):
    _fields_ = [
     (
      'tractionControl', ctypes.c_uint8),
     (
      'antiLockBrakes', ctypes.c_uint8),
     (
      'fuelMix', ctypes.c_uint8),
     (
      'frontBrakeBias', ctypes.c_uint8),
     (
      'pitLimiterStatus', ctypes.c_uint8),
     (
      'fuelInTank', ctypes.c_float),
     (
      'fuelCapacity', ctypes.c_float),
     (
      'fuelRemainingLaps', ctypes.c_float),
     (
      'maxRPM', ctypes.c_uint16),
     (
      'idleRPM', ctypes.c_uint16),
     (
      'maxGears', ctypes.c_uint8),
     (
      'drsAllowed', ctypes.c_uint8),
     (
      'drsActivationDistance', ctypes.c_uint16),
     (
      'actualTyreCompound', ctypes.c_uint8),
     (
      'tyreVisualCompound', ctypes.c_uint8),
     (
      'm_tyres_age_laps', ctypes.c_uint8),
     (
      'vehicleFiaFlags', ctypes.c_int8),
     (
      'ersStoreEnergy', ctypes.c_float),
     (
      'ersDeployMode', ctypes.c_uint8),
     (
      'ersHarvestedThisLapMGUK', ctypes.c_float),
     (
      'ersHarvestedThisLapMGUH', ctypes.c_float),
     (
      'ersDeployedThisLap', ctypes.c_float),
     (
      'network_paused', ctypes.c_uint8)]


class PacketCarStatusData(PackedLittleEndianStructure):
    _fields_ = [
     (
      'header', PacketHeader),
     (
      'carStatusData', CarStatusData * 22)]


class FinalClassificationData(PackedLittleEndianStructure):
    _fields_ = [
     (
      'position', ctypes.c_uint8),
     (
      'num_laps', ctypes.c_uint8),
     (
      'grid_position', ctypes.c_uint8),
     (
      'points', ctypes.c_uint8),
     (
      'num_pit_stops', ctypes.c_uint8),
     (
      'result_status', ctypes.c_uint8),
     (
      'bestLapTime', ctypes.c_uint32),
     (
      'total_race_time', ctypes.c_double),
     (
      'penalties_time', ctypes.c_uint8),
     (
      'num_penalties', ctypes.c_uint8),
     (
      'num_tyre_stints', ctypes.c_uint8),
     (
      'tyre_stints_actual', ctypes.c_uint8 * 8),
     (
      'tyre_stints_visual', ctypes.c_uint8 * 8)]


class PacketFinalClassificationData(PackedLittleEndianStructure):
    _fields_ = [
     (
      'header', PacketHeader),
     (
      'num_cars', ctypes.c_uint8),
     (
      'classification_data', FinalClassificationData * 22)]


class LobbyInfoData(PackedLittleEndianStructure):
    _fields_ = [
     (
      'ai_controlled', ctypes.c_uint8),
     (
      'team_id', ctypes.c_uint8),
     (
      'nationality', ctypes.c_uint8),
     (
      'name', ctypes.c_char * 48),
     (
      'car_number', ctypes.c_uint8),
     (
      'ready_status', ctypes.c_uint8)]


class PacketLobbyInfoData(PackedLittleEndianStructure):
    _fields_ = [
     (
      'header', PacketHeader),
     (
      'num_players', ctypes.c_uint8),
     (
      'lobby_players', LobbyInfoData * 22)]


class CarDamageData(PackedLittleEndianStructure):
    _fields_ = [
     (
      'tyres_wear', ctypes.c_float * 4),
     (
      'tyres_damage', ctypes.c_uint8 * 4),
     (
      'brakes_damage', ctypes.c_uint8 * 4),
     (
      'front_left_wing_damage', ctypes.c_uint8),
     (
      'front_right_wing_damage', ctypes.c_uint8),
     (
      'rear_wing_damage', ctypes.c_uint8),
     (
      'floor_damage', ctypes.c_uint8),
     (
      'diffuser_damage', ctypes.c_uint8),
     (
      'sidepod_damage', ctypes.c_uint8),
     (
      'drs_fault', ctypes.c_uint8),
     (
      'gear_box_damage', ctypes.c_uint8),
     (
      'engine_damage', ctypes.c_uint8),
     (
      'engine_mguhwear', ctypes.c_uint8),
     (
      'engine_eswear', ctypes.c_uint8),
     (
      'engine_cewear', ctypes.c_uint8),
     (
      'engine_icewear', ctypes.c_uint8),
     (
      'engine_mgukwear', ctypes.c_uint8),
     (
      'engine_tcwear', ctypes.c_uint8)]


class PacketCarDamageData(PackedLittleEndianStructure):
    _fields_ = [
     (
      'header', PacketHeader),
     (
      'car_damage_data', CarDamageData * 22)]


class LapHistoryData(PackedLittleEndianStructure):
    _fields_ = [
     (
      'lap_time_in_ms', ctypes.c_uint32),
     (
      'sector1_time_in_ms', ctypes.c_uint16),
     (
      'sector2_time_in_ms', ctypes.c_uint16),
     (
      'sector3_time_in_ms', ctypes.c_uint16),
     (
      'lap_valid_bit_flags', ctypes.c_uint8)]


class TyreStintHistoryData(PackedLittleEndianStructure):
    _fields_ = [
     (
      'end_lap', ctypes.c_uint8),
     (
      'tyre_actual_compound', ctypes.c_uint8),
     (
      'tyre_visual_compound', ctypes.c_uint8)]


class PacketSessionHistoryData(PackedLittleEndianStructure):
    _fields_ = [
     (
      'header', PacketHeader),
     (
      'car_idx', ctypes.c_uint8),
     (
      'num_laps', ctypes.c_uint8),
     (
      'num_tyre_stints', ctypes.c_uint8),
     (
      'best_lap_time_lap_num', ctypes.c_uint8),
     (
      'best_sector1_lap_num', ctypes.c_uint8),
     (
      'best_sector2_lap_num', ctypes.c_uint8),
     (
      'best_sector3_lap_num', ctypes.c_uint8),
     (
      'lap_history_data', LapHistoryData * 100),
     (
      'tyre_stints_history_data', TyreStintHistoryData * 8)]


HeaderFieldsToPacketType = {(2021, 1, 0): PacketMotionData, 
 (2021, 1, 1): PacketSessionData, 
 (2021, 1, 2): PacketLapData, 
 (2021, 1, 3): PacketEventData, 
 (2021, 1, 4): PacketParticipantsData, 
 (2021, 1, 5): PacketCarSetupData, 
 (2021, 1, 6): PacketCarTelemetryData, 
 (2021, 1, 7): PacketCarStatusData, 
 (2021, 1, 8): PacketFinalClassificationData, 
 (2021, 1, 9): PacketLobbyInfoData, 
 (2021, 1, 10): PacketCarDamageData, 
 (2021, 1, 11): PacketSessionHistoryData}

class UnpackError(Exception):
    """'Exception for packets that cannot be unpacked'"""
    pass


def unpack_udp_packet(packet: bytes) -> PackedLittleEndianStructure:
    """Convert raw UDP packet to an appropriately-typed telemetry packet.

    Args:
        packet: the contents of the UDP packet to be unpacked.

    Returns:
        The decoded packet structure.

    Raises:
        UnpackError if a problem is detected.
    """
    actual_packet_size = len(packet)
    header_size = ctypes.sizeof(PacketHeader)
    if actual_packet_size < header_size:
        raise UnpackError(f"Bad telemetry packet: too short ({actual_packet_size} bytes).")
    header = PacketHeader.from_buffer_copy(packet)
    key = (header.packetFormat, header.packetVersion, header.packetId)
    if key not in HeaderFieldsToPacketType:
        raise UnpackError(f"Bad telemetry packet: no match for key fields {key!r}.")
    packet_type = HeaderFieldsToPacketType[key]
    expected_packet_size = ctypes.sizeof(packet_type)
    if actual_packet_size != expected_packet_size:
        raise UnpackError('Bad telemetry packet: bad size for {} packet; expected {} bytes but received {} bytes.'.format(packet_type.__name__, expected_packet_size, actual_packet_size))
    return packet_type.from_buffer_copy(packet)
