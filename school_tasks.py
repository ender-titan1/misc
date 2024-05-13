def rect_area():
    a = int(input("Input witdh: "))
    b = int(input("Input lenght: "))

    return a * b

def grades():
    grade = int(input("Input Grade: "))

    grades = {
        "Excelent": 80,
        "Very Good": 70,
        "Fairly Good": 60,
        "Average": 50,
        "Weak": 20,
        "Poor": 0
    }

    for r, g in grades.items():
        if grade >= g:
            print(r)
            break

def numbers():
    digits = {
        1: "one",
        2: "two",
        3: "three",
        4: "four",
        5: "five",
        6: "six",
        7: "seven",
        8: "eight",
        9: "nine",
        0: "zero"
    }

    tens = {
        2: "twenty",
        3: "thirty",
        4: "forty",
        5: "fifty",
        6: "sixty",
        7: "seventy",
        8: "eighty",
        9: "ninety"
    }

    number = input("Input number: ")
    if len(number) == 1:
        print(digits[int(number)])
        return

    a = list(number)[0]
    b = list(number)[1]

    if a == "1":
        if b == "0":
            print("ten")
        elif b == "1":
            print("eleven")
        elif b == "2":
            print("twelve")
        elif b == "3":
            print("thirteen")
        elif b == "5":
            print("fifteen")
        else:
            print(f"{digits[int(b)]}teen")
        
        return

    digits[0] = ""
    separator = "-" if b != "0" else ""
    print(f"{tens[int(a)]}{separator}{digits[int(b)]}")


if __name__ == "__main__":
    numbers()