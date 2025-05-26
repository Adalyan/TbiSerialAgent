import sys

import cryptography
from PySide2.QtGui import QIcon
from PySide2.QtWidgets import QApplication, QSystemTrayIcon, QMenu, QAction
import base64

from cryptography.fernet import Fernet

from fnc import encrypt, decrypt, days_between
from views.main_window import MainWindow
import logging
from datetime import date
import datetime
logging.basicConfig(filename='error.log', level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s - %(name)s - %(message)s')
logger=logging.getLogger(__name__)


#
# # print(encrypt("2001-04-19").decode("utf-8"))
# license_date = decrypt("gAAAAABhvxy-kQFp6EhzKPxdTq26HyIfrwsPk-aOKYyxgbCgUL6By5Kkq6gOL-oSm0c3GKP2-W68xbFdK-k4vu85YXhf3-OCJw==".encode("utf-8"))
# # license_date = decrypt("gAAAAABhvx0wNBYKOJZxvo-544d_UBCQxBtghVQ0S_t6sJOTpzBGIku5uX8_IV35Bu-PsgBVCFWPXjaDk7c-k8oR9yhxLMyVYw==".encode("utf-8"))
# # license_date_obj = datetime.datetime.strptime(license_date, '%Y-%m-%d')
# today = date.today().strftime("%Y-%m-%d")
# days = days_between(license_date, today)
# print("license", days)
# if int(days) > 0:
#     quit()

if __name__ == '__main__':
    app = QApplication(sys.argv)

    form = MainWindow()

    app.setQuitOnLastWindowClosed(False)

    tray = QSystemTrayIcon(QIcon("app.ico"), app)
    menu = QMenu()

    action_show = QAction("Göster")
    action_show.triggered.connect(form.btn_show_clicked)
    menu.addAction(action_show)
    menu.setDefaultAction(action_show)

    action_exit = QAction("Çıkış")
    action_exit.triggered.connect(form.btn_exit_clicked)
    menu.addAction(action_exit)

    tray.setContextMenu(menu)
    tray.setToolTip("TBI Serial Agent")
    tray.show()

    app.setQuitOnLastWindowClosed(False)
    app.lastWindowClosed.connect(form.btn_hide_clicked)
    sys.exit(app.exec_())
