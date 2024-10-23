class StateAtLine:
	mathenv_options = {
		"\\begin{prop}" : "Proposotion", 
		"\\begin{lemma}" : "Lemma",
		"\\begin{thm}" : "Theorem",
		"\\begin{cor}" : "Corollary",
		"\\begin{crit}" : "Criterion",
		"\\begin{conj}" : "Conjecture",
		"\\begin{question}" : "Question",
		"\\begin{remark}" : "Remark",
		"\\begin{claim}" : "Claim", 
		"\\begin{defn}" : "Definition",
		"\\begin{example}" : "Example",
		"\\begin{exercise}" : "Exercise",
		"\\begin{fact}" : "Fact",
		"\\begin{guess}" : "Guess",
		"\\begin{specula}" : "Speculation"
	}
	def __init__(self, at_line):
		self.at_line = 0
		self.section = 0
		self.subsection = 0
		self.subsubsection = 0
		self.mathenv_num = 0
		self.mathenv_name = "Introduction"

	def move_state_by(self, tex_line):
		state_changed = False
		if "\\section" in tex_line: 
			self.section += 1
			self.subsection = 0
			self.subsubsection = 0
			self.mathenv_num = 0
			self.mathenv_name = "Section"
			state_changed = True
		if "\\subsection" in tex_line: 
			self.subsection += 1
			self.subsubsection = 0
			self.mathenv_num = 0
			self.mathenv_name = "Subsection"
			state_changed = True
		if "\\subsubsection" in tex_line: 
			self.subsubsection += 1
			state_changed = True

		env_per_line = 0
		for mathenv in self.mathenv_options:
			if mathenv in tex_line:
				self.mathenv_num += 1
				self.mathenv_name = self.mathenv_options[mathenv] 
				env_per_line += 1
				state_changed = True
		if env_per_line >= 2:
			print("ERROR: Two math environments in the same line!")
		self.at_line += 1
		return (self.mathenv_name != "") and state_changed

	def get_name(self):
		# E.g: Theorem 3.1.2 or Lemma 1.1.0
		if self.mathenv_num != 0:
			return f"{self.mathenv_name} {self.section}.{self.subsection}.{self.mathenv_num}"
		elif self.subsection != 0:
			return f"{self.mathenv_name} {self.section}.{self.subsection}"
		elif self.section != 0:
			return f"{self.mathenv_name} {self.section}"
		else:
			return f"{self.mathenv_name}"

