from typing import Dict
from threading import Event, Lock
from dataclasses import dataclass
from datetime import datetime as dt
from copy import deepcopy


class EventPlus(object):
    '''
    threading.Event ++

    Ver 1.0 at 2020-10-10 debut
    '''

    @dataclass()
    class __Mail(object):
        '''
        received data structure
        '''
        isValid: bool = True  # if False: value is invalid(timeout)
        value: any = None
        setter: str = ''  # from
        passed: float = 0  # waited secs

    @dataclass()
    class __Stock(object):
        '''
        inner storage
        '''
        at: dt  # refresh datetime
        event: Event
        value: any = None
        setter: str = ''  # from

    __stock: Dict[str, __Stock] = {}
    __locker = Lock()
    __defaultChannelName = 'default'
    __defaultSetter = 'default'

    @classmethod
    def __takeChannel(cls, *, channel: str) -> __Stock:
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
    def set(cls, *, channel: str = __defaultChannelName, value: any, setter: str = __defaultSetter) -> None:
        '''
        send data
        :param channel: identifier for channel
        :param value: aby! any! any!
        :param setter: from
        :return: none
        '''
        target = cls.__takeChannel(channel=channel)
        with cls.__locker:
            target.value = value
            target.setter = setter
            target.at = dt.now()
            target.event.set()

    @classmethod
    def wait(cls, *, channel: str = __defaultChannelName, timeout: float = 0, raiseme: bool = False) -> __Mail:
        '''
        receive data
        :param channel: identifier for channel
        :param timeout: secs(same as Event.wait)
        :param raiseme: if True raise TimeoutError on timeout
        :return: Mail
        '''
        target = cls.__takeChannel(channel=channel)
        mail = cls.__Mail()
        if target.event.wait(timeout=timeout if timeout else None):
            with cls.__locker:
                target.event.clear()
                mail.passed = (dt.now() - target.at).total_seconds()
                mail.value = deepcopy(target.value)
                mail.setter = target.setter
        else:
            mail.isValid = False
            if raiseme:
                raise TimeoutError('Timeout(%f secs) has occured at channel[%s]' % (timeout, channel))

        return mail
