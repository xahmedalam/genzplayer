from PyQt6.QtWidgets import QDialog, QWidget
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QCursor, QPixmap, QIcon, QMouseEvent
from ui_shortcuts import Ui_Shortcuts
import style


class Shortcuts(QDialog):
    def __init__(self, BASE_DIR: str, parent=None) -> None:
        super().__init__(parent)
        
        icon = QIcon()
        icon.addPixmap(QPixmap(":/img/img/logo_large.png"), QIcon.Mode.Normal, QIcon.State.Off)
        self.setWindowIcon(icon)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setCursor(QCursor(QPixmap(":/icon/img/cursor.png")))
        self.setWindowTitle("Shortcuts - YT Player")

        # with open(f"{BASE_DIR}/src/css/shortcuts.css") as f:
        #     self.setStyleSheet(f.read())
        self.setStyleSheet(style.SHORTCUTS)

        self.uiWidget = QWidget(self)
        self.ui = Ui_Shortcuts(self.uiWidget)
        
        self.ui.exitBtn.clicked.connect(self.close)

        self.ui.headerWidget.mouseMoveEvent = self.header_widget_mouse_move


    def header_widget_mouse_move(self, event: QMouseEvent | None) -> None:
        if not self.isMaximized():
            pos_x = int(int(event.globalPosition().x()) - (self.width() / 2))
            pos_y = int(int(event.globalPosition().y()) - (self.ui.headerWidget.height() / 2))
            self.move(pos_x, pos_y)


if __name__ == "__main__":
    from PyQt6.QtWidgets import QApplication
    import resources
    import sys

    app = QApplication(sys.argv)
    window = Shortcuts(BASE_DIR=sys.argv[0][::-1].split("/", 1)[1][::-1])
    window.show()
    sys.exit(app.exec())