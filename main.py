from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QMenu, QFileDialog, QProxyStyle, QStyle
from PyQt6.QtCore import QUrl, Qt, QTimer
from PyQt6.QtGui import QKeyEvent, QPixmap, QCursor, QMouseEvent, QContextMenuEvent, QFontDatabase
from PyQt6.QtMultimedia import QMediaPlayer, QAudioOutput
from PyQt6.QtMultimediaWidgets import QVideoWidget
from custom_widgets import Icon
from interface import Interface
from author import Author
from shortcuts import Shortcuts
from fonts import FONTS
from datetime import timedelta
from platform import system
import resources
import style
import json
import sys


OS = system()

if OS == "Windows":
    PATH_POINT = "\\"
else:
    PATH_POINT = "/"


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        try:
            with open(f"{BASE_DIR}{PATH_POINT}settings.json") as f:
                self.settings = json.load(f)
        except:
            self.settings = {"volume": 100, "muted": False}
        
        try:
            self.file = sys.argv[1]
        except:
            self.file = None
        
        self.repeat_video = False
        self.old_cursor_position = None
        self.hide_player_widget_time = 0
        self.cursor_showing = True

        super().__init__()
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.centralWidget = QWidget(self)
        self.centralWidget.setFocus()
        self.setCentralWidget(self.centralWidget)
        self.ui = Interface(self.centralWidget)

        self.videoOutput = QVideoWidget()
        self.audioOutput = QAudioOutput(self)
        self.player = QMediaPlayer(self)
        self.player.setAudioOutput(self.audioOutput)
        self.player.setVideoOutput(self.videoOutput)

        self.videoOutput.hide()
        self.ui.videoWidgetLayout.addWidget(self.videoOutput)
        
        self.ui.playBtn.clicked.connect(self.play)
        self.ui.muteBtn.clicked.connect(self.mute)
        self.ui.forwordBtn.clicked.connect(lambda: self.player.setPosition(self.player.position()+5000))
        self.ui.backwordBtn.clicked.connect(lambda: self.player.setPosition(self.player.position()-5000))
        self.ui.fullScreenBtn.clicked.connect(self.full_screen)
        self.ui.repeatBtn.clicked.connect(self.repeat)
        self.ui.minimizeBtn.clicked.connect(self.showMinimized)
        self.ui.maximizeBtn.clicked.connect(self.maximize)
        self.ui.exitBtn.clicked.connect(self.exit)
        
        self.ui.volumeSlider.valueChanged.connect(self.change_volume)
        self.player.positionChanged.connect(self.update_time_line)
        self.player.playingChanged.connect(self.playing_changed)
        self.ui.volumeSlider.setValue(self.settings["volume"])
        self.ui.videoTimeLine.setPlayer(self.player)

        self.show_hide_player_widget_timer = QTimer(self)
        self.show_hide_player_widget_timer.setInterval(100)
        self.show_hide_player_widget_timer.timeout.connect(self.show_hide_player_widget)

        self.ui.headerWidget.mouseMoveEvent = self.header_widget_mouse_move
        self.ui.headerWidget.mouseDoubleClickEvent = self.header_widget_mouse_db_click
        self.ui.videoWidget.contextMenuEvent = self.video_widget_context_menu
        self.ui.videoWidget.mouseDoubleClickEvent = self.video_widget_mouse_db_click

        # Right Click Menu
        self.menu = QMenu(self)
        self.menu.setObjectName("menu")
        self.menu.addAction(Icon("open_file.png"), "Open File", self.open_file)
        self.menu.addAction(Icon("keyboard.png"), "Shortcuts", lambda: Shortcuts(BASE_DIR).exec())
        self.menu.addAction(Icon("author.png"), "Author", lambda: Author(BASE_DIR).exec())
        self.menu.setCursor(QCursor(QPixmap(":/icon/img/cursor.png")))

        if not self.file is None:
            filename = self.file.split(PATH_POINT)[-1]
            self.setWindowTitle(f"{filename} - YT Player")
            self.ui.headingLabel.setText(f"{filename} - YT Player")
            self.player.setSource(QUrl.fromLocalFile(self.file))
            
            if self.player.hasVideo():
                QTimer.singleShot(2500, lambda: self.player.stop() or self.ui.playBtn.click() or QTimer.singleShot(50, self.videoOutput.show))
            else:
                QTimer.singleShot(100, lambda: self.player.stop() or self.ui.playBtn.click())
        else:
            self.setWindowTitle("YT Player")
            self.ui.headingLabel.setText("YT Player")
            self.ui.playBtn.setEnabled(False)
            self.ui.forwordBtn.setEnabled(False)
            self.ui.backwordBtn.setEnabled(False)
            self.ui.videoTimeLine.setEnabled(False)

        if self.settings["volume"] == 0:
            self.change_volume()
        if self.settings["muted"]:
            self.ui.muteBtn.click()


    def maximize(self):
        if self.isMaximized():
            self.showNormal()
            self.ui.maximizeBtn.setIcon(Icon("restore.png"))
            self.ui.headerWidget.setStyleSheet("")
            self.ui.playerWidget.setStyleSheet("")
        else:
            self.showMaximized()
            self.ui.maximizeBtn.setIcon(Icon("maximize.png"))
            self.ui.headerWidget.setStyleSheet("#headerWidget{border-radius: 0px;}")
            self.ui.playerWidget.setStyleSheet("#playerWidget{border-radius: 0px;}")


    def exit(self):
        if self.audioOutput.isMuted():
            self.settings["muted"] = True
        else:
            self.settings["muted"] = False
        
        self.settings["volume"] = self.ui.volumeSlider.value()
        
        with open(f"{BASE_DIR}/settings.json", "w") as f:
            json.dump(self.settings, f)
        
        self.player.stop()
        self.close()


    def play(self) -> None:
        if not self.player.isPlaying() and self.player.position() == self.player.duration():
            self.player.setPosition(0)
            self.player.play()
            self.ui.videoTimeLine.playing = True
            self.ui.playBtn.setIcon(Icon("pause.png"))
        elif self.player.isPlaying():
            self.player.pause()
            self.ui.videoTimeLine.playing = False
            self.ui.playBtn.setIcon(Icon("play.png"))
        else:
            self.player.play()
            self.ui.videoTimeLine.playing = True
            self.ui.playBtn.setIcon(Icon("pause.png"))


    def mute(self) -> None:
        value = self.ui.volumeSlider.value()

        if self.audioOutput.isMuted():
            if value == 0:
                self.ui.volumeSlider.setValue(100)
                self.ui.muteBtn.setIcon(Icon("speaker_100%.png"))
            elif value > 50:
                self.ui.muteBtn.setIcon(Icon("speaker_100%.png"))
            else:
                self.ui.muteBtn.setIcon(Icon("speaker_50%.png"))
            self.audioOutput.setMuted(False)
        else:
            self.ui.muteBtn.setIcon(Icon("speaker_muted.png"))
            self.audioOutput.setMuted(True)


    def change_volume(self) -> None:
        value = self.ui.volumeSlider.value()
        
        if self.audioOutput.isMuted():
            self.audioOutput.setMuted(False)
        
        if value == 0:
            self.audioOutput.setMuted(True)
            self.ui.muteBtn.setIcon(Icon("speaker_muted.png"))
        elif value > 50:
            self.ui.muteBtn.setIcon(Icon("speaker_100%.png"))
        else:
            self.ui.muteBtn.setIcon(Icon("speaker_50%.png"))
        
        self.audioOutput.setVolume(value/100)


    def update_time_line(self) -> None:
        duration = self.player.duration()
        position = self.player.position()
        time_delta = timedelta(milliseconds=position)
        time = str(time_delta).split(".")[0]
        
        if len(time) != 8:
            time = f"0{time}"
        
        self.ui.videoTimeLine.setValue(position)
        self.ui.currentDurationLabel.setText(time)

        if (position+200) > duration:
            if not self.videoOutput.isHidden():
                self.videoOutput.hide()
        elif self.videoOutput.isHidden() and self.player.hasVideo():
            QTimer.singleShot(500, lambda: self.videoOutput.show() if self.videoOutput.isHidden() and self.player.hasVideo() else None)


    def playing_changed(self) -> None:
        duration = self.player.duration()
        position = self.player.position()
        time_delta = timedelta(milliseconds=duration)
        time = str(time_delta).split(".")[0]
        
        if len(time) != 8:
            time = f"0{time}"
        
        self.ui.videoTimeLine.setMaximum(duration)
        self.ui.videoDurationLabel.setText(time)

        if self.repeat_video and position == duration:
            self.player.setPosition(0)
            self.ui.playBtn.click()
        elif position == duration:
            self.ui.videoTimeLine.playing = False
            self.player.pause()
            self.ui.playBtn.setIcon(Icon("play.png"))


    def full_screen(self) -> None:
        self.set_cursor()
        
        if not self.isFullScreen():
            self.ui.headerWidget.hide()
            self.showFullScreen()
            self.show_hide_player_widget_timer.start()
            self.ui.fullScreenBtn.setIcon(Icon("normal_screen.png"))
        else:
            self.ui.headerWidget.show()
            self.ui.playerWidget.show()
            self.maximize()
            self.show_hide_player_widget_timer.stop()
            self.ui.fullScreenBtn.setIcon(Icon("full_screen.png"))


    def set_cursor(self, show=True) -> None:
        if show:
            self.setCursor(QCursor(QPixmap(":/icon/img/cursor.png")))
            self.cursor_showing = True
        else:
            self.setCursor(QCursor(Qt.CursorShape.BlankCursor))
            self.cursor_showing = False


    def show_hide_player_widget(self) -> None:
        cursor_position = self.cursor().pos()

        if cursor_position != self.old_cursor_position:
            self.old_cursor_position = cursor_position
            if self.ui.playerWidget.isHidden():
                if self.menu.isHidden():
                    self.ui.playerWidget.show()
                self.set_cursor()
                self.hide_player_widget_time = 1000
        else:
            if self.cursor_showing and self.ui.playerWidget.isHidden():
                self.set_cursor(False)
            elif self.hide_player_widget_time != 0 and not self.ui.playerWidget.underMouse():
                self.hide_player_widget_time -= 100
            elif not self.ui.playerWidget.isHidden() and not self.ui.playerWidget.underMouse() and self.hide_player_widget_time == 0:
                self.ui.playerWidget.hide()
                self.set_cursor(False)


    def repeat(self):
        if self.repeat_video:
            self.repeat_video = False
            self.ui.repeatBtn.setStyleSheet("")
        else:
            self.repeat_video = True
            self.ui.repeatBtn.setStyleSheet("background-color: #ffbf3f;")


    def open_file(self):
        filename, _ = QFileDialog.getOpenFileName(self, "Open Video", "", "All Media (*);;")
        
        if filename:
            self.videoOutput.hide()
            QTimer.singleShot(
                50,
                lambda: self.player.stop()
                or QTimer.singleShot(
                    100,
                    lambda: self.player.setSource(QUrl.fromLocalFile(filename))
                    or QTimer.singleShot(
                        100,
                        lambda: self.player.stop()
                        or self.ui.playBtn.click()
                        or QTimer.singleShot(
                            100,
                            lambda: self.videoOutput.show() if self.player.hasVideo() else self.videoOutput.hide()),
                    ),
                ),
            )
            
            if self.file is None:
                self.ui.playBtn.setEnabled(True)
                self.ui.forwordBtn.setEnabled(True)
                self.ui.backwordBtn.setEnabled(True)
                self.ui.videoTimeLine.setEnabled(True)
            
            self.file = filename
            _filename = filename.split('/')[-1]
            self.setWindowTitle(f"{_filename} - YT Player")
            self.ui.headingLabel.setText(f"{_filename} - YT Player")


    def header_widget_mouse_move(self, event: QMouseEvent | None) -> None:
        if not self.isMaximized():
            pos_x = int(int(event.globalPosition().x()) - (self.width() / 2))
            pos_y = int(int(event.globalPosition().y()) - (self.ui.headerWidget.height() / 2))
            self.move(pos_x, pos_y)


    def header_widget_mouse_db_click(self, event: QMouseEvent | None) -> None:
        if event.button() == Qt.MouseButton.LeftButton:
            self.ui.maximizeBtn.click()


    def video_widget_mouse_db_click(self, event: QMouseEvent | None) -> None:
        if event.button() == Qt.MouseButton.LeftButton:
            if self.isFullScreen():
                self.ui.fullScreenBtn.click()
            elif self.isMaximized():
                self.ui.fullScreenBtn.click()
            else:
                self.ui.maximizeBtn.click()


    def video_widget_context_menu(self, event: QContextMenuEvent | None) -> None:
        self.menu.exec(event.globalPos())


    def keyPressEvent(self, event: QKeyEvent | None) -> None:
        if event.key() == Qt.Key.Key_Space:
            self.ui.playBtn.click()
        elif event.key() == Qt.Key.Key_Left:
            self.ui.backwordBtn.click()
        elif event.key() == Qt.Key.Key_Right:
            self.ui.forwordBtn.click()
        elif event.key() == Qt.Key.Key_Up:
            self.ui.volumeSlider.setValue(self.ui.volumeSlider.value() + 5)
        elif event.key() == Qt.Key.Key_Down:
            self.ui.volumeSlider.setValue(self.ui.volumeSlider.value() - 5)
        elif event.key() == Qt.Key.Key_M:
            self.ui.muteBtn.click()
        elif event.key() == Qt.Key.Key_F:
            self.ui.fullScreenBtn.click()
        elif event.key() == Qt.Key.Key_R:
            self.ui.repeatBtn.click()
        elif event.key() == Qt.Key.Key_O:
            self.open_file()
        elif event.key() == Qt.Key.Key_Q:
            self.ui.exitBtn.click()
        return super().keyPressEvent(event)


class MyProxyStyle(QProxyStyle):
    def pixelMetric(self, QStyle_PixelMetric, option=None, widget=None):

        if QStyle_PixelMetric == QStyle.PixelMetric.PM_SmallIconSize:
            return 40
        else:
            return QProxyStyle.pixelMetric(self, QStyle_PixelMetric, option, widget)


if __name__ == "__main__":
    if PATH_POINT in sys.argv[0]:
        BASE_DIR = sys.argv[0][::-1].split(PATH_POINT, 1)[1][::-1]
    else:
        from pathlib import Path
        BASE_DIR = str(Path().resolve(__file__))
    
    app = QApplication(sys.argv)
    
    for font in FONTS:
        QFontDatabase.addApplicationFontFromData(bytes.fromhex(font))
    
    myStyle = MyProxyStyle('Fusion')
    app.setStyle(myStyle)
    
    window = MainWindow()
    window.setMinimumSize(500, 400)
    window.resize(500, 400)
    window.set_cursor()
    window.setWindowIcon(Icon("logo_large.png", ":/img/img"))
    window.setWindowFlags(Qt.WindowType.FramelessWindowHint)
    window.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
    # with open(f"{BASE_DIR}/src/css/style.css") as f:
    #     window.setStyleSheet(f.read())
    window.setStyleSheet(style.STYLE)
    window.maximize()
    
    sys.exit(app.exec())
