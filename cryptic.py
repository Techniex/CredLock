"""
Module generates password which are locked with system.
"""
import platform
import uuid
import random
import hashlib
import string
from Crypto.Util.Padding import pad, unpad
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
import psutil

class Cryptic:
    """
    Description
    -----------
    """
    def __init__(self, uname, upass):
        self.uname = uname
        self.upass = upass

    def bxor(self, a, b): return bytes([x ^ y for x, y in zip(a, b)])

    def __passkey__(self, pin, nodelocked=True, saltcount=1):
        """
        Description
        -----------
        Generates a passkey based on SHA3 locked to system info and user PIN

        Arguments
        ---------
        uname(str) : required as multiple user can be there on same machine
        upass(str) : required as additional layer of security
        pin(int) : required to get consistent output everytime (6 digit).
        nodelocked(bool): Is password is bound to system?
        saltcount(int) : Additional strength and randomization (optional)

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
            if nodelocked:
                systemdata.append(self.uname)
                systemdata.append(self.upass)
                systemdata.append(str(platform.machine()))
                systemdata.append(str(platform.system()))
                systemdata.append(str(platform.node()))
                systemdata.append(str(platform.processor()))
                systemdata.append(str(uuid.getnode()))
                systemdata.append(str(psutil.virtual_memory().total))
                systemdata.append(str(psutil.cpu_count(logical=False)))
                systemdata.append(str(psutil.disk_partitions()))
                systemdata.append(str(psutil.swap_memory().total))
            strlistpin = list(str(pin))
            for val in strlistpin:
                newletter = ''.join(random.choice(letters) for iterate in range(0, int(val)))
                systemdata.append(newletter)
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
        except (IOError, ValueError):
            slpkey = 0
        return slpkey

    def crypt_aes(self, rawdata, pin, nodelocked=True, saltcount=1):
        """
        Description
        -----------
        Encrypt data with AES MODE CBC

        Dependent Function call
        -----------------------
        key = __passkey__(pin, nodelocked, saltcount)

        Arguments
        ---------
        rawdata(any): input data to be encrypted
        pin(int) : required to get consistent output everytime (6 digit).
        nodelocked(bool): Is password is bound to system?
        saltcount(int) : Additional strength and randomization (optional)

        Returns
        -------
        cipher(bytes)
        """
        key = self.__passkey__(pin, nodelocked=nodelocked, saltcount=saltcount)
        keyerror = key == 0
        if not keyerror:
            init_vect = get_random_bytes(2 * AES.block_size)
            hashm = hashlib.sha3_256()
            hashm.update(str(pin).encode(encoding='utf-8'))
            preclude = self.bxor(init_vect, hashm.digest())
            cipher_block = AES.new(key, AES.MODE_CBC, init_vect[:AES.block_size])
            if isinstance(rawdata, bytes):
                data = rawdata
            else:
                data = str(rawdata).encode(encoding='utf-8')
            cipher = preclude + cipher_block.encrypt(pad(data, AES.block_size))
        else:
            cipher = 'error'
        return cipher

    def decrypt_aes(self, cipher, pin, nodelocked=True, saltcount=1):
        """
        Description
        -----------
        Decrypt data encrypted by crypt_aes function

        Dependent Function call
        -----------------------
        key = __passkey__(pin, nodelocked, saltcount)

        Arguments
        ---------
        cipher(bytes): input data to be decrypted
        pin(int) : required to get consistent output everytime (6 digit).
        nodelocked(bool): Is password is bound to system?
        saltcount(int) : Additional strength and randomization (optional)

        Returns
        -------
        decipher(str/bytes)
        """
        key = self.__passkey__(pin, nodelocked=nodelocked, saltcount=saltcount)
        keyerror = key == 0
        if not keyerror:
            try:
                preclude = cipher[:AES.block_size]
                cipher_data = cipher[2* AES.block_size:]
                hashm = hashlib.sha3_256()
                hashm.update(str(pin).encode(encoding='utf-8'))
                init_vect = self.bxor(preclude, hashm.digest())
                cipher_block = AES.new(key, AES.MODE_CBC, init_vect)
                decipher = unpad(cipher_block.decrypt(cipher_data), AES.block_size)
            except (ValueError, TypeError):
                decipher = cipher
            try:
                decipher = decipher.decode(encoding='utf-8')
            except (UnicodeDecodeError, AttributeError):
                pass
        else:
            decipher = cipher
        return decipher
