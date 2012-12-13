# -*- coding: utf-8 -*-

import string


class Dictionary:
    """ Implements a dict-based object that whose keys are distinct "words"
    (where words are any alphabetic sequence of length two or greater) and
    whose values represent the frequency with which the words appear. """

    ALLOWED_LETTERS = string.ascii_letters
    ADDITIONAL_VALID_WORDS = ['a', 'i']

    def __init__(self, file_name=None):
        """ Constructor that accepts an optional file_name to load words. """
        self.word_list = {}  # Dict of {word: frequency}
        self.replacement_words = {}
        self.ignored_words = []
        [self.add_word(w) for w in self.ADDITIONAL_VALID_WORDS]
        if file_name:
            self.load(file_name)

    def verify(self, word):
        """ Verifies whether the word appears in the dictionary and returns
        a tuple of (result, word), where result is True or False and word is
        either the original word value or a new, replaced word. """
        if len(word) < 2:
            return (True, word)

        if word.lower() in self.replacement_words.keys():
            return (True, self.replacement_words[word.lower()])

        if word.lower() in self.word_list:
            return (True, word)

        if word.lower() in self.ignored_words:
            return (True, word)

        return (False, word)

    def update(self, action, word, new_word=None):
        if action.lower() == 'p':  # Replace all
            self.replacement_words[word.lower()] = new_word
        elif action.lower() == 'n':  # Ignore all
            self.ignored_words.append(word.lower())

    def add_word(self, word):
        """ Adds word with a frequency of 1.  If word already exists, 
        increment that key's value by 1 to indicate it was seen again. """
        word = word.lower()
        if word in self.word_list:
            self.word_list[word] += 1
        else:
            self.word_list[word] = 1

    def save(self, file_name):
        """ Save the words to the specified file_name. """
        try:
            open(file_name, 'w').write("\n".join(self.word_list.keys()))
        except IOError as e:
            print(e)

    def load(self, file_name):
        """ Load words from the specified dictionary at file_name. """
        try:
            [self.add_word(w) for w in open(file_name).read().splitlines()]
        except IOError as e:
            print(e)
