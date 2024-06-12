import sys
import re
import httpx

from PyQt5 import QtCore
from PyQt5.QtCore import Qt, QTranslator, QLocale
from PyQt5.QtGui import QIcon, QPixmap, QColor
from PyQt5.QtWidgets import QApplication
from star_query_rail_client import Client
from star_query_rail_client.models import EmailRegister,Email
from star_query_rail_client.api.account import register_account_account_signup_post
from star_query_rail_client.types import Response
from qfluentwidgets import setThemeColor, FluentTranslator, setTheme, Theme, SplitTitleBar, isDarkTheme

from .ui_registerwindow import Ui_register
from star_query_rail_desktop.config import url
def isWin11():
    return sys.platform == 'win32' and sys.getwindowsversion().build >= 22000


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
        email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        return re.match(email_regex, email) is not None

    def is_valid_psw(self,psw):
        return psw is not None
    @QtCore.pyqtSlot()
    def jmp_login(self):
        from .login_window import LoginWindow
        self.close()
        w = LoginWindow()
        w.show()

    @QtCore.pyqtSlot()
    def register_account(self):
        email_register = EmailRegister(email=self.emailLineEdit.text(),psw=self.passwordLineEdit.text())
        client = Client(base_url=url)
        with client as client:
            response: Response[Email] = register_account_account_signup_post.sync(client=client,body=email_register)
            response: Email = response
            print(response.to_dict())
