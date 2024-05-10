def rect_area():
    a = int(input("Input witdh: "))
    b = int(input("Input lenght: "))

    return a * b

def grades():
    grade = int(input("Input your grade:  "))

    if grade >= 50:
        print("No retake required")
    else:
        retake = int(input("Input retake grade:  "))

        final = 0.75 * retake + 0.25 * grade

        print(final)

if __name__ == "__main__":
    grades()