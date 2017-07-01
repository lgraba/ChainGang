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
		genesis_nut = self.readconfig()

		transaction = self.server.startListening()
		self.newBlock(genesis_nut, transaction)
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

	def newBlock(self, prev, new):
		print("We're going to make a new block with the following:\n")
		print(prev)
		print(new)

# MAIN
if __name__ == "__main__":
	a = NutChain('butthole')