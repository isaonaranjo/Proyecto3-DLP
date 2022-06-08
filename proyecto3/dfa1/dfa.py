'''
    M. Isabel Ortiz
    Convert Nodeterministic finite automatan (NFA) to Deterministic finite automatan (DFA)
'''

from Thompson.test_expre import EPSILON, OPERATORS

# funcion de epsilon lock del primer nodo
def ecerradura_node(node, automata):
    node =[]
    node.append(nodo)
    move = possible_move(nodo, EPSILON, automata)
    for x in move:
        if x[2] not in node:
            node.append(x[2])
    s = set()
    # chequeamos la clase de datos que tenemos
    if isinstance(node,list):
        for item in node:
            s.add(item)
        return s
    else:
        s.add(node)

# funcion que devuelve los posibles movementss
def possible_move(node, expresion, automata):
    moves = []
    for n in automata:
        if (n[0] == node) and (n[1] == str(expresion)):
            moves.append(n)
    return moves

# funcion ecerradura que indica el libro de texto
def ecerradura(x, automata):
    if isinstance(x, int):
        node = []
        node.append(x)
    else: 
        node = list(x)
    if isinstance(node, list):
        for n in node:
            move = possible_move(n, EPSILON, automata)
            for x in move:
                if x[2] not in node:
                    node.append(x[2])
    # encontramos el nodo actual
    current_node = set()
    for item in node:
        current_node.add(item)
    return current_node

# funcion para indicar hacia donde se mueve cada uno de los estados que se proporciona
def move(nodes, expresion, automata):
    nodes = list(nodes)
    movements = []
    # verificamos los datos
    if isinstance(nodes, list):
        # ciclo para encontrar cada uno de los nodos, y mandarlos hacia la funcion del movimientos
        for n in range(len(nodes)):
            move = possible_move(nodes[n], expresion, automata)
            for x in move:
                if x[2] not in movements:
                    movements.append(x[2])
        current_node = set()
        # encontramos el nodo actual
        for item in movements:
            current_node.add(item)
        return current_node
    
    else:
        # si solo es un nodo, y no es una lista
        move = possible_move(nodes, expresion, automata)
        for x in move:
            if x[2] not in movements:
                movements.append(x[2])
        # encontramos el nodo actual
        current_node = set()
        for item in movements:
            current_node.add(item)
        return current_node

def moving(nodes, expresion, automata):
    if isinstance(nodes, list):
        nodes = list(nodes)
    else:
        nodes = [nodes]

    movements = []
    # verificamos los datos
    if isinstance(nodes, list):
        # ciclo para encontrar cada uno de los nodos, y mandarlos hacia la funcion del movimientos
        for n in range(len(nodes)):
            moves = possible_move(nodes[n], expresion, automata)
            for x in moves:
                if x[2] not in movements:
                    movements.append(x[2])
        current_node = set()
        # encontramos el nodo actual
        for item in movements:
            current_node.add(item)
        return current_node
    
    else:
        # si solo es un nodo, y no es una lista
        moves = possible_move(nodes, expresion, automata)
        for x in moves:
            if x[2] not in movements:
                movements.append(x[2])
        # encontramos el nodo actual
        current_node = set()
        for item in movements:
            current_node.add(item)
        return current_node

def subset(transitions, state):
    # encontramos los simbolos para hacer las transiciones
    symbols = []
    for i in range(len(transitions)):
        if transitions[i][1] != EPSILON:
            if transitions[i][1] not in symbols:
                symbols.append(transitions[i][1])

    # contador de las transiciones
    i = 0
    # lista de los estados
    Dstate =[]
    # guardamos los estados encontrados
    data_state = []
    Dstate.append(ecerradura(state[0][0], transitions))
    # si encuentra nuevos estados
    new_state =[]
    new_state.append(ecerradura(state[0][0], transitions))
    
    # implementacion de algoritmo del libro
    while i < len(Dstate):
        for n in symbols:
            u = ecerradura(move(Dstate[i],n,transitions), transitions)
            data_state.append([Dstate[i],n,u])
            for w in state:
                if w[1] in u:
                    new_state.append(u)
            if u not in Dstate and u is not None:
                Dstate.append(u)         
        i+=1
    
    # Editamos lo que nos devuelve ya que tenemos vacios
    x = 0
    while x < len(data_state):
        if data_state[x][0] == set() or data_state[x][2] == set():
            data_state.pop(x)
            x-=1
            
        x +=1
    
    yes = ["A","B","C","D","E","F","G","H","I","J","k","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z",
            "AA","BB","CC","DD","EE","FF","GG","HH","II","JJ","KK", "LL", "MM", "NN", "OO", "PP", "QQ", "RR", "SS",
            "TT", "QQ", "RR", "SS", "TT", "UU", "VV", "WW", "XX", "YY", "ZZ"]
    
    numbers = [1,2,3,4,5,6,7,8,9]
    alphabet = []

    for j in range(len(numbers)):
        for k in range(len(yes)):
            data_crack = str(yes[k]) + str(numbers[j])
            # print(ooo)
            alphabet.append(data_crack)
    
    x = 0 
    while x < len(data_state):
        index_state = Dstate.index(data_state[x][0])
        data_state[x][0] = alphabet[index_state]
        index_state = Dstate.index(data_state[x][2])
        data_state[x][2] = alphabet[index_state]
        x +=1
    x = 0
    
    while x < len(new_state):
        index_state = Dstate.index(new_state[x])
        new_state[x] = alphabet[index_state]
        x += 1
    new_node = []
    
    for i in range(1, len(new_state)):
        new_node.append([new_state[0],new_state[i]])
    return data_state, new_node

# return the regular expresion
def get_symbol(automata):
    data_symbol = []
    for symbol in automata.expresion:
        if (symbol not in OPERATORS) and (symbol not in data_symbol) and (symbol != EPSILON):
            data_symbol.append(symbol)
    return data_symbol
