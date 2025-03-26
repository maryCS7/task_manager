import os
import json
import hashlib

USER_DATA_FILE = 'user_data.txt'
TASKS_FILE = 'tasks.json'

# create user and task files for storing data
if not os.path.exists(USER_DATA_FILE):
    open(USER_DATA_FILE, 'w').close()

if not os.path.exists(TASKS_FILE):
    with open(TASKS_FILE, 'w') as file:
        json.dump({}, file)

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def is_username_unique(username):
    # check if user name exists 
    if not os.path.exists(USER_DATA_FILE):
        return True  

    with open(USER_DATA_FILE, 'r') as file:
        for line in file:
            stored_username, _ = line.strip().split(',')
            if stored_username == username:
                return False  # username exists
    return True  # username available

# add for password security 
def is_valid_password(password):
    return len(password) >= 8 and any(char.isdigit() for char in password)

# register new user
def register():
    username = input("Enter a username: ")
    while not is_username_unique(username):
        print("🚨 Oops! That username is already taken. Time to unleash your creativity and pick a unique one! 🌟")
        username = input("✨ Pick an awesome username: ")

    password = input("🛡️ Enter a strong password: ")
    while not is_valid_password(password):
        print("🔒 Let's level up your security game! Your password needs to be at least 8 characters long and have a sneaky number hidden in it. 😉")
        password = input("🛡️ Enter a strong password: ")

    hashed_password = hash_password(password)

    # store user credentials 
    with open(USER_DATA_FILE, 'a') as file:
        file.write(f"{username},{hashed_password}\n")

    print("🎉 Success! Your setup is complete. Are you ready to conquer your tasks like a pro? 🚀")

# validate user credentials - check stored data
def validate_credentials(username, password):
    hashed_password = hash_password(password) 

    if not os.path.exists(USER_DATA_FILE):  
        return False  # no user
    
    with open(USER_DATA_FILE, 'r') as file:
        for line in file:
            stored_username, stored_password = line.strip().split(',')
            if stored_username == username and stored_password == hashed_password:
                return True  # successful login
    return False  # login failed - invalid credentials

# login a user
def login():
    # limit attempts for app like expeience and security practice
    attempts = 3
    while attempts > 0:
        username = input("👤 What's your username? ")
        password = input("🔑 Password, please: ")

        if validate_credentials(username, password):
            print("🎉 Success! Are you ready to conquer your tasks like a pro? 🚀")
            return username  
        
        attempts -= 1
        print(f"Invalid username or password. {attempts} attempts remaining.")
    
    print("🚫 Too many failed attempts! Looks like it's time to call in reinforcements. We're here to help—reach out! 👋")
    return None



  

