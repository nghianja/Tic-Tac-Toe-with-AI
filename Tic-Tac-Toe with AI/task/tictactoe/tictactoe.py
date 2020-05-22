# write your code here

field = [[' ' for j in range(4)] for i in range(4)]


def populate_field():
    field_input = input("Enter cells: ")
    input_index = 0
    for i in range(3, 0, -1):
        field[i][0] = '|'
        for j in range(1, 4):
            char = field_input[input_index]
            field[i][j] = ' ' if char == '_' else char
            input_index += 1


def print_field():
    print("---------")
    for i in range(3, 0, -1):
        print(*field[i], sep=' ', end=' |\n')
    print("---------")


if __name__ == "__main__":
    populate_field()
    print_field()
