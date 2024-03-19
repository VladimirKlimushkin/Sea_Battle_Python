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