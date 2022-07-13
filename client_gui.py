import json
import time
from socket import socket
from connection import ListenThread
from PyQt5 import QtCore, QtGui, QtWidgets

ADDRESS = 'localhost'
PORT = 9000
MESSAGES = dict()


class Ui_usernameForm(object):
    def __init__(self):
        self.username = None

    def setupUi(self, usernameForm):
        usernameForm.setObjectName("usernameForm")
        usernameForm.resize(400, 100)
        usernameForm.setMinimumSize(QtCore.QSize(400, 100))
        usernameForm.setMaximumSize(QtCore.QSize(400, 100))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(16)
        font.setBold(True)
        font.setItalic(True)
        usernameForm.setFont(font)
        self.label = QtWidgets.QLabel(usernameForm)
        self.label.setGeometry(QtCore.QRect(12, 12, 151, 16))
        self.label.setObjectName("label")
        self.lineUsername = QtWidgets.QLineEdit(usernameForm)
        self.lineUsername.setGeometry(QtCore.QRect(10, 35, 380, 20))

        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(14)
        font.setBold(False)
        font.setItalic(False)
        self.lineUsername.setFont(font)
        self.lineUsername.setMaxLength(10)
        self.lineUsername.setObjectName("lineUsername")
        self.buttonBox = QtWidgets.QDialogButtonBox(usernameForm)
        self.buttonBox.setGeometry(QtCore.QRect(131, 70, 151, 32))
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel | QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.accepted.connect(lambda: self.methodSaveUsername(usernameForm))
        self.buttonBox.rejected.connect(lambda: usernameForm.close())
        self.buttonBox.setObjectName("buttonBox")
        self.labelTwo = QtWidgets.QLabel(usernameForm)
        self.labelTwo.setGeometry(QtCore.QRect(15, 55, 120, 20))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(10)
        font.setBold(False)
        font.setItalic(False)
        self.labelTwo.setFont(font)
        self.labelTwo.setStyleSheet("color: rgb(255, 16, 0);")
        self.labelTwo.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
        self.labelTwo.setObjectName("label_2")

        self.retranslateUi(usernameForm)
        QtCore.QMetaObject.connectSlotsByName(usernameForm)
        usernameForm.show()

    def retranslateUi(self, usernameForm):
        _translate = QtCore.QCoreApplication.translate
        usernameForm.setWindowTitle(_translate("usernameForm", "Username"))
        self.label.setText(_translate("usernameForm", "Enter your username:"))
        self.labelTwo.setText(_translate("usernameForm", "no more than 10 characters"))

    def methodSaveUsername(self, usernameForm):
        if username := self.lineUsername.text():
            self.username = username
            usernameForm.close()


class Ui_mainForm(object):
    def __init__(self):
        self.user_choose = ""
        self.username = ""
        self.searchUsername = ""

        self.Connection = socket()
        self.Connection.connect((ADDRESS, PORT))

        self.listenThread = ListenThread(self.Connection)
        self.listenThread.listen_var.connect(self.ServerResponse)
        self.listenThread.start()

    def setupUi(self, mainForm):
        mainForm.setObjectName("mainForm")
        mainForm.setEnabled(True)
        mainForm.resize(580, 350)
        mainForm.setMinimumSize(QtCore.QSize(580, 350))
        mainForm.setMaximumSize(QtCore.QSize(580, 350))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(16)
        font.setBold(True)
        font.setItalic(True)
        mainForm.setFont(font)
        self.labelOne = QtWidgets.QLabel(mainForm)
        self.labelOne.setGeometry(QtCore.QRect(210, 10, 370, 20))
        self.labelOne.setAlignment(QtCore.Qt.AlignCenter)
        self.labelOne.setObjectName("labelOne")
        self.labelUsermae = QtWidgets.QLabel(mainForm)
        self.labelUsermae.setGeometry(QtCore.QRect(10, 10, 170, 20))
        self.labelUsermae.setAlignment(QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
        self.labelUsermae.setObjectName("labelUsermae")
        self.labelThree = QtWidgets.QLabel(mainForm)
        self.labelThree.setEnabled(True)
        self.labelThree.setGeometry(QtCore.QRect(40, 40, 121, 20))
        self.labelThree.setAlignment(QtCore.Qt.AlignCenter)
        self.labelThree.setObjectName("labelThree")
        self.textConversation = QtWidgets.QTextBrowser(mainForm)
        self.textConversation.setGeometry(QtCore.QRect(200, 29, 370, 291))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(14)
        font.setBold(False)
        font.setItalic(False)
        self.textConversation.setFont(font)
        self.textConversation.setObjectName("textConversation")
        self.textConversation.installEventFilter(self)
        self.lineMessage = QtWidgets.QLineEdit(mainForm)
        self.lineMessage.setGeometry(QtCore.QRect(200, 323, 315, 25))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(14)
        font.setBold(False)
        font.setItalic(False)
        self.lineMessage.setFont(font)
        self.lineMessage.setObjectName("lineMessage")
        self.lineMessage.installEventFilter(self)
        self.buttonSend = QtWidgets.QPushButton(mainForm)
        self.buttonSend.setGeometry(QtCore.QRect(510, 320, 65, 32))
        self.buttonSend.setObjectName("buttonSend")
        self.buttonSend.clicked.connect(self.SendButton)
        self.listUsers = QtWidgets.QListWidget(mainForm)
        self.listUsers.setGeometry(QtCore.QRect(10, 60, 180, 260))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(14)
        font.setBold(False)
        font.setItalic(False)
        self.listUsers.setFont(font)
        self.listUsers.setObjectName("listUsers")
        self.listUsers.itemClicked.connect(self.UserProcess)
        self.buttonAddUser = QtWidgets.QPushButton(mainForm)
        self.buttonAddUser.setGeometry(QtCore.QRect(10, 320, 180, 32))
        self.buttonAddUser.setObjectName("buttonAddUser")

        self.retranslateUi(mainForm)
        QtCore.QMetaObject.connectSlotsByName(mainForm)
        mainForm.show()

    def retranslateUi(self, mainForm):
        _translate = QtCore.QCoreApplication.translate
        mainForm.setWindowTitle(_translate("mainForm", "Client"))
        self.labelOne.setText(_translate("mainForm", "---Conversation---"))
        self.labelThree.setText(_translate("mainForm", "---List of users---"))
        self.buttonSend.setText(_translate("mainForm", "Send"))
        self.buttonAddUser.setText(_translate("mainForm", "Add user"))

    def ServerResponse(self, data: dict):
        if data["code"] == "receive":
            t = MESSAGES.get(data["from"])
            if t is None:
                MESSAGES[data['from']] = {
                    'button': self.addUser(data['from']),
                    'message': [["user", data['message']]],
                    'read': False
                }
                MESSAGES[data["from"]]['message'].append(["user", data['message']])

            if data["from"] == self.user_choose:
                self.textConversation.append(data['message'])
                self.textConversation.setAlignment(QtCore.Qt.AlignRight)

        if data["code"] == "user":
            MESSAGES[data['message']] = {
                'button': self.addUser(data['message']),
                'message': [],
                'read': True
            }

    def SendButton(self):
        if self.user_choose != "":
            self.ServerSend("send", self.user_choose, self.lineMessage.toPlainText())
            MESSAGES[self.user_choose]['message'].append(["me", self.lineMessage.toPlainText()])
            self.textConversation.append(self.lineMessage.toPlainText())
            self.textConversation.setAlignment(QtCore.Qt.AlignLeft)
            self.lineMessage.clear()

    def closeEvent(self, event) -> None:
        self.ServerSend("exit")
        time.sleep(1000)
        self.Connection.close()
        super().closeEvent(event)

    def eventFilter(self, obj, event):
        if event.type() == QtCore.QEvent.KeyPress and obj is self.textConversation:
            if event.key() == QtCore.Qt.Key_Return and self.textConversation.hasFocus():
                self.SendButton()
                self.textConversation.clear()
        if event.type() == QtCore.QEvent.KeyPress and obj is self.sendto:
            if event.key() == QtCore.Qt.Key_Return and self.sendto.hasFocus():
                self.ServerSend("find", message=self.sendto.toPlainText())
        return super().eventFilter(obj, event)

    def ServerSend(self, code: str, to: str = "server", message: str = ""):
        dict_send = {"code": code,
                     "from": self.username,
                     "to": to,
                     "message": message}
        self.Connection.send(json.dumps(dict_send).encode())

    def UserProcess(self, item):
        name = item.text()
        self.user_choose = name
        self.textConversation.clear()
        if len(MESSAGES[name]['message']) != 0:
            for i in MESSAGES[name]['message']:
                if i[0] == "me":
                    self.textConversation.append(i[1])
                    self.textConversation.setAlignment(QtCore.Qt.AlignLeft)
                else:
                    self.textConversation.append(i[1])
                    self.textConversation.setAlignment(QtCore.Qt.AlignRight)

    def addUser(self, name: str):
        self.listUsers.addItem(name)


class Ui_addForm(object):
    def __init__(self):
        self.searchUsername = None

    def setupUi(self, addForm):
        addForm.setObjectName("addForm")
        addForm.resize(400, 100)
        addForm.setMinimumSize(QtCore.QSize(400, 100))
        addForm.setMaximumSize(QtCore.QSize(400, 100))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(16)
        font.setBold(True)
        font.setItalic(True)
        addForm.setFont(font)
        self.label = QtWidgets.QLabel(addForm)
        self.label.setGeometry(QtCore.QRect(12, 12, 346, 16))
        self.label.setObjectName("label")
        self.lineUsername = QtWidgets.QLineEdit(addForm)
        self.lineUsername.setGeometry(QtCore.QRect(12, 39, 381, 21))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(14)
        font.setBold(False)
        font.setItalic(False)
        self.lineUsername.setFont(font)
        self.lineUsername.setMaxLength(10)
        self.lineUsername.setObjectName("lineUsername")
        self.buttonBox = QtWidgets.QDialogButtonBox(addForm)
        self.buttonBox.setGeometry(QtCore.QRect(12, 64, 261, 32))
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel | QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.accepted.connect(lambda: self.methodSearchUsername(addForm))
        self.buttonBox.rejected.connect(lambda: addForm.close())
        self.buttonBox.setObjectName("buttonBox")

        self.retranslateUi(addForm)
        QtCore.QMetaObject.connectSlotsByName(addForm)
        addForm.show()

    def retranslateUi(self, addForm):
        _translate = QtCore.QCoreApplication.translate
        addForm.setWindowTitle(_translate("addForm", "Add user"))
        self.label.setText(_translate("addForm", "Enter the username of the user you want to communicate "))

    def methodSearchUsername(self, addForm):
        if searchUsername := self.lineUsername.text():
            self.searchUsername = searchUsername
            addForm.close()
