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
        # CNF The kb and add the negated query to it
        kb_with_negated_query = [self.sentence_to_cnf(i) for i in self.kb]
        kb_with_negated_query.append(('NOT', self.sentence_to_cnf(query)))
        
        while True:
            # Comparing each clause with every other clause in the kb
            for i in range(len(kb_with_negated_query) - 1):
                for j in range(i + 1, len(kb_with_negated_query)):
                    resolved = self.resolve(kb_with_negated_query[i], kb_with_negated_query[j])

                    # Check if this is the last possible pair of clauses, if it is we return True when the kb contradicts itself and False when it doesn't
                    if set(resolved).issubset(set(kb_with_negated_query)) and i + 2 == len(kb_with_negated_query) and j + 1 == len(kb_with_negated_query):
                        if query in kb_with_negated_query and ('NOT', query) in kb_with_negated_query:
                            return True
                        else:
                            return False
                        
                    # If this is not the last possible pair of clauses, simply add the new clause to the kb if it isn't already
                    else:
                        for clause in resolved:
                            if clause not in kb_with_negated_query:
                                kb_with_negated_query.append(clause)

    def resolve(self, clause_1, clause_2):
        """
        Takes a pair of CNFs and returns a list of resolved CNFs. 
        """
        def is_complementary(lit1, lit2):
            """
            Simple helper function that determines if two literals are complementary
            """
            if isinstance(lit1, tuple) and lit1[0] == 'NOT' and lit1[1] == lit2:
                return True
            
            if isinstance(lit2, tuple) and lit2[0] == 'NOT' and lit2[1] == lit1:
                return True
                
            return False

        def get_literals(clause):
            """
            Helper function to take a clause and extract the literals from it
            """
            if isinstance(clause, tuple) and clause[0] == 'OR':
                literals = []
                for part in clause[1:]:
                    literals.extend(get_literals(part))
                return literals
            
            return [clause]

        def remove_literal(clause, literal):
            """
            Helper function to remove a specific literal from a clause.
            """
            if isinstance(clause, tuple) and clause[0] == 'OR':
                # Takes all of the clauses in the tuple that aren't the literal to be removed and puts them in a new tuple
                remaining_literals = tuple(lit for lit in clause[1:] if lit != literal)
                return ('OR', *remaining_literals) if remaining_literals else None
            
            return None if clause == literal else clause

        literals_1 = get_literals(clause_1)
        literals_2 = get_literals(clause_2)

        resolved_clauses = []

        for literal_1 in literals_1:
            for literal_2 in literals_2:
                # If there are complementary literals they must be removed
                if is_complementary(literal_1, literal_2):
                    new_clause_1 = remove_literal(clause_1, literal_1)
                    new_clause_2 = remove_literal(clause_2, literal_2)

                    # If both clauses still contain literals after removal we must combine the remaining literals with 'OR'
                    if new_clause_1 and new_clause_2:
                        resolved = ('OR', get_literals(new_clause_1), get_literals(new_clause_2))

                    # If only clause_1 has remaining literals, use it as the resolved clause
                    elif new_clause_1:
                        resolved = new_clause_1

                    # If only clause_2 has remaining literals, use it as the resolved clause
                    elif new_clause_2:
                        resolved = new_clause_2

                    # If both clauses are empty after removing complementary literals, return an empty clause
                    else:
                        resolved = None

                    # If the resolved clause has only one literal, we must remove the 'OR' and keep the single literal
                    if isinstance(resolved, tuple) and resolved[0] == 'OR' and len(resolved) == 2:
                        resolved = resolved[1] 

                    # Add the resolved clause to the list of resolved clauses, if it exists
                    if resolved:
                        resolved_clauses.append(resolved)
        
        return resolved_clauses
        
    def sentence_to_cnf(self, sentence):
        """
        Converts a propositional logic sentence into CNF using a recursive approach.
        """
        # If the sentence is a literal or does not have 'IMPLIES' or 'IFF' in it, the sentence is already in CNF
        if isinstance(sentence, str) or (sentence[0] not in {'IMPLIES', 'IFF'}):
            return sentence

        # We need to recursively call the function on any nested tuples
        sentence_1 = self.sentence_to_cnf(sentence[1]) if isinstance(sentence[1], tuple) else sentence[1]
        sentence_2 = self.sentence_to_cnf(sentence[2]) if isinstance(sentence[2], tuple) else sentence[2]

        # P⇔Q is just (￢P⋁Q) ⋀ (￢Q⋁P)!
        if sentence[0] == 'IFF':
            return ('AND', ('OR', ('NOT', sentence_1), sentence_2), ('OR', ('NOT', sentence_2), sentence_1))

        # P⇒Q is just ￢P⋁Q!
        if sentence[0] == 'IMPLIES':
            return ('OR', ('NOT', sentence_1), sentence_2)

        return (sentence[0], sentence_1, sentence_2)

if __name__ == '__main__':
    initial_kb = [
        'P',
        ('IMPLIES', 'P', 'Q'),
    ]

    initial_kb_2 = [
        ('NOT', 'B11'), 
        ('IFF', 'B11', ('OR', 'P12', 'P21'))
    ]

    # Minimal tests to pass

    player = Player(kb=initial_kb)
    player_2 = Player(kb=initial_kb_2)

    query = 'Q'
    query_2 = ('NOT', 'Q')
    query_3 = 'P21'

    print("Q: " + str(player.inference_by_resolution(query)))
    print("Not Q: " + str(player.inference_by_resolution(query_2)))
    print("P21: " + str(player_2.inference_by_resolution(query_3)))
