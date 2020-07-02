class User():
    def __init__(self, unames=[], upassh=[], utypes=[], ubcount=[]):
        self.unames = unames
        self.upassh = upassh
        self.utypes = utypes
        self.ubcount = ubcount
        
    def create_user(self, uname, password, usertype='user'):

