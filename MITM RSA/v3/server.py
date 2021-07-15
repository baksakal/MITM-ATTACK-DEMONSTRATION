import socket
import sys
import math

from Crypto.Cipher import AES

def countBits(number): 
      
    # log function in base 2  
    # take only integer part 
    return int((math.log(number) / 
                math.log(2)) + 1)

count = 0

sharedPrime = 1087    # p
sharedBase = 7      # g

clientSecret = 5      # b

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
ciphertext = ""
tag= ""
nonce = ""
# Bind the socket to the port
server_address = ('localhost', 10000)
print("SERVER-SERVER-SERVER-SERVER-SERVER-SERVER-SERVER-SERVER-SERVER-SERVER")
print('starting up on {} port {}'.format(*server_address))
sock.bind(server_address)

count = 0
buyukA = ""

while True:
    # Receive response
    print('waiting to receive\n')
    data, address = sock.recvfrom(12000)

    if data:
        print('received {!r}'.format(data))
        if count == 0:
            ciphertext = data
            sent = sock.sendto(data, address)
            count = count + 1
        elif count == 1:
            tag = data
            sent = sock.sendto(data, address)
            count = count +1
        elif count == 2:
            nonce = data
            sent = sock.sendto(data, address)
            count = count +1
        elif count == 3:
            buyukA = data
            sent = sock.sendto(data, address)
            count = count +1
            
    if count == 4:
        key = buyukA
        cipher = AES.new(key, AES.MODE_EAX, nonce=nonce)
        plaintext = cipher.decrypt(ciphertext)
        try:
            cipher.verify(tag)
            print("---------------------------------")
            print("DECRYPTING USING")
            print("Key:")
            print(key)
            print("Ciphertext:")
            print(ciphertext)
            print("Tag:")
            print(tag)
            print("Nonce:")
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
            
            filename1 = var1 + " - Sifreli.bin"
            filename2 = var1 + ".txt"
            
            f = open(filename1, "wb")
            f.write(plaintext)
            f.write(key)
            f.write(nonce)
            f.write(tag)
            f.close
            print("Incoming message written to a Binary File")
            
            f = open(filename2, "w")
            f.write(var2)
            f.write("\n")
            f.write(var3)
            f.write("\n")
            f.write(var4)
            f.close()
            print("Decrypted message written to a Txt File")
            

        except ValueError:
            print("Key incorrect or message corrupted")
            




