from tui import TUI, UI, SimpleSelection, AbstractSelection
from typing import List, Callable
from abc import ABC, abstractmethod
from termcolor import cprint, colored

class Option(ABC):
    def __init__(self, name: str, action: Callable[[UI, str], None]):
        self.action = action
        self.name = name

    @abstractmethod
    def __repr__(self):
        pass

    @abstractmethod
    def on_input(self, key):
        pass

    @staticmethod
    def edit(ui: UI, s: str):
        ui.get_interface().goto(f"__option__{s}")

class SliderOption(Option):
    def __init__(self, name, action, 
                 default: int, max: int, fill: bool = True,
                 left_label: str = "", right_label: str = ""):
        super().__init__(name, action)
        self.default = default
        self.current = default
        self.max = max
        self.fill = fill
        self.left = left_label
        self.right = right_label

    def on_input(self, key):
        if key == "left":
            self.current -= 1
        elif key == "right":
            self.current += 1

        if self.current > self.max:
            self.current = self.max
        
        if self.current < 1:
            self.current = 1

    def __repr__(self):
        empty_sq = "□"
        full_sq =  "■"
        remaining = (self.max - self.current)

        if (self.fill):
            string = (full_sq * self.current) + (empty_sq * remaining)
        else:
            empty = self.current - 1
            string = (empty_sq * empty) + full_sq + (empty_sq * remaining)

        return f"{self.left} {string} {self.right}"

class OptionSelection(AbstractSelection):
    def __init__(self, selection: List[Option], padding=0):
        super().__init__(len(selection))
        self.selection = selection

        self.padding = padding
        self.max_name_len = max([len(o.name) for o in selection])
        self.edit_mode = False

    def on_input(self, key):
        if not self.edit_mode:
            super().on_input(key)
        
        if key == "enter":
            self.edit_mode = not self.edit_mode

        for i, o in enumerate(self.selection):
            if i == self.idx and self.edit_mode:
                if key == "enter":
                    o.action(self, o.name)
                else:
                    o.on_input(key)

    def update(self):
        for i, o in enumerate(self.selection):
            padding = self.max_name_len - len(o.name) + self.padding

            if len(o.name) != self.max_name_len:
                padding -= 1

            option_str = str(o)

            if i == self.idx and self.edit_mode:
                option_str = colored(option_str, "black", "on_white", attrs=["bold"])

            text = f"{o.name}:{' ' * padding} {option_str}"
            
            if i == self.idx:
                text += " <"

            print(text)

so = SliderOption("Volume", Option.edit, 3, 10, False, "Quiet", "Loud")
so2 = SliderOption("Test", Option.edit, 3, 6)
options = OptionSelection([so, so2], 1)
tui = TUI() \
    .add_ui(options, "options") \
    .add_nav()

tui.goto("options")
tui.update()
tui.main()