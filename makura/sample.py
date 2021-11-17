from PIL import Image
import pathlib


class Magick(object):
    def __init__(self, *, file: str):
        self.src = pathlib.Path(file)
        self.img = Image.open(self.src)

    def to2(self):
        dst = self.img.convert(mode='1', dither=Image.FLOYDSTEINBERG)
        dst.show()
        name = self.src.stem + '_mode1' + '.PNG'
        dst.save(name)

        dst = self.img.convert(mode='P')
        dst.show()
        name = self.src.stem + 'modeP' + '.PNG'
        dst.save(name)

        dst = self.img.convert(mode='L')
        dst.show()
        name = self.src.stem + 'modeL' + '.PNG'
        dst.save(name)


if __name__ == '__main__':
    def main():
        mg = Magick(file='./kana.jpg')
        mg.to2()


    main()
