#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys

from dictionary import Dictionary, parseWords


def main():
    files = sys.argv[1:]
    d = Dictionary()
    for f in files:
        for word in parseWords(f):
            d.add(word)
    d.save("words.dat")


if __name__ == "__main__":
    main()
