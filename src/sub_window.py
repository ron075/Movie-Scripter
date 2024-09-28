from __future__ import annotations

from PyQt6.QtGui import QCloseEvent, QMouseEvent
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *
from .custom_widgets import *

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .main_window import NodeEditor

class SettingsMenu(QWidget):
    def __init__(self, session, parent:NodeEditor=None):
        
        super().__init__(parent)

        self.parent_window = parent
        self.session = session  
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)

        self.moving=False
        self.offset = 0

        self.settings_widgets = {}

        self.base_normal_residues = ["ALA", "CYS", "ASP", "GLU", "PHE", "GLY", "HIS", "ILE", "LYS", "LEU", "MET", "ASN", "PYL", "PRO", "GLN", "ARG", "SER", "THR", "SEC", "VAL", "TRP", "TYR"]
        self.base_normal_residues.sort()
        self.normal_residues = list(self.base_normal_residues)
        self.settings_residue_list = list(self.base_normal_residues)

        self.model_special_residues = True
        self.model_residues = True
        self.model_atoms = False

        self.update_normal_residues = False
        self.update_model = False

        self.initUI()

    def initUI(self):     
        self.settings_layout = QVBoxLayout()
        
        self.options_layout = QHBoxLayout()

        self.options = QListWidget()

        self.settings_scroll = QScrollArea()

        self.residues_widget = QWidget()

        self.residues_layout = QGridLayout()

        self.lNormalResidues = QLabel("Normal Residues")
        self.NormalResidue = QLineEdit()
        self.NormalResidue.setMaximumWidth(50)
        self.AddNormalResidue = QPushButton("Add")
        self.AddNormalResidue.setEnabled(False)
        self.NormalResidue.textChanged.connect(self.updateAddNormalResidue)
        self.AddNormalResidue.clicked.connect(self.addNormalResidueList)

        self.NormalResidueList = QListWidget()
        self.NormalResidueList.setObjectName("list")
        self.NormalResidueList.setMaximumWidth(100)
        self.NormalResidueList.setSortingEnabled(True)
        self.NormalResidueList.currentRowChanged.connect(self.updateRemoveNormalResidue)

        self.RemoveNormalResidue = QPushButton("Remove")
        self.RemoveNormalResidue.setEnabled(False)
        self.RemoveNormalResidue.clicked.connect(self.removeNormalResidueList)
        self.ResetNormalResidue = QPushButton("Reset")
        self.ResetNormalResidue.clicked.connect(self.resetNormalResidueList)

        self.residues_layout.addWidget(self.lNormalResidues, 0, 0, 1, 2, Qt.AlignmentFlag.AlignCenter)
        self.residues_layout.addWidget(self.NormalResidue, 1, 0, 1, 1, Qt.AlignmentFlag.AlignCenter)
        self.residues_layout.addWidget(self.AddNormalResidue, 1, 1, 1, 1, Qt.AlignmentFlag.AlignCenter)
        self.residues_layout.addWidget(self.NormalResidueList, 2, 0, 4, 2, Qt.AlignmentFlag.AlignCenter)
        self.residues_layout.addWidget(self.RemoveNormalResidue, 6, 0, 1, 1, Qt.AlignmentFlag.AlignCenter)
        self.residues_layout.addWidget(self.ResetNormalResidue, 6, 1, 1, 1, Qt.AlignmentFlag.AlignCenter)

        self.residues_widget.setLayout(self.residues_layout)



        self.model_widget = QWidget()

        self.model_layout = QGridLayout()
        self.lModelResidues = QLabel("Residues")
        self.ModelResidues = QSwitchControl(self.parent_window, checked=self.model_residues)
        self.lModelSpecialResidues = QLabel("Special Residues")
        self.ModelSpecialResidues = QSwitchControl(self.parent_window, checked=self.model_special_residues)
        self.ModelResidues.stateChanged.connect(self.updateModelAtoms)
        self.lModelAtoms = QLabel("Atoms")
        self.ModelAtoms = QSwitchControl(self.parent_window, checked=self.model_atoms)
        self.model_layout.addWidget(self.lModelResidues, 0, 0, 1, 1, Qt.AlignmentFlag.AlignCenter)
        self.model_layout.addWidget(self.ModelResidues, 0, 1, 1, 1, Qt.AlignmentFlag.AlignCenter)
        self.model_layout.addWidget(self.lModelSpecialResidues, 1, 0, 1, 1, Qt.AlignmentFlag.AlignCenter)
        self.model_layout.addWidget(self.ModelSpecialResidues, 1, 1, 1, 1, Qt.AlignmentFlag.AlignCenter)
        self.model_layout.addWidget(self.lModelAtoms, 2, 0, 1, 1, Qt.AlignmentFlag.AlignCenter)
        self.model_layout.addWidget(self.ModelAtoms, 2, 1, 1, 1, Qt.AlignmentFlag.AlignCenter)

        self.model_widget.setLayout(self.model_layout)



        self.test_widget2 = QWidget()

        self.test_layout2 = QGridLayout()
        self.ltest2 = QLabel("Test2")
        self.test_layout2.addWidget(self.ltest2, 0, 0, 1, 1, Qt.AlignmentFlag.AlignCenter)

        self.test_widget2.setLayout(self.test_layout2)



        self.settings_widgets["Residues"] = self.residues_widget
        self.settings_widgets["Model"] = self.model_widget
        self.settings_widgets["Test2"] = self.test_widget2

        for widget in self.settings_widgets.values():
            self.settings_scroll.setWidget(widget)
            self.settings_scroll.takeWidget()
            widget.setObjectName("settings")

        self.options.addItems(self.settings_widgets.keys())
        self.options.setCurrentRow(0)
        
        self.settings_scroll.setWidget(self.settings_widgets[self.options.currentItem().text()])
        self.settings_scroll.setSizePolicy(QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.Minimum)

        self.options_layout.addWidget(self.options)
        self.options_layout.addWidget(self.settings_scroll)
        self.options.currentRowChanged.connect(self.changeOptions)

        self.layoutV1H2 = QHBoxLayout()
        self.Apply = QPushButton("Apply")
        self.Apply.clicked.connect(self.applySettings)
        self.Cancel = QPushButton("Cancel")
        self.Cancel.clicked.connect(self.cancelSettings)
        self.layoutV1H2.addWidget(self.Apply)
        self.layoutV1H2.addWidget(self.Cancel)
        self.settings_layout.addLayout(self.options_layout)
        self.settings_layout.addLayout(self.layoutV1H2)
        self.settings_layout.setSizeConstraint(QLayout.SizeConstraint.SetMinimumSize)

        self.setLayout(self.settings_layout)
        
        self.hide()

    def mousePressEvent(self, event: QMouseEvent | None) -> None:
        self.moving=True
        self.offset = event.pos()

    def mouseMoveEvent(self, event: QMouseEvent | None) -> None:
        if self.moving:
            if event.buttons() == Qt.MouseButton.LeftButton:
                self.move(self.mapToParent(event.pos() - self.offset))
    
    def mouseReleaseEvent(self, event: QMouseEvent | None) -> None:
        self.moving=False
        self.offset = 0

    def openSettings(self):
        if self.parent_window.settings_button.property("State") == "Closed":
            self.NormalResidueList.clear()
            self.AddNormalResidue.setEnabled(False)
            self.RemoveNormalResidue.setEnabled(False)
            self.NormalResidueList.addItems(self.normal_residues)

            self.ModelSpecialResidues.setChecked(self.model_special_residues)
            self.ModelResidues.setChecked(self.model_residues)
            self.ModelAtoms.setChecked(self.model_atoms)

            self.parent_window.settings_button.setProperty("State", "Opened")

            self.show()

    def changeOptions(self):
        self.settings_scroll.takeWidget()
        self.settings_scroll.setWidget(self.settings_widgets[self.options.currentItem().text()])

    def updateAddNormalResidue(self, text:str):
        if len(text) == 3:
            if text.upper() not in self.normal_residues:
                self.AddNormalResidue.setEnabled(True)
            else:
                self.AddNormalResidue.setEnabled(False)
        else:
            self.AddNormalResidue.setEnabled(False)

    def updateRemoveNormalResidue(self, value):
        if value > -1:
            self.RemoveNormalResidue.setEnabled(True)
        else:
            self.RemoveNormalResidue.setEnabled(False)

    def addNormalResidueList(self):
        self.update_normal_residues = True
        self.NormalResidueList.addItem(self.NormalResidue.text().upper())
        self.settings_residue_list.append(self.NormalResidue.text().upper())
        self.settings_residue_list.sort()
        self.NormalResidue.clear()

    def removeNormalResidueList(self):
        self.update_normal_residues = True
        row = self.NormalResidueList.currentIndex().row()
        self.NormalResidueList.takeItem(row)
        del self.settings_residue_list[row]

    def resetNormalResidueList(self):
        if self.normal_residues != self.base_normal_residues:
            self.update_normal_residues = True
        self.settings_residue_list = list(self.base_normal_residues)
        self.NormalResidueList.clear()
        self.AddNormalResidue.setEnabled(False)
        self.RemoveNormalResidue.setEnabled(False)
        self.NormalResidueList.addItems(self.settings_residue_list)

    def updateModelAtoms(self):
        if self.ModelResidues.isChecked():
            self.ModelSpecialResidues.setEnabled(True)
            self.ModelAtoms.setEnabled(True)
        else:
            self.ModelSpecialResidues.setEnabled(False)
            self.ModelSpecialResidues.setChecked(False)
            self.ModelAtoms.setEnabled(False)
            self.ModelAtoms.setChecked(False)
            

    def applySettings(self, cancel:bool=False):
        self.update_model = (self.model_special_residues != self.ModelSpecialResidues.isChecked() or self.model_residues != self.ModelResidues.isChecked() or self.model_atoms != self.ModelAtoms.isChecked())
        if cancel:
            self.settings_residue_list = list(self.normal_residues)
        elif self.update_normal_residues or self.update_model:
            if self.update_normal_residues:
                self.normal_residues = list(self.settings_residue_list)
                self.update_normal_residues = False
            if self.update_model:
                self.model_special_residues = self.ModelSpecialResidues.isChecked()
                self.model_residues = self.ModelResidues.isChecked()
                self.model_atoms = self.ModelAtoms.isChecked()
                self.parent_window.reload_presets()
                self.update_model = False
            for picker in self.parent_window.pickers:
                picker.updateModels(self.parent_window.current_models)
        else:
            self.settings_residue_list = list(self.normal_residues)
        self.parent_window.settings_button.setProperty("State", "Closed")
        self.hide()

    def cancelSettings(self):
        self.applySettings(cancel=True)