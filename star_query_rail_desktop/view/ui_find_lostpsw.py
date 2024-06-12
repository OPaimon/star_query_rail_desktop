from PyQt5 import QtCore, QtGui, QtWidgets
from qfluentwidgets import BodyLabel, CheckBox, HyperlinkButton, LineEdit, PrimaryPushButton
import requests
class Ui_findpsw(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(300, 500)
        Form.setMinimumSize(QtCore.QSize(100, 200))

        #
        self.backgroundLabel = QtWidgets.QLabel(Form)
        self.backgroundLabel.setGeometry(Form.rect())
        self.backgroundLabel.setPixmap(QtGui.QPixmap("./resource/background.jpeg").scaled(self.backgroundLabel.size()))
        self.backgroundLabel.setScaledContents(True)
        self.backgroundLabel.lower()
        # 创建一个垂直布局
        self.verticalLayout = QtWidgets.QVBoxLayout(Form)
        self.verticalLayout.setContentsMargins(20, 20, 20, 20)
        self.verticalLayout.setSpacing(20)
        self.verticalLayout.setObjectName("verticalLayout")

        # 添加一个返回按钮，并将其向上移动
        self.backButton = PrimaryPushButton(Form)
        self.backButton.setText("返回")
        self.backButton.setObjectName("backButton")
        self.verticalLayout.addWidget(self.backButton, 0, QtCore.Qt.AlignLeft)
        self.upperSpacer = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(self.upperSpacer)

        # 添加一个邮箱文本框，并将其向下移动
        self.emailLineEdit = LineEdit(Form)
        self.emailLineEdit.setPlaceholderText("Email")
        self.emailLineEdit.setClearButtonEnabled(True)
        self.emailLineEdit.setObjectName("emailLineEdit")
        self.verticalLayout.addWidget(self.emailLineEdit)
        self.middleSpacer = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.verticalLayout.addItem(self.middleSpacer)

        # 添加一个密码文本框
        self.passwordLineEdit = LineEdit(Form)
        self.passwordLineEdit.setPlaceholderText("oldPassword")
        self.passwordLineEdit.setEchoMode(QtWidgets.QLineEdit.Password)
        self.passwordLineEdit.setClearButtonEnabled(True)
        self.passwordLineEdit.setObjectName("passwordLineEdit")
        self.verticalLayout.addWidget(self.passwordLineEdit)

        # 添加一个密码文本框
        self.passwordLineEdit_2 = LineEdit(Form)
        self.passwordLineEdit_2.setPlaceholderText("newPassword")
        self.passwordLineEdit_2.setEchoMode(QtWidgets.QLineEdit.Password)
        self.passwordLineEdit_2.setClearButtonEnabled(True)
        self.passwordLineEdit_2.setObjectName("newpasswordLineEdit")
        self.verticalLayout.addWidget(self.passwordLineEdit_2)

        self.passwordLineEdit_3 = LineEdit(Form)
        self.passwordLineEdit_3.setPlaceholderText("Psw")
        self.passwordLineEdit_3.setEchoMode(QtWidgets.QLineEdit.Password)
        self.passwordLineEdit_3.setClearButtonEnabled(True)
        self.passwordLineEdit_3.setObjectName("验证码")
        self.verticalLayout.addWidget(self.passwordLineEdit_3)

        self.findpswbutton = PrimaryPushButton(Form)
        self.findpswbutton.setText("find_lostpsw")
        self.findpswbutton.setObjectName("registerButton")
        self.verticalLayout.addWidget(self.findpswbutton, 0, QtCore.Qt.AlignHCenter)
        self.lowerSpacer = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(self.lowerSpacer)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "找回密码"))



