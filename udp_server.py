import socket

# create a socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)


#bind it to localhost and a port

sock.bind(("127.0.0.1",6001))
print("[udp server] listening on 127.0.0.1:6001")


# receive and reply forever


while True:

	data,addr = sock.recvfrom(1024) #wait for a packet
	print("[udp server] from ", addr, ":", data.decode().strip())

	#send response back to sender
	sock.sendto(b"echo:" + data,addr)


