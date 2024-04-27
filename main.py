import random



CONFIG_SHIPS = {
    'type_1': {'cells': 1, 'amount': 4},
    'type_2': {'cells': 2, 'amount': 3},
    'type_3': {'cells': 3, 'amount': 2},
    'type_4': {'cells': 4, 'amount': 1}
}
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

def input_command(field: list):
    """
    Принимает координату попадания
    :param field: list
    :return:
    """
    command = str(input())
    str_array = list(command)
    if command == 'field':
        print_field(field)
    elif len(str_array) > 3:
        str_array = []
    return str_array

def set_user_field(field: list):
    """
    Функция для установки кораблей на поле пользователя.
    :param field: list
    :return:
    """

    print('Введите координаты корабля')
    for key,config in CONFIG_SHIPS.items():
        cells = config['cells']

        print(f" из {cells} ячеек:\n")
        for i in range(config['amount']):

            print('Введите координаты носа корабля:')

            command1 = input()

            if not command1:
                i -= 1
                continue

            if cells > 1:
                print("Введите координаты кормы корабля:")
                command2 = input()
                if not command2:
                    i -= 1
                    continue
            else:
                command2 = command1

            letter_1 = command1[0].upper()
            letter_2 = command2[0].upper()
            command1 = command1[1:]
            number_1 = int(''.join(command1))

            # 0 - вертикальная ориентация, 1 - горизонтальная
            orientation = letter_1 != letter_2

            letter_index1 = LETTERS.index(letter_1)

            ship_cords = get_ship_cords([letter_index1, number_1], orientation, cells)[0]
            x = ship_cords[0]
            y = ship_cords[1]

            while not check_surrounding(field, [x, y], orientation, cells):
                [x, y] = get_empty_position(field)
                orientation = bool(random.randint(0, 1))  # 0 - вертикальная ориентация, 1 - горизонтальная
            if field[y][x] == 0:
                stand_ship_point_on_field(cells, orientation, field, x, y)
                print_field(field)

def stand_ship_point_on_field(cells: list, orientation: bool, field: list, x: int, y: int):
    for j in range(cells):
        if orientation:
            field[y][x + j] = cells
        else:
            field[y + j][x] = cells

def check_surrounding(field: list, cell_1: list, orientation: bool, type: int):
    """
    Проверяет окружение вокруг точки на наличие посторонних точек
    :param field:
    :param cell_1:
    :param orientation:
    :param type:
    :return:
    """
    cell_0 = [cell_1[0] - 1, cell_1[1] - 1]
    rows_counter = 3 if orientation else 2 + type
    cols_counter = 2 + type if orientation else 3
    ship_cords = get_ship_cords(cell_1, orientation, type)
    for i in range(rows_counter):
        y = cell_0[1] + i
        for j in range(cols_counter):
            x = cell_0[0] + j
            current_cell = [x, y]
            if x <= 0 or y <= 0:
                continue
            if y > 10 or x > 10:
                continue
            if current_cell in ship_cords:
                continue
            if field[y][x] != 0:

                return False
    return True

def get_ship_cords(head: list, orientation: bool, type: int):
    """
    возвращает массив с координатами корабля
    :param head:
    :param orientation:
    :param type:
    :return:
    """
    result = [head]
    for i in range(1, type):
        x = head[0] + (i if orientation else 0)
        y = head[1] + (0 if orientation else i)
        result.append((x, y))
    return result

def get_empty_position(field: list):
    """
    Находит рандомную пустую точку на поле
    :param field:
    :return:
    """
    field_new = field[1:]
    y = random.randrange(1, 10)
    x = random.randrange(1, 10)
    col_value = field_new[y][x]
    if col_value != 0:
        while col_value != 0:
            y = random.randrange(1, 10)
            x = random.randrange(1, 10)
            col_value = field_new[y][x]
    return [x, y]

def generate_ship(field: list, ship_settings: dict):
    """
    Генерирует корабли
    :param field:
    :param ship_settings:
    :param ships:
    :return:
    """
    amount = ship_settings['amount']
    cells = ship_settings['cells']
    for i in range(amount):
        is_head = True
        key = ''
        while True:
            orientation = bool(random.randint(0, 1))  # 0 - вертикальная ориентация, 1 - горизонтальная
            [x, y] = get_empty_position(field)
            while not check_surrounding(field, [x, y], orientation, cells):
                [x, y] = get_empty_position(field)
                orientation = bool(random.randint(0, 1))  # 0 - вертикальная ориентация, 1 - горизонтальная

            y_cord = y + cells - 1 if orientation else y
            x_cord = x + cells - 1 if orientation else x

            key, is_head = toggle_is_head(is_head, x_cord, y_cord)
            is_in_if = add_ship_on_field(field, x_cord, y_cord, cells, orientation, x, y)
            if is_in_if:
                break

def toggle_is_head(is_head:bool, x_cord:int, y_cord:int):
    key = ""
    if is_head:
        key = f"{x_cord}{y_cord}"
        is_head = False
    return [key, is_head]


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
def shoot_coords_user(field: list, field_user: list, total_score: int, user_score: int):
    """
    Спрашивает координату выстрела юзера
    :param field:
    :param field_user:
    :param total_score:
    :param user_score:
    :return:
    """
    while True:
        print("Введите координаты выстрела:")
        command = input_command(field_user)
        letter = command[0].upper()
        if letter == "":
            continue
        del(command[0])
        number = int(''.join(set(command)))
        letter_index = LETTERS.index(letter)
        point_cords = get_ship_cords([letter_index, number], 0, 1)[0]
        x = int(point_cords[0])
        y = int(point_cords[1])
        if field[y][x] != 0:
            if not(check_ship_hit_user(y, x, field, user_score, total_score)):
                return False
        else:
            print("Вы промазали!")
            break
    return True

def check_ship_hit_user(y, x, field, user_score, total_score):
    if field[y][x] != "X":
        print("Вы попали!")
        field[y][x] = "X"
        user_score += 1
        if total_score == user_score:
            print("Поздравляем! Вы победили!")
            return False
    else:
        print("Вы сюда уже стреляли!")
    return True
def get_available_coords_shoot(field: list, cell_coords: list, go_up=False):
    """
    Возвращает массив координат, доступных для выстрела
    :param field:
    :param cell_coords:
    :param go_up:
    :return:
    """
    last_shot = cell_coords[-1] if not(go_up) else cell_coords[0]
    cell_0 = [last_shot[0]-1, last_shot[1]-1]
    hit_points = []
    range_list = range(3)
    for i in range_list:
        y = cell_0[1] + i
        for j in range_list:
            x = cell_0[0] + j
            current_cell = [x, y]

            # Проверяет на выход за пределы карты
            if y > len(field) or x > len(field[y]) or x == 0 or y == 0:
                continue
            # Проверка на диагонали
            if (i == 0 and j == 0) or (i == 0 and j == 2) or (i == 2 and j == 0) or (i == 2 and j == 2):
                continue
            # Проверка на пустоту ячейки
            if field[y][x] == 'O' or field[y][x] == 'X':
                continue
            hit_points.append(current_cell)
    for coords in cell_coords:
        if coords in hit_points:
            key = hit_points.index(coords)
            del(hit_points[key])
    print(hit_points)
    if not(go_up) and hit_points == []:
        print("recurs,", cell_coords)
        hit_points = get_available_coords_shoot(field, cell_coords, True)
        print("recurs,", hit_points)
        print_field(field)
    return hit_points

def shoot_coords_computer(field: list, total_score: int, computer_score: int, hit_coords_computer: list):
    """
    Спрашивает координату выстрела компьютера
    :param field:
    :param total_score:
    :param computer_score:
    :param hit_coords_computer:
    :return:
    """
    while True:
        if len(hit_coords_computer) > 0:
            hit_points = get_available_coords_shoot(field, hit_coords_computer)
            random_shoot_key = hit_points.index(random.choice(hit_points))
            random_shoot = hit_points[random_shoot_key]
            letter = LETTERS[random_shoot[0]]
            hit_coord = field[random_shoot[1]][random_shoot[0]]
            if hit_coord != 0:
                if hit_coord not in ['X', 'O']:
                    coord_print = letter+str(random_shoot[1])
                    print(f"Противник попал: {coord_print}")
                    hit_coords_computer.append(random_shoot)
                    ship_type = int(field[random_shoot[1]][random_shoot[0]])
                    field[random_shoot[1]][random_shoot[0]] = 'X'
                    if len(hit_coords_computer) == ship_type:
                        print(hit_points)
                        print("Корабль уничтожен!")
                        hit_coords_computer = []
                        continue
                    if total_score == computer_score:
                        print("К сожалению, Вы проиграли!")
                        return False
            else:
                coord_print = letter + str(random_shoot[1])
                print(f"Противник промазал: {coord_print}")
                field[random_shoot[1]][random_shoot[0]] = 'O'
                break
        else:
            number = random.randint(1, 10)
            letter_index = random.randint(1, 10)
            point_cords = get_ship_cords([letter_index, number], 0, 1)[0]
            letter = LETTERS[letter_index]
            hit_coord = field[point_cords[1]][point_cords[0]]
            if hit_coord != 0:
                if hit_coord not in ['X', 'O']:
                    coord_print = letter+str(point_cords[1])
                    print(f"Противник попал: {coord_print}")
                    hit_coords_computer.append(point_cords)
                    ship_type = int(field[point_cords[1]][point_cords[0]])
                    field[point_cords[1]][point_cords[0]] = "X"
                    if len(hit_coords_computer) == ship_type:
                        print("Корабль уничтожен!")
                        hit_coords_computer = []
                        continue
                    if total_score == computer_score:
                        print("К сожалению, Вы проиграли!")
                        return False
            else:
                coord_print = letter + str(point_cords[1])
                print(f"Противник промазал: {coord_print}")
                field[point_cords[1]][point_cords[0]] = 'O'
                break
    return True



def init():
    """
    Инициация программы
    :return:
    """
    user_score = 0 # Счёт игрока, увеличивается при подбитии
    computer_score = 0 # Счёт компьютера, увеличивается при подбитии
    total_score = 0 # Тотальный счёт, по которому проверяем конец игры

    hit_coords_computer = [] # Координаты всех сделанных компьютером попаданий
    hit_coords_user = []

    field = generate_field()
    field_user = generate_field()
    for index, ship_conf in CONFIG_SHIPS.items():
        generate_ship(field, ship_conf)
        generate_ship(field_user, ship_conf)
        total_score += ship_conf['cells'] * ship_conf['amount']

    # set_user_field(field_user)
    is_user_move = bool(random.randint(0, 1)) # ходит ли пользователь первым
    if is_user_move:
        print("Первым стреляете Вы\n")
    else:
        print("Первым стреляет противник\n")

    game = True # идёт ли игра
    while game:
        # game = shoot_coords_user(field, field_user, total_score, user_score) if is_user_move else shoot_coords_computer(field_user, total_score, computer_score, hit_coords_computer)
        print(is_user_move)
        game = shoot_coords_computer(field, total_score, user_score, hit_coords_user) if is_user_move else shoot_coords_computer(field_user, total_score, computer_score, hit_coords_computer) # Ходы пользователя и компьютера
        is_user_move = not(is_user_move) # смена ходов

init()