from tui import TUI, SimpleSelection
import os

DATA = []

def display_value(func):
    def display_val(*args):
        os.system("clear")
        func(args[0])
        args[0].goto("main")
        args[0].update()

    return display_val

@display_value
def total_sold(tui):
    print("Test od decorator")


item_selection = SimpleSelection({
    "Total items sold": lambda ui, s: total_sold(ui.get_interface()),
    "Total cost of items sold": None,
    "Amount of items sold < 10": None,
    "Amount of item sold >= 10": None,
    "Quit": lambda ui, s: ui.get_interface().quit_app()
})

menu = TUI().add_nav().add_ui(item_selection, "main")
menu.goto("main")
menu.update()
menu.main()