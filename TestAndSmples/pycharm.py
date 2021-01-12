from dataclasses import dataclass

@dataclass()
class Profeel(object):
    name: str
    age: int
    gauge: float

class Sample(object):

    def __init__(self):
        self.onDict = {
            'name': 'sekitakovich',
            'age': 18,
            'gauge': 45.6,
        }
        self.onDC = Profeel(name='sekitakovich', age=18, gauge=100.0)


if __name__ == '__main__':

    s = Sample()

    name = s.onDC.name