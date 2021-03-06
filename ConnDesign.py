import sys
from pathlib import Path
from PyQt5.QtWidgets import (QApplication, QMainWindow, QFileDialog, QMessageBox, QTableWidgetItem)
from PyQt5.QtGui import QIcon
from PyQt5.uic import loadUi
from projectdialog import ProjectDialog
from matspecsdialog import MaterialDialog
from sheargussetdialog import ShearGussetDialog
from shearcopedialog import ShearCopeDialog
from shearclipdialog import ShearClipDialog
from shearendplatedialog import ShearEndPlateDialog
from loaddialog import LoadDialog
from utility.xmlwriter import XMLWriter
from utility.xmlreader import XMLReader
from utility.viewer import Viewer
from utility.detailer import Detailer
from utility.statusinfo import StatusInfo
from designresult import DesignResult
from resources import resources


class Window(QMainWindow):
    def __init__(self):
        super(Window, self).__init__()
        loadUi("ui/mainwindow.ui", self)
        self.setWindowIcon(QIcon('resources/icons/conndesign.png'))
        self.app_name = 'Connection Design v1.00'
        self.actionOpen.triggered.connect(self.openFileDialog)
        self.actionSave.triggered.connect(self.saveFileDialog)
        self.actionSaveAs.triggered.connect(self.saveFileAsDialog)
        self.actionDescription.triggered.connect(self.openProjectDialog)
        self.actionMaterialSpecs.triggered.connect(self.openMaterialDialog)
        self.actionShearGusset.triggered.connect(self.openShearGussetDialog)
        self.actionShearCope.triggered.connect(self.openShearCopeDialog)
        self.actionShearClipAngle.triggered.connect(self.openShearClipDialog)
        self.actionShearEndPlate.triggered.connect(self.openShearEndPlateDialog)
        self.actionLoadings.triggered.connect(self.openLoadDialog)
        self.actionCalculate.triggered.connect(self.designCalculation)
        self.actionExit.triggered.connect(self.exitApp)
        self.project_desc = {}
        self.mat_specs = ('A36', 'A325-N', 'E70XX')
        self.conn_type = ""
        self.gusset_geometry = {}
        self.cope_geometry = {}
        self.clip_geometry = {}
        self.load_data = []
        self.calc_result = []
        self.isProjectDescUpdated = False
        self.isMaterialUpdated = False
        self.isGussetUpdated = False
        self.isCopeUpdated = False
        self.isClipUpdated = False
        self.isSaved = False
        self.file_path = ""
        self.textEdit.setFontPointSize(10)
        self.text_info.setFontPointSize(10)

    def drawConnGeometry(self, conn_geometry):
        detailer = Detailer(self.conn_type, conn_geometry)
        detailer.drawDetail(self.canvas_label)

    def displayInfo(self, conn_geometry):
        status_info = StatusInfo(self.text_info, self.conn_type, conn_geometry)
        status_info.displayInfo()
        status_info.checkDimensions()

    def openFileDialog(self):
        user_dir = str(Path.home())
        # user_dir = str(Path.cwd()) + '/template'
        fileObj = QFileDialog.getOpenFileName(self, self.app_name, user_dir, filter="XML files (*.xml)")
        self.file_path = fileObj[0]
        if self.file_path != "":
            xml_reader = XMLReader(self.file_path)
            xml_reader.readProjectDesc(self.project_desc)
            self.mat_specs = xml_reader.readMaterial()
            self.text_info.clear()
            self.textEdit.clear()
            conn_geometry = {}
            self.conn_type = xml_reader.readConnGeometry(conn_geometry)

            if self.conn_type == 'ShearGusset':
                self.gusset_geometry = conn_geometry
                self.isGussetUpdated = True
                self.drawConnGeometry(self.gusset_geometry)
                self.displayInfo(self.gusset_geometry)
                self.openShearGussetDialog()

            elif self.conn_type == 'ShearCope':
                self.cope_geometry = conn_geometry
                self.isCopeUpdated = True
                self.drawConnGeometry(self.cope_geometry)
                self.displayInfo(self.cope_geometry)
                self.openShearCopeDialog()

            elif self.conn_type == 'ShearClip':
                self.clip_geometry = conn_geometry
                self.isClipUpdated = True
                self.drawConnGeometry(self.clip_geometry)
                self.displayInfo(self.clip_geometry)
                self.openShearClipDialog()

            self.load_data = []
            xml_reader.readLoads(self.load_data)
            self.isProjectDescUpdated = True
            self.isMaterialUpdated = True
            self.isSaved = True


    def saveFileDialog(self):
        if not self.isSaved:
            user_dir = str(Path.home())
            fileObj = QFileDialog.getSaveFileName(self, self.app_name, user_dir, filter="XML files (*.xml)")
            self.file_path = fileObj[0]
            if self.conn_type == 'ShearGusset':
                conn_geometry = self.gusset_geometry
            elif self.conn_type == 'ShearCope':
                conn_geometry = self.cope_geometry
            elif self.conn_type == 'ShearClip':
                conn_geometry = self.clip_geometry
            if self.file_path != "":
                if conn_geometry != "" and self.load_data != "":
                    xml_writer = XMLWriter()
                    xml_writer.projectDesc(self.project_desc)
                    xml_writer.material(self.mat_specs)
                    xml_writer.connGeometry(self.conn_type, conn_geometry)
                    xml_writer.loadings(self.load_data)
                    xml_writer.saveXMLFile(self.file_path)
                    self.isSaved = True
        else:
            if self.conn_type == 'ShearGusset':
                conn_geometry = self.gusset_geometry
            elif self.conn_type == 'ShearCope':
                conn_geometry = self.cope_geometry
            elif self.conn_type == 'ShearClip':
                conn_geometry = self.clip_geometry
            if conn_geometry != "" and self.load_data != "":
                xml_writer = XMLWriter()
                xml_writer.projectDesc(self.project_desc)
                xml_writer.material(self.mat_specs)
                xml_writer.connGeometry(self.conn_type, conn_geometry)
                xml_writer.loadings(self.load_data)
                xml_writer.saveXMLFile(self.file_path)

    def saveFileAsDialog(self):
        user_dir = str(Path.home())
        fileObj = QFileDialog.getSaveFileName(self, self.app_name, user_dir, filter="XML files (*.xml)")
        self.file_path = fileObj[0]
        if self.conn_type == 'ShearGusset':
            conn_geometry = self.gusset_geometry
        elif self.conn_type == 'ShearCope':
            conn_geometry = self.cope_geometry
        elif self.conn_type == 'ShearClip':
            conn_geometry = self.clip_geometry
        if self.file_path != "":
            if conn_geometry != "" and self.load_data != "":
                xml_writer = XMLWriter()
                xml_writer.projectDesc(self.project_desc)
                xml_writer.material(self.mat_specs)
                xml_writer.connGeometry(self.conn_type, conn_geometry)
                xml_writer.loadings(self.load_data)
                xml_writer.saveXMLFile(self.file_path)
                self.isSaved = True

    def openProjectDialog(self):
        dialog = ProjectDialog()
        if self.isProjectDescUpdated:
            dialog.setProjectDesc(self.project_desc)
        if dialog.exec_():
            self.project_desc = dialog.getProjectDesc()
            self.isProjectDescUpdated = True

    def openMaterialDialog(self):
        dialog = MaterialDialog()
        if self.isMaterialUpdated:
            dialog.steel_combo.setCurrentText(self.mat_specs[0])
            dialog.bolt_combo.setCurrentText(self.mat_specs[1])
            dialog.weld_combo.setCurrentText(self.mat_specs[2])
        if dialog.exec_():
            self.mat_specs = dialog.getMaterial()
            self.isMaterialUpdated = True
        else:
            QMessageBox.warning(self, self.app_name, "Design parameters not saved!")

    def openShearGussetDialog(self):
        dialog = ShearGussetDialog(self.isGussetUpdated, self.gusset_geometry)
        if len(self.gusset_geometry) != 0:
            dialog.showMemberProperties()
        if dialog.exec_():
            self.conn_type = "ShearGusset"
            if dialog.validateInput() and dialog.nonZeroValues():
                self.gusset_geometry = dialog.getConnGeometry()
                self.drawConnGeometry(self.gusset_geometry)
                self.text_info.clear()
                self.displayInfo(self.gusset_geometry)
            if len(self.gusset_geometry) != 0:
                self.isGussetUpdated = True
            dialog.db.close()
        else:
            QMessageBox.warning(self, self.app_name, "Design parameters not saved!")

    def openShearCopeDialog(self):
        dialog = ShearCopeDialog(self.isCopeUpdated, self.cope_geometry)
        if len(self.cope_geometry) != 0:
            dialog.showMemberProperties()
        if dialog.exec_():
            self.conn_type = "ShearCope"
            if dialog.validateInput() and dialog.nonZeroValues():
                self.cope_geometry = dialog.getConnGeometry()
                self.drawConnGeometry(self.cope_geometry)
                self.text_info.clear()
                self.displayInfo(self.cope_geometry)
            if len(self.cope_geometry) != 0:
                self.isCopeUpdated = True
            dialog.db.close()
        else:
            QMessageBox.warning(self, self.app_name, "Design parameters not saved!")

    def openShearClipDialog(self):
        dialog = ShearClipDialog(self.isClipUpdated, self.clip_geometry)
        if len(self.clip_geometry) != 0:
            dialog.showMemberProperties()
        if dialog.exec_():
            self.conn_type = "ShearClip"
            if dialog.validateInput() and dialog.nonZeroValues():
                self.clip_geometry = dialog.getConnGeometry()
                self.drawConnGeometry(self.clip_geometry)
                self.text_info.clear()
                self.displayInfo(self.clip_geometry)
            if len(self.clip_geometry) != 0:
                self.isClipUpdated = True
            dialog.db.close()

    def openShearEndPlateDialog(self):
        dialog = ShearEndPlateDialog()

        dialog.exec_()

    def openLoadDialog(self):
        dialog = LoadDialog()
        if len(self.load_data) != 0:
            for row in range(0, len(self.load_data)):
                for col in range(0, 8):
                    dialog.tableWidget.setItem(row, col, QTableWidgetItem(self.load_data[row][col]))
        if dialog.exec_():
            k = dialog.getRows()
            if dialog.validateInput(k):
                self.load_data = dialog.getLoads(k)
                QMessageBox.information(self, self.app_name, "Total number of load cases for design : " + str(k))
        else:
            QMessageBox.warning(self, self.app_name, "Design loadings not saved!")

    @staticmethod
    def maxStressRatio(results):
        index = 0
        max_ratio = 0
        max_index = 0
        for result in results:
            if result[2] > max_ratio:
                max_ratio = result[2]
                max_index = index
            index = index + 1
        return max_index, results[max_index][0], results[max_index][1], results[max_index][2]

    def designCalculation(self):
        if self.conn_type == 'ShearGusset':
            conn_geometry = self.gusset_geometry
        elif self.conn_type == 'ShearCope':
            conn_geometry = self.cope_geometry

        if len(conn_geometry) != 0 and len(self.load_data) != 0 and len(self.mat_specs) != 0 and len(self.project_desc) != 0:
            # display the input parameters
            self.textEdit.clear()
            viewer = Viewer(self.textEdit, self.conn_type)
            viewer.displayProject(self.project_desc)
            viewer.displayMaterial(self.mat_specs)
            viewer.displayConnGeometry(conn_geometry)
            viewer.displayLoadings(self.load_data)
            viewer.displayMaterialStrength(self.mat_specs)

            # do design calculation

            dr = DesignResult(self.mat_specs, self.conn_type, conn_geometry)
            self.calc_result = []
            bolt_shear = []
            bearing = []
            block_shear = []
            shear_yielding = []
            shear_rupture = []
            tensile_yielding = []
            tensile_rupture = []
            bending_in = []
            bending_out = []
            weld_shear = []
            if self.conn_type == 'ShearCope':
                web_block_shear = []
                web_shear_yielding = []
                web_shear_rupture = []
                web_tensile_yielding = []
                web_tensile_rupture = []
                web_bending_in = []
                web_bending_out = []
            for row in range(0, len(self.load_data)):
                design_load = self.load_data[row]
                bolt_shear.append(dr.check_bolt_shear(design_load))
                bearing.append(dr.check_bolt_bearing(design_load))
                block_shear.append(dr.check_plate_block_shear(design_load))
                shear_yielding.append(dr.check_plate_shear_yielding(design_load))
                shear_rupture.append(dr.check_plate_shear_rupture(design_load))
                tensile_yielding.append(dr.check_plate_tensile_yielding(design_load))
                tensile_rupture.append(dr.check_plate_tensile_rupture(design_load))
                bending_in.append(dr.check_plate_bending_in(design_load))
                bending_out.append(dr.check_plate_bending_out(design_load))
                weld_shear.append(dr.check_welding_shear(design_load))
                if self.conn_type == 'ShearCope':
                    web_block_shear.append(dr.check_web_block_shear(design_load))
                    web_shear_yielding.append(dr.check_web_shear_yielding(design_load))
                    web_shear_rupture.append(dr.check_web_shear_rupture(design_load))
                    web_tensile_yielding.append(dr.check_web_tensile_yielding(design_load))
                    web_tensile_rupture.append(dr.check_web_tensile_rupture(design_load))
                    web_bending_in.append(dr.check_web_bending_in(design_load))
                    web_bending_out.append(dr.check_web_bending_out(design_load))


            self.calc_result.append(self.maxStressRatio(bolt_shear))
            self.calc_result.append(self.maxStressRatio(bearing))
            self.calc_result.append(self.maxStressRatio(block_shear))
            self.calc_result.append(self.maxStressRatio(shear_yielding))
            self.calc_result.append(self.maxStressRatio(shear_rupture))
            self.calc_result.append(self.maxStressRatio(tensile_yielding))
            self.calc_result.append(self.maxStressRatio(tensile_rupture))
            self.calc_result.append(self.maxStressRatio(bending_in))
            self.calc_result.append(self.maxStressRatio(bending_out))
            self.calc_result.append(self.maxStressRatio(weld_shear))
            if self.conn_type == 'ShearCope':
                self.calc_result.append(self.maxStressRatio(web_block_shear))
                self.calc_result.append(self.maxStressRatio(web_shear_yielding))
                self.calc_result.append(self.maxStressRatio(web_shear_rupture))
                self.calc_result.append(self.maxStressRatio(web_tensile_yielding))
                self.calc_result.append(self.maxStressRatio(web_tensile_rupture))
                self.calc_result.append(self.maxStressRatio(web_bending_in))
                self.calc_result.append(self.maxStressRatio(web_bending_out))

            # display calculation result on textEdit
            viewer.displayCalculationResult(dr, self.calc_result)

            """QMessageBox.information(self, self.app_name, "Design calculation done! You can view the report.",
                                    QMessageBox.Ok)"""
        else:
            QMessageBox.warning(self, self.app_name, "Design parameters setting not complete yet!", QMessageBox.Ok)

    def closeEvent(self, event):
        rsp = QMessageBox.question(self, self.app_name, "Are you sure you want to exit?", QMessageBox.Yes | QMessageBox.No,
                                   QMessageBox.No)
        if rsp == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

    def exitApp(self):
        rsp = QMessageBox.question(self, self.app_name, "Are you sure you want to exit?", QMessageBox.Yes | QMessageBox.No,
                                   QMessageBox.No)
        if rsp == QMessageBox.Yes:
            sys.exit(0)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = Window()
    win.show()
    sys.exit(app.exec_())
