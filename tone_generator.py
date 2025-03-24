import numpy as np
import sounddevice as sd
import threading
import time

# Globals to control the loop
is_playing = True

def generate_tone(frequency, sample_rate=44100):
    global is_playing
    t = 0
    block_size = 1024

    def callback(outdata, frames, time, status):
        nonlocal t
        if not is_playing:
            raise sd.CallbackStop()
        samples = 0.5 * np.sin(2 * np.pi * frequency * (np.arange(frames) + t) / sample_rate)
        outdata[:] = samples.reshape(-1, 1)
        t += frames

    # Start streaming
    with sd.OutputStream(channels=1, callback=callback, samplerate=sample_rate, blocksize=block_size):
        print(f"Playing {frequency} Hz tone. Press Enter to stop...")
        input()  # Wait for user input
        is_playing = False


# Run it
try:
    freq = float(input("Enter frequency in Hz (e.g., 432 or 440): "))
    generate_tone(freq)
except ValueError:
    print("Invalid input. Please enter a number.")
