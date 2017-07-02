import socket
import sys
import time
import pickle
import transaction

class NutServer:
	""" NutServer: Logan's super sexy Server built to accept transactions to add to the Nutchain"""

	# Server Configuration Parameters
	server_address = ('localhost', 10000)

	def __init__(self):
		# Create TCP/IP Socket
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

		# Bind socket to port
		host, port = self.server_address
		print("Starting up server...\nHost: {}\nPort: {}\n".format(host, port))
		self.sock.bind(self.server_address)

	def startListening(self):
		# Listen (1 connection at a time)
		self.sock.listen(1)
		# Any received transactions
		transactions = []
		done_loopin = False

		# Loop
		while not done_loopin:
			# Wait for connection
			print("Waiting for a connection...\n")
			connection, client_address = self.sock.accept()

			try:
				print("Connection from {}".format(client_address))

				t_list = b''
				# Receive Data
				while True:
					data = connection.recv(4096)
					# Current UNIX timestamp
					data_time = time.time()
					# print("Received '{}'".format(data))

					if data:
						# print("Sending data back to client for confirmation.")
						connection.sendall(data)

						# Test
						# test_data1 = "Give Sarah 10n from Logan"
						# test_data2 = "Give Sarah 10n from Logan; What a gal!"
						t_list += data
						# print("Added data to t_list")
						
					else:
						print("No more data from {}, the filthy animal!".format(client_address))
						break

				# Split Transactions on bytes
				split_data = t_list.split(b'\x80\x03')
				# Add each Transaction object to transactions array
				for tx_data in split_data:
					if tx_data:
						received_tx = transaction.Transaction(None, tx_data)
						transactions.append(received_tx)
				
			finally:
				# Clean Up!
				connection.close()
				done_loopin = True

		# Check Transactions for Validity
		check = self.checkTransactions(transactions)
		if (check):
			print("The following transactions were fucked:\n")
			print(check)
			return False

		# Return Transactions array
		if (transactions):
			print("Submitting transactions to NutChain")
			return transactions
		else:
			print("No transactions received")
			return False

	# checkTransactions()
	# Eventually we'll need to verify that the data we're receiving are actually transactions
	def checkTransactions(self, txs):
		# print(txs)
		return False
