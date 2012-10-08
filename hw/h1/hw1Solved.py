"""
Programming Assignment 1
Handed out: 9/12/12
Due back: 9/26/12 by midnight
"""

def int_list(s):
    """Return a list of integers that comprise a string ending in a newline.

    s: string that ends in a newline (comes from a file)
    """
    nList = s.rstrip().split()
    return [int(k) for k in nList]

def locate(f):
    """Return a list containing possible values 'inside', 'outside' or 'edge'
    
    See the assignment page describing the function.

    f: name of text file containing input

    >>> print( locate("../../data/hw1_1.txt"))
    ['inside', 'edge', 'outside']
    """
    f_handle = open(f, 'r')
    m, n = int_list(f_handle.readline())      # read num of rows, columns
    table = []
    for i in range(m):
        tableRow = int_list(f_handle.readline()) # read next row of table
        table.append(tableRow)
    # read and process queries
    result = []
    query = f_handle.readline()
    while(query.strip()):
        [r, c] = int_list(query)
        if table[r][c] == 1:
            result.append('edge')
        else:                          # count the ones parity within row to a boundary.
            if sum(table[r][:c])%2==0:
                result.append('outside')
            else:
                result.append('inside')
        query = f_handle.readline()
    return result

def seatingOrder(f, outp):
    """Return the shortest elapsed time to serve all customers

    See the assignment page describing the function.

    f: name of text file containing input
    outp: name of output file in which output will be written

    >>> seatingOrder("../../data/hw1_2.txt", "hw1_2_out.txt")
    9
    """
    f_handle = open(f, 'r')
    o_handle = open(outp, 'w')
    w = f_handle.readlines()
    f_handle.close()
    # queue of customers waiting to be serviced: each entry is (arr_time, svc_time)
    customers = []                      
    while len(w)>=2:
        arr_time = int_list(w[0])[0]     # next wave starts
        sTimes = sorted(int_list(w[1]))
        sTimes.reverse()
        customers += [(arr_time, svc_time) for svc_time in sTimes]
        w = w[2:]

    # Note: for the same arrival time, customers are queued in decreasing order
    # of service time
    start = min(customers)[0]
    # keys are times; values are list of stools that will become available at that time
    avail = {start: list(range(6))}
    stools = []
    while customers:
        # find the first available time for seating
        t = min(avail)

        stools += avail[t]
        del avail[t]
        out_line = [' _' for i in range(6)]
        while customers and stools:
            if customers[0][0] <= t:
                i = stools.pop(0)
                svc_time = customers[0][1]
                customers.pop(0)
                out_line[i] = ' '+str(svc_time)
                avail[t+svc_time] = avail.get(t+svc_time, [])+[i]
            else:
                break
        else:
            # print output line:
            o_handle.write(str(t)+''.join(out_line)+'\n')
    o_handle.close()
    return max(avail)-start

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
    'John wins.'
    """
    f_handle = open(f, 'r')
    names = ['Jane', 'John']
    facedownPiles = dict()
    faceupPiles = dict()
    # index 0 for Jane, index 1 for John
    for i in range(2):
        facedownPiles[i] = f_handle.readline().rstrip()
        faceupPiles[i] = ''
    snapWinners = f_handle.readline().rstrip()
    f_handle.close()
    s = snapWinners[:]
    cards = dict()
    turns = 0
    while turns < 1000:    # both facedown piles are non-empty
        turns += 1
        assert len(facedownPiles[0])>0 and len(facedownPiles[1])>0 
        for i in range(2):
            cards[i] = facedownPiles[i][0]
            facedownPiles[i] = facedownPiles[i][1:]
            faceupPiles[i] = cards[i]+faceupPiles[i]
        if cards[0]==cards[1]:    # simulate snap!
            winner = int(s[0])
            s = s[1:]
            if len(s)==0:
                s = snapWinners[:]
            faceupPiles[winner] = faceupPiles[1-winner] + faceupPiles[winner]
            faceupPiles[1-winner] = ''
            print("Snap! for "+names[winner]+": "+faceupPiles[winner])
        for i in range(2):
            lup = len(faceupPiles[i])
            if len(facedownPiles[i])==0:
                if lup==0:
                    return names[1-i]+' wins.'
                else:
                    facedownPiles[i] = faceupPiles[i][-1:-(lup+1):-1]
                    faceupPiles[i] = ''
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
    import math
    n = len(d)
    votes = sum(d[k] for k in d)
    majority = votes//2 + 1               # needed for a majority.
    parties = list(d.keys())
    subsetVotes = dict()
    for i in range(int(math.pow(2,len(d)))):
        bits = bin(i)[2:]
        if len(bits)<n:
            bits = '0'*(n-len(bits)) + bits
        # treat bits as a subset: 0 bit indicates absence, 1 indicates presence
        subset = [parties[k] for k in range(n) if bits[k]=='1']
        subsetVotes[bits] = sum(d[k] for k in subset)
    result = dict()
    for p in parties:
        posn = parties.index(p)
        vitalSets = 0
        for b in subsetVotes:
            v = subsetVotes[b]
            if b[posn]=='0' and v<majority and v+d[p]>=majority:
                vitalSets += 1
        result[p] = vitalSets
    return result


if __name__=="__main__":
    import doctest
    doctest.testmod()

