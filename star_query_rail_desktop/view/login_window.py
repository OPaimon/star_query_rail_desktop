import sys

from PyQt5 import QtCore
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor, QIcon, QPixmap
from PyQt5.QtWidgets import QApplication
from qfluentwidgets import (
    InfoBarIcon,
    SplitTitleBar,
    TeachingTip,
    TeachingTipTailPosition,
    isDarkTheme,
    setThemeColor,
)
from star_query_rail_desktop.clinet.action import get_info, login
from star_query_rail_desktop.clinet.config import settings, status

from ..config import url
from .ui_loginwindow import Ui_Form


def isWin11():
    return sys.platform == "win32" and sys.getwindowsversion().build >= 22000


if isWin11():
    from qframelesswindow import AcrylicWindow as Window
else:
    from qframelesswindow import FramelessWindow as Window


class LoginWindow(Window, Ui_Form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        # setTheme(Theme.DARK)
        setThemeColor("#28afe9")

        self.setTitleBar(SplitTitleBar(self))
        self.titleBar.raise_()

        self.label.setScaledContents(False)
        self.setWindowTitle("STAR_QUERY_RAIL")
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
        self.move(w // 2 - self.width() // 2, h // 2 - self.height() // 2)

        # connect to slot
        self.pushButton.clicked.connect(self.jmp_mainwindow)
        self.pushButton_3.clicked.connect(self.jmp_register)

    def resizeEvent(self, e):
        super().resizeEvent(e)
        pixmap = QPixmap(":/resource/login_picture.jpeg").scaled(
            self.label.size(), Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation
        )
        self.label.setPixmap(pixmap)

    @QtCore.pyqtSlot()
    def jmp_register(self):
        from .register_window import register_window

        settings.API_url = (
            "http://" + self.lineEdit.text() + ":" + self.lineEdit_2.text()
        )
        self.close()
        w = register_window()
        w.show()

    @QtCore.pyqtSlot()
    def jmp_mainwindow(self):
        from .mainwindow import Window

        url = "http://" + self.lineEdit.text() + ":" + self.lineEdit_2.text()

        settings.API_url = url

        client = login(self.lineEdit_3.text(), self.lineEdit_4.text())
        user = get_info()
        print((user))
        if client is not None:
            self.close()
            w = Window()
            w.show()
        else:
            self.showBottomTip()

    def showBottomTip(self):
        TeachingTip.create(
            target=self.pushButton_2,
            icon=InfoBarIcon.SUCCESS,
            title="error",
            content="账号或密码有误 请重新登录",
            isClosable=True,
            tailPosition=TeachingTipTailPosition.TOP,
            duration=2000,
            parent=self,
        )
