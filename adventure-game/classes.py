from dataclasses import dataclass
from termcolor import colored
from enum import Enum

class Status(Enum):
    NONE = 0
    FREEZING = 1
    STARVING = 2

@dataclass
class Person:
    name: str
    health: int
    max_health: int
    status: Enum
    status_left: int
    status_max: int

    def __repr__(self):
        string = f"{self.name} | {'♥' * self.health}"
        
        if self.status != Status.NONE:
            string += f" | "
            string += colored(f"{'■' * self.status_left}{'□' * (self.status_max - self.status_left)}", "red")

        return string

print(Person("Jack", 3, 4, Status.FREEZING, 3, 5))