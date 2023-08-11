
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
f = open(START_FILE,'w',encoding='utf-8')
f.write('1')
f.close()
f = open(STOP_FILE,'w',encoding='utf-8')
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
        amplitude = np.abs(indata).mean()
        if amplitude < SILENCE_THRESHOLD:
            if tm.time() - start_time > SILENCE_TIME:
                # Stop recording
                print('stop record with silent ... ')
                reset_when_over()
                # Send audio file to server
                with open(RECORD_FILE, 'rb') as f:
                    print('send record ... ')
                    requests.post(SERVER_URL, files={'file': f})
        else:
            start_time = tm.time()
        return




def loop():
    CMDID = DF2301Q.get_CMDID()
    if (0 != CMDID):
        print("CMDID = %u\n" % CMDID)
    if 1 == CMDID or 5 == CMDID:
        f = open(START_FILE,'w',encoding='utf-8')
        f.write("5")
        f.close()
    if 6 == CMDID:
        f = open(STOP_FILE,'w',encoding='utf-8')
        f.write("6")
        f.close()
    time.sleep(1)

# Start audio stream
with sd.InputStream(callback=callback):
    CMDID = DF2301Q.get_CMDID()
    while True:
        loop()
        tm.sleep(1)