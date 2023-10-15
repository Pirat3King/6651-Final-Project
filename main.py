from os import system
import hangman.hangman_trevor as hangman
import snake.snake_game as snake
import checkers.checkers as checkers
system('cls')
print("Welcome to the Team Pheonix final project for CSCI 6651-01.")

def main_menu():
    selection = ""
    the_games = ["1", "2", "3"]
    print("Make your selection\n1. Hangman\n2. Snake\n3. Checkers")
    selection = input("> ")
    while selection not in the_games:
        print("Invalid Selection")
        print("Make your selection\n1. Hangman\n2. Snake\n3. Checkers")
        selection = input("> ")
    return int(selection)

game_over = False
while not game_over:
    game = main_menu()

    if game == 1:
        hangman.play_hangman()
    if game == 2:
        snake.play_snake()
    if game == 3:
        checker_game = checkers.Checkers()
        checker_game.run()

    play_again = input("Play again? (y or n): ").upper()
    while play_again != "Y" and play_again != "N":
        print("Ivalid Input.")
        play_again = input("Play again? (y or n): ").upper()
    if play_again == "Y":
        pass
    elif play_again == "N":
        game_over = True

