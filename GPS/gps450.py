from typing import List
from datetime import datetime as dt
from contextlib import closing
import time
import math
import socket
from threading import Thread, Event
from functools import reduce
from operator import xor
from loguru import logger
from hexdump import hexdump
import argparse


class GPS450(object):

    def __init__(self, *, sog: float, cog: float, mg: str, mp: int, interval: int, sfi: str):

        self.running: bool = True

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
        self.interval = interval
        self.sfi = sfi.encode()

        rmc = 'GPRMC,085120.307,A,3541.1493,N,13945.3994,E,000.0,240.3,181211,,,A'
        self.rmc: List[str] = rmc.split(',')
        gga = 'GPGGA,085120.307,3541.1493,N,13945.3994,E,1,08,1.0,6.9,M,35.9,M,,0000'
        self.gga: List[str] = gga.split(',')
        gll = 'GPGLL,3421.7686,N,13222.3345,E,073132,A,A'
        self.gll: List[str] = gll.split(',')
        zda = 'GPZDA,082220.00,09,01,2006,0,0'
        self.zda: List[str] = zda.split(',')

        self.counter = 1
        self.timerEvent = Event()
        self.te = Thread(target=self.intervalTimer, daemon=True)
        self.te.start()

    def intervalTimer(self):
        while self.running:
            self.timerEvent.set()
            time.sleep(self.interval)

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

    def docking(self, *, body: str) -> bytes:
        cs: str = '*%02X' % self.checkSum(body=body.encode())
        nmea: str = '$' + body + cs
        sentence = (nmea + '\r\n').encode()
        return sentence

    def ZDA(self, *, now: dt) -> bytes:
        self.zda[1] = now.strftime('%H%M%S.%f')[:-3]
        self.zda[2] = str(now.day)
        self.zda[3] = str(now.month)
        self.zda[4] = str(now.year)

        return self.docking(body=','.join(self.zda))

    def GLL(self, *, now: dt) -> bytes:
        self.gll[1] = '%.4f' % self.GoogleMaptoGPS(val=self.lat)
        self.gll[3] = '%.4f' % self.GoogleMaptoGPS(val=self.lng)
        self.gll[5] = now.strftime('%H%M%S.%f')[:-3]

        return self.docking(body=','.join(self.gll))

    def GGA(self, *, now: dt) -> bytes:
        self.gga[1] = now.strftime('%H%M%S.%f')[:-3]
        self.gga[2] = '%.4f' % self.GoogleMaptoGPS(val=self.lat)
        self.gga[4] = '%.4f' % self.GoogleMaptoGPS(val=self.lng)

        return self.docking(body=','.join(self.gga))

    def RMC(self, *, now: dt) -> bytes:
        self.rmc[1] = now.strftime('%H%M%S.%f')[:-3]
        self.rmc[3] = '%.4f' % self.GoogleMaptoGPS(val=self.lat)
        self.rmc[5] = '%.4f' % self.GoogleMaptoGPS(val=self.lng)
        self.rmc[7] = '%.1f' % self.sog
        self.rmc[8] = '%.1f' % self.cog
        self.rmc[9] = now.strftime('%y%m%d')

        return self.docking(body=','.join(self.rmc))

    def start(self) -> None:

        try:
            logger.debug('Start mg=%s mp=%d speed=%f, heading=%f interval %d(secs)' % (
            self.group, self.port, self.sog, self.cog, self.interval))
            with closing(socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)) as sock:
                sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 1)

                while self.running:

                    if self.timerEvent.wait():
                        self.timerEvent.clear()

                        distance: float = ((self.sog * 1000 * 1.852) / 3600) * self.interval
                        theta: float = math.radians((self.cog * -1) + 90)

                        latS: float = (distance * math.sin(theta)) / self.latMeterPerSec
                        self.lat = ((self.lat * 3600) + latS) / 3600

                        lngS: float = (distance * math.cos(theta)) / self.lngMeterPerSec
                        self.lng = ((self.lng * 3600) + lngS) / 3600

                        logger.info('+++ sendto %s' % self.group)
                        now = dt.utcnow()

                        for sentence in [self.RMC(now=now), self.GGA(now=now), self.ZDA(now=now), self.GLL(now=now)]:
                            f = self.F450(nmea=sentence)
                            sock.sendto(f, (self.group, self.port))
                            print(f)

                    else:
                        break
        except (KeyboardInterrupt,) as e:
            self.running = False
        except (socket.error, socket.gaierror) as e:
            logger.error(e)
            self.running = False
        else:
            pass


if __name__ == '__main__':
    version = '2.03'

    sog = 30
    cog = 45
    mg = '239.192.0.1'
    mp = 56001
    interval = 1
    sfi = 'GP0001'

    parser = argparse.ArgumentParser()
    parser.add_argument('--speed', type=int, default=sog, help='速度(初期値: %d)' % sog)
    parser.add_argument('--heading', type=int, default=cog, help='方角(初期値: %d)' % cog)
    parser.add_argument('--interval', type=int, default=interval, help='出力間隔(初期値: %d)' % interval)
    parser.add_argument('--group', type=str, default=mg, help='マルチキャストグループ(初期値: %s)' % mg)
    parser.add_argument('--port', type=int, default=mp, help='マルチキャストポート(初期値: %d)' % mp)
    parser.add_argument('--sfi', type=str, default=sfi, help='SFI(初期値: %s)' % sfi)
    parser.add_argument('--version', action='version', version=version)

    args = parser.parse_args()

    g = GPS450(sog=args.speed, cog=args.heading, mg=args.group, mp=args.port, interval=args.interval, sfi=args.sfi)
    g.start()

    # while True:
    #     try:
    #         time.sleep(60)
    #     except (KeyboardInterrupt, ) as e:
    #         logger.error(e)
    #         g.running = False
    #         break
