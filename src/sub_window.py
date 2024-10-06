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

        self.settings_widgets:dict[str,QWidget] = {}

        self.model_residues = True
        self.model_atoms = False
        self.model_hetero = True
        self.model_water = True

        self.save_script_folder = ""
        self.save_log_folder = ""

        self.nodes_transparency_title:int = 100
        self.nodes_transparency_background:int = 90

        self.command_delay:float = 0.0

        self.current_info_type:int = 0

        self.update_model = False
        self.update_folder = False
        self.update_nodes = False
        self.update_run = False
        self.update_info = False

        self.initUI()

    def initUI(self):     
        self.settings_layout = QVBoxLayout()
        
        self.options_layout = QHBoxLayout()

        self.options = QListWidget()

        self.settings_scroll = QScrollArea()

        self.model_widget = QWidget()

        self.model_layout = QGridLayout()
        self.lModelResidues = QLabel("Residues")   
        self.lModelResidues.setMinimumWidth(100)
        self.ModelResidues = QSwitchControl(self.parent_window, checked=self.model_residues)
        self.lModelAtoms = QLabel("Atoms")   
        self.lModelAtoms.setMinimumWidth(100)
        self.ModelAtoms = QSwitchControl(self.parent_window, checked=self.model_atoms)
        self.lModelHetero = QLabel("Hetero")   
        self.lModelHetero.setMinimumWidth(100)
        self.ModelHetero = QSwitchControl(self.parent_window, checked=self.model_hetero)
        self.lModelWater = QLabel("Water")   
        self.lModelWater.setMinimumWidth(100)
        self.ModelWater = QSwitchControl(self.parent_window, checked=self.model_water)
        self.ModelResidues.stateChanged.connect(self.updateModelAtoms)
        self.ResetModel = QPushButton("Reset")
        self.ResetModel.clicked.connect(self.resetModel)
        self.model_layout.addWidget(self.lModelResidues, 0, 0, 1, 1, Qt.AlignmentFlag.AlignCenter)
        self.model_layout.addWidget(self.ModelResidues, 0, 1, 1, 1, Qt.AlignmentFlag.AlignCenter)
        self.model_layout.addWidget(self.lModelAtoms, 1, 0, 1, 1, Qt.AlignmentFlag.AlignCenter)
        self.model_layout.addWidget(self.ModelAtoms, 1, 1, 1, 1, Qt.AlignmentFlag.AlignCenter)
        self.model_layout.addWidget(self.lModelHetero, 2, 0, 1, 1, Qt.AlignmentFlag.AlignCenter)
        self.model_layout.addWidget(self.ModelHetero, 2, 1, 1, 1, Qt.AlignmentFlag.AlignCenter)
        self.model_layout.addWidget(self.lModelWater, 3, 0, 1, 1, Qt.AlignmentFlag.AlignCenter)
        self.model_layout.addWidget(self.ModelWater, 3, 1, 1, 1, Qt.AlignmentFlag.AlignCenter)
        self.model_layout.addWidget(self.ResetModel, 4, 0, 1, 1, Qt.AlignmentFlag.AlignCenter)

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
        


        self.info_widget = QWidget()

        self.info_layout = QVBoxLayout()
        self.lInfoType = QLabel("Info type")   
        self.lInfoType.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.InfoType = QComboBox()
        self.InfoType.addItems(["Simple", "Formal"])
        self.InfoType.setCurrentIndex(self.current_info_type)
        self.InfoType.setMinimumWidth(100)
        self.InfoType.currentIndexChanged.connect(self.change_info)
        self.ResetModel = QPushButton("Reset")
        self.ResetModel.clicked.connect(self.resetInfoType)
        self.info_layout.addWidget(self.lInfoType, alignment= Qt.AlignmentFlag.AlignCenter)
        self.info_layout.addWidget(self.InfoType, alignment=Qt.AlignmentFlag.AlignCenter)
        self.info_layout.addWidget(self.ResetModel, alignment=Qt.AlignmentFlag.AlignCenter)

        self.info_widget.setLayout(self.info_layout)
        self.info_widget.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)



        self.settings_widgets["Model"] = self.model_widget
        self.settings_widgets["Folder"] = self.folder_widget
        self.settings_widgets["Nodes"] = self.nodes_widget
        self.settings_widgets["Run"] = self.run_widget
        self.settings_widgets["Info"] = self.info_widget

        for widget in self.settings_widgets.values():
            self.settings_scroll.setWidget(widget)
            self.settings_scroll.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignTop)
            self.settings_scroll.takeWidget()
            widget.setObjectName("settings")

        self.options.addItems(self.settings_widgets.keys())
        self.options.setCurrentRow(0)
        
        self.settings_scroll.setWidget(self.settings_widgets[self.options.currentItem().text()])
        self.settings_scroll.setSizePolicy(QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.Minimum) 
        self.settings_scroll.setMinimumWidth(200) 
        self.settings_scroll.setMinimumHeight(300)

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

            self.ModelResidues.setChecked(self.model_residues)
            self.ModelAtoms.setChecked(self.model_atoms)
            self.ModelHetero.setChecked(self.model_hetero)
            self.ModelWater.setChecked(self.model_water)

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

    def updateModelAtoms(self):
        if self.ModelResidues.isChecked():
            self.ModelAtoms.setEnabled(True)
            self.ModelHetero.setEnabled(True)
            self.ModelWater.setEnabled(True)
        else:
            self.ModelAtoms.setEnabled(False)
            self.ModelAtoms.setChecked(False)
            self.ModelHetero.setEnabled(False)
            self.ModelHetero.setChecked(False)
            self.ModelWater.setEnabled(False)
            self.ModelWater.setChecked(False)

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

    def change_info(self, index):
        if self.current_info_type != index:
            self.update_info = True

    def resetModel(self):
        if not self.ModelResidues.isChecked():
            self.ModelResidues.setChecked(True)
        if self.ModelAtoms.isChecked():
            self.ModelAtoms.setChecked(False)
        if not self.ModelHetero.isChecked():
            self.ModelHetero.setChecked(True)
        if not self.ModelWater.isChecked():
            self.ModelWater.setChecked(True)
        self.update_model = (self.model_hetero != self.ModelHetero.isChecked() or self.model_water != self.ModelWater.isChecked() or 
                             self.model_residues != self.ModelResidues.isChecked() or self.model_atoms != self.ModelAtoms.isChecked())
        
    def resetFolder(self):
        self.update_folder = False
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

    def resetInfoType(self):
        self.update_info = False
        self.InfoType.setCurrentIndex(0)
        if self.InfoType.currentIndex() != self.current_info_type:
            self.update_info = True

    def applySettings(self, cancel:bool=False):
        self.update_model = (self.model_hetero != self.ModelHetero.isChecked() or self.model_water != self.ModelWater.isChecked() or 
                             self.model_residues != self.ModelResidues.isChecked() or self.model_atoms != self.ModelAtoms.isChecked())
        self.update_nodes = (int(self.NodeTransparencyTitle.getText()) != self.nodes_transparency_title or int(self.NodeTransparencyBackground.getText()) != self.nodes_transparency_background)
        self.update_run = (float(self.CommandDelay.getText()) != self.command_delay)

        if cancel:
            self.parent_window.settings_button.setProperty("State", "Closed")
            self.hide()
            return

        if self.update_model:
            self.model_residues = self.ModelResidues.isChecked()
            self.model_atoms = self.ModelAtoms.isChecked()
            self.model_hetero = self.ModelHetero.isChecked()
            self.model_water = self.ModelWater.isChecked()
            self.parent_window.reload_presets()
            self.update_model = False
            for picker in self.parent_window.pickers:
                picker.updateModels(self.parent_window.current_models)
        if self.update_folder:
            self.save_script_folder = self.lSaveScriptFolder.toPlainText()
            self.save_log_folder = self.lSaveLogFolder.toPlainText()
            self.update_folder = False
        if self.update_nodes:
            self.nodes_transparency_title = int(self.NodeTransparencyTitle.getText())
            self.nodes_transparency_background = int(self.NodeTransparencyBackground.getText())
            for node in self.parent_window.scene.nodes:
                node.grNode.updateBrushesAlpha()
                for picker in node.picker_inputs:
                    picker.edge.start_socket.node.grNode.updateBrushesAlpha()
            self.update_nodes = False
        if self.update_run:
            self.command_delay = float(self.CommandDelay.getText())
            self.update_run = False
        if self.update_info:
            self.current_info_type = self.InfoType.currentIndex()
            for node in self.parent_window.scene.nodes:
                node.set_info(self.current_info_type)
            self.update_info = False

        self.parent_window.settings_button.setProperty("State", "Closed")
        self.hide()

    def cancelSettings(self):
        self.applySettings(cancel=True)