# Este es el scanner que se generara con las reglas establecidas por ./Inputs/ArchivoPrueba1.ATG

import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from structure_tokens import State, Automata, Token, Handler
from utils import ecerradura_node, simulate_dfa_direct
from analysis import terminacion_compilador

class Production_Parse:
	def __init__(self, tokens):
		self.tokens = tokens
		self.counter_tokens = 0
		self.first_token = self.tokens[self.counter_tokens]
		self.last_token = ''

	def operation_tokens( self ):
		self.counter_tokens += 1
		if self.counter_tokens < len(self.tokens):
			self.first_token = self.tokens[self.counter_tokens]
			self.last_token = self.tokens[self.counter_tokens - 1]

	def expect(self, item, arg = None):
		counter_tokens = self.counter_tokens
		possible = False
		if item != None:
			try:
				if arg == None:
					ans = item()
				else:
					ans = item(arg)
				# si es booleano
				if type(ans) == bool:
					possible = ans
				else:
					possible = True
			except:
				possible = False
		self.counter_tokens = counter_tokens
		self.first_token = self.tokens[self.counter_tokens]
		self.last_token = self.tokens[self.counter_tokens - 1]
		return possible

	def read_token(self, item, type = False):
		if type:
			if self.first_token.type == item:
				self.operation_tokens()
				return True
			else:
				return False
		else:
			if self.first_token.value == item:
				self.operation_tokens()
				return True
			else:
				return False

	# COMIENZA LAS EVALUACIONES DE LAS PRODUCCIOENS
	# funcion Expr
	def Expr(self):
		while self.expect(self.Stat,) :
			self.Stat()
			self.read_token(";")
		self.read_token(".")

	# funcion Stat
	def Stat(self):
		value = 0
		value=self.Expression(value)
		print(str(value))

	# funcion Expression
	def Expression(self,resultado):
		resultado1, resultado2 = 0, 0
		resultado1=self.Term(resultado1)
		while self.expect(self.read_token,"+"):
			if self.expect(self.read_token,"+"	):
				self.read_token("+")
				resultado2=self.Term(resultado2)
				resultado1+=resultado2
	
			elif self.expect(self.read_token,"-"):
				self.read_token("-")
				resultado2=self.Term(resultado2)
				resultado1-=resultado2
		resultado=resultado1
		return resultado 


	# funcion Term
	def Term(self,resultado):
		resultado1, resultado2 =  0,0
		resultado1=self.Factor(resultado1)
		while self.expect(self.read_token,"*"):
			if self.expect(self.read_token,"*"	):
				self.read_token("*")
				resultado2=self.Factor(resultado2)
				resultado1*=resultado2
		resultado=resultado1
		return resultado 


	# funcion Factor
	def Factor(self,resultado):
		signo=1
		if self.expect(self.read_token,'-'):
			self.read_token("-")
			signo = -1
		if self.expect(self.Number,resultado):
			resultado=self.Number(resultado)
			
		elif self.expect(self.read_token,"("):
			self.read_token("(")
			resultado=self.Expression(resultado)
			self.read_token(")")
		resultado*=signo
		return resultado 


	# funcion Number
	def Number(self,resultado):
		self.read_token('numero', True)
		resultado = int(self.last_token.value)
		return resultado 




def generate_transition_automata():
	automatas = []
	automata0 = Automata("parse_aritmetica")
	node= State(0)
	transition = Handler('0', 1)
	node.transitions.append(transition)
	transition = Handler('1', 1)
	node.transitions.append(transition)
	transition = Handler('2', 1)
	node.transitions.append(transition)
	transition = Handler('3', 1)
	node.transitions.append(transition)
	transition = Handler('4', 1)
	node.transitions.append(transition)
	transition = Handler('5', 1)
	node.transitions.append(transition)
	transition = Handler('6', 1)
	node.transitions.append(transition)
	transition = Handler('7', 1)
	node.transitions.append(transition)
	transition = Handler('8', 1)
	node.transitions.append(transition)
	transition = Handler('9', 1)
	node.transitions.append(transition)
	transition = Handler(';', 2)
	node.transitions.append(transition)
	transition = Handler('.', 2)
	node.transitions.append(transition)
	transition = Handler('-', 2)
	node.transitions.append(transition)
	transition = Handler('/', 2)
	node.transitions.append(transition)
	automata0.states.append(node)
	node= State(1)
	node.accept = True
	transition = Handler('0', 1)
	node.transitions.append(transition)
	transition = Handler('1', 1)
	node.transitions.append(transition)
	transition = Handler('2', 1)
	node.transitions.append(transition)
	transition = Handler('3', 1)
	node.transitions.append(transition)
	transition = Handler('4', 1)
	node.transitions.append(transition)
	transition = Handler('5', 1)
	node.transitions.append(transition)
	transition = Handler('6', 1)
	node.transitions.append(transition)
	transition = Handler('7', 1)
	node.transitions.append(transition)
	transition = Handler('8', 1)
	node.transitions.append(transition)
	transition = Handler('9', 1)
	node.transitions.append(transition)
	automata0.states.append(node)
	node= State(2)
	node.accept = True
	automata0.states.append(node)
	automatas.append(automata0)

	automata1 = Automata("numero")
	node= State(0)
	transition = Handler('0', 1)
	node.transitions.append(transition)
	transition = Handler('1', 1)
	node.transitions.append(transition)
	transition = Handler('2', 1)
	node.transitions.append(transition)
	transition = Handler('3', 1)
	node.transitions.append(transition)
	transition = Handler('4', 1)
	node.transitions.append(transition)
	transition = Handler('5', 1)
	node.transitions.append(transition)
	transition = Handler('6', 1)
	node.transitions.append(transition)
	transition = Handler('7', 1)
	node.transitions.append(transition)
	transition = Handler('8', 1)
	node.transitions.append(transition)
	transition = Handler('9', 1)
	node.transitions.append(transition)
	automata1.states.append(node)
	node= State(1)
	node.accept = True
	transition = Handler('0', 1)
	node.transitions.append(transition)
	transition = Handler('1', 1)
	node.transitions.append(transition)
	transition = Handler('2', 1)
	node.transitions.append(transition)
	transition = Handler('3', 1)
	node.transitions.append(transition)
	transition = Handler('4', 1)
	node.transitions.append(transition)
	transition = Handler('5', 1)
	node.transitions.append(transition)
	transition = Handler('6', 1)
	node.transitions.append(transition)
	transition = Handler('7', 1)
	node.transitions.append(transition)
	transition = Handler('8', 1)
	node.transitions.append(transition)
	transition = Handler('9', 1)
	node.transitions.append(transition)
	automata1.states.append(node)
	automatas.append(automata1)

	# lista para los tokens
	tokens = []

	# comienza la solicitud del archiv
	m_file = input('Ingrese el archivo a evaluar: ')
	prueba = open(m_file)
	data = prueba.read()
	prueba.close()
	last = 0
	# recorremos el archivo abierto
	for i in range(len(data)):
		valid = terminacion_compilador(data, automata0, i)
		if valid:
			if (last != 0) and (i - last > 0):
				while last < i:
					print(data[last], end='')
					last += 1
				print(': False')
			last += len(valid)
			aut = 1
			evaluate_token = Token('Token', valid)
			while aut<len(automatas):
				if (simulate_dfa_direct(automatas[aut], valid)):
					evaluate_token = Token(automatas[aut].id, valid)
					break
				aut += 1
			print('%s = %s' % (evaluate_token.type,evaluate_token.value))
			tokens.append(evaluate_token)
			i += len(valid)
		else:
			break
	parser = Production_Parse(tokens)
	# Operaciones de las expresiones anteriormente analizadas
	print("SE REALIZAN LAS OPERACIONES")
	parser.Expr()

if __name__ == "__main__":
   generate_transition_automata()