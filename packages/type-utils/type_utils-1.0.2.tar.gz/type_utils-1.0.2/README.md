# Type Utils

This python module provides some basic type utilities.

## Installation

You can install *Type Utils* from this Github repository with `python3 setup.py install`, or just install it directly from pypi with `pip3 install type-utils`.

## API

### Conversions

 - `b2s` : bytes to string
 - `s2b` : string to bytes
 - `b2h` : bytes to hex
 - `h2b` : hex to bytes
 - `b2timestamp` : bytes to timestamp
 - `timestamp2b` : timestamp to bytes
 - `b2b64urlsafe` : bytes to base64urlsafe
 - `b64urlsafe2b` : base64urlsafe to bytes
 - `b2b64` : bytes to base64
 - `b642b` : base64 to bytes
  
### Requires

the *require_\** functions ensure the given argument is from a specify type and try to convert them if possible.

 - `require_bytes`
 - `require_timestamp_bytes`
 - `require_string`
 - `require_int`