# this board takes coordinate as input
board = [[' ', ' ', ' '], [' ', ' ', ' '], [' ', ' ', ' ']]
player = ['O']
winner = ' '
game_is_still_going = True


# changes element according to given coordinate
def coordinate():
    try:
        global board
        x, y = input("Enter the coordinates: ").split()

        if x.isalpha() and y.isalpha():
            print("You should enter numbers!")
        elif int(x) >= 4 or int(y) >= 4:
            print("Coordinates should be from 1 to 3!")
        elif board[int(x) - 1][int(y) - 1] == " " and player[-1] != "X":
            board[int(x) - 1][int(y) - 1] = "X"
            player.append("X")
            display_board()
        elif board[int(x) - 1][int(y) - 1] == " " and player[-1] != "O":
            board[int(x) - 1][int(y) - 1] = "O"
            player.append("O")
            display_board()
        elif board[int(x) - 1][int(y) - 1] == "X" or "O":
            print("This cell is occupied! Choose another one!")

    except ValueError:
        print("You should enter numbers")


def display_board():
    print("---------")
    print("|" + ' ' + board[0][2] + ' ' + board[1][2] + ' ' + board[2][2] + ' ' + "|")
    print("|" + ' ' + board[0][1] + ' ' + board[1][1] + ' ' + board[2][1] + ' ' + "|")
    print("|" + ' ' + board[0][0] + ' ' + board[1][0] + ' ' + board[2][0] + ' ' + "|")
    print("---------")


def play():
    global game_is_still_going
    while game_is_still_going:
        coordinate()
        check_for_winner()
        if winner == "X" or winner == "O":
            print(winner + " wins")
            game_is_still_going = False
        elif winner == 'draw' and len(player) == 10:
            print("Draw")
            break


def check_for_winner():
    row_winner = check_row()
    column_winner = check_column()
    diagonal_winner = check_diagonal()

    global winner
    if row_winner:
        winner = row_winner
    elif column_winner:
        winner = column_winner
    elif diagonal_winner:
        winner = diagonal_winner
    else:
        winner = 'draw'
    return


def check_row():
    row_1 = board[0][2] == board[1][2] == board[2][2] != ' '
    row_2 = board[0][1] == board[1][1] == board[2][1] != ' '
    row_3 = board[0][0] == board[1][0] == board[2][0] != ' '
    if row_1:
        return board[0][2]
    elif row_2:
        return board[0][1]
    elif row_3:
        return board[0][0]
    return


def check_column():
    row_1 = board[0][0] == board[0][1] == board[0][2] != ' '
    row_2 = board[1][0] == board[1][1] == board[1][2] != ' '
    row_3 = board[2][0] == board[2][1] == board[2][2] != ' '
    if row_1:
        return board[0][0]
    elif row_2:
        return board[1][0]
    elif row_3:
        return board[2][0]
    return


def check_diagonal():
    row_1 = board[0][2] == board[1][1] == board[2][0] != ' '
    row_2 = board[0][0] == board[1][1] == board[2][2] != ' '
    if row_1:
        return board[0][2]
    elif row_2:
        return board[0][0]
    return


display_board()
play()