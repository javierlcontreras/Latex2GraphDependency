from dependency_graph import DependencyGraph, DependencyGraphNode
from state_at_line import StateAtLine

class DependencyParser:
	label_indicator = "\\label{"
	ref_indicator = "\\ref{"

	def __init__(self):
		self.environments = {}
		self.labels = {}
		self.refs = {}
		self.graph = DependencyGraph([])

	def _add_label(self, label, node):
		self.labels[label] = node

	def _add_ref(self, ref, node):
		self.refs[ref] = node
		if ref not in self.labels: 
			print(f"ERROR: ref {ref} doesn't match with any labels")
		self._add_ref_label_edge(ref, node)

	def _add_ref_label_edge(self, ref, node):
		self.graph.add_edge(node, self.labels[ref])

	def _create_node_for_state(self, state):
		node = DependencyGraphNode(state.get_name())
		return node

	def _save_environments(self, tex_lines):
		state = StateAtLine(0)
		for tex_line in tex_lines:
			state_changed = state.move_state_by(tex_line)
			if state_changed:
				node = self._create_node_for_state(state)
				self.environments[state.get_name()] = node
		
		for env in self.environments:
			self.graph.add_node(self.environments[env])

	def _save_labels(self, tex_lines):
		state = StateAtLine(0)
		for tex_line in tex_lines:
			state.move_state_by(tex_line)
			if self.label_indicator in tex_line:
				if tex_line.count(self.label_indicator) >= 2:
					print("ERROR: more than one label in one line")

				label = tex_line.split("\\label{")[1].split("}")[0]
				node = self.environments[state.get_name()]
				self._add_label(label, node)

	def _save_references(self, tex_lines):
		state = StateAtLine(0)
		prev_environment = state.get_name() 
		for tex_line in tex_lines:
			state_changed = state.move_state_by(tex_line)
			if state_changed:
				if state.get_name() in self.environments: 
					prev_environment = self.environments[state.get_name()]

			if self.ref_indicator in tex_line:
				refs = tex_line.split("\\ref{")[1:]
				for ref in refs:
					ref_name = ref.split("}")[0]
					self._add_ref(ref_name, prev_environment)

	def parse(self, tex):
		tex_lines = tex.split("\n")
		self._save_environments(tex_lines)
		self._save_labels(tex_lines)
		self._save_references(tex_lines)
		
		print(self.graph.to_csv())