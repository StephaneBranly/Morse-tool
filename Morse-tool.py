import numpy as np
from playsound import playsound
import pyaudio
import speech_recognition as s_r
import time

r = s_r.Recognizer()
my_mic = s_r.Microphone(device_index=1)
CHANNELS = 1
RATE = 48000

p = pyaudio.PyAudio()
fulldata = np.array([])


continuer = True
code = np.array([["a", ".-"],
["b", "-..."],
["c", "-.-."],
["d", "-.."],
["e", "."],
["f", "..-."],
["g", "--."],
["h", "...."],
["i", ".."],
["j", ".---"],
["k", "-.-"],
["l", ".-.."],
["m", "--"],
["n", "-."],
["o", "---"],
["p", ".--."],
["q", "--.-"],
["r", ".-."],
["s", "..."],
["t", "-"],
["u", "..-"],
["v", "...-"],
["w", ".--"],
["x", "-..-"],
["y", "-.--"],
["z", "--.."]])

sav = np.array([["",""],["",""]])
final_sentence = ""

def decode(sentence):
    global final_sentence
    final_sentence = ""
    code_copy = []
    code_copy = code[:,1]
    for letter in sentence:
        result = np.where(code_copy == letter)
        if(len(result[0])==1):
            final_sentence += str(code[result[0][0]][0])
        else:
            final_sentence += " "
    print(str(final_sentence))
    
def encode(sentence):
    global final_sentence
    final_sentence = ""
    for word in sentence:
        word=word.lower()
        for letter in word:
            if(ord(letter)-97 >= 0 and ord(letter)-97 <= 25):
                final_sentence += str(code[ord(letter)-97][1])+" "
        final_sentence += "   "
    print(str(final_sentence))

def save(id,sentence):
    global sav
    id_save = "#"+id
    sentence = " ".join(sentence)
    new_sav = [id_save,sentence]

    sav_copy = []
    sav_copy = sav[:,0]
    result = np.where(sav_copy == id_save)
    if(len(result[0])!=1):
        sav = np.vstack([sav, new_sav])
        print("saved as "+str(id_save))

def listen_morse(time_record):
    global final_sentence, fulldata
    fulldata = np.array([])
    stream = p.open(format=pyaudio.paFloat32,
                    channels=CHANNELS,
                    rate=RATE,
                    output=False,
                    input=True,
                    stream_callback=callback)
    print("I listen")
    stream.start_stream()

    while stream.is_active():
        time.sleep(int(time_record))
        stream.stop_stream()
    stream.close()
    print("Finished.")
    result = []
    average_tab = []
    average = 0
    somme = 0
    somme_state = 0
    last_state = 0
    size_cut = 100
    i = 0
    min_dur = RATE*int(time_record)
    max_dur = 0
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
                if(somme_state < min_dur):
                    min_dur = somme_state
                if(somme_state > max_dur):
                    max_dur = somme_state
                last_state = 0
                somme_state = 1
        somme = somme+abs(x)
        i = i+1
        somme_state = somme_state+1

    middle = (min_dur+max_dur)/2
    final_sentence = ""
    for z in result:
        if(z[0] == 0 and z[1] > 2*middle):
            final_sentence = final_sentence+"  "
        elif(z[0] == 0 and z[1] > middle):
            final_sentence = final_sentence+" "
        elif(z[0] == 1 and z[1] < middle):
            final_sentence = final_sentence+"."
        elif(z[0] == 1 and z[1] > middle):
            final_sentence = final_sentence+"-"
    p.terminate()

def callback(in_data, frame_count, time_info, flag):
    global b, a, fulldata, frames
    audio_data = np.fromstring(in_data, dtype=np.float32)
    fulldata = np.append(fulldata, audio_data)
    return (audio_data, pyaudio.paContinue)

def emit(sentence):
    for letter in sentence:
        for c in letter:
            if(c=="."):
                playsound("bip.mp3")
                time.sleep(.100)
            elif(c=="-"):
                playsound("biiip.mp3")
                time.sleep(.300)
        time.sleep(.200)

def action(line):
    global continuer
    line=line.split(" ")
    sav_copy = []
    sav_copy = sav[:,0]

    if(len(line) > 0):
        if(line[0] == "stop"):
            continuer=False
        if(line[0] == "help"):
            print("> encode latin sentence")
            print("> decode morse sentence")
            print("> emit morse sentence")
            print("> save name sentence")
            print("sentence could be write, or you can use saved sentence with #name, the last with #last, sentence from microphone with #mic")
        elif(line[0] == "decode" and len(line) > 1):
            if(len(line[1])>0 and line[1][0]=="#"):
                if(line[1]=="#mic"):
                    if(len(line)>2):
                        time=line[2]
                    else:
                        time=15
                    listen_morse(time)
                    print(final_sentence)
                    decode(final_sentence.split(" "))
                elif(line[1]=="#last"):
                    decode(final_sentence.split(" "))
                else:
                    result = np.where(sav_copy == line[1])
                    if(len(result[0])==1):
                        decode(sav[result[0][0]][1].split(" "))
            else:
                decode(line[1:])
        elif(line[0] == "encode" and len(line) > 1):
            if(len(line[1])>0 and line[1][0]=="#"):
                if(line[1]=="#mic"):
                    with my_mic as source:
                        print("I listen")
                        r.adjust_for_ambient_noise(source)
                        audio = r.listen(source)
                    sentence = r.recognize_google(audio)
                    print(sentence)
                    encode(sentence.split(" "))
                elif(line[1]=="#last"):
                    encode(final_sentence.split(" "))
                else:
                    result = np.where(sav_copy == line[1])
                    if(len(result[0])==1):
                        encode(sav[result[0][0]][1].split(" "))
            else:
                encode(line[1:])
        elif(line[0] == "save" and len(line) > 2):
            save(line[1],line[2:])
        elif(line[0] == "emit" and len(line) > 1):
            if(len(line[1])>0 and line[1][0]=="#"):
                if(line[1]=="#last"):
                    emit(final_sentence.split(" "))
                else:
                    result = np.where(sav_copy == line[1])
                    if(len(result[0])==1):
                        emit(sav[result[0][0]][1].split(" "))
            else:
                emit(line[1:])
    print()

print("\033[0;37;41m#####      Morse-Tool      #####")
print("")
print("By @stephane_branly")
print("https://github.com/StephaneBranly")
print("Python 3.6.2")
print("")
print("\033[0;37;41m#####                       #####")
print("\033[0;37;48m")
playsound('bip.mp3')
playsound('biiip.mp3')
print("write help to know the commands")
while(continuer):
    line=input("> ")
    action(line)
