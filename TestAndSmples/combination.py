import numpy as np
from loguru import logger


class NumberPlace(object):  # numpy again
    def __init__(self):
        self.core = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9], dtype='uint8')

    def isUnique(self, *, nbox: np.ndarray) -> bool:
        # print(nbox)
        ok: bool = True
        for index, v in enumerate(nbox):
            s = np.unique(v).size
            if s < 9:
                logger.debug('Break at %d' % index)
                ok = False
                break
        return ok

    def sample(self) -> np.ndarray:
        nbox = np.zeros(shape=[9, 9], dtype='uint32')

        while True:
            for y in range(0, 9, 3):
                for x in range(0, 9, 3):
                    nbox[x:x + 3, y: y + 3] = np.random.permutation(self.core).reshape([3, 3])

            if self.isUnique(nbox=nbox):
                break
        return nbox


if __name__ == '__main__':
    # ooo = NumberPlace()
    # ppp = ooo.sample()
    # print(ppp)

    core = np.array([n for n in range(1, 10)], dtype='uint32')
    print(core)

    trio = np.zeros([3, 9], dtype='uint32')
    print(trio)

    full = np.zeros([9, 9], dtype='uint32')
    print(full)

    cell = np.random.permutation(core).reshape([3, 3])
    print(cell)

    full[1:4, 4:7] = cell
    print(full)
