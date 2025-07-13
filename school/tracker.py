import os
from tui import InterfaceManager, SimpleSelection
from getch import getch

scores = []

def get_grade(score):
    if score > 80:
        return "A"
    if score > 70 and score < 80:
        return "B"
    if score > 60 and score < 70:
        return "C"
    if score > 50 and score < 60:
        return "D"
    if score > 40 and score < 50:
        return "E"
    else:
        return "U"

def view_all(tui):
    os.system("clear")

    for score in scores:
        (name, subj, score_n) = score.split(",")
        print(f"{name.ljust(20)} | {subj.ljust(20)} | {score_n.rjust(4)} | {get_grade(int(score_n))}")

    print("\nPress any key to exit")

    getch()
    tui.goto("main")
    tui.update()

def search(tui):
    os.system("clear")
    query = input("Search for name: ").replace(" ", "").lower()
    os.system("clear")

    for score in scores:
        (name, subj, score_n) = score.split(",")

        if query not in name.lower():
            continue

        print(f"{name.ljust(20)} | {subj.ljust(20)} | {score_n.rjust(4)} | {get_grade(int(score_n))}")

    print("\nPress any key to exit")

    getch()

    tui.goto("main")
    tui.update()

def add_score(tui):
    os.system("clear")
    name = input("What is the name of the student? ")
    name = name.replace(" ", "").capitalize()
    subject = input("What is the subject? ")
    subject = subject.replace(" ", "").capitalize()
    score_number = int(input("What was the score of this student? "))
    while score_number < 0 or score_number>100:
        print("The number is out of bounds!")
        score_number = int(input("What was the score of this student? "))
    scores.append(name + "," + subject + "," + str(score_number))

    print("\nAdd another? [Y/N] ")
    ch = getch()

    if ch.lower() == "y":
        add_score(tui)
    else:

        with open("scores.csv", "w") as file:
            for score in scores:
                file.write(score + "\n") 

        tui.goto("main")
        tui.update()

main_menu = SimpleSelection({
    "Add a new record": lambda ui, s: add_score(ui.get_interface()),
    "View all scores": lambda ui, s: view_all(ui.get_interface()),
    "Search by name": lambda ui, s: search(ui.get_interface()),
    "Quit": lambda ui, s: ui.get_interface().quit_app()
})


interface = InterfaceManager().add_nav().add_ui(main_menu, "main")
interface.goto("main")
interface.update()
interface.main()

