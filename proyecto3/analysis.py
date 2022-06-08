import pprint
'''
ARCHIVO PARA ANALIZAR LAS EVALUACIONES REALIZADAS
'''
from Thompson.test_expre import regex_tree
from dfaDir.dfaDir_ import sintetic_tree, simulate_dfa_direct
from parser_decom import parser


OPERATORS = ['|', 'ξ']
EPSILON  = "ε"

def arrgl(string):
    arrayOfLines = string.split("\n")
    arrayOfLines2 = []
    flag = False

    for index in range(0, len(arrayOfLines)):
        if flag == True:
            if arrayOfLines[index] != "":
                arrayOfLines2.append(arrayOfLines[index])
            else:
                arrayOfLines2.append("\t\treturn resultado\n")
                flag = False

        if "def" in arrayOfLines[index] and "resultado" in arrayOfLines[index]:
            arrayOfLines2.append(arrayOfLines[index])
            flag = True

        if flag == False and ("def" in arrayOfLines[index] and "resultado" in arrayOfLines[index]) == False:
            arrayOfLines2.append(arrayOfLines[index])
    string2 = ""

    for ele in arrayOfLines2:
        string2 += ele + "\n"

    return string2

def analyze(name, characters, keywords, tokens, productions):
    # obtenemos los valores de characters
    character_parse = read_characters(characters)
    print(character_parse)

    # obtenemos los valores de los keywords
    keyword_parse = read_keywords(keywords)
    print(keyword_parse)

    # obtenemos los valores de los tokens
    token_parse = read_tokens(tokens, character_parse)
    print(token_parse)
    
    automata_dfa, string = scanner_data(keyword_parse, token_parse)

    # obtenemos los datos con los producciones correctas
    parser_line, complete_tokens = parser(productions, string, tokens, keywords)

    # creamos el automata que estara utilizando
    dfa = make_automata_automatic(complete_tokens)

    return dfa, automata_dfa, parser_line

def read_characters(characters):
    # guardamos en un diccionarios los characters
    character_parse_line = {}
    for c in characters:
        temp_string = ""
        flag = False
        i = 0
        string_to_parse = ""
        while i < len(characters[c]):
            if characters[c][i] == '"' or characters[c][i] == "'":
                flag = not flag
                if not flag:
                    temp_string = temp_string[:-1] + ")"
                    string_to_parse += temp_string 
                    temp_string = ""
                else:
                    temp_string += "("
            elif flag:
                temp_string += characters[c][i] + "|"
            elif characters[c][i] == "+":
                string_to_parse += "|"
            elif temp_string + characters[c][i] in character_parse_line:
                string_to_parse += character_parse_line[temp_string+characters[c][i]]
                temp_string = ""
            elif temp_string == ".":
                if characters[c][i] == ".":
                    start = string_to_parse[-2]
                    finish = ""
                    while i < len(characters[c]):
                        if characters[c][i] == "'":
                            break
                        i += 1
                    finish = characters[c][i + 1]
                    j = ord(start)
                    while j < ord(finish):
                        string_to_parse += "|" + chr(j)
                        j += 1
                    string_to_parse += "|" + finish

            elif temp_string == "CHR(":
                number = ""
                while i < len(characters[c]):
                    if characters[c][i] == ")":
                        break
                    elif characters[c][i] == " ":
                        pass
                    else:
                        number += characters[c][i]
                    i += 1
                number = int(number)
                symbol = chr(number)
                string_to_parse += "'"+symbol+"'"
                temp_string = ""
            else:
                temp_string += characters[c][i]
            i += 1
        character_parse_line[c] = "(" +  string_to_parse + ")"
    return character_parse_line

def read_keywords(keywords):
    keyword_parse = {}
    for k in keywords:
        word = keywords[k][:-1]
        i = 0
        temp = ""
        flag = False
        while i < len(word):
            if word[i] == '"':
                flag = not flag
                if not flag:
                    temp = temp[:-1] +  ")"
                else:
                    temp += "("
            else:
                temp += word[i] + "ξ"
            i += 1
        keyword_parse[k] = temp
    return(keyword_parse)

def compiler(line, characters, i=0, data=''):
    ''' datos iniciales para el compilador '''
    # igualamos los contadores
    temp = data
    i += 1
    data_value = [data]
    while i < len(line):
        temp += line[i]
        if temp in characters:
            data_value.append(temp)
        i += 1
    max_value = max(data_value, key = len)
    # retornamos cada identificador de los diccionarios utilizados
    return max_value

def read_tokens(tokens, characters):
    # guardamos los tokens en un diccionario
    tokens_parse_lines = {}
    for t in tokens:
        token = tokens[t]
        i = 0
        temp = ""
        parse_line = ""
        flag = False
        while i < len(token):
            temp += token[i]
            if temp in characters:
                og = temp
                temp = compiler(token, characters, i, temp)
                #print(temp)
                if og != temp:
                    i += len(temp) - len(og)
                if flag:
                    parse_line += characters[temp] + ")*"
                else:
                    parse_line += characters[temp]
                temp = ""
            if "|" == temp:
                parse_line = parse_line[:-2] + "|"
                temp = ""
            if temp == "{":
                flag = not flag
                parse_line += "ξ("
                temp = ""
            if temp == "}" and flag:
                flag = not flag
                temp = ""
            if temp == "[":
                second_flag = True
                if parse_line != "":
                    parse_line += "ξ"
                parse_line += "("
                temp = ""
            if temp == "]":
                second_flag = False
                parse_line += "?"
                temp = ""
            if temp == '"':
                inner = ""
                i += 1
                while i < len(token):
                    if token[i] == '"':
                        break
                    inner += token[i]
                    i += 1
                if parse_line != "" :
                    parse_line += "ξ(" + inner + ")"
                else:
                    parse_line += "(" + inner + ")"
                if token[i + 1] != "" and token[i + 1] != "\n" and token[i + 1] != ".":
                    parse_line += "ξ"
                temp = ""
            if temp == "(":
                parse_line += "("
                temp = ""
            if temp == ")":
                parse_line += ")"
                temp = ""
            i += 1
        if parse_line[-1] in OPERATORS:
            parse_line = parse_line[:-1]
        tokens_parse_lines[t] = parse_line
    return tokens_parse_lines
            
def scanner_data(keyword_parse, token_parse):
    string = ""
    # los automatas creados, se guardaran en un diccionario
    automata_dfa = {}

    # recorremos cada uno de los diccionarios, para analizarlos y crear el automata. 
    for keyword in keyword_parse:
        # obtenemos el regex con los keywords
        string += "(" + keyword_parse[keyword] + ")" + "|"
        
        # evaluamos el regex obtenido
        tree = regex_tree(keyword_parse[keyword])

        # creamos el automata con el algoritmo de creacion de dfa directo
        automata_dfa[keyword] = sintetic_tree(tree, keyword_parse[keyword])

    for token in token_parse:
        # obtenemos el regex con los tokens 
        string += "(" + token_parse[token] +")" + "|"
        
        # evaluamos el regex obtenido
        tree = regex_tree(token_parse[token])
        
        # creamos el automata, por medio del regex que se evaluo. 
        automata_dfa[token] = sintetic_tree(tree, token_parse[token])

    string = string[:-1]
    tree = regex_tree(string)
    return automata_dfa, string

def make_automata_automatic(string):
    tree = regex_tree(string)
    # automata dfa direct, con el regex obtenido
    dfa = sintetic_tree(tree, string)
    return dfa

def terminacion_compilador(file, automata, count = 0):
    temp = ''
    simbolos_validos = []
    while count < len(file):
        temp += file[count]
        if simulate_dfa_direct(automata, temp):
            simbolos_validos.append(temp)
        elif len(temp) == 1  and simulate_dfa_direct(automata, str(ord(temp))):
            simbolos_validos.append(temp)
        count += 1
        if simbolos_validos:
            return max(simbolos_validos, key = len)
    return False