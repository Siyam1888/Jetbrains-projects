# Write your code here
import random

move = ['scissors', 'paper', 'rock']
lose_conditions = {"rock": "paper", "paper": "scissors", "scissors": "rock"}


def turn(lis):
    last = lis.pop(-1)
    lis.insert(0, last)
    return lis


name = input()
print(f"Hello, {name}")
options = input().split(',')
print("Okay, let's start")


players = {}
with open("rating.txt", "r") as file:
    for line in file:
        nme, pts = line.split()
        players[nme] = int(pts)

points = players.get(name, 0)


while True:
    player_move = input()
    if player_move == "!exit":
        print("Bye!")
        break
    elif player_move == "!rating":
        print(f"Your rating: {points}")

        """Game with multiple options"""
    elif len(options) > 1:
        if player_move in options:
            ind = options.index(player_move)
            span = (len(options) // 2) + 1
            comp_winning_list = options[ind:ind + span]
            comp_choice = random.choice(options)
            turn_cond = len(comp_winning_list) < span

            while turn_cond:
                options = turn(options)
                ind = options.index(player_move)
                comp_winning_list = options[ind:ind + span]
                turn_cond = len(comp_winning_list) < span

            if player_move == comp_choice:
                print(f'There is a draw ({player_move})')
                points += 50
            elif comp_choice in comp_winning_list:
                print(f'Sorry, but computer chose {comp_choice}')
            else:
                print(f'Well done. Computer chose {comp_choice} and failed')
                points += 100
        else:
            print('Invalid input')

    else:
        """Traditional rock-paper-scissors"""
        r = random.randint(0, 2)
        if player_move not in move:
            print("Invalid input")
        elif player_move == move[r]:
            print(f"There is a draw ({move[r]})")
            points += 50
        elif lose_conditions[player_move] == move[r]:
            print(f"Sorry, but computer chose {move[r]}")
        else:
            print(f"Well done. Computer chose {move[r]} and failed")
            points += 100
