from collections import Counter

class CharStorage(dict):
    def add(self, symname, char):
        if char in self:
            self[char].append(symname)
        else:
            self[char] = [symname]

    def find(self, chars):
        assert len(chars) > 0
        c = Counter()
        for char in chars:
            c.update(self[char])

        common = c.most_common()
        assert len(common) > 0
        best = common[0][1]
        matches = []
        for item, count in common:
            if count == best:
                matches.append(item)
            else:
                break
        return matches

