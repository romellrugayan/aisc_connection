from PyQt5.QtWidgets import QDialog
from PyQt5.QtGui import QIcon
from PyQt5.uic import loadUi


class MaterialDialog(QDialog):
    def __init__(self):
        super(MaterialDialog, self).__init__()
        loadUi("ui/materialspecs.ui", self)
        self.setWindowIcon(QIcon('resources/icons/conndesign.png'))
        self.loadMaterial()

    def loadMaterial(self):
        self.steel_combo.addItems(["A36", "A992"])
        self.bolt_combo.addItems(["A325-N", "A325-X", "A490-N", "A490-X"])
        self.weld_combo.addItems(["E60XX", "E70XX"])

    def getMaterial(self):
        return self.steel_combo.currentText(), self.bolt_combo.currentText(), self.weld_combo.currentText()



