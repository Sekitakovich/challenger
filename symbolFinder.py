from loguru import logger


class SymbolFinder(object):
    '''
    ストリーム受信の度にパターンマッチングをするためのクラス
    '''

    def __init__(self, *, pattern: bytes) -> None:  # 期待するパターンをbytesでセットする
        self.pattern = [int(c) for c in pattern]
        self.length = len(pattern)
        self.position = 0
        self.counter = 0

        logger.debug(f'start with pattern = {pattern}')

    def check(self, *, inchar: int) -> bool:
        '''
        inchar: 受信した文字(データ)
        これを含むストリームがself.patternとマッチしたらTrueを返す
        '''
        found = False
        correct = self.pattern[self.position]
        good = (inchar == correct)

        logger.debug(
            f'[{self.counter:06d}:{self.position}] checking 0x{inchar:02X}({chr(inchar)}) with 0x{correct:02X} - {good}')

        if good:
            self.position += 1
            if self.position == self.length:
                found = True
                self.position = 0  # Initialize checkpoint
                logger.debug(f'Completed!')
            else:
                pass  # to be continue
        else:
            self.position = 0  # Reset checkpoint

        self.counter += 1
        return found


if __name__ == '__main__':
    def main():
        symbol = b'Now&Then'
        C = SymbolFinder(pattern=symbol)
        sample = b'\x01\x02\x03' + symbol + b'abc'
        for s in sample:
            result = C.check(inchar=s)
            if result:
                logger.info(f'Ready go')
        pass


    main()
