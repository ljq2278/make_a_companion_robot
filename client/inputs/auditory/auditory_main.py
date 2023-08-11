import sounddevice as sd
import soundfile as sf
import numpy as np
import queue
import RPi.GPIO as GPIO
import time, os
import requests
from client_utils.path import AUDITORY_FILE_PATH, AUDITORY_SERVER_IP_PATH

makerobo_Bpin = 12

# Set the duration for silence
silence_limit_seconds = 4

# Sampling frequency
fs = 44100  # Sample rate in Hz
# block_size
bs = 512
# Threshold to detect silence
threshold = 2.5

# Buffer to hold audio
buffer = []

sub_type = "PCM_16"

record_scale = 4
q = queue.Queue()

GPIO.setmode(GPIO.BCM)  # 采用BCM映射管脚给GPIO口
GPIO.setwarnings(False)  # 忽略GPIO操作注意警告
GPIO.setup(makerobo_Bpin, GPIO.OUT)
p_B = GPIO.PWM(makerobo_Bpin, 2000)  # 设置频率为2K
p_B.start(0)


def audio_callback(indata, frames, time, status):
    volume_norm = np.linalg.norm(indata) * 10
    # print(volume_norm)  # You can print it out for debugging
    buffer.append(volume_norm)
    q.put(indata.copy() * record_scale)


def listen():
    global p_B
    try:
        os.remove(AUDITORY_FILE_PATH)
    except Exception as e:
        print(e)
    p_B.ChangeDutyCycle(100)
    with sf.SoundFile(AUDITORY_FILE_PATH, mode='w', samplerate=fs, channels=1, subtype=sub_type) as file:
        with sd.InputStream(callback=audio_callback, channels=1, samplerate=fs, blocksize=bs) as stream:
            while True:
                file.write(q.get())
                if len(buffer) > silence_limit_seconds * fs / bs:  # Convert seconds to frames
                    if np.mean(buffer[-int(silence_limit_seconds * fs / bs):]) < threshold:  # If the mean volume in the last X frames is below the threshold
                        print("Silence detected, stopping...")
                        stream.close()
                        file.close()
                        if len(buffer) > 350:
                            with open(AUDITORY_FILE_PATH, 'rb') as f:
                                print('send record ... buffer cont: ', len(buffer))
                                requests.post(AUDITORY_SERVER_IP_PATH, files={'file': f})
                        p_B.ChangeDutyCycle(0)
                        break


if __name__ == '__main__':
    # Start the stream
    while True:
        print("listen start ...")
        listen()
        print("listen end ...")
        buffer.clear()
        time.sleep(2)
