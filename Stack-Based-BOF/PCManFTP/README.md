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
I'm fairly certain we can overload the username field and crash the program, so we are going to use a python script to do so. In the file *fuzzer1.py* we will use a socket connection to send the username as an increasingly large number of "A's" until we crash the program. Each time the process runs it send the username as a string of A's and then the word pass for the password before disconnecting and telling us hw many characters it sent. Eventually the program will crash and we'll have a good idea of how many characters to send to cause the crash.

*rest of article coming soon*




