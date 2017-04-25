from contextlib import contextmanager

import time

from .timeout import timeout

@contextmanager
def timedblock(label, saveDict=None, maxTime=None):
    with timeout(maxTime):
        start = time.perf_counter()
        try:
            yield
        except TimeoutError:
            print('!', end='', flush=True)
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
