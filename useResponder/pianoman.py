import responder
import pathlib
from loguru import logger

from useResponder.common import Responder


class PianoMan(object):
    def __init__(self):
        self.path = pathlib.Path('MP3s')

    def listup(self):
        for file in self.path.iterdir():
            logger.info(file.name)

    def on_get(self, req: responder.Request, res: responder.Response):
        pass

if __name__ == '__main__':
    def main():
        P = PianoMan()
        P.listup()
        pass


    main()
