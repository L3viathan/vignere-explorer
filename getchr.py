import tty
import sys
import glob
import subprocess
import os
import termios

BOLD='\033[1m'
END='\033[0m'

n = open("/dev/null","w")

def getchr():
    #import termios, sys, tty
    fd = sys.stdin.fileno()
    old = termios.tcgetattr(fd)
    tty.setraw(sys.stdin.fileno())
    ch = sys.stdin.read(1)
    termios.tcsetattr(fd,termios.TCSADRAIN,old)
    if ord(ch) == 3: sys.exit(0) #^C
    return ch

def iterchr():
    while True:
        yield getchr()

def replaceLine(what):
    print(" "*80,end='\r')
    print(what,end='\r')

def fuzzymatch(req,ls):
    if req == "": return (False,False)
    for candidate in ls:
        reqc = req
        formatted = ""
        for char in candidate:
            if len(reqc) and char.lower() == reqc[0]:
                reqc = reqc[1:]
                formatted += BOLD + char + END
            else:
                formatted += char
        if len(reqc) == 0: return (candidate,formatted)
    return (False,False)

if __name__ == "__main__":
    targets = glob.glob("*")

    string, result,raw = "","",""
    for i in iterchr():
        if ord(i) == 27: #escape
            string = ""
        elif ord(i) == 13: #enter
            replaceLine("Playing " + raw);
            subprocess.call(["mplayer",raw],stdout=n,stderr=n)
            print();
            break
        elif ord(i) == 127: #backspace
            if len(string): string = string[:-1]
        else: string += i.lower()
        (raw,result) = fuzzymatch(string,targets)
        if result:
            replaceLine("Wanna play " + result + "?")
        else:
            replaceLine("Looking for " + string)


    #os.system("setterm -cursor on")
