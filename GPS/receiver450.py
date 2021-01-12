import socket
from functools import reduce
from operator import xor
from contextlib import closing
import argparse

from loguru import logger


class Receiver(object):
    def __init__(self, *, mg: str, mp: int):
        self.mg = mg
        self.mp = mp
        self.running = True
        self.bufferSize = 4096
        self.localIP = socket.gethostbyname(socket.gethostname())

    def checkSum(self, *, body: bytes = b'') -> int:

        return reduce(xor, body, 0)

    def dump450(self, *, stream: bytes):
        try:
            part = stream.split(b'\x5c')
            if part[0][:5] == b'UdPbC':
                content = part[1].split(b'*')
                if self.checkSum(body=content[0]) == int(content[1], 16):
                    tag = {}
                    for t in part[1].split(b','):
                        item = t.split(b':')
                        tag[item[0]] = item[1]

                    sfi = tag[b's'].decode()
                    nmea = part[2]
                    print('%s %s' % (sfi, nmea))
                else:
                    logger.warning('checksum mismatch')
        except (KeyError, IndexError) as e:
            logger.error(e)
        else:
            pass

    def start(self):
        try:
            with closing(socket.socket(socket.AF_INET, socket.SOCK_DGRAM)) as sock:
                sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                sock.bind(('', self.mp))
                sock.setsockopt(socket.IPPROTO_IP,
                                socket.IP_ADD_MEMBERSHIP,
                                socket.inet_aton(self.mg) + socket.inet_aton(self.localIP))
                while self.running:
                    data, address = sock.recvfrom(self.bufferSize)
                    self.dump450(stream=data)
        except (socket.error, socket.gaierror) as e:
            logger.error(e)
            self.running = False
        except (KeyboardInterrupt,) as e:
            self.running = False


if __name__ == '__main__':

    mg = '239.192.0.1'
    mp = 56001

    parser = argparse.ArgumentParser()
    parser.add_argument('--group', type=str, default=mg, help='マルチキャストグループ(初期値: %s)' % mg)
    parser.add_argument('--port', type=int, default=mp, help='マルチキャストポート(初期値: %d)' % mp)

    args = parser.parse_args()

    R = Receiver(mg=args.group, mp=args.port)
    R.start()
