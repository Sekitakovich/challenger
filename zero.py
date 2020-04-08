import logzero


class Sample(object):

    def __init__(self, *, file: str = 'logs/python.log'):

        self.logfile: str = file

        if file:
            logzero.logfile(filename=self.logfile)

    def debug(self, *, msg: str):
        logzero.logger.debug(msg)


if __name__ == '__main__':

    s = Sample()

    s.debug(msg='Hi!')
