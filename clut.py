from PIL import Image

if __name__ == '__main__':
    def main():
        src = Image.open('TR.bmp')
        dst = src.convert('P')
        dst.save('TR.png')
        cp = dst.getpalette()
        plen = len(cp)
        print(f'size={plen} entries={plen//3}')
        pass

    main()