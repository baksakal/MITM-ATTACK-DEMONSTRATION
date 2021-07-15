import socket
import sys
import math
# pip install pycryptodome
# pip install pycryptodomex
from Crypto.Cipher import AES

def countBits(number): 
      
    # log function in base 2  
    # take only integer part 
    return int((math.log(number) / 
                math.log(2)) + 1)

count = 0

sharedPrime = 1087    # p
sharedBase = 7      # g

clientSecret = 13      # b

key = (sharedBase ** clientSecret) % sharedPrime

#the key has this many bits
#the key will be 128 bits so we will somehow add bits
bits_to_add = 16 - countBits(key)

#find the bit length of the key
lenof = len(("{0:b}".format(key)))

key = str(key)
res = len(key.encode('utf-8'))
# we should add 16-res characters
res = 16-res

for x in range(0, res):
    key += "1"
key = key.encode('utf-8')

# Create a UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

print("CLIENT-CLIENT-CLIENT-CLIENT-CLIENT-CLIENT-CLIENT-CLIENT-CLIENT-CLIENT")
server_address = ('localhost', 12000)

message = input("Isim ve soyisim: \n")
message = message + "+"
message = bytearray(message, 'utf-8')

card = input("Kredi karti numaraniz: \n")
card = card + "+"
card = bytearray(card, 'utf-8')

tarih = input("Gecerlilik suresi: \n")
tarih = tarih + "+"
tarih = bytearray(tarih, 'utf-8')

kod = input("Guvenlik kodu: \n")
kod = bytearray(kod, 'utf-8')

message.extend(card)
message.extend(tarih)
message.extend(kod)

#encrypt the message
#remember we already made the key

key = key
cipher = AES.new(key, AES.MODE_EAX)
nonce = cipher.nonce
ciphertext, tag = cipher.encrypt_and_digest(message)


#lets see if we can decrypt the message
#lets use our key
key = key
cipher = AES.new(key, AES.MODE_EAX, nonce=nonce)
plaintext = cipher.decrypt(ciphertext)

try:
  cipher.verify(tag)
  print("---------------------------------")
  print("DECRYPTING USING")
  print("Key:")
  print(key)
  print("Ciphertext")
  print(ciphertext)
  print("Tag")
  print(tag)
  print("Nonce")
  print(nonce)
  print("DECRPT SUCCESSFUL")
  print("---------------------------------\n")
  print("The message is authentic:", plaintext)
  a = plaintext.decode("utf-8")
  b = a.split("+", 3)
  var1 = b[0] 
  var2 = b[1] 
  var3 = b[2]
  var4 = b[3]
  print("Client Inputs:")
  print(var1)
  print(var2)
  print(var3)
  print(var4)
except ValueError:
    print("Key incorrect or message corrupted")

#first we will send the ciphertext and the tag
try:

    # Send data
    print('sending {!r}'.format(ciphertext))
    sent = sock.sendto(ciphertext, server_address)
    print('waiting to receive')
    data, server = sock.recvfrom(12000)
    print('received {!r}'.format(data))

    print('sending {!r}'.format(tag))
    sent = sock.sendto(tag, server_address)
    print('waiting to receive')
    data, server = sock.recvfrom(12000)
    print('received {!r}'.format(data))

    print('sending {!r}'.format(nonce))
    sent = sock.sendto(nonce, server_address)
    print('waiting to receive')
    data, server = sock.recvfrom(12000)
    print('received {!r}'.format(data))

    print('sending {!r}'.format(key))
    sent = sock.sendto(key, server_address)
    print('waiting to receive')
    data, server = sock.recvfrom(12000)
    print('received {!r}'.format(data))

finally:
    print('closing socket')
    sock.close()
