# -*- coding: utf-8 -*-

from collections import defaultdict
import itertools
import string

PHONETIC_PAIRS = [
    ('a', 'e'),
    ('c', 's'),
    ('c', 'k'),
    ('e', 'i'),
    ('g', 'j'),
    ('i', 'y'),
    ('o', 'u'),
    ('v', 'w'),
    ('s', 'z'), ]
PHONETIC_PAIRS = PHONETIC_PAIRS + [(p2, p1) for p1, p2 in PHONETIC_PAIRS]
PHONETIC_PAIRS = PHONETIC_PAIRS + [(p1, p1) for p1, p2 in PHONETIC_PAIRS]


def makehash(word, m):
    """ Hash function that accepts a string of characters and outputs
    an integer between 0 and m-1. """
    if not word:
        return 0
    if len(word) == 1:
        return 26 * ord(word) % m
    return (26 * makehash(word[1:], m) + ord(word[0])) % m

def edits(word):
    """ Generates possible permutations of a given word based on operations
    using the PHONETIC_PAIRS. """
    deletes = [word.replace(p[0], ''.join(p)) for p in PHONETIC_PAIRS]
    inserts = [word.replace(''.join(p), p[0]) for p in PHONETIC_PAIRS]
    subs = [word.replace(p[0], p[1]) for p in PHONETIC_PAIRS]
    swaps = [word.replace(''.join(p), ''.join((p[1], p[0]))) for p in PHONETIC_PAIRS]
    return set(deletes + inserts + subs + swaps)


class Dictionary(dict):
    """ Implements a dict-based object that whose keys are distinct "words"
    (where words are any alphabetic sequence of length two or greater) and
    whose values represent the frequency with which the words appear. When
    words are added with add_word the word and its frequency count is stored
    as a key: value pair in self.  When a words.dat file is loaded, the words
    are stored in two different hash tables.  See save() and load(). """

    ALLOWED_LETTERS = string.ascii_letters + "'"
    WHITESPACE = string.whitespace
    ADDITIONAL_VALID_WORDS = ['a', 'i']
    HASH_LOAD_FACTOR = 5001
    CACHE_SIZE = 500

    def __init__(self, file_name=None):
        """ Constructor that accepts an optional file_name to load words. """
        self.word_list = defaultdict(list)  # Hash table for words
        self.word_cache = defaultdict(list)  # Hash table for most frequent words
        self.replacement_words = {}
        self.ignored_words = []
        [self.add_word(w) for w in self.ADDITIONAL_VALID_WORDS]
        if file_name:
            self.load(file_name)

    def verify(self, word, begins_sentence=False):
        """ Verifies whether the word appears in the dictionary and returns
        a tuple of (result, word), where result is True or False and word is
        either the original word value or a new, replaced word.  If the word
        does not begin a sentence but is capitalized, we assume it's a proper
        noun and does not need to be spellchecked. """
        if not word:
            return (True, "")

        if word[0] == word[0].upper() and not begins_sentence:
            # Ignore proper nouns
            return (True, word)

        if len(word) < 2:
            # Ignore words less than 2 characters
            return (True, word)

        if word.lower() in self.replacement_words.keys():
            return (True, self.replacement_words[word.lower()])

        # Compute hash for word and check both lists
        word_hash = makehash(word.lower(), self.HASH_LOAD_FACTOR)
        if word.lower() in self.word_cache[word_hash]:
            return (True, word)
        if word.lower() in self.word_list[word_hash]:
            return (True, word)

        if word.lower() in self.ignored_words:
            # Don't correct previously 'Ignore All' words
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
        if len(word) < 2:
            return
        word = word.lower()
        if word in self:
            self[word] += 1
        else:
            self[word] = 1

    def find_similar(self, word):
        """ Creates permutations of word via deletions, insertions, 
        substitutions, and transpositions, checking whether the given 
        permutation exists in the dictionary and, if so, returning it in a list
        of up to 10 possible replacements. """
        similar_words = []
        for w in edits(word.lower()):
            word_hash = makehash(w, self.HASH_LOAD_FACTOR)
            if w in self.word_cache[word_hash]:
                similar_words.append(w)
            if w in self.word_list[word_hash]:
                similar_words.append(w)

        # If we found less than 10 results, call edits() on its result to get
        # all permutations with an edit distance of 2 so we can keep looking.
        if len(similar_words) >= 10:
            return similar_words[:10]

        # Create a nested list of all the sets of permutations
        edits_of_edits = [edits(w) for w in edits(word.lower())]
        # Then flatten the list
        edits_of_edits = set(itertools.chain.from_iterable(edits_of_edits))

        for w in edits_of_edits:
            word_hash = makehash(w, self.HASH_LOAD_FACTOR)
            if w in self.word_cache[word_hash]:
                similar_words.append(w)
            if w in self.word_list[word_hash]:
                similar_words.append(w)

        return similar_words[:10]


    def statistics(self):
        print("Stats on Primary Dictionary")
        print("-"*20)
        if self.word_cache:
            print("Length".ljust(10) + "Number of Lists")
            stats = {}
            max_len = len(max(*self.word_cache.values(), key=len))
            for i in range(max_len+1):
                stats[i] = len([l for l in self.word_cache.values() if len(l) == i])
            for k, v in stats.items():
                print("{}".format(k).rjust(4) + "{}".format(v).rjust(14))
        else:
            print "(Empty)"
        print(" ")

        print("Stats on Secondary Dictionary")
        print("-"*20)
        if self.word_list:
            print("Length".ljust(10) + "Number of Lists")
            stats = {}
            max_len = len(max(*self.word_list.values(), key=len))
            for i in range(max_len+1):
                stats[i] = len([l for l in self.word_list.values() if len(l) == i])
            for k, v in stats.items():
                print("{}".format(k).rjust(4) + "{}".format(v).rjust(14))
        else:
            print "(Empty)"

    def save(self, file_name):
        """ Save the words to the specified file_name. """
        try:
            sorted_list = sorted(self, key=self.get, reverse=True)
            with open(file_name, 'w') as file_out:
                [file_out.write("{}\n".format(w)) 
                        for w in sorted_list[:self.CACHE_SIZE]]
                [file_out.write("{}\n".format(w)) 
                        for w in sorted_list[self.CACHE_SIZE:]]
        except IOError as e:
            print(e)

    def load(self, file_name):
        """ Load words from the specified dictionary at file_name. """
        try:
            with open(file_name, 'r') as file_in:
                for i in range(self.CACHE_SIZE):
                    word = file_in.readline().rstrip('\n')
                    if not word:
                        break
                    w_hash = makehash(word, self.HASH_LOAD_FACTOR)
                    self.word_cache[w_hash].append(word)
                while True:
                    word = file_in.readline().rstrip('\n')
                    if not word:
                        break
                    w_hash = makehash(word, self.HASH_LOAD_FACTOR)
                    self.word_list[w_hash].append(word)
        except IOError as e:
            print(e)
