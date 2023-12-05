"""
Author: Kiren Chaudry and Muhammad Hammad
Date Authored: Oct. 17, 2023
Last Updated: Dec. 05, 2023 by Kiren
Class: CSCI 6651-01
Goal: This is a program to run a simple game of hangman
Sources:
OpenAI's ChatGPT was utilized to assist in the creation of this program
Words classified by difficultry from: https://github.com/LoraineYoko/word_difficulty/blob/master/README.md
Zhang, S., Jia, Q., Shen, L., Zhao, Y. (2020). Automatic Classification and Comparison of Words by Difficulty.
In: Yang, H., Pasupa, K., Leung, A.CS., Kwok, J.T., Chan, J.H., King, I. (eds) Neural Information Processing.
ICONIP 2020. Communications in Computer and Information Science, vol 1332. Springer, Cham.
https://doi.org/10.1007/978-3-030-63820-7_72
"""

"""
Updates from Trevor: update_hangman() now includes the gallow itself, reseting the game now resets the hangman drawing properly
    the reset_button places on top of the reset button from main with the same appearance to appear as one button
    but this is still its own button
    guesses are now limited to one char
    also made the bg color for some of the features a different shade of grey so it doesn't blend in with the background
Updates from Kiren 12/3: check that user entered alphabetic character
                        Check and do not allow repeat guesses
                        Don't allow negative attempts
                        Allow user to click 'Enter' to guess
Updates from Kiren 12/4-12/5: Refactored code to make it more modular
                        Updated program to take hangman_canvas from main
                        Updated colors and graphics
                        Added easy, medium, difficult words
"""

import random
import json
import tkinter as tk

WIDTH, HEIGHT = 400, 400
GRID_SIZE = 20

class Hangman:

    def __init__(self, main_tkinter, canvas_window, user_data, username):
        self.root = main_tkinter

        #Initialize hangman canvas
        self.canvas = canvas_window
        self.root.geometry(f"900x700")
        #root.state('zoomed')
        #self.root.geometry(f"{WIDTH}x{HEIGHT}")

        self.user_data = user_data  # Pass user_data to Hangman
        self.username = username  # Pass the record just for the current user

        self.word_to_guess = ""
        self.guessed_letters = []
        self.attempts = 6
        self.current_attempt = 0
        self.max_attempts_message_displayed = False
        self.word_display = tk.StringVar()

        self.create_widgets()
        self.set_difficulty()
    def create_widgets(self):
        self.create_labels()
        self.create_entry_and_button()

        # Initially, make labels and entry invisible
        self.attempts_label.place_forget()
        self.letters_guessed_label.place_forget()
        self.message_label.place_forget()
        self.max_attempts_label.place_forget()
        self.letter_entry.place_forget()
        self.guess_button.place_forget()
        self.word_label.place_forget()

        # Set up binding for the Enter key
        self.letter_entry.bind("<Return>", self.guess_letter)

    def create_labels(self):
        self.word_label = tk.Label(self.canvas, textvariable=self.word_display, bg="#FAF5BA")
        self.attempts_label = tk.Label(self.canvas, text="", font=("Arial", 14), bg="#FAF5BA")
        self.letters_guessed_label = tk.Label(self.canvas, text="", font=("Arial", 14), bg="#FAF5BA")
        self.max_attempts_label = tk.Label(self.canvas, text="", bg="#FAF5BA")
        self.message_label = tk.Label(self.canvas, text="", font=("Arial", 14), bg="#FAF5BA")

        self.word_label.place(relx=0.1, rely=0.50)
        self.attempts_label.place(relx=0.1, rely=0.70)
        self.letters_guessed_label.place(relx=0.1, rely=0.80)
        self.message_label.place(relx=0.1, rely=0.90)
        self.max_attempts_label.place(relx=0.1, rely=1.0)
    def create_entry_and_button(self):
        self.entry_value = tk.StringVar()
        self.letter_entry = tk.Entry(self.canvas, textvariable=self.entry_value, validate="key")
        # Trace the variable to limit the length of the entry
        self.entry_value.trace_add('write', self.on_entry_change)
        self.letter_entry.place(relx=0.1, rely=0.60)

        self.guess_button = tk.Button(self.canvas, text="Guess", command=self.guess_letter)
        self.guess_button.place(relx=0.42, rely=0.59)

    def set_difficulty(self):
        self.difficulty_label = tk.Label(self.canvas, text="Choose Difficulty Level:", font="Arial, 12", bg="#FAF5BA")
        self.easy_button = tk.Button(self.canvas, text="Easy", bg="#FAE070", command=lambda: self.start_game('easy'))
        self.medium_button = tk.Button(self.canvas, text="Medium", bg="#F18D32", command=lambda: self.start_game('medium'))
        self.hard_button = tk.Button(self.canvas, text="Hard", bg="#DE4923", command=lambda: self.start_game('hard'))

        self.difficulty_label.place(relx=0.32, rely=0.3)
        self.easy_button.place(relx=0.45, rely=0.38)
        self.medium_button.place(relx=0.43, rely=0.46)
        self.hard_button.place(relx=0.45, rely=0.54)

    def start_game(self, difficulty):
        # Destroy the buttons
        self.difficulty_label.destroy()
        self.easy_button.destroy()
        self.medium_button.destroy()
        self.hard_button.destroy()

        # Make labels and entry visible
        self.word_label.place(relx=0.4, rely=0.47)
        self.attempts_label.place(relx=0.05, rely=0.61)
        self.letters_guessed_label.place(relx=0.05, rely=0.70)
        self.message_label.place(relx=0.05, rely=0.79)
        self.max_attempts_label.place(relx=0.05, rely=.88)
        self.letter_entry.place(relx=0.3, rely=0.53)
        self.guess_button.place(relx=0.62, rely=0.52)

        # Update labels and start the game
        self.attempts_label.config(text=f"Attempts left: {self.attempts}")
        self.letters_guessed_label.config(text="Letters Guessed:")
        self.message_label.config(text="")

        self.difficulty = difficulty
        self.word_to_guess = self.choose_random_word(self.difficulty)

        # Set up initial display of underscores in word_display
        self.word_display.set(" ".join(["_" for _ in self.word_to_guess]))

        # Start the game
        self.update_hangman()

    def choose_random_word(self, difficulty):
        file_path = ''
        if difficulty == 'easy':
            file_path = 'easy_words.txt'
        elif difficulty == 'medium':
            file_path = 'medium_words.txt'
        elif difficulty == 'hard':
            file_path = 'hard_words.txt'
        with open(file_path, 'r') as file:
            words = file.read().splitlines()
        selected_word = random.choice(words)
        # print(f"The selected word is: {selected_word}")
        return selected_word

    def update_hangman_wins(self):
        users = self.user_data.get("users", [])

        for user in users:
            if user["username"] == self.username["username"]:
                user["hangman_wins"] += 1
                break

        self.user_data["users"] = users
        with open("user_data.json", "w") as file:
            json.dump(self.user_data, file, indent=4)

    # Check if the entered character is a single character
    def validate_entry(self, char, entry_value):
        return len(char) == 1

    # Limit the entry length to 1 character
    def on_entry_change(self, *args):
        self.entry_value.set(self.entry_value.get()[:1])

    # Function to check if the game is won
    def is_game_won(self):
        return all(letter in self.guessed_letters for letter in self.word_to_guess)

    # Function to handle letter guesses
    def guess_letter(self, event=None):
        if self.current_attempt >= self.attempts:
            # No more attempts left, don't process further guesses
            # Add a new label for the "max attempts reached" message
            self.max_attempts_label.config(text="Maximum attempts reached. Game over!", font=("Arial", 14), bg="#D36B2E")
            self.max_attempts_message_displayed = True  # Set the flag to indicate the message has been displayed
            return
        elif self.is_game_won():
            self.max_attempts_label.config(text="You already won. Game over!", font=("Arial", 14), bg="#D36B2E",)
            self.max_attempts_message_displayed = True  # Set the flag to indicate the message has been displayed
            return

        letter = self.letter_entry.get().lower()

        # check that user entered an alphabetic character
        if not letter.isalpha():  # if user did not enter a letter
            self.message_label.config(text="Please enter a valid alphabetical character.", bg="#D36B2E", fg="#FFFFFF")
            return

        # check if user already guessed the letter
        if letter in self.guessed_letters:  # if user already guessed the letter
            self.message_label.config(text="You already guessed this letter. Try a different one.", font=("Arial", 12), bg="#D36B2E", fg="#FFFFFF")
            return

        self.guessed_letters.append(letter)
        self.letter_entry.delete(0, tk.END)

        if letter not in self.word_to_guess:
            self.current_attempt += 1
            self.update_hangman()

        self.word_display.set(" ".join([char if char in self.guessed_letters else "_" for char in self.word_to_guess]))

        # Update attempts label
        attempts_left = max(0, self.attempts - self.current_attempt)  # make sure user cannot have negative attempts
        self.attempts_label.config(text=f"Attempts left: {attempts_left}")

        # Update letters guessed label
        self.letters_guessed_label.config(text=f"Letters Guessed: {' '.join(self.guessed_letters)}")

        if self.is_game_won():
            self.message_label.config(text="Congratulations! You've won!", font=("Arial", 14), bg="#F8B802", fg="#000000")
            self.update_hangman_wins()  # Call the method to update wins
        elif self.current_attempt == self.attempts:
            self.message_label.config(text=f"Game over! The word was '{self.word_to_guess}'", font=("Arial", 14), bg="#E7131B", fg="#FFFFFF")
        else:
            self.message_label.config(text="", bg="#FAF5BA")  # Clear the message label for the next guess

    def update_hangman(self):
        if self.current_attempt == 0:  # gallow
            self.canvas.create_line(120, 180, 200, 180, tags="hangmang_lines")
            self.canvas.create_line(160, 180, 160, 10, tags="hangmang_lines")
            self.canvas.create_line(160, 10, 210, 10, tags="hangmang_lines")
            self.canvas.create_line(210, 10, 210, 30, tags="hangmang_lines")
        elif self.current_attempt == 1:  # head
            self.canvas.create_oval(195, 30, 225, 60, tags="hangmang_lines")
        elif self.current_attempt == 2:  # body
            self.canvas.create_line(210, 60, 210, 120, tags="hangmang_lines")
        elif self.current_attempt == 3:  # left arm
            self.canvas.create_line(210, 80, 190, 60, tags="hangmang_lines")
        elif self.current_attempt == 4:  # right arm
            self.canvas.create_line(210, 80, 230, 60, tags="hangmang_lines")
        elif self.current_attempt == 5:  # left leg
            self.canvas.create_line(210, 120, 190, 140, tags="hangmang_lines")
        elif self.current_attempt == 6:  # right leg
            self.canvas.create_line(210, 120, 230, 140, tags="hangmang_lines")
            # X's inside the circle for dead eyes
            self.canvas.create_text(205, 40, text="x", tags="hangmang_lines")
            self.canvas.create_text(215, 40, text="x", tags="hangmang_lines")

    # Function to play again
    def play_again(self, user_data):
        self.reset_game()

    def reset_game(self):
        # Reset all game-related variables to their initial state
        self.canvas.delete("hangmang_lines")
        self.word_to_guess = ""
        self.guessed_letters = []
        self.attempts = 6
        self.current_attempt = 0
        self.max_attempts_message_displayed = False

        # Reset labels and entry
        self.word_display.set("")  # Clear the displayed word
        self.attempts_label.config(text="")
        self.letters_guessed_label.config(text="")
        self.message_label.config(text="", bg="#FAF5BA", fg="#FFFFFF")
        self.max_attempts_label.config(text="", bg="#FAF5BA")
        self.letter_entry.delete(0, tk.END)

        # Hide unnecessary widgets
        self.word_label.place_forget()
        self.attempts_label.place_forget()
        self.letters_guessed_label.place_forget()
        self.message_label.place_forget()
        self.max_attempts_label.place_forget()
        self.letter_entry.place_forget()
        self.guess_button.place_forget()

        # Show difficulty selection again
        self.set_difficulty()

# Uncomment to run outside of main application
# The text files will also need to be in the hangman folder
# if __name__ == "__main__":
#     root = tk.Tk()
#     canvas = tk.Canvas(root, width=400, height=400, bg="#FAF5BA")
#     canvas.pack()
#     hangman_game = Hangman(root, canvas, user_data=None, username='kiren')
#     root.mainloop()

