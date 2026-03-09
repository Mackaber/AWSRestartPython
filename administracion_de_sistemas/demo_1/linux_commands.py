import importlib
import os
import subprocess

def reload():
    importlib.reload(os.path)

def new_user():
    confirm = "N"
    while confirm != "Y":
        username = input("Enter the name of the user to add: ")
        print(f"Use the username {username} ? (Y/N)")
        confirm = input().upper()
    os.system(f"sudo adduser {username}")

def remove_user():
    confirm = "N"
    while confirm != "Y":
        username = input("Enter the name of the user to remove: ")
        print(f"Use the username {username} ? (Y/N)")
        confirm = input().upper()
    os.system(f"sudo userdel -r {username}")

def add_user_to_group():
    # (1)
    username = input("Enter the name of the user that you want to add to a group: ")
    output = subprocess.Popen('groups', stdout=subprocess.PIPE).communicate()[0]
    output = output.decode("utf-8")
    print("Enter a list of groups to add the user to")
    print("The list should be separated by spaces, for example:\r\n group1 group2 group3")
    print(f"The available groups are:\r\n {output}")
    chosenGroups = str(input("Groups: "))    
    # (2)
    output = output.strip().split(" ")
    chosenGroups = chosenGroups.split(" ")
    print("Add to:")
    found = True
    groupString=""
    # (3)
    for grp in chosenGroups:
        for existingGrp in output:
            if grp == existingGrp:
                found = True
                print(f"- Existing group: {grp}")
                groupString = groupString + grp + ","
        if found == False:
            print(f"- New group: {grp}")
            groupString = groupString + grp + ","
            found = True
        else:
            found = False
    # (4)
    groupString = f"{groupString[:-1]} " 
    confirm = ""
    while confirm != "Y" and confirm != "N":
        print(f"Add the user {username} to the following groups: {groupString}? (Y/N)")
        confirm = input().upper()
    if confirm == "N":
        print(f"User {username} not added to groups {groupString}")
    elif confirm == "Y":
        #breakpoint()
        os.system(f"sudo usermod -aG {groupString} {username}")
        print(f"User {username} added to groups {groupString}")


def install_or_remove_packages():
    # (1)
    iorR = ""
    while iorR != "I" and iorR != "R":
        print("Would you like to install or remove packages? (I/R)")
        iorR = input().upper()
    if iorR == "I":
        iorR = "install"
    elif iorR == "R":
        iorR = "remove"
    
    breakpoint()

    # (2)
    print("Enter a list of packages to install")
    print("The list should be separated by spaces, for example:")
    print(" package1 package2 package3")
    print(f"Otherwise, input 'default' to {iorR} the default packages listed in this program")
    packages = input().lower()
    
    if packages == "default":
        packages = "vim tmux htop" # Default packages
        
    if iorR == "install":
        os.system("sudo apt-get install " + packages)
        breakpoint()

    #(3)
    elif iorR == "remove":
        while True:
            print("Purge files after removing? (Y/N)")
            choice = input().upper()
            if choice == "Y":
                os.system("sudo apt-get --purge " + iorR + " " + packages)
                break
            elif choice == "N":
                os.system("sudo apt-get " + iorR + " " + packages)
                break
        os.system("sudo apt autoremove")
    
    breakpoint()

# (4)
def clean_environment():
    os.system("sudo apt-get autoremove")
    os.system("sudo apt-get autoclean")

#(5)
def update_environment():
    os.system("sudo apt-get update")
    os.system("sudo apt-get upgrade")
    os.system("sudo apt-get dist-upgrade")