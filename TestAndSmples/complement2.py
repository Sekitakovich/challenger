if __name__ == '__main__':
    def main():
        b = 0b11111110
        c = b.to_bytes(1,byteorder='little')
        d = int.from_bytes(c, byteorder='little', signed=True)
        print(b, c, d)
    main()
