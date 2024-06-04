for i in range(100, 201):
    digits = []
    num = i

    while num > 0:
        digit = num % 10
        digits.append(digit)
        num = num // 10

    d_sum = sum(digits)

    #print(f"{i} : {d_sum}")

    if d_sum % 2 == 0:
        print(i)