import hashlib
import random
from .models import AuthBlob

def hash_sha256(value):
    # Create a new SHA-256 hash object
    sha256_hash = hashlib.sha256()

    # Convert the value to bytes if it's not already
    if isinstance(value, str):
        value = value.encode('utf-8')

    # Update the hash object with the value
    sha256_hash.update(value)

    # Get the hexadecimal representation of the hash
    hashed_value = sha256_hash.hexdigest()

    return hashed_value

def generate_code(length):
    choices = ['B', 'C', 'D', 'F', 'G', 'H', 'J', 'M', 'P', 'Q', 'R', 'T', 'V', 'W', 'X', 'Y', '2', '3', '4', '6', '7',
               '8', '9']
    code = ''.join(random.choices(choices, k=length))
    hashed = hash_sha256(code)
    while AuthBlob.objects.filter(value=hashed).exists():
        code = ''.join(random.choices(choices, k=length))
        hashed = hash_sha256(code)
    return code

