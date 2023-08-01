from .TLPM import *
from ctypes import cdll,c_long, c_ulong, c_uint32,byref,create_string_buffer,c_bool,c_char_p,c_int,c_int16,c_double, sizeof, c_voidp
from datetime import datetime
import time
from loguru import logger
import sys
import numpy as np

class Dynamometer:
    def __init__(self) -> None:
        tlPM = TLPM()
        self.deviceCount = c_uint32()
        tlPM.findRsrc(byref(self.deviceCount))
        logger.debug("device found " + str(self.deviceCount.value))
        resourceName = create_string_buffer(1024)
        for i in range(0, self.deviceCount.value):
            tlPM.getRsrcName(c_int(i), resourceName)
            print(c_char_p(resourceName.raw).value)
            break
        tlPM.close()
        self.tlPM = TLPM()
        self.tlPM.open(resourceName, c_bool(True), c_bool(True))
        message = create_string_buffer(1024)
        self.tlPM.getCalibrationMsg(message)
        print(c_char_p(message.raw).value)
        time.sleep(5)

    def set_waveLength(self, waveLength):
        ret = self.tlPM.setWavelength(waveLength)
        if ret == 0:
            logger.debug("set waveLength success !")
        else:
            logger.error("set waveLength fail !")
            sys.exit(1)
    
    def get_waveLength(self):
        waveLength = c_double()
        self.tlPM.getWavelength(TLPM_ATTR_SET_VAL, byref(waveLength))
        return waveLength.value
    
    def get_power(self):
        power_measurements = []
        # times = []
        count = 0
        while count < 20:
            power =  c_double()
            self.tlPM.measPower(byref(power))
            power_measurements.append(power.value)
            # times.append(datetime.now())
            logger.debug(power.value)
            count+=1
            time.sleep(1)

        return float(np.mean(power_measurements))
    
    def close_dynamometer(self):
        self.tlPM.close()
