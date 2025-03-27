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
    confirm_password = input("🔑 Confirm your password: ")
    while password != confirm_password:
        print("🚨 Passwords do not match! Please re-enter.")
        password = input("🛡️ Enter a strong password: ")
        confirm_password = input("🔑 Confirm your password: ")
    while not is_valid_password(password):
        print("🔒 Let's level up your security game! Your password needs to be at least 8 characters long and have a sneaky number hidden in it. 😉")
        password = input("🛡️ Enter a strong password: ")

    hashed_password = hash_password(password)

    # store user credentials 
    with open(USER_DATA_FILE, 'a') as file:
        file.write(f"{username},{hashed_password}\n")

    print("🎉 Success! Your setup is complete. Are you ready to conquer your tasks like a pro? 🚀")
    task_manager(username)

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

# get tasks for a logged-in user
def get_user_tasks(username):
    if not os.path.exists(TASKS_FILE):
        return []
    with open(TASKS_FILE, 'r') as file:
        tasks = json.load(file)
    return tasks.get(username, [])

def view_tasks(username):
    tasks = get_user_tasks(username)
    if tasks:
        print()
        print("📋 Your tasks:")
        for i, task in enumerate(tasks, start=1):
            print(f"{i}. {task['description']} - {'✅ Completed' if task['status'] == 'Completed' else '🕓 Pending'}")
    else:
        print()
        print("✨ No tasks found. Start adding some and stay productive!")

# login a user
def login():
    attempts = 3
    while attempts > 0:
        username = input("👤 What's your username? ")
        password = input("🔑 Password, please: ") 

        if validate_credentials(username, password):
            print("🎉 Success! Are you ready to conquer your tasks like a pro? 🚀")
            # check and display tasks
            view_tasks(username)
            task_manager(username)
            return username
        
        attempts -= 1
        print(f"Invalid username or password. {attempts} attempts remaining.")
    
    print("🚫 Too many failed attempts! Looks like it's time to call in reinforcements. We're here to help—reach out! 👋")
    return None

# enter the task manager menu
def task_manager(username):
    while True:
        print("\n📋 Task Manager Options:")
        print("1. Add a Task")
        print("2. View Tasks")
        print("3. Mark a Task as Completed")
        print("4. Delete a Task")
        print("5. Logout")

        choice = input("Choose an option (1-5): ")
        if choice == "1":
            add_task(username)  
        elif choice == "2":
            view_tasks(username)  
        elif choice == "3":
            mark_task_completed(username)  
        elif choice == "4":
            delete_task(username)  
        elif choice == "5":
            print("👋 Logging out. See you next time!")
            break
        else:
            print("❗ Invalid choice. Please try again.")


# add task
def add_task(username):
    task_description = input("📝 What's the task you want to add? ")
    task_id = str(hash(task_description + username))  # generate task ID

    # create new task
    new_task = {
        "id": task_id,
        "description": task_description,
        "status": "Pending"
    }
    # load tasks from the file
    with open(TASKS_FILE, 'r') as file:
        tasks = json.load(file)
    # add the task to the user's list
    if username not in tasks:
        tasks[username] = []
    tasks[username].append(new_task)
    # save updated tasks back to the file
    with open(TASKS_FILE, 'w') as file:
        json.dump(tasks, file, indent=4)
    print(f"✅ Task added successfully: \"{task_description}\"")

# mark task completed
def mark_task_completed(username):
    tasks = get_user_tasks(username)
    if not tasks:
        print("✨ No tasks found to mark as completed!")
        return

    view_tasks(username)  # Show tasks to pick from
    task_input = input("Enter the task number to mark as completed or press Enter to return to the menu: ")

    if task_input == "":  
        print("🔙 Returning to the task menu...")
        return

    try:
        task_number = int(task_input)  # Convert the input to an integer
        if 1 <= task_number <= len(tasks):  # Validate the task number
            tasks[task_number - 1]["status"] = "Completed"
            with open(TASKS_FILE, 'r') as file:
                all_tasks = json.load(file)
            all_tasks[username] = tasks
            with open(TASKS_FILE, 'w') as file:
                json.dump(all_tasks, file, indent=4)
            print("✅ Task marked as completed!")
        else:
            print("❗ Invalid task number!")
    except ValueError:  # handle non-integer inputs
        print("❗ Please enter a valid number!")


# delete a task
def delete_task(username):
    tasks = get_user_tasks(username)
    if not tasks:
        print("✨ No tasks found to delete!")
        return

    view_tasks(username)  # show tasks to pick from
    task_input = input("Enter the task number to delete or press Enter to return to the menu: ")

    if task_input == "":
        print("🔙 Returning to the task menu...")
        return

    try:
        task_number = int(task_input)  
        if 1 <= task_number <= len(tasks):  #
            deleted_task = tasks.pop(task_number - 1)
            with open(TASKS_FILE, 'r') as file:
                all_tasks = json.load(file)
            all_tasks[username] = tasks
            with open(TASKS_FILE, 'w') as file:
                json.dump(all_tasks, file, indent=4)
            print(f"🗑️ Task deleted: \"{deleted_task['description']}\"")
        else:
            print("❗ Invalid task number!")
    except ValueError: 
        print("❗ Please enter a valid number!")



  

