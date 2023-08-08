import smbus  # import SMBus module of I2C
from time import sleep  # import sleep
import numpy as np

# some MPU6050 Registers and their Address
Register_A = 0  # Address of Configuration register A
Register_B = 0x01  # Address of configuration register B
Register_mode = 0x02  # Address of mode register

X_axis_H = 0x03  # Address of X-axis MSB data register
Z_axis_H = 0x05  # Address of Z-axis MSB data register
Y_axis_H = 0x07  # Address of Y-axis MSB data register
declination = -0.00669  # define declination angle of location where measurement going to be done
pi = 3.14159265359  # define pi value

x_min, x_max = -637, -373
y_min, y_max = -352, -130
z_min, z_max = -121, -87


def Magnetometer_Init():
    # write to Configuration Register A
    bus.write_byte_data(Device_Address, Register_A, 0x70)

    # Write to Configuration Register B for gain
    bus.write_byte_data(Device_Address, Register_B, 0xa0)

    # Write to mode Register for selecting mode
    bus.write_byte_data(Device_Address, Register_mode, 0)


def read_raw_data(addr):
    # Read raw 16-bit value
    high = bus.read_byte_data(Device_Address, addr)
    low = bus.read_byte_data(Device_Address, addr + 1)

    # concatenate higher and lower value
    value = ((high << 8) | low)

    # to get signed value from module
    if value > 32768:
        value = value - 65536
    return value


bus = smbus.SMBus(1)  # or bus = smbus.SMBus(0) for older version boards
Device_Address = 0x1e  # HMC5883L magnetometer device address

Magnetometer_Init()  # initialize HMC5883L magnetometer


def get_body_direct(use_rad=False):
    x = read_raw_data(X_axis_H)
    z = read_raw_data(Z_axis_H)
    y = read_raw_data(Y_axis_H)
    x_cali = (x - (x_min + x_max) / 2) / (x_max - x_min)
    y_cali = (y - (y_min + y_max) / 2) / (y_max - y_min)
    z_cali = (z - (z_min + z_max) / 2) / (z_max - z_min)
    if x_cali == 0:
        x_cali = 0.0001
    deg = np.rad2deg(np.arctan(y_cali / x_cali))
    if y_cali > 0 and x_cali < 0:
        deg = deg + 180
    elif y_cali < 0 and x_cali < 0:
        deg = deg - 180
    # print(x, y, z)
    print(x, y, z, x_cali, y_cali, z_cali, deg)
    if use_rad:
        return np.deg2rad(deg)
    else:
        return deg


if __name__ == '__main__':
    while True:
        # Read Accelerometer raw value
        print(get_body_direct(True))
        sleep(1)
