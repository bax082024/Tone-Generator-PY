import numpy as np
import sounddevice as sd
import threading
import keyboard  # For real-time key input

# Settings
frequency = 432  # Starting frequency
volume = 0.5
sample_rate = 44100
block_size = 1024
running = True

def tone_callback(outdata, frames, time, status):
    global frequency, sample_rate
    t = (np.arange(frames) + tone_callback.phase) / sample_rate
    wave = volume * np.sin(2 * np.pi * frequency * t)
    outdata[:] = wave.reshape(-1, 1)
    tone_callback.phase += frames

tone_callback.phase = 0

def play_tone():
    with sd.OutputStream(channels=1, callback=tone_callback, samplerate=sample_rate, blocksize=block_size):
        print("Press ↑ to increase frequency, ↓ to decrease, ESC to stop.")
        while running:
            sd.sleep(100)

def control_frequency():
    global frequency, running
    while running:
        if keyboard.is_pressed("up"):
            frequency += 1
            print(f"↑ Frequency: {frequency} Hz")
            sd.sleep(200)
        elif keyboard.is_pressed("down"):
            frequency -= 1
            print(f"↓ Frequency: {frequency} Hz")
            sd.sleep(200)
        elif keyboard.is_pressed("esc"):
            print("Exiting...")
            running = False
            break

# Start both threads
tone_thread = threading.Thread(target=play_tone)
key_thread = threading.Thread(target=control_frequency)

tone_thread.start()
key_thread.start()

tone_thread.join()
key_thread.join()
