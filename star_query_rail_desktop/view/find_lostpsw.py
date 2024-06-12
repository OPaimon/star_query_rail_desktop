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
from qfluentwidgets import setThemeColor, FluentTranslator, setTheme, Theme, SplitTitleBar, isDarkTheme, MessageBox

from .ui_registerwindow import Ui_register
from star_query_rail_desktop.config import url
from  .ui_find_lostpsw import Ui_findpsw
def isWin11():
    return sys.platform == 'win32' and sys.getwindowsversion().build >= 22000


if isWin11():
    from qframelesswindow import AcrylicWindow as Window
else:
    from qframelesswindow import FramelessWindow as Window


class findlostpsw_window(Window, Ui_findpsw):

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.backButton.clicked.connect(self.jmp_login)
        self.findpswbutton.clicked.connect(self.find_lostpsw)

    @QtCore.pyqtSlot()
    def jmp_login(self):
        from .login_window import LoginWindow
        self.close()
        w = LoginWindow()
        w.show()

    @QtCore.pyqtSlot()
    def find_lostpsw(self):
        if self.passwordLineEdit.text()!= self.passwordLineEdit_2.text():
            self.showDialog(t="抱歉",s="前后两次密码不一致")
            return


        if type(response) is Email:
            self.showDialog(t="恭喜", s="成功!!")
        else :
            self.showDialog(t="抱歉", s="邮箱账号错误 或网络状况不佳 请重新")

    def showDialog(self,t:str, s:str):
        title = t
        content = s
        w = MessageBox(title, content, self)
        if w.exec():
            print('Yes button is pressed')
        else:
            print('Cancel button is pressed')
