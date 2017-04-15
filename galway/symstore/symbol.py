from collections import namedtuple
from pprint      import pprint

'''
Specific:

    Apple:
        origin: tree
        is: fruit
        has:
            body: round, red, green, apple-taste (sweet, tart)
            stem: brown, short

General: 

    Object:
        origin:          [names]
        kind:            [names]
        components:      [Objects]
        characteristics: [adjectives]

        Adjectives should be based on senses:
            i.e. color = visual
'''

Symbol = namedtuple('Symbol', ['name', 'origin', 'kind', 'components', 'characteristics'])
Symbol.__new__.__defaults__ = (None, None, None, [], [])

# Shorthand factory function
def Atom(name, characteristics):
    return Symbol(name=name, characteristics=characteristics)

