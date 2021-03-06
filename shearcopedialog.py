from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtWidgets import QDialog, QMessageBox, QApplication
from PyQt5.uic import loadUi
import sqlite3
import sys


class ShearCopeDialog(QDialog):

    def __init__(self, isCopeUpdated, cope_geometry):
        super(ShearCopeDialog, self).__init__()
        loadUi("ui/shearcope.ui", self)
        self.setWindowIcon(QIcon('resources/icons/conndesign.png'))
        self.loadImage('resources/images/shear_notched.png')
        self.db = sqlite3.connect('data/aisc.db')
        self.db.row_factory = sqlite3.Row
        self.cur = self.db.cursor()
        self.isCopeUpdated = isCopeUpdated
        self.cope_geometry = cope_geometry
        self.loadData()
        self.showMemberProperties()
        self.main_combo.currentIndexChanged.connect(self.updateMemberProperties)
        self.support_combo.currentIndexChanged.connect(self.updateSupportProperties)

    def loadImage(self, image_path):
        canvas = QPixmap(image_path)
        self.canvas_label.setPixmap(canvas)

    def loadData(self):
        self.cur.execute("SELECT size FROM shearcope")
        data = self.cur.fetchall()
        for size in data:
            self.main_combo.addItem(size[0])
            self.support_combo.addItem(size[0])

    def showMemberProperties(self):
        if not self.isCopeUpdated:
            self.main_combo.setEditable(False)
            self.support_combo.setEditable(False)
            member = (self.main_combo.currentText(),)
            self.cur.execute("SELECT * FROM shearcope WHERE size=?", member)
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
            self.main_combo.setCurrentText(self.cope_geometry['size'])
            self.dia_edit.setText(self.cope_geometry['dia'])
            self.nos_edit.setText(self.cope_geometry['nos'])
            self.col_edit.setText(self.cope_geometry['col'])
            self.spacing_edit.setText(self.cope_geometry['spacing'])
            self.weld_edit.setText(self.cope_geometry['weld'])
            self.ev_edit.setText(self.cope_geometry['ev'])
            self.eh_edit.setText(self.cope_geometry['eh'])
            self.tg_edit.setText(self.cope_geometry['tg'])
            self.H_edit.setText(self.cope_geometry['H'])
            self.c_edit.setText(self.cope_geometry['c'])
            self.support_combo.setCurrentText(self.cope_geometry['size2'])

    def updateMemberProperties(self):
        self.main_combo.setEditable(False)
        member = (self.main_combo.currentText(),)
        self.cur.execute("SELECT * FROM shearcope WHERE size=?", member)
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

    def validateInput(self):
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
        geometry = dict(size=self.main_combo.currentText(), dia=self.dia_edit.text(), nos=self.nos_edit.text(),
                        col=self.col_edit.text(), spacing=self.spacing_edit.text(), weld=self.weld_edit.text(),
                        ev=self.ev_edit.text(), eh=self.eh_edit.text(), tg=self.tg_edit.text(),
                        H=self.H_edit.text(), c=self.c_edit.text(), support='Beam',
                        size2=self.support_combo.currentText())
        return geometry

    def closeEvent(self, event):
        rsp = QMessageBox.question(self, "Connection Design", "Close this Window?", QMessageBox.Yes | QMessageBox.No,
                                   QMessageBox.No)
        if rsp == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    dialog = ShearNotchedDialog()
    dialog.show()
    sys.exit(app.exec_())