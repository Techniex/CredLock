# -*- coding: utf-8 -*-
"""
Created on Thu Apr  2 11:53:31 2020

@author: satak
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct  3 15:13:04 2019

@author: qunu-labs
"""
import re
import hashlib
from Crypto.Util.Padding import pad, unpad
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from datetime import datetime
from os import path
import os

class Cryptic:
    def __init__(self):
        self.__auth = 1
        self.__usrpass = get_random_bytes(2*AES.block_size)
        self.__pin = "r@9D*-"
        
# Private classes       
    def __bxor(self, a,b):
        return bytes(x ^ y for x, y in zip(a, b))
    
    def __timenowenc(self):
        now = datetime.now()
        dt_string = now.strftime("%d/%m/%Y %H:%M:%S ")
        return dt_string.encode(encoding='utf-8')

# Public classes  
    def dataEncode(self, rawdata):
        if (self.__auth == 0):
            m = hashlib.sha3_256()
            m.update(self.__pin.encode(encoding='utf-8'))
            ikey = m.digest()
            if ikey==self.__usrpass:
                return[2,0]
            else:
                pkey = self.__bxor(self.__usrpass,ikey)
                salt = get_random_bytes(AES.block_size)
                m.update(salt)
                key = m.digest()
                iv = get_random_bytes(AES.block_size)
                siv = (salt+iv)
                preclude = self.__bxor(siv,pkey)
                cipher = AES.new(key, AES.MODE_CBC, iv)
                data = rawdata.encode(encoding='utf-8')
                ct = cipher.encrypt(pad(data, AES.block_size))
                return [0, preclude+ct]
        else:
            return [1, 0]
        
    def dataDecode(self, cipherdata):
        if (self.__auth == 0):
            try:
                m = hashlib.sha3_256()
                m.update(self.__pin.encode(encoding='utf-8'))
                ikey = m.digest()
                pkey = self.__bxor(self.__usrpass,ikey)
                sivr = self.__bxor(cipherdata[:(AES.block_size*2)],pkey)
                saltr = sivr[:AES.block_size]
                ivr = sivr[AES.block_size:]
                ctr = cipherdata[(AES.block_size*2):]
                m.update(saltr)
                keyr = m.digest()
                cipher = AES.new(keyr, AES.MODE_CBC, ivr)
                pt = unpad(cipher.decrypt(ctr), AES.block_size)
                return [0, pt.decode(encoding='utf-8')]
            except:
                return [1, "Wrong Pin, Failure"]
        else:
            return [2, "No Authorization"]      
        
    def createUser(self, uid, upass):
        self.userfile = "./"+uid+".usr"
        if path.exists(self.userfile):
            return 1; # user exist
        else:
            with open(self.userfile, "wb") as cu:
                cu.write( self.__timenowenc())
                cu.write(os.linesep.encode("utf-8"))
                m = hashlib.sha3_256()
                m.update(upass.encode(encoding='utf-8'))
                upkey = m.digest()
                cu.write(upkey)
                cu.write(os.linesep.encode("utf-8"))
            return 0; # user created
        
    def removeUser(self, upass):
        if path.exists(self.userfile):
            m = hashlib.sha3_256()
            m.update(upass.encode(encoding='utf-8'))
            upkey = m.digest()
            print(upkey)
            uc =[]
            with open(self.userfile, "rb") as lu:
                for line in lu:
                    uc.append(line)
            print(uc[1])
            if (upkey+os.linesep.encode("utf-8")) == uc[1]:
                self.usercreation = "00/00/00 00:00:00"
                self.__usrpass = get_random_bytes(2*AES.block_size)
                self.__auth = 1;
                os.remove(self.userfile);
                return 0;
            else:
                return 1; # wrong password
        else:
            return 2; # user doesn't exist
        
    def login(self, uid, upass):
        self.__cred = [];
        self.userfile = "./"+uid+".usr"
        if path.exists(self.userfile):
            m = hashlib.sha3_256()
            m.update(upass.encode(encoding='utf-8'))
            upkey = m.digest()
            uc =[]
            with open(self.userfile, "rb") as lu:
                for line in lu:
                    uc.append(line)
            if (upkey+os.linesep.encode("utf-8")) == uc[1]:
                self.usercreation = uc[0].decode(encoding='utf-8')
                self.__usrpass = uc[1]
                self.__auth = 0;
                return 0;
            else:
                return 1; # wrong password
        else:
            return 2; # user doesn't exist
        
    def logout(self):
        self.usercreation = "00/00/00 00:00:00"
        self.__usrpass = get_random_bytes(2*AES.block_size)
        self.__auth = 1;
        self.__cred = [];
        return 0;
    
    # def updatePassword(self, oldpassword, newpassword1, newpassword2):
        
    # def updatePin(self, oldpin, newpin1, newpin2):
        
        
    def addCred(self, pin, group, descr, credval):
        strval = group +"\t"+ descr +"\t"+ credval;
        [stat, cypher] = self.dataEncode(pin, strval);
        if stat == 0:
            with open(self.userfile, "ab") as ac:
                ac.write(cypher)
                ac.write(os.linesep.encode('utf-8'))
        return stat
    
    def refreshCred(self, pin):
        self.__cred = [];
        stat = self.fetchCred(pin);
        return stat
        
    def deleteCred(self, group, descr, credval):
        strval = group +"\t"+ descr +"\t"+ credval;
        stat = self.fetchCred()
        if stat ==0:
            self.__cred.remove(strval)
            with open(self.userfile, "wb") as sa:
                sa.write(self.__timenowenc)
                sa.write(self.__usrpass)
                sa.write(os.linesep.encode("utf-8"))
                for elements in self.__cred:
                    sa.write(self.dataEncode(elements)[1]) ## no error flag
                    sa.write(os.linesep.encode('utf-8'))
        return stat            
        
    def fetchCred(self):
        with open(self.userfile, "rb") as cre:
            c = cre.readlines()[2:]
            for lines in c:
                [stat, msg] = self.dataDecode(lines[0:-2])
                if stat == 0:
                    self.__cred.append(msg)
        return stat;
    
    def passStrength(self, uid, upass):
        while True:   
            if (len(upass)<12): 
                flag = -1
                break
            elif not re.search("[a-z]", upass): 
                flag = -1
                break
            elif not re.search("[A-Z]", upass): 
                flag = -1
                break
            elif not re.search("[0-9]", upass): 
                flag = -1
                break
            elif not re.search("[#&_@$]", upass): 
                flag = -1
                break
            elif re.search("\s", upass): 
                flag = -1
                break
            else: 
                flag = 0
                break
        if uid.lower() in upass.lower():
            flag = -1
        return flag
        
        
    # def searchCred(self, group, keyword):