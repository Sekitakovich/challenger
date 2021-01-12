import time
from threading import Thread, Event
from loguru import logger


class Child(Thread):
    def __init__(self, *, quit: Event):
        super().__init__()
        self.daemon = False
        self.counter: int = 0
        self.quitEvent = quit
        self.loop: bool = True

        Thread(target=self.loopKeeper, daemon=True).start()

    def loopKeeper(self):
        logger.debug('%s: start waiting' % self.name)
        self.quitEvent.wait()
        logger.debug('%s: catch!' % self.name)
        try:
            raise KeyboardInterrupt
        except KeyboardInterrupt as e:
            pass
        self.loop = False

    def run(self) -> None:
        try:
            while self.loop:
                logger.debug('%s: +++ %d' % (self.name, self.counter))
                time.sleep(1)
                self.counter += 1
        except KeyboardInterrupt as e:
            logger.error(e)
            self.loop = False

        logger.debug('%s: in cleanup' % self.name)
        time.sleep(2)
        logger.debug('%s: completed' % self.name)


if __name__ == '__main__':
    qe = Event()

    c = Child(quit=qe)
    c.start()

    time.sleep(1)

    d = Child(quit=qe)
    d.start()

    time.sleep(3)
    logger.info('set quit event')
    qe.set()
    logger.info('waiting join')
    c.join()
    d.join()
    logger.info('Fin')
