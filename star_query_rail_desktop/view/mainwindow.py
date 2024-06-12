import sys

import httpx
import requests
from PyQt5 import QtCore
from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtGui import QIcon, QDesktopServices, QPixmap
from PyQt5.QtNetwork import QNetworkAccessManager, QNetworkRequest
from PyQt5.QtWidgets import QApplication, QFrame, QHBoxLayout, QLineEdit, QPushButton, QVBoxLayout, QInputDialog, \
    QMessageBox, QLabel, QScrollArea, QWidget, QDialog, QSizePolicy, QSpacerItem
from qfluentwidgets import (NavigationItemPosition, MessageBox, setTheme, Theme, FluentWindow,
                            NavigationAvatarWidget, qrouter, SubtitleLabel, setFont, InfoBadge,
                            InfoBadgePosition, FluentBackgroundTheme, FlyoutView, PushButton, Flyout, setThemeColor,
                            SplitTitleBar)
from qfluentwidgets import FluentIcon as FIF
from star_query_rail_client import AuthenticatedClient as Client
from star_query_rail_client.api.user import get_characters_detail_user_get_post
from star_query_rail_client.api.example import get_characters_example_post
from star_query_rail_client.models import UserCreate, EUCPublic, UserTest, ConnectUCRegister, StarRailDetailCharacters, StarRailDetailCharacter
from star_query_rail_client.types import Response
import functools

import simnet
from xcffib.xproto import Window

from ..config import url, token_dict

class Widget(QFrame):

    def __init__(self, text: str, parent=None):
        super().__init__(parent=parent)
        self.vBoxLayout = QVBoxLayout(self)
        self.setObjectName(text.replace(' ', '-'))


class CustomDialog(QDialog):
    def __init__(self, items: StarRailDetailCharacters, item: StarRailDetailCharacter):
        super().__init__()
        self.setWindowTitle('details')
        self.setFixedSize(800, 600)

        # 创建主布局
        main_layout = QHBoxLayout()

        # 左边的图片
        pixmap = QPixmap()
        response = requests.get(item.image)
        if response.status_code == 200:
            pixmap.loadFromData(response.content)
            image_label = QLabel()
            image_label.setPixmap(pixmap.scaled(350, 640, Qt.KeepAspectRatio, Qt.SmoothTransformation))
            main_layout.addWidget(image_label)

        # 右边的数据滚动区域
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)  # 让内容自适应滚动区域大小
        scroll_content = QWidget()
        scroll_layout = QVBoxLayout(scroll_content)

        # 添加数据布局
        name_level_ele_rarity_layout = QHBoxLayout()
        name_level_ele_rarity_layout.addWidget(QLabel("名字:"))
        name_level_ele_rarity_layout.addWidget(QLabel(item.name))
        name_level_ele_rarity_layout.addSpacing(10)
        name_level_ele_rarity_layout.addWidget(QLabel("等级:"))
        name_level_ele_rarity_layout.addWidget(QLabel(str(item.level)))
        name_level_ele_rarity_layout.addWidget(QLabel("稀有度:"))
        name_level_ele_rarity_layout.addWidget(QLabel(str(item.rarity)))
        name_level_ele_rarity_layout.addWidget(QLabel("属性:"))
        name_level_ele_rarity_layout.addWidget(QLabel(item.element))
        name_level_ele_rarity_layout.addWidget(QLabel("命座:"))
        name_level_ele_rarity_layout.addWidget(QLabel(str(item.rank)))
        scroll_layout.addLayout(name_level_ele_rarity_layout)

        for proper in item.properties:
            properitieslayout = QHBoxLayout()
            url: str
            name: str
            for tag in items.property_info:
                if tag.property_type == proper.property_type:
                    name = tag.name
                    url = tag.icon
                    break
            picture = QPixmap()
            response = requests.get(url)
            if response.status_code == 200:
                picture.loadFromData(response.content)
                picture_label = QLabel()
                picture_label.setPixmap(picture.scaled(40, 20, Qt.KeepAspectRatio, Qt.SmoothTransformation))
                properitieslayout.addWidget(picture_label)
            properitieslayout.addWidget(QLabel(name + ":"))
            properitieslayout.addWidget(QLabel(str(proper.base) + "+" + str(proper.add) + '=' + str(proper.final)))
            scroll_layout.addLayout(properitieslayout)
        scroll_layout.addWidget(QLabel("圣遗物:"))
        scroll_layout.addSpacing(10)

        for relic in item.relics:
            reliclayout = QHBoxLayout()
            reliclayout.setAlignment(Qt.AlignLeft)
            relic_image = QPixmap()
            response = requests.get(relic.icon)
            if response.status_code == 200:
                relic_image.loadFromData(response.content)
                reimage_label = QLabel()
                reimage_label.setPixmap(relic_image.scaled(50, 40, Qt.KeepAspectRatio, Qt.SmoothTransformation))
                reliclayout.addWidget(reimage_label)

            relicdatalayout = QVBoxLayout()
            relicdatalayout.addWidget(QLabel("名字:" + relic.name + "   等级:" + str(relic.level)))
            des = QLabel(relic.desc)
            des.setWordWrap(True)
            relicdatalayout.addWidget(des)

            relic_properity = relic.main_property
            relic_properity_layout = QHBoxLayout()
            url: str
            name: str
            for tag in items.property_info:
                if tag.property_type == relic_properity.property_type:
                    name = tag.name
                    url = tag.icon
                    break
            picture = QPixmap()
            response = requests.get(url)
            if response.status_code == 200:
                picture.loadFromData(response.content)
                picture_label = QLabel()
                picture_label.setPixmap(picture.scaled(40, 20, Qt.KeepAspectRatio, Qt.SmoothTransformation))
                relic_properity_layout.addWidget(picture_label)
            relic_properity_layout.addWidget(QLabel(name + " 数值:" + str(relic_properity.value) + " 强化次数:" + str(relic_properity.times)))
            relicdatalayout.addLayout(relic_properity_layout)

            for relic_properity in relic.properties:
                relic_properity_layout = QHBoxLayout()
                url: str
                name: str
                for tag in items.property_info:
                    if tag.property_type == relic_properity.property_type:
                        name = tag.name
                        url = tag.icon
                        break
                picture = QPixmap()
                response = requests.get(url)
                if response.status_code == 200:
                    picture.loadFromData(response.content)
                    picture_label = QLabel()
                    picture_label.setPixmap(picture.scaled(40, 20, Qt.KeepAspectRatio, Qt.SmoothTransformation))
                    relic_properity_layout.addWidget(picture_label)
                relic_properity_layout.addWidget(QLabel(name + " 数值:" + str(relic_properity.value) + " 强化次数:" + str(relic_properity.times)))
                relicdatalayout.addLayout(relic_properity_layout)
            reliclayout.addLayout(relicdatalayout)
            scroll_layout.addLayout(reliclayout)


        for relic in item.ornaments:
            reliclayout = QHBoxLayout()
            reliclayout.setAlignment(Qt.AlignLeft)
            relic_image = QPixmap()
            print(relic.icon)
            response = requests.get(relic.icon)
            if response.status_code == 200:
                relic_image.loadFromData(response.content)
                reimage_label = QLabel()
                reimage_label.setPixmap(relic_image.scaled(50, 40, Qt.KeepAspectRatio, Qt.SmoothTransformation))
                reliclayout.addWidget(reimage_label)

            relicdatalayout = QVBoxLayout()
            relicdatalayout.addWidget(QLabel("名字:" + relic.name + "   等级:" + str(relic.level)))
            rec = QLabel(relic.desc)
            rec.setWordWrap(True)
            relicdatalayout.addWidget(rec)

            relic_properity = relic.main_property
            relic_properity_layout = QHBoxLayout()
            url: str
            name: str
            for tag in items.property_info:
                if tag.property_type == relic_properity.property_type:
                    name = tag.name
                    url = tag.icon
                    break
            picture = QPixmap()
            response = requests.get(url)
            if response.status_code == 200:
                picture.loadFromData(response.content)
                picture_label = QLabel()
                picture_label.setPixmap(picture.scaled(40, 20, Qt.KeepAspectRatio, Qt.SmoothTransformation))
                relic_properity_layout.addWidget(picture_label)
            relic_properity_layout.addWidget(
                QLabel(name + " 数值:" + str(relic_properity.value) + " 强化次数:" + str(relic_properity.times)))
            relicdatalayout.addLayout(relic_properity_layout)

            for relic_properity in relic.properties:
                relic_properity_layout = QHBoxLayout()
                url: str
                name: str
                for tag in items.property_info:
                    if tag.property_type == relic_properity.property_type:
                        name = tag.name
                        url = tag.icon
                        break
                picture = QPixmap()
                response = requests.get(url)
                if response.status_code == 200:
                    picture.loadFromData(response.content)
                    picture_label = QLabel()
                    picture_label.setPixmap(picture.scaled(40, 20, Qt.KeepAspectRatio, Qt.SmoothTransformation))
                    relic_properity_layout.addWidget(picture_label)
                relic_properity_layout.addWidget(
                    QLabel(name + " 数值:" + str(relic_properity.value) + " 强化次数:" + str(relic_properity.times)))
                relicdatalayout.addLayout(relic_properity_layout)
            reliclayout.addLayout(relicdatalayout)
            scroll_layout.addLayout(reliclayout)


        #EQUIPMENT
        equipment_layout = QHBoxLayout()
        pixmap = QPixmap()
        response = requests.get(item.equip.icon)
        if response.status_code == 200:
            pixmap.loadFromData(response.content)
            image_label = QLabel()
            image_label.setPixmap(pixmap.scaled(50, 40, Qt.KeepAspectRatio, Qt.SmoothTransformation))
            equipment_layout.addWidget(image_label)

        equipment_des_layout =QVBoxLayout()
        name_level_layout = QHBoxLayout()
        name_level_layout.addWidget(QLabel("名字:"+item.equip.name))
        name_level_layout.addWidget(QLabel("等级:"+str(item.equip.level)))
        equipment_des_layout.addLayout(name_level_layout)

        des_layout = QHBoxLayout()
        des = QLabel(item.equip.desc)
        des.setWordWrap(True)
        equipment_des_layout.addWidget(des)

        equipment_layout.addLayout(equipment_des_layout)
        scroll_layout.addLayout(equipment_layout)

        spacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        scroll_layout.addItem(spacer)
        scroll_content.setLayout(scroll_layout)
        scroll_area.setWidget(scroll_content)
        main_layout.addWidget(scroll_area)

        # 将主布局设置给对话框
        self.setLayout(main_layout)







class HomeInterface(Widget):
    def __init__(self, text: str, parent=None):
        super().__init__('Home', parent)


        items =self.get_Character()
            # 创建滚动区域
        scroll_area = QScrollArea(self)
        scroll_area.setWidgetResizable(True)

        # 创建滚动内容的 QWidget
        scroll_content = QWidget()
        scroll_layout = QVBoxLayout(scroll_content)

        self.manager = QNetworkAccessManager()
        self.manager.finished.connect(self.on_image_downloaded)
            # 添加图片、名字、信息和按钮
        for item in items.avatar_list:
            layout = QHBoxLayout()

            # 左边的图片
            image_label = QLabel(scroll_content)
            layout.addWidget(image_label)

            # 下载图片
            url =item.icon  # 替换为实际图片的URL
            request = QNetworkRequest(QUrl(url))
            self.manager.get(request)
            image_label.setProperty('url', url)  # 将URL与标签关联

            # 中间的名字和信息
            middle_layout = QVBoxLayout()

            name_label = QLabel('Your Name', scroll_content)
            middle_layout.addWidget(name_label)

            info_label = QLabel('Additional info here', scroll_content)
            middle_layout.addWidget(info_label)

            layout.addLayout(middle_layout)

            # 右边的详情按钮
            details_button = QPushButton('Details', scroll_content)
            details_button.clicked.connect(functools.partial(self.show, items,item))
            layout.addWidget(details_button)
            details_button.setFixedWidth(150)

                # 将每个条目布局添加到滚动布局
            scroll_layout.addLayout(layout)

            # 设置滚动内容的布局
            scroll_content.setLayout(scroll_layout)

            # 将滚动内容设置为滚动区域的子部件
            scroll_area.setWidget(scroll_content)

            # 将滚动区域添加到主布局
            self.vBoxLayout.addWidget(scroll_area)

    @QtCore.pyqtSlot()
    def show(self, items: StarRailDetailCharacters,item: StarRailDetailCharacter):
        print(1)
        w = CustomDialog(items,item)
        w.exec()

    def on_image_downloaded(self, reply):
        if reply.error() == 0:
            url = reply.request().url().toString()
            data = reply.readAll()
            pixmap = QPixmap()
            pixmap.loadFromData(data)

            # 查找关联的标签并设置图片
            for label in self.findChildren(QLabel):
                if label.property('url') == url:
                    label.setPixmap(pixmap)
                    label.setScaledContents(True)
                    label.setFixedSize(pixmap.size())
                    break
        else:
            print("Error downloading image:", reply.errorString())



    def get_Character (self):
        from ..config import token
        from ..config import character
        from ..config import cookies, url
        user_test = UserTest(userid=character.pop(), cookie=cookies)
        body = ConnectUCRegister(userid=284738632,cid=100678548)
        client = Client(base_url=url, token=token)
        with client as client:
            response: StarRailDetailCharacters = get_characters_detail_user_get_post.sync(client=client,body=body)
        # from ..config import url, userid, character
        # ans = []
        # for cid in character:
        #
        #     headers_val:str = token_dict.get("token_type") + " " + token_dict.get("access_token")
        #     headers: dict = {"Authorizzation": headers_val}
        #     client: Client = Client(base_url=url,headers=headers)
        #     connect_uc_reg: ConnectUCRegister = ConnectUCRegister(userid=userid,cid=cid)
        #     with client as client:
        #         response: Response[StarRailDetailCharacters] = get_characters_detail_user_get_post.sync(client=client,body=connect_uc_reg)
        #     response: StarRailDetailCharacters = response
        #     ans.append(response.to_dict()
        return response






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




