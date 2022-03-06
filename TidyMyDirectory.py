import os
import sys

from PySide2 import QtGui, QtCore
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
    QListWidgetItem, QGridLayout
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
    path = QFileDialog.getExistingDirectory()
    os.chdir(path)

    files = sort_by_ext(path)

    count = 0
    prod_png_count = 0
    prod_jpg_count = 0
    weta_png_count = 0
    weta_jpg_count = 0

    for count, f in enumerate(files):

        f_fullname, f_ext = os.path.splitext(f)

        # split file name and number
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

        #  todo: For all other names and extensions
        else:
            if f_ext == ".png":
                prod_png_count += 1
                f_name = renamed_file(f_name, prod_png_count)

            elif f_ext == ".jpg":
                prod_jpg_count += 1
                f_name = renamed_file(f_name, prod_jpg_count)

            new_name = f'{f_name}{f_ext}'
            print(f"Renaming " + f + " to " + new_name)
            os.rename(f, new_name)


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

        # Button UI
        browse_button = QPushButton("Choose a folder to tidy up", self)
        browse_button.move(80, 230)
        browse_button.resize(750, 270)
        browse_button.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        browse_button.setStyleSheet(
            "*{ background-color: '#36B0CB';" +
            "border-radius: 35px;" +
            "font-size: 20px;" +
            "font-weight: 2px;" +
            "color: 'white';" +
            "padding: 10px 0px;" +
            "margin: 100px 200px; }" +
            "*:hover{background: '#36A2BB'; }"
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

    def button_clicked(self):
        dlg = CustomDialog(self)
        button = dlg.exec_()

        if button == 1:  # 1 = QDialogBox.Ok
            rename_resequence()
            print("success")
        else:
            print("cancelled")


def main():
    app = QApplication(sys.argv)

    GUI = TidyMyDirectory()
    GUI.show()

    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
