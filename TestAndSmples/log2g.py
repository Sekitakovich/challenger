from loguru import logger


class LoguruStart(object):

    logFile: str = 'logs/sample.log'

    @classmethod
    def init(cls):

        logger.level('DEBUG')
        logger.add(cls.logFile, rotation='1 day', retention='15 day', level='INFO', encoding='utf-8')


class Sample(object):

    def __init__(self):

        logger.debug('tako')
        logger.warning('ika')
        logger.info('日本人')


if __name__ == '__main__':

    LoguruStart.init()

    s = Sample()

