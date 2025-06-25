import os 

def getenv(key: str) -> str:
    res = os.getenv(key)
    return res if res else ''