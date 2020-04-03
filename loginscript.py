# -*- coding: utf-8 -*-
"""
Created on Fri Apr  3 10:05:15 2020

@author: satak
"""

from PyQt5 import QtWidgets
from loginDialogue import Ui_Login
from crypt import Cryptic


Login = QtWidgets.QDialog()


class funcLogin(Ui_Login, Cryptic):
    def __init__(self, Login):
        Ui_Login.__init__(self,Login)
        Cryptic.__init__(self)
        sttime = self._Cryptic__timenowenc().decode('utf-8')
        self.statusbar.setText("Login: Please enter User Id and Password")
        self.timebar.setText("App Started: "+sttime)
        self.loginButton.clicked.connect(self.loginClicked)
        self.signupButton.clicked.connect(self.signupClicked)
        self.hideButton.clicked.connect(self.hideClicked)
        self.continueButton.clicked.connect(self.continueClicked)
        self.logoutButton.clicked.connect(self.logoutClicked)
        if self._Cryptic__auth == 1:
            Login.show()
        
    def loginClicked(self):
        un = self.UserName.text()
        self.UserName.clear()
        pw = self.Password.text()
        self.Password.clear()
        status = self.login(un, pw)
        if status == 0:
            self.showPinScr()
        else:
            if status == 1:
                self.statusbar.setText("Wrong Password: Please try Again")
            else:
                self.statusbar.setText("User doesn't exist: Sign up")

    def signupClicked(self):
        un = self.UserName.text()
        self.UserName.clear()
        pw = self.Password.text()
        self.Password.clear()
        flag = self.passStrength(un, pw)
        if flag == 0:
            status = self.createUser(un, pw)
            if status == 0:
                self.login(un, pw)
                Login.close()
            else:
                self.statusbar.setText("User Exists: Please Log In")
        else:
            self.statusbar.setText("Password Policy Violated: Week password")
            self.showPPScr()
            
    def hideClicked(self):
        self.showLoginScr()
        
    def continueClicked(self):
        pw = self.pinsecret.text()
        self.pinsecret.clear()
        self._Cryptic__pin = pw
        Login.close()
        
    def logoutClicked(self):
        self.logout()
        Login.close()
            