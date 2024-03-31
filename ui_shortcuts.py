from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_Shortcuts(object):
    def __init__(self, Shortcuts):
        Shortcuts.setObjectName("Shortcuts")
        Shortcuts.resize(450, 600)
        Shortcuts.setMinimumSize(QtCore.QSize(450, 600))
        Shortcuts.setMaximumSize(QtCore.QSize(450, 600))
        self.headerWidget = QtWidgets.QWidget(parent=Shortcuts)
        self.headerWidget.setGeometry(QtCore.QRect(0, 0, 450, 35))
        self.headerWidget.setMinimumSize(QtCore.QSize(450, 35))
        self.headerWidget.setMaximumSize(QtCore.QSize(450, 35))
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

        self.retranslateUi(Shortcuts)
        QtCore.QMetaObject.connectSlotsByName(Shortcuts)

    def retranslateUi(self, Shortcuts):
        _translate = QtCore.QCoreApplication.translate
        Shortcuts.setWindowTitle(_translate("Shortcuts", "Form"))
        self.headingLabel.setText(_translate("Shortcuts", "Shortcuts - YT Player"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Shortcuts = QtWidgets.QWidget()
    ui = Ui_Shortcuts(Shortcuts)
    Shortcuts.show()
    sys.exit(app.exec())
