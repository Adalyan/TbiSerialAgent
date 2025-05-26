import sys

import PySide2
from PySide2 import QtCore, QtWidgets
from PySide2.QtCore import QFile, QObject
from PySide2.QtUiTools import QUiLoader
from PySide2.QtWidgets import QPushButton, QApplication

from app import start_server, stop_server
from fnc import resource_path


class MainWindow(QObject):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        file = QFile(resource_path("ui/mainwindow.ui"))
        file.open(QFile.ReadOnly)
        loader = QUiLoader()
        self.window = loader.load(file)

        self.btn_startserver = self.window.findChild(QPushButton, 'btn_startserver')
        self.btn_startserver.clicked.connect(self.btn_startserver_clicked)

        self.btn_stopserver = self.window.findChild(QPushButton, 'btn_stopserver')
        self.btn_stopserver.clicked.connect(self.btn_stopserver_clicked)

        self.btn_exit = self.window.findChild(QPushButton, 'btn_exit')
        self.btn_exit.clicked.connect(self.btn_exit_clicked)

        self.btn_settings = self.window.findChild(QPushButton, 'btn_settings')
        self.btn_settings.clicked.connect(self.btn_settings_clicked)

        self.btn_scripts = self.window.findChild(QPushButton, 'btn_scripts')
        self.btn_scripts.clicked.connect(self.btn_scripts_clicked)

        self.btn_startserver.setEnabled(False)
        self.btn_stopserver.setEnabled(True)

        self.window.setWindowIcon(PySide2.QtGui.QIcon("app.ico"))

        self.window.setWindowFlags(self.window.windowFlags() & QtCore.Qt.CustomizeWindowHint)
        self.window.setWindowFlags(self.window.windowFlags() & ~QtCore.Qt.WindowMaximizeButtonHint)
        file.close()
        self.window.show()
        start_server()

    def btn_startserver_clicked(self):
        self.btn_startserver.setEnabled(False)
        self.btn_stopserver.setEnabled(True)
        start_server()
        pass

    def btn_stopserver_clicked(self):
        self.btn_startserver.setEnabled(True)
        self.btn_stopserver.setEnabled(False)
        stop_server()
        pass

    def btn_exit_clicked(self):
        stop_server()
        app = QtWidgets.QApplication.instance()

        app.quit()
        quit()

    def btn_show_clicked(self):
        self.window.show()

    def btn_hide_clicked(self):
        try:
            self.window.hide()
        except:
            print("window hide error")

    def btn_settings_clicked(self):
        from views.settings import Settings
        Settings()
        pass

    def btn_scripts_clicked(self):
        from views.scripts import Scripts
        Scripts()
        pass
