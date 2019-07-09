import socket

target_host = "192.168.43.214" 
target_port = 13
# create a socket object
client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# send some data 
client.sendto(b"aabbccddee",(target_host,target_port))
# receive some data w 
data, addr = client.recvfrom(4096)
 
print (data)
