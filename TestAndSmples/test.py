from dataclasses import dataclass


# dataclass()
class Code(object):

    BS: bytes = b'\x08'
    ESC: bytes = b'\x1b'

c = Code.ESC
print(c)
