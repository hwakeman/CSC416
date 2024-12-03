import csv
import math
from collections import Counter

def calculate_information_gain(feature, data):
    total_decisions = len(data)

    # Gets the total amount of 'yes' and 'no' decisions remaining
    decision_counts = Counter([row['Decision'] for row in data])

    # Uses the entropy formula you provided
    initial_entropy = 0
    for count in decision_counts.values():
        probability = count / total_decisions
        initial_entropy -= probability * math.log2(probability)
    
    # Gets the possible values for the current feature
    feature_values = set(row[feature] for row in data)

    # Uses the information gain formula you provided
    weighted_entropy = 0    
    for value in feature_values:
        subset = [row for row in data if row[feature] == value]

        subset_total = len(subset)
        subset_decision_counts = Counter([row['Decision'] for row in subset])
        subset_entropy = 0
        for count in subset_decision_counts.values():
            probability = count / subset_total
            subset_entropy -= probability * math.log2(probability)
        
        weighted_entropy += (subset_total / total_decisions) * subset_entropy
    

    information_gain = initial_entropy - weighted_entropy
    return information_gain

def build_decision_tree(data):
    features = list(data[0].keys())[:-1]
    decisions = set(row['Decision'] for row in data)

    # Base case
    if len(decisions) == 1:
        return Node(value=decisions.pop())
    
    # Gets the feature that will provide the most information gain and creates a node with it
    best_feature = max(features, key=lambda feature: calculate_information_gain(feature, data))
    root = Node(feature=best_feature, children={})

    feature_values = set(row[best_feature] for row in data)
    
    # Builds any subtrees within the current tree
    for value in feature_values:
        subset = [row for row in data if row[best_feature] == value]
        child_node = build_decision_tree(subset)
        root.children[value] = child_node
    
    return root

class Node:
    def __init__(self, feature=None, value=None, children=None):
        self.feature = feature
        self.value = value
        self.children = children

def print_tree(node, indent=""):
    # A node with a value is a decision
    if node.value is not None:
        print(f"{indent}Decision: {node.value}")
        
    # A node without a value is a feature
    else:
        print(f"{indent}Feature: {node.feature}")
        for value, child in node.children.items():
            print(f"{indent}  -> {value}:")
            print_tree(child, indent + "    ")

data = []
with open('decision_tree_data.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        data = [row for row in reader]

tree = build_decision_tree(data)

print_tree(tree)
