from dataclasses import dataclass
from enum import IntEnum
import random
from typing import List
from loguru import logger


class Suits(IntEnum):
    none = 0
    S = 1
    H = 2
    D = 3
    C = 4


@dataclass()
class Card(object):
    suit: Suits  # S:H:D:C
    number: int
    mark: str
    name: str
    hcp: int

class CBox(object):
    def __init__(self):
        self.card = []  # 52枚のカード(Joker不要!)
        self.suit = [Suits.S, Suits.H, Suits.D, Suits.C]
        self.name = ['A', 'K', 'Q', 'J', '10', '9', '8', '7', '6', '5', '4', '3', '2']
        self.numbers = [13, 12, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1]
        self.indexs = [n for n in range(52)]
        self.marks = ['♠','♡','♢','♣']
        self.hcps = [4, 3, 2, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0]

        for a in range(4):
            for b in range(13):
                self.card.append(Card(suit=self.suit[a], name=self.name[b], mark=self.marks[a], number=self.numbers[b], hcp=self.hcps[b]))

    def hand(self) -> List[Card]:
        result = [self.card[c] for c in sorted(random.sample(self.indexs, 13))]
        return result


if __name__ == '__main__':
    def main():
        cbox = CBox()
        hand = cbox.hand()

        HCP = 0
        many = {
            Suits.S: 0,
            Suits.H: 0,
            Suits.D: 0,
            Suits.C: 0,
        }
        for h in hand:
            logger.info(f'{h.mark}{h.name}')
            HCP += h.hcp
            many[h.suit] += 1
        pass
        logger.debug(f'HCP = {HCP}')
        logger.debug(many)


    main()
