# !/usr/bin/env python
# nutchain.py
# Just the pimpest nutchain in the world

import os
import hashlib
import configparser
import time
import nutserver

class NutChain:
	"""NutChain: A super-sexy NutChain"""

	# Bytes
	leaf_byte = bytes(0)
	node_byte = bytes(1)
	version = '.01'

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
		# print(genesis_nut)
		# self.HashList(self.genesis_nut)
		# self.PrintHashList()
		# self.MT()
		# print ("Merkle Tree for {}: ".format(self._root))
		# self.PrintMT(self._tophash)
		# self.Line()
	
	def readconfig(self):
		self.Config = configparser.ConfigParser()
		self.Config.read("genesis.nut")
		header = self.configSectionMap('Header')
		transactions = self.configSectionMap('Transactions')
		accounts = self.configSectionMap('Accounts')

		data = {}
		data['header'] = header
		data['transactions'] = transactions
		data['accounts'] = accounts

		print("Genesis block read")

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

	def newNut(self, prev, new_transactions):
		print("We're going to make a new Nut with the following shit:\n")
		print(prev)
		print(new_transactions)
		print("\n\n")

		# Vars
		transactions = {}

		# Loop through new transactions array
		for transaction in new_transactions:
			# Convert to bytes, hash
			m = hashlib.md5()
			m.update(transaction)
			tx_hash = m.hexdigest()

			# Add strings from array to transactions dictionary -> (eventually) Transactions Section
			transactions[tx_hash] = transaction

		# Hash each tx_hash (keys of transactions dictionary)
		mh = hashlib.md5()
		for tx_hash, transaction in transactions.items():
			mh.update(tx_hash.encode('utf-8'))
		
		crush = mh.hexdigest()
		print("Crush: " + crush + "\n")
		print(transactions)

		# Make Header
		# header = {'version':self.version,}

		# Make Block
		# data = {}
		# data['header'] = header
		# data['transactions'] = transactions
		# data['accounts'] = accounts
		# 
		# return data # New nut

# MAIN
if __name__ == "__main__":
	a = NutChain('butthole')