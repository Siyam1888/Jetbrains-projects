import random

print("H A N G M A N")
lis = ['python', 'java', 'kotlin', 'javascript']


def get_word():
    random_word = random.choice(lis)
    return random_word


def play(random_word):
    guessed_letters = []
    word_completion = len(random_word) * '-'
    word_in_list = list(word_completion)
    count = 0
    while True:
        print()
        print(word_completion)
        guess = input("Input a letter: ")
        if len(guess) != 1:
            print('You should print a single letter')
        elif guess.islower() is False:
            print("It is not an ASCII lowercase letter")
        elif guess in guessed_letters:
            print("You already typed this letter ")
        elif guess not in random_word:
            print('No such letter in the word')
            count += 1
        guessed_letters.append(guess)
        indices = [i for i, letter in enumerate(random_word) if letter == guess]
        for index in indices:
            word_in_list[index] = guess
        word_completion = ''.join(word_in_list)
        if "-" not in word_completion:
            print(f"You guessed the word {random_word}!")
            print("You survived!")
            break
        elif count == 8:
            print("You are hanged!")
            break


def main():
    while True:
        decision = input('Type "play" to play the game, "exit" to quit:')
        if decision == 'play':
            random_word = get_word()
            play(random_word)
        elif decision == 'exit':
            break


main()

