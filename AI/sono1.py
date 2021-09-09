import cv2
import pathlib
from loguru import logger


class Main(object):
    def __init__(self, *, path: str='./IMGs'):
        self.path = pathlib.Path(path)

    def show(self, *, file: str):
        fullPath = self.path / file
        if fullPath.exists():
            try:
                filename = str(fullPath)
                mat = cv2.imread(filename=filename)
                if mat.size:
                    pass
                    # logger.info(mat)
                else:
                    logger.warning(f'not found f{filename}')
            except (cv2.error, AttributeError) as e:
                logger.error(e)
            else:
                cv2.imshow(winname='color', mat=mat)
                cv2.waitKey(delay=0)

        else:
            logger.error(f'{fullPath} not found')

if __name__ == '__main__':
    def main():
        M = Main()
        M.show(file='FK.jpg')
        pass


    main()
