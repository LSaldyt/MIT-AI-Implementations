from symbol    import Symbol
from charstore import CharStorage

class SymbolStorage(dict):
    def __init__(self):
        super().__init__()
        self.charstore = CharStorage()
        self.undefined = []

    def add(self, *args, **kwargs):
        if len(args) == 1 and len(kwargs) == 0:
            symbol = args[0]
        else:
            symbol = Symbol(*args, **kwargs)
        self[symbol.name] = symbol
        
        self.undefined.append(symbol.name)
        self.update()

    def update(self):
        pending = []
        for name in self.undefined:
            if name not in self:
                pending.append(name)
            else:
                for char in self.chars_of(name):
                    self.charstore.add(name, char)
        self.undefined = pending

    def chars_of(self, name):
        '''
        Recursively retrieve the characteristics of a symbol "name"
        Stops once atomic symbols (no parents) are found
        '''
        chars = []
        if name not in self: 
            if name not in self.undefined:
                self.undefined.append(name)
            return chars
        sym   = self[name]

        chars += sym.characteristics
        for component in sym.components:
            # Components are atomic, no recursion needed
            chars += component.characteristics
        if sym.kind is not None:
            chars += self.chars_of(sym.kind)
        return chars

    def find_by_chars(self, chars):
        print('%s best matched the characteristics %s' % (self.charstore.find(chars), chars))

