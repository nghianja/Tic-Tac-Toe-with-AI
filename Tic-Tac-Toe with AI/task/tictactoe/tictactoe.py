from random import randint

# Note: coordinates (x, y) is field[y][x]
mapping = {0: (1, 3), 1: (2, 3), 2: (3, 3),
           3: (1, 2), 4: (2, 2), 5: (3, 2),
           6: (1, 1), 7: (2, 1), 8: (3, 1)}

field = [[' ' for j in range(4)] for i in range(4)]
num_x = 0
num_o = 0
next_player = 'O'
this_player = 'X'


def next_move():
    global num_x, num_o

    move = 'X' if num_x == num_o else 'O'
    if move == 'X':
        num_x += 1
    else:
        num_o += 1
    return move


def populate_field():
    global num_x, num_o

    num_x = 0
    num_o = 0

    field_input = input("Enter cells: ")
    input_index = 0

    for i in range(3, 0, -1):
        field[i][0] = '|'

        for j in range(1, 4):
            char = field_input[input_index]
            field[i][j] = ' ' if char == '_' else char
            if char == 'X':
                num_x += 1
            elif char == 'O':
                num_o += 1
            input_index += 1


def empty_field():
    global num_x, num_o, field

    num_x = 0
    num_o = 0

    field = [[' ' for _j in range(4)] for _i in range(4)]
    for i in range(3, 0, -1):
        field[i][0] = '|'


def print_field():
    print("---------")
    for i in range(3, 0, -1):
        print(*field[i], sep=' ', end=' |\n')
    print("---------")


def get_coordinates():
    while True:
        try:
            coords = input("Enter the coordinates: ").split()
            x = int(coords[0])
            y = int(coords[1])
            if x < 1 or x > 3 or y < 1 or y > 3:
                print("Coordinates should be from 1 to 3!")
                continue
            if field[y][x] != " ":
                print("This cell is occupied! Choose another one!")
                continue
            field[y][x] = next_move()
            break
        except ValueError:
            print("You should enter numbers!")


def has_won():
    if (field[3][1] == field[3][2] and field[3][2] == field[3][3] and field[3][3] != " ") or \
            (field[2][1] == field[2][2] and field[2][2] == field[2][3] and field[2][3] != " ") or \
            (field[1][1] == field[1][2] and field[1][2] == field[1][3] and field[1][3] != " "):
        return True
    elif (field[3][1] == field[2][1] and field[2][1] == field[1][1] and field[1][1] != " ") or \
            (field[3][2] == field[2][2] and field[2][2] == field[1][2] and field[1][2] != " ") or \
            (field[3][3] == field[2][3] and field[2][3] == field[1][3] and field[1][3] != " "):
        return True
    elif (field[3][1] == field[2][2] and field[2][2] == field[1][3] and field[1][3] != " ") or \
            (field[1][1] == field[2][2] and field[2][2] == field[3][3] and field[3][3] != " "):
        return True
    return False


def analyse_field():
    wins = has_won()
    if not wins and num_x + num_o < 9:
        # print("Game not finished")
        return False
    elif not wins and num_x + num_o == 9:
        print("Draw")
    elif wins and num_x == num_o:
        print("O wins")
    else:
        print("X wins")
    return True


def play_move(parameters, turn):
    if parameters[turn % 2] == 'user':
        get_coordinates()
    elif parameters[turn % 2] == 'easy':
        print('Making move level "easy"')
        play_random()
    elif parameters[turn % 2] == 'medium':
        print('Making move level "medium"')
        play_medium()
    else:
        print('Making move level "hard"')
        play_hard()


def play_random():
    while True:
        x = randint(1, 3)
        y = randint(1, 3)
        if field[y][x] != " ":
            continue
        field[y][x] = next_move()
        break


def play_medium():
    if not to_win() and not to_block():
        play_random()


def to_win():
    move = 'X' if num_x == num_o else 'O'
    if move == 'X' and num_x < 2 or move == 'O' and num_o < 2:
        return False
    for i in range(3, 0, -1):
        for j in range(1, 4):
            if field[i][j] == ' ':
                field[i][j] = next_move()
                if has_won():
                    return True
                else:
                    field[i][j] = ' '
    return False


def to_block():
    opp_move = 'O' if num_x == num_o else 'X'
    if opp_move == 'X' and num_x < 2 or opp_move == 'O' and num_o < 2:
        return False
    for i in range(3, 0, -1):
        for j in range(1, 4):
            if field[i][j] == ' ':
                field[i][j] = opp_move
                if has_won():
                    field[i][j] = next_move()
                    return True
                else:
                    field[i][j] = ' '
    return False


def play_hard():
    global this_player, next_player
    next_player = 'O' if num_x == num_o else 'X'
    this_player = 'X' if num_x == num_o else 'O'
    original_board = field[3][1:4] + field[2][1:4] + field[1][1:4]
    for i in range(9):
        if original_board[i] == ' ':
            original_board[i] = str(i)
    best_spot = minimax(original_board, this_player)
    coords = mapping[int(best_spot['index'])]
    field[coords[1]][coords[0]] = next_move()


def minimax(board, player):
    # Minimax implementation based on
    # https://github.com/ahmadabdolsaheb/minimaxarticle/blob/master/index.js
    global this_player, next_player
    avail_spots = list(filter(lambda s: s != 'O' and s != 'X', board))

    # checks for the terminal states such as win, lose, and tie and returning a value accordingly
    if winning(board, next_player):
        return {"score": -10}
    elif winning(board, this_player):
        return {"score": 10}
    elif len(avail_spots) == 0:
        return {"score": 0}

    # an array to collect all the objects
    moves = []

    # loop through available spots
    for spot in avail_spots:
        # create an object for each and store the index of that spot
        # that was stored as a number in the object's index key
        move = {'index': board[int(spot)]}

        # set the empty spot to the current player
        board[int(spot)] = player

        # if collect the score resulted from calling minimax on the opponent of the current player
        if player == this_player:
            result = minimax(board, next_player)
            move['score'] = result['score']
        else:
            result = minimax(board, this_player)
            move['score'] = result['score']

        # reset the spot to empty
        board[int(spot)] = move['index']

        # push the object to the array
        moves.append(move)

    best_move = 0
    if player == this_player:
        best_score = -10000
        for i in range(len(moves)):
            if moves[i]['score'] > best_score:
                best_score = moves[i]['score']
                best_move = i
    else:
        best_score = 10000
        for i in range(len(moves)):
            if moves[i]['score'] < best_score:
                best_score = moves[i]['score']
                best_move = i

    return moves[best_move]


def winning(board, player):
    if (board[0] == player and board[1] == player and board[2] == player) or \
            (board[3] == player and board[4] == player and board[5] == player) or \
            (board[6] == player and board[7] == player and board[8] == player) or \
            (board[0] == player and board[3] == player and board[6] == player) or \
            (board[1] == player and board[4] == player and board[7] == player) or \
            (board[2] == player and board[5] == player and board[8] == player) or \
            (board[0] == player and board[4] == player and board[8] == player) or \
            (board[2] == player and board[4] == player and board[6] == player):
        return True
    return False


if __name__ == "__main__":
    modes = ['user', 'easy', 'medium', 'hard']
    while True:
        parameters = input("Input command: ").split()
        if len(parameters) == 1 and parameters[0] == 'exit':
            break
        if len(parameters) < 3 or parameters[0] != 'start' or \
                parameters[1] not in modes or parameters[2] not in modes:
            print("Bad parameters!")
            continue

        # populate_field()
        empty_field()
        print_field()

        parameters.pop(0)
        turn = 0
        play_move(parameters, turn)
        turn += 1
        print_field()
        while not analyse_field():
            play_move(parameters, turn)
            turn += 1
            print_field()
