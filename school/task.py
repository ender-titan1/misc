import os

def get_word(text=None):
    word = input(text if text != None else "Input a 5-letter word: ")

    if len(word) != 5:
        print("Word must be 5 letters")
        return get_word()
    
    return [char for char in word]

def get_char():
    char = input("Guess Letter: ")

    if len(char) != 1:
        print("Input a single letter")
        return get_char()
    
    return char[0]

def main():
    word_list = get_word()
    guesses = 5
    while guesses > 0:
        os.system("clear")
        print(f"You have {guesses}/5 guesses remaining")

        char = get_char()

        if char not in word_list:
            print(f"'{char}' is not in the word!")
        else:
            chars = [i+1 for i, c in enumerate(word_list) if c == char]
            if len(chars) == 1:
                print(f"'{char}' is number {chars[0]} in the word")
            else:
                print(f"'{char}' is number {chars[0]} and number {chars[1]} in the word")

        guess = get_word("Try to guess the word: ")

        if guess == word_list:
            print("YOU GUESSED CORRECTLY!")    
            break
        else:
            print("Incorrect!")

        guesses -= 1
        input("\nInput anything to continue")
    else:
        os.system("clear")
        string = ""
        for char in word_list:
            string += char

        print(f"You failed! The word was {string}")

main()