#!/usr/bin/env python3
from symbol   import Symbol, Atom
from symstore import SymbolStorage

'''
Apple:
    origin: tree
    is: fruit
    has:
        body: round, red, green, apple-taste (sweet, tart)
        stem: brown, short

Object:
    origin: 
    class:
    characteristics:

'''

def syllogism():
    # Solving syllogisms in a few lines:
    symstore = SymbolStorage()
    symstore.add('man', characteristics=['mortal'])
    symstore.add('Socrates', kind='man')

    if 'mortal' in symstore.chars_of('Socrates'):
        print('Solved Plato\'s basic syllogism')

def find_by_chars():
    symstore = SymbolStorage()
    symstore.add('firetruck', None, 'vehicle', [Atom('body', ['rectangular', 'red', 'metal']),
                                                Atom('tires', ['black', 'circular'])], [])
    symstore.add('apple', 'tree', 'fruit', [Atom('body', ['round', 'red', 'green', 'sweet', 'tart']),
                                            Atom('stem', ['brown', 'short'])], [])
    symstore.find_by_chars(['red', 'sweet'])
    symstore.find_by_chars(['red', 'rectangular'])
    symstore.find_by_chars(['red'])

if __name__ == '__main__':
    syllogism()
    find_by_chars()

