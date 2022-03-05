import glob
import os
import re
import shutil
import sys

from PySide2 import QtGui
from PySide2.QtWidgets import QDesktopWidget, QApplication, QLineEdit, QLabel, QWidget, QToolTip, \
    QPushButton, QMessageBox, QFileDialog

PATH = "C:/Users\Mel\Documents/1.IMPORTANT/Unity_CodeChallenge/original - Copy"

files = [f for f in os.listdir(PATH)
         if os.path.isfile(os.path.join(PATH, f))]

files.sort(key=lambda f: os.path.splitext(f)[1])

for key in files:
    fileName, fileExtension = os.path.splitext(key)

png_ext_count = 0
jpg_ext_count = 0

for count, f in enumerate(files):

    f_fullname, f_ext = os.path.splitext(f)
    f_name, f_num = f_fullname.split(".")

    if f_name.lower() == "prodeng" and f_ext == ".png":
        png_ext_count += 1

        if png_ext_count < 10:
            f_name = "prodeng." + str(png_ext_count).zfill(2)
        else:
            f_name = "prodeng." + str(png_ext_count)

        new_name = f'{f_name}{f_ext}'

        print(new_name)
        os.rename(f, new_name)

#
    elif f_name.lower() == "weta":
        f_name = "weta." + ""
        new_name = f'{f_name}.{f_ext}'
        os.rename(f, new_name)
    else:
        pass
