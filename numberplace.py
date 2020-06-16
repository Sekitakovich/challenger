import numpy as np


class NumberPlace(object):

    def __init__(self):
        self.core = np.array([n + 1 for n in range(9)], dtype='uint8')
        self.nbox = np.zeros([9, 9], dtype='uint8')

    def create(self) -> np.ndarray:
        # nbox = np.zeros([9, 9], dtype='uint8')

        for x in range(0, 9, 3):
            for y in range(0, 9, 3):
                cell = np.random.permutation(self.core).reshape([3, 3])
                # print('X:Y = %d:%d' % (x, y))

                self.nbox[y:y+3, x:x+3] = cell  # Never forget!

        return self.nbox

if __name__ == '__main__':

    sd = NumberPlace()
    ooo = sd.create()
    print(ooo)