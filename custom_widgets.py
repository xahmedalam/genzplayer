from PyQt6.QtWidgets import QProgressBar
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QMouseEvent, QIcon, QPixmap
from PyQt6.QtMultimedia import QMediaPlayer


class CustomQProgressBar(QProgressBar):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.player: QMediaPlayer = None
        self.playing = False

    def setPlayer(self, player: QMediaPlayer) -> None:
        self.player = player

    def mousePressEvent(self, event: QMouseEvent | None) -> None:
        if event.button() == Qt.MouseButton.LeftButton:
            pos_x = event.pos().x()
            width = self.width()
            min_value = self.minimum()
            max_value = self.maximum()
            progress_value = int((pos_x / width) * (max_value - min_value) + min_value)
            self.player.setPosition(progress_value)
        return super().mousePressEvent(event)

    def mouseMoveEvent(self, event: QMouseEvent | None) -> None:
        pos_x = event.pos().x()
        width = self.width()
        min_value = self.minimum()
        max_value = self.maximum()
        progress_value = int((pos_x / width) * (max_value - min_value) + min_value)
        self.player.pause()
        self.player.setPosition(progress_value)
        return super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event: QMouseEvent | None) -> None:
        if self.playing:
            self.player.play()
        return super().mouseReleaseEvent(event)


class Icon(QIcon):
    def __init__(self, filename: str, DIR: str = ":/icon/img"):
        super().__init__()
        self.addPixmap(QPixmap(f"{DIR}/{filename}"), QIcon.Mode.Normal, QIcon.State.Off)
