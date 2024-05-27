import random
import os
from enum import Enum
from getch import getch

class Item(Enum):
    YOGURT = 1
    CORNFLAKES = 2
    MILK = 3

stock = {
    Item.YOGURT:      [30000, 0, "20-05-2024", 1.99],
    Item.CORNFLAKES:  [20000, 0, "25-05-2024", 5.49],
    Item.MILK:        [10000, 0, "31-05-2024", 2.99]
}

sales_0 = {
    Item.YOGURT:     [20,  40, 50, 60, 10, 20,  80],
    Item.CORNFLAKES: [50, 100, 10, 20, 50, 90, 100],
    Item.MILK:       [20, 500, 80, 10, 80, 10,  70]
}

sales_1 = {
    Item.YOGURT:     [30,  40, 50, 60, 10, 20,  80],
    Item.CORNFLAKES: [50, 200, 10, 20, 90, 90, 100],
    Item.MILK:       [20, 500, 80, 10, 80, 10,  70]
}

sales_2 = {
    Item.YOGURT:     [20,  40, 50, 60, 10, 20, 100],
    Item.CORNFLAKES: [50, 100, 10, 20, 50, 90, 100],
    Item.MILK:       [20, 500, 80, 10, 80, 10,  70]
}

sales_3 = {
    Item.YOGURT:     [20,  40, 50, 60, 10, 0, 0],
    Item.CORNFLAKES: [50, 100, 10, 20, 50, 0, 0],
    Item.MILK:       [20, 500, 80, 10, 80, 0, 0]
}

sales = [
    sales_0,
    sales_1,
    sales_2,
    sales_3
]

CURRENT_DAY = (3, 3) # Week 3, Thursday

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

    for week in sales:
        for commodity in Item:
            stock[commodity][1] += sum(week[commodity])

    while True:
        (opt, _) = selection(["Buy 10", "See Stock", "Check Expiration", "See profit", "Quit"])

        if opt == 0:
            buy_item()

        if opt == 1:
            see_stock()

        if opt == 2:
            check_expired()

        if opt == 3:
            profit()

        if opt == 4:
            return

def buy_item():
    arr = [f"Buy {str(key).split('.')[1].lower()}" for key in stock.keys()]
    arr.append("Return")

    (_, opt) = selection(arr)

    if opt == "Return":
        return

    commodity = Item[opt.split(" ")[1].upper()]
    commodity_data = stock[commodity]
    price = commodity_data[3]

    (week, day) = CURRENT_DAY
    sales[week][commodity][day] += 10
    stock[commodity][1] += 10 

    print()
    print(f"${price * 10} withdrawn from account.")
    print("Press any key to continue...")

    getch()

def see_stock():
    os.system("clear")
    for commodity in Item:
        print(f"{str(commodity).split('.')[1].lower().ljust(15, ' ')}", end="")
        data = stock[commodity]
        print(f": {str(data[0] - data[1]).rjust(5, ' ')} remaining | expires {data[2]}")

    print()
    print("Press any key to continue...")

    getch()

def check_expired():
    os.system("clear")

    something_expired = False
    for commodity in Item:
        current_date = CURRENT_DAY[0] * 7 + CURRENT_DAY[1] - 2
        expired_date = int(stock[commodity][2].split("-")[0])

        if current_date > expired_date:
            print(f"{str(commodity).split('.')[1].lower()}", end="")
            print(" expired!")
            something_expired = True

    if not something_expired:
        print("Nothing expired!")

    print()
    print("Press any key to continue...")

    getch()

def profit():
    os.system("clear")
    total = 0 
    for commodity in Item:
        p = stock[commodity][1] * stock[commodity][3]

        print(f"{str(commodity).split('.')[1].lower().ljust(15, ' ')}", end="")
        print(f"| ${p} of profit")

        total += p

    print(f"\nTotal{' ' * 10}| ${total}")


    print()
    print("Press any key to continue...")

    getch()

prices()