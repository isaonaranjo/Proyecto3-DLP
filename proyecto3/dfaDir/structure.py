# to create the automata
class Automata:
    def __init__(self, expresion):
        self.expresion = expresion
        self.state = []

    def __str__(self):
        string = 'State: ' + str(self.state)
        return string

class State:
    def __init__(self, name, id):
        self.name = name
        self.id = id
        # transition list
        self.transition = []
        # is it accept transition
        self.accept = False

    def __str__(self):
        string = 'Id: ' + str(self.name) + '\n'
        return string


class Handler:
    def __init__(self, symbol, id):
        # symbol in the tree
        self.symbol = symbol
        # id where is go
        self.id = id

        