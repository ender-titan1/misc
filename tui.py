import os, math
from abc import ABC, abstractmethod
from typing import Dict, Callable
from getch import getch

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
    def bind_interface(self, interface):
        pass

class AbstractSelection(UI):
    def __init__(self, sel_len: int):
        self.interface = None
        self.idx = 0
        self.sel_len = sel_len

    def bind_interface(self, interface):
        self.interface = interface

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


    def update(self):
        for i, s in enumerate(self.selection.keys()):
            print(s, end="")
            if self.idx == i:
                print(" <")
            else:
                print()


class TUI:
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
        key = self.input_map[char.lower()]
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