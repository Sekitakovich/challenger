import numpy as np


class NumberPlace(object):  # numpy again
    def __init__(self):
        self.core = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9], dtype='uint8')

    def isUnique(self, *, nbox: np.ndarray) -> bool:
        print(nbox)
        ok: bool = True
        for v in nbox:
            s = np.unique(v).size
            if s < 9:
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

    stage = np.zeros([9, 9], dtype='uint32')
    print(stage)

    core = np.array([n for n in range(1, 10)], dtype='uint32')
    print(core)
    cell = np.random.permutation(core).reshape([3, 3])
    print(cell)

    stage[1:4, 4:7] = cell
    print(stage)
