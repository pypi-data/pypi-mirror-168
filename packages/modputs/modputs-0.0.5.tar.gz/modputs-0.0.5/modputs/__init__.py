import os
import sys
import msvcrt
import shutil


from time import sleep
from setuptools import setup, Extension


#TO DO LIST:@
#MAKE AN ADVANDED PRINT
#

RETURN = []
Black= "\u001b[30m"
Red= "\u001b[31m"
Green= "\u001b[32m"
Yellow= "\u001b[33m"
Blue= "\u001b[34m"
Magenta= "\u001b[35m"
Cyan= "\u001b[36m"
White= "\u001b[37m"
Reset= "\u001b[0m"

COLORLIST = ["\u001b[30m","\u001b[31m","\u001b[32m","\u001b[33m","\u001b[34m","\u001b[35m","\u001b[36m","\u001b[37m","\u001b[0m"]

def INPUT(text,x,y,NOENTER=False, NPRINT=False):
    print(text, end='')
    sys.stdout.write('\r' + (' ' * shutil.get_terminal_size()[0]))
    print ("\033[A")
    sys.stdout.write("\x1b7\x1b[%d;%df%s\x1b8" % (x,y, f"{text}"))
    sys.stdout.flush()
    f = open("keys.txt", "a")
    while True:
        PRINT = False
        if msvcrt.kbhit():
            key = (str(msvcrt.getch()))
            s = key.replace(key[1:], '')
            d = s.replace("'", "")
            if PRINT == True:
                print(d)
                break
            PRINT = True
            # box = F'''
            # ╔═╗
            # ║{d}║
            # ╚═╝'''
            if d == r"\r":
                pass
            else:
                f = open("keys.txt", "a")
                f.write(F"{d}")
            if d == r"\x08":
                sys.stdout.write('\r' + (' ' * shutil.get_terminal_size()[0]))
                print ("\033[A")
                sys.stdout.write("\x1b7\x1b[%d;%df%s\x1b8" % (x,y, f"{text}"))
                sys.stdout.flush()
                f.close()
                os.remove("keys.txt")
            elif NOENTER == True:
                if d == r"\r":
                    pass
                else:
                    f = open("keys.txt", "a")
                    f.write(F"{d}")
            elif d == r"\r":
                f = open("keys.txt", "r")
                e = f.read()
                userinput = e.replace('\r', '')
                print("                             \033[A")
                f.close()
                break
                #STORE IT IN A VARIABLE
            else:
                if NPRINT == True:
                    sys.stdout.write(F"{d}")
                    sys.stdout.flush()
                else:
                    sys.stdout.write("\x1b7\x1b[%d;%df%s\x1b8" % (x,y+2, f"{d}"))
                    sys.stdout.flush()
                    #print(F"{d}", end = '')
                    sys.stdout.write("\x1b7\x1b[%d;%df%s\x1b8" % (14, 4+1, f"\r"))
                    sys.stdout.flush()

def READ():
    global userinput
    f = open("keys.txt", "r")
    lines = f.read()
    f.close()
    os.remove("keys.txt")
    READ.userinput = lines.replace('\n', '')
    #print("\n"+READ.userinput)


def RAINBOW(x,y,Loop=False):
    if Loop==True:
        while True:
            for i in COLORLIST:
                sleep(0.5)
                sys.stdout.write("\x1b7\x1b[%d;%df%s\x1b8" % (x, y, F"{i}Some shit"))
                sys.stdout.flush()
    elif Loop==False:
        for i in COLORLIST:
            sleep(0.5)
            sys.stdout.write("\x1b7\x1b[%d;%df%s\x1b8" % (x, y, F"{i}Some shit"))
            sys.stdout.flush()
    else:
        print(F"{White}There was an error! Please pick Loops={Red}False{White}/{Green}True{White} or {Green}1/{Red}2{White}")