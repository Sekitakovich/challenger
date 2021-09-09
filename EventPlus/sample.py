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


    class OptionSetter(Thread):
        def __init__(self, *, name: str, channel: str):
            super().__init__()
            self.daemon = True
            self.name = name
            self.channel = channel

            self.value = [c for c in range(10)]

        def run(self) -> None:
            logger.info('+++ start [%s] on channel=%s' % (self.name, self.channel))
            for counter in range(1000):
                random.shuffle(self.value)
                logger.debug('[%s] set value %s to [%s]' % (self.name, self.value, self.channel))
                EventPlus.set(value=self.value, channel=self.channel, setter=self.name)
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
                if mail.inTime is True:
                    logger.info(
                        '[%s] after %f secs' % (self.name,  mail.passed))
                else:
                    logger.error('[%s] timeout!' % (self.name))


    class OptionGetter(Thread):
        def __init__(self, *, name: str, timeout: float, channel: str):
            super().__init__()
            self.daemon = True
            self.name = name
            self.channel = channel
            self.timeout = timeout

        def run(self) -> None:
            logger.info('+++ start [%s] on channel=%s timeout=%f' % (self.name, self.channel, self.timeout))
            while True:
                try:
                    mail = EventPlus.wait(channel=self.channel, timeout=self.timeout, raiseme=True)
                except (TimeoutError) as e:
                    logger.error(e)
                else:
                    logger.info(
                        '[%s] from [%s] at [%s] after %f secs' % (
                            self.name, mail.setter, self.channel, mail.passed))


    def main():
        DefaultGetter(name='DefaultGetter-1').start()
        DefaultGetter(name='DefaultGetter-2').start()
        OptionGetter(name='OptionGetter-1', channel='CH1', timeout=2).start()
        DefaultSetter(name='DefaultSetter-1').start()
        OptionSetter(name='OptoinSetter-1', channel='CH1').start()
        while True:
            time.sleep(10)


    main()
