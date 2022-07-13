import sys
from PyQt5 import QtWidgets
from client_gui import Ui_mainForm, Ui_usernameForm, Ui_addForm


def openAddFoem():
    global addForm
    addForm = QtWidgets.QWidget()

    uiAddF.setupUi(addForm)

    uiAddF.buttonBox.accepted.connect(lambda: uiMainF.addUser(uiAddF.searchUsername) if uiAddF.searchUsername else None)


def openMainForm():
    global mainForm
    mainForm = QtWidgets.QWidget()
    uiMainF.setupUi(mainForm)

    uiMainF.username = uiUserF.username
    uiMainF.ServerSend("username", message=uiMainF.username)
    uiMainF.labelUsermae.setText("Hi " + uiUserF.username)
    uiMainF.buttonAddUser.clicked.connect(openAddFoem)


def openEnterUsername():
    usernameForm = QtWidgets.QWidget()

    uiUserF.setupUi(usernameForm)

    uiUserF.buttonBox.accepted.connect(lambda: openMainForm() if uiUserF.username else None)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    uiUserF = Ui_usernameForm()
    uiMainF = Ui_mainForm()
    uiAddF = Ui_addForm()

    openEnterUsername()

    sys.exit(app.exec_())
