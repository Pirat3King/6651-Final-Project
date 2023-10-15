from os import system
from tkinter import *
import random
#use tkinter frame
system('cls')

def hangman_was_clicked():
    my_file = open("hangman_words.txt","r")
    word_list = my_file.read().splitlines()
    chosen_word = random.choice(word_list)
    my_file.close()
    display = []
    for _ in chosen_word:
        display.append('_')


    my_canvas.create_line(400,300,400,50,fill="yellow",width=2)
    my_canvas.create_line(400,50,300,50,fill="yellow",width=2)
    my_canvas.create_line(300,50,300,75,fill="yellow",width=2)
    my_canvas.create_oval(325,125,275,75,fill="yellow",width=2)
    my_canvas.create_line(300,125,300,220,fill="yellow",width=2)
    my_canvas.create_line(300,130,350,175,fill="yellow",width=2)
    my_canvas.create_line(300,130,250,175,fill="yellow",width=2)
    my_canvas.create_line(300,220,250,260,fill="yellow",width=2)
    my_canvas.create_line(300,220,350,260,fill="yellow",width=2)

    word_display = Label(my_canvas, text=display, fg='yellow', bg='black')
    word_display.pack()
    instruction = Label(my_canvas, text='guess a letter', fg='yellow', bg='black')
    instruction.pack()
    my_canvas.create_window(100, 100, window=word_display)
    my_canvas.create_window(100, 130, window=instruction)
    

game_window = Tk()
game_window.title("CSCI 6651-01 | Team Pheonix Final Project")
game_window.geometry("900x700")

hman_button = Button(game_window, text="Play Hangman", command=hangman_was_clicked)
hman_button.place(x=100, y=600)

snake_button = Button(game_window, text="Play Snake")
snake_button.place(x=400, y=600)

check_button = Button(game_window, text="Play Checkers")
check_button.place(x=700, y=600)

my_canvas = Canvas(game_window, height=500, width=600, bg="black")
my_canvas.pack(pady=50)











game_window.mainloop()