import string
import hashlib

CHARS = string.digits + string.ascii_lowercase + string.ascii_uppercase
ENCODING_LENGTH = 8


def base62_encode(num: int) -> str:
    if num == 0:
        return CHARS[0]

    encoding = ""
    while num > 0:
        num, rem = divmod(num, len(CHARS))
        encoding += CHARS[rem]
    return encoding[:ENCODING_LENGTH]


def hash_url_to_base62(long_url: str) -> str:
    encoded_url = long_url.encode("utf-8")
    sha256_hash = hashlib.sha256()
    sha256_hash.update(encoded_url)
    hash_int = int.from_bytes(sha256_hash.digest(), "big")
    return base62_encode(hash_int)
