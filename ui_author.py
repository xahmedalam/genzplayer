from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_Author(object):
    def __init__(self, Author):
        Author.setObjectName("Author")
        Author.resize(400, 500)
        Author.setMinimumSize(QtCore.QSize(400, 500))
        Author.setMaximumSize(QtCore.QSize(400, 500))
        self.headerWidget = QtWidgets.QWidget(parent=Author)
        self.headerWidget.setGeometry(QtCore.QRect(0, 0, 400, 35))
        self.headerWidget.setMinimumSize(QtCore.QSize(400, 35))
        self.headerWidget.setMaximumSize(QtCore.QSize(400, 35))
        self.headerWidget.setObjectName("headerWidget")
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout(self.headerWidget)
        self.horizontalLayout_6.setContentsMargins(12, 0, 12, 0)
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.logoLabel = QtWidgets.QLabel(parent=self.headerWidget)
        self.logoLabel.setMinimumSize(QtCore.QSize(20, 21))
        self.logoLabel.setMaximumSize(QtCore.QSize(20, 21))
        self.logoLabel.setPixmap(QtGui.QPixmap(":/icon/img/logo.png"))
        self.logoLabel.setObjectName("logoLabel")
        self.horizontalLayout_6.addWidget(self.logoLabel)
        self.headingLabel = QtWidgets.QLabel(parent=self.headerWidget)
        self.headingLabel.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.headingLabel.setObjectName("headingLabel")
        self.horizontalLayout_6.addWidget(self.headingLabel)
        self.exitBtn = QtWidgets.QPushButton(parent=self.headerWidget)
        self.exitBtn.setMinimumSize(QtCore.QSize(20, 20))
        self.exitBtn.setMaximumSize(QtCore.QSize(20, 20))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icon/img/exit.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.exitBtn.setIcon(icon)
        self.exitBtn.setIconSize(QtCore.QSize(14, 14))
        self.exitBtn.setObjectName("exitBtn")
        self.horizontalLayout_6.addWidget(self.exitBtn)
        self.githubBtn = QtWidgets.QPushButton(parent=Author)
        self.githubBtn.setGeometry(QtCore.QRect(179, 422, 42, 40))
        self.githubBtn.setObjectName("githubBtn")
        self.copyEmailBtn = QtWidgets.QPushButton(parent=Author)
        self.copyEmailBtn.setGeometry(QtCore.QRect(350, 323, 20, 19))
        self.copyEmailBtn.setObjectName("copyEmailBtn")

        self.retranslateUi(Author)
        QtCore.QMetaObject.connectSlotsByName(Author)

    def retranslateUi(self, Author):
        _translate = QtCore.QCoreApplication.translate
        self.headingLabel.setText(_translate("Author", "Author - YT Player"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Author = QtWidgets.QWidget()
    ui = Ui_Author(Author)
    Author.show()
    sys.exit(app.exec())
