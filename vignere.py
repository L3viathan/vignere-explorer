# coding=utf-8
from __future__ import division, print_function, absolute_import
from getchr import *
def add(x,y):
    if x == "_" or y == "_":
        return "_"
    return chr((((ord(x)-65)+(ord(y)-65)) % 26)+65)
def sub(x,y):
    if x == "_" or y == "_":
        return "_"
    return chr((((ord(x)-65)-(ord(y)-65)) % 26)+65)
def adds(a,b):
    return "".join([add(x,y) for (x,y) in zip(a,b)])
def subs(a,b):
    return "".join([sub(x,y) for (x,y) in zip(a,b)])
def encode(text, key):
    text, key = clean(text), clean(key)
    ret = ""
    while len(text) > len(key):
        ret += adds(text, key)
        text = text[len(key):]
    ret += adds(text, key[:len(text)])
    return ret
def decode(text, key):
    text, key = clean(text), clean(key)
    if len(key)> len(text):
        key = key[:len(text)]
    ret = ""
    while len(text) > len(key):
        ret += subs(text, key)
        text = text[len(key):]
    ret += subs(text, key[:len(text)])
    return ret
def clean(text):
    return "".join(filter(lambda x: x in "ABCDEFGHIJKLMNOPQRSTUVWXYZ_",text.upper()))

def is_repetition(hay, needle):
    hay, needle = clean(hay), clean(needle)
    if not hay or not needle:
        return True
    return hay[0] == needle[0] and is_repetition(hay[1:], needle[1:] + needle[0])
def build_key_from_part(keypart, index, length):
    keypart = clean(keypart)
    keypart = keypart[:length]
    keypart = keypart[index:] + "_" * (length-len(keypart)) + keypart[:index]
    return keypart
def guess_key(crypt, guess, length=3):
    '''Returns list of tuples of guesses for given key length'''
    solutions = []
    for i in range(len(crypt)-len(guess)+1):
        crypart = crypt[i:i+len(guess)]
        keypart = subs(crypart, guess)
        if len(keypart) > length:
            if not is_repetition(keypart, keypart[:length]):
                continue
        decoded = False
        for n in range(length):
            key = build_key_from_part(keypart, (i+n) % length, length)
            decoded = decode(crypt, key)
            if guess in decoded:
                break
        if decoded and guess in decoded:
            solutions.append((decoded, key))
    return solutions

if __name__ == '__main__':
    if len(sys.argv) > 1:
        args = sys.argv[1:]
        if args[0] == "-m":
            crypt = "".join(args[1:])
        elif args[0] == "-d":
            for line in sys.stdin:
                print(decode(line,args[1]).lower())
            sys.exit()
        elif args[0] == "-e":
            for line in sys.stdin:
                print(encode(line,args[1]))
            sys.exit()
    else:
        print('''Usage:
        python3 vignere.py -d|-e <key>              #en/decodes stdin
        python3 vignere.py -m <encrypted_message>   #starts interactive mode

In interactive mode, enter possible keys or expected message parts,
use arrow keys (up and down) to change expected key size.''')
        sys.exit()
    buffr = ""
    key_length = 1
    while True:
        print(chr(27) + "[2J")
        results = guess_key(crypt, buffr, key_length)
        for text, key in results:
            print(text.lower(), "(" + key + ")")
        else:
            print()
        if len(buffr) > 1:
            print("<" + buffr + ">:", decode(crypt, buffr).lower())
        sys.stdout.flush()
        print("[↕"+ str(key_length) + "]> " + buffr.lower(), end="")
        sys.stdout.flush()
        char = getchr()
        sys.stdout.flush()
        if char == "\x1b":
            char = getchr()
            if char == "\x1b":
                sys.exit()
            char = getchr()
            if char == "A":
                key_length += 1
            elif char == "B" and key_length > 1:
                key_length -= 1
        elif char == "\x7f": #backspace
            if buffr:
                buffr = buffr[:-1]
                buffr = clean(buffr)
        else:
            buffr += clean(char)
