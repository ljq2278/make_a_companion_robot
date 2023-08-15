# import smbus  # 导入I2C的SMBus模块
# from time import sleep  # 导入延时函数
#
# # 一些MPU6050寄存器及其地址
# PWR_MGMT_1 = 0x6B
# SMPLRT_DIV = 0x19
# CONFIG = 0x1A
# GYRO_CONFIG = 0x1B
# INT_ENABLE = 0x38
# ACCEL_XOUT_H = 0x3B
# ACCEL_YOUT_H = 0x3D
# ACCEL_ZOUT_H = 0x3F
# GYRO_XOUT_H = 0x43
# GYRO_YOUT_H = 0x45
# GYRO_ZOUT_H = 0x47
#
# makerobo_bus = smbus.SMBus(1)  # 或bus = smbus.SMBus(0)用于较老的版本板
# makerobo_Device_Address = 0x68  # MPU6050设备地址
#
# bias_Gx = -0.67
# bias_Gy = -0.21
# bias_Gz = 0.03
# bias_Ax = 0.10
# bias_Ay = 0.04
# bias_Az = 0.10
#
#
# # MPU 6050 初始化工作
# def makerobo_MPU_Init():
#     # 写入抽样速率寄存器
#     makerobo_bus.write_byte_data(makerobo_Device_Address, SMPLRT_DIV, 7)
#
#     # 写入电源管理寄存器
#     makerobo_bus.write_byte_data(makerobo_Device_Address, PWR_MGMT_1, 1)
#
#     # 写入配置寄存器
#     makerobo_bus.write_byte_data(makerobo_Device_Address, CONFIG, 0)
#
#     # 写入陀螺配置寄存器
#     makerobo_bus.write_byte_data(makerobo_Device_Address, GYRO_CONFIG, 24)
#
#     # 写中断使能寄存器
#     makerobo_bus.write_byte_data(makerobo_Device_Address, INT_ENABLE, 1)
#
#
# # 读取MPU6050数据寄存器
# def makerobo_read_raw_data(addr):
#     # 加速度值和陀螺值为16位
#     high = makerobo_bus.read_byte_data(makerobo_Device_Address, addr)
#     low = makerobo_bus.read_byte_data(makerobo_Device_Address, addr + 1)
#
#     # 连接更高和更低的值
#     value = ((high << 8) | low)
#
#     # 从mpu6050获取有符号值
#     if value > 32768:
#         value = value - 65536
#     return value
#
#
# def get_posture():
#     # 读取加速度计原始值
#     acc_x = makerobo_read_raw_data(ACCEL_XOUT_H)
#     acc_y = makerobo_read_raw_data(ACCEL_YOUT_H)
#     acc_z = makerobo_read_raw_data(ACCEL_ZOUT_H)
#
#     # 读陀螺仪原始值
#     gyro_x = makerobo_read_raw_data(GYRO_XOUT_H)
#     gyro_y = makerobo_read_raw_data(GYRO_YOUT_H)
#     gyro_z = makerobo_read_raw_data(GYRO_ZOUT_H)
#
#     # 全刻度范围+/- 250度/℃，根据灵敏度刻度系数
#     Ax = acc_x / 16384.0 - bias_Ax
#     Ay = acc_y / 16384.0 - bias_Ay
#     Az = acc_z / 16384.0 - bias_Az
#
#     Gx = gyro_x / 131.0 - bias_Gx
#     Gy = gyro_y / 131.0 - bias_Gy
#     Gz = gyro_z / 131.0 - bias_Gz
#
#     # 打印出MPU相关信息
#     print("Gx=%.2f" % Gx, u'\u00b0' + "/s", "\tGy=%.2f" % Gy, u'\u00b0' + "/s", "\tGz=%.2f" % Gz, u'\u00b0' + "/s", "\tAx=%.2f g" % Ax, "\tAy=%.2f g" % Ay, "\tAz=%.2f g" % Az)
#     return Gx, Gy, Gz, Ax, Ay, Az
#
#
# makerobo_MPU_Init()  # 初始化MPU6050
#
# if __name__ == '__main__':
#     while True:
#         get_posture()
#         sleep(0.1)



import time
import board
import adafruit_mpu6050
import numpy as np

i2c = board.I2C()  # uses board.SCL and board.SDA
# i2c = board.STEMMA_I2C()  # For using the built-in STEMMA QT connector on a microcontroller
mpu = adafruit_mpu6050.MPU6050(i2c)

bias_Gx = -0.0
bias_Gy = -0.21
bias_Gz = 0.12
bias_Ax = 0.7
bias_Ay = 0.45
bias_Az = 10.6


def get_posture():
    gyro = mpu.gyro
    # acceleration = np.mean([np.array(mpu.acceleration) for _ in range(0,10)], axis=0)
    acceleration = mpu.acceleration
    return gyro[0] - bias_Gx, gyro[1] - bias_Gy, gyro[2] - bias_Gz, acceleration[0] - bias_Ax, acceleration[1] - bias_Ay, acceleration[2] - bias_Az


if __name__ == '__main__':
    while True:
        res = get_posture()
        print("Gyro X:%.2f, Y: %.2f, Z: %.2f rad/s" % (res[0],res[1],res[2]))
        print("Acceleration: X:%.2f, Y: %.2f, Z: %.2f m/s^2" % (res[3],res[4],res[5]))
        print("Temperature: %.2f C" % mpu.temperature)
        print("")
        time.sleep(0.1)
