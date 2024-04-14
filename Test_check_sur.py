LETTERS = (' ', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J')

def generate_field() -> list:
    """
    Генерирует поле 10*10
    :return: list
    """
    field = []
    for i in range(11):
        field.append([0]*11)
        if i == 0:
            field[i] = LETTERS
        else:
            field[i][0] = i
    return field

def print_field(field: list):
    """
    Вывод поля в консоль
    :param field:
    :return:
    """
    sep_lst = ['  | ']*10
    sep_lst.append(' | ')
    for i in range(11):
        for j in range(11):
            point = field[i][j]
            point_str = str(point)
            if point == 0:
                print(' '+' | ', end="")
            elif j == 0:
                print(point_str + sep_lst[i], end="")
            else:
                print(point_str + ' | ', end="")
        print(f"\n   "+"-"*41)

def add_ship_on_field(field: list, x_cord: int, y_cord: int, cells, orientation: bool, x: int, y: int):
    is_in_if = False
    if (not(orientation) and (y_cord > 0 and y_cord <= 11-cells) and (x_cord > 0 and x_cord <= 10)) or (orientation and (y_cord > 0 and y_cord <= 10) and (x_cord > 0 and x_cord <= 11-cells)):
        is_in_if = True
        for j in range(cells):
            if orientation:
                field[y][x + j] = cells
            else:
                field[y + j][x] = cells
    return is_in_if

field = generate_field()

counter_errors = 0

for i in range(0, 12):
    for j in range(0, 12):
        if not add_ship_on_field(field, i, j, 4, True, i, j):
            counter_errors += 1

print_field(field)

print(counter_errors)