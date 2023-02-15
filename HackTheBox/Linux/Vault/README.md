### writeup
* https://0xdf.gitlab.io/2019/04/06/htb-vault.html

### Fuzzing and foothold
* https://github.com/A1vinSmith/OSCP-PWK/wiki#holy-war-on-fuzzing-tools

dave:Dav3therav3123

### Network Enumeration
##### Host Identification
```bash
dave@ubuntu:~$ ip a
2: ens192: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc mq state UP group default qlen 1000
    link/ether 00:50:56:b9:f5:72 brd ff:ff:ff:ff:ff:ff
    inet 10.129.87.83/16 brd 10.129.255.255 scope global ens192
       valid_lft forever preferred_lft forever
    inet6 dead:beef::250:56ff:feb9:f572/64 scope global mngtmpaddr dynamic 
       valid_lft 86396sec preferred_lft 14396sec
    inet6 fe80::250:56ff:feb9:f572/64 scope link 
       valid_lft forever preferred_lft forever
3: virbr0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc noqueue state UP group default qlen 1000
    link/ether fe:54:00:17:ab:49 brd ff:ff:ff:ff:ff:ff
    inet 192.168.122.1/24 brd 192.168.122.255 scope global virbr0
       valid_lft forever preferred_lft forever
4: virbr0-nic: <BROADCAST,MULTICAST> mtu 1500 qdisc pfifo_fast state DOWN group default qlen 1000
    link/ether 52:54:00:ff:fd:68 brd ff:ff:ff:ff:ff:ff
5: vnet0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc pfifo_fast master virbr0 state UNKNOWN group default qlen 1000
    link/ether fe:54:00:3a:3b:d5 brd ff:ff:ff:ff:ff:ff
    inet6 fe80::fc54:ff:fe3a:3bd5/64 scope link 
       valid_lft forever preferred_lft forever
6: vnet1: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc pfifo_fast master virbr0 state UNKNOWN group default qlen 1000
    link/ether fe:54:00:e1:74:41 brd ff:ff:ff:ff:ff:ff
    inet6 fe80::fc54:ff:fee1:7441/64 scope link 
       valid_lft forever preferred_lft forever
7: vnet2: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc pfifo_fast master virbr0 state UNKNOWN group default qlen 1000
    link/ether fe:54:00:c6:70:66 brd ff:ff:ff:ff:ff:ff
    inet6 fe80::fc54:ff:fec6:7066/64 scope link 
       valid_lft forever preferred_lft forever
8: vnet3: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc pfifo_fast master virbr0 state UNKNOWN group default qlen 1000
    link/ether fe:54:00:17:ab:49 brd ff:ff:ff:ff:ff:ff
    inet6 fe80::fc54:ff:fe17:ab49/64 scope link 
       valid_lft forever preferred_lft forever
       ```

So  there are hosts in the `192.168.122.0/24` range. I can see that my current host is the .1:
```bash
dave@ubuntu:~$ time for i in $(seq 1 254); do (ping -c 1 192.168.122.${i} | grep "bytes from" &); done
64 bytes from 192.168.122.1: icmp_seq=1 ttl=64 time=0.045 ms
64 bytes from 192.168.122.5: icmp_seq=1 ttl=64 time=0.539 ms 	<- Firewall
64 bytes from 192.168.122.4: icmp_seq=1 ttl=64 time=1.43 ms 	<- DNS + Configurator

real    0m0.371s
user    0m0.193s
sys     0m0.114s
```

### Firewall
Nothing there
```bash
time for i in $(seq 1 65535); do (nc -zvn 192.168.122.5 ${i} 2>&1 | grep -v "Connection refused" &); done
```

### DNS + Configurator
```bash
time for i in $(seq 1 65535); do (nc -zvn 192.168.122.4 ${i} 2>&1 | grep -v "Connection refused" &); done

Connection to 192.168.122.4 22 port [tcp/*] succeeded!
Connection to 192.168.122.4 80 port [tcp/*] succeeded!
```

* https://0xdf.gitlab.io/2019/04/06/htb-vault.html#shell-on-dns-as-root

I ened up using 2 ssh sesions to get the shell. One portfoward for burp socks proxy. The other is opening the nc listener.

new creds for `ssh dave@192.168.122.4`

```txt
dave
dav3gerous567
```

### SPICE
* https://0xdf.gitlab.io/2019/04/06/htb-vault.html#firewall-bypass
* https://en.wikipedia.org/wiki/Simple_Protocol_for_Independent_Computing_Environments