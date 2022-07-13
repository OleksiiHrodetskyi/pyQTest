import sys
from PyQt5 import QtWidgets
from server_gui import Ui_Form
from server import *

if __name__ == "__main__":
    asyncio.run(run_server())
    # app = QtWidgets.QApplication(sys.argv)
    #
    # Form = QtWidgets.QWidget()
    # ui = Ui_Form(Form)
    #
    # sys.exit(app.exec_())
