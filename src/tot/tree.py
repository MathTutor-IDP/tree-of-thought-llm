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

class tree:
    def __init__(self,step=4):
        self.__idcount = 0
        self.__tree = [[] for _ in range(step)]

    @property
    def idcount(self):
        self.__idcount += 1
        return self.__idcount

    @property
    def tree(self):
        return self.__tree
    
    def add_node(self, node, level):
        self.__tree[level].append(node)

