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


*rest of article coming soon*




