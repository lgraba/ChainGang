import socket
import sys

# Create TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect the socket to the port where the server is listening
server_address = ('localhost', 10000)
print("Connecting to {}:{}...".format(server_address))
sock.connect(server_address)

try:
	# Get and Send Data
	message = raw_input('Please enter your message to send to the server:\n')
	# message = 'This is a rather long message. I suppose it will be repeated. Logan is a pimp!'
	print("Sending '{}'".format(message))
	sock.sendall(message)

	# Gather Response
	amount_received = 0
	amount_expected = len(message)

	while amount_received < amount_expected:
		data = sock.recv(16)
		amount_received += len(data)
		print("Received '{}'".format(data))

finally:
	print("Closing Socket... ")
	sock.close()
	print("Complete!\n")