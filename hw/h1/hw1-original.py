"""
Programming Assignment 1
Handed out: 9/12/12
Due back: 9/26/12 by midnight
"""

def locate(f):
    """Return a list containing possible values 'inside', 'outside' or 'edge'
    
    See the assignment page describing the function.

    f: name of text file containing input

    >>> print( locate("../../data/hw1_1.txt"))
    ['inside', 'edge', 'outside']
    """
    return []

def seatingOrder(f, outp):
    """Return the shortest elapsed time to serve all customers

    See the assignment page describing the function.

    f: name of text file containing input
    outp: name of output file in which output will be written

    >>> seatingOrder("../../data/hw1_2.txt", "hw1_2_out.txt")
    9
    """
    return 0

import random
def snap(f):
    """Return who wins the game of snap

    See the assignment page describing the function.

    f: name of text file containing input

    >>> snap("../../data/hw1_3.txt")
    Snap! for Jane: BCBA
    Snap! for Jane: DADCBCBA
    Snap! for John: CBAC
    Snap! for John: ADADCBAC
    John wins.
    """
    return "Keeps going and going ..."

def powerIndex(d):
    """Return a dictionary containing power indices associated with parties.

    See the assignment page describing the function.

    d: a dictionary containing parties (keys) and their membership numbers (values)

    >>> d = {'A': 7, 'B':4,'C':2,'D':6,'E':6}
    >>> w = powerIndex(d)
    >>> print(w['A'], w['C'])
    10 2
    """
    return dict()

if __name__=="__main__":
    import doctest
    doctest.testmod()

