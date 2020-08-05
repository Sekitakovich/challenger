from dataclasses import dataclass
from enum import IntEnum
from typing import List


class TGroup(IntEnum):
    Wind = 1
    Color = 2
    Numeric = 3


class WGroup(IntEnum):
    E = 1
    S = 2
    W = 3
    N = 4


class CGroup(IntEnum):
    W = 1
    G = 2
    R = 3


class NGroup(IntEnum):
    M = 1
    P = 2
    S = 3


@dataclass()
class Tile(object):
    tgroup: int
    sgroup: int
    index: int = 0


if __name__ == '__main__':

    tile: List[Tile] = []

    for a in range(1, 1 + 4):
        tile.append(Tile(tgroup=TGroup.Wind, sgroup=WGroup.E))
        tile.append(Tile(tgroup=TGroup.Wind, sgroup=WGroup.S))
        tile.append(Tile(tgroup=TGroup.Wind, sgroup=WGroup.W))
        tile.append(Tile(tgroup=TGroup.Wind, sgroup=WGroup.N))

        tile.append(Tile(tgroup=TGroup.Color, sgroup=CGroup.W))
        tile.append(Tile(tgroup=TGroup.Color, sgroup=CGroup.G))
        tile.append(Tile(tgroup=TGroup.Color, sgroup=CGroup.R))

        for index in range(1, 1 + 9):
            tile.append(Tile(tgroup=TGroup.Numeric, sgroup=NGroup.M, index=index))
            tile.append(Tile(tgroup=TGroup.Numeric, sgroup=NGroup.P, index=index))
            tile.append(Tile(tgroup=TGroup.Numeric, sgroup=NGroup.S, index=index))

    print(tile)
