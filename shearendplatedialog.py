from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtWidgets import QDialog, QMessageBox, QApplication
from PyQt5.uic import loadUi
import sqlite3
import sys


class ShearEndPlateDialog(QDialog):

    def __init__(self):
        super(ShearEndPlateDialog, self).__init__()
        loadUi("ui/shearendplate.ui", self)
        self.setWindowIcon(QIcon('resources/icons/conndesign.png'))
        self.loadImage('resources/images/shear_endplate1.png')

    def loadImage(self, image_path):
        canvas = QPixmap(image_path)
        self.canvas_label.setPixmap(canvas)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    dialog = ShearEndPlateDialog()
    dialog.show()
    sys.exit(app.exec_())