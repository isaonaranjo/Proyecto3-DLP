from operator import itemgetter
from Thompson.test_expre import EPSILON, flat

def get_operation(expresion, node=2):
    i = 0
    final_state = []
    handler = []

    while i < len(expresion):
        # Se realiza las operaciones del OR 
        if expresion[i] == "|":
            s0 = handler[-1]
            handler.pop()
            s1 = handler[-1]
            handler.pop()
            handler.append([s0, s1, [node,EPSILON, final_state[-2][0]], [node,EPSILON,final_state[-1][0]], [final_state[-2][1], EPSILON, node+1], [final_state[-1][1], EPSILON, node+1]])
            initial = node
            final = node +1
            node +=2
            final_state.pop()
            final_state.pop()
            final_state.append([initial,final])
        
        # Se realiza la funcion de Kleene
        elif expresion[i] == "*":
            initial = final_state[-1][0]
            final = final_state[-1][1]
            x = [node, EPSILON, initial]
            y = [final, EPSILON, initial]
            initial = node
            node +=1
            z = [final, EPSILON, node]
            k = [initial, EPSILON, node]
            final = node
            v = handler[-1]
            handler.pop()
            handler.append([v,x,y,z,k])
            final_state.pop()
            final_state.append([initial, final])
            node += 1
        
        # Se realiza la concatenacion
        elif expresion[i] == " ":
            first = handler[-1]
            handler.pop()
            second_expresion = handler[-1]
            handler.pop()
            final_sorted = final_state[-1]
            final_state.pop()
            get_final_sorted = final_state[-1]
            final_state.pop()
            try:
                second_expresion = flat(second_expresion, [])
                for a in range(len(second_expresion)):
                    for n in range(0,3):
                        if second_expresion[a][n] == get_final_sorted[1]:
                            second_expresion[a][n] = final_sorted[0]
            except:
                for a in range(len(second_expresion)):
                    if second_expresion[a] == get_final_sorted[1]:
                        second_expresion[a] = final_sorted[0]
            
            final_state.append([get_final_sorted[0], final_sorted[1]])
            handler.append([second_expresion, first])
        
        # si no hay ninguna operacion
        elif expresion[i] != " " and expresion[i] != "|" and expresion[i] != "*" :
            handler.append([node, expresion[i], node+1])
            final_state.append([node, node +1])
            node +=2
        
        i+=1

    resultado = sorted(flat(handler,[]), key= itemgetter(0))
    return resultado, final_state

def delete_parentesis(expresion):
    i = 0
    while (i<len(expresion)):
        if expresion[i] == '(':
            expresion.pop(i)
            i -= 1
        i += 1