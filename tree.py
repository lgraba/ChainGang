# !/usr/bin/env python
# tree.py
# A Merkel Tree class


import os
import hashlib

class Tree:
	"""LoganTree: A super-sexy Merkel Tree"""

	# __INIT__()
	# Initialize a new Tree from Directory root
	def __init__(self, root):
		self.space = ''
		self._linelength = 30
		self._root = root
		self._mt = {}
		self._hashlist = {}
		self._tophash = ''
		self.__MT__()

	# __MT__()
	# Create and print Merkel Tree from Directory Structure
	def __MT__(self):
		self.HashList(self._root)
		self.PrintHashList()
		self.MT()
		print ("Merkle Tree for {}: ".format(self._root))
		self.PrintMT(self._tophash)
		self.Line()

	# HashList()
	# Create a Hashlist entry for each item found in the directory structure
	def HashList(self, rootdir):
		self.HashListChild(rootdir)
		items = self.GetItems(rootdir)
		if not items:
			self._hashlist[rootdir] = ''
			return
		s = ''
		for subitem in items:
			subitem = os.path.join(rootdir, subitem)
			s = s + self._hashlist[subitem]
		self._hashlist[rootdir] = self.md5sum(s)

	def PrintHashList(self):
		self.Line()
		for item, itemhash in self._hashlist.items():
			print ("{} {}".format(itemhash, item))
		self.Line()
		return

	# MT()
	# Create Merkel Tree from HashList
	def MT(self):
		for node, hash in self._hashlist.items():
			items = self.GetItems(node)
			value = []
			value.append(node)
			list = {}
			for item in items:
				if node == self._root:
					list[self._hashlist[os.path.join(node, item)]] = os.path.join(node, item)
				else: 
					list[self._hashlist[os.path.join(node, item)]] = os.path.join(node, item)
			value.append(list)
			self._mt[hash] = value
		self._tophash = self._hashlist[self._root]

	def PrintMT(self, hash):
		value = self._mt[hash]
		item = value[0]
		child = value[1]
		# print ("{} {}".format(hash, item))
		if not child:
			return
		for itemhash, item in child.items():
			self.space += '    '
			print ("{}-> {} {}".format(self.space, itemhash, item))
			self.PrintMT(itemhash)
			self.space = self.space[:-4]

	def Line(self):
		print (self._linelength*'-')

	# GetItems()
	# Get all items in a given directory
	def GetItems(self, directory):
		value = []
		if os.path.isdir(directory):
			items = os.listdir(directory)
			for item in items:
				value.append(item)
			value.sort()
		return value

	# md5sum()
	# Create an md5 checksum from directory path or file.
	# This serves as a hash for any given object represented.
	def md5sum(self, data):
		m = hashlib.md5()
		fn = data
		if os.path.isfile(fn):
			try:   
				f = open(fn, 'rb')
			except:
				return "ERROR: unable to open {}".format(fn)
			while True:
				d = f.read(8096)
				if not d:
					break
				m.update(d)
			f.close()
		else:
			m.update(data.encode('utf-8'))
		return m.hexdigest()

	# HashListChild()
	# The recursive function that builds a HashList from
	# the directory structure supplied. Note HashList contains
	# full directory paths.
	def HashListChild(self, rootdir):
		items = self.GetItems(rootdir)
		if not items:
			self._hashlist[rootdir] = ''
			return
		for item in items:
			itemname = os.path.join(rootdir, item)
			# print("{} => {}".format(item, itemname))

			if os.path.isdir(itemname): # Neds to be full path from /testA/, or it won't return TRUE
				self.HashListChild(itemname)
				subitems = self.GetItems(itemname)

				s = ''
				for subitem in subitems:
					s = s + self._hashlist[os.path.join(itemname, subitem)]
				self._hashlist[itemname] = self.md5sum(s)
			else:
				self._hashlist[itemname] = self.md5sum(itemname)

# MTDiff()
# Get the differences between two directory path generated Merkel Trees
def MTDiff(mt_a, a_tophash, mt_b, b_tophash):
	if a_tophash == b_tophash:
		print ("Top hash is equal for {} and {}".format(mt_a._root, mt_b._root))
	else:
		a_value = mt_a._mt[a_tophash] 
		a_child = a_value[1]    # Retrieve child list for MT A
		b_value = mt_b._mt[b_tophash] 
		b_child = b_value[1]    # Retrieve child list for MT B

	for itemhash, item in a_child.items():
		try:
			if b_child[itemhash] == item:
				print ("Info: SAME : {}".format(item))
		except:
			print ("Info: DIFFERENT : {}".format(item))
		temp_value = mt_a._mt[itemhash]
		if len(temp_value[1]) > 0:      # Directory?
			diffhash = list(set(b_child.keys()) - set(a_child.keys()))
			if diffhash:
				MTDiff(mt_a, itemhash, mt_b, diffhash[0])

# MAIN
if __name__ == "__main__":
	mt_a = Tree('testA')
	print (mt_a._mt)
	mt_b = Tree('testB')
	MTDiff(mt_a, mt_a._tophash, mt_b, mt_b._tophash)