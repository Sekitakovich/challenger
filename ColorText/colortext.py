from dataclasses import dataclass

class Decorator(object):
    RESET = '\033[0m'  # 全てリセット

    @dataclass()
    class ForeGround(object):
        BLACK: str = '\033[30m'  # (文字)黒
        RED: str = '\033[31m'  # (文字)赤
        GREEN: str = '\033[32m'  # (文字)緑
        YELLOW: str = '\033[33m'  # (文字)黄
        BLUE: str = '\033[34m'  # (文字)青
        MAGENTA: str = '\033[35m'  # (文字)マゼンタ
        CYAN: str = '\033[36m'  # (文字)シアン
        WHITE: str = '\033[37m'  # (文字)白
        DEFAULT: str = '\033[39m'  # 文字色をデフォルトに戻す

    @dataclass()
    class Attribute():
        BOLD = '\033[1m'  # 太字
        UNDERLINE = '\033[4m'  # 下線
        INVISIBLE = '\033[08m'  # 不可視
        REVERCE = '\033[07m'  # 文字色と背景色を反転

    @dataclass()
    class BackGround():
        BG_BLACK: str = '\033[40m'  # (背景)黒
        BG_RED: str = '\033[41m'  # (背景)赤
        BG_GREEN: str = '\033[42m'  # (背景)緑
        BG_YELLOW: str = '\033[43m'  # (背景)黄
        BG_BLUE: str = '\033[44m'  # (背景)青
        BG_MAGENTA: str = '\033[45m'  # (背景)マゼンタ
        BG_CYAN: str = '\033[46m'  # (背景)シアン
        BG_WHITE: str = '\033[47m'  # (背景)白
        BG_DEFAULT: str = '\033[49m'  # 背景色をデフォルトに戻す

    @classmethod
    def paint(cls, *, src: str, color: str) -> str:
        result = f'{color}{src}{cls.RESET}'
        return result


if __name__ == '__main__':
    def main():

        sample = Decorator.paint(src='sample', color=Decorator.ForeGround.CYAN)
        print(sample)
        pass


    main()
