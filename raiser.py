import time
from threading import Thread, Event
from loguru import logger


class Child(Thread):
    def __init__(self, *, quit: Event):
        super().__init__()
        self.daemon = True
        self.counter: int = 0
        self.quitEvent = quit
        self.loop: bool = True

        Thread(target=self.loopKeeper, daemon=True).start()

    def loopKeeper(self):
        logger.debug('start waiting')
        self.quitEvent.wait()
        self.loop = False
        logger.debug('catch!')

    def run(self) -> None:
        try:
            while self.loop:
                logger.info('+++ %d' % self.counter)
                time.sleep(1)
                self.counter += 1
        except KeyboardInterrupt as e:
            logger.error(e)
            self.loop = False

        logger.debug('completed')


if __name__ == '__main__':

    qe = Event()

    c = Child(quit=qe)
    c.start()

    time.sleep(3)
    logger.info('set quit event')
    qe.set()
    logger.info('waiting join')
    c.join()
    logger.info('Fin')
