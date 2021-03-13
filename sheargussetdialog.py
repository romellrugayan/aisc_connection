from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtWidgets import QDialog, QMessageBox
from PyQt5.uic import loadUi
import sqlite3


class ShearGussetDialog(QDialog):
    """
    User interface for Shear Connection of Gusset Plate Type.
    """

    def __init__(self, isGussetUpdated, gusset_geometry):
        super(ShearGussetDialog, self).__init__()
        loadUi("ui/sheargusset.ui", self)
        self.setWindowIcon(QIcon('resources/icons/conndesign.png'))
        self.db = sqlite3.connect('data/aisc.db')
        self.db.row_factory = sqlite3.Row
        self.cur = self.db.cursor()
        self.isGussetUpdated = isGussetUpdated
        self.gusset_geometry = gusset_geometry
        self.loadData()
        self.showMemberProperties()
        self.main_combo.currentIndexChanged.connect(self.updateMemberProperties)
        self.support_combo.currentIndexChanged.connect(self.updateSupportProperties)
        self.support_rad_button1.toggled.connect(self.changeImage)
        self.support_rad_button2.toggled.connect(self.changeImage)
        self.support_rad_button3.toggled.connect(self.changeImage)
        self.changeImage()

    def loadImage(self, image_path):
        canvas = QPixmap(image_path)
        self.canvas_label.setPixmap(canvas)

    def changeImage(self):
        if self.support_rad_button1.isChecked():
            self.loadImage('resources/images/shear_gusset1')
        if self.support_rad_button2.isChecked():
            self.loadImage('resources/images/shear_gusset2')
        if self.support_rad_button3.isChecked():
            self.loadImage('resources/images/shear_gusset3')

    def loadData(self):
        self.cur.execute("SELECT size FROM sheargusset")
        data = self.cur.fetchall()
        for size in data:
            self.main_combo.addItem(size[0])
            self.support_combo.addItem(size[0])

    def showMemberProperties(self):
        """
        Showing the saved connection geometry properties or retrieve the data from database
        """
        if not self.isGussetUpdated:
            self.main_combo.setEditable(False)
            self.support_combo.setEditable(False)
            member = (self.main_combo.currentText(),)
            self.cur.execute("SELECT * FROM sheargusset WHERE size=?", member)
            data = dict(self.cur.fetchone())
            self.dia_edit.setText(str(data['dia']))
            self.nos_edit.setText(str(data['nos']))
            self.col_edit.setText(str(data['col']))
            self.spacing_edit.setText(str(data['spacing']))
            self.weld_edit.setText(str(data['weld']))
            self.ev_edit.setText(str(data['ev']))
            self.eh_edit.setText(str(data['eh']))
            self.tg_edit.setText(str(data['tg']))
            self.H_edit.setText(str(data['H']))
            self.c_edit.setText(str(data['c']))
        else:
            self.main_combo.setEditable(True)
            self.support_combo.setEditable(True)
            self.main_combo.setCurrentText(self.gusset_geometry['size'])
            self.dia_edit.setText(self.gusset_geometry['dia'])
            self.nos_edit.setText(self.gusset_geometry['nos'])
            self.col_edit.setText(self.gusset_geometry['col'])
            self.spacing_edit.setText(self.gusset_geometry['spacing'])
            self.weld_edit.setText(self.gusset_geometry['weld'])
            self.ev_edit.setText(self.gusset_geometry['ev'])
            self.eh_edit.setText(self.gusset_geometry['eh'])
            self.tg_edit.setText(self.gusset_geometry['tg'])
            self.H_edit.setText(self.gusset_geometry['H'])
            self.c_edit.setText(self.gusset_geometry['c'])
            self.support_combo.setCurrentText(self.gusset_geometry['size2'])
            self.setCheckedRadButton(self.gusset_geometry['support'])

    def updateMemberProperties(self):
        self.main_combo.setEditable(False)
        member = (self.main_combo.currentText(),)
        self.cur.execute("SELECT * FROM sheargusset WHERE size=?", member)
        data = dict(self.cur.fetchone())
        self.dia_edit.setText(str(data['dia']))
        self.nos_edit.setText(str(data['nos']))
        self.col_edit.setText(str(data['col']))
        self.spacing_edit.setText(str(data['spacing']))
        self.weld_edit.setText(str(data['weld']))
        self.ev_edit.setText(str(data['ev']))
        self.eh_edit.setText(str(data['eh']))
        self.tg_edit.setText(str(data['tg']))
        self.H_edit.setText(str(data['H']))
        self.c_edit.setText(str(data['c']))

    def updateSupportProperties(self):
        self.support_combo.setEditable(False)

    def supportType(self):
        if self.support_rad_button1.isChecked():
            return "Beam"
        elif self.support_rad_button2.isChecked():
            return "Column Web"
        else:
            return "Column Flange"

    def setCheckedRadButton(self, caption):
        if caption == "Beam":
            self.support_rad_button1.setChecked(True)
        elif caption == "Column Web":
            self.support_rad_button2.setChecked(True)
        else:
            self.support_rad_button3.setChecked(True)

    def validateInput(self):
        """
        Validate if the user's input is valid numeric value
        """
        try:
            dia = float(self.dia_edit.text())
            nos = int(self.nos_edit.text())
            col = int(self.col_edit.text())
            spacing = float(self.spacing_edit.text())
            weld = float(self.weld_edit.text())
            ev = float(self.ev_edit.text())
            eh = float(self.eh_edit.text())
            tg = float(self.tg_edit.text())
            H = float(self.H_edit.text())
            c = float(self.c_edit.text())
            return True
        except ValueError:
            QMessageBox.critical(self, "Connection Design", "Non-numeric value is invalid. Parameters not saved!")
            return False

    def nonZeroValues(self):
        """
        Validate if the user's input is non-zero or not negative value.
        """
        if float(self.dia_edit.text()) == 0 or float(self.dia_edit.text()) < 0:
            QMessageBox.critical(self, "Connection Design", "Zero or negative value is invalid. Parameters not saved!")
            return False
        if int(self.nos_edit.text()) == 0 or int(self.nos_edit.text()) < 0:
            QMessageBox.critical(self, "Connection Design", "Zero or negative value is invalid. Parameters not saved!")
            return False
        if int(self.col_edit.text()) == 0 or int(self.col_edit.text()) < 0:
            QMessageBox.critical(self, "Connection Design", "Zero or negative value is invalid. Parameters not saved!")
            return False
        if float(self.spacing_edit.text()) == 0 or float(self.spacing_edit.text()) < 0:
            QMessageBox.critical(self, "Connection Design", "Zero or negative value is invalid. Parameters not saved!")
            return False
        if float(self.ev_edit.text()) == 0 or float(self.ev_edit.text()) < 0:
            QMessageBox.critical(self, "Connection Design", "Zero or negative value is invalid. Parameters not saved!")
            return False
        if float(self.eh_edit.text()) == 0 or float(self.eh_edit.text()) < 0:
            QMessageBox.critical(self, "Connection Design", "Zero or negative value is invalid. Parameters not saved!")
            return False
        if float(self.tg_edit.text()) == 0 or float(self.tg_edit.text()) < 0:
            QMessageBox.critical(self, "Connection Design", "Zero or negative value is invalid. Parameters not saved!")
            return False
        if float(self.H_edit.text()) == 0 or float(self.H_edit.text()) < 0:
            QMessageBox.critical(self, "Connection Design", "Zero or negative value is invalid. Parameters not saved!")
            return False
        if float(self.weld_edit.text()) == 0 or float(self.weld_edit.text()) < 0:
            QMessageBox.critical(self, "Connection Design", "Zero or negative value is invalid. Parameters not saved!")
            return False
        if float(self.c_edit.text()) == 0 or float(self.c_edit.text()) < 0:
            QMessageBox.critical(self, "Connection Design", "Zero or negative value is invalid. Parameters not saved!")
            return False
        return True

    def getConnGeometry(self):
        """
        Retrieve the value from the input widgets and save to dictionary. This method should be called after
        both methods; validateInput() and nonZeroValues() return True.
        """
        geometry = dict(size=self.main_combo.currentText(), dia=self.dia_edit.text(), nos=self.nos_edit.text(),
                        col=self.col_edit.text(), spacing=self.spacing_edit.text(), weld=self.weld_edit.text(),
                        ev=self.ev_edit.text(), eh=self.eh_edit.text(), tg=self.tg_edit.text(),
                        H=self.H_edit.text(), c=self.c_edit.text(), support=self.supportType(),
                        size2=self.support_combo.currentText())
        return geometry

    def closeEvent(self, event):
        rsp = QMessageBox.question(self, "Connection Design", "Close this Window?", QMessageBox.Yes | QMessageBox.No,
                                   QMessageBox.No)
        if rsp == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()



