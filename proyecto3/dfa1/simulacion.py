from dfa1.dfa import move, possible_move, moving
from Thompson.test_expre import EPSILON

def simulate_nfa(expresion, automata, node):
    automata.append([node[0][1]+1, EPSILON, node[0][1]])
    node = [[node[0][1]+1, node[0][1]]]
    states = []
    for i in range(len(automata)):
        # si no encuentra en los primeros datos los estados
        if automata[i][0] not in states:
            states.append(automata[i][0])
        
        # si no encuentra en los segundos datos de los estados
        if automata[i][2] not in states:
            states.append(automata[i][2])
    
    # ciclo para agregar los datos
    for i in states:
        automata.append([i, EPSILON, i])

    # contadores para los ciclos
    x = 0
    a = 0
    inicial_state =[]
    inicial_state.append(node[0][0])
    x = found_epsilon(expresion[0], automata, node[0])
    current_node = set(node[0])
  
    for i in range(len(expresion)):
        x = found_epsilon(expresion[i], automata, list(current_node))
        m = 0
        while m < len(x):
            x  = list(x)
            current_node = move([x[m]],expresion[i],automata)
            m += 1
    
    # indicamos SI si pertenece al alphabeto o NO
    if found_final_state(list(current_node)[0], automata, node) == 'SI' or change_state(expresion, automata, node) == 'SI':
        return 'SI'
    else:
        return 'NO'

# funcion para encontrar los epsilon en las transiciones
def found_epsilon(expresion, automata, node):
    y = move([node[0]], EPSILON, automata)
    x = []
    y = list(y)
    
    # contador de ciclo
    i = 0
    while i < len(y):
        new_state = list(move([y[i]], EPSILON, automata))
        x.append([y[i], EPSILON, move([y[i]], EPSILON, automata)])
        x.append([y[i], expresion, move([y[i]], expresion, automata)])
        if len(new_state)>0:
            for u in range(len(new_state)):
                if new_state[u] not in y:
                    y.append(new_state[u])
        i+=1

    positions = []
    for i in range(len(y)):
        if len(move([y[i]], expresion, automata)) > 0:
            positions.append(y[i])
        
    positions = set(positions)
    # split de los primeros estados
    x = x[::-1]
    a = 0
    while a < len(positions):
        for i in range(len(x)):
            if len(positions.intersection(x[i][2])) > 0:
                positions.add(x[i][0])     
        a+=1

    return positions

def change_state(expresion, automata, node):
    state = []
    for i in range(len(automata)):
        if automata[i][0] not in state:
            state.append(automata[i][0])
                
        if automata[i][2] not in state:
            state.append(automata[i][2])
        
    alphabet = ["A","B","C","D","E","F","G","H","I","J", "K", 'L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z','AA','BB','CC','DD']
    x = 0 

    while x < len(automata):
        new_index = state.index(automata[x][0])
        automata[x][0] = alphabet[new_index]
        new_index = state.index(automata[x][2])
        automata[x][2] = alphabet[new_index]
        x +=1    
    x = 0

    # cambiamos el estado final y el inicial
    inicial_node = [0,0]
    while x < len(node[0]):
        new_index = state.index(node[0][x])
        inicial_node[x]= alphabet[new_index]
        x += 1
    y = []
    
    x = 0
    a = 0
    inicial =[]
    inicial.append(inicial_node[0][0])
    x = found_epsilon(expresion[0], automata, inicial_node[0])
  
    current_node = set(inicial_node[0])
    m = 0
    for i in range(len(expresion)):
        x = found_epsilon(expresion[i], automata, list(current_node))
        m = 0
        while m < len(x):
            x  = list(x)
            current_node = move([x[m]], expresion[i], automata)
            m += 1
    try: 
        if simulate_dfa(expresion, automata, [inicial_node]) == 'SI':
            return 'SI'
    except:
        print('')

# indica si existe en nuestro lenguaje (automata)
def simulate_dfa(expresion, automata, node):
    i = 0
    inicial_node = node[0][0]
    
    for n in expresion:
        x = moving(inicial_node, n, automata)
        # si es la longitud es cero entonces no pertenece
        if len(x) == 0:
            return 'NO'
        x = list(x)
        inicial_node = x[0]
    i = 0 
    for n in range(len(node)):
        if inicial_node == node[n][1]:
            i += 1
    #d devuelve si o no dependiendo de la longitud de la cadena
    if i !=0:
        return 'SI'
    else:
        return 'NO'

def found_final_state(expresion, automata, node):
    x = possible_move(expresion, EPSILON, automata)
    i = 0
    while i < len(x):
        a = possible_move(x[i][2], EPSILON, automata)
        for m in range(len(a)):
            if a[m] not in x:
                x.append(a[m])
        i+=1
        
    l = 0
    for i in range(len(x)):
        if x[i][2] == node[0][1]:
            l += 1

    if l >0:
        return 'SI'
    else:
        return 'NO'

