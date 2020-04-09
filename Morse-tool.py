import numpy as np
 
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



def action(line):
    global continuer
    line=line.split(" ")
    if(len(line) > 0):
        if(line[0] == "stop"):
            continuer=False
        elif(line[0] == "decode" and len(line) > 1):
            decode(line[1:])
        elif(line[0] == "encode" and len(line) > 1):
            encode(line[1:])
    print()

print("\033[0;37;41m#####      Morse-Tool      #####")
print("")
print("By @stephane_branly")
print("https://github.com/StephaneBranly")
print("Python 3.6.2")
print("")
print("\033[0;37;41m#####                       #####")
print("\033[0;37;48m")

while(continuer):
    line=input("> ")
    action(line)
