import re
import sys

import httpx
from PyQt5 import QtCore
from PyQt5.QtCore import QLocale, Qt, QTranslator
from PyQt5.QtGui import QColor, QIcon, QPixmap
from PyQt5.QtWidgets import QApplication
from qfluentwidgets import (
    FluentTranslator,
    MessageBox,
    SplitTitleBar,
    Theme,
    isDarkTheme,
    setTheme,
    setThemeColor,
)
from star_query_rail_client import Client
from star_query_rail_client.api.account import register_account_account_signup_post
from star_query_rail_client.models import Email, EmailRegister
from star_query_rail_client.types import Response
from star_query_rail_desktop.clinet.action import register
from star_query_rail_desktop.config import url

from .ui_registerwindow import Ui_register


def isWin11():
    return sys.platform == "win32" and sys.getwindowsversion().build >= 22000


if isWin11():
    from qframelesswindow import AcrylicWindow as Window
else:
    from qframelesswindow import FramelessWindow as Window


class register_window(Window, Ui_register):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.backButton.clicked.connect(self.jmp_login)
        self.registerButton.clicked.connect(self.register_account)

    def is_valid_email(self, email):
        # 使用正则表达式验证电子邮件地址格式
        email_regex = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
        return re.match(email_regex, email) is not None

    def is_valid_psw(self, psw):
        return psw is not None

    @QtCore.pyqtSlot()
    def jmp_login(self):
        from .login_window import LoginWindow

        self.close()
        w = LoginWindow()
        w.show()

    @QtCore.pyqtSlot()
    def register_account(self):
        # email_register = EmailRegister(
        #     email=self.emailLineEdit.text(), psw=self.passwordLineEdit.text()
        # )
        # client = Client(base_url=url)
        # with client as client:
        #     response: Response[Email] = register_account_account_signup_post.sync(
        #         client=client, body=email_register
        #     )
        #     response: Email = response
        # print(type(response))
        email = register(self.emailLineEdit.text(), self.passwordLineEdit.text())
        if type(email) is Email:
            self.showDialog(t="恭喜", s="成功注册!!")
        else:
            self.showDialog(t="抱歉", s="注册失败!!")

    def showDialog(self, t: str, s: str):
        title = t
        content = s
        # w = MessageDialog(title, content, self)   # Win10 style message box
        w = MessageBox(title, content, self)
        if w.exec():
            print("Yes button is pressed")
        else:
            print("Cancel button is pressed")
