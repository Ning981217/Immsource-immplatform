# uncompyle6 version 3.5.0
# Python bytecode 3.6 (3379)
# Decompiled from: Python 2.7.5 (default, Nov 16 2020, 22:23:17) 
# [GCC 4.8.5 20150623 (Red Hat 4.8.5-44)]
# Embedded file name: f1_2018_telemetry\packets.py
# Compiled at: 1995-09-28 00:18:56
# Size of source mod 2**32: 257 bytes
"""F1 2018 UDP Telemetry support package

This package is based on the CodeMasters Forum post documenting the F1 2018 packet format:

    https://forums.codemasters.com/topic/38920-f1-2018-udp-specification/

Compared to the definitions given there, the Python version has the following changes:

(1) In the 'PacketMotionData' structure, the comments for the three m_angularAcceleration{X,Y,Z} fields erroneously
    refer to 'velocity' rather than 'acceleration'. This was corrected.
(2) In the 'CarSetupData' structure, the comment of the m_rearAntiRollBar refer to rear instead of front. This was corrected.
(3) In the Driver IDs table, driver 34 has name "Wilheim Kaufmann".
    This is a typo; whenever this driver is encountered in the game, his name is given as "Wilhelm Kaufmann".
"""
import ctypes, enum

class PackedLittleEndianStructure(ctypes.LittleEndianStructure):
    r"""'The standard ctypes LittleEndianStructure, but tightly packed (no field padding), and with a proper repr() function.\n\n    This is the base type for all structures in the telemetry data.\n    '"""
    _pack_ = 1

    def __repr__(self):
        fstr_list = []
        for fname, ftype in self._fields_:
            value = getattr(self, fname)
            if isinstance(value, (PackedLittleEndianStructure, int, float, bytes)):
                vstr = repr(value)
            elif isinstance(value, ctypes.Array):
                vstr = '[{}]'.format(', '.join(repr(e) for e in value))
            else:
                raise RuntimeError('Bad value {!r} of type {!r}'.format(value, type(value)))
            fstr = '{}={}'.format(fname, vstr)
            fstr_list.append(fstr)

        return '{}({})'.format(self.__class__.__name__, ', '.join(fstr_list))


class PacketHeader(PackedLittleEndianStructure):
    """'The header for each of the UDP telemetry packets.'"""
    _fields_ = [
     (
      'packetFormat', ctypes.c_uint16),
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
      'playerCarIndex', ctypes.c_uint8)]


@enum.unique
class PacketID(enum.IntEnum):
    """'Value as specified in the PacketHeader.packetId header field, used to distinguish packet types.'"""
    MOTION = 0
    SESSION = 1
    LAP_DATA = 2
    EVENT = 3
    PARTICIPANTS = 4
    CAR_SETUPS = 5
    CAR_TELEMETRY = 6
    CAR_STATUS = 7


PacketID.short_description = {PacketID.MOTION: 'Motion', 
 PacketID.SESSION: 'Session', 
 PacketID.LAP_DATA: 'Lap Data', 
 PacketID.EVENT: 'Event', 
 PacketID.PARTICIPANTS: 'Participants', 
 PacketID.CAR_SETUPS: 'Car Setups', 
 PacketID.CAR_TELEMETRY: 'Car Telemetry', 
 PacketID.CAR_STATUS: 'Car Status'}
PacketID.long_description = {PacketID.MOTION: u"Contains all motion data for player's car \u2013 only sent while player is in control", 
 PacketID.SESSION: u'Data about the session \u2013 track, time left', 
 PacketID.LAP_DATA: 'Data about all the lap times of cars in the session', 
 PacketID.EVENT: 'Various notable events that happen during a session', 
 PacketID.PARTICIPANTS: 'List of participants in the session, mostly relevant for multiplayer', 
 PacketID.CAR_SETUPS: 'Packet detailing car setups for cars in the race', 
 PacketID.CAR_TELEMETRY: 'Telemetry data for all cars', 
 PacketID.CAR_STATUS: 'Status data for all cars such as damage'}

class CarMotionData_V1(PackedLittleEndianStructure):
    """"This type is used for the 20-element 'carMotionData' array of the PacketMotionData_V1 type, defined below.\""""
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


class PacketMotionData_V1(PackedLittleEndianStructure):
    u"""The motion packet gives physics data for all the cars being driven.

    There is additional data for the car being driven with the goal of being able to drive a motion platform setup.

    N.B. For the normalised vectors below, to convert to float values divide by 32767.0f \u2013 16-bit signed values are
    used to pack the data and on the assumption that direction values are always between -1.0f and 1.0f.

    Frequency: Rate as specified in menus
    Size: 1343 bytes
    Version: 1
    """
    _fields_ = [
     (
      'header', PacketHeader),
     (
      'carMotionData', CarMotionData_V1 * 20),
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


class MarshalZone_V1(PackedLittleEndianStructure):
    """"This type is used for the 21-element 'marshalZones' array of the PacketSessionData_V1 type, defined below.\""""
    _fields_ = [
     (
      'zoneStart', ctypes.c_float),
     (
      'zoneFlag', ctypes.c_int8)]


class PacketSessionData_V1(PackedLittleEndianStructure):
    r"""'The session packet includes details about the current session in progress.\n\n    Frequency: 2 per second\n    Size: 149 bytes\n    Version: 1\n    '"""
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
      'marshalZones', MarshalZone_V1 * 21),
     (
      'safetyCarStatus', ctypes.c_uint8),
     (
      'networkGame', ctypes.c_uint8)]


class LapData_V1(PackedLittleEndianStructure):
    """"This type is used for the 20-element 'lapData' array of the PacketLapData_V1 type, defined below.\""""
    _fields_ = [
     (
      'lastLapTime', ctypes.c_float),
     (
      'currentLapTime', ctypes.c_float),
     (
      'bestLapTime', ctypes.c_float),
     (
      'sector1Time', ctypes.c_float),
     (
      'sector2Time', ctypes.c_float),
     (
      'lapDistance', ctypes.c_float),
     (
      'totalDistance', ctypes.c_float),
     (
      'safetyCarDelta', ctypes.c_float),
     (
      'carPosition', ctypes.c_uint8),
     (
      'currentLapNum', ctypes.c_uint8),
     (
      'pitStatus', ctypes.c_uint8),
     (
      'sector', ctypes.c_uint8),
     (
      'currentLapInvalid', ctypes.c_uint8),
     (
      'penalties', ctypes.c_uint8),
     (
      'gridPosition', ctypes.c_uint8),
     (
      'driverStatus', ctypes.c_uint8),
     (
      'resultStatus', ctypes.c_uint8)]


class PacketLapData_V1(PackedLittleEndianStructure):
    r"""'The lap data packet gives details of all the cars in the session.\n\n    Frequency: Rate as specified in menus\n    Size: 843 bytes\n    Version: 1\n    '"""
    _fields_ = [
     (
      'header', PacketHeader),
     (
      'lapData', LapData_V1 * 20)]


class PacketEventData_V1(PackedLittleEndianStructure):
    r"""'This packet gives details of events that happen during the course of a session.\n\n    Frequency: When the event occurs\n    Size: 32 bytes\n    Version: 1\n    '"""
    _fields_ = [
     (
      'header', PacketHeader),
     (
      'eventStringCode', ctypes.c_char * 4)]


@enum.unique
class EventStringCode(enum.Enum):
    """'Value as specified in the PacketEventData_V1.eventStringCode header field, used to distinguish packet types.'"""
    SSTA = 'SSTA'
    SEND = 'SEND'
    FTLP = 'FTLP'
    RTMT = 'RTMT'
    DRSE = 'DRSE'
    DRSD = 'DRSD'
    TMPT = 'TMPT'
    CHQF = 'CHQF'
    RCWN = 'RCWN'


EventStringCode.short_description = {EventStringCode.SSTA: 'Session Started', 
 EventStringCode.SEND: 'Session Ended', 
 EventStringCode.FTLP: 'Fastest Lap', 
 EventStringCode.RTMT: 'Retirement', 
 EventStringCode.DRSE: 'DRS enabled', 
 EventStringCode.DRSD: 'DRS disabled', 
 EventStringCode.TMPT: 'Team mate in pits', 
 EventStringCode.CHQF: 'Chequered flag', 
 EventStringCode.RCWN: 'Race Winner'}
EventStringCode.long_description = {EventStringCode.SSTA: 'Sent when the session starts', 
 EventStringCode.SEND: 'Sent when the session ends', 
 EventStringCode.FTLP: 'When a driver achieves the fastest lap', 
 EventStringCode.RTMT: 'When a driver retires', 
 EventStringCode.DRSE: 'Race control have enabled DRS', 
 EventStringCode.DRSD: 'Race control have disabled DRS', 
 EventStringCode.TMPT: 'Your team mate has entered the pits', 
 EventStringCode.CHQF: 'The chequered flag has been waved', 
 EventStringCode.RCWN: 'The race winner is announced'}

class ParticipantData_V1(PackedLittleEndianStructure):
    """"This type is used for the 20-element 'participants' array of the PacketParticipantsData_V1 type, defined below.\""""
    _fields_ = [
     (
      'aiControlled', ctypes.c_uint8),
     (
      'driverId', ctypes.c_uint8),
     (
      'teamId', ctypes.c_uint8),
     (
      'raceNumber', ctypes.c_uint8),
     (
      'nationality', ctypes.c_uint8),
     (
      'name', ctypes.c_char * 48)]


class PacketParticipantsData_V1(PackedLittleEndianStructure):
    r"""'This is a list of participants in the race.\n\n    If the vehicle is controlled by AI, then the name will be the driver name.\n    If this is a multiplayer game, the names will be the Steam Id on PC, or the LAN name if appropriate.\n    On Xbox One, the names will always be the driver name, on PS4 the name will be the LAN name if playing a LAN game,\n    otherwise it will be the driver name.\n\n    Frequency: Every 5 seconds\n    Size: 1104 bytes\n    Version: 1\n    '"""
    _fields_ = [
     (
      'header', PacketHeader),
     (
      'numActiveCars', ctypes.c_uint8),
     (
      'participants', ParticipantData_V1 * 20)]


class CarSetupData_V1(PackedLittleEndianStructure):
    """"This type is used for the 20-element 'carSetups' array of the PacketCarSetupData_V1 type, defined below.\""""
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
      'frontTyrePressure', ctypes.c_float),
     (
      'rearTyrePressure', ctypes.c_float),
     (
      'ballast', ctypes.c_uint8),
     (
      'fuelLoad', ctypes.c_float)]


class PacketCarSetupData_V1(PackedLittleEndianStructure):
    r"""'This packet details the car setups for each vehicle in the session.\n\n    Note that in multiplayer games, other player cars will appear as blank, you will only be able to see your car setup and AI cars.\n\n    Frequency: 2 per second\n    Size: 843 bytes\n    Version: 1\n    '"""
    _fields_ = [
     (
      'header', PacketHeader),
     (
      'carSetups', CarSetupData_V1 * 20)]


class CarTelemetryData_V1(PackedLittleEndianStructure):
    """"This type is used for the 20-element 'carTelemetryData' array of the PacketCarTelemetryData_V1 type, defined below.\""""
    _fields_ = [
     (
      'speed', ctypes.c_uint16),
     (
      'throttle', ctypes.c_uint8),
     (
      'steer', ctypes.c_int8),
     (
      'brake', ctypes.c_uint8),
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
      'brakesTemperature', ctypes.c_uint16 * 4),
     (
      'tyresSurfaceTemperature', ctypes.c_uint16 * 4),
     (
      'tyresInnerTemperature', ctypes.c_uint16 * 4),
     (
      'engineTemperature', ctypes.c_uint16),
     (
      'tyresPressure', ctypes.c_float * 4)]


class PacketCarTelemetryData_V1(PackedLittleEndianStructure):
    r"""'This packet details telemetry for all the cars in the race.\n\n    It details various values that would be recorded on the car such as speed, throttle application, DRS etc.\n\n    Frequency: Rate as specified in menus\n    Size: 1347 bytes\n    Version: 1\n    '"""
    _fields_ = [
     (
      'header', PacketHeader),
     (
      'carTelemetryData', CarTelemetryData_V1 * 20),
     (
      'buttonStatus', ctypes.c_uint32)]


class CarStatusData_V1(PackedLittleEndianStructure):
    u"""This type is used for the 20-element 'carStatusData' array of the PacketCarStatusData_V1 type, defined below.

    There is some data in the Car Status packets that you may not want other players seeing if you are in a multiplayer game.
    This is controlled by the "Your Telemetry" setting in the Telemetry options. The options are:

        Restricted (Default) \u2013 other players viewing the UDP data will not see values for your car;
        Public \u2013 all other players can see all the data for your car.

    Note: You can always see the data for the car you are driving regardless of the setting.

    The following data items are set to zero if the player driving the car in question has their "Your Telemetry" set to "Restricted":

        fuelInTank
        fuelCapacity
        fuelMix
        fuelRemainingLaps
        frontBrakeBias
        frontLeftWingDamage
        frontRightWingDamage
        rearWingDamage
        engineDamage
        gearBoxDamage
        tyresWear (All four wheels)
        tyresDamage (All four wheels)
        ersDeployMode
        ersStoreEnergy
        ersDeployedThisLap
        ersHarvestedThisLapMGUK
        ersHarvestedThisLapMGUH
    """
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
      'maxRPM', ctypes.c_uint16),
     (
      'idleRPM', ctypes.c_uint16),
     (
      'maxGears', ctypes.c_uint8),
     (
      'drsAllowed', ctypes.c_uint8),
     (
      'tyresWear', ctypes.c_uint8 * 4),
     (
      'tyreCompound', ctypes.c_uint8),
     (
      'tyresDamage', ctypes.c_uint8 * 4),
     (
      'frontLeftWingDamage', ctypes.c_uint8),
     (
      'frontRightWingDamage', ctypes.c_uint8),
     (
      'rearWingDamage', ctypes.c_uint8),
     (
      'engineDamage', ctypes.c_uint8),
     (
      'gearBoxDamage', ctypes.c_uint8),
     (
      'exhaustDamage', ctypes.c_uint8),
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
      'ersDeployedThisLap', ctypes.c_float)]


class PacketCarStatusData_V1(PackedLittleEndianStructure):
    r"""'This packet details car statuses for all the cars in the race.\n\n    It includes values such as the damage readings on the car.\n\n    Frequency: Rate as specified in menus\n    Size: 1143 bytes\n    Version: 1\n    '"""
    _fields_ = [
     (
      'header', PacketHeader),
     (
      'carStatusData', CarStatusData_V1 * 20)]


TeamIDs = {0:'Mercedes', 
 1:'Ferrari', 
 2:'Red Bull Racing', 
 3:'Williams', 
 4:'Racing Point', 
 5:'Renault', 
 6:'Toro Rosso', 
 7:'Haas', 
 8:'McLaren', 
 9:'Alfa Romeo', 
 10:'McLaren 1988', 
 11:'McLaren 1991', 
 12:'Williams 1992', 
 13:'Ferrari 1995', 
 14:'Williams 1996', 
 15:'McLaren 1998', 
 16:'Ferrari 2002', 
 17:'Ferrari 2004', 
 18:'Renault 2006', 
 19:'Ferrari 2007', 
 21:'Red Bull 2010', 
 22:'Ferrari 1976', 
 23:'ART Grand Prix', 
 24:'Campos Vexatec Racing', 
 25:'Carlin', 
 26:'Charouz Racing System', 
 27:'DAMS', 
 28:'Russian Time', 
 29:'MP Motorsport', 
 30:'Pertamina', 
 31:'McLaren 1990', 
 32:'Trident', 
 33:'BWT Arden', 
 34:'McLaren 1976', 
 35:'Lotus 1972', 
 36:'Ferrari 1979', 
 37:'McLaren 1982', 
 38:'Williams 2003', 
 39:'Brawn 2009', 
 40:'Lotus 1978', 
 63:'Ferrari 1990', 
 64:'McLaren 2010', 
 65:'Ferrari 2010'}
DriverIDs = {0:'Carlos Sainz', 
 1:'Daniil Kvyat', 
 2:'Daniel Ricciardo', 
 6:u'Kimi Ra\u0308ikko\u0308nen', 
 7:'Lewis Hamilton', 
 9:'Max Verstappen', 
 10:'Nico Hulkenberg', 
 11:'Kevin Magnussen', 
 12:'Romain Grosjean', 
 13:'Sebastian Vettel', 
 14:'Sergio Perez', 
 15:'Valtteri Bottas', 
 19:'Lance Stroll', 
 20:'Arron Barnes', 
 21:'Martin Giles', 
 22:'Alex Murray', 
 23:'Lucas Roth', 
 24:'Igor Correia', 
 25:'Sophie Levasseur', 
 26:'Jonas Schiffer', 
 27:'Alain Forest', 
 28:'Jay Letourneau', 
 29:'Esto Saari', 
 30:'Yasar Atiyeh', 
 31:'Callisto Calabresi', 
 32:'Naota Izum', 
 33:'Howard Clarke', 
 34:'Wilhelm Kaufmann', 
 35:'Marie Laursen', 
 36:'Flavio Nieves', 
 37:'Peter Belousov', 
 38:'Klimek Michalski', 
 39:'Santiago Moreno', 
 40:'Benjamin Coppens', 
 41:'Noah Visser', 
 42:'Gert Waldmuller', 
 43:'Julian Quesada', 
 44:'Daniel Jones', 
 45:'Artem Markelov', 
 46:'Tadasuke Makino', 
 47:'Sean Gelael', 
 48:'Nyck De Vries', 
 49:'Jack Aitken', 
 50:'George Russell', 
 51:u'Maximilian Gu\u0308nther', 
 52:'Nirei Fukuzumi', 
 53:'Luca Ghiotto', 
 54:'Lando Norris', 
 55:u'Se\u0301rgio Sette Ca\u0302mara', 
 56:u'Louis Dele\u0301traz', 
 57:'Antonio Fuoco', 
 58:'Charles Leclerc', 
 59:'Pierre Gasly', 
 62:'Alexander Albon', 
 63:'Nicholas Latifi', 
 64:'Dorian Boccolacci', 
 65:'Niko Kari', 
 66:'Roberto Merhi', 
 67:'Arjun Maini', 
 68:'Alessio Lorandi', 
 69:'Ruben Meijer', 
 70:'Rashid Nair', 
 71:'Jack Tremblay', 
 74:'Antonio Giovinazzi', 
 75:'Robert Kubica'}
TrackIDs = {0:'Melbourne', 
 1:'Paul Ricard', 
 2:'Shanghai', 
 3:'Sakhir (Bahrain)', 
 4:'Catalunya', 
 5:'Monaco', 
 6:'Montreal', 
 7:'Silverstone', 
 8:'Hockenheim', 
 9:'Hungaroring', 
 10:'Spa', 
 11:'Monza', 
 12:'Singapore', 
 13:'Suzuka', 
 14:'Abu Dhabi', 
 15:'Texas', 
 16:'Brazil', 
 17:'Austria', 
 18:'Sochi', 
 19:'Mexico', 
 20:'Baku (Azerbaijan)', 
 21:'Sakhir Short', 
 22:'Silverstone Short', 
 23:'Texas Short', 
 24:'Suzuka Short'}
NationalityIDs = {1:'American', 
 2:'Argentinian', 
 3:'Australian', 
 4:'Austrian', 
 5:'Azerbaijani', 
 6:'Bahraini', 
 7:'Belgian', 
 8:'Bolivian', 
 9:'Brazilian', 
 10:'British', 
 11:'Bulgarian', 
 12:'Cameroonian', 
 13:'Canadian', 
 14:'Chilean', 
 15:'Chinese', 
 16:'Colombian', 
 17:'Costa Rican', 
 18:'Croatian', 
 19:'Cypriot', 
 20:'Czech', 
 21:'Danish', 
 22:'Dutch', 
 23:'Ecuadorian', 
 24:'English', 
 25:'Emirian', 
 26:'Estonian', 
 27:'Finnish', 
 28:'French', 
 29:'German', 
 30:'Ghanaian', 
 31:'Greek', 
 32:'Guatemalan', 
 33:'Honduran', 
 34:'Hong Konger', 
 35:'Hungarian', 
 36:'Icelander', 
 37:'Indian', 
 38:'Indonesian', 
 39:'Irish', 
 40:'Israeli', 
 41:'Italian', 
 42:'Jamaican', 
 43:'Japanese', 
 44:'Jordanian', 
 45:'Kuwaiti', 
 46:'Latvian', 
 47:'Lebanese', 
 48:'Lithuanian', 
 49:'Luxembourger', 
 50:'Malaysian', 
 51:'Maltese', 
 52:'Mexican', 
 53:'Monegasque', 
 54:'New Zealander', 
 55:'Nicaraguan', 
 56:'North Korean', 
 57:'Northern Irish', 
 58:'Norwegian', 
 59:'Omani', 
 60:'Pakistani', 
 61:'Panamanian', 
 62:'Paraguayan', 
 63:'Peruvian', 
 64:'Polish', 
 65:'Portuguese', 
 66:'Qatari', 
 67:'Romanian', 
 68:'Russian', 
 69:'Salvadoran', 
 70:'Saudi', 
 71:'Scottish', 
 72:'Serbian', 
 73:'Singaporean', 
 74:'Slovakian', 
 75:'Slovenian', 
 76:'South Korean', 
 77:'South African', 
 78:'Spanish', 
 79:'Swedish', 
 80:'Swiss', 
 81:'Thai', 
 82:'Turkish', 
 83:'Uruguayan', 
 84:'Ukrainian', 
 85:'Venezuelan', 
 86:'Welsh'}
SurfaceTypes = {0:'Tarmac', 
 1:'Rumble strip', 
 2:'Concrete', 
 3:'Rock', 
 4:'Gravel', 
 5:'Mud', 
 6:'Sand', 
 7:'Grass', 
 8:'Water', 
 9:'Cobblestone', 
 10:'Metal', 
 11:'Ridged'}

@enum.unique
class ButtonFlag(enum.IntEnum):
    """"Bit-mask values for the 'button' field in Car Telemetry Data packets.\""""
    CROSS = 1
    TRIANGLE = 2
    CIRCLE = 4
    SQUARE = 8
    D_PAD_LEFT = 16
    D_PAD_RIGHT = 32
    D_PAD_UP = 64
    D_PAD_DOWN = 128
    OPTIONS = 256
    L1 = 512
    R1 = 1024
    L2 = 2048
    R2 = 4096
    LEFT_STICK_CLICK = 8192
    RIGHT_STICK_CLICK = 16384


ButtonFlag.description = {ButtonFlag.CROSS: 'Cross or A', 
 ButtonFlag.TRIANGLE: 'Triangle or Y', 
 ButtonFlag.CIRCLE: 'Circle or B', 
 ButtonFlag.SQUARE: 'Square or X', 
 ButtonFlag.D_PAD_LEFT: 'D-pad Left', 
 ButtonFlag.D_PAD_RIGHT: 'D-pad Right', 
 ButtonFlag.D_PAD_UP: 'D-pad Up', 
 ButtonFlag.D_PAD_DOWN: 'D-pad Down', 
 ButtonFlag.OPTIONS: 'Options or Menu', 
 ButtonFlag.L1: 'L1 or LB', 
 ButtonFlag.R1: 'R1 or RB', 
 ButtonFlag.L2: 'L2 or LT', 
 ButtonFlag.R2: 'R2 or RT', 
 ButtonFlag.LEFT_STICK_CLICK: 'Left Stick Click', 
 ButtonFlag.RIGHT_STICK_CLICK: 'Right Stick Click'}
HeaderFieldsToPacketType = {(2018, 1, 0): PacketMotionData_V1, 
 (2018, 1, 1): PacketSessionData_V1, 
 (2018, 1, 2): PacketLapData_V1, 
 (2018, 1, 3): PacketEventData_V1, 
 (2018, 1, 4): PacketParticipantsData_V1, 
 (2018, 1, 5): PacketCarSetupData_V1, 
 (2018, 1, 6): PacketCarTelemetryData_V1, 
 (2018, 1, 7): PacketCarStatusData_V1}

class UnpackError(Exception):
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
        raise UnpackError('Bad telemetry packet: too short ({} bytes).'.format(actual_packet_size))
    header = PacketHeader.from_buffer_copy(packet)
    key = (header.packetFormat, header.packetVersion, header.packetId)
    if key not in HeaderFieldsToPacketType:
        raise UnpackError('Bad telemetry packet: no match for key fields {!r}.'.format(key))
    packet_type = HeaderFieldsToPacketType[key]
    expected_packet_size = ctypes.sizeof(packet_type)
    if actual_packet_size != expected_packet_size:
        raise UnpackError('Bad telemetry packet: bad size for {} packet; expected {} bytes but received {} bytes.'.format(packet_type.__name__, expected_packet_size, actual_packet_size))
    return packet_type.from_buffer_copy(packet)


if __name__ == '__main__':
    if not ctypes.sizeof(PacketMotionData_V1) == 1341:
        raise AssertionError
    if not ctypes.sizeof(PacketSessionData_V1) == 147:
        raise AssertionError
    if not ctypes.sizeof(PacketLapData_V1) == 841:
        raise AssertionError
    if not ctypes.sizeof(PacketEventData_V1) == 25:
        raise AssertionError
    if not ctypes.sizeof(PacketParticipantsData_V1) == 1082:
        raise AssertionError
    if not ctypes.sizeof(PacketCarSetupData_V1) == 841:
        raise AssertionError
    if not ctypes.sizeof(PacketCarTelemetryData_V1) == 1085:
        raise AssertionError
    if not ctypes.sizeof(PacketCarStatusData_V1) == 1061:
        raise AssertionError
