from __future__ import annotations

from PyQt6.QtGui import QCloseEvent, QMouseEvent
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *
import os
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

        self.save_script_folder = ""
        self.save_log_folder = ""

        self.nodes_transparency_title:int = 100
        self.nodes_transparency_background:int = 90

        self.command_delay:float = 0.0

        self.update_normal_residues = False
        self.update_model = False
        self.update_folder = False
        self.update_nodes = False
        self.update_run = False

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
        self.ResetNormalResidue.clicked.connect(self.resetResidues)

        self.residues_layout.addWidget(self.lNormalResidues, 0, 0, 1, 2, Qt.AlignmentFlag.AlignCenter)
        self.residues_layout.addWidget(self.NormalResidue, 1, 0, 1, 1, Qt.AlignmentFlag.AlignCenter)
        self.residues_layout.addWidget(self.AddNormalResidue, 1, 1, 1, 1, Qt.AlignmentFlag.AlignCenter)
        self.residues_layout.addWidget(self.NormalResidueList, 2, 0, 4, 2, Qt.AlignmentFlag.AlignCenter)
        self.residues_layout.addWidget(self.RemoveNormalResidue, 6, 0, 1, 1, Qt.AlignmentFlag.AlignCenter)
        self.residues_layout.addWidget(self.ResetNormalResidue, 6, 1, 1, 1, Qt.AlignmentFlag.AlignCenter)

        self.residues_widget.setLayout(self.residues_layout)
        self.residues_widget.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)



        self.model_widget = QWidget()

        self.model_layout = QGridLayout()
        self.lModelResidues = QLabel("Residues")   
        self.lModelResidues.setMinimumWidth(100)
        self.ModelResidues = QSwitchControl(self.parent_window, checked=self.model_residues)
        self.lModelSpecialResidues = QLabel("Special\nResidues")        
        self.lModelSpecialResidues.setMinimumWidth(100)
        self.ModelSpecialResidues = QSwitchControl(self.parent_window, checked=self.model_special_residues)
        self.ModelResidues.stateChanged.connect(self.updateModelAtoms)
        self.lModelAtoms = QLabel("Atoms")   
        self.lModelAtoms.setMinimumWidth(100)
        self.ModelAtoms = QSwitchControl(self.parent_window, checked=self.model_atoms)
        self.ResetModel = QPushButton("Reset")
        self.ResetModel.clicked.connect(self.resetModel)
        self.model_layout.addWidget(self.lModelResidues, 0, 0, 1, 1, Qt.AlignmentFlag.AlignCenter)
        self.model_layout.addWidget(self.ModelResidues, 0, 1, 1, 1, Qt.AlignmentFlag.AlignCenter)
        self.model_layout.addWidget(self.lModelSpecialResidues, 1, 0, 1, 1, Qt.AlignmentFlag.AlignCenter)
        self.model_layout.addWidget(self.ModelSpecialResidues, 1, 1, 1, 1, Qt.AlignmentFlag.AlignCenter)
        self.model_layout.addWidget(self.lModelAtoms, 2, 0, 1, 1, Qt.AlignmentFlag.AlignCenter)
        self.model_layout.addWidget(self.ModelAtoms, 2, 1, 1, 1, Qt.AlignmentFlag.AlignCenter)
        self.model_layout.addWidget(self.ResetModel, 3, 0, 1, 1, Qt.AlignmentFlag.AlignCenter)

        self.model_widget.setLayout(self.model_layout)
        self.model_widget.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)



        self.folder_widget = QWidget()

        self.folder_layout = QGridLayout()
        self.SaveScriptFolder = QPushButton("Script Save Folder")
        self.SaveScriptFolder.clicked.connect(self.pickSaveScriptFolder)
        self.lSaveScriptFolder = QTextEdit()
        self.lSaveScriptFolder.setText("No Folder")
        self.lSaveScriptFolder.setFixedWidth(150)
        self.lSaveScriptFolder.setFixedHeight(75)
        self.lSaveScriptFolder.setReadOnly(True)
        self.SaveLogFolder = QPushButton("Log Save Folder")
        self.SaveLogFolder.clicked.connect(self.pickSaveLogFolder)
        self.lSaveLogFolder = QTextEdit()
        self.lSaveLogFolder.setText("No Folder")
        self.lSaveLogFolder.setFixedWidth(150)
        self.lSaveLogFolder.setFixedHeight(75)
        self.lSaveLogFolder.setReadOnly(True)
        self.ResetFolder = QPushButton("Reset")
        self.ResetFolder.clicked.connect(self.resetFolder)
        self.folder_layout.addWidget(self.SaveScriptFolder, 0, 0, 1, 1, alignment=Qt.AlignmentFlag.AlignCenter)
        self.folder_layout.addWidget(self.lSaveScriptFolder, 1, 0, 3, 1, alignment=Qt.AlignmentFlag.AlignCenter)
        self.folder_layout.addWidget(self.SaveLogFolder, 4, 0, 1, 1, alignment=Qt.AlignmentFlag.AlignCenter)
        self.folder_layout.addWidget(self.lSaveLogFolder, 5, 0, 3, 1, alignment=Qt.AlignmentFlag.AlignCenter)
        self.folder_layout.addWidget(self.ResetFolder, 8, 0, 1, 1, alignment=Qt.AlignmentFlag.AlignCenter)

        self.folder_widget.setLayout(self.folder_layout)
        self.folder_widget.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        


        self.nodes_widget = QWidget()

        self.nodes_layout = QGridLayout()
        self.NodeTransparencyTitle = QNumEdit(0, 100, label = "Title Transparency", addSlider = True)
        self.NodeTransparencyTitle.Label.setFixedWidth(150)
        self.NodeTransparencyTitle.setText(self.nodes_transparency_title)
        self.NodeTransparencyBackground = QNumEdit(0, 100, label = "Background Transparency", addSlider = True)
        self.NodeTransparencyBackground.Label.setFixedWidth(150)
        self.NodeTransparencyBackground.setText(self.nodes_transparency_background)
        self.ResetNodes = QPushButton("Reset")
        self.ResetNodes.clicked.connect(self.resetNodes)
        self.nodes_layout.addLayout(self.NodeTransparencyTitle.widget_layout, 0, 0, 1, 1, alignment=Qt.AlignmentFlag.AlignCenter)
        self.nodes_layout.addLayout(self.NodeTransparencyBackground.widget_layout, 1, 0, 1, 1, alignment=Qt.AlignmentFlag.AlignCenter)
        self.nodes_layout.addWidget(self.ResetNodes, 2, 0, 1, 1, alignment=Qt.AlignmentFlag.AlignCenter)

        self.nodes_widget.setLayout(self.nodes_layout)
        self.nodes_widget.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        


        self.run_widget = QWidget()

        self.run_layout = QGridLayout()
        self.CommandDelay = QNumEdit(0, decimals = 1, label = "Command Delay (sec)")
        self.CommandDelay.Label.setFixedWidth(150)
        self.ResetRun = QPushButton("Reset")
        self.ResetRun.clicked.connect(self.resetRun)
        self.run_layout.addLayout(self.CommandDelay.widget_layout, 0, 0, 1, 1, alignment=Qt.AlignmentFlag.AlignCenter)
        self.run_layout.addWidget(self.ResetRun, 1, 0, 1, 1, alignment=Qt.AlignmentFlag.AlignCenter)

        self.run_widget.setLayout(self.run_layout)
        self.run_widget.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        


        self.settings_widgets["Residues"] = self.residues_widget
        self.settings_widgets["Model"] = self.model_widget
        self.settings_widgets["Folder"] = self.folder_widget
        self.settings_widgets["Nodes"] = self.nodes_widget
        self.settings_widgets["Run"] = self.run_widget

        for widget in self.settings_widgets.values():
            self.settings_scroll.setWidget(widget)
            self.settings_scroll.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignTop)
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

            if os.path.exists(self.save_script_folder):
                self.lSaveScriptFolder.setText(self.save_script_folder)
            else:
                self.save_script_folder = ""
                self.lSaveScriptFolder.setText("No Folder")

            if os.path.exists(self.save_log_folder):
                self.lSaveLogFolder.setText(self.save_log_folder)
            else:
                self.save_log_folder = ""
                self.lSaveLogFolder.setText("No Folder")

            self.NodeTransparencyTitle.setText(self.nodes_transparency_title)
            self.NodeTransparencyBackground.setText(self.nodes_transparency_background)

            self.CommandDelay.setText(self.command_delay)

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

    def updateModelAtoms(self):
        if self.ModelResidues.isChecked():
            self.ModelSpecialResidues.setEnabled(True)
            self.ModelAtoms.setEnabled(True)
        else:
            self.ModelSpecialResidues.setEnabled(False)
            self.ModelSpecialResidues.setChecked(False)
            self.ModelAtoms.setEnabled(False)
            self.ModelAtoms.setChecked(False)

    def pickSaveScriptFolder(self):
        save_script_folder = str(QFileDialog.getExistingDirectory(self, "Select Save Folder"))
        if self.lSaveScriptFolder.toPlainText() != save_script_folder:
            if save_script_folder is not None:
                if save_script_folder == "":
                    self.lSaveScriptFolder.setText("No Folder")
                else:
                    self.lSaveScriptFolder.setText(save_script_folder)
            else:
                self.lSaveScriptFolder.setText("No Folder")
            self.update_folder = True
        

    def pickSaveLogFolder(self):
        save_log_folder = str(QFileDialog.getExistingDirectory(self, "Select Save Folder"))
        if self.lSaveLogFolder.toPlainText() != save_log_folder:
            if save_log_folder is not None:
                if save_log_folder == "":
                    self.lSaveLogFolder.setText("No Folder")
                else:
                    self.lSaveLogFolder.setText(save_log_folder)
            else:
                self.lSaveLogFolder.setText("No Folder")
            self.update_folder = True

    def resetResidues(self):
        if self.normal_residues != self.base_normal_residues:
            self.update_normal_residues = True
        self.settings_residue_list = list(self.base_normal_residues)
        self.NormalResidueList.clear()
        self.AddNormalResidue.setEnabled(False)
        self.RemoveNormalResidue.setEnabled(False)
        self.NormalResidueList.addItems(self.settings_residue_list)

    def resetModel(self):
        if not self.ModelSpecialResidues.isChecked():
            self.ModelSpecialResidues.setChecked(True)
        if not self.ModelResidues.isChecked():
            self.ModelResidues.setChecked(True)
        if self.ModelAtoms.isChecked():
            self.ModelAtoms.setChecked(False)
        self.update_model = (self.model_special_residues != self.ModelSpecialResidues.isChecked() or self.model_residues != self.ModelResidues.isChecked() or self.model_atoms != self.ModelAtoms.isChecked())
        
    def resetFolder(self):
        save_script_folder = "No Folder"
        if self.save_script_folder != save_script_folder:
            self.lSaveScriptFolder.setText("No Folder")
            self.update_folder = True
        save_log_folder = "No Folder"
        if self.save_log_folder != save_log_folder:
            self.lSaveLogFolder.setText("No Folder")
            self.update_folder = True

    def resetNodes(self):
        self.update_nodes = (int(self.NodeTransparencyTitle.getText()) != self.nodes_transparency_title or int(self.NodeTransparencyBackground.getText()) != self.nodes_transparency_background)

    def resetRun(self):
        self.update_run = (float(self.CommandDelay.getText()) != self.command_delay)

    def applySettings(self, cancel:bool=False):
        self.update_model = (self.model_special_residues != self.ModelSpecialResidues.isChecked() or self.model_residues != self.ModelResidues.isChecked() or self.model_atoms != self.ModelAtoms.isChecked())
        self.update_nodes = (int(self.NodeTransparencyTitle.getText()) != self.nodes_transparency_title or int(self.NodeTransparencyBackground.getText()) != self.nodes_transparency_background)
        self.update_run = (float(self.CommandDelay.getText()) != self.command_delay)

        if cancel:
            self.settings_residue_list = list(self.normal_residues)
            self.parent_window.settings_button.setProperty("State", "Closed")
            self.hide()
            return
        
        updates = False

        if self.update_normal_residues or self.update_model:
            updates = True
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
        if self.update_folder:
            updates = True
            self.save_script_folder = self.lSaveScriptFolder.toPlainText()
            self.save_log_folder = self.lSaveLogFolder.toPlainText()
            self.update_folder = False
        if self.update_nodes:
            updates = True
            self.nodes_transparency_title = int(self.NodeTransparencyTitle.getText())
            self.nodes_transparency_background = int(self.NodeTransparencyBackground.getText())
            for node in self.parent_window.scene.nodes:
                node.grNode.updateBrushesAlpha()
                for picker in node.picker_inputs:
                    picker.edge.start_socket.node.grNode.updateBrushesAlpha()
            self.update_nodes = False
        if self.update_run:
            updates = True
            self.command_delay = float(self.CommandDelay.getText())
            self.update_run = False

        if not updates:
            self.settings_residue_list = list(self.normal_residues)

        self.parent_window.settings_button.setProperty("State", "Closed")
        self.hide()

    def cancelSettings(self):
        self.applySettings(cancel=True)