from itertools import permutations
import numpy as np

core = [1, 2, 3, 4, 5, 6, 7, 8, 9]

family = [np.fromiter(baby, dtype='uint32') for baby in permutations(core)]

# sono1 = family[0].reshape([3, 3])
# sono2 = family[1].reshape([3, 3])
#
# twin = np.concatenate([sono1, sono2], axis=1)
#
# print(twin)
#

for a in range(len(family)):
    for b in range(len(family)):
        for c in range(len(family)):
            trio = np.concatenate(
                [family[a].reshape([3, 3]), family[b].reshape([3, 3]), family[c].reshape([3, 3])],
                axis=1)
            print(trio)
            ok = True
            for d in range(3):
                result = np.unique(trio[d])
                if result.size < 9:
                    ok = False
                    break
            if ok:
                print(trio)
