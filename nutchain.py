# !/usr/bin/env python
# nutchain.py
# Just the pimpest nutchain in the world

import os
import hashlib
import configparser
import time
import nutserver
import transaction

class NutChain:
	"""NutChain: A super-sexy NutChain"""

	# Bytes
	leaf_byte = bytes(0)
	node_byte = bytes(1)
	version = '.01'
	difficulty = 1
	nonce = 0

	def __init__(self, root):
		# Attributes
		self.space = ''
		self._linelength = 30
		self._root = root
		self._mt = {}
		self._hashlist = {}
		self._tophash = ''

		# Start Server
		self.server = nutserver.NutServer()

		# Start Merkle Tree
		self.__MT__()

	# Create and print Merkel Sack from Config File
	def __MT__(self):
		# Initialize with Genesis Nut
		genesis_nut = self.readconfig()
		previous_nut = genesis_nut

		while True:
			txs = self.server.startListening()
			if (txs):
				previous_nut = self.newNut(previous_nut, txs)
				print(previous_nut)
		# print(genesis_nut)
		# self.HashList(self.genesis_nut)
		# self.PrintHashList()
		# self.MT()
		# print ("Merkle Tree for {}: ".format(self._root))
		# self.PrintMT(self._tophash)
		# self.line()
	
	def readconfig(self):
		self.Config = configparser.ConfigParser()
		self.Config.read("genesis.nut")
		header = self.configSectionMap('Header')
		transactions = self.configSectionMap('Transactions')
		accounts = self.configAccountMap('Accounts')

		data = {}
		data['header'] = header
		data['transactions'] = transactions
		data['accounts'] = accounts

		print("Genesis block read")
		self.line()

		return data

	def configSectionMap(self, section):
	    data = {}
	    options = self.Config.options(section)
	    for option in options:
	        try:
	            data[option] = self.Config.get(section, option)
	            if data[option] == -1:
	                DebugPrint("skip: %s" % option)
	        except:
	            print("exception on %s!" % option)
	            data[option] = None
	    return data

	def configAccountMap(self, section):
	    data = {}
	    options = self.Config.options(section)
	    for option in options:
	        try:
	            data[option] = float(self.Config.get(section, option))
	            if data[option] == -1:
	                DebugPrint("skip: %s" % option)
	        except:
	            print("exception on %s!" % option)
	            data[option] = None
	    return data

	def newNut(self, prev, new_transactions):
		self.line()
		print("We're going to make a new Nut with the following shit:")
		print("Previous Block: ")
		print(prev)
		print("New Transactions: ")

		# Unpack prev
		previous_header = prev['header']
		previous_transactions = prev['transactions']
		previous_accounts = prev['accounts']

		# New Transactions to add to New Nut
		transactions = {}

		# Loop through new transactions array
		for transaction in new_transactions:
			print(transaction)

			# Transaction specifics
			sender = transaction.sender
			amount = transaction.amount
			receiver = transaction.receiver

			# TODO: VERIFY TRANSACTION

			# Convert to bytes, hash
			m = hashlib.md5()
			m.update(transaction.byte_representation())
			tx_hash = m.hexdigest()

			# Subtract inputs from Previous Accounts
			if sender in previous_accounts:
				previous_accounts[sender] -= amount
			else:
				print("ERROR; No '" + sender + "' account to pull " + str(amount) + " from to transfer to " + receiver + "!")
				continue
			# Add outputs to Previous Accounts and New Accounts
			if receiver in previous_accounts:
				previous_accounts[receiver] += amount
			else:
				previous_accounts[receiver] = amount
				print("Created '" + receiver + "' account to receive " + str(amount) + " from " + sender + "!")

			# Add transactions from array to transactions dictionary -> (eventually) Transactions Section
			transactions[tx_hash] = transaction

		self.line()

		# Hash each tx_hash (keys of transactions dictionary)
		mh = hashlib.md5()
		for tx_hash, transaction in transactions.items():
			mh.update(tx_hash.encode('utf-8'))
		
		crush = mh.hexdigest()

		# Make pre_header
		pre_header = {
			'version':self.version,
			'previous':previous_header['hash'],
			'crush':crush,
			'time':time.time(),
			'difficulty':self.difficulty,
			'nonce':self.nonce
		}

		# Hash pre_header to get Nut Crush (Hash)
		ph = hashlib.md5()
		for element in pre_header:
			# print("Adding " + str(element) + " to Preheader hash")
			ph.update(element.encode('utf-8'))
		nut_hash = ph.hexdigest()

		# Header
		header = {
			'hash': nut_hash,
			'version':self.version,
			'previous':previous_header['hash'],
			'crush':crush,
			'time':time.time(),
			'difficulty':self.difficulty,
			'nonce':self.nonce
		}
		# print(header)

		# Balance Accounts
		accounts = previous_accounts

		# Make Nut
		nut = {}
		nut['header'] = header
		nut['transactions'] = transactions
		nut['accounts'] = accounts
		
		return nut # New nut

	def line(self):
		print(self._linelength*'-')

# MAIN
if __name__ == "__main__":
	a = NutChain('butthole')