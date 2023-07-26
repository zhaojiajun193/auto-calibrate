import serial
import serial.tools.list_ports
from loguru import logger
from configs import settings

ports_list = list(serial.tools.list_ports.comports())
if len(ports_list) <= 0:
    logger.debug("无串口设备 请连接")
else:
    logger.debug("可用串口设备如下")
    for comport in ports_list:
        print(list(comport)[0], list(comport)[1])
        print(type(list(comport)), list(comport))


ser = serial.Serial(port="COM1", baudrate=9600, timeout=1)
if ser.isOpen():
    logger.debug("串口打开成功")
else:
    logger.debug("串口打开失败")

s = "hello world"
hex_str = s.encode().hex()
print(hex_str)
print(type(hex_str))
data = bytes.fromhex(hex_str)
print(data)
ser.write(b'hello world')

logger.debug(settings.Serial.baud_rate)
logger.debug(type(settings.Serial.baud_rate))