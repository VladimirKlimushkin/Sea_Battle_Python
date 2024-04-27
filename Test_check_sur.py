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
    if not(go_up) and hit_points == []:
        hit_points = get_available_coords_shoot(field, cell_coords, True)
        print("", hit_points)
    return hit_points

field = generate_field()

hit_points = get_available_coords_shoot(field, [[5, 3]])
print(hit_points)
hit_points = get_available_coords_shoot(field, [[5, 3], [5, 2]])
print(hit_points)
hit_points = get_available_coords_shoot(field, [[5, 3], [5, 2], [5, 1]])
print(hit_points)
hit_points = get_available_coords_shoot(field, [[5, 3], [5, 2], [4, 1], [6, 1], [5, 1]])
print(hit_points)
hit_points = get_available_coords_shoot(field, [[5, 3], [5, 2], [4, 1], [4, 3], [6, 3], [6, 1], [5, 1]])
print(hit_points)