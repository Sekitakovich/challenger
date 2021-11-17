import time
from threading import Thread
from loguru import logger


class BG(Thread):
    def __init__(self, interval: int=1):
        super().__init__()
        self.daemon = True

        self.counter = 0
        self.interval = interval

    def run(self) -> None:
        while True:
            try:
                time.sleep(self.interval)
            except (KeyboardInterrupt) as e:
                logger.debug(e)
                break
            else:
                logger.info(f'[{self.counter}]')
                self.counter += 1

    def abort(self):
        raise KeyboardInterrupt


if __name__ == '__main__':
    def main():
        s = BG()
        s.start()
        time.sleep(3)

        try:
            # s.abort()
            raise KeyboardInterrupt

        except (KeyboardInterrupt) as e:
            logger.warning(e)
        else:
            s.join()

    main()
