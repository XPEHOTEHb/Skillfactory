from random import randint


class Dot:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __repr__(self):
        return f"({self.x},{self.y})"


class BoardException(Exception):
    pass


class BoardOutException(BoardException):
    def __str__(self):
        return "Координаты вне игового поля!"


class BoardUsedException(BoardException):
    def __str__(self):
        return "Вы уже стреляли в эту клетку"


class BoardWrongShipException(BoardException):
    pass


class Ship:
    def __init__(self, bow, length, orient):
        self.bow = bow
        self.lenght = length
        self.orient = orient  # bool type True = Horizontal, False = Vertical
        self.lives = length

    @property
    def hull(self):
        ship_hull = []
        for i in range(self.lenght):
            _x = self.bow.x
            _y = self.bow.y
            if self.orient:
                _x += i
            else:
                _y += i
            ship_hull.append(Dot(_x, _y))
        return ship_hull

    def hit(self, shot):
        return shot in self.hull


class Gameboard:
    def __init__(self, hid=False, size=6):
        self.size = size
        self.hid = hid
        self.busy = []
        self.deadship = 0
        self.ships = []
        self.field = [[" "]*size for i in range(size)]

    def add_ship(self, ship):
        for d in ship.hull:
            if self.out(d) or d in self.busy:
                raise BoardWrongShipException

            self.field[d.x][d.y] = "■"
            self.busy.append(d)

        self.ships.append(ship)
        self.contour(ship)

    def contour(self, ship, visible=False):
        near = [
                (-1, -1), (-1, 0), (-1, 1),
                (0, -1), (0, 0), (-0, 1),
                (1, -1), (1, 0), (1, 1)
                ]
        for d in ship.hull:
            for dx, dy in near:
                cur_dot = Dot(d.x + dx, d.y + dy)
                if cur_dot not in self.busy and not self.out(cur_dot):
                    if visible:
                        self.field[cur_dot.x][cur_dot.y] = "◦"
                    self.busy.append(cur_dot)

    def __str__(self):
        output = ""
        output += '\u0332'.join(" │1│2│3│4│5│6│")
        for i, j in enumerate(self.field):
            output += '\u0332'.join(f"\n{i+1}" + "│" + "│".join(j) + "│")

        if self.hid:
            output = output.replace("■", " ")

        return output

    def out(self, d):
        return not((0 <= d.x < self.size) and (0 <= d.y < self.size))

    def shot(self, d):
        if self.out(d):
            raise BoardOutException

        if d in self.busy:
            raise BoardUsedException

        self.busy.append(d)

        for ship in self.ships:
            if d in ship.hull:
                ship.lives -= 1
                self.field[d.x][d.y] = "☒"

                if ship.lives == 0:
                    self.deadship += 1
                    self.contour(ship, visible=True)
                    print("Корабль убит!")
                    return False
                else:
                    print("Корабль ранен!")
                    return True

        self.field[d.x][d.y] = "◦"
        print("Мимо!")
        return False

    def begin(self):
        self.busy = []


class Game:
    def __init__(self, size=6):
        self.size = size
        human = self.random_board()
        computer = self.random_board()
        computer.hid = True
        self.ai = AI(computer, human)
        self.us = User(human, computer)

    def clearscreen(self):
        print('\n' * 50)

    def random_board(self):
        board = None
        while board is None:
            board = self.random_place()
        return board

    def random_place(self):
        boat_queue = [3, 2, 2, 1, 1, 1, 1]
        board = Gameboard()
        attempts = 0
        for _length in boat_queue:
            while True:
                attempts += 1
                if attempts > 2000:
                    return None
                ship = Ship(Dot(randint(0, self.size), randint(0, self.size)), _length, randint(0, 1))
                try:
                    board.add_ship(ship)
                    break
                except BoardWrongShipException:
                    pass
        board.begin()
        return board

    def hi(self):
        print("╔═══════════════════════╗")
        print("║  Добро поджаловать в  ║")
        print("║   игру Морской Бой!   ║")
        print("║⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯║")
        print("║     Формат ввода      ║")
        print("║   XY или X Y, где:    ║")
        print("║   X - номер строки    ║")
        print("║   Y - номер столбца   ║")
        print("╚═══════════════════════╝")

    def loop(self):
        num = 0
        while True:
            #self.clearscreen()
            print("Доска игрока")
            print(self.us.board)
            print("-"*27)
            print("Доска компьютера")
            print(self.ai.board)
            if num % 2:
                print("-" * 27)
                print("Ходит компьютер!")
                repeat = self.ai.move()
            else:
                print("-" * 27)
                print("Вы ходите!")
                repeat = self.us.move()
            if repeat:
                num -= 1

            if self.ai.board.deadship == 7:
                print("-" * 27)
                print("Вы выиграли!")
                print(self.ai.board)
                break

            if self.us.board.deadship == 7:
                print("-" * 27)
                print("Компьютер выиграл!")
                print(self.us.board)
                break
            num += 1

    def start(self):
        self.hi()
        self.loop()


class Player:
    def __init__(self, board, enemy):
        self.board = board
        self.enemy = enemy

    def ask(self):
        raise NotImplementedError()

    def move(self):
        while True:
            try:
                target = self.ask()
                repeat = self.enemy.shot(target)
                return repeat
            except BoardException as e:
                print(e)


class AI(Player):
    def ask(self):
        while True:
            try:
                d = Dot(randint(0, 5), randint(0, 5))
                print(f"Ход компьютера: {d.x + 1}, {d.y + 1}")
                break
            except BoardUsedException:
                pass
        return d


class User(Player):
    def ask(self):
        while True:
            cords = str(input("Введите координаты в формате XY или X Y:"))

            if len(cords) != 2:
                print(" Введите 2 координаты! ")
                continue

            if cords.isdigit():
                x, y = int(cords) // 10, int(cords) % 10
                return Dot(x - 1, y - 1)
            else:
                print("Должны быть числа!")
                continue

            x, y = cords.split()


            if not (x.isdigit()) or not (y.isdigit()):
                print(" Введите числа! ")
                continue

            x, y = int(x), int(y)

            return Dot(x - 1, y - 1)

g = Game()
g.start()
