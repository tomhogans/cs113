"""
Assignment 4: You must document all the code; points will be
taken off for not having appropriate docstrings for classes,
methods and functions. Please avoid inline documentation unless
absolutely necessary, and ensure that your code compiles on clam
without syntax errors before submitting it.
"""
class Card:
    """This is incomplete!!!"""
    def __init__(self, rank, suit): pass 

    def __str__(self): pass

class Deck:
    """A standard deck of 52 cards"""
    def __init__(self, shuffler):
        """Gets as argument a shuffling strategy (as an object).

        This definition is incomplete!!

        shuffler: an instance of ShuffleStrategy
        """
        self.strategy = shuffler
        self.cards = self.strategy.shuffle(self)

    def dealACard(self):
        """Always deals as the next card, the card on top of the deck.
        Once 'dealt', the card is no longer in the Deck.
        """
        pass

class ShuffleStrategy:
    """An abstract class that promises that all subclasses will provide
    a 'shuffle' method: **do not** modify this.
    """
    def __init__(self, deck):
        """Use the given Deck object to shuffle"""
        self.deck = deck
        
    def shuffle(self):
        raise NotImplementedError()

class Inshuffle(ShuffleStrategy):
    """Implements the in-shuffle, i.e. repeats the following process a random
    number of times (at least 6 and at most 10): interleave cards from the two
    halves of the deck using cards from the top half and the bottom half
    alternately. You will need to provide the shuffle method.
    """
    def shuffle(self):
        pass

class RandomShuffle(ShuffleStrategy):
    """Implements the random shuffling strategy (this code is complete;
    do not modify it). 
    """
    def shuffle(self):
        import random
        n = len(self.deck)
        for i in range(n-1):
            j = random.randint(i+1,n-1)       # swap with random card beyond i^th
            self.deck[i], self.deck[j] = self.deck[j], self.deck[i]
        return self.deck

class Hand:
    """Not implemented at all! You need to complete this."""
    pass
        

def pokerTrials(n=1000000):
    """Simulate dealing, scoring and recording the score of a poker hand for n trials

    The code is incomplete: extend it beyond the code provided below.
    
    n: number of trails
    """
    from collections import defaultdict
    numPokerHands = defaultdict(int)          

    # keys from 1 to 9 for the possible ranks of a poker hand
    # values are the number of hands seen with those ranks.

    for i in range(n):
        # Create a new deck, shuffle if needed, then deal a 5-card poker hand.
        # Rank the hand and increment the associated value in numPokerHands
        pass

    # Compute probabilities for each possible hand and print them
    pass

if __name__=="__main__":
    pokerTrials()
    
    
    
    
