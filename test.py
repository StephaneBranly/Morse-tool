import pyaudio
import time
import numpy as np
from matplotlib import pyplot as plt
import scipy.signal as signal
print("Start run")


CHANNELS = 1
RATE = 2000

p = pyaudio.PyAudio()
fulldata = np.array([])
dry_data = np.array([])


def main():
    stream = p.open(format=pyaudio.paFloat32,
                    channels=CHANNELS,
                    rate=RATE,
                    output=True,
                    input=True,
                    stream_callback=callback)

    stream.start_stream()

    while stream.is_active():
        time.sleep(15)
        stream.stop_stream()
    stream.close()
    print("mic closed")

    numpydata = np.hstack(fulldata)
    numpydata_abs = abs(numpydata)
    numpydata_bi = np.array([])
    for x in numpydata_abs:
        if x > 0.2:
            numpydata_bi = np.append(numpydata_bi, 1)
        else:
            numpydata_bi = np.append(numpydata_bi, 0)

    plt.plot(numpydata)
    plt.plot(numpydata_abs)
    plt.plot(numpydata_bi)
    plt.title("mic")
    plt.show()

    print("End")

    p.terminate()


def callback(in_data, frame_count, time_info, flag):
    global b, a, fulldata, dry_data, frames
    audio_data = np.fromstring(in_data, dtype=np.float32)
    dry_data = np.append(dry_data, audio_data)
    # do processing here
    fulldata = np.append(fulldata, audio_data)
    return (audio_data, pyaudio.paContinue)


main()
