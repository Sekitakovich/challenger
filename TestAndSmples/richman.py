from dataclasses import dataclass
from rich.console import Console


@dataclass()
class Sample(object):
    name: str
    age: int
    tention: float


s = Sample(name='sekitakovich', age=18, tention=12)

console = Console()
console.print(s)