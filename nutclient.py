import socket
import sys
import time

# Create TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect the socket to the port where the server is listening
server_address = ('localhost', 10000)
host, port = server_address
print("Connecting to {}:{}...".format(host, port))
sock.connect(server_address)

try:
	lines = []
	# Get and Send Data
	print("Please enter your transactions, one line at a time:\n")
	while True:
		line = input()
		if line:
			# Check for necessary components
			if "Give" not in line and "give" not in line:
				continue
			if "Send" not in line and "send" not in line:
				continue
			if ";" in line:
				# Break up line by ;
				parts = line.split(';')
				# Add time
				full_line = parts[0] + " at " + str(time.time()) + ";" + parts[1]
			else:
				full_line = line + " at " + str(time.time())

			lines.append(full_line)
		else:
			break
	message = '\n'.join(lines)

	print("Sending '{}'".format(message))
	sock.sendall(message.encode('utf-8'))

	# Gather Response
	amount_received = 0
	amount_expected = len(message)

	while amount_received < amount_expected:
		data = sock.recv(128)
		amount_received += len(data)
		print("Received '{}'".format(data))

finally:
	print("Closing Socket... ")
	sock.close()
	print("Complete!\n")