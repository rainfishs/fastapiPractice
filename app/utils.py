# define get salt function, if file "salt" exists, read it, else create it
import os


def get_salt():
    if os.path.exists("salt"):
        with open("salt", "rb") as f:
            salt = f.read()
    else:
        salt = os.urandom(32)
        with open("salt", "wb") as f:
            f.write(salt)
    return salt
