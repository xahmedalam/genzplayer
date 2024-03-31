from PyQt6.QtWidgets import QDialog, QWidget
from PyQt6.QtCore import Qt, QUrl
from PyQt6.QtGui import QCursor, QPixmap, QIcon, QDesktopServices, QMouseEvent
from ui_author import Ui_Author
import clipboard
import style


class Author(QDialog):
    def __init__(self, BASE_DIR: str, parent=None) -> None:
        super().__init__(parent)

        icon = QIcon()
        icon.addPixmap(QPixmap(":/img/img/logo_large.png"), QIcon.Mode.Normal, QIcon.State.Off)
        self.setWindowIcon(icon)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setCursor(QCursor(QPixmap(":/icon/img/cursor.png")))
        self.setWindowTitle("Author - YT Player")

        # with open(f"{BASE_DIR}/src/css/author.css") as f:
        #     self.setStyleSheet(f.read())
        self.setStyleSheet(style.AUTHOR)

        self.uiWidget = QWidget(self)
        self.ui = Ui_Author(self.uiWidget)
        
        self.ui.exitBtn.clicked.connect(self.close)
        self.ui.copyEmailBtn.clicked.connect(lambda: clipboard.copy("m.ahmed.g.1982@gmail.com"))
        self.ui.githubBtn.clicked.connect(lambda: QDesktopServices().openUrl(QUrl("https://github.com/mahmedalam")))

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
    window = Author(BASE_DIR=sys.argv[0][::-1].split("/", 1)[1][::-1])
    window.show()
    sys.exit(app.exec())