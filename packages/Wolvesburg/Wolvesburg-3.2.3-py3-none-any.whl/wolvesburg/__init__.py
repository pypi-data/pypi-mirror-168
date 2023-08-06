import pickle
listy = [[]]
global listyval
listyval = 0


def get(filename: str):
    """
    Fetches data from a .wolvesburg file
    :param filename: filename without extension
    :return: data from file
    """
    filename += '.wolvesburg'
    f = open(filename, 'rb')
    data = pickle.load(f)
    f.close()
    return data


class Wolvesburg:
    def __init__(self):
        pass


def deposit(filename: str, data: Wolvesburg):
    """deposit(filename without extension, data: wolvesburg object)
    :returns Nothing
    :parameter filename -> filename without extension
    :parameter data -> data, object of wolvesburg class
    Adds data to a wolvesburg file
    """
    filename += '.wolvesburg'
    f = open(filename, 'wb')
    pickle.dump(data, f)
    f.close()


def importxt(filename, object:Wolvesburg):
    """

    :param filename: filename of import file without extension
    :param object: Object of wolvesburg class to upload data to
    :return: nothing
    Adds data from a txt file to a wolvesburg object
    """
    filename += '.txt'
    f = open(filename, 'r')
    for i in f:
        listy[listyval].append(i)
    global listyval
    listyval += 1
    object.txt = listy

