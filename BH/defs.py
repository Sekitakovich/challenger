from dataclasses import dataclass


@dataclass()
class Note(object):
    key: int  # 鍵盤の位置
    volume: int  # 打鍵の強さ

