from typing import List
from itertools import permutations
import numpy as np

core: List[int] = [1, 2, 3, 4, 5, 6, 7, 8, 9]
this = permutations(core)

for indexS, src in enumerate(this):
    L = np.array(src, dtype=int).reshape([3, 3])
    print(L)
    for indexD, dst in enumerate(this):
        if indexD != indexS:
            ok = True
            C = np.array(dst, dtype=int).reshape([3, 3])
            ddd = np.concatenate([L, C], axis=1)
            for a in range(3):
                uuu = np.unique(ddd[a])
                if uuu.size < 6:
                    ok = False
                    break
            if ok:
                print(indexS, indexD)
                print(ddd)
