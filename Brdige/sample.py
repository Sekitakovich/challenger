from dataclasses import dataclass
from enum import IntEnum
import random
from typing import List
from loguru import logger


class Suits(IntEnum):
    S = 1
    H = 2
    D = 3
    C = 4


@dataclass()
class Card(object):
    suit: Suits
    name: str
    value: int


class CBox(object):
    def __init__(self):
        self.card = []  # 52枚のカード(Joker不要!)
        self.suit = [Suits.S, Suits.H, Suits.D, Suits.C]
        self.name = ['A', 'K', 'Q', 'J', '10', '9', '8', '7', '6', '5', '4', '3', '2']
        self.indexs = [n for n in range(52)]
        vals = [13, 12, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1]

        for a in range(4):
            # plus = 4 - a
            plus = 0
            for b in range(13):
                self.card.append(Card(suit=self.suit[a], name=self.name[b], value=vals[b] + plus))

    def hand(self) -> List[Card]:
        result = [self.card[c] for c in sorted(random.sample(self.indexs, 13))]
        return result


if __name__ == '__main__':
    def main():
        cbox = CBox()
        hand = cbox.hand()

        value = 0
        for h in hand:
            logger.info(h)
            value += h.value
        pass
        logger.debug(f'total {value}')


    main()
