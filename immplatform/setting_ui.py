from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import QTimer
from PyQt5.QtSerialPort import QSerialPort, QSerialPortInfo
from PyQt5.QtCore import QIODevice, pyqtSignal
import time, main
from base_ui import WidgetUI
from setting_define import *
from uitl import Utiliy
from uitl import Refresher
import configparser
from setting_define import *

class SettingChooser(Utiliy):

    def __init__(self, hidchooser, main):
        self.main = main
        self.hidchooser = hidchooser
        self.cf = configparser.ConfigParser()
        self.cf.read('setting.cfg')
        self.secs = self.cf.sections()
        for sec in self.secs:
            if 'ffb_effect-' in sec:
                self.main.cfg_comboBox.addItem(sec.replace('ffb_effect-', ''))

        self.soft_estop_mode = [
         30, 200]
        self.normal_estop_mode = [50, 120]
        self.hard_estop_mode = [80, 50]
        self.inertia_offset = -1
        self.Value_List = [
         self.main.FF_Global_strength_Value, self.main.FF_Response_Value, self.main.Speed_Limit_Value, self.main.Detail_Enhancer_Value, self.main.FF_Filter_Value, self.main.FF_Maxtorque_Value,
         self.main.Mech_Spring_Value, self.main.Mech_Friction_Value, self.main.Mech_Damping_Value, self.main.Mech_Inertia_Value, self.main.Mech_Endstop_Value,
         self.main.Dyna_Damping_Value, self.main.Understeer_Effect_Value,
         self.main.FF_Constant_Value, self.main.FF_Friction_Value, self.main.FF_Damping_Value,
         self.main.FF_Sine_Value, self.main.FF_Spring_Value]
        self.Slider_List = [
         self.main.FF_Global_strength_Slider, self.main.FF_Response_Slider, self.main.Speed_Limit_Slider, self.main.Detail_Enhancer_Slider, self.main.FF_Filter_Slider, self.main.FF_Maxtorque_Slider,
         self.main.Mech_Spring_Slider, self.main.Mech_Friction_Slider, self.main.Mech_Damping_Slider, self.main.Mech_Inertia_Slider, self.main.Mech_Endstop_Slider,
         self.main.Dyna_Damping_Slider, self.main.Understeer_Effect_Slider,
         self.main.FF_Constant_Slider, self.main.FF_Friction_Slider, self.main.FF_Damping_Slider,
         self.main.FF_Sine_Slider, self.main.FF_Spring_Slider]
        self.port_thread = Refresher(1)
        self.port_thread.sinOut.connect(self.readSetting)
        self.port_thread.start()
        self.setConnect()

    def setConnect(self):
        """ Slider -> Value """

        def LambdaCallback1(Slider, Value):
            return lambda : Value.setText(str(Slider.value()))

        for Slider, Value in zip(self.Slider_List, self.Value_List):
            Slider.valueChanged.connect(LambdaCallback1(Slider, Value))

        self.main.FF_Maxtorque_Slider.valueChanged.connect(lambda : self.main.FF_Maxtorque_Value.setText(str(self.main.FF_Maxtorque_Slider.value() / 10)))
        self.main.Mech_Inertia_Slider.valueChanged.connect(lambda : self.main.Mech_Inertia_Value.setText(str(self.main.Mech_Inertia_Slider.value() - 100)))
        self.main.FF_Global_strength_Slider.valueChanged.connect(lambda val: self.ffbSentHandler(self.main.FF_Global_strength_Slider, SETTING_FFB_STRENGTH, val))
        self.main.FF_Global_strength_Slider.valueChanged.connect(lambda val: self.setEffsetCfg(SETTING_FFB_STRENGTH, val))
        self.main.Speed_Limit_Slider.valueChanged.connect(lambda val: self.ffbSentHandler(self.main.Speed_Limit_Slider, SETTING_FFB_SPEED_LIMIT, val))
        self.main.Speed_Limit_Slider.valueChanged.connect(lambda val: self.setEffsetCfg(SETTING_FFB_SPEED_LIMIT, val))
        self.main.FF_Response_Slider.valueChanged.connect(lambda val: self.ffbSentHandler(self.main.FF_Response_Slider, SETTING_FFB_RESPONSE, val))
        self.main.FF_Response_Slider.valueChanged.connect(lambda val: self.setEffsetCfg(SETTING_FFB_RESPONSE, val))
        self.main.FF_Filter_Slider.valueChanged.connect(lambda val: self.ffbSentHandler(self.main.FF_Filter_Slider, SETTING_FFB_FILTER, val))
        self.main.FF_Filter_Slider.valueChanged.connect(lambda val: self.setEffsetCfg(SETTING_FFB_FILTER, val))
        self.main.FF_Maxtorque_Slider.valueChanged.connect(lambda val: self.ffbSentHandler(self.main.FF_Maxtorque_Slider, SETTING_FFB_LINEARITY, val))
        self.main.FF_Maxtorque_Slider.valueChanged.connect(lambda val: self.setEffsetCfg(SETTING_FFB_LINEARITY, val))
        self.main.Detail_Enhancer_Slider.valueChanged.connect(lambda val: self.ffbSentHandler(self.main.Detail_Enhancer_Slider, SETTING_FFB_DETAIL_ENHANCER, val))
        self.main.Mech_Friction_Slider.valueChanged.connect(lambda val: self.ffbSentHandler(self.main.Mech_Friction_Slider, SETTING_MECH_FRICTION_STRENGTH, val))
        self.main.Mech_Friction_Slider.valueChanged.connect(lambda val: self.setEffsetCfg(SETTING_MECH_FRICTION_STRENGTH, val))
        self.main.Mech_Damping_Slider.valueChanged.connect(lambda val: self.ffbSentHandler(self.main.Mech_Damping_Slider, SETTING_MECH_DAMPING_STRENGTH, val))
        self.main.Mech_Damping_Slider.valueChanged.connect(lambda val: self.setEffsetCfg(SETTING_MECH_DAMPING_STRENGTH, val))
        self.main.Mech_Inertia_Slider.valueChanged.connect(lambda val: self.ffbSentHandler(self.main.Mech_Inertia_Slider, SETTING_MECH_INERTIA_STRENGTH, val))
        self.main.Mech_Inertia_Slider.valueChanged.connect(lambda val: self.setEffsetCfg(SETTING_MECH_INERTIA_STRENGTH, val))
        self.main.Mech_Endstop_Slider.valueChanged.connect(lambda val: self.ffbSentHandler(self.main.Mech_Endstop_Slider, SETTING_ENDSTOP_STRENGTH, val))
        self.main.Mech_Endstop_Slider.valueChanged.connect(lambda val: self.setEffsetCfg(SETTING_ENDSTOP_STRENGTH, val))
        self.main.Mech_Spring_Slider.valueChanged.connect(lambda val: self.ffbSentHandler(self.main.Mech_Spring_Slider, SETTING_MECH_SPRING_STRENGTH, val))
        self.main.Mech_Spring_Slider.valueChanged.connect(lambda val: self.setEffsetCfg(SETTING_MECH_SPRING_STRENGTH, val))
        self.main.FF_Constant_Slider.valueChanged.connect(lambda val: self.ffbSentHandler(self.main.FF_Constant_Slider, SETTING_FFB_CONSTANT_STRENGTH, val))
        self.main.FF_Constant_Slider.valueChanged.connect(lambda val: self.setEffsetCfg(SETTING_FFB_CONSTANT_STRENGTH, val))
        self.main.FF_Friction_Slider.valueChanged.connect(lambda val: self.ffbSentHandler(self.main.FF_Friction_Slider, SETTING_FFB_FRICTION_STRENGTH, val))
        self.main.FF_Friction_Slider.valueChanged.connect(lambda val: self.setEffsetCfg(SETTING_FFB_FRICTION_STRENGTH, val))
        self.main.FF_Damping_Slider.valueChanged.connect(lambda val: self.ffbSentHandler(self.main.FF_Damping_Slider, SETTING_FFB_DAMPING_STRENGTH, val))
        self.main.FF_Damping_Slider.valueChanged.connect(lambda val: self.setEffsetCfg(SETTING_FFB_DAMPING_STRENGTH, val))
        self.main.FF_Sine_Slider.valueChanged.connect(lambda val: self.ffbSentHandler(self.main.FF_Sine_Slider, SETTING_FFB_SINE_STRENGTH, val))
        self.main.FF_Sine_Slider.valueChanged.connect(lambda val: self.setEffsetCfg(SETTING_FFB_SINE_STRENGTH, val))
        self.main.FF_Spring_Slider.valueChanged.connect(lambda val: self.ffbSentHandler(self.main.FF_Spring_Slider, SETTING_FFB_SPRING_STRENGTH, val))
        self.main.FF_Spring_Slider.valueChanged.connect(lambda val: self.setEffsetCfg(SETTING_FFB_SPRING_STRENGTH, val))

    def simply_setting(self, val):
        if val == True:
            enable = 0
        else:
            enable = 1
        simply_cfg = configparser.ConfigParser()
        simply_cfg.read('./cfg/simply_setting.cfg')
        response = simply_cfg.get('general', 'response')
        speed_limit = simply_cfg.get('general', 'speed limit')
        filter = simply_cfg.get('general', 'filter')
        inherent_friction = simply_cfg.get('inherent feature', 'friction')
        inherent_speed_limit = simply_cfg.get('inherent feature', 'friction')
        ffb_constant = simply_cfg.get('force feedback signal', 'constant')
        ffb_friction = simply_cfg.get('force feedback signal', 'friction')
        ffb_damping = simply_cfg.get('force feedback signal', 'damping')
        ffb_inertia = simply_cfg.get('force feedback signal', 'inertia')
        ffb_sine = simply_cfg.get('force feedback signal', 'sine')
        ffb_spring = simply_cfg.get('force feedback signal', 'spring')
        ffb_ramp = simply_cfg.get('force feedback signal', 'ramp')
        ffb_square = simply_cfg.get('force feedback signal', 'square')
        ffb_sawtooth = simply_cfg.get('force feedback signal', 'sawtooth')
        ffb_triangle = simply_cfg.get('force feedback signal', 'triangle')
        val = [
         enable, response, speed_limit, filter, inherent_friction, inherent_speed_limit,
         ffb_constant, ffb_friction, ffb_damping, ffb_inertia, ffb_sine, ffb_spring, ffb_ramp, ffb_square, ffb_sawtooth, ffb_triangle]
        for i in range(len(val)):
            val[i] = int(val[i])

        self.hidchooser.sent_list_handler(SETTING_FFB_SIMPLY_SETTING, val)

    def ffbSentHandler(self, slider, cmd, val):
        self.hidchooser.sent_handler(cmd, val)

    def readEffectCfg(self):
        pass

    def setEffsetCfg(self, SETTING, val):
        pass

    def initFFBSetting(self, slider, cmd):
        self.hidchooser.sent_handler(cmd, slider.value())

    def readSetting(self):
        if self.hidchooser.usbhidDataReady() and self.hidchooser.cmd_sending == False:
            if self.hidchooser.init_base == False:
                self.initFFBSetting(self.main.FF_Global_strength_Slider, SETTING_FFB_STRENGTH)
                self.initFFBSetting(self.main.Speed_Limit_Slider, SETTING_FFB_SPEED_LIMIT)
                self.initFFBSetting(self.main.FF_Response_Slider, SETTING_FFB_RESPONSE)
                self.initFFBSetting(self.main.FF_Filter_Slider, SETTING_FFB_FILTER)
                self.initFFBSetting(self.main.FF_Maxtorque_Slider, SETTING_FFB_LINEARITY)
                self.initFFBSetting(self.main.Detail_Enhancer_Slider, SETTING_FFB_DETAIL_ENHANCER)
                self.initFFBSetting(self.main.base_angle_range_Slider, SETTING_SET_RANGE)
                self.hidchooser.sent_handler(SETTING_SYNA_LOCK, 1)
                self.initFFBSetting(self.main.Mech_Friction_Slider, SETTING_MECH_FRICTION_STRENGTH)
                self.initFFBSetting(self.main.Mech_Damping_Slider, SETTING_MECH_DAMPING_STRENGTH)
                self.initFFBSetting(self.main.Mech_Inertia_Slider, SETTING_MECH_INERTIA_STRENGTH)
                self.initFFBSetting(self.main.Mech_Spring_Slider, SETTING_MECH_SPRING_STRENGTH)
                self.initFFBSetting(self.main.Dyna_Damping_Slider, SETTING_DYNA_DAMPING)
                self.initFFBSetting(self.main.FF_Constant_Slider, SETTING_FFB_CONSTANT_STRENGTH)
                self.initFFBSetting(self.main.FF_Friction_Slider, SETTING_FFB_FRICTION_STRENGTH)
                self.initFFBSetting(self.main.FF_Damping_Slider, SETTING_FFB_DAMPING_STRENGTH)
                self.initFFBSetting(self.main.FF_Sine_Slider, SETTING_FFB_SINE_STRENGTH)
                self.initFFBSetting(self.main.FF_Spring_Slider, SETTING_FFB_SPRING_STRENGTH)
                self.hidchooser.init_base = True
            else:
                global_strength = self.hidchooser.ffb_global_strength
                response = self.hidchooser.ffb_response
                speed_limit = self.hidchooser.speed_limit
                detail_enhancer = self.hidchooser.ffb_detail_enhancer
                force_filter = self.hidchooser.ffb_filter
                maxtorque = self.hidchooser.ffb_maxtorque
                affect_deadband = 0
                base_featrue_spring = self.hidchooser.mech_spring_strength
                base_featrue_friction = self.hidchooser.mech_friction_strength
                base_featrue_damping = self.hidchooser.mech_damping_strength
                base_featrue_inertia = self.hidchooser.mech_inertia_strength
                base_featrue_endstop_strength = self.hidchooser.mech_endstop_strength
                dyna_damping = self.hidchooser.dyna_damping_strength
                dyna_threshold = self.hidchooser.dyna_threshold
                dyna_range = self.hidchooser.dyna_range
                ff_constant = self.hidchooser.ffb_constant_strength
                ff_friction = self.hidchooser.ffb_friction_strength
                ff_damping = self.hidchooser.ffb_damping_strength
                ff_inertia = self.hidchooser.ffb_inertia_strength
                ff_sine = self.hidchooser.ffb_sine_strength
                ff_spring = self.hidchooser.ffb_spring_strength
                ff_ramp = self.hidchooser.ffb_ramp_strength
                ff_square = self.hidchooser.ffb_square_strength
                ff_sawtooth = self.hidchooser.ffb_sawtooth_strength
                ff_triangle = self.hidchooser.ffb_triangle_strength
                ff_friction_filter = self.hidchooser.ffb_friction_filter_strength
                ff_damping_filter = self.hidchooser.ffb_damping_filter_strength
                ff_inertia_filter = self.hidchooser.ffb_inertia_filter_strength
                setting_value_list = [
                 global_strength, response, speed_limit, detail_enhancer, force_filter, maxtorque,
                 base_featrue_spring, base_featrue_friction, base_featrue_damping, base_featrue_inertia, base_featrue_endstop_strength,
                 dyna_damping, dyna_threshold,
                 ff_constant, ff_friction, ff_damping, ff_sine, ff_spring,
                 ff_friction_filter, ff_damping_filter, ff_inertia_filter]
                for Slider, Value, setting_value in zip(self.Slider_List, self.Value_List, setting_value_list):
                    if not Slider == self.main.Dyna_Damping_Slider:
                        if Slider == self.main.Understeer_Effect_Slider:
                            pass
                        else:
                            Slider.setValue(setting_value)

                try:
                    ch = ch_list.index(int(self.hidchooser.wireless_ch)) + 1
                    self.main.CH_label.setText('CH : ' + str(ch))
                except Exception as e:
                    print('self.main.CH_label.setText  error', self.hidchooser.wireless_ch)

                self.main.FF_Constant_Label.setEnabled(self.hidchooser.ffb_constant_active)
                self.main.FF_Friction_Label.setEnabled(self.hidchooser.ffb_friction_active)
                self.main.FF_Damping_Label.setEnabled(self.hidchooser.ffb_damping_active)
                self.main.FF_Sine_Label.setEnabled(self.hidchooser.ffb_sine_active)
                self.main.FF_Spring_Label.setEnabled(self.hidchooser.ffb_spring_active)
