import binascii
import serial
from test import MonochromatorTest, HikCameraTest, DynamometerTest
from loguru import logger
from configs import settings
from time import sleep
import os
import cv2
from utils import ImageUtils
from ctypes import c_double
from saver import Saver
def main_camera():
    base_path = "./image"
    if not os.path.exists(base_path):
        os.makedirs(base_path)
    hikCameraTest = HikCameraTest()
    sleep(5)
    hikCameraTest.test_set_exposure_time(100)
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
        logger.debug(start_wavelength)
        image_savedir = os.path.join(base_path, str(start_wavelength))
        if not os.path.exists(image_savedir):
            os.makedirs(image_savedir)
        monochromator_test.test_move_to_destWaveLength(start_wavelength)
        hikCameraTest.test_auto_exposure_adjustment(settings.Camera.means_min, settings.Camera.means_max)
        image = hikCameraTest.test_get_one_image()
        ret, exposure_time = hikCameraTest.test_get_exposure_time()
        cv2.imwrite(os.path.join(image_savedir, str(int(exposure_time)) + ".bmp"), image)
        ImageUtils.save_monoimage_hist(image, image_savedir)
        start_wavelength += step
        sleep(2)
    hikCameraTest.test_stop_grabing()
    hikCameraTest.test_close_camera()

def main_dynamometer():
    #功率计测试
    dynamometerTest = DynamometerTest()
    power = dynamometerTest.test_get_power()
    logger.debug("power is " + str(power))
    dynamometerTest.test_set_waveLength(c_double(500))
    waveLength = dynamometerTest.test_get_waveLength()
    logger.debug("now waveLength is " + str(waveLength))
    #单色仪
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
    #逻辑
    now_raster = monochromator_test.test_query_now_raster()
    logger.debug(now_raster)
    start_wavelength = settings.Monochromator.start_wave_length
    end_wavelength = settings.Monochromator.end_wave_length
    step = settings.Monochromator.step
    waveLength_power_dict = {}
    while start_wavelength <= end_wavelength:
        logger.debug(start_wavelength)
        monochromator_test.test_move_to_destWaveLength(start_wavelength)
        dynamometerTest.test_set_waveLength(c_double(start_wavelength))
        now_dynamometer_waveLength = dynamometerTest.test_get_waveLength()
        logger.debug("now dynamometer waveLength is " + str(now_dynamometer_waveLength))
        power = dynamometerTest.test_get_power()
        logger.debug("now power is " + str(power))
        waveLength_power_dict[str(start_wavelength)] = power
        start_wavelength += step
        sleep(2)
    dynamometerTest.test_close_dynamometer()
    power_path = './power'
    if not os.path.exists(power_path):
        os.makedirs(power_path)
    dict_saver = Saver()
    dict_saver.save_power(waveLength_power_dict, os.path.join(power_path, "result.xlsx"))

def main_together():
    #功率计测试
    dynamometerTest = DynamometerTest()
    power = dynamometerTest.test_get_power()
    logger.debug("power is " + str(power))
    dynamometerTest.test_set_waveLength(c_double(500))
    waveLength = dynamometerTest.test_get_waveLength()
    logger.debug("now waveLength is " + str(waveLength))

    base_path = "./image"
    if not os.path.exists(base_path):
        os.makedirs(base_path)
    hikCameraTest = HikCameraTest()
    sleep(5)
    hikCameraTest.test_set_exposure_time(100)
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
    waveLength_power_dict = {}
    while start_wavelength <= end_wavelength:
        logger.debug(start_wavelength)
        image_savedir = os.path.join(base_path, str(start_wavelength))
        if not os.path.exists(image_savedir):
            os.makedirs(image_savedir)
        monochromator_test.test_move_to_destWaveLength(start_wavelength)
        hikCameraTest.test_auto_exposure_adjustment(settings.Camera.means_min, settings.Camera.means_max)
        image = hikCameraTest.test_get_one_image()
        ret, exposure_time = hikCameraTest.test_get_exposure_time()
        cv2.imwrite(os.path.join(image_savedir, str(int(exposure_time)) + ".bmp"), image)
        ImageUtils.save_monoimage_hist(image, image_savedir)
        dynamometerTest.test_set_waveLength(c_double(start_wavelength))
        now_dynamometer_waveLength = dynamometerTest.test_get_waveLength()
        logger.debug("now dynamometer waveLength is " + str(now_dynamometer_waveLength))
        power = dynamometerTest.test_get_power()
        logger.debug("now power is " + str(power))
        waveLength_power_dict[str(start_wavelength)] = power
        start_wavelength += step
        sleep(2)
    hikCameraTest.test_stop_grabing()
    hikCameraTest.test_close_camera()
    dynamometerTest.test_close_dynamometer()
    power_path = './power'
    if not os.path.exists(power_path):
        os.makedirs(power_path)
    dict_saver = Saver()
    dict_saver.save_power(waveLength_power_dict, os.path.join(power_path, "result.xlsx"))

def main_2():
    hikCameraTest = HikCameraTest()
    base_path = './image'
    if not os.path.exists(base_path):
        os.makedirs(base_path)
    image = hikCameraTest.test_get_one_image()
    assert image is not None, "image should not be None"
    cv2.imwrite("./1.bmp", image)
    ImageUtils.save_monoimage_hist(image, "./")
    image_mean = ImageUtils.get_monoimage_histmean(image)
    logger.debug(image_mean)
    ret, exposure_time = hikCameraTest.test_get_exposure_time()
    logger.debug(str(ret) + str(exposure_time))
    ret = hikCameraTest.test_set_exposure_time(100)
    logger.debug(ret)
    hikCameraTest.test_stop_grabing()
    hikCameraTest.test_close_camera()

def main_3():
    hikCameraTest = HikCameraTest()
    base_path = './image'
    if not os.path.exists(base_path):
        os.makedirs(base_path)
    i = 0
    while True:
        i += 1
        image = hikCameraTest.test_get_one_image()
        cv2.imshow("test", image)
        cv2.waitKey(1)
        image_mean = ImageUtils.get_monoimage_histmean(image)
        if image_mean >= 50 and image_mean <= 100:
            image_save_path = os.path.join(base_path, str(i))
            if not os.path.exists(image_save_path):
                os.makedirs(image_save_path)
            cv2.imwrite(os.path.join(image_save_path, "1.bmp"), image)
            ImageUtils.save_monoimage_hist(image, image_save_path)
        else:
            if image_mean < 50:
                gain = float(75 / image_mean)
                logger.debug(type(gain))
                ret, now_exposure_time = hikCameraTest.test_get_exposure_time()
                logger.debug(type(now_exposure_time))
                want_exposure_time = gain * now_exposure_time
                want_exposure_time = int(want_exposure_time)
                logger.debug(want_exposure_time)
                hikCameraTest.test_set_exposure_time(want_exposure_time)
            else:
                gain = float(75 / image_mean)
                ret, now_exposure_time = hikCameraTest.test_get_exposure_time()
                want_exposure_time = gain * now_exposure_time
                want_exposure_time = int(want_exposure_time)
                logger.debug(want_exposure_time)
                hikCameraTest.test_set_exposure_time(want_exposure_time)

def main_4():
    hikCameraTest = HikCameraTest()
    hikCameraTest.test_set_exposure_time(100)
    sleep(5)
    while True:
        image = hikCameraTest.test_get_one_image()
        # width = int(image.shape[1] / 4)
        # height = int(image.shape[0] / 4)
        # logger.debug(str(width) + " " + str(height))
        # image = cv2.resize(image, (width, height))
        # cv2.imshow("test", image)
        # cv2.waitKey(1)
        hikCameraTest.test_auto_exposure_adjustment(50, 100)
if __name__=='__main__':
    main_dynamometer()
# message = "hello"
# end = b"\x0D"
# hex_message = binascii.hexlify(message.encode())
# print(hex_message)
# print(type(hex_message))
# hex_message = hex_message + b'0d'
# print(type(hex_message))
# print(hex_message)