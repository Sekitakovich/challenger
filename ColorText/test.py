'''
pythonで引数の候補を設定できる仕組みがあればと願う
'''

if __name__ == '__main__':
    def main(*, ooo: int) -> int:
        value = ooo + 1
        return value

    ooo = main(ooo='a')
    print(ooo)