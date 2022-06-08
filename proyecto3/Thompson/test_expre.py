'''
 Reference https://medium.com/swlh/visualizing-thompsons-construction-algorithm-for-nfas-step-by-step-f92ef378581b
'''
from dfaDir.structure import Automata
from dfaDir.structure import Handler
from dfaDir.structure import State
from dfaDir.tree import Tree
from dfaDir.cal import OPERATORS

EPSILON = "ε" 
OPERATORS = ['|', '*', 'ψ', '?', 'ξ', ')', '(']
SPECIAL = ['*', 'ψ', '?']

# funcion para las predencias de la expresion
def predence(operation):
    if (operation == '*'):
        return 3
    if (operation == '|'):
        return 2
    if (operation == " "):
        return 1
    if (operation == "("):
        return 3
    else:
        return 0

# funcion para cambiar de lista a string
def list_to_string(cadena):
    expresion = ''
    for i in range(0, len(cadena)):
        expresion = expresion + str(cadena[i])
    return expresion

# funcion para cambiar de string a lista
def string_to_list(cadena):
    i = 0
    expresion = []
    while (i<len(cadena)):
        expresion.append(cadena[i])
        i += 1
    return expresion

# devuelve las transciones quitando el parentesis
def flat(l, a):
    x = []
    for i in l:
        if isinstance(i, list):
            flat(i, a)
        else:
            a.append(i)

    for i in range(0,len(a),3):
        if i != len(a):
            x.append([a[i],a[i+1],a[i+2]])
    
    return x

# cambia la expresion
# ? = |EPSILON       
# a+ = aa* 
def change_data(cadena):
    stack = []
    value = []
    count = 0

    for n in cadena:
        if n != "?" and n != "+":
            stack.append(n)  
        if n == "?" or n == "+":
            count += 1
            if (n == "?" and stack[-1] != ")") or (n == "+" and stack[-1] != ")"):
                count += 1
                x = True
                z = len(stack)-1
                while x == True and z != -1:
                    if stack[z] == ")" or stack[z] == " ":
                        stack.pop()
                        x = False
                    else:
                        value.append(stack[z])
                        stack.pop()
                    z-=1
                if n == "?":
                    count += 1
                    stack.append(' ')
                    stack.append('(')
                    for i in value[::-1]:
                        stack.append(i)
                    stack.append('|')
                    stack.append(EPSILON)
                    stack.append(')')
                    #stack.append(str("("+list_to_string(value[::-1])+"|"+EPSILON+")"))
                elif n == "+":
                    count +=1
                    stack.append(' ')
                    stack.append('(')
                    for i in value[::-1]:
                        stack.append(i)
                    stack.append(')')
                    stack.append(' ')
                    stack.append('(')
                    for i in value[::-1]:
                        stack.append(i)
                    stack.append('*')
                    stack.append(')')
                    #stack.append(str("("+list_to_string(value[::-1])+").("+list_to_string(value[::-1])+"*)"))
                value = []
            else: 
                v = len(stack)-1
                z = True
                while z == True:
                    if stack[v] == "(" :
                        value.append("(")
                        stack.pop()
                        z = False
                    else:
                        value.append(stack[v])
                        stack.pop()
                    v-=1
                if n == "?":
                    count += 1
                    stack.append(' ')
                    stack.append('(')
                    for i in value[::-1]:
                        stack.append(i)
                    stack.append('|')
                    stack.append(EPSILON)
                    stack.append(')')
                    #stack.append(str("("+list_to_string(value[::-1])+"|"+EPSILON+")"))

                elif n == "+":
                    count +=1
                    stack.append(' ')
                    stack.append('(')
                    for i in value[::-1]:
                        stack.append(i)
                    stack.append(')')
                    stack.append(' ')
                    stack.append('(')
                    for i in value[::-1]:
                        stack.append(i)
                    stack.append('*')
                    stack.append(')')
                    #stack.append(str("("+list_to_string(value[::-1])+").("+list_to_string(value[::-1])+"*"))
                value = []
    i = 0
    exp = string_to_list(stack)
    if exp[0] == " ":
        exp.pop(0)
    
    return list_to_string(exp)

def regex(cadena):
    # operadores validos
    OPERATORS  = ["|", "*", " "]
    # stack
    stack = []
    # output
    value = []
    i = 0
    letter = []

    while i < len(cadena):
        if cadena[i] == "(":
            stack.append(cadena[i])

        elif cadena[i] == ")":
            x = len(stack) - 1
            while stack[x] != "(":
                if len(letter) != 0:
                    value.append(list_to_string(letter))
                    letter = []
                value.append(stack[x])
                stack.pop()
                x -= 1
            stack.pop()

        elif cadena[i] in OPERATORS :
            if len(stack) == 0:
                stack.append(cadena[i])
                if len(letter) != 0:
                    value.append(list_to_string(letter))
                    letter = []
            else:
                if stack[-1] != '(':
                    if predence(cadena[i]) < predence(stack[-1]):
                        z = len(stack) - 1
                        if z != 0:
                            while stack[z] != '(':
                                if len(letter) != 0:
                                    value.append(list_to_string(letter))
                                    letter = []
                                
                                value.append(stack[-1])
                                stack.pop()
                                z -= 1
                            stack.append(cadena[i])
                        else:
                            if len(letter) != 0:
                                value.append(list_to_string(letter))
                                letter = []
                            value.append(stack[-1])
                            stack.pop()
                            stack.append(cadena[i])
                    elif predence(cadena[i]) >= predence(stack[-1]):
                        if len(letter) != 0:
                            value.append(list_to_string(letter))
                            letter = []
                        stack.append(cadena[i])
                else:
                    if len(letter) != 0:
                        value.append(list_to_string(letter))
                        letter = []
                    stack.append(cadena[i])
        else:
            value.append(cadena[i])
        # contador
        i += 1

    if len(letter) != 0:
        value.append(list_to_string(letter))
        letter = []
        
    if len(stack) != 0:
        for i in range(len(stack)):
            value.append(stack[-1])
            stack.pop()
    return value

def regex_tree(expresion):
    values = []
    operation = []
    # counter
    i = 0
    while (i < len(expresion)):
        # there is space
        if (expresion[i] == ' '):
            i += 1
            continue
        # there is open parentesis
        elif (expresion[i] == "("):
            operation.append(expresion[i])
        
        elif (expresion[i] not in OPERATORS):
            val = ""
            while (i < len(expresion)) and expresion[i] not in OPERATORS:
                val = str(val) + expresion[i]
                i -= -1
            # take the class of tree
            tree = Tree()
            tree.data = val
            # append to list data of the tree
            values.append(tree)
            i -= 1
            
        # there is close parentesis
        elif expresion[i] == ")":
            while len(operation) != 0 and operation[-1] != "(":
                val2 = values.pop()
                val1 = values.pop()
                op = operation.pop()
                # take the class of tree
                tree = Tree()
                tree.data = op
                tree.left = val1
                tree.right = val2
                # add the data to list
                values.append(tree)
            operation.pop()

        # expresion[i] == '('
        else:
            if (expresion[i] in SPECIAL):
                op = expresion[i]
                val = values.pop()
                # take the class of tree
                tree = Tree()
                tree.data = op
                tree.left = val
                tree.right = None
                # add the data to list
                values.append(tree)
            else:
                while (len(operation) != 0  and operation[-1] != '('):
                    op = operation.pop()
                    val2 = values.pop()
                    val1 = values.pop()
                    # take the class of tree
                    tree = Tree()
                    tree.data = op
                    tree.left = val1
                    tree.right = val2
                    # add the data to list
                    values.append(tree)
                operation.append(expresion[i])
        
        i -= -1
    
    # if no empty the list 
    while(len(operation) != 0):
        val2 = values.pop()
        val1 = values.pop()
        op = operation.pop()
        # take the class of tree
        tree = Tree()
        tree.data = op
        tree.left = val1
        tree.right = val2
        # add the data to list
        values.append(tree)
        if (len(values) == 1):
            return values[-1]

    return values[-1]