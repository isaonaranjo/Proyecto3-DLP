EPSILON = 'ε'
OPERATORS = ['|', '*', 'ψ', '?', 'ξ', ')', '(']

# found the epsilon into tree
def states_tree(tree):
    nodes = []
    if (tree.data not in OPERATORS) and (tree.data != EPSILON) and (tree.left == None) and (tree.right == None):
        nodes.append(tree)
    if (tree.left != None):
        resp = states_tree(tree.left)
        for i in resp:
            nodes.append(i)
    if (tree.right != None):
        resp = states_tree(tree.right)
        for i in resp:
            nodes.append(i)
    return nodes

# nullable reference table 3.58
def nullable(tree):
    # chech the tree
    if (tree.data == EPSILON):
        return True
    # chech n = c1|c2
    elif (tree.data == '|'):
        c1 = tree.left
        c2 = tree.right
        if nullable(c1) or nullable(c2):
            return True
    # n = c1*
    elif (tree.data == '*'):
        return True
    # n = c1.c2
    elif (tree.data == 'ξ'):
        c1 = tree.left
        c2 = tree.right
        if nullable(c1) and nullable(c2):
            return True
        else:
            return False
    # n+
    elif (tree.data == 'ψ'):
        c1 = tree.left
        if nullable(c1):
            return True
        else:
            return False
    # n?
    elif (tree.data == '?'):
        return True
    return False

# firstpos in table 3.58 
def firstpos(tree):
    position = []
    if (tree.data in OPERATORS):
        # n = c1.c2
        if (tree.data == 'ξ'):
            val = firstpos(tree.left)
            for i in val:
                position.append(i)
            if nullable(tree.left):
                c2 = firstpos(tree.right)
                for i in c2:
                    position.append(i)
        # n = c1*
        elif (tree.data == '*'):
            val = firstpos(tree.left)
            for i in val:
                position.append(i)
        # n = c1|c2
        elif (tree.data == '|'):
            c1 = firstpos(tree.left)
            c2 = firstpos(tree.right)
            for i in c1:
                position.append(i)
            for i in c2:
                position.append(i)
        # n+
        elif (tree.data == 'ψ'):
            c1 = firstpos(tree.left)
            for i in c1:
                position.append(i)
        # n?
        elif (tree.data == '?'):
            c1 = firstpos(tree.left)
            for i in c1:
                position.append(i)
    elif tree.data != EPSILON:
        position.append(tree)
    return position

# no change with firstopos only interchange the childrens
def lastpos(tree):
    position = []
    if (tree.data in OPERATORS):
        # n = c1.c2
        if (tree.data == 'ξ'):
            val = lastpos(tree.right)
            if nullable(tree.right):
                c2 = lastpos(tree.left)
                for i in c2:
                    position.append(i)
            for i in val:
                position.append(i)
        # n = c1*
        elif (tree.data == '*'):
            val = lastpos(tree.left)
            for i in val:
                position.append(i)
        # n = c1 | c2
        elif (tree.data == '|'):
            c1 = lastpos(tree.left)
            c2 = lastpos(tree.right)
            for i in c1:
                position.append(i)
            for i in c2:
                position.append(i)
        # n+
        elif (tree.data == 'ψ'):
            c1 = lastpos(tree.left)
            for i in c1:
                position.append(i)
        # n?
        elif (tree.data == '?'):
            c1 = lastpos(tree.left)
            for i in c1:
                position.append(i)
    elif (tree.data != EPSILON):
        position.append(tree)
    return position

# followpos reference book table 3.9.4
def followpos(tree, table):
    if (tree.data == 'ξ'):
        c1 = lastpos(tree.left)
        c2 = firstpos(tree.right)
        for i in c1:
            for j in c2:
                table[i].append(j)
    elif (tree.data == '*'):
        c1 = lastpos(tree)
        c2 = firstpos(tree)
        for i in c1:
            for j in c2:
                table[i].append(j)
    elif (tree.data == 'ψ'):
        c1 = lastpos(tree.left)
        c2 = firstpos(tree.left)
        for i in c1:
            for j in c2:
                table[i].append(j)

    if (tree.left != None):
        followpos(tree.left, table)
    if (tree.right != None):
        followpos(tree.right, table)


