from typing import List
from datetime import datetime as dt
from contextlib import closing
import time
import math
import socket
from threading import Thread
from functools import reduce
from operator import xor
from loguru import logger
from hexdump import hexdump
import argparse


class GPSSendor(Thread):

    def __init__(self, *, sog: float, cog: float, mg: str, mp: int):
        super().__init__()
        self.daemon = True

        self.interval: float = 1.0
        self.latMeterPerSec: float = 30.820
        self.lngMeterPerSec: float = 25.153

        self.group = mg
        self.port = mp

        self.toplat: float = 35.221975  # 久里浜
        self.toplng: float = 139.719938

        self.lat: float = self.toplat
        self.lng: float = self.toplng
        self.sog = sog
        self.cog = cog

        rmc = 'GPRMC,085120.307,A,3541.1493,N,13945.3994,E,000.0,240.3,181211,,,A'
        self.rmc: List[str] = rmc.split(',')
        gga = 'GPGGA,085120.307,3541.1493,N,13945.3994,E,1,08,1.0,6.9,M,35.9,M,,0000'
        self.gga: List[str] = gga.split(',')
        gll = 'GPGLL,3421.7686,N,13222.3345,E,073132,A,A'
        self.gll: List[str] = gll.split(',')
        zda = 'GPZDA,082220.00,09,01,2006,0,0'
        self.zda: List[str] = zda.split(',')

        self.sfi = b'GP0001'
        self.counter = 1

        self.running: bool = True

    def F450(self, *, nmea: bytes) -> bytes:
        header = b'UdPdC\x00'
        section: List[bytes] = []
        section.append(b's:' + self.sfi)
        section.append(b'n:%d' % self.counter)
        body = b','.join(section)
        cs = self.checkSum(body=body)
        body += b'*%02X' % cs
        result = header + b'\x5c' + body + b'\x5c' + nmea
        self.counter += 1
        if self.counter == 1000:
            self.counter = 1
        return result

    def GoogleMaptoGPS(self, *, val: float = None) -> float:  # GoogleMaps -> GPGGA

        decimal, integer = math.modf(val)
        value: float = (integer + ((decimal * 60) / 100)) * 100
        return value

    def checkSum(self, *, body: bytes = b'') -> int:

        return reduce(xor, body, 0)

    def ZDA(self, *, now: dt) -> bytes:
        self.zda[1] = now.strftime('%H%M%S.%f')
        self.zda[2] = str(now.day)
        self.zda[3] = str(now.month)
        self.zda[4] = str(now.year)

        body: str = ','.join(self.zda)
        cs: str = '*%02X' % self.checkSum(body=body.encode())
        nmea: str = '$%s%s' % (body, cs)
        sentence = (nmea + '\r\n').encode()
        return sentence

    def GLL(self, *, now: dt) -> bytes:
        self.gll[1] = '%.4f' % self.GoogleMaptoGPS(val=self.lat)
        self.gll[3] = '%.4f' % self.GoogleMaptoGPS(val=self.lng)
        self.gll[5] = now.strftime('%H%M%S.%f')

        body: str = ','.join(self.gll)
        cs: str = '*%02X' % self.checkSum(body=body.encode())
        nmea: str = '$%s%s' % (body, cs)
        sentence = (nmea + '\r\n').encode()
        return sentence

    def GGA(self, *, now: dt) -> bytes:
        self.gga[1] = now.strftime('%H%M%S.%f')
        self.gga[2] = '%.4f' % self.GoogleMaptoGPS(val=self.lat)
        self.gga[4] = '%.4f' % self.GoogleMaptoGPS(val=self.lng)

        body: str = ','.join(self.gga)
        cs: str = '*%02X' % self.checkSum(body=body.encode())
        nmea: str = '$%s%s' % (body, cs)
        sentence = (nmea + '\r\n').encode()
        return sentence

    def RMC(self, *, now: dt) -> bytes:
        self.rmc[1] = now.strftime('%H%M%S.%f')
        self.rmc[3] = '%.4f' % self.GoogleMaptoGPS(val=self.lat)
        self.rmc[5] = '%.4f' % self.GoogleMaptoGPS(val=self.lng)
        self.rmc[7] = '%.1f' % self.sog
        self.rmc[8] = '%.1f' % self.cog
        self.rmc[9] = now.strftime('%y%m%d')

        body: str = ','.join(self.rmc)
        cs: str = '*%02X' % self.checkSum(body=body.encode())
        # nmea: str = '$%s%s' % (body, cs)
        nmea: str = body + cs
        sentence = (nmea + '\r\n').encode()
        return sentence

    def run(self) -> None:

        logger.debug('Start mg=%s mp=%d speed=%f, heading=%f' % (self.group,self.port,self.sog,self.cog))
        with closing(socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)) as sock:
            sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 1)

            while self.running:

                distance: float = ((self.sog * 1000 * 1.852) / 3600) * self.interval
                theta: float = math.radians((self.cog * -1) + 90)

                latS: float = (distance * math.sin(theta)) / self.latMeterPerSec
                self.lat = ((self.lat * 3600) + latS) / 3600

                lngS: float = (distance * math.cos(theta)) / self.lngMeterPerSec
                self.lng = ((self.lng * 3600) + lngS) / 3600

                now = dt.utcnow()

                for sentence in [self.RMC(now=now), self.GGA(now=now), self.ZDA(now=now), self.GLL(now=now)]:
                    f = self.F450(nmea=sentence)
                    print(f)
                    try:
                        sock.sendto(f, (self.group, self.port))
                    except KeyboardInterrupt as e:
                        break
                    except socket.error as e:
                        print(e)
                    else:
                        pass

                time.sleep(1)


if __name__ == '__main__':

    sog = 30
    cog = 45
    mg = '239.192.0.1'
    mp = 56001
    parser = argparse.ArgumentParser()
    parser.add_argument('--speed', type=int, default=sog, help='速度(初期値: %d)' % sog)
    parser.add_argument('--heading', type=int, default=cog, help='方角(初期値: %d)' % cog)
    parser.add_argument('--group', type=str, default=mg, help='マルチキャストグループ(初期値: %s)' % mg)
    parser.add_argument('--port', type=int, default=mp, help='マルチキャストポート(初期値: %d)' % mp)

    args = parser.parse_args()

    g = GPSSendor(sog=args.speed, cog=args.heading, mg=args.group, mp=args.port)
    g.start()

    while True:
        try:
            time.sleep(60)
        except (KeyboardInterrupt, ) as e:
            logger.error(e)
            g.running = False
            break