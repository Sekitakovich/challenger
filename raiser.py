import time
from threading import Thread, Event
from loguru import logger


class Child(Thread):
    def __init__(self, *, quit: Event):
        super().__init__()
        self.daemon = True
        self.counter: int = 0
        self.quit = quit
        self.loop: bool = True

        Thread(target=self.waiter, daemon=True).start()

    def waiter(self):
        logger.debug('... waiting')
        self.quit.wait()
        logger.debug('Roger')
        self.loop = False

    def run(self) -> None:
        try:
            while self.loop:
                logger.info('+++ %d' % self.counter)
                time.sleep(1)
                self.counter += 1
        except KeyboardInterrupt as e:
            logger.error(e)
            loop = False

        logger.debug('Bye!')


if __name__ == '__main__':

    qe = Event()

    c = Child(quit=qe)
    c.start()

    time.sleep(3)
    qe.set()
    c.join()
