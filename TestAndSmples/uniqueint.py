from typing import List
from random import randint
import time
from numba import jit
from loguru import logger

@jit
def uniqueIntList(*, size: int) -> List[int]:
    max: int = size * 1000
    miss: int = 0
    result: List[int] = []
    for index in range(size):
        while True:
            value: int = randint(0, max)
            if value not in result:
                result.append(value)
                break
            else:
                miss += 1
    print(miss)
    return result

size = 100000

for loop in range(3):

    logger.debug('Start buildup for %d' % size)

    ts = time.time()
    ooo = uniqueIntList(size=size)
    te = time.time()

    logger.debug('size: %d passing %.3f secs' % (size, te-ts))