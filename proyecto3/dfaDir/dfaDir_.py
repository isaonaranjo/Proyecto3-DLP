'''
    Maria Isabel Ortiz Naranjo
'''


from dfaDir.structure import Automata, State, Handler
from dfaDir.tree import Tree
from dfaDir.cal import lastpos, firstpos, followpos, states_tree
from collections import Counter

OPERATORS = ['|', '*', 'ψ', '?', 'ξ', ')', '(']
EPSILON = "ε"

def sintetic_tree(data_tree, expresion):
    # class Tree
    value_tree = Tree()
    value_tree.data = 'ξ'
    leaves = Tree()
    # mark symbol
    leaves.data = '#'
    # add to the new tree
    value_tree.right = leaves
    value_tree.left = data_tree

    # to create
    tree = states_tree(value_tree)
    first = firstpos(value_tree)
    last = lastpos(value_tree)
    # dictionary with the id state of node
    data = {}
    for position in tree:
        data[position] = []
    followpos(value_tree, data)
    
    tree_sintetic = direct(first, last, data, expresion)

    return tree_sintetic

def direct(first, last, data, expresion):
    automata = Automata(expresion)
    inicial = State(first, len(automata.state))
    automata.state.append(inicial)

    # take the last position
    if last[-1] in inicial.name:
        inicial.accept = True

    # symbols = get_symbol(expresion)
    symbols = []
    
    i = 0
    temp = ''

    while (i<len(expresion)):
        if (expresion[i] not in OPERATORS) and (expresion[i] not in symbols) and (expresion[i] != EPSILON):
            temp += expresion[i]
        if (expresion[i] in OPERATORS) and (temp != EPSILON) and (temp not in symbols) and (temp != ''):
            symbols.append(temp)
            temp = ""
        # sumamos al contador
        i += 1

    if temp != "":
        symbols.append(temp)

    # go through the states of the automata
    for state in automata.state:
        for i in symbols:
            value = []
            for position in state.name:
                if position.data == i:
                    temp = data[position]
                    for j in temp:
                        if j not in value:
                            value.append(j)
            # if movements, ando no empty
            if movements(automata, value) and value != []:
                new_node = State(value, len(automata.state))
                if last[-1] in value:
                    new_node.accept = True
                automata.state.append(new_node)
                state.transition.append(Handler(i, automata.state[-1].id))
            # if value is emtpy
            elif value != []:
                # go to tree, and search the id
                add = add_tree(automata, value)
                if add:
                    state.transition.append(Handler(i, add.id))
                else:
                    print('There ir no node with %s ' % value)

    return automata

# if exist the node into the tree
def movements(tree, state):
    for node in tree.state:
        if Counter(node.name) == Counter(state):
            return False
    return True

def add_tree(automata, id):
    for node in automata.state:
        if Counter(node.name) == Counter(id):
            return node
    return False

# funcion de epsilon lock del primer nodo
def ecerradura_node(automata, node):
    for i in node:
        for j in automata.states[i].transitions:
            if (j.symbol == EPSILON) and (j.id not in node):
                node.append(j.id)
    return node

def simulate_dfa_direct(automata, expresion):
    if expresion == ' ' or expresion == '':
        expresion = EPSILON
    current_node = [0]
    current_node = ecerradura_node(automata, current_node)
    i = 0
    while True:
        value = []
        for node in current_node:
            for transitions in automata.states[node].transitions:
                # si el simbolo se encuentra en la expresion y no en los evaluados, se agrega a la lista
                if (transitions.symbol == expresion[i]) and (transitions.id not in value):
                    value.append(transitions.id)
        i += 1
        # tomamos de la lista la nueva cerradura
        value = ecerradura_node(automata, value)

        # si no esta en la cerrado, y la expresion solo tiene epsilon, terminamos el ciclo
        if (not value) and (expresion == EPSILON):
            break

        # si el contador se acaba terminamos el prcesos copiamos los datos a la lista
        current_node = value.copy()
        if i > len(expresion)-1:
            break
    # recorremos la lista, para ver si son aceptados o no
    for node in current_node:
        if automata.states[node].accept == True:
            return 'Si'
    return 'No'
    