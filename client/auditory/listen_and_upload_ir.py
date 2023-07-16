#!/usr/bin/python3

import pylirc
import time
import RPi.GPIO as GPIO
import os
import sounddevice as sd
import numpy as np
import requests
import time as tm
import wave
import soundfile as sf
from DFRobot_DF2301Q import *

DF2301Q = DFRobot_DF2301Q_I2C(i2c_addr=DF2301Q_I2C_ADDR, bus=1)

# Constants
SERVER_URL = "http://192.168.1.8:8003/auditory/"
SILENCE_THRESHOLD = 0.1
SILENCE_TIME = 3.0
START_FILE = "wake_signal.txt"
STOP_FILE = "over_signal.txt"
RECORD_FILE = "record.wav"
# SAMPLE_RATE = 16000
SAMPLE_RATE = 16000
SUB_TYPE = "PCM_16"
CHANNELS = 2
DEVICE = 2

sd.default.samplerate = SAMPLE_RATE
sd.default.device = DEVICE

# Store the last modification times
f = open(START_FILE, 'w', encoding='utf-8')
f.write('1')
f.close()
f = open(STOP_FILE, 'w', encoding='utf-8')
f.write('1')
f.close()
start_mtime = os.path.getmtime(START_FILE)
stop_mtime = os.path.getmtime(STOP_FILE)
sf_file = None
# Initialize recording variables
start_time = 9999999999999999
recording = False


def reset_when_over():
    global start_time, recording, sf_file
    start_time = 9999999999999999
    recording = False
    sf_file.close()


def reset_when_start(new_start_mtime):
    global start_time, recording, sf_file, start_mtime
    start_mtime = new_start_mtime
    start_time = tm.time()
    recording = True
    try:
        os.remove(RECORD_FILE)
    except Exception as e:
        print(e)
    sf_file = sf.SoundFile(RECORD_FILE, mode='wb', samplerate=SAMPLE_RATE, channels=CHANNELS, subtype=SUB_TYPE)


# Recording callback
def callback(indata, frames, time, status):
    global recording, start_time, start_mtime, stop_mtime, sf_file

    # Check if start.txt has been modified
    new_start_mtime = os.path.getmtime(START_FILE)
    if new_start_mtime != start_mtime and not recording:
        print('start record ... ')
        reset_when_start(new_start_mtime)
        return

    # Check if stop.txt has been modified
    new_stop_mtime = os.path.getmtime(STOP_FILE)
    if new_stop_mtime != stop_mtime and recording:
        stop_mtime = new_stop_mtime
        print('stop record with order ... ')
        reset_when_over()
        # Send audio file to server
        with open(RECORD_FILE, 'rb') as f:
            print('send record ... ')
            requests.post(SERVER_URL, files={'file': f})
        return

    # Record audio
    if recording:
        print('on record ... ')
        sf_file.write(indata)
        # Check for silence
        # amplitude = np.abs(indata).mean()
        # if amplitude < SILENCE_THRESHOLD:
        #     if tm.time() - start_time > SILENCE_TIME:
        #         # Stop recording
        #         print('stop record with silent ... ')
        #         reset_when_over()
        #         # Send audio file to server
        #         with open(RECORD_FILE, 'rb') as f:
        #             print('send record ... ')
        #             requests.post(SERVER_URL, files={'file': f})
        # else:
        #     start_time = tm.time()
        return


################################################################################### above: audio record functions

makerobo_Bpin = 27  # RGB—LED,蓝色管脚定义
makerobo_blocking = 0  # 判断值

rgb_Lv = [0, 20]  # RGB 亮度配置
rgb_color = 0  # RGB 颜色配置


# GPIO初始化设置
def makerobo_setup():
    global p_R, p_G, p_B
    GPIO.setmode(GPIO.BCM)  # 采用BCM映射管脚给GPIO口
    GPIO.setwarnings(False)  # 忽略GPIO操作注意警告
    GPIO.setup(makerobo_Bpin, GPIO.OUT)  # 设置蓝色LED管脚为输出模式
    p_B = GPIO.PWM(makerobo_Bpin, 2000)  # 设置频率为2K
    p_B.start(0)  # 初始化占空比为0
    pylirc.init("pylirc", "/etc/lirc/conf", makerobo_blocking)  # 载入配置参数


def RGB_and_listen_control(config):
    # print("rgb_color[2], rgb_Lv[2]: ", rgb_color[2], rgb_Lv[2])
    global rgb_color
    if config == 'KEY_VOLUMEDOWN' and rgb_color != rgb_Lv[0]:  # 第三行第一个
        rgb_color = rgb_Lv[0]
        print('stop listen')
        fl = open(STOP_FILE, 'w', encoding='utf-8')
        fl.write("0")
        fl.close()

    if config == 'KEY_VOLUMEUP' and rgb_color != rgb_Lv[1]:  # 第三行第二个
        rgb_color= rgb_Lv[1]
        print('start listen')
        fl = open(START_FILE, 'w', encoding='utf-8')
        fl.write("1")
        fl.close()


# 循环函数
def makerobo_loop():
    while True:
        s = pylirc.nextcode(1)  # 获取红外遥控器码值
        if s is not None:
            for code in s:
                print("Command: ", code["config"])  # 调试信息，可以具体知道按下了哪个按键
                RGB_and_listen_control(code["config"])  # 调用控制RGB函数
                p_B.ChangeDutyCycle(rgb_color)  # RGB-LED 颜色设置 (改变PWM占空比)
        tm.sleep(1)


# 释放函数
def destroy():
    p_B.stop()
    GPIO.output(makerobo_Bpin, GPIO.LOW)
    GPIO.cleanup()  # 释放资源
    pylirc.exit()  # 退出红外遥控器接收


# 程序入口
if __name__ == '__main__':
    with sd.InputStream(callback=callback):
        try:
            makerobo_setup()  # GPIO初始化程序
            makerobo_loop()  # 调用循环函数
        except KeyboardInterrupt:  # 如果按下ctrl + C,退出，处理异常
            destroy()  # 释放资源
