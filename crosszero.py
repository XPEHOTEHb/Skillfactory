def clearscreen(nl=50):
    print('\n' * nl)


def hi():
    print("╔═══════════════════════╗")
    print("║  Добро поджаловать в  ║")
    print("║ игру Крестики-нолики! ║")
    print("║⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯║")
    print("║     Формат ввода      ║")
    print("║   XY или X Y, где:    ║")
    print("║   X - номер строки    ║")
    print("║   Y - номер столбца   ║")
    print("╚═══════════════════════╝")


def output():
    print(f"  │ 0 │ 1 │ 2 │")
    for i in range(3):
        print(f"──┼───┼───┼───┤")
        row_str = str(i) + " │ " + " │ ".join(field[i]) + " │"
        print(row_str)
    print(f"──┴───┴───┴───┘")


def user_input():
    while True:
        from_user = str(input("Введите координаты в формате XY или X Y:"))
        if len(from_user) != 2:
            print("Неверный формат координат!")
            continue

        if from_user.isdigit():
            x, y = int(from_user) // 10, int(from_user) % 10
            if field[x][y] != " ":
                print("Клетка занята!")
                continue
            else:
                return x, y

        x, y = map(str, from_user.split())
        if not x.isdigit() and not y.isdigit():
            print("Координаты должны быть цифрами!")
            continue

        x, y = int(x), int(y)
        if x < 0 or x > 2 or y < 0 or y > 2:
            print(x, y)
            print("Вне диапазона!")
            continue

        if field[x][y] != " ":
            print("Клетка занята!")
            continue

        return(x, y)


def check_win():
    win_x = ["X", "X", "X"]
    win_0 = ["0", "0", "0"]
    for i in range(3):
        simbols = []
        for j in range(3):
            simbols.append(field[i][j])
        if simbols == win_x or simbols == win_0:
            print(f"Выиграл {simbols[1]}!")
            return True

    for i in range(3):
        simbols = []
        for j in range(3):
            simbols.append(field[j][i])
        if simbols == win_x or simbols == win_0:
            print(f"Выиграл {simbols[1]}!")
            return True

    simbols = []
    for i in range(3):
        simbols.append(field[i][i])
    if simbols == win_x or simbols == win_0:
        print(f"Выиграл {simbols[1]}!")
        return True

    simbols = []
    for i in range(3):
        simbols.append(field[i][2-i])
    if simbols == win_x or simbols == win_0:
        print(f"Выиграл {simbols[1]}!")
        return True


clearscreen()
hi()
field = [[" "] * 3 for i in range(3)]
counter = 0
while True:
    counter += 1
    output()
    if counter % 2 == 1:
        print("Ходит X")
    else:
        print("Ходит 0")
    x, y = user_input()
    if counter % 2 == 1:
        field[x][y] = "X"
    else:
        field[x][y] = "0"

    clearscreen()

    if check_win():
        output()
        break

    if counter == 9:
        output()
        print("Ничья!")
        break