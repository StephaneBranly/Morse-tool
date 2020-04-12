import pyaudio
import time
import numpy as np
from matplotlib import pyplot as plt
import scipy.signal as signal
print("Start run")


CHANNELS = 1
RATE = 44000

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
    print(fulldata)
    print("traitement en cours")
    result = []
    result2 = []

    retraitement = []
    retraitement2 = []

    average_tab = []
    average = 0
    somme = 0
    somme_state = 0
    last_state = 0
    size_cut = 100
    i = 0
    for x in fulldata:
        if(i == size_cut):
            average = somme/size_cut
            for z in range(0, size_cut):
                average_tab.append(average)
            somme = 0
            i = 0
            if (last_state == 0 and average > 0.1):
                result.append([0, somme_state])
                last_state = 1
                somme_state = 0
            elif(last_state == 1 and average < 0.1):
                result.append([1, somme_state])
                last_state = 0
                somme_state = 1
        somme = somme+abs(x)
        i = i+1
        somme_state = somme_state+1

    for z in result:
        for x in range(0, z[1]):
            result2.append(z[0])

    numpydata = np.hstack(fulldata)
    numpydata_bi = np.hstack(result2)
    numpydata_avr = np.hstack(average_tab)
    plt.plot(numpydata)
    plt.plot(numpydata_bi)
    plt.plot(numpydata_avr)
    plt.title("mic")
    plt.show()

    print(str(result))

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
