class Token:
	def __init__(self, type, value):
		self.type = type
		self.value = value

# to create the automata
class Automata:
	def __init__(self, expression):
		self.id = expression 
		self.states = []

	def __str__(self):
		string = 'State: ' + str(self.state)
		return string
		
class State: 
	def __init__(self, number):
		self.id = number
		# transition list
		self.transitions = []
		# is it accept transition
		self.accept = False 
		
class Handler: 
   def __init__(self, symbol, id):
	   # symbol in the tree
	   self.symbol = symbol
	   # id where is go
	   self.id = id