import RPi.GPIO as GPIO
import time
import numpy as np
from client_utils.others import wait_for_static

# utr_TRIG = 11  # 超声波模块Tring控制管脚
# utr_ECHO = 35  # 超声波模块Echo控制管脚
utr_TRIG = 20  # 超声波模块Tring控制管脚
utr_ECHO = 19  # 超声波模块Echo控制管脚

GPIO.setmode(GPIO.BCM)
GPIO.setup(utr_TRIG, GPIO.OUT)  # Tring设置为输出模式
GPIO.setup(utr_ECHO, GPIO.IN)  # Echo设置为输入模式


# 超声波计算距离函数


def ur_disMeasure():
    GPIO.output(utr_TRIG, 0)  # 开始起始
    time.sleep(0.000002)  # 延时2us

    GPIO.output(utr_TRIG, 1)  # 超声波启动信号，延时10us
    time.sleep(0.00001)  # 发出超声波脉冲
    GPIO.output(utr_TRIG, 0)  # 设置为低电平

    cont_start = 0
    while GPIO.input(utr_ECHO) == 0 and cont_start < 100000:  # 等待回传信号
        cont_start += 1
    us_time1 = time.time()  # 获取当前时间
    cont_end = 0
    while GPIO.input(utr_ECHO) == 1 and cont_end < 100000:  # 回传信号截止信息
        cont_end += 1
    us_time2 = time.time()  # 获取当前时间
    if cont_end == 100000 or cont_start == 100000:
        print("ultrasound error!")
    us_during = us_time2 - us_time1  # 转换微秒级的时间

    # 声速在空气中的传播速度为340m/s, 超声波要经历一个发送信号和一个回波信息，
    # 计算公式如下所示：
    return us_during * 340 / 2 * 100  # 求出距离


def get_dist():
    np.mean([ur_disMeasure() for _ in range(0, 5)])
    res = np.mean([ur_disMeasure() for _ in range(0, 10) if time.sleep(0.1) is None])
    wait_for_static(1)
    return res


# 程序入口
if __name__ == "__main__":
    tt = 0
    while tt < 100000:
        tt += 1
        print(get_dist(), "cm")  # 调用循环函数
    GPIO.cleanup()  # 释放资源
