import sys

from PyQt5 import QtCore
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QPixmap, QColor
from PyQt5.QtWidgets import QApplication
from qfluentwidgets import setThemeColor, SplitTitleBar, isDarkTheme, TeachingTipTailPosition, InfoBarIcon, TeachingTip
from star_query_rail_client import Client
from star_query_rail_client.models import BodyLoginAccessTokenLoginAccessTokenPost, Token
from star_query_rail_client.types import Response
from star_query_rail_client.api.login import login_access_token_login_access_token_post

from .ui_loginwindow import Ui_Form
from ..config import url


def isWin11():
    return sys.platform == 'win32' and sys.getwindowsversion().build >= 22000


if isWin11():
    from qframelesswindow import AcrylicWindow as Window
else:
    from qframelesswindow import FramelessWindow as Window


class LoginWindow(Window, Ui_Form):

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        # setTheme(Theme.DARK)
        setThemeColor('#28afe9')

        self.setTitleBar(SplitTitleBar(self))
        self.titleBar.raise_()

        self.label.setScaledContents(False)
        self.setWindowTitle('STAR_QUERY_RAIL')
        self.setWindowIcon(QIcon(":/resource/login_picture.jpeg"))
        self.resize(1000, 650)

        self.windowEffect.setMicaEffect(self.winId(), isDarkMode=isDarkTheme())
        if not isWin11():
            color = QColor(25, 33, 42) if isDarkTheme() else QColor(240, 244, 249)
            self.setStyleSheet(f"LoginWindow{{background: {color.name()}}}")

        self.titleBar.titleLabel.setStyleSheet("""
            QLabel{
                background: transparent;
                font: 13px 'Segoe UI';
                padding: 0 4px;
                color: white
            }
        """)

        desktop = QApplication.desktop().availableGeometry()
        w, h = desktop.width(), desktop.height()
        self.move(w//2 - self.width()//2, h//2 - self.height()//2)

        #connect to slot
        self.pushButton.clicked.connect(self.jmp_mainwindow)
        self.pushButton_3.clicked.connect(self.jmp_register)

    def resizeEvent(self, e):
        super().resizeEvent(e)
        pixmap = QPixmap(":/resource/login_picture.jpeg").scaled(
            self.label.size(), Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation)
        self.label.setPixmap(pixmap)

    @QtCore.pyqtSlot()
    def jmp_register(self):
        from .register_window import register_window
        self.close()
        w = register_window()
        w.show()


    @QtCore.pyqtSlot()
    def jmp_mainwindow(self):
        from .mainwindow import Window
        from ..config import token

        url = "http://" + self.lineEdit.text() + self.lineEdit_2.text()
        client = Client(base_url=url)
        username = self.lineEdit_3
        password=self.lineEdit_4
        username = "paimoe@bupt.edu.cn"
        password = "testpw"
        body = BodyLoginAccessTokenLoginAccessTokenPost(username=username,password=password)
        url = "http://" + self.lineEdit.text() + self.lineEdit_2.text()
        client = Client(base_url=url)
        username = self.lineEdit_3
        password = self.lineEdit_4
        username = "paimoe@bupt.edu.cn"
        password = "testpw"
        body = BodyLoginAccessTokenLoginAccessTokenPost(username=username, password=password)

        try:
            with client as client:
                response: Token = login_access_token_login_access_token_post.sync(client=client, body=body)

            if response:
                self.close()
                w = Window()
                w.show()
            else:
                self.showBottomTip()

        except Exception as e:
            print("连接错误:", e)
            self.showBottomTip()

    def showBottomTip(self):
        TeachingTip.create(
            target=self.pushButton_2,
            icon=InfoBarIcon.SUCCESS,
            title='error',
            content="账号或密码有误 请重新登录",
            isClosable=True,
            tailPosition=TeachingTipTailPosition.TOP,
            duration=2000,
            parent=self
        )






