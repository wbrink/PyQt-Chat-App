import base64
import os
from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

import configparser
# password = b"password"
# read the config file
config = configparser.ConfigParser()
config.read('chat.ini')

password = config['Keys']['password']
password = password.encode('utf-8')
print(f'password from the config file: {password}')
salt = config['Keys']['salt']
salt = salt.encode('utf-8') # converts the string into bytes
print(f'salt from the config file: {salt}')
kdf = PBKDF2HMAC(
    algorithm=hashes.SHA256(),
    length=32,
    salt=salt,
    iterations=100000,
    backend=default_backend()
)
key = base64.urlsafe_b64encode(kdf.derive(password))
f = Fernet(key)
print(key)
#token = f.encrypt(b"Secret message!")

#f.decrypt(token)
#b'Secret message!
