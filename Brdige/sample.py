import random
import sys
from dataclasses import dataclass
from enum import IntEnum
from typing import List, Dict

from loguru import logger

logger.remove()
logger.add(
    sys.stdout,
    colorize=True,
    format="<level>{time:HH:mm:ss} {file}:{line}:{function} {message}</level>")
# logger.add(
#     'logs/mc.log',
#     rotation='1 day',
#     retention=180,
#     level='WARNING',
#     encoding='cp932')

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


@dataclass()
class Pointer(object):
    volume: int = 0
    series: int = 0


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
        # self.marks = ['♠', '♥', '♦', '♣']
        self.marks = ['S', 'H', 'D', 'C']
        self.hcps = [4, 3, 2, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        # self.fcps = [13, 12, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1]
        self.SQUARE = 4
        self.GOLGO = 13

        index = 0
        for a in range(self.SQUARE):
            for b in range(self.GOLGO):
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
        for p in range(self.SQUARE):
            card = []
            hcp = 0
            for m in sorted(self.indexs[(p * self.GOLGO): (p * self.GOLGO) + self.GOLGO]):
                this = self.card[m]
                hcp += this.hcp
                card.append(this)
            hand = Hand(card=card, hcp=hcp)
            result.append(hand)
        return result


if __name__ == '__main__':

    def series(*, card: List[Card]) -> int:
        result = 0
        cont = 0
        for c in range(len(card) - 1):
            if card[c].suit == card[c + 1].suit:
                # logger.info(f'checking {c}')
                if card[c].index == card[c + 1].index - 1:
                    cont += 1
                    result += 1
                else:
                    if cont:
                        logger.debug(f'{card[c].mark}{card[c].name} = {cont}')
                    cont = 0
            else:
                cont = 0
        return result

    def main():
        cbox = CBox()
        deal = cbox.deal()

        for seat, m in enumerate(deal):
            # card = ' '.join([colored(f'{c.mark}{c.name}','red') for c in m.card])
            name = []
            for card in m.card:
                text = f'{card.mark}{card.name}'
                color = f'{card.color}'
                attr = f'{card.attr}'
                view = colored(text, color, attrs=[f'{attr}'])
                name.append(view)

            golgo = ' '.join(name)
            cont = series(card=m.card)
            logger.info(f'[{cbox.seat[seat]}] HCP={m.hcp:02d} cont={cont} card=[{golgo}]')


    main()
