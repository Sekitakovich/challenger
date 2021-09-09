import loguru


class Sample(object):
    def __init__(self, *, name:str):
        self.logger = loguru.logger

        self.logger.debug(f'{name} START')


if __name__ == '__main__':
    def main():
        sono1 = Sample(name='sono1')
        sono2 = Sample(name='sono2')

        pass

    main()