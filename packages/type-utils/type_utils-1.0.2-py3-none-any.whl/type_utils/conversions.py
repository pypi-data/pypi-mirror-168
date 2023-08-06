import base64
import binascii
import datetime


def b2s(b):
    if isinstance(b, str):
        return b
    if not isinstance(b, bytes):
        raise TypeError("Invalid Bytes type")
    return b.decode("utf-8")


def s2b(s):
    if isinstance(s, bytes):
        return s
    if not isinstance(s, str):
        raise TypeError("Invalid String type")
    return s.encode("utf-8")


def b2h(b):
    if not isinstance(b, bytes):
        raise TypeError("Invalid Bytes type")
    return binascii.hexlify(b).decode("utf-8")


def h2b(h):
    if not isinstance(h, (str, bytes)):
        raise TypeError("Invalid Hex type")
    return binascii.unhexlify(h)


def b2timestamp(b, byteorder="big"):
    if not isinstance(b, bytes):
        raise TypeError("Invalid Bytes type")
    return int.from_bytes(b, byteorder=byteorder)


def timestamp2b(timestamp, n=8, byteorder="big"):
    if isinstance(timestamp, bytes):
        return timestamp
    if isinstance(timestamp, datetime.datetime):
        print(timestamp.timestamp())
        timestamp = int(timestamp.timestamp())
    if isinstance(timestamp, float):
        timestamp = int(timestamp)
    if not isinstance(timestamp, int):
        raise TypeError("Invalid Timestamp Type")
    return timestamp.to_bytes(n, byteorder=byteorder)


def b2b64urlsafe(b):
    if not isinstance(b, bytes):
        raise TypeError("Invalid Bytes type")
    return base64.urlsafe_b64encode(b).decode("utf-8")


def b64urlsafe2b(urlsafe):
    if not isinstance(urlsafe, (str, bytes)):
        raise TypeError("Invalid base64 type")
    return base64.urlsafe_b64decode(urlsafe)


def b2b64(b):
    if not isinstance(b, bytes):
        raise TypeError("Invalid Bytes type")
    return base64.b64encode(b).decode("utf-8")


def b642b(b64):
    if not isinstance(b64, (str, bytes)):
        raise TypeError("Invalid base64 type")
    return base64.b64decode(b64)
