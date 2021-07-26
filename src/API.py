'''
The module contains a private data:
'''


# Read Kraken API key and secret stored in environment variables
api_url = "https://api.kraken.com"
api_key = 'ryLjX46KdNpKT1rrgQmAqgyemt+1O8uhP70Sn5w0rnAKHcJvBVQ8T6ej'
api_sec = 'UZYifPgpFKAUJX1sYprIwh/L7wNmFNyPXV1bUwHbzIjogAndmbmFBbp5kut+wWvbQcGNncLeuSz75Rux39trSA=='

import urllib.parse
import hashlib
import hmac
import base64

def get_kraken_signature(urlpath, data, secret):
    postdata = urllib.parse.urlencode(data)
    encoded = (str(data['nonce']) + postdata).encode()
    message = urlpath.encode() + hashlib.sha256(encoded).digest()

    mac = hmac.new(base64.b64decode(secret), message, hashlib.sha512)
    sigdigest = base64.b64encode(mac.digest())
    return sigdigest.decode()
