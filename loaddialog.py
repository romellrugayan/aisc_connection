from PyQt5.QtWidgets import (QDialog, QMessageBox, QTableWidgetItem, QFileDialog)
from PyQt5.QtGui import QIcon
from PyQt5.uic import loadUi
import xlrd
from pathlib import Path


class LoadDialog(QDialog):
    def __init__(self):
        super(LoadDialog, self).__init__()
        loadUi("ui/load.ui", self)
        self.setWindowIcon(QIcon('resources/icons/conndesign.png'))
        self.tableWidget.setColumnWidth(0, 80)
        self.tableWidget.setColumnWidth(1, 80)
        self.tableWidget.setColumnWidth(2, 80)
        self.tableWidget.setColumnWidth(3, 80)
        self.tableWidget.setColumnWidth(4, 80)
        self.tableWidget.setColumnWidth(5, 80)
        self.tableWidget.setColumnWidth(6, 80)
        self.tableWidget.setColumnWidth(7, 80)
        self.tableWidget.setHorizontalHeaderLabels(["Member", "Load Comb", "Node", "Fx (kip)", "Fy (kip)", "Fz (kip)",
                                                    "My (kip-in)", "Mz (kip-in)"])
        self.row = 6
        self.tableWidget.setRowCount(self.row)
        self.setLoads()
        self.excel_button.clicked.connect(self.readExcel)

    def getRows(self):
        k = 0
        for row in range(0, 6):
            item = QTableWidgetItem.text(self.tableWidget.item(row, 0))
            if item != '':
                k += 1
            else:
                break
        return k

    def setLoads(self):
        for row in range(0, self.row):
            for col in range(0, 3):
                self.tableWidget.setItem(row, col, QTableWidgetItem(""))
            for col in range(3, 8):
                self.tableWidget.setItem(row, col, QTableWidgetItem("0.0"))

    def getLoads(self, k):
        data = []
        for row in range(0, k):
            item = []
            for col in range(0, 8):
                item.append(QTableWidgetItem.text(self.tableWidget.item(row, col)))
            data.append(item)
        return data

    def validateInput(self, k):
        try:
            for row in range(0, k):
                for col in range(0, 3):
                    int(QTableWidgetItem.text(self.tableWidget.item(row, col)))
                for col in range(3, 8):
                    float(QTableWidgetItem.text(self.tableWidget.item(row, col)))
            return True
        except ValueError:
            QMessageBox.critical(self, "Connection Design", "Non-numeric value is invalid. Parameters not saved!")
            return False

    def readExcel(self):
        # user_dir = str(Path.home())
        user_dir = str(Path.cwd()) + '/template'
        fileObj = QFileDialog.getOpenFileName(self, "Connection Design", user_dir, filter="Excel files (*.xlsx)")
        path = fileObj[0]
        if path != "":
            inputWorkbook = xlrd.open_workbook(path)
            inputWorksheet = inputWorkbook.sheet_by_index(0)
            for row in range(0, self.row):
                for col in range(0, 3):
                    item = str(int(inputWorksheet.cell_value(row + 1, col)))
                    self.tableWidget.setItem(row, col, QTableWidgetItem(item))
                for col in range(3, 8):
                    item = str(inputWorksheet.cell_value(row + 1, col))
                    self.tableWidget.setItem(row, col, QTableWidgetItem(item))
