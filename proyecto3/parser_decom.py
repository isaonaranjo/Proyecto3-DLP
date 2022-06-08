# File for productions only

OPS  = ["[", "{", "|", "("]
OPERATORS = ['|', '*', '+', '?', '^', ')', '(']

def parser(productions, parse_line, tokens, keywords):
    # creamos una archivo de producciones
    file = open("./Outputs/producciones.py", 'w+')
    string = "class Production_Parse:\n"

    string += "\tdef __init__(self, tokens):\n"
    string += "\t\tself.tokens = tokens\n"
    string += "\t\tself.counter_tokens = 0\n"
    string += "\t\tself.first_token = self.tokens[self.counter_tokens]\n"
    string += "\t\tself.final = ''\n\n"

    string += "\tdef sig(self):\n"
    string += "\t\tself.counter_tokens += 1\n"
    string += "\t\tif self.counter_tokens < len(self.tokens):\n"
    string += "\t\t\tself.first_token = self.tokens[self.counter_tokens]\n"
    string += "\t\t\tself.final = self.tokens[self.counter_tokens - 1]\n\n"

    string += "\tdef simulate(self, item, arg = None):\n"
    string += "\t\tcounter_tokens = self.counter_tokens\n"
    string += "\t\tpossible = False\n"
    string += "\t\tif item != None:\n"
    string += "\t\t\ttry:\n"
    string += "\t\t\t\tif arg == None:\n"
    string += "\t\t\t\t\tans = item()\n"
    string += "\t\t\t\telse:\n"
    string += "\t\t\t\t\tans = item(arg)\n"
    string += "\t\t\t\t# si es booleano\n"
    string += "\t\t\t\tif type(ans) == bool:\n"
    string += "\t\t\t\t\tpossible = ans\n"
    string += "\t\t\t\telse:\n"
    string += "\t\t\t\t\tpossible = True\n"
    string += "\t\t\texcept:\n"
    string += "\t\t\t\tpossible = False\n"
    string += "\t\tself.counter_tokens = counter_tokens\n"
    string += "\t\tself.first_token = self.tokens[self.counter_tokens]\n"
    string += "\t\tself.final = self.tokens[self.counter_tokens - 1]\n"
    string += "\t\treturn possible\n\n"

    string += "\tdef peek(self, item, type = False):\n"
    string += "\t\tif type:\n"
    string += "\t\t\tif self.first_token.type == item:\n"
    string += "\t\t\t\tself.sig()\n"
    string += "\t\t\t\treturn True\n"
    string += "\t\t\telse:\n"
    string += "\t\t\t\treturn False\n"
    string += "\t\telse:\n"
    string += "\t\t\tif self.first_token.value == item:\n"
    string += "\t\t\t\tself.sig()\n"
    string += "\t\t\t\treturn True\n"
    string += "\t\t\telse:\n"
    string += "\t\t\t\treturn False\n\n"

    string += "\t# COMIENZA LAS EVALUACIONES DE LAS PRODUCCIOENS\n"

    # los tokens permitidos dentro de las produccionse
    new_tokens = []
    for p in productions:
        string = encabezado_funcion(p, string)
        string, news = body_funcion(productions[p], string, parse_line, tokens, keywords)
        string += "\n"
        for token in news:
            if token not in new_tokens:
                new_tokens.append(token)

    file.write(string)
    file.close()

    automata_parse = parse_line[:-1]
    for token in new_tokens:
        if token in OPERATORS:
            automata_parse += "|" + str(ord(token))
        else:
            automata_parse += "|" + token
    # automata generados por los tokens y el algoritmo directo
    automata_parse = automata_parse + ")"
    #print(automata_parse)
    fixed_parser = fix_expect(string)
    
    return fixed_parser, automata_parse

def fix_expect(parser):
    parser = parser.split("\n")
    automata_parser = ""
    for line in parser:
        if "self.simulate(" in line and "while" not in line:
            new_line = line.split("(",1)
            automata_parser += new_line[0] + "("
            args = new_line[1].split("(", 1)
            second = args[1].replace(")", "")
            second = second.replace(":", "")
            automata_parser += args[0] + "," + second + "):\n"
        elif "self.simulate(" in line and "while" in line:
            or_parted = line.split("or")
            for part in or_parted:
                new_line = part.split("(",1)
                automata_parser += new_line[0] + "("
                args = new_line[1].split("(", 1)
                second = args[1].replace(")", "")
                automata_parser += args[0] + "," + second[:-1] + ") or"
            automata_parser = automata_parser[:-2] +  ":\n"
        else:
            automata_parser += line + "\n"
    return automata_parser

# devuelve el nombre de la funcion
def encabezado_funcion(data, string):
    # quitamos los valores tab y enter que encontremos en producciones
    data = data.replace("\n", "")
    data = data.replace("\t", "")
    data = data.replace(" ", "")

    # como esta en C, ree-escribimos la funcion
    # este nos da el nombre de la funcion
    funciton_data = data.split("<")[0]
    
    string += "\t# funcion %s\n" % funciton_data
    string += "\tdef " + funciton_data + "(self"
    if "<" in data:
        function_params = data.split("<")[1]
        string +="," + function_params[:-1]
    string += "):\n"
    return string

# encontramos el resto de la función
def body_funcion(body, string, parse_line, tokens, key_words):
    # guardamos la informacion en un array
    new_tokens = []
    actual = 0
    temp = ""
    extras = "\t\t"
    conditional = False
    inside_if = False

    # hacemos un ciclo para sobreescribir el archivos
    while actual < len(body):
        if body[actual] == "{":
            extra = actual + 1
            counter = 0
            # si no encuentra dentro de las operaciones validas, anada las siguientes lineas
            while body[extra] not in OPS and counter != 2:
                if body[extra] == " ":
                    pass
                elif body[extra] == '"':
                    counter += 1
                    temp += body[extra]
                else:
                    temp += body[extra]
                extra += 1
            # este simbolo representa las funciones en C, las escribimos en python    
            if "<" in temp:
                    if conditional:
                        temp = "self.simulate('" + temp + "'):"
                        conditional = False
                    name = temp.split("<", 1)[0]
                    arg = temp.split("<", 1)[1][:-1]
                    temp = "self."+ name + "(" + arg + ")"
            elif '"' in temp:
                temp = "self.peek(" + temp +")"
            else:
                temp = "self."+ temp + "()"
            # escribimos funciones con respecto a lo encontrado anteriormente
            string += extras + "while self.simulate(" + temp +"):\n"
            temp = ""
            extras += "\t"
        elif body[actual] == "}":
            extras = extras.replace("\t", "", 1)
            if inside_if:
                extras = extras.replace("\t", "", 1)
        
        # como el archivo encuentra . los eliminamos 
        elif body[actual] == "(" and body[actual+1] == ".":
            actual += 2
            while body[actual] != "." or body[actual + 1] != ")":
                temp += body[actual]
                actual += 1
            actual += 1
            string += extras + temp + "\n"
            temp = ""
            
        elif body[actual] == '"':
            actual += 1
            while body[actual] != '"':
                temp += body[actual]
                actual += 1
            # añadimos condicionales a las funciones de producciones creadas anteriormente
            if conditional:
                string += "self.simulate(self.peek('" + temp + "')):\n"
                conditional = False
            string += extras + 'self.peek("' + temp + '")\n'
            new_tokens.append(temp)
            temp = ""

        elif body[actual] == "(":
            pass

        elif body[actual] == ")":
            if inside_if:
                extras = extras.replace("\t", "", 1)

        elif body[actual] == "[":
            string += extras + "if "
            conditional = True
            extras += "\t"
        elif body[actual] == "]":
            extras = extras.replace("\t", "", 1)
            if inside_if:
                extras = extras.replace("\t", "", 1)

        # si encuentra la funcion or, evalua los siguientes aspectos
        elif body[actual] == "|":
            extra = actual -1
            while extra > 0:
                if body[extra] == " " or body[extra] == "\n":
                    pass
                elif body[extra] =="." and body[extra - 1] == "(":
                    extra -= 1 
                elif body[extra] in OPS:
                    break
                extra -= 1
            if body[extra] == "{":
                part = string.rfind("while")
                while string[part] != ":":
                    part += 1
                counter = 0
                cond = ""
                i = actual + 1
                while body[i] not in OPS and counter != 2:
                    if body[i] == " ":
                        pass
                    elif body[i] == '"':
                        counter += 1
                        temp += body[i]
                    else:
                        temp += body[i]
                    i += 1
                # como dijimos, creamos la funcion en python, a partir de este simbolo
                if "<" in temp:
                        if conditional:
                            string += "self.simulate('" + temp + "'):"
                            conditional = False
                        name = temp.split("<", 1)[0]
                        arg = temp.split("<", 1)[1][:-1]
                        temp = "self."+ name + "(" + arg + ")"
                elif '"' in temp:
                    temp = "self.peek(" + temp +")"
                else:
                    temp = "self."+ temp + "()"
                first_if = string[part+2:].split("\n")[0]
                string_parted = string[part+1:]
                string = string[:part] + " or self.simulate("+ temp + ")" + ":\n"
                first_if = first_if.replace("\t", "")
                string += extras + "if self.simulate(" + first_if + "):"
                lines = string_parted.split("\n")
                for line in lines:
                    string += "\t" + line + "\n"
            elif body[extra] == "(":
                i = extra + 1
                counter = 0
                while body[i] not in OPS and counter != 2:
                    if body[i] == " ":
                        pass
                    elif body[i] == '"':
                        counter += 1
                        temp += body[i]
                    else:
                        temp += body[i]
                    i += 1
                if "<" in temp:
                        if conditional:
                            string += "self.simulate('" + temp + "'):"
                            conditional = False
                        name = temp.split("<", 1)[0]
                        arg = temp.split("<", 1)[1][:-1]
                        temp = arg + "=self."+ name + "(" + arg + ")"
                elif '"' in temp:
                    temp = "self.peek(" + temp +")"
                else:
                    temp = "self."+ temp + "()"
                previous = string.rfind(temp)
                string_parted = string[previous:]

                if "=" in temp:
                    expect_arg = temp.split("=")[1]
                else:
                    expect_arg = temp
                string = string[:previous] + "if self.simulate(" + expect_arg +"):\n"

                lines = string_parted.split("\n")
                for line in lines:
                    string += extras + "\t"+ line + "\n"
                temp == ""

            elif body[extra] == "|":
                pass
            temp = ""
            inside_if = True
            i = actual + 1
            counter = 0 
            in_comillas = False
            while (body[i] not in OPS or not in_comillas) and counter != 2:
                if body[i] == ")" and not in_comillas:
                    break
                if body[i] == " ":
                    pass
                elif body[i] == '"':
                    counter += 1
                    temp += body[i]
                else:
                    temp += body[i]
                i += 1
            if "<" in temp:
                    if conditional:
                        string += "self.simulate('" + temp + "'):"
                        conditional = False
                    name = temp.split("<", 1)[0]
                    arg = temp.split("<", 1)[1][:-1]
                    temp = "self."+ name + "(" + arg + ")"
            elif '"' in temp:
                temp = "self.peek(" + temp +")"
            else:
                temp = "self."+ temp + "()"
            string += extras + "elif self.simulate(" + temp + "):\n"
            extras += "\t"
            temp = ""

        elif body[actual] == " " or body[actual] == "\n" or body[actual] == "\t":
            if temp != "":
                if temp in tokens or temp in key_words:
                    string += extras + "self.peek('" + temp + "', True)\n"
                elif "<" in temp:
                    if conditional:
                        string += "self.simulate('" + temp + "'):\n"
                        conditional = False
                    name = temp.split("<", 1)[0]
                    arg = temp.split("<", 1)[1][:-1]
                    string += extras + arg.replace(" ", "") + "=self."+ name + "(" + arg + ")\n"
                else:
                    if conditional:
                        string += "self.simulate('" + temp + "'):\n"
                        conditional = False
                    string += extras + "self."+ temp + "()\n"
                temp = ""
            else:
                pass


        else:
            temp += body[actual]
        actual += 1
    return string, new_tokens