
from typing import List, Dict, Tuple, Union

QUOTATIONS = ('"', '“', '”')

class Semantic:
	def __init__(self) -> None:
		# Tabela de símbolos implementada como
		# uma pilha (lista) de tabelas (dicionários)
		# {'lexema': (valor, tipo)}
		self.__stack: List[Dict[str,Tuple[Union[str,float,None],str]]] = []
		self.__n: int = 0

	# Trata sobre as declarações das variáveis.
	# Se tudo ocorrer bem retorna None, caso
	# contrário, retorna uma lista de str descrevendo o(s) erro(s).
	def __declare_id(self, stmt: str, number: bool):
		errors:List[str] = []
		for var in map(lambda v: v.strip(), stmt.split(',')):
			id = var.split('=')[0].strip() if '=' in var else var
			if id in self.__stack[-1]:
				errors.append('id ({}) já foi declarado anteriormente no mesmo escopo'.format(var))
				continue
			self.__stack[-1][id] = (None, 'numero' if number else 'cadeia')
			if '=' in var: # quando houver atribuição na declaração chama a função adequada
				err = self.__attr(var)
				if err:
					errors.append(err)
		if len(errors) > 0:
			return errors
	
	# busca um identificador na tabela de simbolos
	# retorna o index se encontrar ou None caso contrário
	def __find_id(self, id: str):
		for i in range(1, self.__n + 1):
			if id in self.__stack[-i]:
				return self.__n - i
		
	# Trata sobre as instruções de atribuição
	# Se tudo ocorrer bem retorna None, caso
	# contrário, retorna uma str descrevendo o erro.
	def __attr(self, stmt: str):
		id, val = map(lambda v: v.strip(), stmt.split('='))
		idx_id = self.__find_id(id)
		if idx_id == None:
			return '({}) não encontrado'.format(id)
		symbol = self.__stack[idx_id][id]
		if val.isalpha():
			idx_val = self.__find_id(val)
			if idx_val == None:
				return '({}) não encontrado'.format(val)
			id_val = val
			val = self.__stack[idx_val][val]
			if symbol[1] == val[1]:
				self.__stack[idx_id][id] = val
			else:
				return '({}) e ({}) são de tipos incompatíveis'.format(id, id_val)
		elif symbol[1] == 'cadeia' and val[0] not in QUOTATIONS:
			return 'tipo incompatível: valor deve ser do tipo cadeia'
		elif symbol[1] == 'numero' and val[0] in QUOTATIONS:
			return 'tipo incompatível: valor deve ser numérico'
		else:
			val = float(val) if symbol[1] == 'numero' else val[1:-1]
			self.__stack[idx_id][id] = (val, self.__stack[idx_id][id][1])

	# Função geral que avalia o tipo de instrução
	# e chama a função adequada.
	# Responsável tbm por informar eventuais erros
	# e quais linhas eles ocorreram
	def read_line(self, line: str, row: int):
		if line.startswith('BLOCO'):
			self.__stack.append({})
			self.__n += 1
		elif self.__n > 0:
			if line.startswith('FIM'):
				self.__stack.pop()
				self.__n -= 1
			elif line.startswith('NUMERO'):
				err = self.__declare_id(line[6:].strip(), True)
				if err:
					print(('** ERRO **', row, err))
			elif line.startswith('CADEIA'):
				err = self.__declare_id(line[6:].strip(), False)
				if err:
					print(('** ERRO **', row, err))
			elif line.startswith('PRINT'):
				id = line[5:].strip()
				i = self.__find_id(id)
				if i != None:
					print((row, self.__stack[i][id][0]))
				else:
					print(('** ERRO **', row, '({}) não encontrado'.format(id)))
			else:
				err = self.__attr(line)
				if err:
					print(('** ERRO **', row, err))
