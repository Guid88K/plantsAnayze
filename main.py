from logic import *
from migrate import *
from histogram import *


def getDataById():
    connection = my_db_connection()

    plant_id = input("Введіть потрібне ID рослини: ")

    plantById = get_from_table(connection, plant_id)

    weightedAverageValueIndex = 0
    countPlantData = len(plantById)

    for p in plantById:
        weightedAverageValueIndex = weightedAverageValueIndex + float(p[5])

    print("Cереднє зважене значення індексу:", weightedAverageValueIndex / countPlantData)


def f():
    print("Недоступно")


def main():
    print("1 - Провести міграцію БД")
    print("2 - Імпортувати дані в таблицю")
    print("3 - Отримати дані по ID рослини")
    print("4 - Візуалізація «частоти» даних в розрізі місяців")
    print("5 - Візуалізація даних по ID")
    print("6 - Завершити роботу")
    cmd = input("Введіть команду: ")

    while cmd != "Exit":
        if cmd == "1":
            migrate()
        elif cmd == "2":
            moveData()
        elif cmd == "3":
            getDataById()
        elif cmd == "4":
            f()
        elif cmd == "6":
            quit()
        elif cmd == "5":
            print("1 - Все")
            print("2 - Візуалізація гістограм частоти")
            print("0 - Вихід")
            cmd1 = input("Введіть команду: ")
            while cmd1 != "Exit":
                if cmd1 == "1":
                    histogram([2, 3, 6, 5, 4, 8])
                    break
                elif cmd == "2":
                    f()
                    break
                else:
                    break
        else:
            print("Такої команди немає!")

        print("1 - Провести міграцію БД")
        print("2 - Імпортувати дані в таблицю")
        print("3 - Отримати дані по ID рослини")
        print("4 - Візуалізація «частоти» даних в розрізі місяців")
        print("5 - Візуалізація даних по ID")
        print("6 - Завершити роботу")
        cmd = input("Введіть команду: ")
    return


if __name__ == '__main__':
    main()
