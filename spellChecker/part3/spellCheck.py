#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from dictionary import Dictionary


def getUserResponse(word, word_options=[]):
    """ Prompts the user for action concerning the specified word.

    Returns a tuple of (response, new_word), where response is the action
    given by the user and new_word is the word entered by the user (or the
    original word if 'Ignore' option was chosen. """

    resp = raw_input("\"{}\" is unknown: Replace (R), replace all (P), ignore (I), "
                     "ignore all (N), or exit (E)?  ".format(word)).lower()
    if resp == 'e':
        print("Spellcheck aborted.")
        sys.exit(0)
    elif resp == 'r' or resp == 'p':
        if word_options:
            for i, w in enumerate(word_options):
                print("( {} ) {}".format(i, w))
            print("( {} ) Use my replacement".format(i+1))
            choice = raw_input("Your choice: ")
            if int(choice) == i+1:
                replacement_word = raw_input("Enter replacement word: ")
            else:
                replacement_word = word_options[int(choice)]
            return (resp, replacement_word)
        else:
            return (resp, raw_input("Enter replacement word: "))
    elif resp == 'i' or resp == 'n':
        return (resp, word)
    else:
        # Ask again
        return getUserResponse(word)


def checkFile(file_name, dictionary_file="words.dat"):
    # Set up dictionary based on words.dat
    d = Dictionary(file_name=dictionary_file)
    d.statistics()

    file_in = open(file_name, 'r')
    file_out = open("{}.out".format(file_name), 'w')

    current_word = ""
    starting_sentence = True

    while True:
        # Read one character at a time from the input file
        next_char = file_in.read(1)
        # Exit the loop when there's nothing else to read
        if not next_char:
            break

        if next_char in d.ALLOWED_LETTERS:
            current_word += next_char
        elif current_word:
            # Verify the current_word with the dictionary
            resp, current_word = d.verify(current_word, 
                    begins_sentence=starting_sentence)
            if not resp:  # Word was not found in dictionary
                resp, new_word = getUserResponse(current_word, 
                        d.find_similar(current_word))
                d.update(resp, current_word, new_word)
                current_word = new_word
            file_out.write(current_word)
            current_word = ""
            file_out.write(next_char)
            # Reset the sentence tracker
            starting_sentence = False
        else:
            file_out.write(next_char)

        if next_char == '.':
            # After we've already handled the word, then check if we're 
            # starting a new sentence.
            starting_sentence = True

    file_in.close()
    file_out.close()
    print("Spellchecked file written to {}.out.".format(file_name))


def main():
    files = sys.argv[1:]

    if not files:
        print("No input file")
        return

    if len(files) > 1:
        print("Cannot spellcheck more than one document at a time")

    checkFile(files[0])


if __name__ == "__main__":
    main()
