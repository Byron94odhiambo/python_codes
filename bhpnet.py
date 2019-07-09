import sys
import socket
import getopt
import threading
import subprocess

# defining some global variable
listen                = False
command               = False
upload                = False
execute               = ""
target                = ""
upload_destination    = ""
port                  = 0
 

def usage():
    print ("BHP NET Tool")
    print ()
    print ("Usage:bhpnet.py -t target_host -p port")
    print ("-l --listen                        -listen on [host]:[port] for incoming connection")
    print ("-c --command                       -initialize a command shell")
    print ("-u -- upload=destination            -upon recieving a connection upload a file and write to [destination]")
    print ()
    print ("Examples: ")
    print ("bhpnet.py -t 192.168.0.1 -p 5555 -l -c")
    print ("bhpnet.py -t 192.168.0.1 -p 5555 -l -u=c:\\target.exe")
    print ("bhpnet.py -t 192.168.0.1 -p 5555 -l -e=  \"cat/etc/passwd""")
    print ("echo 'ABHCDEFGHI'./bhpnet.py -t 192.168.11.12 -p 135")
    sys.exit(0)
def main():
    global listen
    global port
    global execute
    global command
    global upload_destination
    global target

    if not len(sys.argv[1:]):
    	usage()

    # read the commandline options	
    try:
    	opts, arg = getopt.getopt(sys.argv[1:],"hle:t:p:cu:",["help", "listen","execute","target","port","command","upload"])

    except getopt.GetoptError as e:
    	print (e)
    	usage()

    for o, a in opts:
           if o in ("-h","--help"):
                  usage()
           elif o in ("-l","--listen"):
                  usage()       
           elif o in ("-e","--execute"):
                  execute= a 
           elif o in ("-c","--commandline"):
                  command=True             
           elif o in ("-u","--upload"):
                  upload_destination = a
           elif o in ("-u","--target"):
                  target = a
           elif o in ("-p","--port"):
                  port = int(a)
           else:
                  assert False, "Unhandled option"
    # are we goin to listen or just send data to stdin?
    if not listen and len(target) and port >0:

    	#read in the buffer from the commandline
    	#this will block, so send CTRL-D if not sending input
    	#to stdin
        buffer = sys.stdin.read()

        #send data off
        client_sender(buffer)

        #we are going to listen and potentially
        #upload things, execute commands and drop a shell back
        #depending on our commandline option above

    if listen:
    	   server_loop()

def client_sender(buffer):
  client = socket.socket(socket.AF_NET, socket.SOCKET_STREAM)
  try:
    client.connect((target,port))

    if len(buffer):
      client.send(buffer)

      while True:
        recv_len=1
        response=""

        
      while recv_len:
          data= client.recv_len(4096)
          recv_len= len(data)
          response+= data

          if recv_len<4096:
            break
      print (response)


      #wait for more input
      buffer = raw_input("")
      buffer+= "\n"    

          #send it off 
      client.send(buffer)
        

          
  except:
     print ("[*]Exeption! Exiting")
      #tear down connection
     client.close()



def server_loop():
  global target


  if not len(target):
    target = "0.0.0.0"

  serve = socket.socket(socket.AF_NET,socket.SOCKET_STREAM)

  server.bind((target,port))


  server.listen(5)

  while True:
    client_socket,addr = server.accept()
    client_thread = threading.Thread(target=client_handler,args =(client_socket))
    client_thread.start()



def run_command():
  command=command.rstrip()
  try:
    output=subprocess.check_output(command,stderr = subprocess.STDOUT, shell=True)
    
  except:
     output= "Failed to execute command.\r\n"

     return output

def client_handler(client_socket):
  global command
  global execute
  global upload

  if len(upload_destination):

    file_buffer=""

    while True:
      data = client_socket.recv(1024)

      if not data:
        break
      else:
        file_buffer+=data
    try:
       file_descriptor = open(upload_destination, "wb")
       file_descriptor.write(file_buffer)
       file_descriptor.close()
    except:
      client_socket.send("Failed to save file to %s\r\n" % upload_destination)


    if len(execute):

       #run the command
       output=run_command(execute)
       client_socket.send(output)
   #now we go into another loop if a command shell was requested
  if command:

         while True:
              #show a simple prompt
              client_socket.send("<BHP:#>")

                   #now we receive until we see a line field(enter key)
              cmd_buffer=""
              while "\n" not in cmd_buffer:
                      cmd_buffer+=client_socket.recv(1024)



              #send back the command output
              response= run_command(cmd_buffer)



              #send back the response
              client_socket.send(response)   


    	
















