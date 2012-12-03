#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import string

from dictionary import Dictionary


ADDITIONAL_VALID_WORDS = ['a', 'i']


def getUserResponse(word):
    """ Prompts the user for action concerning the specified word.

    Returns a tuple of (response, new_word), where response is the action
    given by the user and new_word is the word entered by the user. """

    resp = raw_input("\"{}\": Replace (R), replace all (P), ignore (I), "
                     "ignore all (N), or exit (E)?  ".format(word)).lower()
    if resp == 'e':
        print("Spellcheck aborted.")
        sys.exit(0)
    elif resp == 'r':
        return ('r', raw_input("Enter replacement word: "))
    elif resp == 'p':
        return ('p', raw_input("Enter replacement word: "))
    elif resp == 'i':
        return ('i', word)
    elif resp == 'n':
        return ('n', word)
    else:
        # Ask again
        return getUserResponse(word)


def main():
    files = sys.argv[1:]

    if not files:
        print("No input file")
        return

    if len(files) > 1:
        print("Cannot spellcheck more than one document at a time")

    file_name = files[0]

    # Set up dictionary based on words.dat
    d = Dictionary(file_name="words.dat")
    [d.add_word(w) for w in ADDITIONAL_VALID_WORDS]

    file_in = open(file_name, 'r')
    file_out = open("{}.out".format(file_name), 'w')

    replacements = {}
    ignored_words = []
    current_word = ""

    while True:
        next_char = file_in.read(1)
        if not next_char:
            break
        if next_char in string.ascii_letters:
            current_word += next_char
        else:
            if len(current_word) > 1:
                # Check if we should automatically ignore or replace the word
                if current_word.lower() in ignored_words:
                    # Take no action
                    pass
                elif current_word.lower() in replacements:
                    # Replace the word with previously specified word
                    current_word = replacements[current_word]
                else:
                    # No automatic action taken, so check if it's OK
                    if not current_word.lower() in d:
                        (resp, new_word) = getUserResponse(current_word)
                        if resp is 'r':
                            current_word = new_word
                        elif resp is 'p':
                            replacements[current_word.lower()] = new_word
                            current_word = new_word
                        elif resp is 'i':
                            # Ignore misspelled word this time
                            pass
                        elif resp is 'n':
                            ignored_words.append(current_word)
                file_out.write(current_word)
            else:
                file_out.write(current_word)
            current_word = ""
            file_out.write(next_char)

    print("Spellchecked file written to {}.out.".format(files[0]))


if __name__ == "__main__":
    main()
