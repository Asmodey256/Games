v_coordinats = ("0", "1", "2")

field = [[" " for x in range(3)] for y in range(3)]

def vis_field(field):
    print(" ", "0", "1", "2")
    for y, v in enumerate(v_coordinats):
        print (v, " ".join(field[y]))

def question():
    while True:
        x = input("Введите значение по горизонтали: ")
        y = input("Введите значение по вертикали: ")
        x, y = int(x), int(y)
        if 0<=x<=2 and 0<=y<=2:
            if field [x][y] == " ":
                return x, y
            else:
                print("Позиция занята")
        else:
            print("Значение указано не верно")

def win():
    combination = [((0, 0), (0, 1), (0, 2)), ((1, 0), (1, 1), (1, 2)), ((2, 0), (2, 1), (2, 2)),
                   ((0, 0), (1, 0), (2, 0)), ((0, 1), (1, 1), (2, 1)), ((0, 2), (1, 2), (2, 2)),
                   ((0, 0), (1, 1), (2, 2)), ((0, 2), (1, 1), (2, 0))]
    for comb in combination:
        sign = []
        for a in comb:
            sign.append(field [a[0]][a[1]])
        if sign == ["X", "X", "X"]:
            print("Выйграл Х")
            return True
        if sign == ["О", "О", "О"]:
            print("Выйграл О")
            return True
    return False


num = 0
while True:
    num +=1
    vis_field(field)
    if num % 2 == 1:
        print("Ходит X")
    else:
        print("Ходит O")
    x, y = question()
    if num % 2 == 1:
        field [x][y] = "X"
    else:
        field[x][y] = "O"
    if win():
        break
    if num == 9:
        print("Ходы закончились")
        break


