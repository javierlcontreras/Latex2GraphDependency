class DependencyGraphNode:
	def __init__(self, _name):
		self.name = _name
		self.children = []

	def add_edge(self, node):
		self.children.append(node)

	def __str__(self):
		return self.name

	def __repr__(self):
		return self.__str__()


class DependencyGraph:
	def __init__(self, _nodes):
		self.nodes = _nodes

	def add_node(self, node):
		self.nodes.append(node)

	def add_edge(self, node1, node2):
		node1.add_edge(node2)

	def __str__(self):
		graph_string = ""
		for node in self.nodes:
			graph_string += str(node) + ": " + str(node.children) + "\n"
		return graph_string

	def  __repr__(self):
		return self.__str__()

	# Useful for using gephi
	def to_csv(self):
		graph_csv = ""
		for node in self.nodes:
			graph_csv += node.name
			for child in node.children:
			 	graph_csv += ";" + child.name
			graph_csv += "\n"
		return graph_csv

