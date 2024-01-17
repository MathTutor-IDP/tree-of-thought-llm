import json


class node:
    def __init__(self, data):
        self.__data = data
        self.__index = None
        self.__parent = None

    @property
    def data(self):
        return self.__data
    
    @property
    def index(self):
        return self.__index
    
    @property
    def parent(self):
        return self.__parent
    
    @data.setter
    def data(self, data):
        self.__data = data

    @index.setter
    def index(self, index):
        self.__index = index

    @parent.setter
    def parent(self, parent):
        self.__parent = parent

    def __dict__(self):
        return {'data': self.__data, 'index': self.__index, 'parent': self.__parent}

class tree:
    def __init__(self,step=4):
        self.__parent = None
        self.__index = None
        self.__idcount = 0
        self.__tree = [[] for _ in range(step+1)]

    @property
    def index(self):
        return self.__index
    
    @property
    def tree(self):
        return self.__tree
    
    @property
    def parent(self):
        return self.__parent
    
    @parent.setter
    def parent(self, parent):
        self.__parent = parent
    
    @index.setter
    def index(self, index):
        self.__index = index
    
    def add_node(self, node, level):
        self.__tree[level].append(node)

    def json(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)

    def get_id(self):
        self.__idcount += 1
        return self.__idcount
    
    def __dict__(self):
        returnDict = {'parent': self.__parent.__dict__(), 'index': self.__index, 'idcount': self.__idcount}
        tempTree = []
        for layer in self.__tree:
            temp = []
            for leaf in layer:
                temp.append(leaf.__dict__())
            tempTree.append(temp.copy())
        returnDict["tree"] = tempTree
        return returnDict