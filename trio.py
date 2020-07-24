from typing import List
from itertools import permutations
import numpy as np
import watchdog
from loguru import logger

class Trio(object):

    def __init__(self):

        base = permutations([1, 2, 3, 4, 5, 6, 7, 8, 9])
        core = [np.array(c, dtype=int) for c in base]
        trio = np.zeros(shape=[3, 9], dtype=int)

        print(trio)

        for indexH, H in enumerate(core):
            trio[0] = H
            print('H: %d' % indexH)
            for indexM, M in enumerate(core):
                if indexM != indexH:
                    trio[1] = M
                    print('M: %d' % indexM)
                    for indexL, L in enumerate(core):
                        if indexL not in [indexH, indexM]:
                            trio[2] = L
                            ok = True
                            rot = np.rot90(trio.copy())
                            for ooo in rot:
                                u = np.unique(ooo)
                                if u.size < 3:
                                    ok = False
                                    # print('break at %d' % u.size)
                                    break
                            if ok:
                                print('L: %d' % indexL)
                                print(trio)

if __name__ == '__main__':
    engine = Trio()
