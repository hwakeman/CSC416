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
        self.facts = set()

    def ask(self, sentence):
        """
        Return whether the given sentence input is true in the World.
        For example, we want to be able to ask, W[1,1]? Then return False if no wumpus.
        """
        if isinstance(sentence, str):
            return sentence in self.facts # states of the world we've gathered
        
        operator, *operands = sentence

        if operator == 'NOT':
            return not self.ask(operands[0])
        
        elif operator == 'AND':
            return all(self.ask(op) for op in operands)
        
        elif operator == 'OR':
            return any(self.ask(op) for op in operands)
        
        elif operator == 'IMPLIES':
            return not self.ask(operands[0]) or self.ask(operands[1])
        
        elif operator == 'IFF':
            return self.ask(operands[0]) == self.ask(operands[1])

    def tell(self, sentence):
        """
        Give the world a sentence and tell it that this sentence is true.
        """
        self.facts.add(sentence)

class Player:
    """
    The Player in the Wumpus World.
    The Player should be able to (1) make inference
    """

    def __init__(self, kb):
        self.kb = kb
    
    def make_inferences(self, query):
        """
        Given the Player's knowledge base, determine whether the given query is true.
        """
        facts, implications, bidirectionals = self._transform_kb()

        # set up a flag that tells us we need to derive new propositions
        world = World()

        # add the base facts to the world
        for fact in facts:
            world.tell(fact)

        more_to_derive = True
        while more_to_derive:
            more_to_derive = False
            for premise, conclusion in implications:
                if world.ask(premise) and not world.ask(conclusion):
                    world.tell(conclusion)
                    more_to_derive = True

            for a,b in bidirectionals:
                if world.ask(a) and not world.ask(b):
                    world.tell(b)
                    more_to_derive = True
                
                if world.ask(b) and not world.ask(a):
                    world.tell(a)
                    more_to_derive = True

        return world.ask(query)
    
    def _transform_kb(self):
        """
        Transform the knowledge to seperate its sentences into facts,
        implications, and bidirectionals
        """

        facts = set()
        implications = []
        bidirectionals = []

        for sentence in self.kb:
            if isinstance(sentence, str):
                # singleton strings represent simple facts
                facts.add(sentence)
                continue

            if isinstance(sentence, tuple):
                connective = sentence[0]
                if connective == 'IMPLIES':
                    premise, conclusion = sentence[1:]
                    implications.append((premise, conclusion))
                elif connective == 'IFF':
                    a, b = sentence[1:]
                    bidirectionals.append((a,b))
                elif connective in ['NOT', 'OR', 'AND']:
                    facts.add(sentence)
        
        return facts, implications, bidirectionals

    def inference_by_resolution(self, query):
        """
        This will be the main method that you will call to
        perform inference by resolution.
        """
        pass

    def resolve(self, cnf_1, cnf_2):
        """
        Takes a pair of CNFs and returns a list of resolved CNFs.
        """
        pass

    def sentence_to_cnf(self, sentence):
        """
        Converts a propositional logic sentence into CNF using a recursive approach.
        """
        if isinstance(sentence, str) or (sentence[0] not in {'IMPLIES', 'IFF'}):
            return sentence

        sentence1 = self.sentence_to_cnf(sentence[1]) if isinstance(sentence[1], tuple) else sentence[1]
        sentence2 = self.sentence_to_cnf(sentence[2]) if isinstance(sentence[2], tuple) else sentence[2]

        if sentence[0] == 'IFF':
            return ('AND', ('OR', ('NOT', sentence1), sentence2), ('OR', ('NOT', sentence2), sentence1))

        if sentence[0] == 'IMPLIES':
            return ('OR', ('NOT', sentence1), sentence2)

        return (sentence[0], sentence1, sentence2)

if __name__ == '__main__':
    initial_kb = [
        'P',
        ('IMPLIES', 'P', 'Q'),
    ]

    initial_kb_2 = [
        ('NOT', 'B11'), 
        ('IFF', 'B11', ('OR', 'P12', 'P21'))
    ]

    player = Player(kb=initial_kb)
    player_2 = Player(kb=initial_kb_2)

    query = 'Q'
    query_2 = ('NOT', 'Q')
    query_3 = 'P21'

    print("Q: " + player.inference_by_resolution(query))
    print("Not Q: " + player.inference_by_resolution(query_2))
    print("P21: " + player_2.inference_by_resolution(query_3))