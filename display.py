from tui import TUI, UI, SimpleSelection
from abc import ABC, abstractmethod
from dataclasses import dataclass
from displayable import Displayable

@dataclass
class DisplayedUI:
    ui: UI
    tui: TUI
    base_layer: int
    row: int

class Display(UI):
    def __init__(self):
        self.id = None
        self.interface = None
        self.uis = []
        self.layers = []
        self.rows = []
        self.row_heights = {}

    def get_interface(self):
        return self.interface
    
    def bind_interface(self, id, interface):
        self.interface = interface
        self.id = id

    def add_ui(self, ui, tui, layer=0, row=0):
        self.uis.append(DisplayedUI(ui, tui, layer, row))

        if layer not in self.layers:
            self.layers.append(layer)

        if row not in self.rows:
            self.layers.append(row)

        return self

    def build(self):
        for row in self.rows:
            if row not in self.row_heights.keys():
                self.row_heights[row] = self.calc_max_row_height(row)

    def on_goto(self, from_ui):
        pass

    def on_input(self, key):
        return super().on_input(key)

    def calc_max_row_height(self, row):
        hmax = 0
        for ui in self.uis:
            if ui.row == row:
                hmax = max(hmax, ui.ui.get_height())

        return hmax

    def update(self):
        output = {}
        for layer in self.layers:
            for displayed_ui in self.uis:
                if displayed_ui.base_layer != layer:
                    continue

                ui_row = displayed_ui.row
                column_offset = 0

                for row in self.rows:
                    if row < ui_row:
                        column_offset += self.row_heights[row]

                text = str(displayed_ui.ui)
                lines = text.split('\n')
                ui = displayed_ui.ui
                width = ui.get_width()

                for i in range(self.row_heights[ui_row]):
                    line = ' ' * width
                    if i < len(lines):
                        line = lines[i]

                    if len(line) == 0:
                        continue

                    line = line.replace('\n', '')
                    line = line.ljust(width, " ")
                    line = '|' + line
                    
                    if i not in output.keys():
                        output[i] = ""

                    output[i] += line

        for i in range(len(output)):
            print(output[i])

tui = TUI()
test = SimpleSelection({"Test": None, "Blah": None, "Etc": None})
test2 = SimpleSelection({"This": None, "Is": None, "Inline": None, "Displayed": None})
display = Display().add_ui(test, tui).add_ui(test2, tui).build()

tui.add_ui(display, "Display").add_nav()

tui.goto("Display")
tui.update()
tui.main()