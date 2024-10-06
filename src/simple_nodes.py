from __future__ import annotations

from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtGui import *
from sys import platform
from .custom_widgets import *    
from .enum_classes import * 
from .node_base import * 
from chimerax.core import commands
from chimerax.atomic import structure, all_structures, ChainArg

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .node import Node
    from .graphics_scene import Scene
                
class SimpleNodeStart(NodeBase):
    def __init__(self, session, summary:SimpleNodeSummary, title:str="", parent=None):
        super().__init__(session, summary, title, simple_node=True, parent=parent)

        self.initUI()

    def initUI(self):

        self.BackgroundColorPicked = QColor("#FFFFFF")
        self.main_layout = QVBoxLayout()
        self.main_layout.setSpacing(5)
        self.main_layout.setContentsMargins(10, 10, 10, 10)
        self.setLayout(self.main_layout)

        self.layoutH1 = QHBoxLayout()
        self.lRecord = QLabel("Record Movie")
        self.Record = QSwitchControl(self.summary.node.scene.parent)
        self.summary.node.scene.parent.switches.append(self.Record)
        self.layoutH1.addWidget(self.lRecord)
        self.layoutH1.addWidget(self.Record, alignment=Qt.AlignmentFlag.AlignLeft, stretch=1)

        self.layoutH2 = QHBoxLayout()
        self.lResolution = QLabel("Resolution")
        self.Resolution = QComboBox()
        self.Resolution.addItems(["1280p", "720p", "480p", "360p", "Custom"])
        self.Resolution.currentIndexChanged.connect(self.updateResolution)
        self.layoutH2.addWidget(self.lResolution)
        self.layoutH2.addWidget(self.Resolution)

        self.Height = QNumEdit(min=0, max=2160, step=1, decimals=0, addSlider=True, label="Height")
        self.Height.setText("1024")
        self.Height.setEnabled(False)

        self.Width = QNumEdit(min=0, max=4096, step=1, decimals=0, addSlider=True, label="Height")
        self.Width.setText("1280")
        self.Width.setEnabled(False)

        self.layoutH3 = QHBoxLayout()
        self.BackgroundColor = QPushButton("Change Background\nColor") 
        self.BackgroundColor.setFixedWidth(150)  
        self.BackgroundColor.setFixedHeight(40)   
        self.BackgroundColor.clicked.connect(self.changeBackgroundColor)
        self.ColorLabel = QLabel()
        self.ColorLabel.setFixedWidth(50)   
        self.ColorLabel.setFixedHeight(50)    
        self.ColorLabel.setStyleSheet("QLabel { border: 1px solid black }")
        self.ColorDialog = QColorDialog()
        self.layoutH3.addWidget(self.BackgroundColor)
        self.layoutH3.addWidget(self.ColorLabel)

        self.layoutH4 = QHBoxLayout()
        self.Run = QPushButton("Run")
        self.Run.setFixedWidth(50)
        self.Run.clicked.connect(self.startRunCommand)
        self.RunChain = QPushButton("Run Chain")
        self.RunChain.setFixedWidth(75)
        self.RunChain.clicked.connect(self.runCommandChain)
        self.layoutH4.addWidget(self.Run)
        self.layoutH4.addWidget(self.RunChain)

        self.main_layout.addLayout(self.layoutH1)
        self.main_layout.addLayout(self.layoutH2)
        self.main_layout.addLayout(self.Height.widget_layout)
        self.main_layout.addLayout(self.Width.widget_layout)
        self.main_layout.addLayout(self.layoutH3)
        self.main_layout.addLayout(self.layoutH4)

    def updateRun(self, chain_update:bool=False):
        pass

    def updateTab(self, current_type:int):
        pass

    def updateCommand(self) -> list[str]:
        super().updateCommand()

        if self.Record.isChecked():
            self.start_script_string += f"movie reset<br>"
            self.start_script_string += f"<br>"
            self.script_string += f"movie record;<br>"
            self.script_string += f"<br>"
        else:
            self.start_script_string += f"movie reset<br>"
            self.start_script_string += f"<br>"

        self.script_string += f"windowsize {int(self.Width.getText())} {int(self.Height.getText())}<br>"
        self.script_string += f"set bgColor {self.BackgroundColorPicked.name()}<br>"
        self.script_string += f"<br>"

        return [self.start_script_string, self.script_string, self.end_script_string]
    
    def updateResolution(self):
        if self.Resolution.currentText() == "1280p":
            self.Height.setText("1024")
            self.Width.setText("1280")
            self.Height.setEnabled(False)
            self.Width.setEnabled(False)
        elif self.Resolution.currentText() == "720p":
            self.Height.setText("720")
            self.Width.setText("1280")
            self.Height.setEnabled(False)
            self.Width.setEnabled(False)
        elif self.Resolution.currentText() == "480p":
            self.Height.setText("480")
            self.Width.setText("640")
            self.Height.setEnabled(False)
            self.Width.setEnabled(False)
        elif self.Resolution.currentText() == "360p":
            self.Height.setText("360")
            self.Width.setText("640")
            self.Height.setEnabled(False)
            self.Width.setEnabled(False)
        elif self.Resolution.currentText() == "Custom":
            self.Height.setEnabled(True)
            self.Width.setEnabled(True)

    def changeBackgroundColor(self):
        self.BackgroundColorPicked = self.ColorDialog.getColor()
        self.ColorLabel.setStyleSheet(f"QLabel {{ background-color : rgb({self.BackgroundColorPicked.getRgb()[0]},{self.BackgroundColorPicked.getRgb()[1]},{self.BackgroundColorPicked.getRgb()[2]}); border: 1px solid black}}")
    

class SimpleNodePicker(NodeBase):
    def __init__(self, session, scene:Scene, summary:SimpleNodeSummary, all_views:bool, title:str="", selector_type:NodePickerType=NodePickerType.ModelPicker, parent=None):

        self.selector_type = selector_type

        if self.selector_type == NodePickerType.ModelPicker:
            title = "Model Picker"
        elif self.selector_type == NodePickerType.ColorPicker:
            title = "Color Picker"
        elif self.selector_type == NodePickerType.CenterPicker:
            title = "Center Picker"
        elif self.selector_type == NodePickerType.ViewPicker:
            title = "View Picker"
        elif self.selector_type == NodePickerType.FlyPicker:
            title = "Fly Picker"
        elif self.selector_type == NodePickerType.DeletePicker:
            title = "Delete Picker"
        elif self.selector_type == NodePickerType.SplitPicker:
            title = "Split Picker"
            
        super().__init__(session, summary, title, simple_node=True, parent=parent)

        self.scene = scene
        self.all_views = all_views

        self.initUI()

    def initUI(self):
        self.main_layout = QVBoxLayout()
        self.main_layout.setSpacing(5)
        self.main_layout.setContentsMargins(10, 10, 10, 10)
        self.setLayout(self.main_layout)

        self.Molecule = QTreeViewSelector(self.session, self.scene, self.summary.node, self.all_views, self.selector_type)
        self.scene.parent.pickers.append(self.Molecule)

        self.main_layout.addLayout(self.Molecule.widget_layout)

    def updateRun(self, chain_update:bool=False):
        pass

    def updateTab(self, current_type:int):
        pass
    
class SimpleNodeColorPalette(NodeBase):
    def __init__(self, session, summary:SimpleNodeSummary, title:str="", colormap_height:int=50, parent=None):
        super().__init__(session, summary, title, simple_node=True, parent=parent)

        self.colormap_height = colormap_height
        
        self.current_index = -1

        self.group_colors = []
        
        self.initUI()

    def initUI(self):
        self.main_layout = QVBoxLayout()
        self.setLayout(self.main_layout)
        self.main_layout.setContentsMargins(10, 10, 10, 10)
        self.main_layout.addSpacing(0)

        self.layoutH1 = QHBoxLayout()
        self.lColor = QLabel("Color")
        self.lColor.setWordWrap(True)
        self.Color = QComboBox()
        self.Color.addItems(["By Hetero", "From Palette"])
        self.color_list = ["byhetero", None]
        self.lCustomColor = QLabel("Color Palette")
        self.lCustomColor.setWordWrap(True)
        self.CustomColor = QComboBox()    
        self.CustomColor.setCurrentIndex(1)
        self.layoutH1.addWidget(self.lColor, alignment = Qt.AlignmentFlag.AlignCenter)
        self.layoutH1.addWidget(self.Color, alignment = Qt.AlignmentFlag.AlignCenter)
        self.layoutH1.addWidget(self.lCustomColor, alignment = Qt.AlignmentFlag.AlignCenter)
        self.layoutH1.addWidget(self.CustomColor, alignment = Qt.AlignmentFlag.AlignCenter)

        self.ColorMap = QColorMap(self.colormap_height)
        self.CustomColor.addItems([rangeName for rangeName in self.ColorMap.colorRangeLibrary.keys() if self.ColorMap.colorRangeLibrary[rangeName][0] == ColorRangeType.Simple])    
        self.ColorMap.updateColormap(self.CustomColor.currentText())
        self.CustomColor.currentIndexChanged.connect(self.updateColorMap)

        self.layoutH3 = QHBoxLayout()
        self.Group = QComboBox()
        self.Group.currentIndexChanged.connect(self.groupChange)
        self.Group.setEnabled(False)  
        self.layoutH3.addWidget(self.Group, alignment=Qt.AlignmentFlag.AlignCenter)  

        self.Color.currentIndexChanged.connect(self.switchColors)
        self.CustomColor.currentIndexChanged.connect(self.switchColors)

        self.layoutH4 = QHBoxLayout()
        self.GroupColor = QPushButton("Change Color") 
        self.GroupColor.setFixedWidth(100)   
        self.GroupColor.clicked.connect(self.changeGroupColor)
        self.GroupColor.setEnabled(False)
        self.ColorLabel = QLabel()
        self.ColorLabel.setFixedWidth(50)   
        self.ColorLabel.setFixedHeight(50)    
        self.ColorLabel.setStyleSheet("QLabel { border: 1px solid black }")
        self.ColorDialog = QColorDialog()
        self.layoutH4.addWidget(self.GroupColor)
        self.layoutH4.addWidget(self.ColorLabel)

        self.layoutH5 = QHBoxLayout()
        self.Delete = QPushButton("Delete")
        self.Delete.setFixedWidth(60)
        self.Delete.clicked.connect(self.deleteNode)
        self.Run = QPushButton("Run")
        self.Run.setFixedWidth(50)
        self.Run.setEnabled(False)
        self.Run.clicked.connect(self.startRunCommand)
        self.RunChain = QPushButton("Run Chain")
        self.RunChain.setFixedWidth(75)
        self.RunChain.setEnabled(False)
        self.RunChain.clicked.connect(self.runCommandChain)
        self.layoutH5.addWidget(self.Delete)
        self.layoutH5.addWidget(self.Run)
        self.layoutH5.addWidget(self.RunChain)

        self.main_layout.addLayout(self.layoutH1)
        self.main_layout.addLayout(self.ColorMap.widget_layout)
        self.main_layout.addSpacerItem(QSpacerItem(1,10))
        self.main_layout.addLayout(self.layoutH3)
        self.main_layout.addLayout(self.layoutH4)
        self.main_layout.addLayout(self.layoutH5)

    def updateRun(self, chain_update:bool=False):
        current_run = self.Run.isEnabled()
        if self.summary.picker_color_groups != []:
            self.Run.setEnabled(True)
        else:            
            self.ColorLabel.setStyleSheet("QLabel { background-color : transparent; border: 1px solid black}")
            self.Group.setCurrentText("")
            self.Run.setEnabled(False)
        if current_run != self.Run.isEnabled():
            if not chain_update:
                self.summary.findLastNode()

    def updateTab(self, current_type:int):
        pass
    
    def updateCommand(self) -> list[str]:
        super().updateCommand()

        if self.Run.isEnabled():
            for i, group in enumerate(self.summary.picker_color_groups):
                if self.Color.currentText() == "Partial Random" or self.Color.currentText() == "From Palette":
                    color = f"{self.group_colors[i].name()}"
                else:
                    color_type = "".join(self.group_colors[i].split(" ")).lower()
                    color = f"{color_type}"

                objects = "".join(group)
                if objects == "All":
                    objects = f"<i>'{objects.lower()}'</i>"
                else:
                    objects = f"<i>'{objects}'</i>"

                self.script_string += f"color {objects} {color}<br>"
            self.script_string += f"<br>"

        return [self.start_script_string, self.script_string, self.end_script_string]


    def updateUsedColors(self):
        self.summary.picker_color_groups = self.summary.picker_color_groups
            
    def generateGroups(self):
        self.Group.currentIndexChanged.disconnect(self.groupChange)
        self.Group.clear()
        for i, group in enumerate(self.summary.picker_color_groups):
            self.Group.addItem(f"Group {i + 1}")
        self.current_index = self.Group.currentIndex()
        self.Group.currentIndexChanged.connect(self.groupChange)

    def generateColors(self):
        if self.summary.picker_color_groups != []:
            if self.Color.currentText() == "From Palette":
                self.Group.setEnabled(True)
                self.GroupColor.setEnabled(True)
                self.group_colors = self.ColorMap.get_colors(self.CustomColor.currentText(), len(self.summary.picker_color_groups), False)
            else:
                self.Group.setEnabled(False)
                self.GroupColor.setEnabled(False)
                self.group_colors = [self.Color.currentText()] * len(self.summary.picker_color_groups)

    def addGroup(self):
        self.updateUsedColors()
        self.generateGroups()
        self.generateColors()
        self.switchGroup()

    def addGroups(self):
        self.updateUsedColors()
        self.generateGroups()
        self.generateColors()
        self.switchGroup()

    def removeGroup(self, row_indexes):
        self.updateUsedColors()
        self.generateGroups()
        self.generateColors()
        self.switchGroup()

    def resetGroups(self):
        self.updateUsedColors()
        self.generateGroups()
        self.switchGroup()
  
    def switchGroup(self):
        self.current_index = self.Group.currentIndex()
        if self.current_index > -1:
            if self.Color.currentText() == "Partial Random" or self.Color.currentText() == "From Palette":
                self.ColorLabel.setStyleSheet(f"QLabel {{ background-color : rgb({self.group_colors[self.current_index].getRgb()[0]},{self.group_colors[self.current_index].getRgb()[1]},{self.group_colors[self.current_index].getRgb()[2]}); border: 1px solid black}}")
            else:            
                self.ColorLabel.setStyleSheet("QLabel { background-color : rgb(0,0,0); border: 1px solid black}")
        else:
            self.ColorLabel.setStyleSheet("QLabel { background-color : transparent; border: 1px solid black}")

    def switchColors(self):
        self.generateColors()
        self.switchGroup()
    
    def groupChange(self):
        self.switchGroup()

    def changeGroupColor(self):
        color = self.ColorDialog.getColor()
        self.group_colors[self.Group.currentIndex()] = color
        self.ColorLabel.setStyleSheet(f"QLabel {{ background-color : rgb({self.group_colors[self.Group.currentIndex()].getRgb()[0]},{self.group_colors[self.Group.currentIndex()].getRgb()[1]},{self.group_colors[self.Group.currentIndex()].getRgb()[2]}); border: 1px solid black}}")
    
    def updateColorMap(self):
        self.ColorMap.updateColormap(self.CustomColor.currentText())

class SimpleNodeTransparency(NodeBase):
    def __init__(self, session, summary:SimpleNodeSummary, title:str="", parent=None):
        super().__init__(session, summary, title, simple_node=True, parent=parent)

        self.initUI()

    def initUI(self):
        self.main_layout = QVBoxLayout()
        self.main_layout.setSpacing(5)
        self.main_layout.setContentsMargins(10, 10, 10, 10)
        self.setLayout(self.main_layout)

        self.Surfaces = QNumEdit(min=0, max=100, step=1, decimals=0, label="Surfaces", addSlider=True)
        self.Surfaces.setText("0")

        self.Cartoons = QNumEdit(min=0, max=100, step=1, decimals=0, label="Cartoons", addSlider=True)
        self.Cartoons.setText("0")

        self.Atoms = QNumEdit(min=0, max=100, step=1, decimals=0, label="Atoms", addSlider=True)
        self.Atoms.setText("0")
        self.Atoms.Slider.sliderReleased.connect(self.updateAtomStyle)
        self.Atoms.Text.textChanged.connect(self.updateAtomStyle)
        self.Atoms.Minus.clicked.connect(self.updateAtomStyle)
        self.Atoms.Plus.clicked.connect(self.updateAtomStyle)

        self.layoutH1 = QHBoxLayout()
        self.lAtomsStyle = QLabel("Atoms Style")
        self.AtomsStyle = QComboBox()
        self.AtomsStyle.addItems(["Stick", "Sphere", "Ball"])
        self.AtomsStyle.setCurrentIndex(0)
        self.layoutH1.addWidget(self.lAtomsStyle)
        self.layoutH1.addWidget(self.AtomsStyle, stretch=1, alignment=Qt.AlignmentFlag.AlignLeft)

        self.layoutH2 = QHBoxLayout()
        self.Delete = QPushButton("Delete")
        self.Delete.setFixedWidth(60)
        self.Delete.clicked.connect(self.deleteNode) 
        self.Run = QPushButton("Run")
        self.Run.setFixedWidth(50)
        self.Run.setEnabled(False)
        self.Run.clicked.connect(self.startRunCommand)
        self.RunChain = QPushButton("Run Chain")
        self.RunChain.setFixedWidth(75)
        self.RunChain.setEnabled(False)
        self.RunChain.clicked.connect(self.runCommandChain)
        self.layoutH2.addWidget(self.Delete)
        self.layoutH2.addWidget(self.Run)
        self.layoutH2.addWidget(self.RunChain)

        self.main_layout.addLayout(self.Surfaces.widget_layout)
        self.main_layout.addLayout(self.Cartoons.widget_layout)
        self.main_layout.addLayout(self.Atoms.widget_layout)
        self.main_layout.addLayout(self.layoutH1)
        self.main_layout.addLayout(self.layoutH2)

    def updateRun(self, chain_update:bool=False):
        current_run = self.Run.isEnabled()
        if self.summary.picker_model != []:
            self.Run.setEnabled(True)
        else:
            self.Run.setEnabled(False)
        if current_run != self.Run.isEnabled():
            if not chain_update:
                self.summary.findLastNode()

    def updateTab(self, current_type:int):
        pass
    
    def updateCommand(self) -> list[str]:
        super().updateCommand()

        if self.Run.isEnabled():
            objects = "".join(self.summary.picker_model)
            if objects == "All":
                objects = f"<i>'{objects.lower()}'</i>"
            else:
                objects = f"<i>'{objects}'</i>"

            if int(self.Surfaces.getText()) >= 100 and int(self.Cartoons.getText()) >= 100 and int(self.Atoms.getText()) >= 100:
                self.script_string += f"hide <i>'{objects}'</i> target scabp<br>"
            else:
                if int(self.Surfaces.getText()) < 100:
                    self.script_string += f"show <i>'{objects}'</i> target s<br>"
                    self.script_string += f"transparency <i>'{objects}'</i> {self.Surfaces.getText()} target s<br>"
                else:
                    self.script_string += f"hide <i>'{objects}'</i> target s<br>"
                if int(self.Cartoons.getText()) < 100:
                    self.script_string += f"show <i>'{objects}'</i> target c<br>"
                    self.script_string += f"transparency <i>'{objects}'</i> {self.Cartoons.getText()} target c<br>"
                else:
                    self.script_string += f"hide <i>'{objects}'</i> target c<br>"
                if int(self.Atoms.getText()) < 100:
                    self.script_string += f"show <i>'{objects}'</i> target ab<br>"
                    self.script_string += f"style <i>'{objects}'</i> {self.AtomsStyle.currentText().lower()}<br>"
                    self.script_string += f"transparency <i>'{objects}'</i> {self.Atoms.getText()}  target ab<br>"
                else:
                    self.script_string += f"hide <i>'{objects}'</i>  target ab<br>"
                    
            self.script_string += f"<br>"
        
        return [self.start_script_string, self.script_string, self.end_script_string]    

    def updateAtomStyle(self):
        if int(self.Atoms.getText()) >= 100:
            self.AtomsStyle.setEnabled(False)
        else:
            self.AtomsStyle.setEnabled(True)

class SimpleNodeRotation(NodeBase):
    def __init__(self, session, summary:SimpleNodeSummary, title:str="", parent=None):
        super().__init__(session, summary, title, simple_node=True, parent=parent)

        self.initUI()

    def initUI(self):
        self.main_layout = QVBoxLayout()
        self.main_layout.setSpacing(5)
        self.main_layout.setContentsMargins(10, 10, 10, 10)
        self.setLayout(self.main_layout)

        self.layoutH1 = QHBoxLayout()
        self.lAxis = QLabel("Axis")
        self.Axis = QComboBox()
        self.Axis.addItems(["X", "Y", "Z"])
        self.Axis.setCurrentIndex(0)
        self.layoutH1.addWidget(self.lAxis)     
        self.layoutH1.addWidget(self.Axis, alignment=Qt.AlignmentFlag.AlignLeft)

        self.Angle = QNumEdit(min=0, max=360, step=1, decimals=1, addSlider=True, label="Angle")
        self.Angle.setText("90")
        self.Frames = QNumEdit(min=0, max=None, step=1, decimals=0, addSlider=False, label="Frames")
        self.Frames.setText("1")
        self.Frames.Text.textChanged.connect(self.summary.updateFrames)
        
        self.layoutH2 = QHBoxLayout()
        self.Delete = QPushButton("Delete")
        self.Delete.setFixedWidth(60)
        self.Delete.clicked.connect(self.deleteNode) 
        self.Run = QPushButton("Run")
        self.Run.setFixedWidth(50)
        self.Run.setEnabled(False)
        self.Run.clicked.connect(self.startRunCommand)
        self.RunChain = QPushButton("Run Chain")
        self.RunChain.setFixedWidth(75)
        self.RunChain.setEnabled(False)
        self.RunChain.clicked.connect(self.runCommandChain)
        self.layoutH2.addWidget(self.Delete)
        self.layoutH2.addWidget(self.Run)
        self.layoutH2.addWidget(self.RunChain)

        self.main_layout.addLayout(self.layoutH1)        
        self.main_layout.addLayout(self.Angle.widget_layout)
        self.main_layout.addLayout(self.Frames.widget_layout)     
        self.main_layout.addLayout(self.layoutH2)        

    def updateRun(self, chain_update:bool=False):
        current_run = self.Run.isEnabled()
        if self.summary.picker_model != []:
            self.Run.setEnabled(True)
        else:
            self.Run.setEnabled(False)
        if current_run != self.Run.isEnabled():
            if not chain_update:
                self.summary.findLastNode()

    def updateTab(self, current_type:int):
        pass
    
    def updateCommand(self) -> list[str]:
        super().updateCommand()

        if self.Run.isEnabled():
            center_object = "".join(self.summary.picker_center)
            if self.summary.picker_center is None:
                center = ""
            elif center_object == "":
                center = ""
            else:
                if center_object == "All":
                    center_object = "all"
                center = f"center {center_object}"

            objects = "".join(self.summary.picker_model)
            if objects == "All":
                objects = f"<i>'{objects.lower()}'</i>"
            else:
                objects = f"<i>'{objects}'</i>"

            self.script_string += f"turn {self.Axis.currentText().lower()} {self.Angle.getText()} {self.Frames.getText()} {center}{objects}<br>"
            self.script_string += f"<br>"
        
        return [self.start_script_string, self.script_string, self.end_script_string]    

class SimpleNodeWait(NodeBase):
    def __init__(self, session, summary:SimpleNodeSummary, title:str="", parent=None):
        super().__init__(session, summary, title, simple_node=True, parent=parent)

        self.initUI()

    def initUI(self):
        self.main_layout = QVBoxLayout()
        self.main_layout.setSpacing(5)
        self.main_layout.setContentsMargins(10, 10, 10, 10)
        self.setLayout(self.main_layout)

        self.Frames = QNumEdit(min=0, max=None, step=1, decimals=0, addSlider=False, label="Frames")
        self.Frames.setText("0")
        self.Frames.Text.textChanged.connect(self.summary.updateFrames)

        self.layoutH1 = QHBoxLayout()
        self.Delete = QPushButton("Delete")
        self.Delete.setFixedWidth(60)
        self.Delete.clicked.connect(self.deleteNode) 
        self.RunChain = QPushButton("Run Chain")
        self.RunChain.setFixedWidth(75)
        self.RunChain.setEnabled(False)
        self.RunChain.clicked.connect(self.runCommandChain)
        self.layoutH1.addWidget(self.Delete)
        self.layoutH1.addWidget(self.RunChain)

        self.main_layout.addLayout(self.Frames.widget_layout)
        self.main_layout.addLayout(self.layoutH1)

    def updateRun(self, chain_update:bool=False):
        pass

    def updateTab(self, current_type:int):
        pass

    def updateCommand(self) -> list[str]:
        super().updateCommand()

        if int(self.Frames.getText()) > 0 :
            wait = f"wait {int(self.Frames.getText())}<br>"
        else:
            wait = f"wait"
        self.script_string += f"{wait}"
        self.script_string += f"<br>"
        
        return [self.start_script_string, self.script_string, self.end_script_string]    

class SimpleNodeDelete(NodeBase):
    def __init__(self, session, scene:Scene, summary:SimpleNodeSummary, title:str="", parent=None):
        super().__init__(session, summary, title, simple_node=True, parent=parent)

        self.scene = scene
        self.current_type = 0

        self.initUI()

    def initUI(self):
        self.main_layout = QVBoxLayout()
        self.main_layout.setSpacing(5)
        self.main_layout.setContentsMargins(10, 10, 10, 10)
        self.setLayout(self.main_layout)

        self.layoutH1 = QHBoxLayout()
        self.lType = QLabel("Target")
        self.Type = QComboBox()
        self.Type.addItems(["All", "Custom"])
        self.Type.currentIndexChanged.connect(self.internal_updateRun)
        self.layoutH1.addWidget(self.lType)
        self.layoutH1.addWidget(self.Type)

        self.layoutH2 = QHBoxLayout()
        self.lAttachedHyds = QLabel("Delete attached hydrogens")
        self.lAttachedHyds.setWordWrap(True)
        self.lAttachedHyds.setFixedHeight(40)
        self.AttachedHyds = QSwitchControl(self.summary.node.scene.parent)
        self.summary.node.scene.parent.switches.append(self.AttachedHyds)
        self.layoutH2.addWidget(self.lAttachedHyds, alignment=Qt.AlignmentFlag.AlignHCenter)
        self.layoutH2.addWidget(self.AttachedHyds, alignment=Qt.AlignmentFlag.AlignHCenter)

        self.layoutH3 = QHBoxLayout()
        self.Delete = QPushButton("Delete")
        self.Delete.setFixedWidth(60)
        self.Delete.clicked.connect(self.deleteNode) 
        self.Run = QPushButton("Run")
        self.Run.setFixedWidth(50)
        self.Run.setEnabled(False)
        self.Run.clicked.connect(self.startRunCommand)
        self.layoutH3.addWidget(self.Delete)
        self.layoutH3.addWidget(self.Run)

        self.main_layout.addLayout(self.layoutH1)
        self.main_layout.addLayout(self.layoutH2)
        self.main_layout.addLayout(self.layoutH3)
        
    def updateRun(self, chain_update:bool=False):
        current_run = self.Run.isEnabled()
        if self.summary.picker_delete != []:
            self.Run.setEnabled(True)
        else:
            self.Run.setEnabled(False)
        if current_run != self.Run.isEnabled():
            if not chain_update:
                self.summary.findLastNode()
        
    def updateTab(self, current_type:int):
        self.current_type = current_type
        self.Type.clear()
        if self.current_type == 0:
            self.Type.addItems(["Atoms", "Residues", "Models", "Bonds", "Pseudobonds"])
            self.Type.setCurrentIndex(0)
            self.Type.setEnabled(True)
            self.AttachedHyds.setEnabled(True)
        elif self.current_type == 1:
            self.Type.addItems([])
            self.Type.setEnabled(False)
            self.AttachedHyds.setEnabled(False)
        elif self.current_type == 2:
            self.Type.addItems([])
            self.Type.setEnabled(False)
            self.AttachedHyds.setEnabled(False)
        elif self.current_type == 3:
            self.Type.addItems([])
            self.Type.setEnabled(False)
            self.AttachedHyds.setEnabled(False)

    def updateCommand(self) -> list[str]:
        super().updateCommand()

        if self.Run.isEnabled():
            objects = "".join(self.summary.picker_delete)
            if objects == "All":
                objects = f"<i>'{objects.lower()}'</i>"
            else:
                objects = f"<i>'{objects}'</i>"

            if self.current_type == 0:
                if self.Type.currentText() == "All":
                    self.script_string += f"delete {self.Type.currentText().lower()}<br>"
                else:
                    self.script_string += f"delete <i>'{objects}'</i> attachedHyds {self.AttachedHyds.isChecked()}<br>"
                self.script_string += f"<br>"
            elif self.current_type == 1:
                if self.Type.currentText() == "All":
                    self.script_string += f"2dlabels delete all<br>"
                else:
                    self.script_string += f"2dlabels delete {objects}<br>"
                self.script_string += f"<br>"
            elif self.current_type == 2:
                if self.Type.currentText() == "All":
                    self.script_string += f"label delete<br>"
                else:
                    self.script_string += f"label delete {self.Type.currentText().lower()} {objects}<br>"
                self.script_string += f"<br>"
            elif self.current_type == 3:
                self.script_string += f"view delete {objects}<br>"
                self.script_string += f"<br>"
        
        return [self.start_script_string, self.script_string, self.end_script_string]    

class SimpleNodeSplit(NodeBase):
    def __init__(self, session, summary:SimpleNodeSummary, title:str="", parent=None):
        super().__init__(session, summary, title, simple_node=True, parent=parent)
                        
        self.current_index = -1

        self.initUI()

    def initUI(self):
        self.main_layout = QVBoxLayout()
        self.main_layout.setSpacing(5)
        self.main_layout.setContentsMargins(10, 10, 10, 10)
        self.setLayout(self.main_layout)

        self.Model = QComboBox()
        self.Model.addItems(["Chains", "Ligands", "Connected", "Atoms"])

        self.layoutH2 = QHBoxLayout()
        self.Delete = QPushButton("Delete")
        self.Delete.setFixedWidth(60)
        self.Delete.clicked.connect(self.deleteNode) 
        self.Run = QPushButton("Run")
        self.Run.setFixedWidth(50)
        self.Run.setEnabled(False)
        self.Run.clicked.connect(self.startRunCommand)
        self.layoutH2.addWidget(self.Delete)
        self.layoutH2.addWidget(self.Run)

        self.main_layout.addWidget(self.Model)
        self.main_layout.addLayout(self.layoutH2)

    def updateRun(self, chain_update:bool=False): 
        current_run = self.Run.isEnabled()  
        if self.summary.picker_model != []: 
            self.Run.setEnabled(True)
        else:
            self.Run.setEnabled(False)   
        if current_run != self.Run.isEnabled():
            if not chain_update:
                self.summary.findLastNode() 
                
    def updateTab(self, current_type:int):
        pass
    
    def updateCommand(self) -> list[str]:
        super().updateCommand()

        if self.Run.isEnabled():
            objects = "".join(self.summary.picker_model)
            if objects == "All":
                objects = f"<i>'{objects.lower()}'</i>"
            else:
                objects = f"<i>'{objects}'</i>"
            self.script_string += f"split {objects} {self.Model.currentText().lower()}<br>"
            if self.Model.currentText() == "Ligands":
                self.script_string += f"split {objects} chains<br>"
            self.script_string += f"<br>"

        return [self.start_script_string, self.script_string, self.end_script_string]

class SimpleNodeEnd(NodeBase):
    def __init__(self, session, summary:SimpleNodeSummary, title:str="", parent=None):
        super().__init__(session, summary, title, simple_node=True, parent=parent)

        self.initUI()

    def initUI(self):
        self.main_layout = QVBoxLayout()
        self.main_layout.setSpacing(5)
        self.main_layout.setContentsMargins(10, 10, 10, 10)
        self.setLayout(self.main_layout)

        self.Framerate = QNumEdit(min=10, max=60, step=1, decimals=0, addSlider=True, label="Frames")
        self.Framerate.setText("20")  
        self.Framerate.Text.textChanged.connect(self.summary.updateFrames)

        self.layoutH1 = QHBoxLayout()
        self.lQuality = QLabel("Quality")
        self.Quality = QComboBox()  
        self.Quality.addItems(["Low", "Fair", "Medium", "Good", "High", "Higher", "Highest"])
        self.Quality.setCurrentIndex(3)
        self.layoutH1.addWidget(self.lQuality)
        self.layoutH1.addWidget(self.Quality, alignment=Qt.AlignmentFlag.AlignLeft, stretch=1)

        self.layoutH2 = QHBoxLayout()
        self.lName = QLabel("Movie Name")
        self.Name = QLineEdit()
        self.layoutH2.addWidget(self.lName)
        self.layoutH2.addWidget(self.Name)

        self.layoutH3 = QHBoxLayout()
        self.layoutH3V1 = QVBoxLayout()
        self.lRoundtrip = QLabel("Roundtrip")
        self.Roundtrip = QSwitchControl(self.summary.node.scene.parent)
        self.summary.node.scene.parent.switches.append(self.Roundtrip)
        self.layoutH3V2 = QVBoxLayout()
        self.lFormat = QLabel("Format")
        self.Format = QComboBox()
        self.Format.addItems(["mp4", "webm", "ogv", "mov", "avi", "wmv", "png"])
        self.Format.setCurrentIndex(0)
        self.layoutH3V1.addWidget(self.lRoundtrip)
        self.layoutH3V1.addWidget(self.Roundtrip)
        self.layoutH3V2.addWidget(self.lFormat)
        self.layoutH3V2.addWidget(self.Format)
        self.layoutH3.addLayout(self.layoutH3V1)
        self.layoutH3.addLayout(self.layoutH3V2)

        self.layoutH4 = QHBoxLayout()
        self.RunChain = QPushButton("Run Chain")
        self.RunChain.setFixedWidth(75)
        self.RunChain.clicked.connect(self.runCommandChain)
        self.layoutH4.addWidget(self.RunChain)

        self.main_layout.addLayout(self.Framerate.widget_layout)
        self.main_layout.addLayout(self.layoutH1)
        self.main_layout.addLayout(self.layoutH2)
        self.main_layout.addLayout(self.layoutH3)
        self.main_layout.addLayout(self.layoutH4)

    def updateRun(self, chain_update:bool=False):
        pass

    def updateTab(self, current_type:int):
        pass
    
    def updateCommand(self) -> list[str]:
        super().updateCommand()

        self.end_script_string += f"movie stop;<br>"
        self.end_script_string += f"movie encode {self.Name.text()}.{self.Format.currentText()} quality {self.Quality.currentText().lower()} framerate {self.Framerate.getText()} roundTrip {self.Roundtrip.isChecked()}"

        return [self.start_script_string, self.script_string, self.end_script_string]

class SimpleNodeSummary(QWidget):
    def __init__(self, session, node:Node, model_input:bool=False, color_input:bool=False, center_input:bool=False, view_input:bool=False, fly_input:bool=False, parent=None):
        super().__init__(parent)

        self.session = session
        self.node = node

        self.picker_model = []
        self.picker_color_groups = []
        self.picker_center = []
        self.picker_view = []
        self.picker_fly_groups = []
        self.picker_delete = []
        self.accumulated_frames = 0
        self.used_frames = 0

        self.total_frames = 0

        self.initUI(model_input, color_input, center_input, view_input, fly_input)
        
    def initUI(self, model_input:bool, color_input:bool, center_input:bool, view_input:bool, fly_input:bool):
        self.main_layout = QVBoxLayout()
        self.main_layout.setSpacing(5)
        self.main_layout.setContentsMargins(10, 10, 10, 10)
        self.setLayout(self.main_layout)
        
        if NodeType(self.node.nodeType) == NodeType.Picker:
            if NodePickerType(self.node.nodePickerType) == NodePickerType.ModelPicker:
                self.layoutH1 = QHBoxLayout()
                self.lModelText = QLabel("Picked:")
                self.lModelText.setWordWrap(True)
                self.lModelText.setAlignment(Qt.AlignmentFlag.AlignTop)
                self.ModelText = QLabel()
                self.ModelText.setText("None")
                self.layoutH1.addWidget(self.lModelText)
                self.layoutH1.addWidget(self.ModelText)
                self.main_layout.addLayout(self.layoutH1)
            elif NodePickerType(self.node.nodePickerType) == NodePickerType.ColorPicker:
                self.layoutH1 = QHBoxLayout()
                self.lColorText = QLabel("Picked:")
                self.lColorText.setWordWrap(True)
                self.lColorText.setAlignment(Qt.AlignmentFlag.AlignTop)
                self.ColorText = QLabel()
                self.ColorText.setText("0 Groups")
                self.layoutH1.addWidget(self.lColorText)
                self.layoutH1.addWidget(self.ColorText)
                self.main_layout.addLayout(self.layoutH1)
            elif NodePickerType(self.node.nodePickerType) == NodePickerType.CenterPicker:
                self.layoutH1 = QHBoxLayout()
                self.lCenterText = QLabel("Picked:")
                self.lCenterText.setWordWrap(True)
                self.lCenterText.setAlignment(Qt.AlignmentFlag.AlignTop)
                self.CenterText = QLabel()
                self.CenterText.setText("None")
                self.layoutH1.addWidget(self.lCenterText)
                self.layoutH1.addWidget(self.CenterText)
                self.main_layout.addLayout(self.layoutH1)
            elif NodePickerType(self.node.nodePickerType) == NodePickerType.ViewPicker:
                self.layoutH1 = QHBoxLayout()
                self.lViewText = QLabel("Picked:")
                self.lViewText.setWordWrap(True)
                self.lViewText.setAlignment(Qt.AlignmentFlag.AlignTop)
                self.ViewText = QLabel()
                self.ViewText.setText("None")
                self.layoutH1.addWidget(self.lViewText)
                self.layoutH1.addWidget(self.ViewText)
                self.main_layout.addLayout(self.layoutH1)
            elif NodePickerType(self.node.nodePickerType) == NodePickerType.FlyPicker:
                self.layoutH1 = QHBoxLayout()
                self.lFlyText = QLabel("Picked:")
                self.lFlyText.setWordWrap(True)
                self.lFlyText.setAlignment(Qt.AlignmentFlag.AlignTop)
                self.FlyText = QLabel()
                self.FlyText.setText("0 transitions")
                self.layoutH1.addWidget(self.lFlyText)
                self.layoutH1.addWidget(self.FlyText)
                self.main_layout.addLayout(self.layoutH1)
            elif NodePickerType(self.node.nodePickerType) == NodePickerType.DeletePicker:
                self.layoutH1 = QHBoxLayout()
                self.lDeleteText = QLabel("Picked:")
                self.lDeleteText.setWordWrap(True)
                self.lDeleteText.setAlignment(Qt.AlignmentFlag.AlignTop)
                self.DeleteText = QLabel()
                self.DeleteText.setText("None")
                self.layoutH1.addWidget(self.lDeleteText)
                self.layoutH1.addWidget(self.DeleteText)
                self.main_layout.addLayout(self.layoutH1)
        else:
            self.layoutH1 = QHBoxLayout()
            self.lFrames = QLabel(f"Frames: {self.used_frames}")
            self.layoutH1.addWidget(self.lFrames, alignment=Qt.AlignmentFlag.AlignLeft)
            self.main_layout.addLayout(self.layoutH1)
            if NodeType(self.node.nodeType) == NodeType.End:
                self.layoutH2 = QHBoxLayout()
                self.lTotalFrames = QLabel(f"Total Frames: {self.total_frames}")
                self.layoutH2.addWidget(self.lTotalFrames, alignment=Qt.AlignmentFlag.AlignLeft)
                self.layoutH3 = QHBoxLayout()
                self.lLength = QLabel(f"Length: {self.convertTime(0)}")
                self.layoutH3.addWidget(self.lLength, alignment=Qt.AlignmentFlag.AlignLeft)
                self.main_layout.addLayout(self.layoutH2)
                self.main_layout.addLayout(self.layoutH3)

    def updateModel(self):
        self.node.content.updateRun(chain_update=True)
        self.updateRunChain()

    def updateColor(self):
        self.node.content.updateRun(chain_update=True)
        self.updateRunChain()

    def updateCenter(self):
        self.node.content.updateRun(chain_update=True)
        self.updateRunChain()

    def updateView(self):
        self.node.content.updateRun(chain_update=True)
        self.updateRunChain()

    def updateFly(self):
        self.node.content.updateRun(chain_update=True)
        self.updateRunChain()

    def updateDelete(self):
        self.node.content.updateRun(chain_update=True)

    def updateRunChain(self):
        no_output=True
        if self.node.node_output is not None:
            if self.node.node_output.hasEdge():
                no_output=False
                self.node.node_output.edge.end_socket.node.summary.updateOutputValues()
        if no_output:
            self.updateChainRun() 

    def updateOutputValues(self, update_frames:bool=True, check_update:bool=True):
        #pass frames, model, color, center, view, fly. check run when finished
        #frames:
        if NodeType(self.node.nodeType) == NodeType.Wait:
            if int(self.node.content.Frames.getText()) > 0 and int(self.node.content.Frames.getText()) > self.accumulated_frames:
                self.lFrames.setText(f"Frames: {int(self.node.content.Frames.getText())}")
                self.used_frames = int(self.node.content.Frames.getText())
            else:
                self.lFrames.setText(f"Frames: {self.accumulated_frames}")
                self.used_frames = self.accumulated_frames
        elif NodeType(self.node.nodeType) == NodeType.End:
            self.lFrames.setText(f"Frames: {self.accumulated_frames}")
            self.lTotalFrames.setText(f"Total Frames: {self.total_frames}")
            self.lLength.setText(f"Length: {self.convertTime(self.total_frames / int(self.node.content.Framerate.getText()))}")
        else:
            if hasattr(self.node.content, "Frames"):
                self.used_frames = int(self.node.content.Frames.getText())
            else: 
                self.used_frames = 0
            self.lFrames.setText(f"Frames: {self.accumulated_frames + self.used_frames}")
        
        no_output=True
        if self.node.node_output is not None:
            if self.node.node_output.hasEdge():
                no_output=False
                if (update_frames and check_update) or not check_update:
                    if NodeType(self.node.nodeType) == NodeType.Wait:
                        self.node.node_output.edge.end_socket.node.summary.accumulated_frames = 0
                        self.node.node_output.edge.end_socket.node.summary.total_frames = self.total_frames + self.used_frames - self.accumulated_frames
                        update_frames = False
                    elif NodeType(self.node.node_output.edge.end_socket.node.nodeType) == NodeType.Wait:
                        self.node.node_output.edge.end_socket.node.summary.accumulated_frames = self.accumulated_frames + self.used_frames
                        self.node.node_output.edge.end_socket.node.summary.total_frames = self.total_frames + self.used_frames
                        self.node.node_output.edge.end_socket.node.content.Frames.setMin(self.node.node_output.edge.end_socket.node.summary.accumulated_frames)
                        self.node.node_output.edge.end_socket.node.content.Frames.setText(self.node.node_output.edge.end_socket.node.summary.accumulated_frames)
                    else:
                        if hasattr(self.node.node_output.edge.end_socket.node.content, "Frames"):
                            self.node.node_output.edge.end_socket.node.summary.accumulated_frames = 0
                            self.node.node_output.edge.end_socket.node.summary.total_frames = self.total_frames + self.used_frames
                            update_frames = False
                        else:
                            self.node.node_output.edge.end_socket.node.summary.accumulated_frames = self.accumulated_frames + self.used_frames
                            self.node.node_output.edge.end_socket.node.summary.total_frames = self.total_frames + self.used_frames
                else:
                    if NodeType(self.node.nodeType) == NodeType.Wait:
                        self.node.node_output.edge.end_socket.node.summary.total_frames = self.total_frames
                    else:
                        self.node.node_output.edge.end_socket.node.summary.total_frames = self.total_frames + self.used_frames
                self.node.node_output.edge.end_socket.node.content.updateRun(chain_update=True)
                self.node.node_output.edge.end_socket.node.summary.updateOutputValues(update_frames, check_update)
        if no_output:
            self.updateChainRun() 

    def updateFrames(self):
        self.updateFramesValues()

    def updateFramesValues(self, update_frames:bool=True):
        if NodeType(self.node.nodeType) == NodeType.Wait:
            if int(self.node.content.Frames.getText()) > 0 and int(self.node.content.Frames.getText()) > self.accumulated_frames:
                self.lFrames.setText(f"Frames: {int(self.node.content.Frames.getText())}")
                self.used_frames = int(self.node.content.Frames.getText())
            else:
                self.lFrames.setText(f"Frames: {self.accumulated_frames}")
                self.used_frames = self.accumulated_frames
        elif NodeType(self.node.nodeType) == NodeType.End:
            self.lFrames.setText(f"Frames: {self.accumulated_frames}")
            self.lTotalFrames.setText(f"Total Frames: {self.total_frames}")
            self.lLength.setText(f"Length: {self.convertTime(self.total_frames / int(self.node.content.Framerate.getText()))}")
        else:
            if hasattr(self.node.content, "Frames"):
                self.used_frames = int(self.node.content.Frames.getText())
            else: 
                self.used_frames = 0
            self.lFrames.setText(f"Frames: {self.accumulated_frames + self.used_frames}")
        no_output=True
        if self.node.node_output is not None:
            if self.node.node_output.hasEdge():
                no_output=False
                if update_frames:
                    if NodeType(self.node.nodeType) == NodeType.Wait:
                        self.node.node_output.edge.end_socket.node.summary.accumulated_frames = 0
                        self.node.node_output.edge.end_socket.node.summary.total_frames = self.total_frames + self.used_frames - self.accumulated_frames
                        update_frames = False
                    elif NodeType(self.node.node_output.edge.end_socket.node.nodeType) == NodeType.Wait:
                        self.node.node_output.edge.end_socket.node.summary.accumulated_frames = self.accumulated_frames + self.used_frames
                        self.node.node_output.edge.end_socket.node.summary.total_frames = self.total_frames + self.used_frames
                        self.node.node_output.edge.end_socket.node.content.Frames.setMin(self.node.node_output.edge.end_socket.node.summary.accumulated_frames)
                        self.node.node_output.edge.end_socket.node.content.Frames.setText(self.node.node_output.edge.end_socket.node.summary.accumulated_frames)
                    else:
                        if hasattr(self.node.node_output.edge.end_socket.node.content, "Frames"):
                            self.node.node_output.edge.end_socket.node.summary.accumulated_frames = 0
                            self.node.node_output.edge.end_socket.node.summary.total_frames = self.total_frames + self.used_frames
                            update_frames = False
                        else:
                            self.node.node_output.edge.end_socket.node.summary.accumulated_frames = self.accumulated_frames + self.used_frames
                            self.node.node_output.edge.end_socket.node.summary.total_frames = self.total_frames + self.used_frames
                else:
                    if NodeType(self.node.nodeType) == NodeType.Wait:
                        self.node.node_output.edge.end_socket.node.summary.total_frames = self.total_frames
                    else:
                        self.node.node_output.edge.end_socket.node.summary.total_frames = self.total_frames + self.used_frames
                self.node.node_output.edge.end_socket.node.summary.updateFramesValues(update_frames)
                self.node.node_output.edge.end_socket.node.content.updateRun(chain_update=True)
        if no_output:
            self.updateChainRun()
            
    def findLastNode(self):
        no_outputs = True
        if self.node.node_output is not None:
            if self.node.node_output.hasEdge():
                no_outputs = False
                self.node.node_output.edge.end_socket.node.summary.findLastNode()
        if no_outputs:
            self.updateChainRun()

    def updateChainRun(self, run_enabled:bool=True):
        if run_enabled:
            if hasattr(self.node.content, "Run"):
                run_enabled = self.node.content.Run.isEnabled()
        if self.node.node_input is not None:
            if self.node.node_input.hasEdge():
                run_enabled = self.node.node_input.edge.start_socket.node.summary.updateChainRun(run_enabled)
        if hasattr(self.node.content, "RunChain"):
            self.node.content.RunChain.setEnabled(run_enabled)
        return run_enabled
    
    def resetOutputValues(self, reset_frames:bool=True):
        if NodeType(self.node.nodeType) == NodeType.Wait:
            if int(self.node.content.Frames.getText()) > 0 and int(self.node.content.Frames.getText()) > self.accumulated_frames:
                self.lFrames.setText(f"Frames: {int(self.node.content.Frames.getText())}")
                self.used_frames = int(self.node.content.Frames.getText())
            else:
                self.lFrames.setText(f"Frames: {self.accumulated_frames}")
                self.used_frames = self.accumulated_frames
        elif NodeType(self.node.nodeType) == NodeType.End:
            self.lFrames.setText(f"Frames: {self.accumulated_frames}")
            self.lTotalFrames.setText(f"Total Frames: {self.total_frames}")
            self.lLength.setText(f"Length: {self.convertTime(self.total_frames / int(self.node.content.Framerate.getText()))}")
        else:
            if hasattr(self.node.content, "Frames"):
                self.used_frames = int(self.node.content.Frames.getText())
            else: 
                self.used_frames = 0
            self.lFrames.setText(f"Frames: {self.accumulated_frames + self.used_frames}")
        no_output=True
        if self.node.node_output is not None:
            if self.node.node_output.hasEdge():
                no_output=False
                if reset_frames:
                    self.node.node_output.edge.end_socket.node.summary.accumulated_frames = 0
                    self.node.node_output.edge.end_socket.node.summary.total_frames = 0
                    if NodeType(self.node.nodeType) == NodeType.Wait:
                        reset_frames = False
                    if NodeType(self.node.node_output.edge.end_socket.node.nodeType) == NodeType.Wait:
                        self.node.node_output.edge.end_socket.node.content.Frames.setMin(0)
                        self.node.node_output.edge.end_socket.node.content.Frames.setText(0)
                        reset_frames = False
                    elif hasattr(self.node.node_output.edge.end_socket.node.content, "Frames"):
                        reset_frames = False
                else:
                    if NodeType(self.node.nodeType) == NodeType.Wait:
                        self.node.node_output.edge.end_socket.node.summary.total_frames = self.total_frames
                    else:
                        self.node.node_output.edge.end_socket.node.summary.total_frames = self.total_frames + self.used_frames
                self.node.node_output.edge.end_socket.node.summary.resetOutputValues(reset_frames)
        if no_output:
            self.updateChainRun()

    def convertTime(self, value:int|float) -> str:
        if value < 60:
            return(f"{format(round(value, 2), '.2f')} Seconds")
        else:
            value = value / 60
            if value < 60:
                return(f"{format(round(value, 2), '.2f')} Minutes")
            else:
                value = value / 60
                if value < 24:
                    return(f"{format(round(value, 2), '.2f')} Hours")
                else:
                    value = value / 24
                    if value < 7:
                        return(f"{format(round(value, 2), '.2f')} Days")
                    else:
                        value = value / 7
                        if value < 52.177457:
                            return(f"{format(round(value, 2), '.2f')} Weeks")
                        else:
                            value = value / 52.177457
                            return(f"{format(round(value, 2), '.2f')} Years")