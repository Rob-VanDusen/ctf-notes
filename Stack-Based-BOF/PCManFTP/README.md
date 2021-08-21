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
*rest of article coming soon*




