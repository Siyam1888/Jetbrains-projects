import random


def create_game_field():
    return [" "] * 9
    # return ["X", "O", "X", "O", "O", "X", " ", " ", " "]


def output_game_field(g_f):
    print("-" * 9)
    print("|", *g_f[:3], "|")
    print("|", *g_f[3:6], "|")
    print("|", *g_f[6:9], "|")
    print("-" * 9)


def user_turn(g_f, player):
    while True:
        user_choice = input("Enter the coordinates: ")

        try:
            u_c = [int(i) for i in user_choice.split(" ")]
        except ValueError:
            print("You should enter numbers!")
            continue

        cell = 8 + u_c[0] - u_c[1] * 3

        if u_c[0] not in [1, 2, 3] or u_c[1] not in [1, 2, 3]:
            print("Coordinates should be from 1 to 3!")

        elif g_f[cell] == " ":
            g_f[cell] = "X" if player else "O"
            break

        else:
            print("This cell is occupied! Choose another one!")

    return g_f


def find_empty_cells(g_f):
    empty_cells = []
    for i in range(9):
        if g_f[i] == " ":
            empty_cells.append(i)
    return empty_cells


def easy_computer_turn(g_f, player):
    empty_cells = find_empty_cells(g_f)
    r_c = random.choice(empty_cells)
    print('Making move level \"easy\"')
    g_f[r_c] = "X" if player else "O"
    return g_f


def medium_computer_turn(g_f, player):
    print('Making move level \"medium\"')
    empty_cells = find_empty_cells(g_f)
    for cell in empty_cells:
        g_f[cell] = "X" if player else "O"
        if estimate_game_field(g_f, player) == 10:
            return g_f
        g_f[cell] = " "

    for cell in empty_cells:
        g_f[cell] = "O" if player else "X"
        if estimate_game_field(g_f, player) == -10:
            g_f[cell] = "X" if player else "O"
            return g_f
        g_f[cell] = " "

    r_c = random.choice(empty_cells)
    g_f[r_c] = "X" if player else "O"
    return g_f


def hard_computer_turn(g_f, player):
    empty_cells = find_empty_cells(g_f)
    moves = []
    for cell in empty_cells:
        g_f[cell] = "X" if player else "O"
        moves.append((minimax(g_f, 0, False, player), cell))
        g_f[cell] = " "
    best_move = sorted(moves, reverse=True)[0][1]
    print('Making move level \"hard\"')
    g_f[best_move] = "X" if player else "O"
    return g_f


def minimax(g_f, depth, is_max, player):

    score = estimate_game_field(g_f, player)
    if score == -10 or score == 10:
        return score - depth

    if len(find_empty_cells(g_f)) == 0:
        return 0 - depth

    if is_max:
        best_val = -100
        for move in find_empty_cells(g_f):
            g_f[move] = "X" if player else "O"
            value = minimax(g_f, depth + 1, False, player)
            g_f[move] = " "
            best_val = max(best_val, value)
        return best_val

    else:
        best_val = 100
        for move in find_empty_cells(g_f):
            g_f[move] = "O" if player else "X"
            value = minimax(g_f, depth + 1, True, player)
            g_f[move] = " "
            best_val = min(best_val, value)
        return best_val


def estimate_game_field(g_f, player):

    # Check diagonals
    if g_f[4] != " " and (len({g_f[0], g_f[4], g_f[8]}) == 1 or len({g_f[2], g_f[4], g_f[6]}) == 1):
        return 10 if g_f[4] == ("X" if player else "O") else -10

    # Check rows and col
    for i in range(3):
        first_in_row = 3 * i
        if len({g_f[first_in_row], g_f[first_in_row + 1], g_f[first_in_row + 2]}) == 1 and g_f[first_in_row] != " ":
            return 10 if g_f[first_in_row] == ("X" if player else "O") else -10
        if len({g_f[i], g_f[i + 3], g_f[i + 6]}) == 1 and g_f[i] != " ":
            return 10 if g_f[i] == ("X" if player else "O") else -10

    return 0


while True:
    user_input = input("Input command: ")
    if user_input == "exit":
        break
    try:
        players = user_input.split(" ")
        options = ["easy", "medium", "hard", "user"]
        if not (players[0] == "start" or players[1] in options or players[2] in options):
            print("Bad parameters!")
            continue

    except (ValueError, IndexError):
        print("Bad parameters!")
        continue

    game_over = False
    game_field = create_game_field()
    output_game_field(game_field)

    k = 0
    while not game_over:
        player = (k % 2 == 0)

        current_player_mode = players[1] if player else players[2]
        if current_player_mode == "easy":
            easy_computer_turn(game_field, player)
        elif current_player_mode == "medium":
            medium_computer_turn(game_field, player)
        elif current_player_mode == "hard":
            hard_computer_turn(game_field, player)
        else:
            user_turn(game_field, player)

        output_game_field(game_field)
        current_result = estimate_game_field(game_field, player)

        if current_result == 10:
            print("X" if player else "O", "wins")
            game_over = True
        elif k == 8:
            print("Draw")
            game_over = True

        k += 1






