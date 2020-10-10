from functools import reduce
from operator import add
import time
from numba import jit


def withReduce(*, src: bytes) -> int:
    return reduce(add, src, 0) % 0x10000


@jit
def withLoop(*, src: bytes) -> int:
    val = 0
    for b in src:
        val += b
    return val % 0x10000


if __name__ == '__main__':
    src = bytes([b for b in range(0x100)] * 100000)

    ts = time.time()
    sono1 = withLoop(src=src)
    s1 = (time.time() - ts)

    ts = time.time()
    sono2 = withReduce(src=src)
    s2 = (time.time() - ts)

    print('loop = %d: %.3f, reduce = %d: %.3f' % (sono1, s1, sono2, s2))
