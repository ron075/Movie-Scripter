from __future__ import annotations

from PyQt6.QtGui import QCloseEvent, QMouseEvent
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *
import os
import math
from .util import *
from .custom_widgets import *

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .main_window import NodeEditor

class SettingsMenu(CustomQWidget):
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

        self.command_delay:float = 1.0
        self.model_refresh:float = 1.0
        self.viewer_refresh:float = 1.0

        self.allow_info_link:bool = True

        self.grid_size:int = 20
        self.grid_squares:int = 5
        self.grid_snap:bool = True

        self.update_model = False
        self.update_folder = False
        self.update_nodes = False
        self.update_run = False
        self.update_info = False
        self.update_grid = False
        self.update_viewer = False

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
        self.ModelRefresh = QNumEdit(0, decimals = 1, label = "Refresh Rate (sec)")
        self.ModelRefresh.Label.setFixedWidth(150)
        self.ModelRefresh.setText(self.model_refresh)
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
        self.model_layout.addLayout(self.ModelRefresh.widget_layout, 4, 0, 1, 2, Qt.AlignmentFlag.AlignCenter)
        self.model_layout.addWidget(self.ResetModel, 5, 0, 1, 2, Qt.AlignmentFlag.AlignCenter)

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
        self.NodeTransparencyBackground.Label.setFixedWidth(170)
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
        self.CommandDelay.setText(self.command_delay)
        self.ResetRun = QPushButton("Reset")
        self.ResetRun.clicked.connect(self.resetRun)
        self.run_layout.addLayout(self.CommandDelay.widget_layout, 0, 0, 1, 1, alignment=Qt.AlignmentFlag.AlignCenter)
        self.run_layout.addWidget(self.ResetRun, 1, 0, 1, 1, alignment=Qt.AlignmentFlag.AlignCenter)

        self.run_widget.setLayout(self.run_layout)
        self.run_widget.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        


        self.info_widget = QWidget()

        self.info_layout = QVBoxLayout()
        self.lInfoLink = QLabel("Enable Info Link")   
        self.lInfoLink.setMinimumWidth(100)
        self.lInfoLink.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.InfoLink = QSwitchControl(self.parent_window, checked=self.allow_info_link)
        self.InfoLink.stateChanged.connect(self.change_info)
        self.ResetInfo = QPushButton("Reset")
        self.ResetInfo.clicked.connect(self.resetInfoLink)
        self.info_layout.addWidget(self.lInfoLink, alignment= Qt.AlignmentFlag.AlignCenter)
        self.info_layout.addWidget(self.InfoLink, alignment=Qt.AlignmentFlag.AlignCenter)
        self.info_layout.addWidget(self.ResetInfo, alignment=Qt.AlignmentFlag.AlignCenter)

        self.info_widget.setLayout(self.info_layout)
        self.info_widget.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)



        self.grid_widget = QWidget()

        self.grid_layout = QVBoxLayout()
        self.GridSquares = QNumEdit(1, label = "Squares Count")
        self.GridSquares.Label.setFixedWidth(150)
        self.GridSquares.setText(self.grid_squares)
        self.GridSquares.Text.textChanged.connect(self.change_grid)
        self.GridSize = QNumEdit(1, label = "Square Size",)
        self.GridSize.Label.setFixedWidth(150)
        self.GridSize.setText(self.grid_size)
        self.GridSize.Text.textChanged.connect(self.change_grid)
        self.lGridSnap = QLabel("Enable Grid Snapping")   
        self.lGridSnap.setMinimumWidth(150)
        self.lGridSnap.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.GridSnap = QSwitchControl(self.parent_window, checked=self.allow_info_link)
        self.GridSnap.stateChanged.connect(self.change_grid)
        self.ResetGrid = QPushButton("Reset")
        self.ResetGrid.clicked.connect(self.resetGrid)
        self.grid_layout.addLayout(self.GridSquares.widget_layout)
        self.grid_layout.addLayout(self.GridSize.widget_layout)
        self.grid_layout.addWidget(self.lGridSnap, alignment= Qt.AlignmentFlag.AlignCenter)
        self.grid_layout.addWidget(self.GridSnap, alignment=Qt.AlignmentFlag.AlignCenter)
        self.grid_layout.addWidget(self.ResetGrid, alignment=Qt.AlignmentFlag.AlignCenter)

        self.grid_widget.setLayout(self.grid_layout)
        self.grid_widget.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)



        self.viewer_widget = QWidget()

        self.viewer_layout = QGridLayout()
        self.ViewerRefresh = QNumEdit(0, decimals = 1, label = "Refresh Rate (sec)")
        self.ViewerRefresh.Label.setFixedWidth(150)
        self.ViewerRefresh.setText(self.viewer_refresh)
        self.ResetViewer = QPushButton("Reset")
        self.ResetViewer.clicked.connect(self.resetViewer)
        self.viewer_layout.addLayout(self.ViewerRefresh.widget_layout, 0, 0, 1, 1, alignment=Qt.AlignmentFlag.AlignCenter)
        self.viewer_layout.addWidget(self.ResetViewer, 1, 0, 1, 1, alignment=Qt.AlignmentFlag.AlignCenter)

        self.viewer_widget.setLayout(self.viewer_layout)
        self.viewer_widget.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)



        self.settings_widgets["Model"] = self.model_widget
        self.settings_widgets["Folder"] = self.folder_widget
        self.settings_widgets["Nodes"] = self.nodes_widget
        self.settings_widgets["Run"] = self.run_widget
        self.settings_widgets["Info"] = self.info_widget
        self.settings_widgets["Grid"] = self.grid_widget
        self.settings_widgets["Viewer"] = self.viewer_widget

        for widget in self.settings_widgets.values():
            self.settings_scroll.setWidget(widget)
            self.settings_scroll.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignTop)
            changeCursor(widget.children())
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

    def mousePressEvent(self, event:QMouseEvent|None) -> None:
        self.moving=True
        self.offset = event.pos()

    def mouseMoveEvent(self, event:QMouseEvent|None) -> None:
        if self.moving:
            if event.buttons() == Qt.MouseButton.LeftButton:
                if self.mapToParent(event.pos() - self.offset).x() < 0:
                    move_x = 0
                elif self.mapToParent(event.pos() - self.offset).x() + self.width() > self.parent_window.width():
                    move_x = self.parent_window.width() - self.width()
                else:
                    move_x = self.mapToParent(event.pos() - self.offset).x()
                if self.mapToParent(event.pos() - self.offset).y() < 0:
                    move_y = 0
                elif self.mapToParent(event.pos() - self.offset).y() + self.height() > self.parent_window.height():
                    move_y = self.parent_window.height() - self.height()
                else:
                    move_y = self.mapToParent(event.pos() - self.offset).y()
                self.move(QPoint(move_x, move_y))
    
    def mouseReleaseEvent(self, event:QMouseEvent|None) -> None:
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
            self.move(QPoint(math.floor((self.parent_window.width() / 2) - (self.width() / 2)), math.floor((self.parent_window.height() / 2) - (self.height() / 2))))

    def changeOptions(self):
        self.settings_scroll.takeWidget()
        self.settings_scroll.setWidget(self.settings_widgets[self.options.currentItem().text()])

    def updateModelAtoms(self):
        if self.ModelResidues.isChecked():
            changeEnabled(self.ModelAtoms, True)
            changeEnabled(self.ModelHetero, True)
            changeEnabled(self.ModelWater, True)
        else:
            changeEnabled(self.ModelAtoms, True)
            changeEnabled(self.ModelHetero, True)
            changeEnabled(self.ModelWater, True)
            self.ModelAtoms.setChecked(False)
            self.ModelHetero.setChecked(False)
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

    def change_info(self):
        if self.allow_info_link != self.InfoLink.isChecked():
            self.update_info = True
        else:
            self.update_info = False

    def change_grid(self):
        if self.grid_squares != int(self.GridSquares.getText()):
            self.update_grid = True
        elif self.grid_size != int(self.GridSize.getText()):
            self.update_grid = True
        elif self.grid_snap != self.GridSnap.isChecked():
            self.update_grid = True
        else:
            self.update_grid = False

    def resetModel(self):
        self.ModelResidues.setChecked(True)
        self.ModelAtoms.setChecked(False)
        self.ModelHetero.setChecked(True)
        self.ModelWater.setChecked(True)
        self.model_refresh = 1.0
        
    def resetFolder(self):
        self.lSaveScriptFolder.setText("No Folder")
        self.lSaveLogFolder.setText("No Folder")

    def resetNodes(self):
        self.nodes_transparency_title = 100
        self.nodes_transparency_background = 90

    def resetRun(self):
        self.command_delay = 1.0

    def resetInfoLink(self):
        self.InfoLink.setChecked(True)

    def resetGrid(self):
        self.update_grid = False
        self.GridSquares.setText("5")
        self.GridSize.setText("20")
        self.GridSnap.setChecked(True)

    def resetViewer(self):
        self.viewer_refresh = 1.0

    def applySettings(self, cancel:bool=False):
        self.update_model = (self.model_hetero != self.ModelHetero.isChecked() or self.model_water != self.ModelWater.isChecked() or 
                             self.model_residues != self.ModelResidues.isChecked() or self.model_atoms != self.ModelAtoms.isChecked() or 
                             float(self.ModelRefresh.getText()) != self.model_refresh)
        self.update_folder = (self.save_script_folder != "No Folder" or self.save_log_folder != "No Folder")
        self.update_nodes = (int(self.NodeTransparencyTitle.getText()) != self.nodes_transparency_title or int(self.NodeTransparencyBackground.getText()) != self.nodes_transparency_background)
        self.update_run = (float(self.CommandDelay.getText()) != self.command_delay)
        self.update_info = (self.InfoLink.isChecked() != self.allow_info_link)
        self.update_grid = (int(self.GridSquares.getText()) != self.grid_squares or int(self.GridSize.getText()) != self.grid_size or
                            self.GridSnap.isChecked() != self.grid_snap)
        self.update_viewer = (float(self.ViewerRefresh.getText()) != self.viewer_refresh)

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
            self.model_refresh = float(self.ModelRefresh.getText())
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
            self.allow_info_link = self.InfoLink.isChecked()
            for node in self.parent_window.scene.nodes:
                node.set_info_link(self.allow_info_link)
            self.update_info = False
        if self.update_grid:
            self.grid_squares = int(self.GridSquares.getText())
            self.grid_size = int(self.GridSize.getText())
            self.grid_snap = self.GridSnap.isChecked()
            self.parent_window.scene.grScene.update()
            self.update_grid = False
        if self.update_viewer:
            self.viewer_refresh = float(self.ViewerRefresh.getText())
            self.update_viewer = False

        self.parent_window.settings_button.setProperty("State", "Closed")
        self.hide()

    def cancelSettings(self):
        self.applySettings(cancel=True)


class HelpMenu(QWidget):
    def __init__(self, session, nodeEditor:NodeEditor=None):
        
        super().__init__()

        self.nodeEditor = nodeEditor
        self.session = session  

        self.moving=False
        self.offset = 0

        self.help_width = 300
        self.help_height = 300
        self.edge_size = 10
        self._padding = 4

        self.help = Help(self.session, self)
        self.grHelp = QDMGraphicsHelpMenu(self.session, self)
        
        self.grHelp.setVisible(False)
        self.grHelp.setZValue(-100)

    def openHelp(self):
        if not self.grHelp.isVisible():
            self.grHelp.setVisible(True)
        view_width = self.nodeEditor.view.mapToScene(self.nodeEditor.view.pos()).x() + (self.nodeEditor.view.width() / 2)
        view_height = self.nodeEditor.view.mapToScene(self.nodeEditor.view.pos()).y() + (self.nodeEditor.view.height() / 2)

        self.grHelp.setPos(math.floor(view_width - (self.help_width / 2)), math.floor(view_height - (self.help_height / 2)))

    def closeHelp(self):
        if self.grHelp.isVisible():
            self.grHelp.setVisible(False)

    def changeStyle(self, style:Stylesheet):
        self.help.setStyleSheet(self.nodeEditor.stylesheets[style.name])
        self.grHelp._brush_background_color = QColor(self.nodeEditor.styles._node_brush_background[style.value])
        self.grHelp.updateBrushesAlpha()
        self.grHelp._pen_default.setColor(QColor(self.nodeEditor.styles._node_pen_default[(style.value-1)*-1])) 

class Help(CustomQWidget):
    def __init__(self, session, help_menu:HelpMenu=None, parent=None):
        super().__init__(parent)
        self.session = session
        self.help_menu = help_menu

        self.initUI()

    def initUI(self):
        self.main_layout = QVBoxLayout()
        self.main_layout.setSpacing(5)
        self.main_layout.setContentsMargins(10, 10, 10, 10)
        self.setLayout(self.main_layout)

        self.Tab = QTabWidget()    

        self.container1 = QTextEdit()   
        self.container1.setObjectName("info_text") 
        self.container1.setReadOnly(True) 
        self.container1_text = QTextDocument()
        self.container1_text.setHtml("Testing 1 Volumes")  
        self.container1.setDocument(self.container1_text)     
        self.Tab.insertTab(0, self.container1, "Segemention")

        self.container2 = QTextEdit()  
        self.container2.setObjectName("info_text") 
        self.container2.setReadOnly(True)  
        self.container2_text = QTextDocument()
        self.container2_text.setHtml("Testing 2 Models")  
        self.container2.setDocument(self.container2_text)    
        self.Tab.insertTab(1, self.container2, "Test2")

        self.container3 = QTextEdit() 
        self.container3.setObjectName("info_text") 
        self.container3.setReadOnly(True)  
        self.container3_text = QTextDocument()
        self.container3_text.setHtml("Testing 3 Marks")  
        self.container3.setDocument(self.container3_text)    
        self.Tab.insertTab(2, self.container3, "Test3")

        self.container4 = QTextEdit()  
        self.container4.setObjectName("info_text") 
        self.container4.setReadOnly(True)  
        self.container4_text = QTextDocument()
        self.container4_text.setHtml("Testing 4 Views")  
        self.container4.setDocument(self.container4_text)    
        self.Tab.insertTab(3, self.container4, "Test4")   

        self.main_layout.addWidget(self.Tab)

        self.Close = QPushButton()
        self.Close.setText("Close")
        self.Close.clicked.connect(self.help_menu.closeHelp)
        self.main_layout.addWidget(self.Close)

        changeCursor(self)
        
class QDMGraphicsHelpMenu(QGraphicsItem):
    def __init__(self, session, help_menu:HelpMenu=None):
        
        super().__init__()

        self.session = session  
        self.help = help_menu.help

        self.help_width = help_menu.help_width
        self.help_height = help_menu.help_height
        self.edge_size = help_menu.edge_size
        self._padding = help_menu._padding

        self._pen_default = QPen(QColor("#7F000000"))
        self._pen_default.setWidth(2)
        self._pen_default.setStyle(Qt.PenStyle.SolidLine)
        self._brush_background_color = QColor("#E3212121")
        self.updateBrushesAlpha()

        self.initUI()
        self.initHelp()

    def updateBrushesAlpha(self):
        #self._brush_title_color.setAlphaF(self.node.scene.parent.settings_menu.nodes_transparency_title / 100)
        #self._brush_background_color.setAlphaF(self.node.scene.parent.settings_menu.nodes_transparency_background / 100)
        self._brush_background = QBrush(self._brush_background_color)
        self.update()

    def boundingRect(self) -> QRectF:
        return QRectF(0, 0, self.help_width, self.help_height).normalized()        

    def initUI(self):
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsSelectable)
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsMovable)

    def paint(self, painter:QPainter, QStyleOptionGraphicsItem:QStyleOptionGraphicsItem, widget=None): 
        path = QPainterPath()
        path.setFillRule(Qt.FillRule.WindingFill)
        path.addRoundedRect(0, 0, self.help_width, self.help_height, self.edge_size, self.edge_size)
        painter.setPen(self._pen_default)
        painter.setBrush(self._brush_background)
        painter.drawPath(path.simplified())

    def initHelp(self):
        self.grHelp = QGraphicsProxyWidget(self)
        self.help.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.help.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.grHelp.setWidget(self.help)
        self.help.setGeometry(0, 0, self.help_width, self.help_height) 