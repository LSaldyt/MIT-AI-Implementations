from collections import Counter

class CountStorage(dict):
    def add(self, symname, key):
        if key in self:
            self[key].append(symname)
        else:
            self[key] = [symname]

    def find(self, keys):
        assert len(keys) > 0
        c = Counter()
        for char in keys:
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

