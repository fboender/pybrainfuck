#!/usr/bin/env python
"""
This is a Brainfuck interpreter (not a compiler) written in Python. It is
somewhat optimized for speed, as much as that is possible. By default it allows
for 30000 bytes of memory, but this can be configured by passing a parameter. 

Some protections are in place in order to keep the program from entering an
infinite loop. There is no recursion in the interpreter, in order to avoid
stack overflows. It also contains a very rudementary debugger which, for each
opcode, prints the current position in the code and the contents of the memory.
"""

import sys
import cStringIO
import time

class BrainfuckError(Exception):
	pass

class Brainfuck(object):
	"""
	Brainfuck interpreter. 

	Example:
		# Divide
		bf = brainfuck.Brainfuck(
			\"""
				,>,>++++++[-<--------<-------->>]<<[>[->+>+<<
				]>[-<<-[>]>>>[<[>>>-<<<[-]]>>]<<]>>>+<<[-<<+>>
				]<<<]>[-]>>>>[-<<<<<+>>>>>]<<<<++++++[-<++++++++>]
				<.
			\""", 
			'62')
		out = bf.run()
		print out              # 3
	"""

	operators = ['+', '-', '>', '<', '[', ']', '.', ',']

	def __init__(self, code, input = sys.stdin, output = None):
		"""
		Interpret and run Brainfuck code given in 'code'. Brainfuck program
		will read from input which can be either an open filehandle (default
		stdin) or a string. Will write to output. If output is None (default),
		the run() function will return the output instead.
		"""
		if type(input) == type(''):
			self.input = cStringIO.StringIO(input)
		else:
			self.input = input
		if output == None:
			self.return_output = True
			self.output = cStringIO.StringIO()
		else:
			self.return_output = False
			self.output = output

		# Syntax checking :-D
		if code.count('[') != code.count(']'):
			raise BrainfuckError('Unmatched number of brackets')

		# Remove non-brainfuck operators so the interpreter doesn't have to
		# process them.
		c = ''
		for op in code:
			if op in self.operators:
				c += op
		code = c

		# Find matching brackets upfront so we don't have to do it many times
		# in the code.
		self.jumps = {}        # Reference dict of brackets and their matching brackets
		self.c_len = len(code) # Code length
		d_ip = 0               # Discover Instruction Pointer
		while d_ip < self.c_len:
			instr = code[d_ip]
			if instr == '[':
				# Scan for matching bracket forwards
				heap = 0
				for ip in range(d_ip+1, self.c_len+1):
					if code[ip] == '[':
						heap += 1
					elif code[ip] == ']':
						if heap == 0:
							self.jumps[d_ip] = ip
							break
						else:
							heap -= 1
			elif instr == ']':
				# Scan for matching bracket backwards
				heap = 0
				for ip in range(d_ip-1, -1, -1):
					if code[ip] == ']':
						heap += 1
					elif code[ip] == '[':
						if heap == 0:
							self.jumps[d_ip] = ip
							break
						else:
							heap -= 1
			d_ip += 1

		self.code = code
			
	def run(self, mem_size = 30000, max_instr = 1000000, debug=False):
		"""
		Run the brainfuck code with a maximum number of instructions of
		max_instr (to counter infinite loops). If self.output is None, it
		returns the output instead of directly writing to the file descriptor.
		If debug is set to True, the interpreter will output debugging
		information during execution.
		"""
		# Copy self references for speed.
		code = self.code
		input = self.input
		output = self.output
		jumps = self.jumps
		c_len = self.c_len

		icnt = 0             # Instruction counter against infinite loops
		mem = [0] * mem_size # Memory
		buf_out = ''         # Output buffer for tiny speed increase
		ip = 0               # Instruction pointer (current excecute place in code)
		dp = 0               # Data pointer (current read/write place in mem)
		m_dp = 0             # Maximum Data Pointer (largest memory index access by code)

		while ip < c_len:
			if icnt > max_instr:
				raise BrainfuckError('Maximum nr of instructions exceeded')

			instr = code[ip]

			if instr == '+':
				mem[dp] += 1
			elif instr == '-':
				mem[dp] -= 1
			elif instr == '>': 
				dp += 1
				if debug and dp > m_dp:
					m_dp = dp
			elif instr == '<': 
				dp -= 1
				if debug and dp > m_dp:
					m_dp = dp
			elif instr == '[':
				if mem[dp] == 0:
					ip = jumps[ip]
			elif instr == ']':
				if mem[dp] != 0:
					ip = jumps[ip]
			elif instr == '.':
				buf_out += chr(mem[dp])
			elif instr == ',':
				try:
					mem[dp] = ord(input.read(1))
				except:
					mem[dp] = -1

			ip += 1
			icnt += 1

			if debug:
				sys.stdout.write(code + '    ')
				for i in range(m_dp + 1):
					sys.stdout.write("%03i " % (mem[i]) )
				sys.stdout.write('\n')
				print " " * ip + '^' + ' ' * (c_len - ip) + '   ' + '    ' * dp + '^^^'
				sys.stdout.write('\n')

		output.write(buf_out)
		if self.return_output:
			output.seek(0)
			return(output.read())

if __name__ == "__main__":
	# Some self tests

	tests = (
		('helloworld', '++++++++++[>+++++++>++++++++++>+++>+<<<<-]>++.>+.+++++++..+++.>++.<<+++++++++++++++.>.+++.------.--------.>+.>.', '', 'Hello World!\n'),
		('divide1', ',>,>++++++[-<--------<-------->>]<<[>[->+>+<<]>[-<<-[>]>>>[<[>>>-<<<[-]]>>]<<]>>>+<<[-<<+>>]<<<]>[-]>>>>[-<<<<<+>>>>>]<<<<++++++[-<++++++++>]<.', '62', '3'),
		('divide2', ',>,>++++++[-<--------<-------->>]<<[>[->+>+<<]>[-<<-[>]>>>[<[>>>-<<<[-]]>>]<<]>>>+<<[-<<+>>]<<<]>[-]>>>>[-<<<<<+>>>>>]<<<<++++++[-<++++++++>]<.', '92', '4'),
	)

	for test in tests:
		output = Brainfuck(test[1], test[2]).run()
		if output != test[3]:
			print "Test %-20s: Failed. Output = %s" % ('\''+test[0]+'\'', output)
		else:
			print "Test %-20s: Success" % ('\''+test[0]+'\'')
