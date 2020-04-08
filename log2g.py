from loguru import logger
import sys


class Sample(object):

    def __init__(self, *, file: str = 'logs/python.log'):

        self.logger = logger
        self.logfile: str = file

        # logger.remove()
        #
        # logger.add(
        #     sys.stderr,
        #     colorize=True,
        #     format='<white>{time:YYYY-MM-DD HH:mm:ss}</white> <level>{level} {file}:{line} {message}</level>',
        # )

        if file:
            logger.add(self.logfile, rotation='1 day', retention='15 day', level='WARNING')

    def trace(self, *, msg: str):
        self.logger.trace(msg)

    def debug(self, *, msg: str):
        self.logger.debug(msg)

    def info(self, *, msg: str):
        self.logger.info(msg)

    def success(self, *, msg: str):
        self.logger.success(msg)

    def warning(self, *, msg: str):
        self.logger.warning(msg)

    def error(self, *, msg: str):
        self.logger.error(msg)

    def critical(self, *, msg: str):
        self.logger.critical(msg)


if __name__ == '__main__':

    s = Sample()

    s.debug(msg='Hi!')