# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\python\CredLock\loginDialogue.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Login(object):
    def __init__(self,Login):
        
        #######################Common##################################
        Login.setObjectName("Login")
        Login.resize(300, 190)
        Login.setWindowTitle("CredLock")
        self.icon = QtWidgets.QLabel(Login)
        self.icon.setGeometry(QtCore.QRect(0, 0, 50, 190))
        self.icon.setObjectName("icon")
        self.icon.setPixmap(QtGui.QPixmap('icon.jpg').scaledToWidth(50))
        
        ########################Login Screen###########################
        self.loginButton = QtWidgets.QPushButton(Login)
        self.loginButton.setGeometry(QtCore.QRect(130, 110, 75, 25))
        self.loginButton.setObjectName("loginButton")
        self.loginButton.setText("Log In")
        self.loginButton.setFont(QtGui.QFont('Arial', 11))
        
        self.signupButton = QtWidgets.QPushButton(Login)
        self.signupButton.setGeometry(QtCore.QRect(215, 110, 75, 25))
        self.signupButton.setObjectName("signupButton")
        self.signupButton.setText("Sign Up")
        self.signupButton.setFont(QtGui.QFont('Arial', 11))
        
        self.uid = QtWidgets.QLabel(Login)
        self.uid.setGeometry(QtCore.QRect(60, 30, 60, 25))
        self.uid.setObjectName("uid")
        self.uid.setText("User ID:")
        self.uid.setFont(QtGui.QFont('Arial', 10))
        
        self.upass = QtWidgets.QLabel(Login)
        self.upass.setGeometry(QtCore.QRect(60, 70, 60, 25))
        self.upass.setObjectName("upass")
        self.upass.setText("Password:")
        self.upass.setFont(QtGui.QFont('Arial', 10))
        
        self.UserName = QtWidgets.QLineEdit(Login)
        self.UserName.setGeometry(QtCore.QRect(130, 30, 160, 25))
        self.UserName.setObjectName("UserName")
        
        self.Password = QtWidgets.QLineEdit(Login)
        self.Password.setGeometry(QtCore.QRect(130, 70, 160, 25))
        self.Password.setObjectName("Password")
        self.Password.setEchoMode(QtWidgets.QLineEdit.Password)
        
        ####################Password Polocy###########################
        self.passwordpolicy = QtWidgets.QLabel(Login)
        self.passwordpolicy.setGeometry(QtCore.QRect(60, 30, 230, 80))
        self.passwordpolicy.setObjectName("passwordpolicy")
        self.passwordpolicy.setText("User ID: Case sensitive\nPassword:\nMinimum length: 12\nMust Contain:[a-z][A-Z],[0-9],[#&_@$]\nMust not contain: white space, UserID\nPIN:no restrictions")
        
        self.hideButton = QtWidgets.QPushButton(Login)
        self.hideButton.setGeometry(QtCore.QRect(215, 110, 75, 25))
        self.hideButton.setObjectName("hideButton")
        self.hideButton.setText("Hide")
        self.hideButton.setFont(QtGui.QFont('Arial', 11))
        
        #####################Pin Value Screen#######################
        self.tip = QtWidgets.QLabel(Login)
        self.tip.setGeometry(QtCore.QRect(60, 25, 230, 35))
        self.tip.setObjectName("tip")
        self.tip.setText("Tip: Without secret pin Encryption\n and Decryption will fail.")
        self.tip.setFont(QtGui.QFont('Arial', 10))
        
        self.pin = QtWidgets.QLabel(Login)
        self.pin.setGeometry(QtCore.QRect(60, 70, 60, 25))
        self.pin.setObjectName("pin")
        self.pin.setText("Pin:")
        self.pin.setFont(QtGui.QFont('Arial', 10))
        
        self.pinsecret = QtWidgets.QLineEdit(Login)
        self.pinsecret.setGeometry(QtCore.QRect(130, 70, 160, 25))
        self.pinsecret.setObjectName("pinsecret")
        self.pinsecret.setEchoMode(QtWidgets.QLineEdit.Password)
        
        self.continueButton = QtWidgets.QPushButton(Login)
        self.continueButton.setGeometry(QtCore.QRect(130, 110, 75, 25))
        self.continueButton.setObjectName("continueButton")
        self.continueButton.setText("Continue")
        self.continueButton.setFont(QtGui.QFont('Arial', 11))
        
        self.logoutButton = QtWidgets.QPushButton(Login)
        self.logoutButton.setGeometry(QtCore.QRect(215, 110, 75, 25))
        self.logoutButton.setObjectName("logoutButton")
        self.logoutButton.setText("Log Out")
        self.logoutButton.setFont(QtGui.QFont('Arial', 11))
        ##########################Status#############################
        self.line = QtWidgets.QFrame(Login)
        self.line.setGeometry(QtCore.QRect(50, 140, 250, 20))
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        
        self.statusbar = QtWidgets.QLabel(Login)
        self.statusbar.setGeometry(QtCore.QRect(60, 150, 290, 25))
        self.statusbar.setText("")
        self.statusbar.setObjectName("statusbar")
        
        self.timebar = QtWidgets.QLabel(Login)
        self.timebar.setGeometry(QtCore.QRect(60, 165, 290, 25))
        self.timebar.setText("")
        self.timebar.setObjectName("timebar")
        
        ############################initialize#######################
        self.showLoginScr()
        
                
    def showLoginScr(self):
        self.passwordpolicy.hide()
        self.hideButton.hide()
        self.tip.hide()
        self.pin.hide()
        self.pinsecret.hide()
        self.continueButton.hide()
        self.logoutButton.hide()
        self.loginButton.show()
        self.signupButton.show()   
        self.uid.show()   
        self.upass.show()   
        self.UserName.show()   
        self.Password.show()       

    def showPPScr(self):
        self.passwordpolicy.show()
        self.hideButton.show()
        self.tip.hide()
        self.pin.hide()
        self.pinsecret.hide()
        self.continueButton.hide()
        self.logoutButton.hide()
        self.loginButton.hide()
        self.signupButton.hide()   
        self.uid.hide()   
        self.upass.hide()   
        self.UserName.hide()   
        self.Password.hide() 
        
    def showPinScr(self):
        self.passwordpolicy.hide()
        self.hideButton.hide()
        self.tip.show()
        self.pin.show()
        self.pinsecret.show()
        self.continueButton.show()
        self.logoutButton.show()
        self.loginButton.hide()
        self.signupButton.hide()   
        self.uid.hide()   
        self.upass.hide()   
        self.UserName.hide()   
        self.Password.hide() 