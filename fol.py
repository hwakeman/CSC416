import re

def unify(sentence1, sentence2):
    """
    Unifies two FOL sentences, returning a dictionary of variable substitutions if any exist
    """

    # Split sentences into their components
    sentence1_components = re.split(r'[(),]', sentence1)
    sentence1_components = [component.strip() for component in sentence1_components if component]

    sentence2_components = re.split(r'[(),]', sentence2)
    sentence2_components = [component.strip() for component in sentence2_components if component]

    # Check if the two sentences have the same number of components
    if len(sentence1_components) != len(sentence2_components):
        return {}  # Unification not possible if they don't match in structure

    variable_substitutions = {}

    for component1, component2 in zip(sentence1_components, sentence2_components):
        # We have to check whether the components are a constant or a variable
        if component1.islower() and component2.islower():
            # Both component1 and component2 are variables so no substitutions are necessary
            continue
        elif component1.islower():
            # component1 is a variable and component2 is a constant, substitutions might be necessary
            if component1 in variable_substitutions:
                if variable_substitutions[component1] != component2:
                    return {}  # Conflict in substitutions
            else:
                variable_substitutions[component1] = component2  # Add new substitution
        elif component2.islower():
            # component1 is a constant and component2 is a variable, substitutions might be necessary
            if component2 in variable_substitutions:
                if variable_substitutions[component2] != component1:
                    return {}  # Conflict in substitutions
            else:
                variable_substitutions[component2] = component1  # Add new substitution

    return variable_substitutions

def inference_by_resolution(kb, query):
    """
    Performs inference by resolution for an FOL KB.
    """

    # Negate the query and add it to the knowledge base
    negated_query = ['¬' + query] if query[0] != '¬' else [query[1:]]
    kb_with_negated_query = kb + [negated_query]
    
    while True:
        new_clauses = []
        # Compare each kb clause with every other kb clause
        for i in range(len(kb_with_negated_query) - 1):
            for j in range(i + 1, len(kb_with_negated_query)):
                # Resolve the two clauses
                resolved = resolve(kb_with_negated_query[i], kb_with_negated_query[j])
                
                # Add new resolved clauses to new_clauses if they aren't already in the kb
                for clause in resolved:
                    if clause not in kb_with_negated_query and clause not in new_clauses:
                        new_clauses.append(clause)

                # If an empty clause is found, return True (the query can be inferred)
                if [] in resolved:
                    return True

        # If no new clauses are generated, return False (the query cannot be inferred)
        if not new_clauses:
            return False
        
        kb_with_negated_query += new_clauses


def resolve(clause_1, clause_2):
    """
    Takes two clauses (lists of literals) and returns a list of resolved clauses using unification.
    """

    def get_substitutions(lit1, lit2):
        """
        Gets the possible substitutions between two literals
        """
        if lit1.startswith('¬'):
            return unify(lit1[1:], lit2)
        
        elif lit2.startswith('¬'):
            return unify(lit1, lit2[1:])
        
        return None

    def remove_literal(clause, literal):
        """
        Removes a specific literal from a clause.
        """
        return [lit for lit in clause if lit != literal]

    def apply_substitution(literal, substitution):
        """
        Apply the unification substitution to a given literal.
        """
        for key, value in substitution.items():
            literal = literal.replace(key, value)
            
        return literal

    resolved_clauses = []

    # Iterate over literals in both clauses
    for literal_1 in clause_1:
        for literal_2 in clause_2:
            # Check for complementary literals using unification
            substitution = get_substitutions(literal_1, literal_2)

            if substitution is not None:
                # Remove the complementary literals
                new_clause_1 = remove_literal(clause_1, literal_1)
                new_clause_2 = remove_literal(clause_2, literal_2)

                # Apply the substitution to the remaining literals
                new_clause_1 = [apply_substitution(lit, substitution) for lit in new_clause_1]
                new_clause_2 = [apply_substitution(lit, substitution) for lit in new_clause_2]

                # Combine the remaining literals from both clauses
                resolved_clause = new_clause_1 + new_clause_2

                # Avoid duplicate literals
                resolved_clause = list(set(resolved_clause))

                # Add the resolved clause if it's not already going to be added
                if resolved_clause not in resolved_clauses:
                    resolved_clauses.append(resolved_clause)

    return resolved_clauses


print("Test Case (Part 1) '(Parent(x, y)','Parent(John,Mary))' => " + str(unify('Parent(x, y)','Parent(John,Mary)')))
print("Test Case (Part 1) 'Loves(father(x), x)','Loves(father(John), John)' => " + str(unify('Loves(father(x), x)','Loves(father(John), John)',)))
print("Test Case (Part 1) 'Parent(x, x)','Parent(John,Mary)' => " + str(unify('Parent(x, x)','Parent(John,Mary)')))

kb = [['¬King(x)', '¬Greedy(x)', 'Evil(x)'], ['King(John)'], ['Greedy(x)']]
print("Test Case (Part 2) [['¬King(x)', '¬Greedy(x)', 'Evil(x)'], ['King(John)'], ['Greedy(x)']] -- Evil(John) => " + str(inference_by_resolution(kb, 'Evil(John)')))