import sys

import httpx
import requests
from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtGui import QIcon, QDesktopServices, QPixmap
from PyQt5.QtWidgets import QApplication, QFrame, QHBoxLayout, QLineEdit, QPushButton, QVBoxLayout, QInputDialog, \
    QMessageBox, QLabel, QScrollArea, QWidget
from qfluentwidgets import (NavigationItemPosition, MessageBox, setTheme, Theme, FluentWindow,
                            NavigationAvatarWidget, qrouter, SubtitleLabel, setFont, InfoBadge,
                            InfoBadgePosition, FluentBackgroundTheme)
from qfluentwidgets import FluentIcon as FIF
import simnet


class Widget(QFrame):

    def __init__(self, text: str, parent=None):
        super().__init__(parent=parent)
        self.vBoxLayout = QVBoxLayout(self)
        self.setObjectName(text.replace(' ', '-'))

class HomeInterface(Widget):
    def __init__(self, text: str, parent=None):
        super().__init__('Home', parent)

            # 创建滚动区域
        scroll_area = QScrollArea(self)
        scroll_area.setWidgetResizable(True)

        # 创建滚动内容的 QWidget
        scroll_content = QWidget()
        scroll_layout = QVBoxLayout(scroll_content)

            # 添加图片、名字、信息和按钮
        for i in range(5):  # 添加5个条目
            layout = QHBoxLayout()

            # 左边的图片
            image_label = QLabel(scroll_content)
            pixmap = QPixmap(':/resource/login_picture')
            image_label.setPixmap(pixmap)
            layout.addWidget(image_label)

            # 中间的名字和信息
            middle_layout = QVBoxLayout()

            name_label = QLabel('Your Name', scroll_content)
            middle_layout.addWidget(name_label)

            info_label = QLabel('Additional info here', scroll_content)
            middle_layout.addWidget(info_label)

            layout.addLayout(middle_layout)

            # 右边的详情按钮
            details_button = QPushButton('Details', scroll_content)
            details_button.clicked.connect(lambda checked, text='Details about this item': self.show_details(text))
            layout.addWidget(details_button)

                # 将每个条目布局添加到滚动布局
            scroll_layout.addLayout(layout)

            # 设置滚动内容的布局
            scroll_content.setLayout(scroll_layout)

            # 将滚动内容设置为滚动区域的子部件
            scroll_area.setWidget(scroll_content)

            # 将滚动区域添加到主布局
            self.vBoxLayout.addWidget(scroll_area)

    def show_details(self, details):
        # 这里可以定义如何展示详情信息
        # 例如弹出一个消息框
        QMessageBox.information(self, 'Details', details)

    def get_Character (self):
        from ..config import url, userid, character
        ans = []
        for cid in character:
            data = {
            'userid': userid,
            'cid': cid
            }
            r = httpx.post(url+"/user/get", data=data)
            if r.status_code == 200:
                ans.append(r.json())
            else:
                print(r.status_code)
        return ans






class NoteInterface(Widget):
    def __init__(self,text: str, parent=None):
        super().__init__('Note', parent)



class SettingInterface(Widget):
    def __init__(self, text: str, parent=None):
        super().__init__('Note',parent)



class Window(FluentWindow):

    def __init__(self):
        super().__init__()

        # create sub interface
        self.homeInterface = HomeInterface('Home', self)
        self.searchInterface = Widget('Search Interface', self)
        self.administratorInterface = Widget('Administrator Interface', self)
        self.noteInterface = NoteInterface('note',self);
        self.settingInterface = SettingInterface('', self)
        self.initNavigation()
        self.initWindow()

    def initNavigation(self):
        self.addSubInterface(self.homeInterface, FIF.HOME, 'Home')
        self.addSubInterface(self.searchInterface, FIF.SEARCH, 'Search')
        self.addSubInterface(self.administratorInterface, FIF.CLOUD, 'Administrator')
        self.addSubInterface(self.noteInterface,FIF.ACCEPT,'NOTE')
        self.addSubInterface(self.settingInterface, FIF.SETTING,'')
        self.navigationInterface.addSeparator()
        self.navigationInterface.addWidget(
            routeKey='avatar',
            widget=NavigationAvatarWidget('about us', ':/resource/login_picture.jpeg'),
            onClick=self.showInputBox,
            position=NavigationItemPosition.BOTTOM,
        )
        item = self.navigationInterface.widget(self.administratorInterface.objectName())
        InfoBadge.attension(
            text=1,
            parent=item.parent(),
            target=item,
            position=InfoBadgePosition.NAVIGATION_ITEM
        )

    def initWindow(self):
        self.resize(1000, 700)
        self.setWindowIcon(QIcon(':/resource/login_picture.jpeg'))
        self.setWindowTitle('star_query_rail')
        desktop = QApplication.desktop().availableGeometry()
        w, h = desktop.width(), desktop.height()
        self.move(w // 2 - self.width() // 2, h // 2 - self.height() // 2)

    def bind_cookie(self, text: str) -> int:
        from ..config import url, token  # 请确保正确导入 url 和 token
        headers = {
            'account': 'application/json',
            'Authorization': token,
            'Content-Type': 'application/json'
        }
        data = {'cookie': text}
        r = httpx.post(url + "/user/", headers=headers, json=data)
        status = r.status_code
        return status

    def showInputBox(self):
        text, ok = QInputDialog.getText(self, 'Cookie', 'Enter your cookie:')
        if ok:
            status = self.bind_cookie(text)
            if status == 200:
                QMessageBox.information(self, 'Success', 'Cookie bound successfully!')
            elif status == 401:
                QMessageBox.warning(self, 'Error', 'authorization error!')




