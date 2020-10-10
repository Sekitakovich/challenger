from typing import Dict
from threading import Thread, Event, Lock
from dataclasses import dataclass
from datetime import datetime as dt
from copy import deepcopy


class EventPlus(object):
    '''
    '''

    @dataclass()
    class __Mail(object):
        '''
        received data structure
        '''
        timeout: bool = False  # if True: value is invalid
        value: any = None
        setter: int = 0  # from
        passed: float = 0  # waited secs

    @dataclass()
    class __Stock(object):
        '''
        inner storage
        '''
        at: dt  # refresh datetime
        event: Event
        value: any = None
        setter: int = 0  # from

    __stock: Dict[str, __Stock] = {}
    __locker = Lock()
    __defaultChannelName = 'default'

    @classmethod
    def __getChannel(cls, *, channel: str) -> __Stock:
        '''
        select target channel
        :param channel: identifier for channel
        :return: Stock
        '''
        with cls.__locker:
            if channel not in cls.__stock.keys():
                cls.__stock[channel] = cls.__Stock(event=Event(), at=dt.now())
        return cls.__stock[channel]

    @classmethod
    def set(cls, *, channel: str = __defaultChannelName, value: any, sender: int = 0) -> None:
        '''
        send data
        :param channel: identifier for channel
        :param value: aby! any! any!
        :param sender: from
        :return: none
        '''
        target = cls.__getChannel(channel=channel)
        with cls.__locker:
            target.value = value
            target.setter = sender
            target.at = dt.now()
            target.event.set()

    @classmethod
    def wait(cls, *, channel: str = __defaultChannelName, timeout: float = 0) -> __Mail:
        '''
        recieve data
        :param channel: identifier for channel
        :param timeout: secs(same as Event.wait)
        :return: Mail
        '''
        target = cls.__getChannel(channel=channel)
        mail = cls.__Mail()
        if target.event.wait(timeout=timeout if timeout else None):
            with cls.__locker:
                target.event.clear()
                mail.passed = (dt.now()-target.at).total_seconds()
                mail.value = deepcopy(target.value)
                mail.setter = target.setter
        else:
            mail.timeout = True

        return mail


if __name__ == '__main__':
    import time
    import random
    from loguru import logger


    class Setter(Thread):
        def __init__(self, *, name: str, channel: str, number: int):
            super().__init__()
            self.daemon = True

            self.name = name
            self.channel = channel
            self.number = number

            self.value = [c for c in range(10)]

        def run(self) -> None:
            logger.info('+++ start [%s]' % self.name)
            for counter in range(1000):
                random.shuffle(self.value)
                logger.debug('[%s] set value %s to [%s]' % (self.name, self.value, self.channel))
                EventPlus.set(value=self.value, sender=self.number, channel=self.channel)
                time.sleep(random.randint(1, 3))


    class Getter(Thread):
        def __init__(self, *, name: str, channel: str, timeout: int):
            super().__init__()
            self.daemon = True

            self.name = name
            self.channel = channel
            self.timeout = timeout

        def run(self) -> None:
            while True:
                mail = EventPlus.wait(timeout=self.timeout, channel=self.channel)
                if mail.timeout is False:
                    logger.info('[%s] %s from [%d] after %f secs' % (self.name, mail.value, mail.setter, mail.passed))
                else:
                    logger.error('[%s] timeout!' % (self.name))


    def main():
        Setter(name='sono1', number=1, channel='seki').start()
        Setter(name='sono2', number=2, channel='tako').start()
        Setter(name='sono3', number=3, channel='vich').start()
        Getter(name='SEKI', channel='seki', timeout=0).start()
        Getter(name='TAKO', channel='tako', timeout=0).start()
        Getter(name='VICH', channel='vich', timeout=0).start()
        Getter(name='AAAA', channel='vich', timeout=1).start()
        Getter(name='BBBB', channel='vich', timeout=2).start()
        while True:
            time.sleep(10)


    main()
