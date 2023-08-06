"""
Copyright (c) 2022 Philipp Scheer
"""


import requests
import traceback
from typing import Union


class HaloSigError(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)


def checkUrlIsSet(func):
    global host
    def wrapper(*args, **kwargs):
        global host
        if not isinstance(host, str) or host.strip() == "":
            raise RuntimeError("halosig host is not set")
        return func(*args, **kwargs)
    return wrapper


def halosigError(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            raise HaloSigError(f"{e}")
    return wrapper


def _handle(response):
    if response.status_code != 200:
        print(f"HALOSIG ERROR: {response.status_code}: {response.text}")
        raise RuntimeError(f"internal error (by package)")
    else:
        response = response.json()
        if not response["success"]:
            raise RuntimeError(f"{response['result']}")
        else:
            return response["result"]


@halosigError
def _post(url, *args, **kwargs):
    return _handle(requests.post(f"{proto}://{host}:{port}{url}", *args, **kwargs))


proto: str = "http"
host: str = None
port: int = 7809


@checkUrlIsSet
def chargeToken(token: str, credits: int, usageType: str, customer: str = None):
    """Charge the given token credits"""
    return _post("/chargeToken", json={ k:v for k,v in {
            "token": token, 
            "credits": credits, 
            "usageType": usageType,
            "customer": customer, 
        }.items() if v is not None})

@checkUrlIsSet
def recordUsage(accountId: str, apikey: str, credits: int, endpoint: str, timing: float, code: int):
    """Record usage for an account and apikey"""
    return _post("/recordUsage", json={ k:v for k,v in {
            "accountId": accountId,
            "apikey": apikey,
            "credits": credits,
            "endpoint": endpoint,
            "timing": timing,
            "code": code
        }.items() if v is not None})

@checkUrlIsSet
def tokenExists(token: str):
    """Check if a token exists or got limited"""
    return _post("/recordUsage", json={ k:v for k,v in {
            "token": token,
        }.items() if v is not None})
