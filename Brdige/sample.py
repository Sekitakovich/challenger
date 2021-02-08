from dataclasses import dataclass
from enum import IntEnum
import random
from typing import List
from loguru import logger


class Seat(IntEnum):
    S = 0
    W = 1
    N = 2
    E = 3


class Suits(IntEnum):
    N = 0
    S = 1
    H = 2
    D = 3
    C = 4


@dataclass(frozen=True)
class Card(object):
    suit: Suits  # S:H:D:C
    mark: str  # '♠♡♢♣'
    name: str  # AKQJ + 2-10
    hcp: int  # high card point
    # fcp: int  # full card point (no need?)
    honor: bool  # HCP members + 10
    index: int


@dataclass()
class Hand(object):
    card: List[Card]
    hcp: int = 0
    fcp: int = 0


class CBox(object):
    def __init__(self):
        self.indexs = [n for n in range(52)]
        self.card = []  # 52 cards (without JK)
        self.suit = [Suits.S, Suits.H, Suits.D, Suits.C]
        self.name = ['A', 'K', 'Q', 'J', '10', '9', '8', '7', '6', '5', '4', '3', '2']
        self.marks = ['♠', '♡', '♢', '♣']
        self.hcps = [4, 3, 2, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        # self.fcps = [13, 12, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1]

        index = 0
        for a in range(4):
            for b in range(13):
                self.card.append(Card(
                    suit=self.suit[a],
                    name=self.name[b],
                    mark=self.marks[a],
                    hcp=self.hcps[b],
                    # fcp=self.fcps[b],
                    honor=bool(b < 5),
                    index=index,
                ))
                index += 1

    # def hand(self, *, top: int) -> List[Card]:
    #     result = [self.card[c] for c in sorted(random.sample(self.indexs, top * 13))]
    #     return result

    def deal(self) -> List[Hand]:
        result = []
        random.shuffle(self.indexs)
        for p in range(4):
            card = []
            hcp = 0
            for m in sorted(self.indexs[(p * 13): (p * 13) + 13]):
                this = self.card[m]
                hcp += this.hcp
                card.append(this)
            hand = Hand(card=card, hcp=hcp)
            result.append(hand)
        return result


if __name__ == '__main__':
    def main():
        cbox = CBox()
        deal = cbox.deal()

        for m in deal:
            card = ' '.join([f'{c.mark}{c.name}' for c in m.card])
            logger.info(f'HCP={m.hcp:02d} card=[{card}]')

    main()
