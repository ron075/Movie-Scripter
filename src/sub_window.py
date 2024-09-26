from __future__ import annotations

from PyQt6.QtGui import QCloseEvent, QMouseEvent
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .main_window import NodeEditor

class SettingsMenu(QWidget):
    def __init__(self, session, parent:NodeEditor=None):
        
        super().__init__(parent)

        self.parent_window = parent
        self.session = session  
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)

        self.settings_widgets = {}

        self.base_normal_residues = ["ALA", "CYS", "ASP", "GLU", "PHE", "GLY", "HIS", "ILE", "LYS", "LEU", "MET", "ASN", "PYL", "PRO", "GLN", "ARG", "SER", "THR", "SEC", "VAL", "TRP", "TYR"]
        self.base_normal_residues.sort()
        self.normal_residues = list(self.base_normal_residues)
        self.settings_residue_list = list(self.base_normal_residues)

        self.update_residues = False

        self.initUI()

    def initUI(self):     
        self.settings_layout = QVBoxLayout()
        
        self.options_layout = QHBoxLayout()

        self.options = QListWidget()

        self.settings_scroll = QScrollArea()

        self.residues_widget = QWidget()

        self.residues_layout = QGridLayout()

        self.lResidues = QLabel("Normal Residues")
        self.Residue = QLineEdit()
        self.Residue.setMaximumWidth(50)
        self.AddResidue = QPushButton("Add")
        self.AddResidue.setEnabled(False)
        self.Residue.textChanged.connect(self.updateAddResidue)
        self.AddResidue.clicked.connect(self.addResidueList)

        self.ResidueList = QListWidget()
        self.ResidueList.setObjectName("list")
        self.ResidueList.setMaximumWidth(100)
        self.ResidueList.setSortingEnabled(True)
        self.ResidueList.currentRowChanged.connect(self.updateRemoveResidue)

        self.RemoveResidue = QPushButton("Remove")
        self.RemoveResidue.setEnabled(False)
        self.RemoveResidue.clicked.connect(self.removeResidueList)
        self.ResetResidue = QPushButton("Reset")
        self.ResetResidue.clicked.connect(self.resetResidueList)

        self.residues_layout.addWidget(self.lResidues, 0, 0, 1, 2, Qt.AlignmentFlag.AlignCenter)
        self.residues_layout.addWidget(self.Residue, 1, 0, 1, 1, Qt.AlignmentFlag.AlignCenter)
        self.residues_layout.addWidget(self.AddResidue, 1, 1, 1, 1, Qt.AlignmentFlag.AlignCenter)
        self.residues_layout.addWidget(self.ResidueList, 2, 0, 4, 2, Qt.AlignmentFlag.AlignCenter)
        self.residues_layout.addWidget(self.RemoveResidue, 6, 0, 1, 1, Qt.AlignmentFlag.AlignCenter)
        self.residues_layout.addWidget(self.ResetResidue, 6, 1, 1, 1, Qt.AlignmentFlag.AlignCenter)

        self.residues_widget.setLayout(self.residues_layout)



        self.test_widget = QWidget()

        self.test_layout = QGridLayout()
        self.ltest = QLabel("Test")
        self.test_layout.addWidget(self.ltest, 0, 0, 1, 1, Qt.AlignmentFlag.AlignCenter)

        self.test_widget.setLayout(self.test_layout)



        self.test_widget2 = QWidget()

        self.test_layout2 = QGridLayout()
        self.ltest2 = QLabel("Test2")
        self.test_layout2.addWidget(self.ltest2, 0, 0, 1, 1, Qt.AlignmentFlag.AlignCenter)

        self.test_widget2.setLayout(self.test_layout2)



        self.settings_widgets["Residues"] = self.residues_widget
        self.settings_widgets["Test"] = self.test_widget
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
        self.offset = event.pos()

    def mouseMoveEvent(self, event: QMouseEvent | None) -> None:
        if event.buttons() == Qt.MouseButton.LeftButton:
            self.move(self.mapToParent(event.pos() - self.offset))
    
    def mouseReleaseEvent(self, event: QMouseEvent | None) -> None:
        self.offset = 0

    def openSettings(self):
        if self.parent_window.settings_button.property("State") == "Closed":
            self.ResidueList.clear()
            self.AddResidue.setEnabled(False)
            self.RemoveResidue.setEnabled(False)
            self.ResidueList.addItems(self.normal_residues)
            self.parent_window.settings_button.setProperty("State", "Opened")
            self.show()

    def changeOptions(self):
        self.settings_scroll.takeWidget()
        self.settings_scroll.setWidget(self.settings_widgets[self.options.currentItem().text()])

    def updateAddResidue(self, text:str):
        if len(text) == 3:
            if text.upper() not in self.normal_residues:
                self.AddResidue.setEnabled(True)
            else:
                self.AddResidue.setEnabled(False)
        else:
            self.AddResidue.setEnabled(False)

    def updateRemoveResidue(self, value):
        if value > -1:
            self.RemoveResidue.setEnabled(True)
        else:
            self.RemoveResidue.setEnabled(False)

    def addResidueList(self):
        self.update_residues = True
        self.ResidueList.addItem(self.Residue.text().upper())
        self.settings_residue_list.append(self.Residue.text().upper())
        self.settings_residue_list.sort()
        self.Residue.clear()

    def removeResidueList(self):
        self.update_residues = True
        row = self.ResidueList.currentIndex().row()
        self.ResidueList.takeItem(row)
        del self.settings_residue_list[row]

    def resetResidueList(self):
        if self.normal_residues != self.base_normal_residues:
            self.update_residues = True
        self.settings_residue_list = list(self.base_normal_residues)
        self.ResidueList.clear()
        self.AddResidue.setEnabled(False)
        self.RemoveResidue.setEnabled(False)
        self.ResidueList.addItems(self.settings_residue_list)

    def applySettings(self):
        if self.update_residues:
            self.update_residues = False
            self.normal_residues = list(self.settings_residue_list)
            for picker in self.parent_window.pickers:
                picker.updateModels(self.parent_window.current_models)
        else:
            self.settings_residue_list = list(self.normal_residues)
        self.parent_window.settings_button.setProperty("State", "Closed")
        self.hide()

    def cancelSettings(self):
        self.settings_residue_list = list(self.normal_residues)
        self.parent_window.settings_button.setProperty("State", "Closed")
        self.hide()