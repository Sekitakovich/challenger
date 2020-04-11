from dataclasses import dataclass
from threading import Lock
from queue import Queue


@dataclass()
class WhiteBoard(object):

    msg: str = ''
    counter: int = 0

    locker: Lock = Lock()
    fifo: Queue = Queue()