import socket
import sys
import time

class NutServer:
	""" NutServer: Logan's super sexy Server built to accept transactions to add to the Nutchain"""

	# Server Configuration Parameters
	server_address = ('localhost', 10000)

	def __init__():
		# Create TCP/IP Socket
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

		# Bind socket to port
		print("Starting up server...\nHost: {}\nPort: {}\n".format(server_address))
		self.sock.bind(server_address)

	def startListening():
		# Listen (1 connection at a time)
		self.sock.listen(1)
		# Any received transactions
		transactions = {}

		# Loop
		while !transactions:
			# Wait for connection
			print("Waiting for a connection...\n")
			connection, client_address = self.sock.accept()

			try:
				print("Connection from ".format(client_address))

				# Receive Data
				while !transactions:
					data = connection.recv(16)
					# Current UNIX timestamp
					data_time = time.time()
					print("Received '{}'".format(data)

					if data:
						print("Sending data back to client...\n")
						connection.sendall(data)

						# Test
						test_data = "Give Sarah 10n from Logan at " + data_time + "; What a gal!"
						print("Submitting to NutChain")
						transactions.update({1:test_data})
					else:
						print("No more data from ".format(client_address))
						break
			finally:
				# Clean Up!
				connection.close()

		return transactions