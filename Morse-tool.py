# ************************************************************************************************************************* #
#   UTC Header                                                                                                              #
#                                                         ::::::::::::::::::::       :::    ::: :::::::::::  ::::::::       #
#      Morse-tool.py                                      ::::::::::::::::::::       :+:    :+:     :+:     :+:    :+:      #
#                                                         ::::::::::::::+++#####+++  +:+    +:+     +:+     +:+             #
#      By: branlyst <stephane.branly@etu.utc.fr>          ::+++##############+++     +:+    +:+     +:+     +:+             #
#      https://github.com/StephaneBranly              +++##############+++::::       +#+    +:+     +#+     +#+             #
#                                                       +++##+++::::::::::::::       +#+    +:+     +#+     +#+             #
#                                                         ::::::::::::::::::::       +#+    +#+     +#+     +#+             #
#                                                         ::::::::::::::::::::       #+#    #+#     #+#     #+#    #+#      #
#      Update: 2021/06/01 12:08:06 by branlyst            ::::::::::::::::::::        ########      ###      ######## .fr   #
#                                                                                                                           #
# ************************************************************************************************************************* #

import numpy as np
from playsound import playsound
import speech_recognition as s_r
import time

r = s_r.Recognizer()
my_mic = s_r.Microphone(device_index=1)

continuer = True

# Tableau de correspondance alphabet / Code Morse
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

# Fonction de decodage de message code en morse
def decode(sentence):
    global final_sentence
    final_sentence = ""
    code_copy = []
    code_copy = code[:,1] # selection de la colonne 1, correspondant aux codes morses
    for letter in sentence: # pour chaque caractere code en morse
        result = np.where(code_copy == letter) # recherche du caractere dans la table de codes morse
        if(len(result[0])==1): # si un code morse a ete trouve, on met le caractere alphabetique
            final_sentence += str(code[result[0][0]][0])
        else: # si code non trouvé, on met un espace
            final_sentence += " "
    print(str(final_sentence)) # affichage du message decode
    
# Fonction d'encodage d'un message en alphabet vers un son code morse
def encode(sentence):
    global final_sentence
    final_sentence = ""
    for word in sentence: # pour chaque mot dans la phrase
        word=word.lower() # on met le mot en minuscule
        for letter in word: # pour chaque lettre du mot
            if(ord(letter)-97 >= 0 and ord(letter)-97 <= 25): # s'il s'agit d'un lettre entre a et z,
                final_sentence += str(code[ord(letter)-97][1])+" " # on ajoute le code morse associe (retrouve avec decalage par rappot a la table ascii)
        final_sentence += "   " # ajout d'espace entre les mots
    print(str(final_sentence))

# systeme de sauvegarde de variables
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

# Fonction d'emission de message morse en audio
def emit(sentence):
    for letter in sentence: # pour chaque lettre du message
        for c in letter: # pour chaque . et - de la lettre
            if(c=="."): # si c'est un . , emission du bip
                playsound("bip.mp3")
                time.sleep(.100)
            elif(c=="-"): # si c'est un - , emission du biiip
                playsound("biiip.mp3")
                time.sleep(.300)
        time.sleep(.200)

# Execution de fonction
def action(line):
    global continuer
    line=line.split(" ") # split de la ligne par espace
    sav_copy = []
    sav_copy = sav[:,0]

    if(len(line) > 0): # analyse de la commande demandee line[0]
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
                    with my_mic as source:
                        print("I listen")
                        r.adjust_for_ambient_noise(source)
                        audio = r.listen(source)
                    print(audio)
                    print(sentence)
                    encode(sentence.split(" "))
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
while(continuer): # boucle main
    line=input("> ")
    action(line)
