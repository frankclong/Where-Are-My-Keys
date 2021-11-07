import numpy as np
import pyaudio
import matplotlib.pyplot as plt
from pynput import keyboard
import struct
import math
import scipy.signal
import time

global p
global stream

# Guitar - MIDDLE C IS 2nd String 1st Fret!!!! (NOT 5th string 3rd fret)
NOTE_MIN = 40       # E2
NOTE_MAX = 76       # E5 

FSAMP = 44100       # Sampling frequency in Hz # 22050?
FRAME_SIZE = 2048   # How many samples per frame?
FRAMES_PER_FFT = 16 # FFT takes average across how many frames?

SAMPLES_PER_FFT = FRAME_SIZE*FRAMES_PER_FFT
FREQ_STEP = float(FSAMP)/SAMPLES_PER_FFT

NOTE_NAMES = 'C C# D D# E F F# G G# A A# B'.split()

# For tap recognition
SHORT_NORMALIZE = (1.0/32768.0)


def freq_to_number(f): return 69 + 12*np.log2(f/440.0)
def number_to_freq(n): return 440 * 2.0**((n-69)/12.0)
def note_name(n): return NOTE_NAMES[n % 12] + str(round(n/12 - 1))

# Get min/max index within FFT of notes we care about.
# See docs for numpy.rfftfreq()
def note_to_fftbin(n): return number_to_freq(n)/FREQ_STEP


class StreamProcessor(object):

    def __init__(self):
        self._name = "Frank"
        
    def run(self):
        self._stream = pyaudio.PyAudio().open(format=pyaudio.paInt16,
                                channels=1,
                                rate=FSAMP,
                                input=True,
                                frames_per_buffer=FRAME_SIZE,
                                stream_callback=self._process_frame)

        self._stream.start_stream()

        while self._stream.is_active() and not input():
            time.sleep(0.1)

        self._stream.stop_stream()
        self._stream.close()

    def _process_frame(self, data, frame_count, time_info, status_flag):
        data_array = np.fromstring(data, dtype=np.int16)
        freq0 = 1
        if freq0:
            print("HELLO!")
        return (data, pyaudio.paContinue)


if __name__ == '__main__':
    stream_proc = StreamProcessor()
    stream_proc.run()