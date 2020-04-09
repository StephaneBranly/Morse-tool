continuer = True
code = [['a','.-'],
['b','-...'],
['c','-.-.'],
['d','-..'],
['e','.'],
['f','..-.'],
['g','--.'],
['h','....'],
['i','..'],
['j','.---'],
['k','-.-'],
['l','.-..'],
['m','--'],
['n','-.'],
['o','---'],
['p','.--.'],
['q','--.-'],
['r','.-.'],
['s','...'],
['t','-'],
['u','..-'],]
['v','...-'],
['w','.--'],
['x','-..-'],
['y','-.--'],
['z','--..']]

def decode(sentence):
    print("sentence = "+str(sentence))


def encode(sentence):
    print("sentence = "+str(sentence))


def action(line):
    global continuer
    line = line.split(' ')
    if(len(line) > 0):
        if(line[0] == "stop"):
            continuer = False
        elif(line[0] == "decode" and len(line) > 1):
            decode(line[1:])
        elif(line[0] == "encode" and len(line) > 1):
            encode(line[1:])


print("\033[0;37;41m#####      Morse-Tool      #####")
print("")
print("By @stephane_branly")
print("https://github.com/StephaneBranly")
print("Python 3.6.2")
print("")
print("\033[0;37;41m#####                       #####")
print("\033[0;37;48m")

while(continuer):
    line = input("> ")
    action(line)
