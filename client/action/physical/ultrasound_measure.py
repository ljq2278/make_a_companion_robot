import RPi.GPIO as GPIO
import time

# utr_TRIG = 11  # 超声波模块Tring控制管脚
# utr_ECHO = 35  # 超声波模块Echo控制管脚
utr_TRIG = 17  # 超声波模块Tring控制管脚
utr_ECHO = 19  # 超声波模块Echo控制管脚

GPIO.setmode(GPIO.BCM)
GPIO.setup(utr_TRIG, GPIO.OUT) # Tring设置为输出模式
GPIO.setup(utr_ECHO, GPIO.IN)  # Echo设置为输入模式

# 超声波计算距离函数
def ur_disMeasure():

	GPIO.output(utr_TRIG, 0)  # 开始起始
	time.sleep(0.000002)           # 延时2us

	GPIO.output(utr_TRIG, 1)  # 超声波启动信号，延时10us
	time.sleep(0.00001)            # 发出超声波脉冲
	GPIO.output(utr_TRIG, 0)           # 设置为低电平

	
	while GPIO.input(utr_ECHO) == 0: # 等待回传信号
		us_a = 0
	us_time1 = time.time()                # 获取当前时间
	while GPIO.input(utr_ECHO) == 1: # 回传信号截止信息
		us_a = 1
	us_time2 = time.time()                # 获取当前时间

	us_during = us_time2 - us_time1          # 转换微秒级的时间

	# 声速在空气中的传播速度为340m/s, 超声波要经历一个发送信号和一个回波信息，
	# 计算公式如下所示：
	return us_during * 340 / 2 * 100        # 求出距离



# 程序入口
if __name__ == "__main__":
	print(ur_disMeasure(),"cm") # 调用循环函数
	GPIO.cleanup()  # 释放资源
