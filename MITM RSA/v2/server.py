import socket
import sys

# Create a UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Bind the socket to the port
server_address = ('localhost', 10000)
print('starting up on {} port {}'.format(*server_address))
sock.bind(server_address)

var1 = ""
var2 = ""
var3 = ""
var4 = ""

while True:
    print('\nwaiting to receive message')
    data, address = sock.recvfrom(12000)

    a = data.decode("utf-8")
    b = a.split("+", 3)
    var1 = b[0] 
    var2 = b[1] 
    var3 = b[2]
    var4 = b[3]

    print(var1)
    var1 = var1 + ".txt"
    print(var2)
    print(var3)
    print(var4)

    f = open(var1, "w")
    f.write(var2)
    f.write("\n")
    f.write(var3)
    f.write("\n")
    f.write(var4)
    f.close()
    
    print('received {} bytes from {}'.format(
        len(data), address))
    print(data)

    if data:
        sent = sock.sendto(data, address)
        print('sent {} bytes back to {}'.format(
            sent, address))
