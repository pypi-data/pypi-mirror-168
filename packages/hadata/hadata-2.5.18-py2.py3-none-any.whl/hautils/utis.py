import hashlib
from hashlib import md5


def calculate_md5(filename):
    return md5(filename).hexdigest()


def calculate_md5_file(filename):
    return hashlib.md5(open(filename, 'rb').read()).hexdigest()
