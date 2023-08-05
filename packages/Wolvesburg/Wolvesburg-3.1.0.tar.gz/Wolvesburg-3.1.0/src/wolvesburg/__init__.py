import pickle
listy = [[]]
global listyval
listyval = 0


def get(filename: str):
    filename += '.wolvesburg'
    f = open(filename, 'rb')
    data = pickle.load(f)
    f.close()
    return data


class Wolvesburg:
    def __init__(self):
        pass


def deposit(filename: str, data: Wolvesburg):
    filename += '.wolvesburg'
    f = open(filename, 'wb')
    pickle.dump(data, f)
    f.close()


def importxt(filename, object:Wolvesburg):
    filename += '.txt'
    f = open(filename, 'r')
    for i in f:
        global listyval
        listy[listyval].append(i)
    global listyval
    listyval += 1
    object.txt = listy

