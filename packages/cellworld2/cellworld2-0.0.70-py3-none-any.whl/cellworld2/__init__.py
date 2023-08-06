from .core import *
import requests
def get(uri):
    return requests.get(uri).text