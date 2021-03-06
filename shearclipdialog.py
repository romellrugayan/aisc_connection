from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtWidgets import QDialog, QMessageBox, QApplication
from PyQt5.uic import loadUi
import sqlite3


class ShearClipDialog(QDialog):

    def __init__(self, isClipUpdated, clip_geometry):
        super(ShearClipDialog, self).__init__()
        loadUi("ui/shearclip.ui", self)
        self.setWindowIcon(QIcon('resources/icons/conndesign.png'))
        self.db = sqlite3.connect('data/aisc.db')
        self.db.row_factory = sqlite3.Row
        self.cur = self.db.cursor()
        self.isClipUpdated = isClipUpdated
        self.clip_geometry = clip_geometry
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
            self.loadImage('resources/images/shear_clip1.png')
        if self.support_rad_button2.isChecked():
            self.loadImage('resources/images/shear_clip2.png')
        if self.support_rad_button3.isChecked():
            self.loadImage('resources/images/shear_clip3.png')

    def loadData(self):
        self.cur.execute("SELECT size FROM shearclip")
        data = self.cur.fetchall()
        for size in data:
            self.main_combo.addItem(size[0])
            self.support_combo.addItem(size[0])

    def showMemberProperties(self):
        if not self.isClipUpdated:
            self.main_combo.setEditable(False)
            self.support_combo.setEditable(False)
            member = (self.main_combo.currentText(),)
            self.cur.execute("SELECT * FROM shearclip WHERE size=?", member)
            data = dict(self.cur.fetchone())
            self.dia_edit.setText(str(data['dia']))
            self.nos_edit.setText(str(data['nos']))
            self.gage_edit.setText(str(data['g']))
            self.spacing_edit.setText(str(data['spacing']))
            self.ev_edit.setText(str(data['ev']))
            self.eh_edit.setText(str(data['eh']))
            self.ta_edit.setText(str(data['ta']))
            self.H_edit.setText(str(data['H']))
            self.c_edit.setText(str(data['c']))
        else:
            self.main_combo.setEditable(True)
            self.support_combo.setEditable(True)
            self.main_combo.setCurrentText(self.clip_geometry['size'])
            self.dia_edit.setText(self.clip_geometry['dia'])
            self.nos_edit.setText(self.clip_geometry['nos'])
            self.gage_edit.setText(self.clip_geometry['g'])
            self.spacing_edit.setText(self.clip_geometry['spacing'])
            self.ev_edit.setText(self.clip_geometry['ev'])
            self.eh_edit.setText(self.clip_geometry['eh'])
            self.ta_edit.setText(self.clip_geometry['ta'])
            self.H_edit.setText(self.clip_geometry['H'])
            self.c_edit.setText(self.clip_geometry['c'])
            self.support_combo.setCurrentText(self.clip_geometry['size2'])
            self.setCheckedRadButton(self.clip_geometry['support'])

    def updateMemberProperties(self):
        self.main_combo.setEditable(False)
        member = (self.main_combo.currentText(),)
        self.cur.execute("SELECT * FROM shearclip WHERE size=?", member)
        data = dict(self.cur.fetchone())
        self.dia_edit.setText(str(data['dia']))
        self.nos_edit.setText(str(data['nos']))
        self.gage_edit.setText(str(data['g']))
        self.spacing_edit.setText(str(data['spacing']))
        self.ev_edit.setText(str(data['ev']))
        self.eh_edit.setText(str(data['eh']))
        self.ta_edit.setText(str(data['ta']))
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
        try:
            dia = float(self.dia_edit.text())
            nos = int(self.nos_edit.text())
            g = float(self.gage_edit.text())
            spacing = float(self.spacing_edit.text())
            ev = float(self.ev_edit.text())
            eh = float(self.eh_edit.text())
            ta = float(self.ta_edit.text())
            H = float(self.H_edit.text())
            c = float(self.c_edit.text())
            return True
        except ValueError:
            QMessageBox.critical(self, "Connection Design", "Non-numeric value is invalid. Parameters not saved!")
            return False

    def nonZeroValues(self):
        if float(self.dia_edit.text()) == 0 or float(self.dia_edit.text()) < 0:
            QMessageBox.critical(self, "Connection Design", "Zero or negative value is invalid. Parameters not saved!")
            return False
        if int(self.nos_edit.text()) == 0 or int(self.nos_edit.text()) < 0:
            QMessageBox.critical(self, "Connection Design", "Zero or negative value is invalid. Parameters not saved!")
            return False
        if float(self.gage_edit.text()) == 0 or float(self.gage_edit.text()) < 0:
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
        if float(self.ta_edit.text()) == 0 or float(self.ta_edit.text()) < 0:
            QMessageBox.critical(self, "Connection Design", "Zero or negative value is invalid. Parameters not saved!")
            return False
        if float(self.H_edit.text()) == 0 or float(self.H_edit.text()) < 0:
            QMessageBox.critical(self, "Connection Design", "Zero or negative value is invalid. Parameters not saved!")
            return False
        if float(self.c_edit.text()) == 0 or float(self.c_edit.text()) < 0:
            QMessageBox.critical(self, "Connection Design", "Zero or negative value is invalid. Parameters not saved!")
            return False
        return True

    def getConnGeometry(self):
        geometry = dict(size=self.main_combo.currentText(), dia=self.dia_edit.text(), nos=self.nos_edit.text(),
                        g=self.gage_edit.text(), spacing=self.spacing_edit.text(),
                        ev=self.ev_edit.text(), eh=self.eh_edit.text(), ta=self.ta_edit.text(),
                        H=self.H_edit.text(), c=self.c_edit.text(), support=self.supportType(),
                        size2=self.support_combo.currentText(), col=1, clip_size='L4x4x1/2')
        return geometry

    def closeEvent(self, event):
        rsp = QMessageBox.question(self, "Connection Design", "Close this Window?", QMessageBox.Yes | QMessageBox.No,
                                   QMessageBox.No)
        if rsp == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

