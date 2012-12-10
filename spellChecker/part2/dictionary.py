# -*- coding: utf-8 -*-


import operator


class Dictionary():
    """ Implements a dict-based object that whose keys are distinct "words"
    (where words are any alphabetic sequence of length two or greater) and
    whose values represent the frequency with which the words appear. """

    def __init__(self, file_name=None):
        """ Constructor that accepts an optional file_name to load words. """
        # Cache of frequent words
        self.frequent_words = {}
        # Dictionary of all other words
        self.words = {}
        # List of words to ignore when spell checking.
        self.ignore_words = []
        # Dictionary where keys are words to find when spell checking and
        # the values are the replacement words.
        self.replace_words = {}
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
        """ Save the words to the specified file_name. Before writing to the
        file, sort the words by frequency and save the top 500 words to a
        frequent_words list.  Items from frequent_words are written to the
        file before the other words. """

        self.frequent_words = sorted(self, key=operator.itemgetter(1), 
                reverse=True)[:5]
        map(self.keys(), lambda x: self.pop(x) if x in self.frequent_words)

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

    def verify(self, word):
        """ Verifies the replacement word supplied by the user during the
        spellCheck program. If it finds the word in the data structures that 
        it maintains then it returns a 'new word' that must be output. 
        Otherwise, it returns None."""
        if word.lower() in self.ignore_words:
            return None
        if word.lower() in self.replace_words:
            return self.replace_words[word.lower()]

    def update(self, word, action):
        """ Updates internal data structures in response to the action 
        specified by the user at the occurrence of an unknown word.  Action
        is represented by the single character response from the user. """
        if action.lower() is 'p':
            self.replace_words.append(word.lower())
        elif action.lower() is 'n':
            self.ignore_words.append(word.lower())
