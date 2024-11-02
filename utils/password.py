import hashlib
import re

def hash_password(password: str) -> str:
    """returns the password encoded with sha256
    """
    password_bytes = password.encode('utf-8')
    sha256_hash = hashlib.sha256()
    sha256_hash.update(password_bytes)
    hashed_password = sha256_hash.hexdigest()

    return hashed_password

def check_password(password: str) -> bool:
    """checks if the password matches the hashed password
    """
    return len(password) >= 8 and _has_number(password) and _has_uppercase(password) and _has_special_character(password)

def _has_uppercase(s: str) -> bool:
    """checks if a strign contains at least one uppercase character.
    """
    return any(char.isupper() for char in s)

def _has_number(s: str) -> bool:
    """checks if a string contains at least one number.
    """
    return any(char.isdigit() for char in s)

def _has_special_character(s: str) -> bool:
    """checks if a string contains at least one special character.
    """
    special_characters = re.compile('[@_!#$%^&*()<>?/\|}{~:]')
    return special_characters.search(s) is not None