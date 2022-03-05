import os
import sys

from PySide2 import QtGui
from PySide2.QtWidgets import (
    QDesktopWidget,
    QApplication,
    QLineEdit,
    QLabel,
    QWidget,
    QToolTip,
    QPushButton,
    QMessageBox,
    QFileDialog,
    QInputDialog,
    QListView,
    QListWidget,
    QDialog,
    QMainWindow,
    QDialogButtonBox,
    QVBoxLayout, QListWidgetItem
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

        list = QListWidget()

        files = [f for f in os.listdir(path)]

        for count, f in enumerate(files):
            QListWidgetItem(f, list)

        self.layout = QVBoxLayout()
        message = QLabel("These folders will be renamed, is that okay?")

        self.layout.addWidget(message)
        self.layout.addWidget(list)
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
            # print(new_name)
            print(f"Renaming " + f + " to " + new_name)
            os.rename(f, new_name)

    print("success")


def confirmation(s):
    print("click", s)

    dlg = CustomDialog()
    if dlg.exec_():
        print("Success!")
    else:
        print("Cancel!")


class TidyMyDirectory(QMainWindow):

    def __init__(self):
        super(TidyMyDirectory, self).__init__()

        self.setup()

    def closeEvent(self, event: QtGui.QCloseEvent):
        action = QMessageBox.question(self, "Exiting Tidy my Directory", "Are you sure you want to quit?",
                                      QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if action == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

    def setup(self):

        QToolTip.setFont(QtGui.QFont('OpenSans', 10))

        # Folder Browser
        directory_label = QLabel('Directory:', self)
        directory_label.move(15, 40)

        self.etBrowser = QLineEdit('', self)
        self.etBrowser.resize(210, 20)
        self.etBrowser.move(90, 37)
        self.etBrowser.setEnabled(0)

        btnBrowse = QPushButton('Browse', self)
        btnBrowse.setToolTip('Select directory')
        btnBrowse.resize(btnBrowse.sizeHint())
        btnBrowse.move(305, 37)
        btnBrowse.clicked.connect(selected_directory)

        # Button UI
        btn = QPushButton('Clean up', self)
        btn.setToolTip('This will tidy up your directory.')
        btn.resize(btn.sizeHint())
        btn.move(5, 60)
        btn.clicked.connect(rename_resequence)

        button = QPushButton("Press me for a dialog!", self)
        button.resize(button.sizeHint())
        button.move(30, 160)
        button.clicked.connect(confirmation)

        self.setFixedSize(900, 600)
        self.center_window()

        self.setWindowTitle('Tidy my Directory!')
        self.show()

    def center_window(self):

        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())


def main():
    app = QApplication(sys.argv)
    ex = TidyMyDirectory()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
