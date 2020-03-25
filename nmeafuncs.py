from functools import reduce
from operator import xor
from dataclasses import dataclass
from typing import List


@dataclass()
class NMEA(object):

    top: str = ''
    prefix: str = ''
    suffix: str = ''
    item: List[str] = ''


# class NMEAFuncs(object):
#
#     def __init__(self):
#         pass
#
#     @classmethod
#     def checkTheSum(cls, src: bytes) -> str:
#         result: str = ''
#         part: List[bytes] = src.split(b'*')
#         many: int = len(part)
#         if many == 1:  # no checksum
#             result = src.decode()
#         elif many == 2:
#             csum: int = reduce(xor, part[0][1:], 0)
#             if csum == int(part[1], 16):
#                 result = part[0].decode()
#         return result
#
#     @classmethod
#     def divide(cls, stream: bytes) -> List[bytes]:  # divide multi-nmea-sentence
#         multi = [s for s in stream.split(b'\r\n') if s]
#         return multi  # each nmea are CR/LF supressed
#
#
class FURUNOVDR(object):

    def __init__(self):
        self.header: bytes = b'\x00\x00\x00\x00\x00\x00\x00\x00'
        self.hlen: int = 8
        self.eol: bytes = b'\r\n'

    def reconstruction(self, stream: bytes) -> List[bytes]:  # divide multi-nmea-sentence
        multi = [self.header + s + self.eol for s in stream[self.hlen:].split(self.eol) if s]
        return multi


if __name__ == '__main__':

    data: bytes = b'\x00\x00\x00\x00\x00\x00\x00\x00$PFEC,VRpno,VR,8,1*68\r\n$HEHDT,352.3,T*28\r\n$TIROT,-000.0,A*16\r\n'

    furuno = FURUNOVDR()

    m = furuno.reconstruction(stream=data)
    print(m)