from threading import Thread, Event
import time
from typing import Dict
from loguru import logger


class Sub(Thread):

    def __init__(self, *, name: str, event: Event):
        super().__init__()
        self.name = name
        self.daemon = True
        self.event = event

    def run(self) -> None:
        counter: int = 0
        while True:
            self.event.wait()
            self.event.clear()
            logger.debug('%s: counter = %d' % (self.name, counter))
            counter += 1


class Main(object):

    def __init__(self):
        self.event = Event()
        self.sub: Dict[str, Sub] = {
            'sono1': Sub(name='sono1', event=self.event),
            'sono2': Sub(name='sono2', event=self.event),
        }
        for k, v in self.sub.items():
            v.start()


if __name__ == '__main__':

    main = Main()

    while True:
        time.sleep(1)
        main.event.set()

