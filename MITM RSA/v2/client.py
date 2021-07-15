import socket
import sys

# Create a UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

server_address = ('localhost', 12000)
#message = b'This is the message.  It will be repeated.'

message = input("enter name \n")
message = message + "+"
message = bytearray(message, 'utf-8')

card = input("enter card \n")
card = card + "+"
card = bytearray(card, 'utf-8')

tarih = input("enter tarih \n")
tarih = tarih + "+"
tarih = bytearray(tarih, 'utf-8')

kod = input("enter kod \n")
kod = bytearray(kod, 'utf-8')

message.extend(card)
message.extend(tarih)
message.extend(kod)

try:

    # Send data
    print('sending {!r}'.format(message))
    sent = sock.sendto(message, server_address)

    # Receive response
    print('waiting to receive')
    data, server = sock.recvfrom(12000)
    print('received {!r}'.format(data))

finally:
    print('closing socket')
    sock.close()
