from .symnet import SymbolNet, Clause
from .interface import read_natural_language

def description_matching():
    net = SymbolNet()
    net.add('firetruck', 'isa', 'vehicle')
    net.add('firetruck', 'is', 'red')
    net.add('firetruck', 'is', 'metal')
    net.add('apple', 'isa', 'fruit')
    net.add('apple', 'is', 'red')
    net.add('apple', 'is', 'round')

    print(net.find_by('is', 'red', 'round'))

def macbeth():
    net = SymbolNet()
    net.add('macbeth', 'murder', 'duncan')
    net.add('duncan', 'isa', 'king')
    net.add('macbeth', 'isa', 'noble')
    net.add('macbeth', 'has-spouse', 'lady macbeth')
    net.add('lady-macbeth', 'is', 'greedy')
    net.add('lady-macbeth', 'is', 'domineering')
    net.add('macbeth', 'is', 'tired', cause=Clause('lady-macbeth', 'is', 'domineering'))
    net.add('macbeth', 'is', 'weak', cause=Clause('macbeth', 'is', 'tired'))
    print(net)
    print('* is weak:')
    print(net.find_that('is', 'weak'))
    print('* is weak, greedy, and a noble:')
    print(net.find_close([('is', 'weak'), ('is', 'greedy'), ('isa', 'noble')]))
    print('* is weak and tired:')
    print(net.find_by('is', 'weak', 'tired'))
    print('macbeth is weak because:')
    print(net.trace_reasons(Clause('macbeth', 'is', 'weak')))

def cup():
    net = SymbolNet()
    net.add('brick', 'is', 'stable', cause=Clause('brick', 'hasa', 'flatbottom'))
    net.add('brick', 'is', 'heavy')
    net.add('glass', 'enables', 'drinking', causes=[Clause('glass', 'hasa', 'handle'), Clause('glass', 'carries', 'liquid')])
    net.add('glass', 'is', 'pretty')
    net.add('glass', 'madeof', 'glass')
    net.add('briefcase', 'is', 'liftable', causes=[Clause('briefcase', 'has', 'handle'), Clause('briefcase', 'is', 'light')])
    net.add('briefcase', 'is', 'useful', cause=Clause('briefcase', 'holds', 'papers'))
    net.add('briefcase', 'enables', 'organization', cause=Clause('briefcase', 'holds', 'papers'))
    net.add('bowl', 'carries', 'liquid', cause=Clause('bowl', 'has', 'concavity'))
    net.add('bowl', 'contains', 'cherry-soup')

    net.add('cup', 'is', 'stable')
    net.add('cup', 'enables', 'drinking')

    net.add('mystery-object', 'madeof', 'porcelain')
    net.add('mystery-object', 'hasa', 'decoration')
    net.add('mystery-object', 'hasa', 'concavity')
    net.add('mystery-object', 'hasa', 'handle')
    net.add('mystery-object', 'hasa', 'flatbottom')

    print(net)
    net.show('mystery-object', 'cup')
    print(net.relationTypes)

    net.likely('glass', 'hasa', 'concavity')
    net.likely('cup', 'hasa', 'concavity')
    net.likely('mystery-object', 'is', 'heavy')

    net.analogize('cup', 'drinking', 'briefcase')

def syllogism():
    net = SymbolNet()
    net.add('man', 'is', 'mortal')
    net.add('Socrates', 'isa', 'man')
    net.likely('Socrates', 'is', 'mortal')
    print(net)

def analogy():
    net = SymbolNet()
    net.add('cup', 'holds', 'liquid')
    net.add('briefcase', 'holds', 'paper')
    # A cup is to liquid as a briefcase is to paper?
    # Weak, but A -> B as C -> D, right?
    net.analogize('cup', 'liquid', 'briefcase') # Cup is to liquid as briefcase is to _?

def instance_analogy():
    net = SymbolNet()
    net.add('cup-a', 'is', 'small')
    net.add('cup-a', 'isa', 'cup')
    net.add('cup-b', 'is', 'big')
    net.add('cup-b', 'isa', 'cup')
    net.add('bowl-a', 'is', 'small')
    net.add('bowl-a', 'isa', 'bowl')
    net.add('bowl-b', 'is', 'big')
    net.add('bowl-b', 'isa', 'bowl')
    net.analogize('cup-a', 'bowl-a', 'cup-b')

def high_analogy():
    net = SymbolNet()
    net.add('granny-smith', 'isa', 'apple')
    net.add('apple', 'isa', 'fruit')
    net.add('husky', 'isa', 'dog')
    net.add('dog', 'isa', 'mammal')
    #net.analogize('granny-smith', 'apple', 'husky') # mammal
    net.analogize('granny-smith', 'fruit', 'husky') # mammal
    #print(net)

def demo():
    #description_matching()
    #macbeth()
    #cup()
    #syllogism()
    analogy()
    #read_natural_language('data/syllogism.txt')
    instance_analogy()
    high_analogy()

