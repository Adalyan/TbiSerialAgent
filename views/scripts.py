import logging
import os
import sys

import PySide2
from PySide2 import QtCore, QtUiTools
from PySide2.QtCore import QObject, QFile
from PySide2.QtGui import QColor, QBrush, QPixmap
from PySide2.QtUiTools import QUiLoader
from PySide2.QtWidgets import QPushButton, QPlainTextEdit, QTextEdit

from fnc import resource_path
from interpreter import check_line, directives, keys, constants, is_argument
logger=logging.getLogger(__name__)


class Scripts(QObject):
    def __init__(self, parent=None):
        try:
            super(Scripts, self).__init__(parent)
            file = QFile(resource_path("ui/scripts.ui"))
            file.open(QFile.ReadOnly)
            loader = QUiLoader()
            self.window = loader.load(file)

            self.btn_save = self.window.findChild(QPushButton, 'btn_save')
            self.btn_save.clicked.connect(self.btn_save_clicked)

            self.btn_cancel = self.window.findChild(QPushButton, 'btn_cancel')
            self.btn_cancel.clicked.connect(self.btn_cancel_clicked)

            # self.plainTextEdit = self.window.findChild(QPlainTextEdit, 'plainTextEdit')
            self.textEdit = self.window.findChild(QTextEdit, 'textEdit')

            # self.textEdit.setTextBackgroundColor(QBrush(QColor(0, 255, 0)))
            self.textEdit.setStyleSheet("background-color : rgba(255,255,255,0%); color : transparent;");

            # self.textEdit.setTextColor(QBrush(QColor(0, 255, 0)))
            self.textEdit_2 = self.window.findChild(QTextEdit, 'textEdit_2')
            self.textEdit_3 = self.window.findChild(QTextEdit, 'textEdit_3')
            self.textEdit.textChanged.connect(self.textEdit_textChanged)

            with open(resource_path('scripts.tsc'), "rt") as f:
                self.textEdit.setText(f.read())
                print("scripts.tsc content", f.read())
                print("scripts.tsc path", resource_path('scripts.tsc'))

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
        with open(resource_path('scripts.tsc'), "w") as f:
            f.write(self.textEdit.toPlainText())
        self.window.close()

    def btn_cancel_clicked(self):
        self.window.close()

    def textEdit_textChanged(self):
        # self.textEdit_2.setText(self.textEdit.toPlainText())
        raw = self.textEdit.toPlainText()
        lines = raw.split("\n")
        html = """
        <style>
            .container{
                color: black;
            }
            body{
                background: transparent;
            }
            .ln{
                width: 50px;
                float:left;
                color: grey;
            }
            .key{
                color: blue;
            }
            .directive{
                color: purple;
            }
            .default{
                color: black;
            }
            .constant{
                color: green;
            }
             .argument{
                color: darkorange;
            }
            .fw{
                width: 100%;
                background: transparent;
            }
            .error{
                background: red;
                color: white !important;
            }
            .warning{
                color: red;
                border: 1px solid black;
                border-radius: 5px;
                font-size: small;
            }
        </style>
        <div class="container">
        """
        ln = 0
        html_line = html
        for line in lines:
            # print(line)
            words = line.split()
            parsed_line = ""
            for word in words:
                if word in keys:
                    parsed_line += '<span class="key">{}</span> '.format(word)
                elif word in directives:
                    parsed_line += '<span class="directive">{}</spa_n> '.format(word)
                elif word in constants:
                    parsed_line += '<span class="constant">{}</spa_n> '.format(word)
                elif is_argument(word, words):
                    parsed_line += '<span class="argument">{}</spa_n> '.format(word)
                else:
                    parsed_line += '<span class="default">{}</span> '.format(word)
            check = check_line(words)
            if check != "":
                parsed_line = """<span class="error">{0}</span>&nbsp;&nbsp;<span class="warning">{1}</span>""".format(
                    line, " ~{0} ".format(check))
            ln += 1
            html += """<div class="fw">{0}&nbsp;<div>""".format(parsed_line)
            html_line += """<div class="ln">{0}&nbsp;<div>""".format(ln)

        html += """
        </html>
        """
        self.textEdit_2.setHtml(html)
        self.textEdit_3.setHtml(html_line)
