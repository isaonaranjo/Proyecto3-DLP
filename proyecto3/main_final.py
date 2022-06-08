'''
    Maria Isabel Ortiz Naranjo
'''
from parser_decom import parser
from read_compiler import read_file
from analysis import analyze, arrgl
from create_file import create_file_compiler

file_open = open('proyecto3/Inputs/ArchivoPrueba0.1.atg')
informacion = file_open.read()
file_open.close()

data, character, keywords, tokens, productions = read_file(informacion)
automata_dfa, dfa_more, data_parse = analyze(data, character, keywords, tokens, productions)
new_data_parse = arrgl(data_parse)
create_file_compiler(automata_dfa, dfa_more, new_data_parse, data)