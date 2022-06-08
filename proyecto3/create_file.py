''' Archivo que sirve para leer el lenguaje de COCOr'''

def create_file_compiler(dfa, extras, parser, data = 'productions'):
    print("Se genero el archivo con el nombre %s.py"%data)
    i = 0
    file_name = open("./Outputs/" + data + ".py", "w+", encoding="utf-8")
    file_name.write('# Este es el scanner que se generara con las reglas establecidas por ./Inputs/%s.atg\n\n' % data)

    file_name.write('import os\n')
    file_name.write('import sys\n')
    file_name.write('sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))\n')
    file_name.write('from structure_tokens import State, Automata, Token, Handler\n')
    file_name.write('from utils import ecerradura_node, simulate_dfa_direct\n')
    file_name.write('from analysis import terminacion_compilador\n\n')

    file_name.write(parser)

    file_name.write("def generate_transition_automata():\n")
    
    file_name.write("\tautomatas = []\n")
    creando_automatas(dfa, i, file_name)
    # sumamos uno al contador
    i += 1
    for automata in extras:
        creando_automatas(extras[automata], i, file_name, automata)
        i += 1
    file_name.write("\t# lista para los tokens\n")
    file_name.write("\ttokens = []\n\n")
    file_name.write("\t# comienza la solicitud del archiv\n")
    file_name.write("\tm_file = input('Ingrese el archivo a evaluar: ')\n")
    file_name.write("\tprueba = open(m_file)\n")
    file_name.write("\tdata = prueba.read()\n")
    file_name.write("\tprueba.close()\n")
    
    file_name.write("\tlast = 0\n")
    file_name.write("\t# recorremos el archivo abierto\n")
    file_name.write("\tfor i in range(len(data)):\n")
    file_name.write("\t\tvalid = terminacion_compilador(data, automata0, i)\n")
    file_name.write("\t\tif valid:\n")
    file_name.write("\t\t\tif (last != 0) and (i - last > 0):\n")
    file_name.write("\t\t\t\twhile last < i:\n")
    file_name.write("\t\t\t\t\tprint(data[last], end='')\n")
    file_name.write("\t\t\t\t\tlast += 1\n")
    file_name.write("\t\t\t\tprint(': False')\n")
    file_name.write("\t\t\tlast += len(valid)\n")
    file_name.write("\t\t\taut = 1\n")
    file_name.write("\t\t\tevaluate_token = Token('Token', valid)\n")
    file_name.write("\t\t\twhile aut<len(automatas):\n")
    file_name.write("\t\t\t\tif (simulate_dfa_direct(automatas[aut], valid)):\n")
    file_name.write("\t\t\t\t\tevaluate_token = Token(automatas[aut].id, valid)\n")
    file_name.write("\t\t\t\t\tbreak\n")
    file_name.write('\t\t\t\taut += 1\n')
    file_name.write("\t\t\tprint('%s = %s' % (evaluate_token.type,evaluate_token.value))\n")
    file_name.write("\t\t\ttokens.append(evaluate_token)\n")
    file_name.write("\t\t\ti += len(valid)\n")
    file_name.write("\t\telse:\n")
    file_name.write("\t\t\tbreak\n")
    file_name.write("\tparser = Production_Parse(tokens)\n")
    file_name.write("\t# Operaciones de las expresiones anteriormente analizadas\n")
    file_name.write('\tprint("SE REALIZAN LAS OPERACIONES")\n')
    file_name.write("\tparser.EstadoInicial()\n\n")
    file_name.write('if __name__ == "__main__":\n'+'   generate_transition_automata()')

    file_name.close()

# funcion para ir escribiendo las transcciones conforme a lo indicado
def creando_automatas(automata, i, file, name='parse_aritmetica'):
    file.write("\tautomata"+str(i)+' = Automata("'+ name +'")\n')
    for node in automata.state:
        file.write("\tnode= State("+ str(node.id) + ")\n")
        if node.accept:
            file.write("\tnode.accept = True\n")
        for transition in node.transition:
            file.write("\ttransition = Handler('" +transition.symbol+"', "+str(transition.id) +")\n")
            file.write("\tnode.transitions.append(transition)\n")
        file.write("\tautomata"+str(i)+".states.append(node)\n")
    file.write("\tautomatas.append(automata"+str(i)+")\n")
    file.write("\n")