
from typing import List, Dict, Tuple, Union

class Semantic:
	def __init__(self) -> None:
		# Tabela de símbolos implementada como
		# uma pilha (lista) de tabelas (dicionários)
		# {'lexema': (valor, tipo)}
		self.__stack: List[Dict[str,Tuple[Union[str,int,None],str]]] = []
		self.__n: int = 0

	def __declare_id(self, stmt: str, number: bool):
		for var in map(lambda v: v.strip(), stmt.split(',')):
			value = None
			if '=' in var:
				var, value = tuple(map(lambda val: val.strip(), var.split('=')))
				if number and value[0] == '"':
					return 'tipos incompativeis, valor deve ser numerico'
				elif not number and value[0] != '"':
					return 'tipos incompativeis, valor deve ser cadeia'
				value = float(value) if number else value[1:-1]
			if var in self.__stack:
				return 'id já declarado'
			self.__stack[-1][var] = (value, 'numero' if number else 'cadeia')
	
	def __find_id(self, id: str):
		for i in range(self.__n - 1, -1, -1):
			if id in self.__stack[i]:
				return i
			
	def __attr(self, stmt: str):
		id, val = map(lambda v: v.strip(), stmt.split('='))
		idx_id = self.__find_id(id)
		if idx_id == None:
			return '{} não encontrado'.format(id)
		symbol = self.__stack[idx_id][id]
		if val.isalpha():
			idx_val = self.__find_id(val)
			if idx_val == None:
				return '{} não encontrado'.format(val)
			val = self.__stack[idx_val][val]
			if symbol[1] == val[1]:
				self.__stack[idx_id][id] = val
			else:
				return 'tipos incompatíveis'
		elif symbol[1] == 'cadeia' and val[0] != '"':
			return 'tipos incompatíveis'
		elif symbol[1] == 'numero' and val[0] == '"':
			return 'tipos incompatíveis'
		else:
			self.__stack[idx_id][id] = (val, self.__stack[idx_id][id][1])

	def read_line(self, line: str, row: int):
		if line.startswith('BLOCO'):
			self.__stack.append({})
			self.__n += 1
		elif self.__n > 0:
			if line.startswith('FIM'):
				self.__stack.pop()
				self.__n -= 1
			elif line.startswith('NUMERO'):
				r = self.__declare_id(line[6:].strip(), True)
				if r:
					print((row, r))
			elif line.startswith('CADEIA'):
				r = self.__declare_id(line[6:].strip(), False)
				if r:
					print((row, r))
			elif line.startswith('PRINT'):
				id = line[5:].strip()
				i = self.__find_id(id)
				if i != None:
					print((row, self.__stack[i][id][0]))
				else:
					print((row, '{} não encontrado'.format(id)))
			else:
				r = self.__attr(line)
				if r:
					print((row, r))
