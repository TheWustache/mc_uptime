import hashlib
import secrets


def generate_salt(len):
    """Returns salt of length len consisting of letters and numbers."""
    abc = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    chars = []
    for i in range(len):
        chars.append(secrets.choice(abc))
    return ''.join(chars)


def hash_password(password, salt):
    """Returns salted and hashed password."""
    return hashlib.sha256(password.encode() + salt.encode()).hexdigest()


def check_password(password, salt, hashed_pw):
    """Returns True if password is the same one as hashed_pw, False otherwise."""
    return hash_password(password, salt) == hashed_pw
