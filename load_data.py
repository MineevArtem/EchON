import os
import numpy as np
import scipy.misc


def one_data(r, deg, path):
    # print(path + str(r) + '/' + str(deg) + '.dtu')
    with open(path + str(r) + '/' + str(deg) + '.dtu', 'rb') as f:
        for k in range(51):
            f.readline()
        micro = []
        micro2 = []
        micro3 = []
        micro4 = []
        for k in f:
            line = k.decode().strip().split()
            micro.append(abs(float(line[2])))
            micro2.append(abs(float(line[3])))
            micro3.append(abs(float(line[4])))
            micro4.append(abs(float(line[5])))
        micro = micro[:1024]
        micro2 = micro2[:1024]
        micro3 = micro3[:1024]
        micro4 = micro4[:1024]
        micro = np.array(micro)
        micro2 = np.array(micro2)
        micro3 = np.array(micro3)
        micro4 = np.array(micro4)
        micro = micro.reshape(32, 32, 1)
        micro2 = micro2.reshape(32, 32, 1)
        micro3 = micro3.reshape(32, 32, 1)
        micro4 = micro4.reshape(32, 32, 1)
        micro = np.dstack((micro, micro2))
        micro3 = np.dstack((micro3, micro4))
        micro = np.dstack((micro, micro3))
        micro = micro / np.max(micro)
        micro = micro.reshape(1, 32, 32, 4)
    return micro


def test_data(zet_path):
    with open(zet_path + '/oscgrph_1.dtu', 'rb') as f:
        for k in range(51):
            f.readline()
        micro = []
        micro2 = []
        micro3 = []
        micro4 = []
        for k in f:
            line = k.decode().strip().split()
            micro.append(abs(float(line[2])))
            micro2.append(abs(float(line[3])))
            micro3.append(abs(float(line[4])))
            micro4.append(abs(float(line[5])))
        micro = micro[:1024]
        micro2 = micro2[:1024]
        micro3 = micro3[:1024]
        micro4 = micro4[:1024]
        micro = np.array(micro)
        micro2 = np.array(micro2)
        micro3 = np.array(micro3)
        micro4 = np.array(micro4)
        micro = micro.reshape(32, 32, 1)
        micro2 = micro2.reshape(32, 32, 1)
        micro3 = micro3.reshape(32, 32, 1)
        micro4 = micro4.reshape(32, 32, 1)
        micro = np.dstack((micro, micro2))
        micro3 = np.dstack((micro3, micro4))
        micro = np.dstack((micro, micro3))
        # micro = micro.reshape(1, 1024, 4, 1)
        micro = micro / np.max(micro)
        micro = micro.reshape(1, 32, 32, 4)
    return micro


def bord(row):
    left = int(128 - ((128-row) * np.tan(40 / 360 * np.math.pi * 2)))
    right = int(128 + ((128-row) * np.tan(40 / 360 * np.math.pi * 2)))
    return [left, right]


def map_build(r, deg):
    if r == 0 and deg == 0:
        maps = [0 for i in range(128 * 256)]
    else:
        rad = int(deg) / 180 * np.math.pi
        le = 256  # 100см
        rast = 128  # 50см
        b = []
        a = []
        for i in range(le):
            b.append(i - le / 2)
            a.append(round((np.tan(rad) * b[i]), 1))
            s = str(a[i])
            if s[-1] == '3' or s[-1] == '4' or s[-1] == '6' or s[-1] == '7':
                s = s[:-1] + '5'
                a[i] = float(s)
            else:
                a[i] = round(a[i])
        maps = []
        for y in range(rast):
            maps.append([])
            for x in range(le):
                if x == (b[x] + le / 2) and y == (rast - (a[x] * 2 + int(r) * 2 + 1)):
                    maps[y].append(1)
                else:
                    maps[y].append(0)
        for i in range(128):
            ogr = bord(i)
            for j in range(256):
                if j <= ogr[0] or j >= ogr[1]:
                    maps[i][j] = 0

    maps = np.array(maps)
    # print(np.max(maps))
    maps = maps.reshape(1, 128, 256, 1)
    return maps


def load_data():
    print("Select folder:")
    for i in range(len(os.listdir(os.getcwd() + '/data_sets'))):
        print(i+1, os.listdir(os.getcwd() + '/data_sets')[i])
    folder = input('>>> ')
    exp = os.listdir(os.getcwd() + '/data_sets/' + folder)
    # print(exp)
    data = []
    answers = []
    for i in exp:
        for j in os.listdir(os.getcwd() + '/data_sets/' + folder + '/' + i):
            # os.system('cls')
            data.append(one_data(i, j.split('.')[0], os.getcwd() + '/data_sets/' + folder + '/'))
            answers.append(map_build(i, j.split('_')[0]))
    print("Done")
    data = np.concatenate(data, axis=0)
    answers = np.concatenate(answers, axis=0)
    return data, answers


def form_test_data(data):
    data = data.tolist()
    for i in range(128):
        ogr = bord(i)
        for j in range(256):
            if float(data[i][j]) < 1.:
                if float(data[i][j]) < 0.50:
                    data[i][j] = (0, 0, 0)
                else:
                    data[i][j] = (int(data[i][j] * 255), int(data[i][j] * 255), int(data[i][j] * 255))
            else:
                data[i][j] = (255, 255, 255)
    data = np.array(data)
    return data
