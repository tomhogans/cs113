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
    lines = open(f, 'r').read().splitlines()

    # Assume first line has the rows/columns counts
    height, width = [int(value) for value in lines.pop(0).split()]

    # The next 'height' lines are the actual data
    rows = [lines.pop(0).split() for i in range(height)]

    # Assume all non-blank lines remaining are points we have to process.
    # Make sure we map each result through the int() function so we're left
    # with integer values instead of strings.
    points = [map(int, p.split()) for p in lines if p]

    results = []

    for x, y in points:
        if rows[x][y] == '1':
            results.append('edge')
        else:
            position = "outside"
            for i in range(0, y):
                if rows[x][i] == '1':
                    if position == "outside":
                        position = "inside"
                    else:
                        position = "outside"
            results.append(position)
    
    return results
    
def seatingOrder(f, outp):
    """Return the shortest elapsed time to serve all customers

    See the assignment page describing the function.

    f: name of text file containing input
    outp: name of output file in which output will be written

    >>> seatingOrder("../../data/hw1_2.txt", "hw1_2_out.txt")
    9
    """
    lines = open(f, 'r').read().splitlines()
    stools = {k: 0 for k in range(1, 7)}
    reservations = {}
    seating_history = {}

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
    players = ['Jane', 'John']
    lines = open(f, 'r').read().splitlines()

    # Load Jane and John's cards into down-facing pile; no more than 50 each
    down_pile = {
        'Jane': list(lines[0])[:50],
        'John': list(lines[1])[:50] }
    up_pile = {p: [] for p in players}
    given_results = list(lines[2])

    rounds = 0


    while rounds <= 1000 and given_results:
        rounds += 1

        # If both down piles are empty, flip the up piles over
        if not down_pile['Jane'] and not down_pile['John']:
            down_pile['Jane'] = up_pile['Jane']
            down_pile['John'] = up_pile['John']
            up_pile = {p: [] for p in players}

        if not down_pile['Jane']:
            print("John wins.")
            return

        if not down_pile['John']:
            print("Jane wins.")
            return
        
        # Flip each player's cards over to their up-facing piles
        janes_card = down_pile['Jane'].pop(0)
        johns_card = down_pile['John'].pop(0)
        up_pile['Jane'].insert(0, janes_card)
        up_pile['John'].insert(0, johns_card)

        # Check if there's a SNAP!
        if janes_card == johns_card:
            #winner = random.choice(['Jane', 'John'])
            # For testing purposes, we want to read pre-defined results
            winner = players[int(given_results.pop(0))]
            loser = [person for person in players if person is not winner][0]
            # Winner takes face-up pile from loser
            up_pile[winner] = up_pile[loser] + up_pile[winner]
            up_pile[loser] = []
            print("Snap! for {0}: {1}".format(winner, "".join(up_pile[winner])))

    if rounds > 1000:
        print("Keeps going and going ...")


import itertools
def powerIndex(d):
    """Return a dictionary containing power indices associated with parties.

    See the assignment page describing the function.

    d: a dictionary containing parties (keys) and their membership numbers (values)

    >>> d = {'A': 7, 'B':4,'C':2,'D':6,'E':6}
    >>> w = powerIndex(d)
    >>> print(w['A'], w['C'])
    10 2
    """
    total_votes = sum(d.values())
    majority_threshold = total_votes // 2 + 1
    power_indices = {k: 0 for k in d.keys()}

    for party, party_votes in d.items():
        # Find all parties, excluding the current one
        other_parties = dict((p, v) for p, v in d.items() if p is not party)

        # Find all combinations between 1 and len(other_coalitions)-1 in length
        coalitions = [list(itertools.combinations(other_parties, r)) 
                for r in range(1, len(other_parties))]
        # Flatten the nested lists
        coalitions = list(itertools.chain.from_iterable(coalitions))

        for coalition in coalitions:
            coalition_votes = sum([d[cur_party] for cur_party in coalition])
            if coalition_votes < majority_threshold:
                # `combo` is a minority coalition, so test if their 
                # `combo_votes` + `votes` is enough to make a majority
                if (coalition_votes + party_votes) >= majority_threshold:
                    power_indices[party] += 1

    return power_indices

if __name__=="__main__":
    import doctest
    doctest.testmod()

