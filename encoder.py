from string import ascii_lowercase

key = list(ascii_lowercase)

key.insert(0, "\0")
key.append(" ")

string = input().lower()

def encode(string, offset=0):
    out = []

    def encode_char(i, string, offset=0):
        current = string[i]
        try:
            previous = out[i - 1]
        except IndexError:
            previous = None

        current_code = key.index(current) + offset
        multiplier = 1

        if previous != None:
            previous_code = key.index(previous)
            
            if previous in list("aeiou"):
                multiplier = -1
        else:
            previous_code = 0

        new_code = current_code + previous_code * multiplier
        new_char = key[new_code % len(key)]
        out.append(new_char)

        if i == len(string) - 1:
            return
        
        encode_char(i + 1, string)

    encode_char(0, string, offset)

    out_str = ""
    for char in out:
        out_str += char

    return out_str

def decode(string, offset=0):
    out = []

    def decode_char(i, string):
        current = string[-(i+1)]
        try:
            previous = string[-(i+2)]
        except IndexError:
            previous = None

        current_code = key.index(current)

        if i == len(string) - 1:
            current_code -= offset

        multiplier = 1

        if previous != None:
            previous_code = key.index(previous)

            if previous in list("aeiou"):
                multiplier = -1
        else:
            previous_code = 0

        new_code = current_code - previous_code * multiplier
        new_char = key[new_code % len(key)]
        out.append(new_char)

        if i == len(string) - 1:
            return
        
        decode_char(i+1, string)

    decode_char(0, string)

    out_str = ""
    for char in out[::-1]:
        out_str += char

    return out_str

opt = input("E/D?")

if opt.lower() == "e":
    print(encode(string, 5))

if opt.lower() == "d":
    print(decode(string, 5))
