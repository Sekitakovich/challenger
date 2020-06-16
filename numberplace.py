import numpy as np


class NumberPlace(object):

    def __init__(self):
        self.core = np.array([n + 1 for n in range(9)], dtype='uint8')

    def create(self):
        nbox = np.zeros([9, 9], dtype='uint8')
        print(nbox)

        for x in range(0, 9, 3):
            for y in range(0, 9, 3):
                cell = np.random.permutation(self.core).reshape([3, 3])
                print('X:Y = %d:%d' % (x, y))
                print(cell)

                nbox[y:y+3, x:x+3] = cell  # Never forget!
                print(nbox)

if __name__ == '__main__':

    sd = NumberPlace()
    sd.create()
