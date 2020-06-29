"""
Module generates password which are locked with system.
"""
import platform
import uuid
import random
import hashlib
import string
import psutil

def syslockedpasskey(uname, pin, saltcount=1):
    """
    Description
    -----------
    Generates a passkey based on SHA3 locked to system info and user PIN

    Arguments
    ---------
    uname(str) : required as multiple user can be there on same machine
    pin(int) : required to get consistent output everytime.

    Returns
    -------
    slpkey(byte array) : secret system locked key
    """
    letters = string.ascii_letters
    if saltcount < 1:
        saltcount = 1
    try:
        random.seed(pin)
        systemdata = []
        systemdata.append(uname)
        systemdata.append(str(platform.machine()))
        systemdata.append(str(platform.system()))
        systemdata.append(str(platform.node()))
        systemdata.append(str(platform.processor()))
        systemdata.append(str(uuid.getnode()))
        systemdata.append(str(psutil.virtual_memory().total))
        systemdata.append(str(psutil.cpu_count(logical=False)))
        systemdata.append(str(psutil.disk_partitions()))
        systemdata.append(str(psutil.swap_memory().total))
        random.shuffle(systemdata)
        systemdata = list(''.join(systemdata))
        for sitr in range(0, saltcount):
            random.shuffle(systemdata)
            salt = [random.choice(letters) for itr in range(0, sitr)]
            systemdata = systemdata + salt
        mixedsysinfo = ''.join(systemdata)
        hashm = hashlib.sha3_256()
        hashm.update(mixedsysinfo.encode(encoding='utf-8'))
        slpkey = hashm.digest()
    except IOError:
        slpkey = 0
    return slpkey

UNAME = input("UserName : ")
IPIN = input("PIN : ")
KEY = syslockedpasskey(UNAME, int(IPIN), 1)
print(KEY)
