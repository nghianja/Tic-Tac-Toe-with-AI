from random import randint

# Note: coordinates (x, y) is field[y][x]

field = [[' ' for j in range(4)] for i in range(4)]
num_x = 0
num_o = 0


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


def analyse_field():
    wins = False
    if (field[3][1] == field[3][2] and field[3][2] == field[3][3] and field[3][3] != " ") or \
            (field[2][1] == field[2][2] and field[2][2] == field[2][3] and field[2][3] != " ") or \
            (field[1][1] == field[1][2] and field[1][2] == field[1][3] and field[1][3] != " "):
        wins = True
    elif (field[3][1] == field[2][1] and field[2][1] == field[1][1] and field[1][1] != " ") or \
            (field[3][2] == field[2][2] and field[2][2] == field[1][2] and field[1][2] != " ") or \
            (field[3][3] == field[2][3] and field[2][3] == field[1][3] and field[1][3] != " "):
        wins = True
    elif (field[3][1] == field[2][2] and field[2][2] == field[1][3] and field[1][3] != " ") or \
            (field[1][1] == field[2][2] and field[2][2] == field[3][3] and field[3][3] != " "):
        wins = True
    if not wins and num_x + num_o < 9:
        print("Game not finished")
        return False
    elif not wins and num_x + num_o == 9:
        print("Draw")
    elif wins and num_x == num_o:
        print("O wins")
    else:
        print("X wins")
    return True


def play_random():
    print('Making move level "easy"')
    while True:
        x = randint(1, 3)
        y = randint(1, 3)
        if field[y][x] != " ":
            continue
        field[y][x] = next_move()
        break


if __name__ == "__main__":
    # populate_field()
    empty_field()
    print_field()
    get_coordinates()
    print_field()
    while not analyse_field():
        if num_x == num_o:
            get_coordinates()
        else:
            play_random()
