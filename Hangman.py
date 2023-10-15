# Maddy version of hangman

import random

def welcome_message():
    print("Welcome to Hangman. Good luck!")

def print_guesses_left(guesses_left):
    print(f"\nYou have {guesses_left} incorrect guesses left.")

def print_used_letters(used_letters):
    print("\nYou've used the following letters:\n" + used_letters)

def print_word_so_far(word_so_far):
    print("\nSo far, the word is:\n" + word_so_far)
    print("\t\t******\n\n")

def get_user_guess(used_letters):
    while True:
        user_input = input("Enter your guess: ").upper()

        if len(user_input) == 1 and user_input.isalpha():
            guess = user_input
            if validate_user_guess(guess, used_letters):
                break
        else:
            print("Invalid input! Please enter a single alphabet.")

    return guess

def validate_user_guess(guess, used_letters):
    if not guess.isalpha():
        print("Invalid input. Please enter an alphabet.")
        return False
    elif is_guess_already_used(guess, used_letters):
        print(f"You have already guessed {guess}. Please enter a new letter.")
        return False
    return True

def is_guess_already_used(guess, used_letters):
    return guess in used_letters

def is_guess_in_word(guess, word):
    return guess in word

def update_word_so_far(guess, word, word_so_far):
    for i in range(len(word)):
        if word[i] == guess:
            word_so_far = word_so_far[:i] + guess + word_so_far[i+1:]
    return word_so_far

def get_difficulty_level():
    while True:
        try:
            level = int(input("Choose a difficulty level (1-3):\n1. Easy\n2. Medium\n3. Hard\nEnter your choice: "))
            if 1 <= level <= 3:
                break
            else:
                print("Invalid choice. Please enter a number between 1 and 3.")
        except ValueError:
            print("Invalid choice. Please enter a number between 1 and 3.")

    return level

def main():
    easy_words = ["GUESS", "HANGMAN", "EASY"]
    medium_words = ["HELLO", "WORLD", "COMPUTER"]
    hard_words = ["SYZYGY", "MNEMONIC", "CRYPTOGRAPHY"]

    while True:
        level = get_difficulty_level()
        if level == 1:
            words = easy_words
            max_wrong = 5
        elif level == 2:
            words = medium_words
            max_wrong = 6
        else:
            words = hard_words
            max_wrong = 4

        random.shuffle(words)
        the_word = words[0]
        wrong = 0
        so_far = "-" * len(the_word)
        used = ""

        welcome_message()

        while wrong < max_wrong and so_far != the_word:
            print_guesses_left(max_wrong - wrong)
            print_used_letters(used)
            print_word_so_far(so_far)

            guess = get_user_guess(used)

            while not validate_user_guess(guess, used):
                guess = get_user_guess(used)

            used += guess

            if is_guess_in_word(guess, the_word):
                print(f"That's right! {guess} is in the word.")
                so_far = update_word_so_far(guess, the_word, so_far)
            else:
                print(f"Sorry, {guess} isn't in the word.")
                wrong += 1

        if wrong == max_wrong:
            print("\nYou've been hanged!")
        else:
            print("\nYou guessed it!")

        print(f"The word was {the_word}")

        play_again = input("Do you want to play the game again (Y/N)? ").upper()
        if play_again != "Y":
            break

if __name__ == "__main__":
    main()
1