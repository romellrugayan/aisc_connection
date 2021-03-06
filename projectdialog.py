from PyQt5.QtWidgets import QDialog
from PyQt5.QtGui import QIcon
from PyQt5.uic import loadUi


class ProjectDialog(QDialog):
    def __init__(self):
        super(ProjectDialog, self).__init__()
        loadUi('ui/projectdesc.ui', self)
        self.setWindowIcon(QIcon('resources/icons/conndesign.png'))
        self.project_desc = {}

    def setProjectDesc(self, project_desc):
        self.job_no_edit.setText(project_desc['job_no'])
        self.project_symbol_edit.setText(project_desc['project_symbol'])
        self.project_title_edit.setText(project_desc['project_title'])
        self.client_edit.setText(project_desc['client'])
        self.item_edit.setText(project_desc['item'])
        self.engineer_edit.setText(project_desc['designed_by'])
        self.rev_edit.setText(project_desc['rev'])

    def getProjectDesc(self):
        self.project_desc['job_no'] = self.job_no_edit.text()
        self.project_desc['project_symbol'] = self.project_symbol_edit.text()
        self.project_desc['project_title'] = self.project_title_edit.text()
        self.project_desc['client'] = self.client_edit.text()
        self.project_desc['item'] = self.item_edit.text()
        self.project_desc['designed_by'] = self.engineer_edit.text()
        self.project_desc['rev'] = self.rev_edit.text()
        return self.project_desc






