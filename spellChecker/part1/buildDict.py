#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import string

from dictionary import Dictionary


def parseWords(file_name):
    """ Reads in the specified text field and yields a word whenever a 
    sequence of two or more ASCII letters (a-z) are followed by a non-
    alphabetic character.  It is case insensitive and always yields a
    lower-case version of the word it is emitting. """

    current_word = ""
    try:
        with open(file_name, 'r') as f:
            while True:
                next_char = f.read(1)
                if not next_char:
                    break
                if next_char in string.ascii_letters:
                    current_word += next_char
                else:
                    if len(current_word) > 1:
                        yield current_word.lower()
                    current_word = ""
    except IOError as e:
        print(e)


def main():
    files = sys.argv[1:]
    d = Dictionary()
    for f in files:
        for word in parseWords(f):
            d.add_word(word)
    d.save("words.dat")


if __name__ == "__main__":
    main()
