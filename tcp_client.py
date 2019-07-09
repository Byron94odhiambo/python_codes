import socket

target_host = "127.0.0.1"

target_port = 65432
# create a socket object u 
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
# connect the client v 
client.connect((target_host,target_port))
# send some data w 
client.send(b"GET / HTTP/1.1\r\nHost:127.0.0.1  \r\n\r\n")
# receive some data x 
response = client.recv(4096) 

print (response)
