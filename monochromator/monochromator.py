import serial
from loguru import logger
import binascii
import sys
import math

class Monochromator:
    def __init__(self, com: str, baud_rate:int):
        self.com: str = com
        self.baud_rate: int = baud_rate
        self.raster_dict = {}
        self.ser = serial.Serial(port=self.com, baudrate=self.baud_rate, timeout=1)
        if self.ser.isOpen():
            logger.debug("串口开启成功")
        else:
            logger.debug("串口打开失败")

    def init_monichromator(self):
        #联络指令
        message = b"?"
        # message = binascii.hexlify(message.encode())
        message = message + b'\r'
        logger.debug(message)
        self.ser.write(message)
        result = self.ser.readline()
        result = str(result, 'utf-8')
        result = result.splitlines()
        logger.debug(result)
        if result[-1] == 'OK':
            logger.debug('单色仪初始化成功')
        else:
            logger.error('单色仪初始化失败')
            sys.exit(1)

    #开启设置进程
    def start_set_process(self):
        message = b"S"
        # message = binascii.hexlify(message.encode())
        message = message + b'\r'
        self.ser.write(message)
        result = self.ser.readline()
        result = str(result, 'utf-8')
        result = result.splitlines()
        logger.debug(result)
        if result[-1] == 'OK':
            logger.debug("单色仪开启设置进程成功")
        else:
            logger.error("单色仪设置进程开启失败")
            sys.exit(1)

    #设置完成指令
    def finish_set_process(self):
        message = b"E01"
        # message = binascii.hexlify(message.encode())
        message = message + b'\r'
        self.ser.write(message)
        result = self.ser.readline()
        result = str(result, 'utf-8')
        result = result.splitlines()
        logger.debug(result)
        if result[-1] == 'OK':
            logger.debug("单色仪关闭设置进程成功")
        else:
            logger.error('单色仪关闭设置进程失败')
            sys.exit(1)
    
    #开启滤光片自动切换功能
    def enable_auto_filter_switch(self):
        message = b"f1"
        # message = binascii.hexlify(message.encode())
        message = message + b'\r'
        self.ser.write(message)
        result = self.ser.readline()
        result = str(result, 'utf-8')
        result = result.splitlines()
        logger.debug(result)
        if result[-1] == 'OK':
            logger.debug('单色仪开启滤光片自动切换成功')
        else:
            logger.error('单色仪开启滤光片自动切换失败')
            sys.exit(1)

    #开启参数查询进程
    def start_parameter_query_process(self):
        message = b"Q"
        message = message + b'\r'
        self.ser.write(message)
        result = self.ser.readline()
        result = str(result, 'utf-8')
        result = result.splitlines()
        logger.debug(result)
        if result[-1] == 'OK':
            logger.debug('单色仪开启参数查询进程成功')
        else:
            logger.error("单色仪开启参数查询进程失败")
            sys.exit(1)
    
    #查询系统参数，返回仪器编号、仪器可使用最大光栅数、仪器总步数、光栅台号
    def query_system_parameter(self):
        message = b'L'
        message = message + b'\r'
        self.ser.write(message)
        result = self.ser.readline()
        result = str(result, 'utf-8')
        result = result.splitlines()
        logger.debug(result)
        if result[-1] == 'OK':
            logger.debug('查询系统参数成功')
            self.system_number = result[0]
            #可用光栅数
            self.rasters_number = int(result[1])
            self.total_steps = int(result[2])
        else:
            logger.error("查询系统参数失败")
            sys.exit(1)

    #查询光栅参数 区分1 2 3 使用字典保存对应光栅参数信息
    def query_raster_parameter(self, raster_number):
        message = b"T0"
        message = message + str(raster_number).encode('utf-8') + b'\r'
        self.ser.write(message)
        result = self.ser.readline()
        result = str(result, 'utf-8')
        result = result.splitlines()
        logger.debug(result)
        if result[-1] == 'OK':
            logger.debug("查询光栅" + str(raster_number) + "参数成功")
            self.raster_dict[str(raster_number)] = {
                "data_z":int(result[0]),
                "data_c":int(result[1])/1000,
                "data_L":int(result[2]),
                "data_b":int(result[3])
            }
        else:
            logger.error("查询光栅" + str(raster_number) + "参数失败")
            sys.exit(1)

    def finish_parameter_query_process(self):
        message = b"E"
        message = message + b'\r'
        self.ser.write(message)
        result = self.ser.readline()
        result = str(result, 'utf-8')
        result = result.splitlines()
        logger.debug(result)
        if result[-1] == 'OK':
            logger.debug("单色仪关闭参数查询进程成功")
        else:
            logger.error("单色仪关闭参数查询进程失败")
            sys.exit(1)

    def switch_raster(self, raster_number):
        message = b'G'
        message = message + str(raster_number).encode('utf-8') + b'\r'
        self.ser.write(message)
        logger.debug("单色仪开始移动到" + str(raster_number) + "号光栅")
        while True:
            result = self.ser.readline()
            logger.debug(result)
            result = str(result, 'utf-8')
            result = result.splitlines()
            if len(result) > 0 and result[-1].endswith('OK'):
                logger.debug(result)
                break
        logger.debug('单色仪已经移动到' + str(raster_number) + '号光栅')

    def query_now_raster(self):
        message = b'g'
        message = message + b'\r'
        self.ser.write(message)
        result = self.ser.readline()
        logger.debug(result)
        result = str(result, 'utf-8')
        result = result.splitlines()
        logger.debug(result)
        if result[-1] == 'OK':
            logger.debug("查询当前光栅号成功")
            return int(result[0])
        else:
            logger.error("查询当前光栅号失败")
            return 0
    
    def move_to_destStep(self, step):
        message = b'B'
        message = message + str(step).encode("utf-8") + b'\r'
        self.ser.write(message)
        logger.debug('光谱仪开始移动到' + str(step))
        while True:
            result = self.ser.readline()
            logger.debug(result)
            result = str(result, 'utf-8')
            result = result.splitlines()
            logger.debug(result)
            if len(result) > 0 and result[-1].endswith('OK'):
                logger.debug(result)
                break
        logger.debug('光谱仪移动到' + str(step))

    def move_to_destWaveLength(self, wave_length):
        #依次对应于想要的波长、光栅矫正系数、仪器总步数、光栅零点位置
        def calculate_step(waveLength, data_c, steps_total, raster_zero_locate):
            #光栅台的转角
            raster_corner = math.atan(waveLength/(math.sqrt(data_c*data_c - waveLength*waveLength)))
            if raster_corner < 0:
                return steps_total + (0.5*raster_corner*steps_total)/math.pi + raster_zero_locate
            else:
                return (0.5*raster_corner*steps_total)/math.pi + raster_zero_locate
        raster_num = 0
        if wave_length < 200 or wave_length > 2200:
            logger.error("不支持的波长")
            sys.exit(1)
        if wave_length >= 200 and wave_length < 400:
            raster_num = 1
        elif wave_length >= 400 and wave_length < 1000:
            raster_num = 2
        elif wave_length >= 1000 and wave_length <= 2200:
            raster_num = 3
        now_raster_num = self.query_now_raster()
        if now_raster_num == raster_num:
            logger.debug("光栅无需移动，当前光栅号为" + str(raster_num))
            position = calculate_step(wave_length, self.raster_dict[str(raster_num)]['data_c'], self.total_steps, self.raster_dict[str(raster_num)]['data_z'])
            logger.debug(position)
            self.move_to_destStep(int(position))
            logger.debug('当前波长为' + str(wave_length))
        else:
            self.switch_raster(raster_num)
            position = calculate_step(wave_length, self.raster_dict[str(raster_num)]['data_c'], self.total_steps, self.raster_dict[str(raster_num)]['data_z'])
            logger.debug(position)
            self.move_to_destStep(int(position))
            logger.debug('当前波长为' + str(wave_length))