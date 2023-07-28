#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# －－－－湖南创乐博智能科技有限公司－－－－
#  文件名：18_thermistor.py
#  版本：V2.0
#  author: zhulin
# 说明：模拟温度传感器实验
#####################################################
import PCF8591 as ADC
import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM) # 管脚映射，采用BCM编码

# 初始化工作
def makerobo_setup():
	ADC.setup(0x48)  # 设置PCF8591模块地址

# 循环函数
def makerobo_loop():
	makerobo_count = 0                                        # 计数值
	while True:                                               # 无限循环
		makerobo_voiceValue = ADC.read(0)                     # 读取AIN0上的模拟值             
		if makerobo_voiceValue:                               # 当声音值不为0
			print ("Sound Value:", makerobo_voiceValue)       # 打印出声音值
			if makerobo_voiceValue < 80:                      # 如果声音传感器读取值小于80
				print ("Voice detected! ", makerobo_count)    # 打印出计数值
				makerobo_count += 1                           # 计数值累加
			time.sleep(0.2)                                   # 延时 200ms

# 程序入口
if __name__ == '__main__':
	try:
		makerobo_setup() # 初始化程序
		makerobo_loop()  # 循环函数
	except KeyboardInterrupt: 
		pass	
