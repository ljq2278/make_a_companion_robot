import time
import smbus
import wave
import numpy as np

# PCF8591 settings
PCF8591_ADDRESS = 0x48
PCF8591_ANALOG_IN = 0x40

# Initialize I2C bus
bus = smbus.SMBus(1)

def read_adc(channel):
    bus.write_byte(PCF8591_ADDRESS, PCF8591_ANALOG_IN + channel)
    # Read and discard the first value (previous ADC value)
    bus.read_byte(PCF8591_ADDRESS)
    # Read the actual ADC value
    return bus.read_byte(PCF8591_ADDRESS)

def main():
    try:
        print("Recording... Press Ctrl+C to stop and save the recording.")

        # Recording settings
        duration = 10  # Duration of recording in seconds
        sampling_rate = 20000  # Adjust this value for the desired sampling rate (in Hz)
        filename = "output.wav"

        # Initialize the WAV file
        wav_file = wave.open(filename, "w")
        wav_file.setnchannels(1)
        wav_file.setsampwidth(1)  # 1 byte (8 bits) per sample
        wav_file.setframerate(sampling_rate)

        # Record audio data
        start_time = time.time()
        while time.time() - start_time < duration:
            adc_value = read_adc(0)  # Assuming the LM358 module is connected to the first analog input (AIN0)
            wav_file.writeframes(np.array([adc_value]).tobytes())
            # time.sleep(1.0 / sampling_rate)

    except KeyboardInterrupt:
        print("Stopping recording...")

    finally:
        # Close the WAV file
        wav_file.close()
        print(f"Recording saved to {filename}")

if __name__ == "__main__":
    main()