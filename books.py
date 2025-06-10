from tui import TUI, SimpleSelection
from menus import OptionSelection, TextInputOption, ButtonOption, DropdownOption
from getch import getch
from dataclasses import dataclass
import re
import os

books = []

@dataclass
class Book():
    title: str
    author: str
    year: int

def view_all(tui: TUI):
    os.system("clear")

    query = tui.state["__field__Filter"]
    sort = tui.state["__option__Sort"]
    dir = tui.state["__option__Direction"]

    def sorting_func(b: Book):
        if sort == "Title":
            return b.title
        if sort == "Author":
            return b.author
        if sort == "Year":
            return b.year
        
        raise Exception("Invalid dropdown value")

    books.sort(key=sorting_func, reverse=(dir != "Ascending"))

    b: Book
    for b in books:

        if query != "" and query.lower() not in b.title.lower():
            continue

        print(f"{b.title.ljust(20)} | {b.author.ljust(20)} | {b.year}")

    print("")

def add_book(tui: TUI):
    global add_book_menu
    os.system("clear")

    year = tui.state["__field__Year"]
    title = tui.state["__field__Title"]
    author = tui.state["__field__Author"]

    m = re.findall("^[0-9]{4}$", year)

    if len(m) != 1:
        print("Error: Invalid Date")
        getch()
        tui.goto("add_book")
        tui.update()
        return
    
    if title == "" or author == "":
        print("Error: No author or title provided")
        getch()
        tui.goto("add_book")
        tui.update()
        return
    
    book = Book(title, author, int(year))
    books.append(book)

    print("Do you want to add another? [Y/N] ")
    ch = getch()

    if ch == "y":

        add_book_menu.reset()

        tui.goto("add_book")
        tui.update()
    else:
        with open("books.csv", "w") as file:
            for b in books:
                file.write(f"{b.title},{b.author},{b.year}\n")
        
        tui.goto("main")
        tui.update()

title = TextInputOption("Title")
author = TextInputOption("Author")
year = TextInputOption("Year")
add = ButtonOption("Add Book", lambda ui, s: add_book(ui.get_interface()))
back = ButtonOption("Back", lambda ui, s: TUI.navigate(ui, "main"))
filter = TextInputOption("Filter")
sort = DropdownOption("Sort", ["Title", "Author", "Year"], 0)
direction = DropdownOption("Direction", ["Ascending", "Descending"], 0)

add_book_menu = OptionSelection([title, author, year, add, back], 1)

view_menu = OptionSelection([filter, sort, direction, back], 1, preprocessor=view_all)

main_menu = SimpleSelection({
    "Add new books": lambda ui, s: TUI.navigate(ui, "add_book"),
    "View all books": lambda ui, s: TUI.navigate(ui, "view"),
    "Quit": lambda ui, s: ui.get_interface().quit_app()
})

with open("books.csv", "r") as file:
    for line in file.readlines():
        data = line.split(",")
        print(data)
        book = Book(data[0], data[1], int(data[2]))
        books.append(book)

    getch()

interface = TUI().add_nav() \
    .add_ui(main_menu, "main") \
    .add_ui(add_book_menu, "add_book") \
    .add_ui(view_menu, "view")

interface.goto("main")
interface.update()
interface.main()