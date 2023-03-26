from traceback import format_exc
from time import sleep, time
from mmap import mmap
from os.path import getmtime
from pyRF1 import *
from psutil import pid_exists
from setting_define import *

class pyDashRF1:

    def __init__(self, rf1_pid, game_data, enable):
        self.rf1_pid = rf1_pid
        self.game_data = game_data[0]
        self.game_data_slow = game_data[1]
        self.enable = enable
        self.status = False
        self.rfMapHandle = None
        try:
            self.rfMapHandle = mmap(fileno=0, length=(sizeof(rfShared)), tagname=rfMapTag)
            if pid_exists(self.rf1_pid):
                self.status = True
                self.game_data.t_game_id = game_id['rf1']
        except:
            print('Unable to open shared memory map')

    def isRun(self):
        return self.status

    def __del__(self):
        pass

    def update(self):
        if pid_exists(self.rf1_pid):
            if self.enable:
                try:
                    self.rfMapHandle.seek(0)
                    physics_smm = rfShared.from_buffer_copy(self.rfMapHandle)
                    self.game_data.t_speed = int(physics_smm.speed + 0.5)
                    self.game_data.t_rpm = physics_smm.engineRPM
                    self.game_data_slow.t_max_rpm = physics_smm.engineMaxRPM
                    self.status = True
                    return self.game_data
                except:
                    print('rf1 updata error')
                    self.status = False

        else:
            self.status = False
