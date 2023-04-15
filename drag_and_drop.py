### qt drag and drop file
from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout , QProgressBar
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QFont
import similar_face_finder as finder


class WorkerThread(QThread):
    finished = pyqtSignal() # define a custom signal
    
    def run(self):

        finder.find_similar_face(img)
        self.finished.emit() # emit the signal when the work is done

class ImageLabel(QLabel):

    def __init__(self):

        super().__init__()

        self.setAlignment(Qt.AlignCenter)
        self.setText('\n\n Drop Image Here \n\n')
        self.setMaximumWidth(600)
        self.setMinimumHeight(500)
        self.setMaximumHeight(900)
        self.setScaledContents(True)
        self.setStyleSheet('''
            QLabel{
                border: 4px dashed #aaa
            }
        ''')

    def setPixmap(self, image):
        super().setPixmap(image)

class AppDemo(QWidget):

    def __init__(self):

        super().__init__()
        self.resize(600, 600)
        self.setAcceptDrops(True)

        # self.label = QLabel()
        self.label = QLabel("SIMILAR FACE FINDER")
        self.percentage = QLabel("")
        # self.label.setAlignment(Qt.AlignCenter)

        # progress bar
        self.progress_bar = QProgressBar(self)
        self.progress_bar.setGeometry(0, 0, 300, 25)
        self.progress_bar.setVisible(False)

        # Set the font style for the label
        font = QFont()
        font.setPointSize(24)
        font.setBold(True)
        self.label.setFont(font)
        self.percentage.setFont(font)

        mainLayout = QVBoxLayout()

        self.photoViewer = ImageLabel()

        mainLayout.addWidget(self.label)
        mainLayout.addWidget(self.progress_bar)
        # mainLayout.addLayout(lable_layout)
        mainLayout.addWidget(self.percentage)
        mainLayout.addWidget(self.photoViewer)

        self.setLayout(mainLayout)
    
    def start_progress(self):

        # Show the progress bar
        self.progress_bar.setVisible(True)

        # Start a timer to update the progress bar value
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_progress)
        self.timer.start(100)

    def update_progress(self):

        # Update the progress bar value
        value = finder.get_percentage()
        if value > 100:
            self.timer.stop()
            self.progress_bar.setVisible(False)
        else:
            self.progress_bar.setValue(value)

    def dragEnterEvent(self, event):

        if event.mimeData().hasImage:
            event.accept()
        else:
            event.ignore()

    def dragMoveEvent(self, event):

        if event.mimeData().hasImage:
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):

        if event.mimeData().hasImage:
            event.setDropAction(Qt.CopyAction)
            file_path = event.mimeData().urls()[0].toLocalFile()

            self.set_image(file_path)
            self.start_progress()

            global img
            img = file_path

            self.thread = WorkerThread()
            self.thread.start()

            event.accept()
        else:
            event.ignore()

    def set_image(self, file_path):
        self.photoViewer.setPixmap(QPixmap(file_path))