# -*- coding: utf-8 -*-


class Dictionary(dict):
    """ Implements a dict-based object that whose keys are distinct "words"
    (where words are any alphabetic sequence of length two or greater) and
    whose values represent the frequency with which the words appear. """

    def __init__(self, file_name=None):
        """ Constructor that accepts an optional file_name to load words. """
        if file_name:
            self.load(file_name)

    def add_word(self, word):
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
            [self.add_word(w) for w in open(file_name).read().splitlines()]
        except IOError as e:
            print(e)
