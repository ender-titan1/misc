from tui import InterfaceManager, SimpleSelection
from getch import getch
import os

DATA = [[10, 16, 20, 13, 9, 6, 4, 10, 12], [5, 6, 8, 10, 2, 15, 3, 16, 10]]

def display_value(func):
    def display_val(*args):
        os.system("clear")
        func(args[0])
        getch()
        args[0].goto("main")
        args[0].update()

    return display_val

@display_value
def total_sold(tui):
    print(sum(DATA[1]))

@display_value
def total_cost_sold(tui):
    print(sum([DATA[0][i] * DATA[1][i] for i in range(len(DATA[0]))]))

@display_value
def amount_under_10(tui):
    print(len( [ele for ele in DATA[1] if ele < 10] ))

@display_value
def amount_over_10(tui):
    print(len([ele for ele in DATA[1] if ele >= 10]))

item_selection = SimpleSelection({
    "Total items sold": lambda ui, s: total_sold(ui.get_interface()),
    "Total cost of items sold": lambda ui, s: total_cost_sold(ui.get_interface()),
    "Amount of items sold < 10": lambda ui, s: amount_under_10(ui.get_interface()),
    "Amount of items sold >= 10": lambda ui, s: amount_over_10(ui.get_interface()),
    "Quit": lambda ui, s: ui.get_interface().quit_app()
})

menu = InterfaceManager().add_nav().add_ui(item_selection, "main")
menu.goto("main")
menu.update()
menu.main()