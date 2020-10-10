from typing import List


class EX49(object):
    """
    49抜き連番のエンコーダ・デコーダ
    """

    def __init__(self):

        self.tableE: List[int] = [0, 1, 2, 3, 5, 6, 7, 8]
        self.tableD: List[int] = [0, 1, 2, 3, 0, 4, 5, 6, 7, 8]

    def encode(self, *, src: int) -> int:
        dst: int = 0
        mul: int = 1
        while True:
            quotient, remainder = divmod(src, 8)  # (商,余)
            dst += (self.tableE[remainder] * mul)
            if quotient:
                mul *= 10
                src = int(src / 8)
            else:
                break
        return dst

    def decode(self, *, src: int) -> int:
        dst: int = 0
        mul: int = 1
        while True:
            quotient, remainder = divmod(src, 10)  # (商,余)
            dst += (self.tableD[remainder] * mul)
            if quotient:
                mul *= 8
                src = int((src / 10))
            else:
                break
        return dst


if __name__ == '__main__':

    ex49 = EX49()

    for v in range(1000):
        e = ex49.encode(src=v)
        d = ex49.decode(src=e)
        print('Encode:Decode(status) %d -> %d -> %d = %s' % (v, e, d, (v == d)))
