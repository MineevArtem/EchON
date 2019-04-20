def open_file(path):
    f = open(path + "/.dtu", 'rb')
    for i in range(12):
        f.readline()
    micro = []
    micro2 = []
    micro3 = []
    micro4 = []
    for i in f:
        line = i.decode().strip().split()
        micro.append(abs(float(line[2])))
        micro2.append(abs(float(line[3])))
        micro3.append(abs(float(line[4])))
        micro4.append(abs(float(line[5])))
    micro.extend(micro2)
    micro.extend(micro3)
    micro.extend(micro4)
    return micro
