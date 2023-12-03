"""
Author: Kiren Chaudry and Muhammad Hammad
Date Authored: Oct. 17, 2023
Last Updated: Dec. 03, 2023 by Kiren
Class: CSCI 6651-01
Goal: This is a program to run a simple game of hangman
Updates from Trevor: update_hangman() now includes the gallow itself, reseting the game now resets the hangman drawing properly
    the reset_button places on top of the reset button from main with the same appearance to appear as one button
    but this is still its own button
    guesses are now limited to one char
    also made the bg color for some of the features a different shade of grey so it doesn't blend in with the background
Updates from Kiren 12/3: check that user entered alphabetic character
Check and do not allow repeat guesses
Don't allow negative attempts
Allow user to click 'Enter' to guess

OpenAI's ChatGPT was utilized to assist in the creation of this program
"""

import random
import json
import tkinter as tk

class Hangman:

    def __init__(self, main_tkinter, user_data, username):
        global canvas, attempts_label, letters_guessed_label, letter_label, letter_entry, guess_button, word_label
        global word_display, message_label, max_attempts_label, restart_button #exit_button

        self.user_data = user_data  # Pass user_data to Hangman
        self.username = username # Pass the record just for the current user

        self.window = main_tkinter

        # Initialize variables
        self.word_to_guess = self.choose_random_word()
        self.guessed_letters = []
        self.attempts = 6
        self.current_attempt = 0
        self.max_attempts_message_displayed = False  #tracks if max attempts message is displayed

        # Create a canvas to draw the hangman figure
        canvas = tk.Canvas(self.window, width=200, height=200, bg="#d4cbd1")

        # Create and pack the widgets
        attempts_label = tk.Label(self.window, text=f"Attempts left: {self.attempts - self.current_attempt}", font=("Arial", 14), bg="#BDC3C7")

        letters_guessed_label = tk.Label(self.window, text="Letters Guessed: ", font=("Arial", 14), bg="#BDC3C7")

        letter_label = tk.Label(self.window, text="Guess a letter:", font=("Arial", 14), bg="#BDC3C7")

        self.entry_value = tk.StringVar()
        # Validation function to allow only one character
        self.validate_cmd = self.window.register(self.validate_entry)
        letter_entry = tk.Entry(self.window, textvariable=self.entry_value, validate="key", validatecommand=(self.validate_cmd, '%S', self.entry_value), bg="#d4cbd1")
        # Trace the variable to limit the length of the entry
        self.entry_value.trace_add('write', self.on_entry_change)

        guess_button = tk.Button(self.window, text="Guess", font=("Arial", 12), bg="#5499C7", fg="white" , command=self.guess_letter)
        # Set up binding for the Enter key
        letter_entry.bind("<Return>", self.guess_letter)

        word_display = tk.StringVar()
        word_display.set(" ".join(["_" for _ in self.word_to_guess]))
        word_label = tk.Label(self.window, textvariable=word_display, bg="#d4cbd1")

        message_label = tk.Label(self.window, text="")
        max_attempts_label = tk.Label(self.window, text="")

        restart_button = tk.Button(self.window, text="Reset", font=("Arial", 10), bg="orange", fg="white", command=lambda: self.play_again(user_data))

        # Start the game
        self.update_hangman()

    #function to get hangman wins
    # def hangman_wins(self):
    #     return self.user_data.get("hangman_wins", 0)

    '''
    Validate_entry() and on_entry_changes() are both used to ensure only one char can be entered
    '''

    # Check if the entered character is a single character
    def validate_entry(self, char, entry_value):
        return len(char) == 1

    # Limit the entry length to 1 character
    def on_entry_change(self, *args):
        self.entry_value.set(self.entry_value.get()[:1])

    #function to update hangman wins in the json file
    def update_hangman_wins(self):
        users = self.user_data.get("users", [])

        for user in users:
            if user["username"] == self.username["username"]:
                user["hangman_wins"] += 1
                break
        
        self.user_data["users"] = users
        with open("user_data.json", "w") as file:
            json.dump(self.user_data, file, indent=4)

    # Function to get a random word from wordlist
    def choose_random_word(self):
        #with open('wordlist.txt', 'r') as file:
        #    words = file.read().splitlines()
        #selected_word = random.choice(words)
        selected_word = 'lamp'
        print(f"The selected word is: {selected_word}")
        return selected_word

    # Function to update the hangman figure
    def update_hangman(self):
        if self.current_attempt == 0:  # gallow
            canvas.create_line(10, 180, 90, 180, tags="hangmang_lines")
            canvas.create_line(50, 180, 50, 10, tags="hangmang_lines")
            canvas.create_line(50, 10, 100, 10, tags="hangmang_lines")
            canvas.create_line(100, 10, 100, 30, tags="hangmang_lines")
        elif self.current_attempt == 1:    #head
            canvas.create_oval(85, 30, 115, 60, tags="hangmang_lines")
        elif self.current_attempt == 2:  #body
            canvas.create_line(100, 60, 100, 120, tags="hangmang_lines")
        elif self.current_attempt == 3:  # left arm
            canvas.create_line(100, 80, 80, 60, tags="hangmang_lines")
        elif self.current_attempt == 4:  # right arm
            canvas.create_line(100, 80, 120, 60, tags="hangmang_lines")
        elif self.current_attempt == 5:  # left leg
            canvas.create_line(100, 120, 80, 140, tags="hangmang_lines")
        elif self.current_attempt == 6:  # right leg
            canvas.create_line(100, 120, 120, 140, tags="hangmang_lines")
            # X's inside the circle for dead eyes
            canvas.create_text(95, 40, text="x", tags="hangmang_lines")
            canvas.create_text(105, 40, text="x", tags="hangmang_lines")

    # Function to check if the game is won
    def is_game_won(self):
        return all(letter in self.guessed_letters for letter in self.word_to_guess)

    # Function to handle letter guesses
    def guess_letter(self, event=None):
        if self.current_attempt >= self.attempts:
            # No more attempts left, don't process further guesses
            # Add a new label for the "max attempts reached" message
            max_attempts_label.config(text="Maximum attempts reached. Game over!", font=("Arial", 14), bg="#BDC3C7")
            self.max_attempts_message_displayed = True  # Set the flag to indicate the message has been displayed
            return
        elif self.is_game_won():
            max_attempts_label.config(text="You already won. Game over!", font=("Arial", 14), bg="#BDC3C7")
            self.max_attempts_message_displayed = True  # Set the flag to indicate the message has been displayed
            return

        letter = letter_entry.get().lower()

        # check that user entered an alphabetic character
        if not letter.isalpha():  # if user did not enter a letter
            message_label.config(text="Please enter a valid alphabetical character.")
            return

        # check if user already guessed the letter
        if letter in self.guessed_letters:  # if user already guessed the letter
            message_label.config(text="You already guessed this letter. Try a different one.")
            return

        self.guessed_letters.append(letter)
        letter_entry.delete(0, tk.END)

        if letter not in self.word_to_guess:
            self.current_attempt += 1
            self.update_hangman()

        word_display.set(" ".join([char if char in self.guessed_letters else "_" for char in self.word_to_guess]))

        # Update attempts label
        attempts_left = max(0, self.attempts - self.current_attempt)  # make sure user cannot have negative attempts
        attempts_label.config(text=f"Attempts left: {attempts_left}")

        # Update letters guessed label
        letters_guessed_label.config(text=f"Letters Guessed: {' '.join(self.guessed_letters)}")

        if self.is_game_won():
            message_label.config(text="Congratulations! You've won!")
            self.update_hangman_wins()  # Call the method to update wins
        elif self.current_attempt == self.attempts and not self.max_attempts_message_displayed:
            message_label.config(text=f"Game over! The word was '{self.word_to_guess}'")
            self.max_attempts_message_displayed = True
        else:
            message_label.config(text="")  # Clear the message label for the next guess

    # Function to play again
    def play_again(self, user_data):
        self.reset_game()
        unpack_hangman_elements()
        # hangman_game = Hangman(self.window, user_data)
        pack_hangman_elements()

    # Function to exit the game
    # def exit_game(self):
    #     self.window.destroy()

    # Function to reset the game state
    def reset_game(self):
        canvas.delete("hangmang_lines")
        self.word_to_guess = self.choose_random_word()
        self.guessed_letters = []
        self.attempts = 6
        self.current_attempt = 0
        self.update_hangman()
        word_display.set(" ".join(["_" for _ in self.word_to_guess]))
        attempts_label.config(text=f"Attempts left: {self.attempts}")
        letters_guessed_label.config(text="Letters Guessed: ")
        message_label.config(text="")
        max_attempts_label.config(text="")

    # Run the main loop
    def run(self):
        self.window.mainloop()

# Call the Hangman class to start the game
#hangman_game = Hangman()
#hangman_game.run()

def pack_hangman_elements():
    canvas.pack()
    attempts_label.pack()
    letters_guessed_label.pack()
    letter_label.pack()
    letter_entry.pack()
    guess_button.pack()
    word_label.pack()
    message_label.pack()
    max_attempts_label.pack()
    restart_button.place(relx=0.95, rely=0.10, anchor=tk.NE)

def unpack_hangman_elements():
    canvas.pack_forget()
    attempts_label.pack_forget()
    letters_guessed_label.pack_forget()
    letter_label.pack_forget()
    letter_entry.pack_forget()
    guess_button.pack_forget()
    word_label.pack_forget()
    message_label.pack_forget()
    max_attempts_label.pack_forget()
    restart_button.place_forget()
