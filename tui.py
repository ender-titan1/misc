import os, math
from abc import ABC, abstractmethod
from typing import Dict, Callable
from getch import getch
from displayable import Displayable

class UI(ABC):
    @abstractmethod
    def update(self):
        pass

    @abstractmethod
    def on_goto(self, from_ui):
        pass

    @abstractmethod
    def on_input(self, key: str):
        pass

    @abstractmethod
    def get_interface(self):
        pass

    @abstractmethod
    def bind_interface(self, id, interface):
        pass

    def on_bind(self, interface):
        pass

class AbstractSelection(UI, Displayable):
    def __init__(self, sel_len: int):
        self.interface = None
        self.idx = 0
        self.sel_len = sel_len
        self.id = None

    def bind_interface(self, id, interface):
        self.interface = interface
        self.id = id

    def get_interface(self):
        return self.interface

    def on_goto(self, from_ui):
        self.idx = 0

    def on_input(self, key: str):
        if key == "down":
            self.idx += 1
        if key == "up":
            self.idx -= 1

        if self.idx >= self.sel_len:
            self.idx = self.sel_len - 1
        if self.idx < 0:
            self.idx = 0

    def get_width(self):
        return 30
    
    def get_height(self):
        return self.sel_len


class SimpleSelection(AbstractSelection):
    def __init__(self, selection: Dict[str, Callable[[UI, str], None]]):
        super().__init__(len(selection))
        self.selection = selection

    def on_goto(self, from_ui):
        self.idx = 0

    def on_input(self, key: str):
        super().on_input(key)

        if key == "enter":
            for i, (k, v) in enumerate(zip(self.selection.keys(), self.selection.values())):
                if i == self.idx:
                    v(self, k)

    def __repr__(self):
        out = ""
        for i, s in enumerate(self.selection.keys()):
            out += s
            if self.idx == i:
                out += " <\n"
            else:
                out += "\n"

        return out

    def update(self):
        print(str(self))

    def get_width(self):
        return 30


class TUI:
    def __init__(self):
        self.current_ui: UI = None
        self.uis = {}
        self.input_map = {}
        self.quit = False
        self.state = {}

    def add_input(self, key: str, *ids: str):
        for id in ids:
            self.input_map[id.lower()] = key
        return self

    def add_ui(self, ui: UI, id: str):
        self.uis[id] = ui
        ui.bind_interface(id, self)
        ui.on_bind(self)
        return self
    
    def add_nav(self):
        self.add_input("up", "UP_ARROW", "w") \
            .add_input("down", "DOWN_ARROW", "s") \
            .add_input("enter", "\r", "\n") \
            .add_input("left", "LEFT_ARROW", "a") \
            .add_input("right", "RIGHT_ARROW", "d")
        return self

    def goto(self, id: str):
        if id not in self.uis.keys():
            return
        
        old_ui = self.current_ui
        self.current_ui = self.uis[id]
        self.current_ui.on_goto(old_ui)

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
        try:
            key = self.input_map[char.lower()]
        except(KeyError):
            key = char
        self.current_ui.on_input(key)

    @staticmethod
    def navigate(ui: UI, string: str):
        ui.get_interface().goto(string)

if __name__ == "__main__":
    interface = TUI()
    start = SimpleSelection({
        "start": TUI.navigate,
        "options": TUI.navigate,
        "quit": lambda ui, s: ui.get_interface().quit_app()
    })

    options = SimpleSelection({
        "gameplay": lambda ui, s: print("Changing Gameplay"),
        "audio": lambda ui, s: print("Changing Audio"),
        "back": lambda ui, s: TUI.navigate(ui, "start_menu")
    })

    interface.add_ui(start, "start_menu") \
        .add_ui(options, "options") \
        .add_input("up", "UP_ARROW", "w") \
        .add_input("down", "DOWN_ARROW", "s") \
        .add_input("enter", "\r", "\n")

    interface.goto("start_menu")
    interface.update()
    interface.main()