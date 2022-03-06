import os
import sys

from PySide2 import QtGui, QtCore
# from PySide2.QtCore import QBasicTimer, Qt
from PySide2.QtGui import QPixmap, QCursor, QIcon
from PySide2.QtWidgets import (
    QApplication,
    QLabel,
    QPushButton,
    QMessageBox,
    QFileDialog,
    QListWidget,
    QDialog,
    QMainWindow,
    QDialogButtonBox,
    QVBoxLayout,
    QListWidgetItem,
    QProgressBar
)


class CustomDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Renaming these folders")

        QBtn = QDialogButtonBox.Ok | QDialogButtonBox.Cancel

        self.buttonBox = QDialogButtonBox(QBtn)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        path = selected_directory()
        files = [f for f in os.listdir(path)]
        list_of_files = QListWidget()

        for count, f in enumerate(files):
            QListWidgetItem(f, list_of_files)

        self.layout = QVBoxLayout()

        folder = QLabel("Chosen Directory: <strong>" + path + "</strong>")
        message = QLabel("\nThese folders will be renamed sequentially by extension, is that okay?")

        self.layout.addWidget(folder)
        self.layout.addWidget(message)
        self.layout.addWidget(list_of_files)
        self.layout.addWidget(self.buttonBox)
        self.setLayout(self.layout)


def selected_directory():
    return QFileDialog.getExistingDirectory()


def sort_by_ext(path):
    files = [f for f in os.listdir(path)
             if os.path.isfile(os.path.join(path, f))]

    files.sort(key=lambda f: os.path.splitext(f)[1])

    return files


def renamed_file(name, count):
    if count < 10:
        # zero-pad sequence
        return name + "." + str(count).zfill(2)
    else:
        return name + "." + str(count)


def rename_resequence():
    path = selected_directory()
    os.chdir(path)

    files = sort_by_ext(path)

    prod_png_count = 0
    prod_jpg_count = 0
    weta_png_count = 0
    weta_jpg_count = 0

    for count, f in enumerate(files):

        f_fullname, f_ext = os.path.splitext(f)

        # split file name and number
        try:
            f_name, _f_num = f_fullname.split(".")

            if f_name.lower() == "weta":
                if f_ext == ".png":

                    weta_png_count += 1
                    f_name = renamed_file(f_name, weta_png_count)

                elif f_ext == ".jpg":
                    weta_jpg_count += 1
                    f_name = renamed_file(f_name, weta_jpg_count)

                new_name = f'{f_name}{f_ext}'
                print(f"Renaming " + f + " to " + new_name)
                os.rename(f, new_name)

            elif f_name.lower() == "prodeng":
                if f_ext == ".png":
                    prod_png_count += 1
                    f_name = renamed_file(f_name, prod_png_count)

                elif f_ext == ".jpg":
                    prod_jpg_count += 1
                    f_name = renamed_file(f_name, prod_jpg_count)

                new_name = f'{f_name}{f_ext}'
                print(f"Renaming " + f + " to " + new_name)
                os.rename(f, new_name)

            #  skip other files
            else:
                continue

        except BaseException as e:
            print("An error has occurred: {}".format(e))


class TidyMyDirectory(QMainWindow):

    def __init__(self):
        super(TidyMyDirectory, self).__init__()

        self.setup()

    def setup(self):
        self.setFixedSize(900, 600)
        self.setStyleSheet("background: 'white';")
        self.setWindowTitle('Tidy my Directory!')
        self.setWindowIcon(QIcon("Icon.png"))

        # Setting the logo and icon of the program
        logo = QLabel(self)
        image = QPixmap('Logo.png')
        logo.setPixmap(image)
        logo.resize(logo.sizeHint())
        logo.move(183, 110)

        steps = "To use this program: \n 1. Choose a folder you want to tidy up\n 2. Select OK once you've chosen the " \
                "your folder \n 3. Once you click Ok, the program will immediately clean up your directory! :) "

        styles = "font-size: 15px;" + "font-weight: bold;" + "color: '#36B0CB'; "

        instructions = QLabel("Hover for instructions", self)
        instructions.resize(300, 50)
        instructions.setStyleSheet(styles)
        instructions.setToolTip(steps)

        instructions.move(80, 15)

        # Info Icon + instructions
        info = QLabel(self)
        info_icon = QPixmap('info.png')
        info.move(10, 0)
        info.setPixmap(info_icon)
        info.resize(60, 80)
        info.setStyleSheet(styles)
        info.setToolTip(steps)

        # Button UI
        browse_button = QPushButton("Choose a folder to tidy up", self)
        browse_button.move(250, 300)
        browse_button.resize(400, 80)
        browse_button.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        browse_button.setStyleSheet(
            "*{ background-color: '#36B0CB';" +
            "border-radius: 40px;" +
            "font-size: 20px;" +
            "font-weight: bold;" +
            "color: 'white'; }" +
            "*:hover{background: '#129FBE'; }"
        )
        browse_button.clicked.connect(self.button_clicked)

        self.show()

    def closeEvent(self, event: QtGui.QCloseEvent):
        action = QMessageBox.question(self, "Exiting Tidy my Directory", "Are you sure you want to quit?",
                                      QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if action == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

    # todo: add logic for progress bar here
    def button_clicked(self):

        # progress = QProgressBar(self)
        # popup = QDialog(self)
        # popup.setWindowTitle("Processing images")

        if CustomDialog(self).exec_() == 1:  # 1 = accepted / OK
            rename_resequence()
            print("function has finished running")
        else:
            print("cancelled")

    # def processing_timer(self):
    #     self.completed = 0
    #
    #     while self.completed < 100:
    #         self.completed += 0.0001
    #         self.progress.setValue(self.completed)


def main():
    app = QApplication(sys.argv)

    gui = TidyMyDirectory()
    gui.show()

    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
