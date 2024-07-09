import hashlib


def mask_data(value):
    return hashlib.md5(value.encode('utf-8')).hexdigest()