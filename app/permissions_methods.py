import json, os
from pathlib import Path
from .models import *


def get_permissions():
    with open("C:/Users/Nathan/Desktop/Python Projects/ServerMusicAddHost/app/static/permissions.json", "r") as file:
        permissions = json.load(file)
    return permissions

def delete_permissions():
    os.remove(Path("C:/Users/Nathan/Desktop/Python Projects/ServerMusicAddHost/app/static/permissions.json"))

def create_permissions_file(permissions_data):
    try:
        with open("C:/Users/Nathan/Desktop/Python Projects/ServerMusicAddHost/app/static/permissions.json", "w") as file:
            json.dump(permissions_data, file, indent=4)
    except IOError:
        print(IOError)
        print(permissions_data)

def update_permissions(users, blacklist, whitelist, emails, general):
    permissions_data = {
        "users": users,
        "blacklist": blacklist,
        "whitelist": whitelist,
        "emails": emails,
        "general": general
    }
    old_permissions = get_permissions()
    delete_permissions()
    try:
        create_permissions_file(permissions_data=permissions_data)
    except:
        create_permissions_file(permissions_data=old_permissions)

def update_users(users):
    permissions = get_permissions()
    update_permissions (
        users=users,
        blacklist=permissions["blacklist"],
        whitelist=permissions["whitelist"],
        emails=permissions["emails"],
        general=permissions["general"]
    )

def update_blacklist(blacklist):
    permissions = get_permissions()
    update_permissions (
        users=permissions["users"],
        blacklist=blacklist,
        whitelist=permissions["whitelist"],
        emails=permissions["emails"],
        general=permissions["general"]
    )

def update_whitelist(whitelist):
    permissions = get_permissions()
    update_permissions (
        users=permissions["users"],
        blacklist=permissions["blacklist"],
        whitelist=whitelist,
        emails=permissions["emails"],
        general=permissions["general"]
    )

def update_emails(emails):
    permissions = get_permissions()
    update_permissions (
        users=permissions["users"],
        blacklist=permissions["blacklist"],
        whitelist=permissions["whitelist"],
        emails=emails,
        general=permissions["general"]
    )

def update_general(general):
    permissions = get_permissions()
    update_permissions (
        users=permissions["users"],
        blacklist=permissions["blacklist"],
        whitelist=permissions["whitelist"],
        emails=permissions["emails"],
        general=general
    )

def register_email(email):
    registered_email = {
        "email": email,
        "registered": True
    }
    permissions = get_permissions()
    old_emails = permissions["emails"]
    new_emails = [
        registered_email
    ]
    for old_email in old_emails:
        if old_email["email"] != email:
            new_emails.append(old_email)
    update_emails(emails=new_emails)

def add_user(user, email):
    new_user = {
        "username": user,
        "allow_settings": False,
        "admin": False,
        "email": email
    }
    permissions = get_permissions()
    old_users = permissions["users"]
    new_users = [
        new_user
    ]
    for old_user in old_users:
        if old_user["username"] != user:
            new_users.append(old_user)
    update_users(users=new_users)
    register_email(email=email)

def get_users():
    permissions = get_permissions()
    return permissions["users"]

def get_user(username):
    users = get_users()
    for user in users:
        if user["username"].lower() == username.lower():
            return user
        
def get_username_from_email(email):
    users = get_users()
    for user in users:
        if user["email"].lower() == email.lower():
            return user["username"]

def get_general_settings():
    permissions = get_permissions()
    return permissions["general"]

def get_admin_status(username):
    users = get_users()
    for user in users:
        if user["username"].lower() == username.lower():
            return user["admin"]
        
        
def get_user_settings_status(username):
    users = get_users()
    for user in users:
        if user["username"].lower() == username.lower():
            return user["allow_settings"]
        
def get_bitrate_settings_status():
    general_settings = get_general_settings()
    return general_settings["allow_bitrate"]
        
def allow_user(user) -> bool:
    general_settings = get_general_settings()
    permissions = get_permissions()
    blacklist = permissions["blacklist"]
    whitelist = permissions["whitelist"]
    user_exists = Users.query.filter_by(username=user).first()

    if user_exists:
        if general_settings["enable_blacklist"]:
            for bl_user in blacklist:
                if bl_user["username"].lower() == user.lower():
                    return False
        if general_settings["enable_whitelist"]:
            for wl_user in whitelist:
                if wl_user["username"].lower() == user.lower():
                    return True
                
        return True
