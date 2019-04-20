import os
import neural_network
import load_data
import sys
from pywinauto.application import Application
import collect_data
from shutil import rmtree


def ns_loop(data, answers, zet_path):
    model = neural_network.Neural_Network()
    while True:
        os.system('cls')
        if model.learned:
            model.model.summary()
        print('Сеть обучена:', model.learned)
        key = int(input("1. Обучить нейронную сеть.\n"
                        "2. Сохранить нейронную сеть.\n"
                        "3. Загрузить нейронную сеть.\n"
                        "4. Запуск\n"
                        '5. Графики\n'
                        '6. TT\n'
                        "0. Назад.\n"))
        if key == 1:
            model.fit_model(data, answers)
        elif key == 2:
            model.save_neural_network()
        elif key == 3:
            model.load_neural_network()
        elif key == 4:
            model.work_neural_network(app, zet_path)
        elif key == 5:
            model.plotting()
        elif key == 6:
            model.test()
        elif key == 0:
            return


def main_loop(app, gen):
    ready_data = False
    data = []
    answers = []
    while True:
        os.system('cls')
        print('Data ready:', ready_data)
        key = input("1. Сохранить выборку.\n"
                    "2. Загрузить данные.\n"
                    '3. Нейронная сеть\n'
                    '4. Запустить ZET210\n'
                    "0. Exit.\n")
        if key == '1':
            os.system('cls')
            collect_data.collect_data(zet_path, app)
        elif key == '2':
            os.system('cls')
            print('Данные загружаются')
            data, answers = load_data.load_data()
            ready_data = True
        elif key == '3':
            ns_loop(data, answers, zet_path)
        elif key == '4':
            if not app.is_process_running():
                app.start("OscGraph.exe")
            if not gen.is_process_running():
                gen.start("DAC_OCX.exe")
        elif key == '0':
            if app.is_process_running():
                app.kill()
            if gen.is_process_running():
                gen.kill()
            sys.exit()


if __name__ == "__main__":
    zet_path = "C:/Users/Public/Documents/ZETLab/artem/result"  # ПУТЬ К ДАННЫМ
    try:
        rmtree(zet_path)
    except FileNotFoundError:
        pass
    print("Find path to oscgraph:", zet_path)
    app = Application(backend="uia")
    gen = Application(backend="uia")
    main_loop(app, gen)
