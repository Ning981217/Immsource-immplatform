from traceback import format_exc
from time import sleep, time
from os.path import getmtime
from psutil import pid_exists
import mmap, struct
from setting_define import *

class Ets2SdkBoolean:
    CruiseControl = 0
    Wipers = 1
    ParkBrake = 2
    MotorBrake = 3
    ElectricEnabled = 4
    EngineEnabled = 5
    BlinkerLeftActive = 6
    BlinkerRightActive = 7
    BlinkerLeftOn = 8
    BlinkerRightOn = 9
    LightsParking = 10
    LightsBeamLow = 11
    LightsBeamHigh = 12
    LightsAuxFront = 13
    LightsAuxRoof = 14
    LightsBeacon = 15
    LightsBrake = 16
    LightsReverse = 17
    BatteryVoltageWarning = 18
    AirPressureWarning = 19
    AirPressureEmergency = 20
    AdblueWarning = 21
    OilPressureWarning = 22
    WaterTemperatureWarning = 23
    TrailerAttached = 24


class SharedMemory:

    def __init__(self):
        self.map_name = 'Local\\SimTelemetryETS2'
        self.map_size = 1024
        self.mmap = None

    def connect(self):
        self.mmap = mmap.mmap(0, self.map_size, self.map_name, mmap.ACCESS_READ)

    def update(self):
        self.connect()
        updated_data = Ets2SdkData()
        updated_data.time = self.retrieve_field('I', 0, 4)
        updated_data.paused = self.retrieve_field('I', 4, 8)
        updated_data.ets2_telemetry_plugin_revision = self.retrieve_field('I', 8, 12)
        updated_data.ets2_version_major = self.retrieve_field('I', 12, 16)
        updated_data.ets2_version_minor = self.retrieve_field('I', 16, 20)
        updated_data.flags = self.mmap[20:24]
        updated_data.speed = self.retrieve_field('f', 24, 28)
        updated_data.accelerationX = self.retrieve_field('f', 28, 32)
        updated_data.accelerationY = self.retrieve_field('f', 32, 36)
        updated_data.accelerationZ = self.retrieve_field('f', 36, 40)
        updated_data.coordinateX = self.retrieve_field('f', 40, 44)
        updated_data.coordinateY = self.retrieve_field('f', 44, 48)
        updated_data.coordinateZ = self.retrieve_field('f', 48, 52)
        updated_data.rotationX = self.retrieve_field('f', 52, 56)
        updated_data.rotationY = self.retrieve_field('f', 56, 60)
        updated_data.rotationZ = self.retrieve_field('f', 60, 64)
        updated_data.gear = self.retrieve_field('I', 64, 68)
        updated_data.gears = self.retrieve_field('I', 68, 72)
        updated_data.gearRanges = self.retrieve_field('I', 72, 76)
        updated_data.gearRangeActive = self.retrieve_field('I', 76, 80)
        updated_data.engineRpm = self.retrieve_field('f', 80, 84)
        updated_data.engineRpmMax = self.retrieve_field('f', 84, 88)
        updated_data.fuel = self.retrieve_field('f', 88, 92)
        updated_data.fuelCapacity = self.retrieve_field('f', 92, 96)
        updated_data.fuelRate = self.retrieve_field('f', 96, 100)
        updated_data.fuelAvgConsumption = self.retrieve_field('f', 100, 104)
        updated_data.userSteer = self.retrieve_field('f', 104, 108)
        updated_data.userThrottle = self.retrieve_field('f', 108, 112)
        updated_data.userBrake = self.retrieve_field('f', 112, 116)
        updated_data.userClutch = self.retrieve_field('f', 116, 120)
        updated_data.gameSteer = self.retrieve_field('f', 120, 124)
        updated_data.gameThrottle = self.retrieve_field('f', 124, 128)
        updated_data.gameBrake = self.retrieve_field('f', 128, 132)
        updated_data.gameClutch = self.retrieve_field('f', 132, 136)
        updated_data.truckWeight = self.retrieve_field('f', 136, 140)
        updated_data.trailerWeight = self.retrieve_field('f', 140, 144)
        updated_data.modelOffset = self.retrieve_field('I', 144, 148)
        updated_data.modelLength = self.retrieve_field('I', 148, 152)
        updated_data.trailerOffset = self.retrieve_field('I', 152, 156)
        updated_data.trailerLength = self.retrieve_field('I', 156, 160)
        updated_data.timeAbsolute = self.retrieve_field('I', 160, 164)
        updated_data.gearsReverse = self.retrieve_field('I', 164, 168)
        updated_data.trailerMass = self.retrieve_field('f', 168, 172)
        updated_data.trailerId = self.mmap[172:236]
        updated_data.trailerName = self.mmap[236:300]
        updated_data.jobIncome = self.retrieve_field('I', 300, 304)
        updated_data.jobDeadline = self.retrieve_field('I', 304, 308)
        updated_data.jobCitySource = self.mmap[308:372]
        updated_data.jobCityDestination = self.mmap[372:436]
        updated_data.jobCompanySource = self.mmap[436:500]
        updated_data.jobCompanyDestination = self.mmap[500:564]
        updated_data.retarderBrake = self.retrieve_field('I', 564, 568)
        updated_data.shifterSlot = self.retrieve_field('I', 568, 572)
        updated_data.shifterToggle = self.retrieve_field('I', 572, 576)
        updated_data.fill = self.retrieve_field('I', 576, 580)
        updated_data.aux = self.mmap[580:604]
        updated_data.airPressure = self.retrieve_field('f', 604, 608)
        updated_data.brakeTemperature = self.retrieve_field('f', 608, 612)
        updated_data.fuelWarning = self.retrieve_field('I', 612, 616)
        updated_data.adblue = self.retrieve_field('f', 616, 620)
        updated_data.adblueConsumption = self.retrieve_field('f', 620, 624)
        updated_data.oilPressure = self.retrieve_field('f', 624, 628)
        updated_data.oilTemperature = self.retrieve_field('f', 628, 632)
        updated_data.waterTemperature = self.retrieve_field('f', 632, 636)
        updated_data.batteryVoltage = self.retrieve_field('f', 636, 640)
        updated_data.lightsDashboard = self.retrieve_field('f', 640, 644)
        updated_data.wearEngine = self.retrieve_field('f', 644, 648)
        updated_data.wearTransmission = self.retrieve_field('f', 648, 652)
        updated_data.wearCabin = self.retrieve_field('f', 652, 656)
        updated_data.wearChassis = self.retrieve_field('f', 656, 660)
        updated_data.wearWheels = self.retrieve_field('f', 660, 664)
        updated_data.wearTrailer = self.retrieve_field('f', 664, 668)
        updated_data.truckOdometer = self.retrieve_field('f', 668, 672)
        updated_data.cruiseControlSpeed = self.retrieve_field('f', 672, 676)
        updated_data.truckMake = self.mmap[676:740]
        updated_data.truckMakeId = self.mmap[740:804]
        updated_data.truckModel = self.mmap[804:868]
        updated_data.speedlimit = self.retrieve_field('f', 868, 872)
        updated_data.routeDistance = self.retrieve_field('f', 872, 876)
        updated_data.routeTime = self.retrieve_field('f', 876, 880)
        updated_data.fuelRange = self.retrieve_field('f', 880, 884)
        updated_data.gearRatioForward = self.retrieve_array('24f', 884, 980)
        updated_data.gearRatioReverse = self.retrieve_array('8f', 980, 1012)
        updated_data.gearRatioDifferential = self.retrieve_field('f', 1012, 1016)
        updated_data.gearDashboard = self.retrieve_field('I', 1016, 1020)
        updated_data.onJob = self.retrieve_field('b', 1020, 1021)
        updated_data.jobFinished = self.retrieve_field('b', 1021, 1022)
        return updated_data

    def retrieve_field(self, f, start, end):
        field_data = struct.unpack(f, self.mmap[start:end])[0]
        return field_data

    def retrieve_array(self, f, start, end):
        array_data = struct.unpack(f, self.mmap[start:end])
        return array_data


class ets2sdkclient:

    def GetBool(self, i):
        return True

    def update(self):
        self.mm = mmap.mmap(fileno=0, length=32768, tagname='Local\\SimTelemetryETS2')
        self.mm.seek(0)
        self.time = struct.unpack('I', self.mm[0:4])[0]
        self.paused = struct.unpack('I', self.mm[4:8])[0]
        self.ets2_telemetry_plugin_revision = struct.unpack('I', self.mm[8:12])[0]
        self.ets2_version_major = struct.unpack('I', self.mm[12:16])[0]
        self.ets2_version_minor = struct.unpack('I', self.mm[16:20])[0]
        self.flags = self.mm[20:24]
        self.speed = struct.unpack('f', self.mm[24:28])[0]
        self.accelerationX = struct.unpack('f', self.mm[28:32])[0]
        self.accelerationY = struct.unpack('f', self.mm[32:36])[0]
        self.accelerationZ = struct.unpack('f', self.mm[36:40])[0]
        self.coordinateX = struct.unpack('f', self.mm[40:44])[0]
        self.coordinateY = struct.unpack('f', self.mm[44:48])[0]
        self.coordinateZ = struct.unpack('f', self.mm[48:52])[0]
        self.rotationX = struct.unpack('f', self.mm[52:56])[0]
        self.rotationY = struct.unpack('f', self.mm[56:60])[0]
        self.rotationZ = struct.unpack('f', self.mm[60:64])[0]
        self.gear = struct.unpack('I', self.mm[64:68])[0]
        self.gears = struct.unpack('I', self.mm[68:72])[0]
        self.gearRanges = struct.unpack('I', self.mm[72:76])[0]
        self.gearRangeActive = struct.unpack('I', self.mm[76:80])[0]
        self.engineRpm = struct.unpack('f', self.mm[80:84])[0]
        self.engineRpmMax = struct.unpack('f', self.mm[84:88])[0]
        self.fuel = struct.unpack('f', self.mm[88:92])[0]
        self.fuelCapacity = struct.unpack('f', self.mm[92:96])[0]
        self.fuelRate = struct.unpack('f', self.mm[96:100])[0]
        self.fuelAvgConsumption = struct.unpack('f', self.mm[100:104])[0]
        self.userSteer = struct.unpack('f', self.mm[104:108])[0]
        self.userThrottle = struct.unpack('f', self.mm[108:112])[0]
        self.userBrake = struct.unpack('f', self.mm[112:116])[0]
        self.userClutch = struct.unpack('f', self.mm[116:120])[0]
        self.gameSteer = struct.unpack('f', self.mm[120:124])[0]
        self.gameThrottle = struct.unpack('f', self.mm[124:128])[0]
        self.gameBrake = struct.unpack('f', self.mm[128:132])[0]
        self.gameClutch = struct.unpack('f', self.mm[132:136])[0]
        self.truckWeight = struct.unpack('f', self.mm[136:140])[0]
        self.trailerWeight = struct.unpack('f', self.mm[140:144])[0]
        self.modelOffset = struct.unpack('I', self.mm[144:148])[0]
        self.modelLength = struct.unpack('I', self.mm[148:152])[0]
        self.trailerOffset = struct.unpack('I', self.mm[152:156])[0]
        self.trailerLength = struct.unpack('I', self.mm[156:160])[0]
        self.timeAbsolute = struct.unpack('I', self.mm[160:164])[0]
        self.gearsReverse = struct.unpack('I', self.mm[164:168])[0]
        self.trailerMass = struct.unpack('f', self.mm[168:172])[0]
        self.trailerId = self.mm[172:236]
        self.trailerName = self.mm[236:300]
        self.jobIncome = struct.unpack('I', self.mm[300:304])[0]
        self.jobDeadline = struct.unpack('I', self.mm[304:308])[0]
        self.jobCitySource = self.mm[308:372]
        self.jobCityDestination = self.mm[372:436]
        self.jobCompanySource = self.mm[436:500]
        self.jobCompanyDestination = self.mm[500:564]
        self.retarderBrake = struct.unpack('I', self.mm[564:568])[0]
        self.shifterSlot = struct.unpack('I', self.mm[568:572])[0]
        self.shifterToggle = struct.unpack('I', self.mm[572:576])[0]
        self.aux = self.mm[580:604]
        self.airPressure = struct.unpack('f', self.mm[604:608])[0]
        self.brakeTemperature = struct.unpack('f', self.mm[608:612])[0]
        self.fuelWarning = struct.unpack('I', self.mm[612:616])[0]
        self.adblue = struct.unpack('f', self.mm[616:620])[0]
        self.adblueConsumption = struct.unpack('f', self.mm[620:624])[0]
        self.oilPressure = struct.unpack('f', self.mm[624:628])[0]
        self.oilTemperature = struct.unpack('f', self.mm[628:632])[0]
        self.waterTemperature = struct.unpack('f', self.mm[632:636])[0]
        self.batteryVoltage = struct.unpack('f', self.mm[636:640])[0]
        self.lightsDashboard = struct.unpack('f', self.mm[640:644])[0]
        self.wearEngine = struct.unpack('f', self.mm[644:648])[0]
        self.wearTransmission = struct.unpack('f', self.mm[648:652])[0]
        self.wearCabin = struct.unpack('f', self.mm[652:656])[0]
        self.wearChassis = struct.unpack('f', self.mm[656:660])[0]
        self.wearWheels = struct.unpack('f', self.mm[660:664])[0]
        self.wearTrailer = struct.unpack('f', self.mm[664:668])[0]
        self.truckOdometer = struct.unpack('f', self.mm[668:672])[0]
        self.cruiseControlSpeed = struct.unpack('f', self.mm[672:676])[0]
        self.truckMake = self.mm[676:740]
        self.truckMakeId = self.mm[740:804]
        self.truckModel = self.mm[804:868]
        self.speedLimit = struct.unpack('f', self.mm[868:872])[0]
        self.routeDistance = struct.unpack('f', self.mm[872:876])[0]
        self.routeTime = struct.unpack('f', self.mm[876:880])[0]
        self.fuelRange = struct.unpack('f', self.mm[880:884])[0]
        self.gearRatioDifferential = struct.unpack('f', self.mm[1012:1016])[0]
        self.gearDashboard = struct.unpack('I', self.mm[1016:1020])[0]
        self.CruiseControl = self.GetBool(Ets2SdkBoolean.CruiseControl)
        self.Wipers = self.GetBool(Ets2SdkBoolean.Wipers)
        self.ParkBrake = self.GetBool(Ets2SdkBoolean.ParkBrake)
        self.MotorBrake = self.GetBool(Ets2SdkBoolean.MotorBrake)
        self.ElectricEnabled = self.GetBool(Ets2SdkBoolean.ElectricEnabled)
        self.EngineEnabled = self.GetBool(Ets2SdkBoolean.EngineEnabled)
        self.BlinkerLeftActive = self.GetBool(Ets2SdkBoolean.BlinkerLeftActive)
        self.BlinkerRightActive = self.GetBool(Ets2SdkBoolean.BlinkerRightActive)
        self.BlinkerLeftOn = self.GetBool(Ets2SdkBoolean.BlinkerLeftOn)
        self.BlinkerRightOn = self.GetBool(Ets2SdkBoolean.BlinkerRightOn)
        self.LightsParking = self.GetBool(Ets2SdkBoolean.LightsParking)
        self.LightsBeamLow = self.GetBool(Ets2SdkBoolean.LightsBeamLow)
        self.LightsBeamHigh = self.GetBool(Ets2SdkBoolean.LightsBeamHigh)
        self.LightsAuxFront = self.GetBool(Ets2SdkBoolean.LightsAuxFront)
        self.LightsAuxRoof = self.GetBool(Ets2SdkBoolean.LightsAuxRoof)
        self.LightsBeacon = self.GetBool(Ets2SdkBoolean.LightsBeacon)
        self.LightsBrake = self.GetBool(Ets2SdkBoolean.LightsBrake)
        self.LightsReverse = self.GetBool(Ets2SdkBoolean.LightsReverse)
        self.BatteryVoltageWarning = self.GetBool(Ets2SdkBoolean.BatteryVoltageWarning)
        self.AirPressureWarning = self.GetBool(Ets2SdkBoolean.AirPressureWarning)
        self.AirPressureEmergency = self.GetBool(Ets2SdkBoolean.AirPressureEmergency)
        self.AdblueWarning = self.GetBool(Ets2SdkBoolean.AdblueWarning)
        self.OilPressureWarning = self.GetBool(Ets2SdkBoolean.OilPressureWarning)
        self.WaterTemperatureWarning = self.GetBool(Ets2SdkBoolean.WaterTemperatureWarning)
        self.TrailerAttached = self.GetBool(Ets2SdkBoolean.TrailerAttached)
        self.mm.close()


class pyDashETS2:

    def __init__(self, ets2_pid, dash, game_data, enable):
        self.ets2_pid = ets2_pid
        self.game_data = game_data[0]
        self.game_data_slow = game_data[1]
        self.enable = enable
        self.dash = dash
        self.status = False
        self.e = None
        try:
            self.e = ets2sdkclient()
            if pid_exists(self.ets2_pid):
                self.status = True
                self.game_data.t_game_id = game_id['ets2']
        except:
            print('Unable to open shared memory map')

    def isRun(self):
        return self.status

    def __del__(self):
        pass

    def update(self):
        if pid_exists(self.ets2_pid) and self.enable:
            try:
                self.e.update()
                self.game_data.t_speed = int(self.e.speed * 3.6 + 0.5)
                self.game_data.t_rpm = self.e.engineRpm
                self.game_data_slow.t_max_rpm = self.e.engineRpmMax
                self.game_data.t_gas = int(self.gameThrottle)
                self.game_data.t_brake = int(self.gameBrake)
                self.game_data.t_clutch = int(self.gameClutch)
                if self.e.gear == 0:
                    self.game_data.t_gear = 30
                elif self.e.gear == 1:
                    self.game_data.t_gear = 31
                else:
                    self.game_data.t_gear = int(self.e.gear - 1)
                self.game_data.t_speed = int(self.e.speed + 0.5)
                self.game_data.t_fuel = int(self.e.fuel)
                self.status = True
                return self.game_data
            except Exception as e:
                print('ets2 updata error', e)
                self.status = False

        else:
            self.status = False