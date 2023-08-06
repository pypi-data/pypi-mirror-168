import datetime

from .conversions import b2s, s2b, timestamp2b



def require_bytes(a, int_to_string=False):
    if int_to_string and isinstance(a, int):
        a = str(a)
    if isinstance(a, str):
        return s2b(a)
    if not isinstance(a, bytes):
        raise TypeError(f"A byte object is required, not {str(type(a))}")
    return a


def require_timestamp_bytes(a, n=8, byteorder="big"):
    if isinstance(a, (int, datetime.datetime)):
        return timestamp2b(a, n=n, byteorder=byteorder)
    if not isinstance(a, bytes):
        raise TypeError(f"A byte object is required, not {str(type(a))}")
    return a


def require_string(a, int_to_string=False):
    if int_to_string and isinstance(a, int):
        a = str(a)
    if isinstance(a, bytes):
        a = b2s(a)
    if not isinstance(a, str):
        raise TypeError(f"A string object is required, not {str(type(a))}")
    return a


def require_int(a, str_to_int=False, byteorder="little"):
    if str_to_int and isinstance(a, str):
        a = int(a)
    if isinstance(a, bytes):
        a = int.from_bytes(a, byteorder=byteorder)
    if not isinstance(a, int):
        raise TypeError(f"A int object is required, not {str(type(a))}")
    return a
