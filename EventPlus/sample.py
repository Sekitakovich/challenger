from threading import Thread
from EventPlus.eventPlus import EventPlus
import time
import random
from loguru import logger

if __name__ == '__main__':
    '''
    test and sample for EventPlus
    '''


    class DefaultSetter(Thread):
        def __init__(self, *, name: str):
            super().__init__()
            self.daemon = True
            self.name = name

            self.value = [c for c in range(10)]

        def run(self) -> None:
            logger.info('+++ start [%s]' % self.name)
            for counter in range(1000):
                random.shuffle(self.value)
                logger.debug('[%s] set value %s' % (self.name, self.value))
                EventPlus.set(value=self.value)
                time.sleep(random.randint(1, 3))


    class DefaultGetter(Thread):
        def __init__(self, *, name: str):
            super().__init__()
            self.daemon = True
            self.name = name

        def run(self) -> None:
            logger.info('+++ start [%s]' % self.name)
            while True:
                mail = EventPlus.wait()
                if mail.isValid is True:
                    logger.info(
                        '[%s] got %s after %f secs' % (self.name, mail.value, mail.passed))
                else:
                    logger.error('[%s] timeout!' % (self.name))


    def main():
        DefaultGetter(name='DefaultGetter-1').start()
        DefaultGetter(name='DefaultGetter-2').start()
        DefaultGetter(name='DefaultGetter-3').start()
        DefaultSetter(name='DefaultSetter').start()
        while True:
            time.sleep(10)


    main()
