import numpy as np
import sounddevice as sd

def play_tone(frequency, duration=2, sample_rate=44100):
    t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
    waveform = 0.5 * np.sin(2 * np.pi * frequency * t)
    sd.play(waveform, sample_rate)
    sd.wait()

    