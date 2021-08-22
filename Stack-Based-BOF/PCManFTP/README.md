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

Once we have both programs running, go into Immunity Debugger and click File > Attach and choose the PCManFTP program from the list and click "Attach." Next, click the Play arrow in the upper left - make sure the lower left corner says "Running".


*rest of article coming soon*




