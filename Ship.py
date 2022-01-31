from random import randint

class BoardException(Exception):
    pass

class BoardOut(BoardException):
    def __str__(self):
        return "Вы выстрелили за границы поля, скорректируйте огонь"

class BoardRepeat(BoardException):
    def __str__(self):
        return "Повторный выстрел по координатам"

class BoardShipPlascemnt(BoardException):
    pass

class Dot:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __repr__(self):
        return f"({self.x}, {self.y})"

class Ship:
    def __init__(self, shipx, shipy, shipz):
        self.shipx = shipx
        self.shipy = shipy
        self.shipz = shipz
        self.leavs = shipy
    @property
    def stern(self):
        ship_stern = []
        for i in range(self.shipy):
            stern_x = self.shipx.x
            stern_y = self.shipx.y
            if self.shipz == 0:
                stern_x += i
            elif self.shipz == 1:
                stern_y += i
            ship_stern.append(Dot(stern_x, stern_y))
        return ship_stern

    def shooten (self, shoot):
        return shoot in self.stern


class Board:
    def __init__(self, hid = False, size = 6):
        self.hid = hid
        self.size = size
        self.field = [["O"]*size for _ in range(size)]
        self.Ship = []
        self.cont = 0
        self.busy = []

    def __str__(self):
        res = ""
        res += "  | 1 | 2 | 3 | 4 | 5 | 6 |"
        for i, row in enumerate(self.field):
            res += f"\n{i + 1} | " + " | ".join(row) + " |"
        if self.hid:
            res = res.replace("■", "O")
        return res

    def contour(self, ship, verb=False):
        located = [
                   (-1, -1), (0, -1), (1, -1),
                   (-1, 0), (0, 0), (1, 0),
                   (-1, 1), (0, 1), (1, 1)
                   ]
        for n in ship.stern:
            for nx, ny in located:
                cur = Dot(n.x + nx, n.y + ny)
                if not (self.out(cur)) and cur not in self.busy:
                    if verb:
                        self.field[cur.x][cur.y] = "."
                    self.busy.append(cur)

    def r_ship(self, ship):
        for n in ship.stern:
            if self.out(n) or n in self.busy:
                raise BoardShipPlascemnt()
        for n in ship.stern:
            self.field[n.x][n.y] = "■"
            self.busy.append(n)
        self.Ship.append(ship)
        self.contour(ship)

    def out(self, n):
        return not((0<= n.x < self.size) and (0<= n.y < self.size))

    def shoot(self, n):
        if self.out(n):
            raise BoardOut()
        if n in self.busy:
            raise BoardRepeat()
        self.busy.append(n)
        for ship in self.Ship:
            if n in ship.stern:
                ship.leavs -= 1
                self.field [n.x][n.y] = "X"
                if ship.leavs == 0:
                    self.cont += 1
                    self.contour(ship, verb=True)
                    print("-" * 30)
                    print("Корабль потоплен")
                    return False
                else:
                    print("-" * 30)
                    print("Есть пробитие")
                    return True
        self.field[n.x][n.y] = "."
        print("-"*30)
        print("Промах")
        return False

    def begin(self):
        self.busy = []


class Players:
    def __init__(self, board, enemy):
        self.board = board
        self.enemy = enemy

    def ask(self):
        raise NotImplementedError()

    def step(self):
        while True:
            try:
                target = self.ask()
                repeat = self.enemy.shoot(target)
                return repeat
            except BoardException as a:
                print(a)

class User(Players):
    def ask(self):
        while True:
            y = int(input("Введите координаты по горизонтали: "))
            x = int(input("Введите координаты по вертикали: "))
            x, y = int(x), int(y)
            return Dot(x - 1, y - 1)

class Aiplayers(Players):
    def ask(self):
        x = randint(1, 6)
        y = randint(1, 6)
        return Dot(x - 1, y - 1)

class Games:
    def __init__(self, size = 6):
        self.size = size
        player = self.random_board()
        computer = self.random_board()
        computer.hid = True
        self.ai = Aiplayers(computer, player)
        self.us = User(player, computer)

    def random_board(self):
        board = None
        while board is None:
            board = self.n_board()
        return board

    def n_board(self):
        lens = [3, 2, 2, 1, 1, 1, 1]
        board = Board(size = self.size)
        version = 0
        for n in lens:
            while True:
                version += 1
                if version > 3000:
                    return None
                ship = Ship(Dot(randint(0, self.size), randint(0, self.size)), n, randint(0,1))
                try:
                    board.r_ship(ship)
                    break
                except BoardShipPlascemnt:
                    pass
        board.begin()
        return board

    def turn(self):
        step = 0
        while True:
            print("Доска пользователя:")
            print(self.us.board)
            print("Доска компьютера:")
            print(self.ai.board)
            if step % 2 == 0:
                print("Ход игрока")
                repeat = self.us.step()
            else:
                print("Ход компьютера")
                repeat = self.ai.step()
            if repeat:
                step -= 1
            if self.ai.board.cont == 7:
                print("Выйграл пользователь")
                break
            if self.us.board.cont == 7:
                print("Выйграл компютер")
                break
            step += 1

    def start(self):
        self.turn()

a = Games()
a.start()