"""
We want to write a program that consists of
1. The Wumpus World
2. A Player / Agent that has limited visibility of the world but can collect percepts
and perform logic inference.

"""

class World:
    """
    The Wumpus World.
    """
    def __init__(self):
        """
        Initialize the state of the game, where the Wumpus is, where the pits are, etc.
        Represent the entities in the world
        - Maybe 2d array to represent the grid.
        """
        pass

    def ask(self, sentence):
        """
        Return whether the given sentence input is true in the World.
        For example, we want to be able to ask, W[1,1]? Then return False if no wumpus.
        """
        pass

class Player:
    """
    The Player in the Wumpus World.
    The Player should be able to (1) make inference

    """

    def __init__(self, kb):
        self.kb = kb
    
    def make_inference(self):
        """
        Given the Player's knowledge base, determine whether the given query is true.
        """
        return False

if __name__ == '__main__':
    # the initial knowledge base for the player
    initial_kb = [
        ('NOT', 'P11'),
        ('NOT', 'W11'),
        ('NOT', 'B11'),
        ('NOT', 'S11'),
        ('IFF', 'B11', ('OR', 'P12', 'P21'))
    ]
    # our question - is there a pit in [2,1] (so that we can move there)
    query = 'P21' # we expect the answer to be False or ('NOT', 'P21') to be true
    # kb = {"1.1": [not p, not w, not b, not s]}
    player = Player(kb=initial_kb)
    player.make_inference(query) # -> either True or False