from datetime import datetime
from ctypes import cdll,c_long, c_ulong, c_uint32,byref,create_string_buffer,c_bool,c_char_p,c_int,c_int16,c_double, sizeof, c_voidp
from TLPM import *
import time
import numpy as np
#getWavelength
#setWavelength

tlPM = TLPM()
deviceCount = c_uint32()
tlPM.findRsrc(byref(deviceCount))

print("devices found: " + str(deviceCount.value))

resourceName = create_string_buffer(1024)

for i in range(0, deviceCount.value):
    tlPM.getRsrcName(c_int(i), resourceName)
    print(c_char_p(resourceName.raw).value)
    break

tlPM.close()

tlPM = TLPM()
#resourceName = create_string_buffer(b"COM1::115200")
#print(c_char_p(resourceName.raw).value)
tlPM.open(resourceName, c_bool(True), c_bool(True))

message = create_string_buffer(1024)
tlPM.getCalibrationMsg(message)
print(c_char_p(message.raw).value)

time.sleep(5)

waveLength = c_double()
tlPM.getWavelength(TLPM_ATTR_SET_VAL, byref(waveLength))
print(waveLength.value)

waveLength = c_double(500)
ret = tlPM.setWavelength(waveLength)
print(ret)
waveLength = c_double()
tlPM.getWavelength(TLPM_ATTR_SET_VAL, byref(waveLength))
print(waveLength.value)

power_measurements = []
times = []
count = 0
while count < 20:
    power =  c_double()
    tlPM.measPower(byref(power))
    power_measurements.append(power.value)
    times.append(datetime.now())
    print(power.value)
    print(type(power.value))
    count+=1
    time.sleep(1)

mean_value = np.mean(power_measurements)
print(float(mean_value))
print(type(float(mean_value)))

tlPM.close()
print('End program')
