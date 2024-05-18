# List for usernames and passwords
users_list = [
    {'username': 'admin1', 'password': 'adpass1'},
    {'username': 'user1', 'password': 'pass1'}
]

def validate_user(username, password):
    for user in users_list:
        if user['username'] == username and user['password'] == password:
            return True
    return False
