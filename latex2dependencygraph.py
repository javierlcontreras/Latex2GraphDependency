from dependency_parser import DependencyParser 

def main():
	with open("../input.tex", 'r') as reader:
		tex = reader.read()

	DependencyParser().parse(tex)

if __name__ == "__main__":
	main()