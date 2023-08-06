Introduction
------------

This module contains cryptography handling functions to implement in a Python project.

## Installation
Install via pip:

    pip install os-crypto-handler


## Usage       
Require the toolbox:
        
    from os_crypto import crypto_tools
    
# crpyto tools
```python
# will encrypt a data block
def encrypt(data, key, iv, mode=AES.MODE_CBC, padding_size=AES.block_size)


# will decrypt a data block
def decrypt(data, key, iv, mode=AES.MODE_CBC, padding_size=AES.block_size)
```


## Links
[GitHub - osapps](https://github.com/osfunapps)

## Licence
ISC# os-crypto-py
