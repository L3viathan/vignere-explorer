# Vignère Explorer

This little toolkit is supposed to help you crack a Vignère cipher. Not in general, of course, since the Vignère cipher is absolutely secure given a random one-time pad. No, I'm talking short-ish keylengths, and some knowledge of the message.

## The Vignère cipher

I won't go into too much detail, but how it essentially works is encrypting each letter with a Caesar cipher, whose setting is determined by the current letter of the encryption key.

**A simple example:**
Say you want to encrypt the message "Hello reader, this text is a secret!" using the key "Coca-Cola"[tm], you first convert both the message and the key to only contain latin letters: `helloreaderthistextisasecret` is your text, `COCACOLA` your key (by convention, cleartext is in lower case, and encrypted text and key are upper-case). We start with the first letter of the text, "h", and shift it by 2 letters, because "C" is the second character after A (given A we don't shift at all, saving us the task of shifting a character a useless 26 times when encountering a Z in the key). The next letter is shifted based on the next letter in our key, O, and therefore by 14 letters (because O is the 15th character in the alphabet), yielding an S, and the next one again 2 letters, because of the C. The fourth letter (l) isn't shifted at all, because the fourth letter of the key is an A. So far, we have the encrypted message `JSNL`, which encrypts `hell`. Continuing, we eventually get `JSNLQFPAFSTTJWDTGLVIUODEEFGT`.

Encrypting using the Vignère Explorer can be done like this:

    $ python3 vignere.py -e cocacola
    helloreaderthistextisasecret

And the output will be:

    JSNLQFPAFSTTJWDTGLVIUODEEFGT

(Note: Vignère Explorer is compatible with both Python 2 and 3, the behaviour is a little bit different, though. With Python 3, once you enter a line, you get the output. Python 2 waits until you supply the complete text (finishing with a ^D), before giving you the output. This is probably related to Python 2 not flushing stdin after one line or something. No idea.)

If you have an encrypted message and you know the key, you just do the whole thing backwards: The J gets moved 2 letters to the "left", becoming an "h", and so on. With this tool:

    $ python3 vignere.py -d cocacola
    JSNLQFPAFSTTJWDTGLVIUODEEFGT

Output:

    helloreaderthistextisasecret

## Interactive Mode
So far, so good. But what if you don't know the key?

There are a few weaknesses of the Vignère, despite it being called unbreakable for centuries. The Kasiski examination looks at repetition of letter groups to determine the key length. Other methods rely on knowing the language the text was written in and make use of known letter distributions (which is easy given knowledge of the key length).

This all is only really useful with longer texts though. The Vignère explorer was built because I was given very short sequences (like in the example above) and suspected them to be Vignère-encrypted.

Because of how the algorithm works when wrapping around the alphabet (it really only is modulo arithmetic), it is commutative: If you know the text, you can get to the key, if you know how the text starts, you can get to that first part of the key and if you know some word contained in the text, you can get possible keys (or key parts), or the key (or part) if you know *where* it occurs. The interactive mode of the Vignère Explorer makes this process of extraction a lot less tedious.

Say you have given the encrypted message above, but have no knowledge of the key. You suspect however, that "secret" might be in it.
You start up the script with the secret word as an argument:

    python3 -m JSNLQFPAFSTTJWDTGLVIUODEEFGT

and enter "secret":

![](https://i.imgur.com/9ECucoE.png)

Directly above the input line, you see what the message would be if it was decrypted with the key "secret". No hit. To the left, you see a `1`, that's the current key size. You can use the arrow keys on your keyboard to increase it. Once it get's to 5, we see a match. However, the decrypted text is gibberish, apart from the "secret" part. At 6, you can spot something, if you look close: The last line starts with "hell", ends with "secret", and the key is "COCALA". If you catch that, you might as well try COCACOLA as a key, but let's increase it up to the actual key length, 8:

![](http://i.imgur.com/uAqRE1A.png)

Eureka! What happens to be the last line contains not only the correct text (minus a few blanks), but also the almost complete key! If you got there, you might further guess that the `eadert` part was either "leader" or "reader", and try them both (with the "t" appended), if you do that, you'll find the line `hell_readert_istexti_asecret (COCA_OLA)`, which confirms our previous findings and renders the task absolutely trivial. You can then either quit the tool (with Esc-Esc, or Ctrl-C), or replace the current word with `COCACOLA` and see the decoded text in the interactive mode.
