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

def is_valid_password(password):
    """Ensure password is at least 8 characters and contains a number."""
    return len(password) >= 8 and any(char.isdigit() for char in password)

# register new user
def register():
    username = input("Enter a username: ")
    while not is_username_unique(username):
        print("Username already exists. Please choose another one.")
        username = input("Enter a username: ")

    password = input("Enter a password: ")

    while not is_valid_password(password):
        print("Password must be at least 8 characters long and include a number.")
        password = input("Enter a password: ")

    hashed_password = hash_password(password)

    # store user credentials 
    with open(USER_DATA_FILE, 'a') as file:
        file.write(f"{username},{hashed_password}\n")

    print("Registration successful!")

