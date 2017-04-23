from contextlib import contextmanager

import time

@contextmanager
def timedblock(label, saveDict=None):
    start = time.perf_counter()
    try:
        yield
    finally:
        end  = time.perf_counter()
        t = end - start
        if saveDict is not None:
            if isinstance(saveDict[label], list):
                saveDict[label].append(t)
            else:
                saveDict[label] = t
        else:
            print('{} : {}'.format(label, t))
