import time
import hashlib
import pickle
from collections import namedtuple

Tx = namedtuple("Tx", "input, output, time, comment")

class Transaction():
	""" Transaction: A class to parse and represent NutSwings (transactions) """

	# Initialize a new Transaction object from whatever string the user shit into the client or a bytes representation
	def __init__(self, line, tx_bytes = None):
		if (tx_bytes):
			# De-serialize into namedTuple and set self.transaction
			self.transaction = pickle.loads(tx_bytes)
		else:
			comment_part = None
			# Split on semicolon, if present
			if ";" in line:
				# Break up line by ; and get comment
				parts = line.split(';')
				tx_part = parts[0]
				comment_part = parts[1].strip()
			else:
				tx_part = line


			words = tx_part.split()
			send_array = ['Give', 'give', 'Send', 'send', 'Swing', 'swing']
			from_array = ['From', 'from']

			# Construct Transaction
			if (words[0] in send_array):
				self.receiver = words[1]
			if (words[2]):
				self.amount = float(words[2])
			if (words[3] in from_array):
				self.sender = words[4]

			self.transaction = Tx({self.sender:self.amount}, {self.receiver:self.amount}, time.time(), comment_part)

	# Return Printable on special function repr
	def __repr__(self):
		return str(self.transaction)

	# Return string
	def __str__(self):
		return str(self.transaction)

	def crush(self):
		c = hashlib.md5()
		for element in transaction.items():
			c.update(element.encode('utf-8'))
		return c.hexdigest()

	def byte_representation(self):
		tx = self.transaction
		serialized_tx = pickle.dumps(tx)
		return serialized_tx

	def unpickle_bytes(self, tx_bytes):
		return pickle.loads(tx_bytes)