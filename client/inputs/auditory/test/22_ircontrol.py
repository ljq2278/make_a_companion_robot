#!/usr/bin/python3
# -*- coding: utf-8 -*-
# －－－－湖南创乐博智能科技有限公司－－－－
#  文件名：22.ircontrol.py
#  版本：V2.0
#  author: zhulin
#  说明：红外遥控器实验
#####################################################

import pylirc
import time
import RPi.GPIO as GPIO

# makerobo_Rpin = 17  # RGB—LED,红色管脚定义
# makerobo_Gpin = 18  # RGB—LED,绿色管脚定义
makerobo_Bpin = 27  # RGB—LED,蓝色管脚定义
makerobo_blocking = 0 # 判断值

rgb_Lv = [100, 20, 0]   # RGB 亮度配置
rgb_color = [00, 00, 00]  # RGB 颜色配置

# RGB-LED 颜色设置
def makerobo_ledColorSet(color):
	# p_R.ChangeDutyCycle(100 - color[0])     # 改变PWM占空比
	# p_G.ChangeDutyCycle(100 - color[1])     # 改变PWM占空比
	p_B.ChangeDutyCycle(100 - color[2])     # 改变PWM占空比

# GPIO初始化设置
def makerobo_setup():
	global p_R, p_G, p_B
	GPIO.setmode(GPIO.BCM)                 # 采用BCM映射管脚给GPIO口       
	GPIO.setwarnings(False)                # 忽略GPIO操作注意警告
	# GPIO.setup(makerobo_Rpin, GPIO.OUT)    # 设置红色LED管脚为输出模式
	# GPIO.setup(makerobo_Gpin, GPIO.OUT)    # 设置绿色LED管脚为输出模式
	GPIO.setup(makerobo_Bpin, GPIO.OUT)    # 设置蓝色LED管脚为输出模式
	
	# p_R = GPIO.PWM(makerobo_Rpin, 2000)     # 设置频率为2K
	# p_G = GPIO.PWM(makerobo_Gpin, 2000)     # 设置频率为2K
	p_B = GPIO.PWM(makerobo_Bpin, 2000)     # 设置频率为2K
	
	# p_R.start(0)                       # 初始化占空比为0
	# p_G.start(0)                       # 初始化占空比为0
	p_B.start(0)                       # 初始化占空比为0
	pylirc.init("pylirc", "/etc/lirc/conf", makerobo_blocking) # 载入配置参数

# 从一个区域映射到另一个区域函数
def makerobo_map(x, in_min, in_max, out_min, out_max):
	return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

def RGB_control(config):
	global color
	if config == 'KEY_CHANNELDOWN':  # 按键第一行第一个
		rgb_color[0] = rgb_Lv[0]
		print ('Makerobo Red OFF')

	if config == 'KEY_CHANNEL':     # 按键第一行第二个
		rgb_color[0] = rgb_Lv[1]
		print ('Makerobo Light Red')

	if config == 'KEY_CHANNELUP':   # 按键第一行第三个
		rgb_color[0] = rgb_Lv[2]
		print ('Makerobo Red')

	if config == 'KEY_PREVIOUS':    # 第二行第一个
		rgb_color[1] = rgb_Lv[0]
		print ('Makerobo Green OFF')

	if config == 'KEY_NEXT':       # 第二行第二个
		rgb_color[1] = rgb_Lv[1]
		print ('Makerobo Light Green')

	if config == 'KEY_PLAYPAUSE':  # 第二行第三个
		rgb_color[1] = rgb_Lv[2]
		print ('Makerobo Green')

	if config == 'KEY_VOLUMEDOWN': # 第三行第一个
		rgb_color[2] = rgb_Lv[0]
		print ('Makerobo Blue OFF')

	if config == 'KEY_VOLUMEUP':  # 第三行第二个
		rgb_color[2] = rgb_Lv[1]
		print ('Makerobo Light Blue')

	if config == 'KEY_EQUAL':    # 第三行第三个
		rgb_color[2] = rgb_Lv[2]
		print ('Makerobo BLUE')

# 循环函数
def makerobo_loop():
	while True:
		s = pylirc.nextcode(1)    # 获取红外遥控器码值		
		while s:
			for code in s:
				print ("Command: ", code["config"]) # 调试信息，可以具体知道按下了哪个按键
				RGB_control(code["config"])  # 调用控制RGB函数
				makerobo_ledColorSet(rgb_color)  # RGB-LED 颜色设置
			if(not makerobo_blocking):       # 读取到值
				s = pylirc.nextcode(1)       # 再一次获取红外遥控器码值	
			else:
				s = []
# 释放函数
def destroy():
	# p_R.stop()   # 停止PWM
	# p_G.stop()
	p_B.stop()
	# GPIO.output(makerobo_Rpin, GPIO.LOW)    # 关闭所有的LED灯
	# GPIO.output(makerobo_Gpin, GPIO.LOW)
	GPIO.output(makerobo_Bpin, GPIO.LOW)
	GPIO.cleanup() # 释放资源
	pylirc.exit()  # 退出红外遥控器接收

# 程序入口
if __name__ == '__main__':
	try:
		makerobo_setup() # GPIO初始化程序
		makerobo_loop()  # 调用循环函数
	except KeyboardInterrupt: # 如果按下ctrl + C,退出，处理异常
		destroy() # 释放资源
