from tui import *
from typing import List, Callable
from abc import ABC, abstractmethod
from termcolor import cprint, colored
import os

class Option(ABC):
    def __init__(self, name: str, action: Callable[[ActionContext], None]):
        self.action = action
        self.name = name

    @abstractmethod
    def __repr__(self):
        pass

    def on_input(self, key):
        pass

    def on_bind(self, manager: InterfaceManager, parent: InterfaceComponent):
        pass

    def reset(self, manager):
        pass

class DropdownOption(Option):
    def __init__(self, name, options, default):
        super().__init__(name, lambda ctx: ctx.manager.goto(f"__option__{self.name}"))
        self.default = default
        self.options = options
        self.current = options[default]

    def on_bind(self, manager, parent):
        option_ui = SimpleSelection({
            s: (lambda _: DropdownOption.selection_method(manager, parent, self, s)) for s in self.options
        })

        manager.add_ui(option_ui, f"__option__{self.name}")

        manager.state[f"__option__{self.name}"] = self.current

    def __repr__(self):
        return f"[{self.current}] ▼"
    
    @staticmethod
    def selection_method(manager, parent, option, s):
        manager.goto(parent.id)
        option.current = s
        manager.state[f"__option__{option.name}"] = option.current

class SliderOption(Option):
    def __init__(self, name, 
                 default: int, max: int, fill: bool = True,
                 left_label: str = "", right_label: str = ""):
        super().__init__(name, lambda ctx: ctx.ui.)
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

class ButtonOption(Option):
    def __init__(self, name, action):
        super().__init__(name, action)

    def __repr__(self):
        return self.name

class TextInputOption(Option):
    def __init__(self, name):
        super().__init__(name, lambda ui, s: TextInputOption.handler(ui, self, s))
        self.contents = ""

    def on_bind(self, manager, parent):

    def reset(self, manager):


    def __repr__(self):
        return self.contents

class OptionSelection(AbstractSelection):
    def __init__(self, selection: List[Option], padding=0, preprocessor=None):
        super().__init__(len(selection))
        self.selection = selection

        self.preprocessor = preprocessor
        self.padding = padding
        self.max_name_len = max([len(o.name) for o in selection])
        self.edit_mode = False
        self.parent = None

    def on_goto(self, from_ui):
        if from_ui == None:
            return
        
        self.edit_mode = False
        
        if not "__option__" in from_ui.id:
            self.idx = 0

    def on_bind(self, manager):
        for o in self.selection:
            o.on_bind(manager, self)

    def on_input(self, key):
        if not self.edit_mode:
            super().on_input(key)
        
        if key == "enter":
            self.edit_mode = not self.edit_mode

        for i, o in enumerate(self.selection):
            if i == self.idx and self.edit_mode:
                if key == "enter":
                    o.action(ActionContext(self, self.get_manager(), o.name))
                else:
                    o.on_input(key)

    def __repr__(self):
        return ""

    def reset(self):
        for option in self.selection:
            option.reset(self.get_manager())

    def update(self):
        if self.preprocessor != None:
            self.preprocessor(self.get_manager())

        for i, o in enumerate(self.selection):
            if type(o) is ButtonOption:
                btn_str = str(o)

                if i == self.idx:
                    btn_str += " <"

                print(btn_str)
                continue

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

#if __name__ == "__main__":
#
#    so = SliderOption("Volume", Option.edit, 3, 10, False, "Quiet", "Loud")
#    so2 = SliderOption("Test", Option.edit, 3, 6)
#    dropdown = DropdownOption("Difficulty", ["Easy", "Medium", "Hard"], 0)
#    advanced_btn = ButtonOption("Advanced Options", lambda ui, s: TUI.navigate(ui, "Advanced"))
#    back = ButtonOption("Back", lambda ui, s: TUI.navigate(ui, "Main"))
#    options = OptionSelection([so, so2, dropdown, advanced_btn, back], 1)
#
#    debug_mode = DropdownOption("Debug Mode", ["Disabled", "Enabled"], 0)
#    xp_multiplier = SliderOption("XP Multiplier", Option.edit, 1, 5, False, "x1", "x5")
#    textfield = TextInputOption("Name")
#    back2 = ButtonOption("Back", lambda ui, s: TUI.navigate(ui, "Options"))
#
#    advanced = OptionSelection([debug_mode, textfield, xp_multiplier, back2], 1)
#
#    main = SimpleSelection({"Start": None, "Options": TUI.navigate})
#    manager = TUI() \
#        .add_ui(main, "Main") \
#        .add_ui(options, "Options") \
#        .add_ui(advanced, "Advanced") \
#        .add_nav()
#
#    manager.goto("Main")
#    manager.update()
#    manager.main()