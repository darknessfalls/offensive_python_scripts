from pwn import *
import sys

if len(sys.argv) != 2:# checking for 2 command line arguments
    print("Invalid arguments!")
    print(">> {} <sha256sum>".format(sys.argv[0]))# [0] is the filename of this file
    exit()

wanted_hash = sys.argv[1]# input value/hash we want to crack
print(wanted_hash)
password_file = ""
attempts = 0
# ALWAYS DECODE WHAT YOU ENCODE!!
with log.progress("Attempting to crack: {}!\n".format(wanted_hash)) as p:# our hash cracking job
  with open(password_file, "r", encoding='latin-1') as password_list:
    for password in password_list:
      password = password.strip("\n").encode('latin-1')# important to remove newline
      password_hash = sha256sumhex(password)# hashing passwords in our list
      p.status("[{}] {} == {}".format(attempts, password.decode('latin-1'), password_hash))
      if password_hash == wanted_hash:
        p.success("Password hash found after {} attempts! {} hashes to {}!".format(attempts, password.decode('latin-1'), password_hash))
        exit()
      attempts += 1
    p.failure("Password hash not found")# if we don't crack the hash