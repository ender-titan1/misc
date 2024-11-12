import os, math
from abc import ABC, abstractmethod
from typing import Dict, Callable
from getch import getch

class UI(ABC):
    @abstractmethod
    def update(self):
        pass

    @abstractmethod
    def on_input(self, key: str):
        pass

    @abstractmethod
    def get_interface(self):
        pass

    @abstractmethod
    def bind_interface(self, interface):
        pass

class SimpleSelection(UI):
    def __init__(self, selection: Dict[str, Callable[[UI, str], None]]):
        self.selection = selection
        self.interface = None
        self.idx = 0

    def bind_interface(self, interface):
        self.interface = interface

    def get_interface(self):
        return self.interface

    def on_input(self, key: str):
        if key == "down":
            self.idx += 1
        if key == "up":
            self.idx -= 1

        if self.idx >= len(self.selection):
            self.idx = len(self.selection) - 1
        if self.idx < 0:
            self.idx = 0

        if key == "enter":
            for i, (k, v) in enumerate(zip(self.selection.keys(), self.selection.values())):
                if i == self.idx:
                    v(self, k)


    def update(self):
        for i, s in enumerate(self.selection.keys()):
            print(s, end="")
            if self.idx == i:
                print(" <")
            else:
                print()


class Interface:
    def __init__(self):
        self.current_ui: UI = None
        self.uis = {}
        self.input_map = {}
        self.quit = False

    def add_input(self, key: str, *ids: str):
        for id in ids:
            self.input_map[id.lower()] = key
        return self

    def add_ui(self, ui: UI, id: str):
        self.uis[id] = ui
        ui.bind_interface(self)
        return self

    def goto(self, id: str):
        if id not in self.uis.keys():
            return
        
        self.current_ui = self.uis[id]

    def update(self):
        os.system("clear")
        self.current_ui.update()

    def main(self):
        while not self.quit:
            self.await_input()
            self.update()

    def quit_app(self):
        self.quit = True

    def await_input(self):
        char = getch()
        key = self.input_map[char.lower()]
        self.current_ui.on_input(key)

    @staticmethod
    def navigate(ui: UI, string: str):
        ui.get_interface().goto(string)


interface = Interface()
selection = SimpleSelection({
    "start": Interface.navigate,
    "options": Interface.navigate,
    "quit": lambda ui, s: ui.get_interface().quit_app()
})

interface.add_ui(selection, "start_menu") \
    .add_input("up", "UP_ARROW", "w") \
    .add_input("down", "DOWN_ARROW", "s") \
    .add_input("enter", "\r", "\n")

interface.goto("start_menu")
interface.update()
interface.main()