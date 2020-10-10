class Sample(object):

    sono1: str = 'a'

    def __init__(self):

        self.sono2:str = 'b'
        sono3: str = 'c'
        sono1 = 'd'

    @classmethod
    def show(cls):
        print(cls.sono1)

s = Sample()
print(s)

o = Sample.show()
print(o)