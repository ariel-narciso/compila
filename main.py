from semantic import Semantic

def __main__():
	s = Semantic()
	r = 1
	while True:
		try:
			s.read_line(input().strip(), r)
			r += 1
		except EOFError:
			break

__main__()