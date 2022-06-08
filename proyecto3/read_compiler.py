from utils import read_str

def read_file(direction):
    list_data =  ['CHARACTERS', 'KEYWORDS', 'PRODUCTIONS']
    i = 0
    # guardamos los datos especificos en una lista correspondiente, estas son las que se requeriran para le creacion
    characters = []
    keywords = []
    tokens = []
    productions = []

    line = ""
    while i < len(direction):
        line, i = read_str(direction, i)
        print(line)
        # si encuentra la palabra COMPILER, data es el nombre del archivo
        if line == "COMPILER":
            data, i = COMPILER(direction, i)
        # si encuentra la palabra CHARACTERS
        if line == "CHARACTERS":
            characters, i = CHARACTERS(direction, i)
        # si encuentra la palabra KEYWORDS
        if line == "KEYWORDS":
            keywords, i = KEYWORDS(direction, i)
        # si encuentra la palabra TOKENS
        if line == "TOKENS":
            tokens, i = TOKENS(direction, i)
        # si encuentra la palabra PRODUCTIONS
        if line == "PRODUCTIONS":
            productions, i = PRODUCTIONS(direction, i)
        # si encuentra la palabra END indica la finalizacion del doc
        if line == "END":
            final = END(direction, i, data)
            if final:
                break
            else:
                break
        
    return data, characters, keywords, tokens, productions

# revisa si char | "CHR", es booleano solo para verificar que se encuentre
def evaluate_char(data):
    if ('chr(' in data) or ('CHR(' in data):
        return True
    else:
        return False

# obtenemos el encabezado del documento
def COMPILER(filename, i):
    i += 1 
    data, i = read_str(filename, i)
    return data, i

def CHARACTERS(filename, i):
    # sumamos uno al contador
    i += 1
    temp = ""
    # guardamos en un diccioanrio los characters
    characters = {}

    # variables que sirven para leer e identifcar las lineas encontradas
    temp_id = ""
    temp_values = ""
    line = ""

    while True:
        temp, i = read_str(filename, i) 
        if temp == "KEYWORDS":
            i -= 8
            break
        line += temp
        if line[-1] == "." and line[-2] != ".":
            if "=" in line:
                lines_complete = line.split("=")
                # obtenemos el id de los characters
                temp_id = lines_complete[0]
                # obtenemos los valores de los characters
                temp_values = lines_complete[1]
                print('ID: %s ---> VALUES: %s ' % (temp_id, temp_values))
                characters[temp_id] = temp_values
                line =  ""
            else:
                print("HAY UN ERROR EN EL ARCHIVO")
    return characters, i

def KEYWORDS(filename, i):
    # sumamos uno al contador
    i += 1
    temp = ""

    # guardamos en un diccioanrio los KEYWORDS
    keywords = {}

    temp_id = ""
    temp_values = ""
    line = ""

    while True:
        temp, i = read_str(filename, i) 
        if temp == "TOKENS":
            i -= 6
            break
        line += temp
        # si encuentra un .
        if line[-1] == ".":
            if "=" in line:
                lines_complete = line.split("=")
                # obtenemos el id de los characters
                temp_id = lines_complete[0]
                # obtenemos los valores de los characters
                temp_values = lines_complete[1]
                print('ID: %s ---> VALUES: %s ' % (temp_id, temp_values))
                keywords[temp_id] = temp_values
                line =  ""
            else:
                print("HAY UN ERROR EN EL ARCHIVO")
    return (keywords, i)

def TOKENS(filename, i):
    # sumamos uno al contador
    i += 1
    temp = ""

    # guardamos en un diccioanrio los TOKENS
    tokens = {}

    temp_id = ""
    temp_values = ""
    line = ""

    while True:
        temp, i = read_str(filename, i) 
        if temp == "PRODUCTIONS":
            i -= 11
            break
        if temp == "END":
            i -= 3
            break
        line += temp
        if line[-1] == ".":
            if "=" in line:
                lines_complete = line.split("=")
                # obtenemos el id de los characters
                temp_id = lines_complete[0]
                # obtenemos los valores de los characters
                temp_values = lines_complete[1]
                print('ID: %s ---> VALUES: %s ' % (temp_id, temp_values))
                tokens[temp_id] = temp_values
                line =  ""
            else:
                print("HAY UN ERROR EN EL ARCHIVO")
    return tokens, i

def PRODUCTIONS(filename, i):
    # sumamos uno al contador
    i += 1
    temp = ""

    # guardamos en un diccioanrio los PRODUCTIONS
    productions = {}
    temp_id = ""
    temp_values = ""

    while i < len(filename):
        temp += filename[i]
        if temp[-1] == "."  and temp[-2] != "(" and (filename[i + 1] == " " or filename[i+1] == "\n"):
            temp_id = temp.split("=", 1)[0]
            temp_values = temp.split("=", 1)[1]
            # print('ID: %s ---> VALUES: %s ' % (temp_id, temp_values))
            productions[temp_id] = temp_values
            temp = ""
        if "\nEND" in temp:
            i -= 3
            temp = ""
            break
        i += 1
    return productions, i

def END(filename, i, data):
    i += 1
    end_data, i = read_str(filename, i)
    if end_data == data:
        return True
    return False