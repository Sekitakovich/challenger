from threading import Thread
from EventPlus.eventPlus import EventPlus
import time
import random
from loguru import logger

if __name__ == '__main__':

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
