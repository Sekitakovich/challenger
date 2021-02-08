import random
from dataclasses import dataclass
from enum import IntEnum
from typing import List

from loguru import logger
from termcolor import colored


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


@dataclass(frozen=True)  # read only
class Card(object):
    suit: Suits  # S:H:D:C
    mark: str  # '♠♡♢♣'
    name: str  # AKQJ + 2-10
    hcp: int  # high card point
    # fcp: int  # full card point (no need?)
    honor: bool  # HCP members + 10
    index: int
    color: str  # for termcolor
    attr: str


@dataclass()
class Hand(object):
    card: List[Card]
    hcp: int = 0
    # fcp: int = 0


class CBox(object):
    def __init__(self):
        self.indexs = [n for n in range(52)]
        self.card = []  # 52 cards (without JK)
        self.suit = [Suits.S, Suits.H, Suits.D, Suits.C]
        self.seat = ['S', 'W', 'N', 'E']
        self.name = ['A', 'K', 'Q', 'J', '10', '9', '8', '7', '6', '5', '4', '3', '2']
        self.marks = ['♠', '♥', '♦', '♣']
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
                    color='red' if self.suit[a] in (Suits.H, Suits.D) else 'grey',
                    attr='bold' if self.suit[a] in (Suits.S, Suits.H) else 'dark',
                ))
                index += 1

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

    def cont(*, card: List[Card]):
        series = 0
        for c in range(len(card) - 1):
            if card[c].suit == card[c + 1].suit:
                # logger.info(f'checking {c}')
                if card[c].index == card[c + 1].index - 1:
                    series += 1
                else:
                    if series:
                        logger.debug(f'{card[c].mark}{card[c].name} = {series}')
                    series = 0
            else:
                series = 0


    def main():
        cbox = CBox()
        deal = cbox.deal()

        for seat, m in enumerate(deal):
            # card = ' '.join([colored(f'{c.mark}{c.name}','red') for c in m.card])
            cont(card=m.card)
            name = []
            for card in m.card:
                text = f'{card.mark}{card.name}'
                color = f'{card.color}'
                attr = f'{card.attr}'
                view = colored(text, color, attrs=[f'{attr}'])
                name.append(view)
            golgo = ' '.join(name)
            logger.info(f'[{cbox.seat[seat]}] HCP={m.hcp:02d} card=[{golgo}]')


    main()
