import random

def generate_user_id(role):
    prefix_name = {
        "admin": "AD",
        "analyst": "AN",
        "viewer": "VI"
    }
    prefix = prefix_name.get(role.lower())
    number = random.randint(10000, 99999)
    return f"{prefix}{number}"