import sounddevice as sd
import soundfile as sf
import numpy as np
import queue

# Set the duration for silence
silence_limit_seconds = 5

# Sampling frequency
fs = 44100  # Sample rate in Hz
# block_size
bs = 512
# Threshold to detect silence
threshold = 1.5

# Buffer to hold audio
buffer = []

sub_type = "PCM_16"
record_scale = 4
q = queue.Queue()


def audio_callback(indata, frames, time, status):
    volume_norm = np.linalg.norm(indata) * 10
    print(volume_norm)  # You can print it out for debugging
    buffer.append(volume_norm)
    q.put(indata.copy() * record_scale)


if __name__ == '__main__':
    # Start the stream
    with sf.SoundFile("tst.wav", mode='w', samplerate=fs, channels=1, subtype=sub_type) as file:
        with sd.InputStream(callback=audio_callback, channels=1, samplerate=fs, blocksize=bs) as stream:
            while True:
                file.write(q.get())
                if len(buffer) > silence_limit_seconds * fs / bs:  # Convert seconds to frames
                    if np.mean(buffer[-int(silence_limit_seconds * fs / bs):]) < threshold:  # If the mean volume in the last X frames is below the threshold
                        print("Silence detected, stopping...")
                        break
