from dataclasses import dataclass
from datetime import datetime as dt
from queue import Queue
from typing import Dict


class QueuePlus(object):
    @dataclass()
    class QueuePack(object):
        data: any
        at: dt
        setter: str = ''

    __defaultChannel = 'default'
    __Qchannel: Dict[str, Queue] = {__defaultChannel: Queue()}

    @classmethod
    def put(cls, *, channel: str = __defaultChannel, data: any = None, setter: str = ''):
        item = cls.QueuePack(at=dt.now(), data=data, setter=setter)
        if channel not in cls.__Qchannel.keys():
            cls.__Qchannel[channel] = Queue()
        target = cls.__Qchannel[channel]
        for k, v in target.items():
            v.put(data)

    @classmethod
    def get(cls, *, channel: str = __defaultChannel, timeout: int = 0):
        pass
