import nltk
from nltk import CFG

# Define a simple grammar
grammar = CFG.fromstring("""
  S -> NP VP
  NP -> DT N | PRP
  VP -> V NP | V
  DT -> 'the' | 'a'
  N -> 'cat' | 'dog'
  V -> 'saw' | 'slept'
  PRP -> 'I'
""")

# Sample sentence
sentence = ['I', 'saw', 'a', 'dog']

# --- Top-Down Parser (Recursive Descent Parser) ---
print("Top-Down Parsing (Recursive Descent):")
rd_parser = nltk.RecursiveDescentParser(grammar)
for tree in rd_parser.parse(sentence):
    print(tree)
    tree.pretty_print()

# --- Bottom-Up Parser (Shift-Reduce Parser) ---
print("\nBottom-Up Parsing (Shift-Reduce):")
sr_parser = nltk.ShiftReduceParser(grammar)
for tree in sr_parser.parse(sentence):
    print(tree)
    tree.pretty_print()
