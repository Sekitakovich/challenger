from itertools import permutations

core = [1, 2, 3, 4, 5, 6, 7, 8, 9]

family = [baby for baby in permutations(core)]

print(len(family))
