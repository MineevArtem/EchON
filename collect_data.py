import script
import os
import time
from shutil import rmtree, move


def collect_data(zet_path, app):
    for i in os.listdir(os.getcwd() + '/data_sets'):
        print(i)
    folder = input("Folder name: ")
    rang = input("Расстояние: ")
    num = 5
    try:
        os.mkdir(os.getcwd() + '/data_sets/' + folder)
    except:
        pass
    try:
        os.mkdir(os.getcwd() + '/data_sets/' + folder + '/' + rang)
    except:
        pass
    ang = input("Угол: ")
    os.system('cls')
    path = os.getcwd() + '/data_sets/' + folder + '/' + rang
    input("Расстояние " + rang + "см" + '\nPress Enter to continue...\n')
    for i in range(num):
        success = False
        print("Экземпляр", i + 1, end=' ..... ')
        while not success:
            try:
                script.save_data(app)
                time.sleep(0.5)
                move(zet_path + '/oscgrph_1.dtu', path + '/' + ang + '_' + str(i + 1) + '.dtu')
                rmtree(zet_path)
                print("Готово!")
                success = True
            except Exception as e:
                input(str(e))
