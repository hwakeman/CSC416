import re

def unify(sentence1, sentence2):
    # Split sentence1 into its variables and then remove any empty strings, whitespace, or duplicates
    sentence1_variables = re.split(r'[(),]', sentence1)
    sentence1_variables = [variable.strip() for variable in sentence1_variables if variable]
    sentence1_variables = list(dict.fromkeys(sentence1_variables))

    # Split sentence2 into its variables and then remove any empty strings, whitespace, or duplicates
    sentence2_variables = re.split(r'[(),]', sentence2)
    sentence2_variables = [variable.strip() for variable in sentence2_variables if variable]
    sentence2_variables = list(dict.fromkeys(sentence2_variables))

    # Check if the two sentences have the same number of variables to unify
    if len(sentence1_variables) != len(sentence2_variables):
        return {}  # Unification not possible if they don't match in structure

    variable_substitutions = {}

    for variable1, variable2 in zip(sentence1_variables, sentence2_variables):
        # Skip duplicate variables (Ex: 'Parent' shouldn't be mapped to 'Parent')
        if variable1 == variable2:
            continue

        # We have to check if variable1 is already substituted
        if variable1 in variable_substitutions:
            # If the variable has already been substituted, we have to 
            # make sure the substitution would work in this case
            if variable_substitutions[variable1] != variable2:
                return {} # Conflict in substitutions

        # We have to check if variable2 is already substituted
        elif variable2 in variable_substitutions:
            # If the variable has already been substituted, we have to 
            # make sure the substitution would work in this case
            if variable_substitutions[variable2] != variable1:
                return {}  # Conflict in substitutions

        else:
            # Add new mapping
            variable_substitutions[variable1] = variable2

    return variable_substitutions


def inference_by_resolution(kb, query):
    pass

def resolve(clause1, clause2):
    pass

# print(unify('Parent(x, y)','Parent(John,Mary)'))
# print(unify('Loves(father(x), x)','Loves(father(John), John)',))
# print(unify('Parent(x, x)','Parent(John,Mary)'))

kb = [['¬King(x)', '¬Greedy(x)', 'Evil(x)'], ['King(John)'], ['Greedy(x)']]
print(inference_by_resolution(kb, 'Evil(John)'))