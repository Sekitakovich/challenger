from typing import List
from itertools import permutations
import numpy as np
from loguru import logger


class Duet(object):

    def __init__(self):

        area = permutations([1, 2, 3, 4, 5, 6, 7, 8, 9])
        self.core = [np.array(c, dtype='uint8').reshape([3, 3]) for c in area]
        self.result = np.zeros([3, 9], dtype='uint8')
        self.collecton: List[List[int]] = []
        self.total: int = 0

    def trio(self, *, duet: np.ndarray, indexL: int, indexC: int):
        self.result[0:3, 0:6] = duet
        for indexR, R in enumerate(self.core):
            self.result[0:3, 6:9] = R
            ok = True
            for eee in self.result:
                if np.unique(eee).size < 9:
                    ok = False
                    break
            if ok:
                self.collecton.append([indexL, indexC, indexR])
                self.total += 1
                # print('at %d: %s' % (indexR, self.result))
                print('+++ %d at %d:%d:%d' % (self.total, indexL, indexC, indexR))
                print(self.result)

    def create(self):
        for indexL, L in enumerate(self.core):
            for indexC, C in enumerate(self.core):
                if indexC != indexL:
                    ok = True
                    ddd = np.concatenate([L, C], axis=1)
                    for eee in ddd:
                        if np.unique(eee).size < 6:
                            ok = False
                            break
                    if ok:
                        logger.debug('at %d:%d' % (indexL, indexC))
                        self.trio(duet=ddd, indexL=indexL, indexC=indexC)
                        # print(ddd)
                        # self.duet.append(ddd)


if __name__ == '__main__':
    duet = Duet()
    duet.create()
