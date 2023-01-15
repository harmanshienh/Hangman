import requests
import sys

wrong_guess = 0
guesses = []
char_in_word = False
valid_second_guess = True
num_invalid_checks = 0

#Hangman iterations to display whenever a wrong guess is inputted
hangman = ["""      _______
     |/      |
     |      
     |      
     |       
     |      
     |
  ___|___""",
"""      _______
     |/      |
     |      (_)
     |      
     |       
     |      
     |
  ___|___ """,
"""      _______
     |/      |
     |      (_)
     |       |
     |       
     |      
     |
  ___|___ """,
"""      _______
     |/      |
     |      (_)
     |      \|            
     |      
     |
     |
  ___|___ """,
"""      _______
     |/      |
     |      (_)
     |      \|/
     |       
     |      
     |
  ___|___ """,
"""      _______
     |/      |
     |      (_)
     |      \|/
     |       |
     |      
     |
  ___|___ """,
 """      _______
     |/      |
     |      (_)
     |      \|/
     |       |
     |      / 
     |
  ___|___""",
"""      _______
     |/      |
     |      (_)
     |      \|/
     |       |
     |      / \\
     |
  ___|___"""]

#Initial message displayed to user
print("HANGMAN\n--------------------\nA random word will be generated and you can either guess character by character, or guess the word at any point!\n")
print("When you're guessing the word, please enter a real word and make sure it is the correct length.")
print("If you guess a word and it fails a check, you must enter an appropriate word before you can enter a character")
print("If you guess a character and it fails a check, you must enter an appropriate character before you can enter a word\n")
print("You have 7 chances, good luck!\n")

#While loop to verify that correct word is in dictionary and can be guessed
while True:
    
    word = requests.get("https://random-word-api.herokuapp.com/word").json()
    
    correct_word = word[0]
    
    dictionary = requests.get("https://api.dictionaryapi.dev/api/v2/entries/en/" + correct_word).status_code
    
    if dictionary == 200:
        break
    
    elif dictionary == 404:
        continue

print(hangman[0])

blank_word = ["_"] * len(correct_word)

print("")
print("")
print("")
print(" ".join(blank_word))

while wrong_guess < 7:
    
    valid_second_guess = True
    
    guess = str(input("\nGuess a character/word: ")).lower()
    
    #Character cannot be entered until an appropriate word is entered
    if len(guess) > 1:
        dictionary = requests.get("https://api.dictionaryapi.dev/api/v2/entries/en/" + guess).status_code

        while len(guess) != len(correct_word) or dictionary != 200 or guess in guesses:

            num_invalid_checks = 0
          
            if len(guess) != len(correct_word):
                num_invalid_checks += 1
                sys.stdout.write("\x1b[2K")
                print(f"Previous word '{guess}' not the correct length!")
            
            if dictionary != 200:
                num_invalid_checks += 1
                sys.stdout.write("\x1b[2K")
                print(f"Previous word '{guess}' not in dictionary!")
           
            if guess in guesses:
                num_invalid_checks += 1
                sys.stdout.write("\x1b[2K")
                print("Enter a new word you have not guessed already!")
            
            #Clearing the original input line so the new one replaces it
            for i in range(1 + num_invalid_checks):
                sys.stdout.write("\x1b[1A")
            sys.stdout.write("\x1b[2K")

            guess = str(input("Please enter a word: ")).lower()

            dictionary = requests.get("https://api.dictionaryapi.dev/api/v2/entries/en/" + guess).status_code
            
            #Clear all error messages for the next guess
            for i in range(num_invalid_checks):
                sys.stdout.write("\x1b[2K\x1b[1B")
        
            #Return cursor to original position
            for i in range(num_invalid_checks):
                sys.stdout.write("\x1b[1A")

        #Clear all error messages for the next guess  
        for i in range(num_invalid_checks):
            sys.stdout.write("\x1b[1B\x1b[2K")
        
        #Return cursor to original position
        for i in range(num_invalid_checks):
            sys.stdout.write("\x1b[1A")    
                
        if guess == correct_word:
            break
        
        elif guess != correct_word:
            
            wrong_guess += 1
            
            guesses.append(guess)
            
            #Clearing previous console output so the new output replaces the old one
            for i in range(14):
                sys.stdout.write("\x1b[1A\x1b[2K")
            
            print(hangman[wrong_guess])
            print("Incorrect!\n")
            print(" ".join(blank_word))
            print("Guesses: " + str(", ".join(guesses[:])))

    elif len(guess) == 1:
        
        while guess.isalpha() != True or guess in guesses or len(guess) != 1:
            
            valid_second_guess = False
            
            if guess.isalpha() != True or len(guess) != 1:
                print(f"Previous guess '{guess}' was not an appropriate character!")
                
                #Clearing the original input line
                for i in range(3):
                    sys.stdout.write("\x1b[1A")
                sys.stdout.write("\x1b[2K")
                
            if guess in guesses:
                print("Enter a new character you have not guessed already!")
                
                #Clearing the original input line
                for i in range(3):
                    sys.stdout.write("\x1b[1A")
                sys.stdout.write("\x1b[2K")
            
            guess = str(input("\nPlease enter a character: ")).lower()
            
            #Clear input line 
            for i in range(2):
                sys.stdout.write("\x1b[1A\x1b[2K")
            
            #Clear invalid input message        
            if not valid_second_guess:
                print("\n")
                sys.stdout.write("\x1b[2K")
            
        for i in range(len(correct_word)):
            if correct_word[i] == guess:
                
                char_in_word = True
                
                #For each instance of the letter, the corresponding blank will be replaced
                #Blank word is stored in a list so the spaces in between letters are not involved
                blank_word[i] = correct_word[i]
        
        if char_in_word == True:    
            
            guesses.append(guess)
            
            #Clearing previous console output so the new output replaces the old one
            for i in range(14):
                sys.stdout.write("\x1b[1A\x1b[2K")
            
            print(hangman[wrong_guess])    
            print("Correct!\n")
            print(" ".join(blank_word))
            print("Guesses: " + str(", ".join(guesses[:])))

        if char_in_word == False:

            wrong_guess += 1

            guesses.append(guess)

            #Clearing previous console output so the new output replaces the old one
            for i in range(14):
                sys.stdout.write("\x1b[1A\x1b[2K")
            
            print(hangman[wrong_guess])
            print("Incorrect!\n")    
            print(" ".join(blank_word))
            print("Guesses: " + str(", ".join(guesses[:])))
        
        #Resetting character in word variable so it checks for each guess
        char_in_word = False
        
        if "".join(blank_word) == correct_word:
            break
    
    #If nothing is guessed cursor will return back up 2 lines as if the input was never given
    elif guess == "":
        sys.stdout.write("\x1b[2A\x1b[2K")        
        
#User lost
if wrong_guess == 7:
    print("\nGame over! You lost.")

#User won
else:
    print("\nYou won!") 

print("The word was " + "'" + correct_word + "'")