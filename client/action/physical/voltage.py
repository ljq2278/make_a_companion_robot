import smbus
# import time

bus = smbus.SMBus(1)
pcf8591_addr = 0x48
voltage_ch = 0


# 读取模拟量信息
def read(chn):  # 通道选择，范围是0-3之间
    try:
        if chn == 0:
            bus.write_byte(pcf8591_addr, 0x40)
        if chn == 1:
            bus.write_byte(pcf8591_addr, 0x41)
        if chn == 2:
            bus.write_byte(pcf8591_addr, 0x42)
        if chn == 3:
            bus.write_byte(pcf8591_addr, 0x43)
        bus.read_byte(pcf8591_addr)  # 开始进行读取转换
    except Exception as e:
        print("Address: %s" % pcf8591_addr)
        print(e)
    return bus.read_byte(pcf8591_addr)


def get_voltage():
    total_v = 0
    measure_time = 100
    for i in range(0, measure_time):
        total_v += read(voltage_ch)
    return total_v / measure_time / 10


def test():
    while True:
        print(read(voltage_ch))
        # time.sleep(0.000001)


# 程序入口
if __name__ == '__main__':
    # test()
    print(get_voltage())
