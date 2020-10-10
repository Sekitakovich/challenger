from typing import List
from itertools import permutations
import numpy as np

core: List[int] = [1, 2, 3, 4, 5, 6, 7, 8, 9]
src = permutations(core)

for s in src:
    area = np.array(s, dtype=int).reshape([3, 3])
    print(area)


# core = [1, 2, 3, 4, 5, 6, 7, 8, 9]
#
# src = permutations(core)
#
# for index, k in enumerate(src):
#     print(index, k)
# sono1 = family[0].reshape([3, 3])
# sono2 = family[1].reshape([3, 3])
#
# twin = np.concatenate([sono1, sono2], axis=1)
#
# print(twin)
#

# for a in range(len(family)):
#     for b in range(len(family)):
#         for c in range(len(family)):
#             trio = np.concatenate(
#                 [family[a].reshape([3, 3]), family[b].reshape([3, 3]), family[c].reshape([3, 3])],
#                 axis=1)
#             print(trio)
#             ok = True
#             for d in range(3):
#                 result = np.unique(trio[d])
#                 if result.size < 9:
#                     ok = False
#                     break
#             if ok:
#                 print(trio)
