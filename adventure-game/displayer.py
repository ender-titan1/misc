from classes import Person, Resource, Status
import os

class Displayer:
    def __init__(self, witdh):
        self.witdh = witdh

    def screen(self, people, resources):
        height = max(len(people), len(resources))
        string = ""

        os.system("clear")

        for i in range(height):
            person = people.get(i)
            resource = resources.get(i)

            person_str = str(person)
            resource_str = str(resource)
            space = self.witdh - Person.LENGTH - Resource.LENGTH

            string += person_str
            string += ' ' * space
            string += resource_str
            string += "\n"

        print(string)
        print("-" * self.witdh)

d = Displayer(80)
p = Person("Jack", 4, Status.NONE, 0)
r2 = Resource("Heat", 10, "yellow")
r = Resource("Wood", 10, "green")

d.screen([p], [r, r2])