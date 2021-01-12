from dataclasses import dataclass
from datetime import datetime as dt
from queue import Queue
from typing import Dict, List


class QueuePlus(object):
    @dataclass()
    class QueuePack(object):
        data: any
        at: dt
        setter: str = ''

    __id: int = 0
    __defaultChannel = 'default'
    __Qchannel: Dict[str, List[int]] = {__defaultChannel: []}

    @classmethod
    def get(cls, *, channel: str = __defaultChannel) -> int:
        if channel not in cls.__Qchannel.keys():
            cls.__Qchannel[channel] = []
        cls.__id += 1
        cls.__Qchannel[channel].append(cls.__id)
        return cls.__id

