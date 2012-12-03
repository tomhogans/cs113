# -*- coding: utf-8 -*-

import string


class Dictionary(dict):
    """ Implements a dict-based object that whose keys are distinct "words"
    (where words are any alphabetic sequence of length two or greater) and
    whose values represent the frequency with which the words appear. """

    def __init__(self, file_name=None):
        """ Constructor that accepts an optional file_name to load words. """
        if file_name:
            self.load(file_name)

    def add(self, word):
        """ Adds word with a frequency of 1.  If word already exists, 
        increment that key's value by 1 to indicate it was seen again. """
        word = word.lower()
        if word in self:
            self[word] += 1
        else:
            self[word] = 1

    def save(self, file_name):
        """ Save the words to the specified file_name. """
        try:
            open(file_name, 'w').write("\n".join(self.keys()))
        except IOError as e:
            print(e)

    def load(self, file_name):
        """ Load words from the specified dictionary at file_name. """
        try:
            with open(file_name, 'w') as f:
                while True:
                    next_word = f.readline()
                    if not next_word:
                        break
                    self.add_word(next_word)
        except IOError as e:
            print(e)
        


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
                        yield current_word
                    current_word = ""
    except IOError as e:
        print(e)
