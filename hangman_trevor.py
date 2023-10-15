import random

def play_hangman():
    myFile = open("hangman_words.txt","r")
    wordList = myFile.read().splitlines()
    chosenWord = random.choice(wordList)
    myFile.close()
    #print(f"Psst, the solution is {chosenWord}")

    display = []
    previousLetters = []
    lives = 0
    endOfGame = False
    hangman = ['''
    +---+
    |   |
        |
        |
        |
        |
    =========''', '''
    +---+
    |   |
    O   |
        |
        |
        |
    =========''', '''
    +---+
    |   |
    O   |
    |   |
        |
        |
    =========''', '''
    +---+
    |   |
    O   |
   /|   |
        |
        |
    =========''', '''
    +---+
    |   |
    O   |
   /|\  |
        |
        |
    =========''', '''
    +---+
    |   |
    O   |
   /|\  |
   /    |
        |
    =========''', '''
    +---+
    |   |
    O   |
   /|\  |
   / \  |
        |
    =========''']

    for letter in chosenWord:
        display.append("_")



    while endOfGame == False:
        print(f"{lives} lives remaining")
        print(f"{hangman[lives]}")
        guess = input("Guess a letter: ").lower()
        for position in range(len(chosenWord)):
            letter = chosenWord[position]
            if letter == guess:
                display[position] = letter
        if guess not in chosenWord:
            if guess in previousLetters:
                print(f"You have already guessed {guess}.")
            else:
                lives += 1
                previousLetters.append(guess)
                if lives >= 6:
                    print(f"{hangman[lives]}")
                    print("Sorry, you lost the game.")
                    print(f"The word was: {chosenWord}")
                    endOfGame = True
        if '_' not in display:
            endOfGame = True
            print("Congratulations! You won the game.")
        print(display)