import numpy as np
from playsound import playsound
import time
 
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

def decode(sentence):
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
    final_sentence = ""
    for word in sentence:
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
        elif(line[0] == "decode" and len(line) > 1):
            if(len(line[1])>0 and line[1][0]=="#"):
                result = np.where(sav_copy == line[1])
                if(len(result[0])==1):
                    decode(sav[result[0][0]][1].split(" "))
            else:
                decode(line[1:])
        elif(line[0] == "encode" and len(line) > 1):
            if(len(line[1])>0 and line[1][0]=="#"):
                result = np.where(sav_copy == line[1])
                if(len(result[0])==1):
                    encode(sav[result[0][0]][1].split(" "))
            else:
                encode(line[1:])
        elif(line[0] == "save" and len(line) > 2):
            save(line[1],line[2:])
        elif(line[0] == "emit" and len(line) > 1):
            if(len(line[1])>0 and line[1][0]=="#"):
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
while(continuer):
    line=input("> ")
    action(line)
