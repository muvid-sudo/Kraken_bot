"""
The module contains a private data:
"""
import requests
import urllib.parse
import hashlib
import hmac
import base64

# Read Kraken API key and secret stored in environment variables
api_url = "https://api.kraken.com"
api_key = ''
api_sec = ''


def get_kraken_signature(urlpath, data, secret):
    postdata = urllib.parse.urlencode(data)
    encoded = (str(data['nonce']) + postdata).encode()
    message = urlpath.encode() + hashlib.sha256(encoded).digest()

    mac = hmac.new(base64.b64decode(secret), message, hashlib.sha512)
    sigdigest = base64.b64encode(mac.digest())
    return sigdigest.decode()


# Attaches auth headers and returns results of a POST request
def kraken_request(uri_path, data):
    headers = {'API-Key': api_key, 'API-Sign': get_kraken_signature(uri_path, data, api_sec)}
    # get_kraken_signature() as defined in the 'Authentication' section
    req = requests.post((api_url + uri_path), headers=headers, data=data)
    return req


def get_response(url):
    response = requests.get(url)
    response.raise_for_status()
    return response.json()
