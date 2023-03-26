from traceback import format_exc
from time import sleep, time
from mmap import mmap
from os.path import getmtime
from pyPCARS import *
from psutil import pid_exists
from setting_define import *

class pyDashAMS2:

    def __init__(self, ams2_pid, dash, game_data, enable):
        self.ams2_pid = ams2_pid
        self.game_data = game_data[0]
        self.game_data_slow = game_data[1]
        self.dash = dash
        self.enable = enable
        self.status = False
        self.rfMapHandle = None
        try:
            self.rfMapHandle = mmap(fileno=0, length=(sizeof(pcarsPhysics)), tagname=pcarsMapTag)
            if pid_exists(self.ams2_pid):
                self.status = True
                self.game_data.t_game_id = game_id['ams2']
        except:
            print('Unable to open shared memory map')

    def isRun(self):
        return self.status

    def __del__(self):
        pass

    def update(self):
        if pid_exists(self.ams2_pid):
            if self.enable:
                try:
                    self.rfMapHandle.seek(0)
                    physics_smm = pcarsPhysics.from_buffer_copy(self.rfMapHandle)
                    self.game_data.t_speed = int(physics_smm.mSpeed + 0.5)
                    self.game_data.t_rpm = int(physics_smm.mRpm)
                    self.game_data_slow.t_max_rpm = int(physics_smm.mMaxRPM)
                    self.status = True
                    return self.game_data
                except Exception as e:
                    print('ams2 updata error', e)
                    self.status = False

        else:
            self.status = False
