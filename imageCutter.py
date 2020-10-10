import pathlib
from PIL import Image

from loguru import logger


class ImageCutter(object):

    def __init__(self, *, dst: str = 'sample.png', dw: int = 1280, dh: int = 1024):
        self.W = dw
        self.H = dh
        self.dst = pathlib.Path(dst)
        if self.dst.exists() is False:
            logger.warning('%s is not exists' % self.dst)

    def crop(self, *, src: str) -> bool:
        success = True
        try:
            image = Image.open(src)
            W, H = image.size
            logger.info('Processing %s (W:H = %d:%d)' % (src, W, H))

            result = image.crop(((W - (self.W if W > self.W else W)) // 2,
                                 (H - (self.H if H > self.H else H)) // 2,
                                 (W + (self.W if W > self.W else W)) // 2,
                                 (H + (self.H if H > self.H else H)) // 2))

            result.save(self.dst)
        except (FileNotFoundError, PermissionError, OSError) as e:
            success = False
            logger.error(e)
        return success


if __name__ == '__main__':
    ImageCutter().crop(src='./imgs/kanagawa.png')
