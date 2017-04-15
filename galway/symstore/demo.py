from .symstore import Symbol, SymbolStorage, Atom

def syllogism():
    # Solving syllogisms in a few lines:
    symstore = SymbolStorage()
    symstore.add('man', characteristics=['mortal'])
    symstore.add('Socrates', kind='man')

    if 'mortal' in symstore.chars_of('Socrates'):
        return True

def find_by():
    symstore = SymbolStorage()
    symstore.add('firetruck', None, 'vehicle', [Atom('body', ['rectangular', 'red', 'metal']),
                                                Atom('tires', ['black', 'circular'])], [])
    symstore.add('apple', 'tree', 'fruit', [Atom('body', ['round', 'red', 'green', 'sweet', 'tart']),
                                            Atom('stem', ['brown', 'short'])], [])

    symstore.find_by(['red', 'sweet'], 'char')
    symstore.find_by(['red', 'rectangular'], 'char')
    symstore.find_by(['red'], 'char')

    symstore.find_by(['body', 'tires'], 'components')
    symstore.find_by(['tree'], 'origin')

def demo():
    syllogism()
    find_by()
