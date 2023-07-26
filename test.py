import binascii
import serial
from test import MonochromatorTest
from loguru import logger
from configs import settings
from time import sleep
def main():
    monochromator_test = MonochromatorTest(settings.Serial.com, settings.Serial.baud_rate)
    monochromator_test.test_init_monichromator()
    monochromator_test.test_start_set_process()
    monochromator_test.test_enable_auto_filter_switch()
    monochromator_test.test_finish_set_process()
    monochromator_test.test_start_parameter_query_process()
    monochromator_test.test_query_system_parameter()
    monochromator_test.test_query_raster_parameter(1)
    monochromator_test.test_query_raster_parameter(2)
    monochromator_test.test_query_raster_parameter(3)
    monochromator_test.test_finish_parameter_query_process()
    # monochromator_test.test_switch_raster(1)
    # monochromator_test.test_switch_raster(2)
    # monochromator_test.test_switch_raster(3)
    now_raster = monochromator_test.test_query_now_raster()
    logger.debug(now_raster)
    start_wavelength = settings.Monochromator.start_wave_length
    end_wavelength = settings.Monochromator.end_wave_length
    step = settings.Monochromator.step
    while start_wavelength <= end_wavelength:
        monochromator_test.test_move_to_destWaveLength(start_wavelength)
        start_wavelength += step
        sleep(2)


if __name__=='__main__':
    main()
# message = "hello"
# end = b"\x0D"
# hex_message = binascii.hexlify(message.encode())
# print(hex_message)
# print(type(hex_message))
# hex_message = hex_message + b'0d'
# print(type(hex_message))
# print(hex_message)