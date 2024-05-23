import random
import os
from getch import getch

STOCK = {
    "Yogurt": (30000, "20-05-2024"),
    "Cornflakes": (20000, "25-05-2024"),
    "Milk": (10000, "31-05-2024")
}

def print_stars(amount):
    for i in range(amount):
        print("*", end="")

    print("")

def pyramid():
    pyramid_height = 5
    pyramid_size = 2 * pyramid_height - 1

    for i in range(pyramid_size):
        idx = i + 1
        minus = idx - pyramid_height
        
        if minus > 0:
            print_stars(idx - (minus * 2))
        else:
            print_stars(idx)

def mult(max_factor=5):
    max_res = max_factor * max_factor
    cell_size = len(str(max_res)) + 1
    table_size = 1 + ((cell_size + 1) * max_factor)

    def print_line(multiplier=1):
        print("|", end="")
        for i in range(1, max_factor + 1):
            print(str(i*multiplier).rjust(cell_size, " "), end="|")

        print("")

        if multiplier == 1:
            print("-" * table_size)

    for i in range(1, max_factor + 1):
        print_line(i)

def game():

    os.system("clear")

    ops = {
        1: ["+", "-"],
        3: ["*"],
        5: ["//"]
    }

    def question(level, questions_left, total_questions, lives):
        print(f"Level: {level} | {questions_left}/{total_questions} | {'❤' * lives}")
        print("-" * 30)

        vaild_ops = []
        for lv, op in ops.items():
            if level >= lv:
                vaild_ops.extend(op)

        op = random.choice(vaild_ops)

        left = random.randint(1, 10 * level)
        right = random.randint(1, 10 * level)

        query = f"{left} {op} {right}"
        answer = eval(query)

        user_answer = int(input(f"{query}\n"))
        
        os.system("clear")

        return user_answer == answer

    lives = 5

    for level in range(10):
        questions = level * 2
        for q in range(questions): 
            if not question(level, q, questions, lives):
                lives -= 1

                if lives <= 0:
                    return

def selection(opts):
    i = 0
    while True:
        os.system("clear")

        for idx, opt in enumerate(opts):
            if idx == i:
                print(f"{opt.ljust(20, ' ')} <")
            else:
                print(opt.ljust(20, ' '))

        chr = getch()

        
        if chr == 'w':
            i -= 1
        if chr == "s":
            i += 1

        if i < 0:
            i = 0
        if i >= len(opts):
            i = len(opts) - 1

        if ord(chr) == 13:
            break
    
    return (i, opts[i])
    
def prices():
    (opt, _) = selection(["Buy Item", "See Stock", "Check Expiration", "Quit"])

    if opt == 3:
        return

prices()