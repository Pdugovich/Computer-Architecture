"""CPU functionality."""

import sys

class CPU:
	"""Main CPU class."""

	def __init__(self):
		"""Construct a new CPU."""
		# Looking further down the file, I can see what they expect to be here
		# We need a register which they expect to be self.reg, which holds 8
		self.reg = [0] * 8
		# We need memory, which looks like they expect to be self.ram
		self.ram = [0] * 256
		# Probably a program counter also
		self.pc = 0
		self.operations = {
			0b00000001: self.HALT,
			0b10100000: self.ADD,
			0b10100001: self.SUB,
			0b10100010: self.MUL,
			0b10100011: self.DIV,
			0b10100100: self.MOD,

			0b01100101: self.INC, 
			0b01100110: self.DEC,

			0b10100111: self.CMP,

			0b10101000: self.AND,
			0b01101001: self.NOT,
			0b10101010: self.OR,
			0b10101011: self.XOR,
			0b10101100: self.SHL,
			0b10101101: self.SHR,

			
			01010000: 'CALL',
			00010001: 'RED',

			01010010: 'INT',
			00010011: 'IRET'

			01010100 
			01010101 
			01010110 
			01010111 
			01011000 
			01011001 
			01011010 
		}
	
	def HALT(self):
		running = False

	def ram_read(self, address):
		return self.ram[address]

	def ram_write(self, to_write, address):
		self.ram[address] = to_write

	def load(self):
		"""Load a program into memory."""
		program_filename = sys.argv[1]
		
		# Making sure the file is the right type
		if program_filename[-4:] == '.ls8':
			# Just a counter to keep track of where we're writing the program
			write_at_address = 0
			with open(program_filename) as f:
				for line in f:
					line = line.split('#')
					line = line[0].strip()

					if line == '':
						continue
					# Converting to a binary. Nums are the same under the hood
					self.ram[write_at_address] = int(line,2)

					write_at_address += 1
		else:
			raise Exception("Unsupported file type. File name must end with .ls8")


	def alu(self, op, reg_a, reg_b):
		"""ALU operations."""

		if op == "ADD":
			self.reg[reg_a] += self.reg[reg_b]
		#elif op == "SUB": etc
		else:
			raise Exception("Unsupported ALU operation")

	def trace(self):
		"""
		Handy function to print out the CPU state. You might want to call this
		from run() if you need help debugging.
		"""

		print(f"TRACE: %02X | %02X %02X %02X |" % (
			self.pc,
			#self.fl,
			#self.ie,
			self.ram_read(self.pc),
			self.ram_read(self.pc + 1),
			self.ram_read(self.pc + 2)
		), end='')

		for i in range(8):
			print(" %02X" % self.reg[i], end='')

		print()

	def run(self):
		"""Run the CPU."""
		self.pc = 0
		running = True
		while running == True:
			# Read the memory stored at current pc
			# Store that value in Instruction Register(IR)
			ir = self.ram_read(self.pc)

			# Using ram_read(), store bytes pc+1 and + 2
			# into variables operand_a and b in case
			# the instructions call for them
			operand_a = self.ram_read(self.pc + 1)
			operand_b = self.ram_read(self.pc + 2)

			# Then, depending(if) on the opcode, perform
			# the action 
			if ir == 0b00000001:
				running = False
			elif ir == 0b10000010:
				self.reg[operand_a] = operand_b
				self.pc += 3
			elif ir == 0b01000111:
				print(self.reg[operand_a])
				self.pc +=2
			elif ir == 0b10100010:
				self.reg[operand_a] = self.reg[operand_a] * self.reg[operand_b]
				self.pc += 3

			# Then, increment PC appropriately.
			# The number of bytes an instruction uses
			# can be determined from bits 6 and 7 
			# in instruction opcode. See ls8 specs
