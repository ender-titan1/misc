from enum import Enum
import random

class Pick(Enum):
    ROCK = 0
    PAPER = 1
    SCISORS = 2
    LIZARD = 3
    SPOCK = 4

result_matrix = [
    "DLWWL",
    "WDLLW",
    "LWDWL",
    "LWLDW",
    "WLWLD"
]

theirs = Pick(random.randint(0, 4))

def get_player_pick():
    pick = None
    while True:
        string = input("Pick:  ")
        try:
            pick = Pick[string.upper()]
        except KeyError:
            continue
        else:
            break

    return pick

for _ in range(0, 10):
    yours = get_player_pick()
    theirs = Pick(random.randint(0, 4))

    print(f"{yours.name.lower()} vs {theirs.name.lower()}")
    result_char = list(result_matrix[theirs.value])[yours.value]

    if result_char == 'W':
        print("You win!")
    elif result_char == 'D':
        print("Draw!")
    else:
        print("You loose!")