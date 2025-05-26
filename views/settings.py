import logging
import os
import sys

import PySide2
from PySide2 import QtCore
from PySide2.QtCore import QObject, QFile
from PySide2.QtGui import QColor, QBrush, QPixmap
from PySide2.QtUiTools import QUiLoader
from PySide2.QtWidgets import QPushButton, QPlainTextEdit, QTextEdit

from fnc import resource_path
logger=logging.getLogger(__name__)

class Settings(QObject):
    def __init__(self, parent=None):
        try:
            super(Settings, self).__init__(parent)
            file = QFile(resource_path("ui/settings.ui"))
            file.open(QFile.ReadOnly)
            loader = QUiLoader()
            self.window = loader.load(file)

            self.btn_save = self.window.findChild(QPushButton, 'btn_save')
            self.btn_save.clicked.connect(self.btn_save_clicked)

            self.btn_cancel = self.window.findChild(QPushButton, 'btn_cancel')
            self.btn_cancel.clicked.connect(self.btn_cancel_clicked)

            # self.plainTextEdit = self.window.findChild(QPlainTextEdit, 'plainTextEdit')
            self.textEdit = self.window.findChild(QTextEdit, 'textEdit')

            with open(resource_path('settings.conf')) as f:
                self.textEdit.setText(f.read())

            # self.textEdit.setText("one<b>two</b>three<br>")
            it = self.textEdit.document().firstBlock().begin()
            while not it.atEnd():
                fragment = it.fragment()
                if fragment.isValid():
                    # print(fragment.text())
                    if (fragment.text() == "one"):
                        # it.fragment().charFormat().setFontUnderline(True)
                        # print(fragment.text())
                        pass
                it += 1

            self.window.setWindowIcon(PySide2.QtGui.QIcon("app.ico"))
            self.window.setWindowFlags(self.window.windowFlags() & QtCore.Qt.CustomizeWindowHint)
            self.window.setWindowFlags(self.window.windowFlags() & ~QtCore.Qt.WindowMaximizeButtonHint)
            self.window.setWindowFlags(self.window.windowFlags() & ~QtCore.Qt.WindowMinimizeButtonHint)
            self.window.setWindowFlags(self.window.windowFlags() & ~QtCore.Qt.WindowCloseButtonHint)
            file.close()
            self.window.show()
            self.setParent(self.window)
        except Exception as err:
            logger.error(err)
    def btn_save_clicked(self):
        self.textEdit = self.window.findChild(QTextEdit, 'textEdit')
        with open(resource_path('settings.conf'), "w") as f:
            f.write(self.textEdit.toPlainText())
        self.window.close()

    def btn_cancel_clicked(self):
        self.window.close()
