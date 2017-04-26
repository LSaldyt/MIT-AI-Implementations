from contextlib import contextmanager

import time

from .timeout import timeout

@contextmanager
def timedblock(label, saveDict=None, maxTime=None):
    if saveDict is not None and label in saveDict and saveDict[label] is None:
        maxTime = 0.0001
    with timeout(maxTime):
        start = time.perf_counter()
        try:
            yield
        except TimeoutError:
            saveDict[label] = None
        finally:
            end  = time.perf_counter()
            t = end - start
            if saveDict is not None:
                if label in saveDict and saveDict[label] is None:
                    return
                if isinstance(saveDict[label], list):
                    saveDict[label].append(t)
                else:
                    saveDict[label] = t
            else:
                print('{} : {}'.format(label, t))
