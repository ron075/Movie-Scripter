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
    
class AdvancedNodeStart(NodeBase):
    def __init__(self, session, summary:AdvancedNodeSummary, title:str="", parent=None):
        super().__init__(session, summary, title, simple_node=False, parent=parent)

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
    
    def updateComment(self) -> list[str]:
        start_script_string_comment = f"<u><b>{self.summary.node.nodeType.name}: {self.summary.node.nodeID}</b></u><br>"
        script_string_comment = f"<u><b>{self.summary.node.nodeType.name}: {self.summary.node.nodeID}</b></u><br>"
        end_script_string_comment = f""

        if self.Record.isChecked():
            start_script_string_comment += f"Resets the movie to free memory<br>"
            start_script_string_comment += f"Start movie recording<br>"
            start_script_string_comment += f"<br>"
        else:
            start_script_string_comment += f"Resets the movie to free memory<br>"
            start_script_string_comment += f"<br>"

        script_string_comment += f"Resizes window to: width={int(self.Width.getText())}px, height={int(self.Height.getText())}px<br>"
        script_string_comment += f"sets background color to <a style='background-color:{self.BackgroundColorPicked.name()};'>{self.BackgroundColorPicked.name()}</a><br>"
        script_string_comment += f"<br>"

        return [start_script_string_comment, script_string_comment, end_script_string_comment]

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
    

class AdvancedNodePicker(NodeBase):
    def __init__(self, session, scene:Scene, summary:AdvancedNodeSummary, all_views:bool, title:str="", selector_type:NodePickerType=NodePickerType.ModelPicker, parent=None):

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

        super().__init__(session, summary, title, simple_node=False, parent=parent)

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
    
    def updateComment(self) -> list[str]:
        start_script_string_comment = f""
        script_string_comment = f"<u><b>{self.summary.node.nodeType.name}: {self.summary.node.nodeID}</b></u><br>"
        end_script_string_comment = f""

        return [start_script_string_comment, script_string_comment, end_script_string_comment]

    def updateCommand(self) -> list[str]:
        super().updateCommand()

        return [self.start_script_string, self.script_string, self.end_script_string]    

class AdvancedNodeColorPalette(NodeBase):
    def __init__(self, session, summary:AdvancedNodeSummary, title:str="", colormap_height:int=50, parent=None):
        super().__init__(session, summary, title, simple_node=False, parent=parent)

        self.colormap_height = colormap_height
        
        self.current_index = -1

        self.group_colors = []
        self.group_target = []
        self.group_halfbond = []
        self.group_change_transparency = []
        self.group_transparency = []
        self.group_level = []
        
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
        self.Color.addItems(["By Element", "By Hetero", "From Atoms", "From Cartoons", "By Nucleotide ", "By Chain", "By Identity", "By Model ", "From Palette", "Partial Random", "Random"])
        self.color_list = ["byelement", "byhetero", "fromatoms", "fromcartoons", "bynucleotide", "bychain", "byidentity", "bymodel", None, None, "random"]
        self.lCustomColor = QLabel("Color Palette")
        self.lCustomColor.setWordWrap(True)
        self.CustomColor = QComboBox()
        self.CustomColor.setCurrentIndex(1)
        self.layoutH1.addWidget(self.lColor, alignment = Qt.AlignmentFlag.AlignCenter)
        self.layoutH1.addWidget(self.Color, alignment = Qt.AlignmentFlag.AlignCenter)
        self.layoutH1.addWidget(self.lCustomColor, alignment = Qt.AlignmentFlag.AlignCenter)
        self.layoutH1.addWidget(self.CustomColor, alignment = Qt.AlignmentFlag.AlignCenter)

        self.ColorMap = QColorMap(self.colormap_height)       
        self.CustomColor.addItems(self.ColorMap.colorRangeLibrary.keys())    
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
        self.Tab = QTabWidget()
        self.container1 = QWidget()
        self.layoutH4T1V1 = QVBoxLayout(self.container1)
        self.layoutH4T1V1H1 = QHBoxLayout()
        self.GroupColor = QPushButton("Change Color") 
        self.GroupColor.setFixedWidth(100)   
        self.GroupColor.clicked.connect(self.changeGroupColor)
        self.GroupColor.setEnabled(False)
        self.ColorLabel = QLabel()
        self.ColorLabel.setFixedWidth(50)   
        self.ColorLabel.setFixedHeight(50)    
        self.ColorLabel.setStyleSheet("QLabel { border: 1px solid black }")
        self.ColorDialog = QColorDialog()
        self.layoutH4T1V1H1.addWidget(self.GroupColor)
        self.layoutH4T1V1H1.addWidget(self.ColorLabel)
        self.layoutH4T1V1H2 = QHBoxLayout()
        self.lHalfbond = QLabel("Halfbond")
        self.Halfbond = QSwitchControl(self.summary.node.scene.parent)
        self.summary.node.scene.parent.switches.append(self.Halfbond)
        self.Halfbond.setEnabled(False)
        self.layoutH4T1V1H2.addWidget(self.lHalfbond)
        self.layoutH4T1V1H2.addWidget(self.Halfbond)
        self.layoutH4T1V1.addLayout(self.layoutH4T1V1H1)
        self.layoutH4T1V1.addLayout(self.layoutH4T1V1H2)
        self.container2 = QWidget()
        self.layoutH4T2H1 = QHBoxLayout(self.container2)
        self.lLevel = QLabel("Level")
        self.Level = QComboBox()
        self.Level.addItems(["Structures", "Polymers", "Chains", "Residues"])
        self.Level.setEnabled(False)
        self.layoutH4T2H1.addWidget(self.lLevel)
        self.layoutH4T2H1.addWidget(self.Level)
        self.Tab.insertTab(0, self.container1, "Simple")
        self.Tab.insertTab(1, self.container2, "Sequential")
        self.layoutH4.addWidget(self.Tab)

        self.layoutH5 = QHBoxLayout()
        self.lTarget = QLabel("Target")
        self.Target = QComboBox()
        self.Target.addItems(["All", "Surfaces", "Cartoons", "Atoms", "Bonds", "Rings", "Labels"])
        self.target_list = ["abcspfl", "s", "c", "a", "b", "f", "l"]
        self.Target.setEnabled(False)
        self.layoutH5.addWidget(self.lTarget, alignment=Qt.AlignmentFlag.AlignHCenter)
        self.layoutH5.addWidget(self.Target, alignment=Qt.AlignmentFlag.AlignHCenter)

        self.layoutH6 = QHBoxLayout()
        self.ChangeTransparency = QSwitchControl(self.summary.node.scene.parent)
        self.summary.node.scene.parent.switches.append(self.ChangeTransparency)
        self.ChangeTransparency.setEnabled(False)
        self.ChangeTransparency.stateChanged.connect(self.updateTransparency)
        self.Transparency = QNumEdit(min=0, max=100, step=1, decimals=0, addSlider=True, label="Transparency")
        self.Transparency.setEnabled(False)
        self.Transparency.setText("0")
        self.layoutH6.addWidget(self.ChangeTransparency)
        self.layoutH6.addLayout(self.Transparency.widget_layout)

        self.layoutH7 = QHBoxLayout()
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
        self.layoutH7.addWidget(self.Delete)
        self.layoutH7.addWidget(self.Run)
        self.layoutH7.addWidget(self.RunChain)

        self.main_layout.addLayout(self.layoutH1)
        self.main_layout.addLayout(self.ColorMap.widget_layout)
        self.main_layout.addLayout(self.layoutH3)
        self.main_layout.addLayout(self.layoutH4)
        self.main_layout.addLayout(self.layoutH5)
        self.main_layout.addLayout(self.layoutH6)
        self.main_layout.addLayout(self.layoutH7)

    def updateRun(self, chain_update:bool=False):
        current_run = self.Run.isEnabled()
        if self.summary.used_color_groups != []:
            self.Group.setEnabled(True)
            self.GroupColor.setEnabled(True)
            self.Target.setEnabled(True)
            self.Halfbond.setEnabled(True)
            self.ChangeTransparency.setEnabled(True)
            self.Level.setEnabled(True)
            self.Run.setEnabled(True)
        else:            
            self.ColorLabel.setStyleSheet("QLabel { background-color : transparent; border: 1px solid black}")
            self.Tab.setCurrentIndex(0)
            self.Group.setEnabled(False)
            self.Group.setCurrentText("")
            self.GroupColor.setEnabled(False)
            self.Target.setEnabled(False)
            self.Target.setCurrentIndex(0)
            self.Halfbond.setEnabled(False)
            self.Halfbond.setChecked(False)
            self.ChangeTransparency.setEnabled(False)
            self.ChangeTransparency.setChecked(False)
            self.Level.setEnabled(False)
            self.Transparency.setText("0")
            self.Run.setEnabled(False)
        if current_run != self.Run.isEnabled():
            if not chain_update:
                self.summary.findLastNode()

    def updateTab(self, current_type:int):
        pass
    
    def updateComment(self) -> list[str]:
        start_script_string_comment = ""
        script_string_comment = f"<u><b>{self.summary.node.nodeType.name}: {self.summary.node.nodeID}</b></u><br>"
        end_script_string_comment = ""

        if self.Run.isEnabled():
            for i, group in enumerate(self.summary.used_color_groups):
                if self.Tab.currentIndex() == 1: #Sequential
                    objects = "".join(group)
                    if objects == "All":
                        objects = "all models"

                    level = f"by {self.Level.itemText(self.group_level[i])} "
                    if self.Target.itemText(self.group_target[self.current_index]) == "All":
                        target = f"everything in"
                    else:
                        target = f"the {self.Target.itemText(self.group_target[self.current_index])} of"
                    color = f";"
                    halfbond = f""
                    if self.group_change_transparency[i]:
                        transparency = f" <i>'{objects}'</i> are {self.group_transparency[i]}% transparent;"
                    else:
                        transparency = " No transparency changes;"
                else:
                    objects = "".join(group)
                    if objects == "All":
                        objects = "all models"

                    level = f""
                    if self.Target.itemText(self.group_target[self.current_index]) == "All":
                        target = f"everything in"
                    else:
                        target = f"the {self.Target.itemText(self.group_target[self.current_index])} of"
                    if self.Color.currentText() == "Partial Random" or self.Color.currentText() == "From Palette":
                        color = f"in <a style='background-color:{self.group_colors[i].name()};'>{self.group_colors[i].name()}</a>;"
                    else:
                        color = f"using '{self.group_colors[i]}';"
                    if self.group_halfbond[i]:
                        halfbond = f" Bonds are shown in halfbond mode - Bond will get it's display options from it's flanking atoms"
                    else:
                        halfbond = f""
                    if self.group_change_transparency[i]:
                        transparency = f" <i>'{objects}'</i> are {self.group_transparency[i]}% transparent;"
                    else:
                        transparency = " No transparency changes;"
                script_string_comment +=f"Colors {target} <b><i>'{objects}'</i></b> {level}{color}{transparency}{halfbond}<br>"
            script_string_comment += f"<br>"
        return [start_script_string_comment, script_string_comment, end_script_string_comment]

    def updateCommand(self) -> list[str]:
        super().updateCommand()

        if self.Run.isEnabled():
            for i, group in enumerate(self.summary.used_color_groups):
                if self.Tab.currentIndex() == 1: #Sequential
                    sequential = "sequential "
                    level = f"level {self.Level.itemText(self.group_level[i])}"
                    palette = f"palette "
                    for i, color in enumerate(self.ColorMap.colorRangeLibrary[self.CustomColor.setCurrentText()][1]):
                        if i == 0:
                            palette += f"{color.name()}"
                        else:
                            palette += f":{color.name()}"
                    color = ""
                    halfbond = ""
                    target = f"target {self.target_list[self.group_target[self.current_index]]}"
                else:
                    sequential = ""
                    level = ""
                    palette = ""
                    if self.Color.currentText() == "Partial Random" or self.Color.currentText() == "From Palette":
                        color = f"{self.group_colors[i].name()}"
                    else:
                        color_type = "".join(self.group_colors[i].split(" ")).lower()
                        color = f"{color_type}"
                    halfbond = f"halfbond {self.group_halfbond[i]}"
                    target = f"target {self.target_list[self.group_target[self.current_index]]}"

                if self.group_change_transparency[i]:
                    transparency = f"transparency {self.group_transparency[i]}"
                else:
                    transparency = ""
                objects = "".join(group)
                if objects == "All":
                    objects = f"<i>'{objects.lower()}'</i>"
                else:
                    objects = f"<i>'{objects}'</i>"

                self.script_string += f"color {sequential}{objects} {color} {level} {target} {halfbond} {palette} {transparency}<br>"
            self.script_string += f"<br>"

        return [self.start_script_string, self.script_string, self.end_script_string]

    def updateUsedColors(self):
        if self.summary.ColorToggle.isChecked():
            self.summary.used_color_groups = self.summary.picker_color_groups
        else:
            self.summary.used_color_groups = self.summary.chain_color_groups
            
    def generateGroups(self):
        self.Group.currentIndexChanged.disconnect(self.groupChange)
        self.Group.clear()
        for i, group in enumerate(self.summary.used_color_groups):
            self.Group.addItem(f"Group {i + 1}")
        self.current_index = self.Group.currentIndex()
        self.Group.currentIndexChanged.connect(self.groupChange)

    def generateColors(self):
        if self.summary.used_color_groups != []:
            if self.Color.currentText() == "From Palette":
                self.GroupColor.setEnabled(True)
                self.group_colors = self.ColorMap.get_colors(self.CustomColor.currentText(), len(self.summary.used_color_groups), False)
            elif self.Color.currentText() == "Partial Random":
                self.GroupColor.setEnabled(True)
                self.group_colors = self.ColorMap.get_colors(self.CustomColor.currentText(), len(self.summary.used_color_groups), True)
            else:
                self.GroupColor.setEnabled(False)
                self.group_colors = [self.Color.currentText()] * len(self.summary.used_color_groups)

    def addGroup(self):
        self.updateUsedColors()
        self.updateGroup()
        self.group_target.append(0)
        self.group_halfbond.append(False)
        self.group_change_transparency.append(False)
        self.group_transparency.append("0")
        self.group_level.append(0)
        self.generateGroups()
        self.generateColors()
        self.switchGroup()

    def addGroups(self):
        self.updateUsedColors()
        self.updateGroup()
        self.group_target = []
        self.group_halfbond = []
        self.group_change_transparency = []
        self.group_transparency = []
        self.group_level = []
        for group in self.summary.used_color_groups:
            self.group_target.append(0)
            self.group_halfbond.append(False)
            self.group_change_transparency.append(False)
            self.group_transparency.append("0")
            self.group_level.append(0)
        self.generateGroups()
        self.generateColors()
        self.switchGroup()

    def removeGroup(self, row_indexes):
        self.updateUsedColors()
        self.updateGroup()
        for index in sorted(row_indexes, reverse=True):
            del self.group_target[index]
            del self.group_halfbond[index]
            del self.group_change_transparency[index]
            del self.group_transparency[index]
            del self.group_level[index]
        self.generateGroups()
        self.generateColors()
        self.switchGroup()

    def resetGroups(self):
        self.updateUsedColors()
        self.group_target = []
        self.group_halfbond = []
        self.group_change_transparency = []
        self.group_transparency = []
        self.group_level = []
        for group in self.summary.used_color_groups:
            self.group_target.append(0)
            self.group_halfbond.append(False)
            self.group_change_transparency.append(False)
            self.group_transparency.append("0")
            self.group_level.append(0)
        self.generateGroups()
        self.switchGroup()
    
    def updateGroup(self):
        if self.current_index > -1:
            self.group_target[self.current_index] = self.Target.currentIndex()
            self.group_halfbond[self.current_index] = self.Halfbond.isChecked()
            self.group_change_transparency[self.current_index] = self.ChangeTransparency.isChecked()
            self.group_transparency[self.current_index] = self.Transparency.getText()
            self.group_level[self.current_index] = self.Level.currentIndex()
  
    def switchGroup(self):
        self.current_index = self.Group.currentIndex()
        if self.current_index > -1:
            if self.Color.currentText() == "Partial Random" or self.Color.currentText() == "From Palette":
                self.ColorLabel.setStyleSheet(f"QLabel {{ background-color : rgb({self.group_colors[self.current_index].getRgb()[0]},{self.group_colors[self.current_index].getRgb()[1]},{self.group_colors[self.current_index].getRgb()[2]}); border: 1px solid black}}")
            else:            
                self.ColorLabel.setStyleSheet("QLabel { background-color : rgb(0,0,0); border: 1px solid black}")
            self.Target.setCurrentIndex(self.group_target[self.current_index])        
            self.Halfbond.setChecked(self.group_halfbond[self.current_index])    
            self.ChangeTransparency.setChecked(self.group_change_transparency[self.current_index]) 
            self.Transparency.setText(self.group_transparency[self.current_index])
            self.Level.setCurrentIndex(self.group_level[self.current_index]) 
        else:
            self.ColorLabel.setStyleSheet("QLabel { background-color : transparent; border: 1px solid black}")

    def switchColors(self):
        self.generateColors()
        self.updateGroup()
        self.switchGroup()
    
    def groupChange(self):
        self.updateGroup()
        self.switchGroup()

    def changeGroupColor(self):
        color = self.ColorDialog.getColor()
        self.group_colors[self.Group.currentIndex()] = color
        self.ColorLabel.setStyleSheet(f"QLabel {{ background-color : rgb({self.group_colors[self.Group.currentIndex()].getRgb()[0]},{self.group_colors[self.Group.currentIndex()].getRgb()[1]},{self.group_colors[self.Group.currentIndex()].getRgb()[2]}); border: 1px solid black}}")
    
    def updateColorMap(self):
        self.ColorMap.updateColormap(self.CustomColor.currentText())

    def updateTransparency(self):
        if self.ChangeTransparency.isChecked():
            self.Transparency.setEnabled(True)
        else:
            self.Transparency.setEnabled(False)

class AdvancedNodeLighting(NodeBase):
    def __init__(self, session, summary:AdvancedNodeSummary, title:str="", parent=None):
        super().__init__(session, summary, title, simple_node=False, parent=parent)

        self.initUI()

    def initUI(self):
        self.main_layout = QVBoxLayout()
        self.main_layout.setSpacing(5)
        self.main_layout.setContentsMargins(10, 10, 10, 10)
        self.setLayout(self.main_layout)

        self.layoutH1 = QHBoxLayout()        
        self.lPreset = QLabel("Preset")
        self.Preset = QComboBox()
        self.Preset.addItems(["Default", "Flat", "Gentle", "Soft", "Full", "Simple"])
        self.Preset.setCurrentIndex(0)
        self.layoutH1.addWidget(self.lPreset)
        self.layoutH1.addWidget(self.Preset)

        self.layoutH2 = QHBoxLayout()    
        self.Delete = QPushButton("Delete")
        self.Delete.setFixedWidth(60)
        self.Delete.clicked.connect(self.deleteNode) 
        self.Run = QPushButton("Run")
        self.Run.setFixedWidth(50)
        self.Run.clicked.connect(self.startRunCommand)
        self.RunChain = QPushButton("Run Chain")
        self.RunChain.setFixedWidth(75)
        self.RunChain.clicked.connect(self.runCommandChain)
        self.layoutH2.addWidget(self.Delete)
        self.layoutH2.addWidget(self.Run)
        self.layoutH2.addWidget(self.RunChain)

        self.main_layout.addLayout(self.layoutH1)
        self.main_layout.addLayout(self.layoutH2)

    def updateRun(self, chain_update:bool=False):
        pass

    def updateTab(self, current_type:int):
        pass
    
    def updateComment(self) -> list[str]:
        start_script_string_comment = f""
        script_string_comment = f"<u><b>{self.summary.node.nodeType.name}: {self.summary.node.nodeID}</b></u><br>"
        end_script_string_comment = f""

        script_string_comment += f"Changes the scene lighting to the <b>'{self.Preset.currentText().lower()}'</b> preset<br>"
        script_string_comment += f"<br>"

        return [start_script_string_comment, script_string_comment, end_script_string_comment]

    def updateCommand(self) -> list[str]:
        super().updateCommand()

        if self.Run.isEnabled():
            self.script_string += f"lighting {self.Preset.currentText().lower()}<br>"
            self.script_string += f"<br>"
        
        return [self.start_script_string, self.script_string, self.end_script_string]    

class AdvancedNodeTransparency(NodeBase):
    def __init__(self, session, summary:AdvancedNodeSummary, title:str="", parent=None):
        super().__init__(session, summary, title, simple_node=False, parent=parent)

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
        if self.summary.used_model != []:
            self.Run.setEnabled(True)
        else:
            self.Run.setEnabled(False)
        if current_run != self.Run.isEnabled():
            if not chain_update:
                self.summary.findLastNode()

    def updateTab(self, current_type:int):
        pass
    
    def updateComment(self) -> list[str]:
        start_script_string_comment = f""
        script_string_comment = f"<u><b>{self.summary.node.nodeType.name}: {self.summary.node.nodeID}</b></u><br>"
        end_script_string_comment = f""

        if self.Run.isEnabled():
            objects = "".join(self.summary.used_model)
            if objects == "All":
                objects = "all models"
            
            script_string_comment += f"Changes <i>'{objects}'</i> transparency:</u><br>"
            script_string_comment += f"   • <u>Surfaces:</u> {self.Surfaces.getText()}% transparent<br>"
            script_string_comment += f"   • <u>Cartoons:</u> {self.Cartoons.getText()}% transparent<br>"
            if int(self.Atoms.getText()) < 100:
                script_string_comment += f"   • <u>Atoms:</u> {self.Atoms.getText()}% transparent with {self.AtomsStyle.currentText().lower()} style<br>"
            else:
                script_string_comment += f"   • <u>Atoms:</u> {self.Atoms.getText()}% transparent<br>"
            script_string_comment += f"<br>"

        return [start_script_string_comment, script_string_comment, end_script_string_comment]

    def updateCommand(self) -> list[str]:
        super().updateCommand()

        if self.Run.isEnabled():
            objects = "".join(self.summary.used_model)
            if objects == "All":
                objects = f"<i>'{objects.lower()}'</i>"
            else:
                objects = f"<i>'{objects}'</i>"

            if int(self.Surfaces.getText()) >= 100 and int(self.Cartoons.getText()) >= 100 and int(self.Atoms.getText()) >= 100:
                self.script_string += f"hide {objects} target scabp<br>"
            else:
                if int(self.Surfaces.getText()) < 100:
                    self.script_string += f"show {objects} target s<br>"
                    self.script_string += f"transparency {objects} {self.Surfaces.getText()} target s<br>"
                else:
                    self.script_string += f"hide {objects} target s<br>"
                if int(self.Cartoons.getText()) < 100:
                    self.script_string += f"show {objects} target c<br>"
                    self.script_string += f"transparency {objects} {self.Cartoons.getText()} target c<br>"
                else:
                    self.script_string += f"hide {objects} target c<br>"
                if int(self.Atoms.getText()) < 100:
                    self.script_string += f"show {objects} target ab<br>"
                    self.script_string += f"style {objects} {self.AtomsStyle.currentText().lower()}<br>"
                    self.script_string += f"transparency {objects} {self.Atoms.getText()}  target ab<br>"
                else:
                    self.script_string += f"hide {objects}  target ab<br>"
                    
            self.script_string += f"<br>"
        
        return [self.start_script_string, self.script_string, self.end_script_string]    

    def updateAtomStyle(self):
        if int(self.Atoms.getText()) >= 100:
            self.AtomsStyle.setEnabled(False)
        else:
            self.AtomsStyle.setEnabled(True)

class AdvancedNode2DLabel(NodeBase):
    def __init__(self, session, summary:AdvancedNodeSummary, title:str="", parent=None):
        super().__init__(session, summary, title, simple_node=False, parent=parent)

        self.font_list = ["Agency FB", "Aharoni", "Algerian", "Arial", "Arial Black", "Arial Narrow", "Arial Rounded MT Bold", "Bahnschrift", "Bahnschrift Condensed", "Bahnschrift Light", 
                          "Bahnschrift Light Condensed", "Bahnschrift Light SemiCondensed", "Bahnschrift SemiBold", "Bahnschrift SemiBold Condensed", "Bahnschrift SemiBold SemiConden", 
                          "Bahnschrift SemiCondensed", "Bahnschrift SemiLight", "Bahnschrift SemiLight Condensed", "Bahnschrift SemiLight SemiConde", "Baskerville Old Face", "Bauhaus 93", 
                          "Bell MT", "Berlin Sans FB", "Berlin Sans FB Demi", "Bernard MT Condensed", "Blackadder ITC", "Bodoni MT", "Bodoni MT Black", "Bodoni MT Condensed", "Bodoni MT Poster Compressed", 
                          "Book Antiqua", "Bookman Old Style", "Bookshelf Symbol 7", "Bradley Hand ITC", "Britannic Bold", "Broadway", "Brush Script MT", "Calibri", "Calibri Light", "Californian FB", "Calisto MT", 
                          "Cambria", "Cambria Math", "Candara", "Candara Light", "Cascadia Code", "Cascadia Code ExtraLight", "Cascadia Code Light", "Cascadia Code SemiBold", "Cascadia Code SemiLight", 
                          "Cascadia Mono", "Cascadia Mono ExtraLight", "Cascadia Mono Light", "Cascadia Mono SemiBold", "Cascadia Mono SemiLight", "Castellar", "Centaur", "Century", "Century Gothic", 
                          "Century Schoolbook", "Chiller", "Colonna MT", "Comic Sans MS", "Consolas", "Constantia", "Cooper Black", "Copperplate Gothic Bold", "Copperplate Gothic Light", "Corbel", "Corbel Light", 
                          "Courier", "Courier New", "Curlz MT", "David", "Dubai", "Dubai Light", "Dubai Medium", "Ebrima", "Edwardian Script ITC", "Elephant", "Engravers MT", "Eras Bold ITC", "Eras Demi ITC", 
                          "Eras Light ITC", "Eras Medium ITC", "Felix Titling", "Fixedsys", "Footlight MT Light", "Forte", "FrankRuehl", "Franklin Gothic Book", "Franklin Gothic Demi", "Franklin Gothic Demi Cond", 
                          "Franklin Gothic Heavy", "Franklin Gothic Medium", "Franklin Gothic Medium Cond", "Freestyle Script", "French Script MT", "Gabriola", "Gadugi", "Garamond", "Georgia", "Gigi", 
                          "Gill Sans MT", "Gill Sans MT Condensed", "Gill Sans MT Ext Condensed Bold", "Gill Sans Ultra Bold", "Gill Sans Ultra Bold Condensed", "Gisha", "Gloucester MT Extra Condensed", 
                          "Goudy Old Style", "Goudy Stout", "Guttman Aharoni", "Guttman Drogolin", "Guttman Frank", "Guttman Frnew", "Guttman Haim", "Guttman Haim-Condensed", "Guttman Hatzvi", "Guttman Kav", 
                          "Guttman Kav-Light", "Guttman Logo1", "Guttman Mantova", "Guttman Mantova-Decor", "Guttman Miryam", "Guttman Myamfix", "Guttman Rashi", "Guttman Stam", "Guttman Stam1", "Guttman Vilna", 
                          "Guttman Yad", "Guttman Yad-Brush", "Guttman Yad-Light", "Guttman-Aharoni", "Guttman-Aram", "Guttman-CourMir", "Hadassah Friedlaender", "Haettenschweiler", "Harlow Solid Italic", 
                          "Harrington", "High Tower Text", "HoloLens MDL2 Assets", "Impact", "Imprint MT Shadow", "Informal Roman", "Ink Free", "Javanese Text", "Jokerman", "Juice ITC", "Kristen ITC", 
                          "Kunstler Script", "Leelawadee", "Leelawadee UI", "Leelawadee UI Semilight", "Levenim MT", "Lucida Bright", "Lucida Calligraphy", "Lucida Console", "Lucida Fax", "Lucida Handwriting", 
                          "Lucida Sans", "Lucida Sans Typewriter", "Lucida Sans Unicode", "MS Gothic", "MS Outlook", "MS PGothic", "MS Reference Sans Serif", "MS Reference Specialty", "MS Sans Serif", "MS Serif", 
                          "MS UI Gothic", "MT Extra", "MV Boli", "Magneto", "Maiandra GD", "Malgun Gothic", "Malgun Gothic Semilight", "Marlett", "Matura MT Script Capitals", "Microsoft Himalaya", 
                          "Microsoft JhengHei", "Microsoft JhengHei Light", "Microsoft JhengHei UI", "Microsoft JhengHei UI Light", "Microsoft New Tai Lue", "Microsoft PhagsPa", "Microsoft Sans Serif", 
                          "Microsoft Tai Le", "Microsoft Uighur", "Microsoft YaHei", "Microsoft YaHei Light", "Microsoft YaHei UI", "Microsoft YaHei UI Light", "Microsoft Yi Baiti", "MingLiU-ExtB", 
                          "MingLiU_HKSCS-ExtB", "Miriam", "Miriam Fixed", "Mistral", "Modern", "Modern No. 20", "Mongolian Baiti", "Monotype Corsiva", "Myanmar Text", "NSimSun", "Narkisim", "Niagara Engraved", 
                          "Niagara Solid", "Nirmala UI", "Nirmala UI Semilight", "OCR A Extended", "Old English Text MT", "Onyx", "PMingLiU-ExtB", "Palace Script MT", "Palatino Linotype", "Papyrus", "Parchment", 
                          "Perpetua", "Perpetua Titling MT", "Playbill", "Poor Richard", "Pristina", "Rage Italic", "Ravie", "Rockwell", "Rockwell Condensed", "Rockwell Extra Bold", "Rod", "Roman", 
                          "Sans Serif Collection", "Script", "Script MT Bold", "Segoe Fluent Icons", "Segoe MDL2 Assets", "Segoe Print", "Segoe Script", "Segoe UI", "Segoe UI Black", "Segoe UI Emoji", 
                          "Segoe UI Historic", "Segoe UI Light", "Segoe UI Semibold", "Segoe UI Semilight", "Segoe UI Symbol", "Segoe UI Variable", "Segoe UI Variable Display", "Segoe UI Variable Display Light", 
                          "Segoe UI Variable Display Semib", "Segoe UI Variable Display Semil", "Segoe UI Variable Small", "Segoe UI Variable Small Light", "Segoe UI Variable Small Semibol", 
                          "Segoe UI Variable Small Semilig", "Segoe UI Variable Text", "Segoe UI Variable Text Light", "Segoe UI Variable Text Semibold", "Segoe UI Variable Text Semiligh", "Showcard Gothic", 
                          "SimSun", "SimSun-ExtB", "Sitka", "Sitka Banner", "Sitka Banner Semibold", "Sitka Display", "Sitka Display Semibold", "Sitka Heading", "Sitka Heading Semibold", "Sitka Small", 
                          "Sitka Small Semibold", "Sitka Subheading", "Sitka Subheading Semibold", "Sitka Text", "Sitka Text Semibold", "Small Fonts", "Snap ITC", "Stencil", "Sylfaen", "Symbol", "System", 
                          "Tahoma", "Tempus Sans ITC", "Terminal", "Times New Roman", "Trebuchet MS", "Tw Cen MT", "Tw Cen MT Condensed", "Tw Cen MT Condensed Extra Bold", "Verdana", "Viner Hand ITC", "Vivaldi", 
                          "Vladimir Script", "Webdings", "Wide Latin", "Wingdings", "Wingdings 2", "Wingdings 3", "Yu Gothic", "Yu Gothic Light", "Yu Gothic Medium", "Yu Gothic UI", "Yu Gothic UI Light", 
                          "Yu Gothic UI Semibold", "Yu Gothic UI Semilight"]
       
        self.initUI()

    def initUI(self):
        self.main_layout = QVBoxLayout()
        self.main_layout.setSpacing(5)
        self.main_layout.setContentsMargins(10, 10, 10, 10)
        self.setLayout(self.main_layout)
 
        self.TextColorPicked = None
        self.BackgroundColorPicked = None

        self.layoutH1 = QHBoxLayout()
        self.lText = QLabel("Text")
        self.Text = QLineEdit()
        self.Text.textChanged.connect(self.internal_updateRun)
        self.layoutH1.addWidget(self.lText)
        self.layoutH1.addWidget(self.Text)

        self.layoutH2 = QHBoxLayout()
        self.TextColor = QPushButton("Text Color")    
        self.TextColor.clicked.connect(self.openTextColorDialog)
        self.TextColorDialog = QColorDialog()
        self.TextColorLabel = QLabel()   
        self.TextColorLabel.setFixedWidth(50)
        self.TextColorLabel.setFixedHeight(50)
        self.TextColorLabel.setStyleSheet("QLabel { border: 1px solid black }")
        self.BackgroundColor = QPushButton("Background Color")    
        self.BackgroundColor.clicked.connect(self.openBackgroundColorDialog)
        self.BackgroundColorDialog = QColorDialog()
        self.BackgroundColorLabel = QLabel()   
        self.BackgroundColorLabel.setFixedWidth(50)
        self.BackgroundColorLabel.setFixedHeight(50)   
        self.BackgroundColorLabel.setStyleSheet("QLabel { border: 1px solid black }")
        self.layoutH2.addWidget(self.TextColor)
        self.layoutH2.addWidget(self.TextColorLabel)
        self.layoutH2.addWidget(self.BackgroundColor)
        self.layoutH2.addWidget(self.BackgroundColorLabel)
        
        self.X = QNumEdit(min=0, max=1, step=1, decimals=2, addSlider=True, label="X Pos")
        self.X.setText("0.5")

        self.Y = QNumEdit(min=0, max=1, step=1, decimals=2, addSlider=True, label="Y Pos")
        self.Y.setText("0.5")

        self.layoutH3 = QHBoxLayout()
        self.Size = QNumEdit(min=0, max=100, step=1, decimals=0, addSlider=False, label="Size")
        self.Size.setText("24")
        self.Outline = QNumEdit(min=0, max=None, step=1, decimals=0, addSlider=False, label="Outline Width")
        self.Outline.setText("0")
        self.Margin = QNumEdit(min=0, max=100, step=1, decimals=0, addSlider=False, label="Margin")
        self.Margin.setText("9")
        self.layoutH3.addLayout(self.Size.widget_layout)
        self.layoutH3.addLayout(self.Outline.widget_layout)
        self.layoutH3.addLayout(self.Margin.widget_layout)

        self.layoutH4 = QHBoxLayout()
        self.layoutH4V1 = QVBoxLayout()
        self.lFont = QLabel("Font")
        self.Font = QComboBox()
        self.Font.addItems(self.font_list)
        self.Font.setCurrentIndex(3)
        self.Font.setStyleSheet("combobox-popup: 0;")
        self.Font.view().setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.Font.setFixedWidth(100)
        self.layoutH4V1.addWidget(self.lFont, alignment=Qt.AlignmentFlag.AlignHCenter)
        self.layoutH4V1.addWidget(self.Font, alignment=Qt.AlignmentFlag.AlignHCenter)
        self.layoutH4V2 = QVBoxLayout()
        self.lBold = QLabel("Bold")
        self.Bold = QSwitchControl(self.summary.node.scene.parent)
        self.summary.node.scene.parent.switches.append(self.Bold)
        self.layoutH4V2.addWidget(self.lBold, alignment=Qt.AlignmentFlag.AlignHCenter)
        self.layoutH4V2.addWidget(self.Bold, alignment=Qt.AlignmentFlag.AlignHCenter)
        self.layoutH4V3 = QVBoxLayout()
        self.lItalic = QLabel("Italic")
        self.Italic = QSwitchControl(self.summary.node.scene.parent)
        self.summary.node.scene.parent.switches.append(self.lItalic)
        self.layoutH4V3.addWidget(self.lItalic, alignment=Qt.AlignmentFlag.AlignHCenter)
        self.layoutH4V3.addWidget(self.Italic, alignment=Qt.AlignmentFlag.AlignHCenter)
        self.layoutH4V4 = QVBoxLayout()
        self.lVisibility = QLabel("Visibility")
        self.Visibility = QSwitchControl(self.summary.node.scene.parent)
        self.summary.node.scene.parent.switches.append(self.Visibility)
        self.Visibility.setChecked(True)
        self.layoutH4V4.addWidget(self.lVisibility, alignment=Qt.AlignmentFlag.AlignHCenter)
        self.layoutH4V4.addWidget(self.Visibility, alignment=Qt.AlignmentFlag.AlignHCenter)
        self.layoutH4.addLayout(self.layoutH4V1)
        self.layoutH4.addLayout(self.layoutH4V2)
        self.layoutH4.addLayout(self.layoutH4V3)
        self.layoutH4.addLayout(self.layoutH4V4)

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
        self.main_layout.addLayout(self.layoutH2)
        self.main_layout.addLayout(self.X.widget_layout)
        self.main_layout.addLayout(self.Y.widget_layout)
        self.main_layout.addLayout(self.layoutH3)
        self.main_layout.addLayout(self.layoutH4)
        self.main_layout.addLayout(self.layoutH5)

    def updateRun(self, chain_update:bool=False):
        current_run = self.Run.isEnabled()
        if self.Text.text() != "" and self.TextColorPicked is not None:
            self.Run.setEnabled(True)
        else:
            self.Run.setEnabled(False)
        if current_run != self.Run.isEnabled():
            if not chain_update:
                self.summary.findLastNode()

    def updateTab(self, current_type:int):
        pass
    
    def updateComment(self) -> list[str]:
        start_script_string_comment = f""
        script_string_comment = f"<u><b>{self.summary.node.nodeType.name}: {self.summary.node.nodeID}</b></u><br>"
        end_script_string_comment = f""

        if self.Run.isEnabled():

            if self.Bold.isChecked():
                bold = f"<u>Bold</u>: <b>True</b>"
            else:
                bold = f"<u>Bold</u>: False"
            if self.Italic.isChecked():
                italic = f"<u>Italic</u>: <i>True</i>"
            else:
                italic = f"<u>Italic</u>: False"

            script_string_comment += f"Adds a 2D label:<br>"
            script_string_comment += f"   • <u>Text:</u> \"{self.Text.text()}\"<br>"
            script_string_comment += f"   • <u>Text color:</u> <a style='background-color:{self.TextColorPicked.name()};'>{self.TextColorPicked.name()}</a><br>"
            if self.BackgroundColorPicked is not None:
                script_string_comment += f"   • <u>Background color:</u> <a style='background-color:{self.BackgroundColorPicked.name()};'>{self.BackgroundColorPicked.name()}</a><br>"
            else:
                script_string_comment += f"   • <u>Background color:</u> Transparent<br>"
            script_string_comment += f"   • <u>Margin:</u> {self.Margin.getText()}, <u>Outline</u>: {self.Outline.getText()})<br>"
            script_string_comment += f"   • <u>Position:</u> ({self.X.getText()}, {self.Y.getText()})<br>"
            script_string_comment += f"   • <u>Font:</u> \"{self.Font.currentText()}\", <u>Size</u>: {self.Size.getText()}, {bold}, {italic}<br>"
            script_string_comment += f"   • <u>Visible:</u> {self.Visibility.isChecked()}<br>"
            script_string_comment += f"<br>"

        return [start_script_string_comment, script_string_comment, end_script_string_comment]

    def updateCommand(self) -> list[str]:
        super().updateCommand()

        if self.Run.isEnabled():
            text = f"text \"{self.Text.text()}\""
            if self.TextColorPicked != None:
                text_color = f"color {self.TextColorPicked.name()}"
            else:
                text_color = f"color default"
            if self.BackgroundColorPicked != None:
                bg_color = f"bgColor {self.BackgroundColorPicked.name()}"
            else:
                bg_color = f""
            margin = f"margin {self.Margin.getText()}"
            outline = f"outline {self.Outline.getText()}"
            size = f"size {self.Size.getText()}"
            xpos = f"x {self.X.getText()}"
            ypos = f"y {self.Y.getText()}"
            font = f"font \"{self.Font.currentText()}\""
            bold = f"bold {self.Bold.isChecked()}"
            italic = f"italic {self.Italic.isChecked()}"
            visibility = f"visibility {self.Visibility.isChecked()}"
            
            self.script_string += f"2dlabel {text} {text_color} {bg_color} {margin} {outline} {size} {xpos} {ypos} {font} {bold} {italic} {visibility}<br>"
            self.script_string += f"<br>"
        
        return [self.start_script_string, self.script_string, self.end_script_string]    

    def openTextColorDialog(self):
        self.TextColorPicked = self.TextColorDialog.getColor()
        self.TextColorLabel.setStyleSheet(f"QLabel {{ background-color : rgb({self.TextColorPicked.getRgb()[0]},{self.TextColorPicked.getRgb()[1]},{self.TextColorPicked.getRgb()[2]}); border: 1px solid black}}")
        self.internal_updateRun()

    def updateTextColor(self):
        self.TextColorLabel.setStyleSheet(f"QLabel {{ background-color : rgb({self.TextColorPicked.getRgb()[0]},{self.TextColorPicked.getRgb()[1]},{self.TextColorPicked.getRgb()[2]}); border: 1px solid black}}")
        
    def openBackgroundColorDialog(self):
        self.BackgroundColorPicked = self.BackgroundColorDialog.getColor()
        self.BackgroundColorLabel.setStyleSheet(f"QLabel {{ background-color : rgb({self.BackgroundColorPicked.getRgb()[0]},{self.BackgroundColorPicked.getRgb()[1]},{self.BackgroundColorPicked.getRgb()[2]}); border: 1px solid black}}")
        
    def updateBackgroundColor(self):
        self.BackgroundColorLabel.setStyleSheet(f"QLabel {{ background-color : rgb({self.BackgroundColorPicked.getRgb()[0]},{self.BackgroundColorPicked.getRgb()[1]},{self.BackgroundColorPicked.getRgb()[2]}); border: 1px solid black}}")
        
class AdvancedNode3DLabel(NodeBase):
    def __init__(self, session, summary:AdvancedNodeSummary, title:str="", parent=None):
        super().__init__(session, summary, title, simple_node=False, parent=parent)

        self.font_list = ["Agency FB", "Aharoni", "Algerian", "Arial", "Arial Black", "Arial Narrow", "Arial Rounded MT Bold", "Bahnschrift", "Bahnschrift Condensed", "Bahnschrift Light", 
                          "Bahnschrift Light Condensed", "Bahnschrift Light SemiCondensed", "Bahnschrift SemiBold", "Bahnschrift SemiBold Condensed", "Bahnschrift SemiBold SemiConden", 
                          "Bahnschrift SemiCondensed", "Bahnschrift SemiLight", "Bahnschrift SemiLight Condensed", "Bahnschrift SemiLight SemiConde", "Baskerville Old Face", "Bauhaus 93", 
                          "Bell MT", "Berlin Sans FB", "Berlin Sans FB Demi", "Bernard MT Condensed", "Blackadder ITC", "Bodoni MT", "Bodoni MT Black", "Bodoni MT Condensed", "Bodoni MT Poster Compressed", 
                          "Book Antiqua", "Bookman Old Style", "Bookshelf Symbol 7", "Bradley Hand ITC", "Britannic Bold", "Broadway", "Brush Script MT", "Calibri", "Calibri Light", "Californian FB", "Calisto MT", 
                          "Cambria", "Cambria Math", "Candara", "Candara Light", "Cascadia Code", "Cascadia Code ExtraLight", "Cascadia Code Light", "Cascadia Code SemiBold", "Cascadia Code SemiLight", 
                          "Cascadia Mono", "Cascadia Mono ExtraLight", "Cascadia Mono Light", "Cascadia Mono SemiBold", "Cascadia Mono SemiLight", "Castellar", "Centaur", "Century", "Century Gothic", 
                          "Century Schoolbook", "Chiller", "Colonna MT", "Comic Sans MS", "Consolas", "Constantia", "Cooper Black", "Copperplate Gothic Bold", "Copperplate Gothic Light", "Corbel", "Corbel Light", 
                          "Courier", "Courier New", "Curlz MT", "David", "Dubai", "Dubai Light", "Dubai Medium", "Ebrima", "Edwardian Script ITC", "Elephant", "Engravers MT", "Eras Bold ITC", "Eras Demi ITC", 
                          "Eras Light ITC", "Eras Medium ITC", "Felix Titling", "Fixedsys", "Footlight MT Light", "Forte", "FrankRuehl", "Franklin Gothic Book", "Franklin Gothic Demi", "Franklin Gothic Demi Cond", 
                          "Franklin Gothic Heavy", "Franklin Gothic Medium", "Franklin Gothic Medium Cond", "Freestyle Script", "French Script MT", "Gabriola", "Gadugi", "Garamond", "Georgia", "Gigi", 
                          "Gill Sans MT", "Gill Sans MT Condensed", "Gill Sans MT Ext Condensed Bold", "Gill Sans Ultra Bold", "Gill Sans Ultra Bold Condensed", "Gisha", "Gloucester MT Extra Condensed", 
                          "Goudy Old Style", "Goudy Stout", "Guttman Aharoni", "Guttman Drogolin", "Guttman Frank", "Guttman Frnew", "Guttman Haim", "Guttman Haim-Condensed", "Guttman Hatzvi", "Guttman Kav", 
                          "Guttman Kav-Light", "Guttman Logo1", "Guttman Mantova", "Guttman Mantova-Decor", "Guttman Miryam", "Guttman Myamfix", "Guttman Rashi", "Guttman Stam", "Guttman Stam1", "Guttman Vilna", 
                          "Guttman Yad", "Guttman Yad-Brush", "Guttman Yad-Light", "Guttman-Aharoni", "Guttman-Aram", "Guttman-CourMir", "Hadassah Friedlaender", "Haettenschweiler", "Harlow Solid Italic", 
                          "Harrington", "High Tower Text", "HoloLens MDL2 Assets", "Impact", "Imprint MT Shadow", "Informal Roman", "Ink Free", "Javanese Text", "Jokerman", "Juice ITC", "Kristen ITC", 
                          "Kunstler Script", "Leelawadee", "Leelawadee UI", "Leelawadee UI Semilight", "Levenim MT", "Lucida Bright", "Lucida Calligraphy", "Lucida Console", "Lucida Fax", "Lucida Handwriting", 
                          "Lucida Sans", "Lucida Sans Typewriter", "Lucida Sans Unicode", "MS Gothic", "MS Outlook", "MS PGothic", "MS Reference Sans Serif", "MS Reference Specialty", "MS Sans Serif", "MS Serif", 
                          "MS UI Gothic", "MT Extra", "MV Boli", "Magneto", "Maiandra GD", "Malgun Gothic", "Malgun Gothic Semilight", "Marlett", "Matura MT Script Capitals", "Microsoft Himalaya", 
                          "Microsoft JhengHei", "Microsoft JhengHei Light", "Microsoft JhengHei UI", "Microsoft JhengHei UI Light", "Microsoft New Tai Lue", "Microsoft PhagsPa", "Microsoft Sans Serif", 
                          "Microsoft Tai Le", "Microsoft Uighur", "Microsoft YaHei", "Microsoft YaHei Light", "Microsoft YaHei UI", "Microsoft YaHei UI Light", "Microsoft Yi Baiti", "MingLiU-ExtB", 
                          "MingLiU_HKSCS-ExtB", "Miriam", "Miriam Fixed", "Mistral", "Modern", "Modern No. 20", "Mongolian Baiti", "Monotype Corsiva", "Myanmar Text", "NSimSun", "Narkisim", "Niagara Engraved", 
                          "Niagara Solid", "Nirmala UI", "Nirmala UI Semilight", "OCR A Extended", "Old English Text MT", "Onyx", "PMingLiU-ExtB", "Palace Script MT", "Palatino Linotype", "Papyrus", "Parchment", 
                          "Perpetua", "Perpetua Titling MT", "Playbill", "Poor Richard", "Pristina", "Rage Italic", "Ravie", "Rockwell", "Rockwell Condensed", "Rockwell Extra Bold", "Rod", "Roman", 
                          "Sans Serif Collection", "Script", "Script MT Bold", "Segoe Fluent Icons", "Segoe MDL2 Assets", "Segoe Print", "Segoe Script", "Segoe UI", "Segoe UI Black", "Segoe UI Emoji", 
                          "Segoe UI Historic", "Segoe UI Light", "Segoe UI Semibold", "Segoe UI Semilight", "Segoe UI Symbol", "Segoe UI Variable", "Segoe UI Variable Display", "Segoe UI Variable Display Light", 
                          "Segoe UI Variable Display Semib", "Segoe UI Variable Display Semil", "Segoe UI Variable Small", "Segoe UI Variable Small Light", "Segoe UI Variable Small Semibol", 
                          "Segoe UI Variable Small Semilig", "Segoe UI Variable Text", "Segoe UI Variable Text Light", "Segoe UI Variable Text Semibold", "Segoe UI Variable Text Semiligh", "Showcard Gothic", 
                          "SimSun", "SimSun-ExtB", "Sitka", "Sitka Banner", "Sitka Banner Semibold", "Sitka Display", "Sitka Display Semibold", "Sitka Heading", "Sitka Heading Semibold", "Sitka Small", 
                          "Sitka Small Semibold", "Sitka Subheading", "Sitka Subheading Semibold", "Sitka Text", "Sitka Text Semibold", "Small Fonts", "Snap ITC", "Stencil", "Sylfaen", "Symbol", "System", 
                          "Tahoma", "Tempus Sans ITC", "Terminal", "Times New Roman", "Trebuchet MS", "Tw Cen MT", "Tw Cen MT Condensed", "Tw Cen MT Condensed Extra Bold", "Verdana", "Viner Hand ITC", "Vivaldi", 
                          "Vladimir Script", "Webdings", "Wide Latin", "Wingdings", "Wingdings 2", "Wingdings 3", "Yu Gothic", "Yu Gothic Light", "Yu Gothic Medium", "Yu Gothic UI", "Yu Gothic UI Light", 
                          "Yu Gothic UI Semibold", "Yu Gothic UI Semilight"]
        self.initUI()

    def initUI(self):
        self.main_layout = QVBoxLayout()
        self.main_layout.setSpacing(5)
        self.main_layout.setContentsMargins(10, 10, 10, 10)
        self.setLayout(self.main_layout)

        self.TextColorPicked = None
        self.BackgroundColorPicked = None

        self.layoutH1 = QHBoxLayout()
        self.lText = QLabel("Text")
        self.Text = QLineEdit()
        self.layoutH1.addWidget(self.lText)
        self.layoutH1.addWidget(self.Text)

        self.layoutH2 = QHBoxLayout()
        self.TextColor = QPushButton("Text Color")    
        self.TextColor.clicked.connect(self.openTextColorDialog)
        self.TextColorDialog = QColorDialog()
        self.TextColorLabel = QLabel()   
        self.TextColorLabel.setFixedWidth(50)
        self.TextColorLabel.setFixedHeight(50)
        self.TextColorLabel.setStyleSheet("QLabel { border: 1px solid black }")
        self.BackgroundColor = QPushButton("Background Color")    
        self.BackgroundColor.clicked.connect(self.openBackgroundColorDialog)
        self.BackgroundColorDialog = QColorDialog()
        self.BackgroundColorLabel = QLabel()   
        self.BackgroundColorLabel.setFixedWidth(50)
        self.BackgroundColorLabel.setFixedHeight(50)   
        self.BackgroundColorLabel.setStyleSheet("QLabel { border: 1px solid black }")
        self.layoutH2.addWidget(self.TextColor)
        self.layoutH2.addWidget(self.TextColorLabel)
        self.layoutH2.addWidget(self.BackgroundColor)
        self.layoutH2.addWidget(self.BackgroundColorLabel)
        
        self.layoutH3 = QHBoxLayout()
        self.lStructure = QLabel("Structure")
        self.Structure = QComboBox()
        self.Structure.addItems(["atoms", "bonds", "models", "residues"])
        self.Structure.setCurrentIndex(2)
        self.layoutH3.addWidget(self.lStructure, alignment=Qt.AlignmentFlag.AlignCenter)
        self.layoutH3.addWidget(self.Structure, alignment=Qt.AlignmentFlag.AlignLeft)
        
        self.layoutH4 = QHBoxLayout()
        self.Height = QComboBox()
        self.Height.addItems(["Fixed", "Custom"])
        self.Height.currentIndexChanged.connect(self.updateHeight)
        self.Height.setFixedWidth(75)
        self.HeightValue = QNumEdit(min=None, max=None, step=1, decimals=0, addSlider=False, label="Height")
        self.Size = QNumEdit(min=0, max=100, step=1, decimals=0, addSlider=False, label="Size")
        self.Size.setText("20")
        self.layoutH4.addWidget(self.Height, alignment=Qt.AlignmentFlag.AlignCenter)
        self.layoutH4.addLayout(self.HeightValue.widget_layout)
        self.layoutH4.addLayout(self.Size.widget_layout)

        self.layoutH5 = QHBoxLayout()
        self.OffsetX = QNumEdit(min=None, max=None, step=1, decimals=0, addSlider=False, label="Offset X")
        self.OffsetX.setText("0")
        self.OffsetY = QNumEdit(min=None, max=None, step=1, decimals=0, addSlider=False, label="Offset Y")
        self.OffsetY.setText("0")
        self.OffsetZ = QNumEdit(min=None, max=None, step=1, decimals=0, addSlider=False, label="Offset Z")
        self.OffsetZ.setText("0")
        self.layoutH5.addLayout(self.OffsetX.widget_layout)
        self.layoutH5.addLayout(self.OffsetY.widget_layout)
        self.layoutH5.addLayout(self.OffsetZ.widget_layout)
        
        self.layoutH6 = QHBoxLayout()
        self.layoutH6V1 = QVBoxLayout()
        self.lFont = QLabel("Font")
        self.Font = QComboBox()
        self.Font.addItems(self.font_list)
        self.Font.setCurrentIndex(3)
        self.Font.setStyleSheet("combobox-popup: 0;")
        self.Font.view().setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.layoutH6V1.addWidget(self.lFont)
        self.layoutH6V1.addWidget(self.Font)
        self.layoutH6V2 = QVBoxLayout()
        self.lOnTop = QLabel("On Top")
        self.OnTop = QSwitchControl(self.summary.node.scene.parent)
        self.summary.node.scene.parent.switches.append(self.OnTop)
        self.layoutH6V2.addWidget(self.lOnTop)
        self.layoutH6V2.addWidget(self.OnTop)
        self.layoutH6.addLayout(self.layoutH6V1)
        self.layoutH6.addLayout(self.layoutH6V2)

        self.layoutH7 = QHBoxLayout()
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
        self.layoutH7.addWidget(self.Delete)
        self.layoutH7.addWidget(self.Run)
        self.layoutH7.addWidget(self.RunChain)

        self.main_layout.addLayout(self.layoutH1)
        self.main_layout.addLayout(self.layoutH2)
        self.main_layout.addLayout(self.layoutH3)
        self.main_layout.addLayout(self.layoutH4)
        self.main_layout.addLayout(self.layoutH5)
        self.main_layout.addLayout(self.layoutH6)
        self.main_layout.addLayout(self.layoutH7)
    
    def updateHeight(self):
        if self.Height.currentText() == "Fixed":
            self.HeightValue.setEnabled(False)
        elif self.Height.currentText() == "Custom":
            self.HeightValue.setEnabled(True)
            

    def updateRun(self, chain_update:bool=False):
        current_run = self.Run.isEnabled()
        if self.summary.used_model != [] and self.Text.text() != "" and self.TextColorPicked is not None:
            self.Run.setEnabled(True)
        else:
            self.Run.setEnabled(False)
        if current_run != self.Run.isEnabled():
            if not chain_update:
                self.summary.findLastNode()

    def updateTab(self, current_type:int):
        pass
    
    def updateComment(self) -> list[str]:
        start_script_string_comment = f""
        script_string_comment = f"<u><b>{self.summary.node.nodeType.name}: {self.summary.node.nodeID}</b></u><br>"
        end_script_string_comment = f""

        if self.Run.isEnabled():
            objects = "".join(self.summary.used_model)
            if objects == "All":
                objects = "all models"

            if self.Text.text() == "":
                label = f"{self.Structure.currentText().lower()}"
            else:
                label = f"text \"{self.Text.text()}\""
            if self.Height.currentText() == "Fixed":
                height = f"Fixed"
            elif self.Height.currentText() == "Custom":
                height = f"height {self.HeightValue.getText()}"

            script_string_comment += f"Adds a 3D label to <i>'{objects}'</i>:<br>"
            script_string_comment += f"   • <u>Text:</u> {label}<br>"
            script_string_comment += f"   • <u>Text color:</u> <a style='background-color:{self.TextColorPicked.name()};'>{self.TextColorPicked.name()}</a><br>"
            if self.BackgroundColorPicked is not None:
                script_string_comment += f"   • <u>Background color:</u> <a style='background-color:{self.BackgroundColorPicked.name()};'>{self.BackgroundColorPicked.name()}</a><br>"
            else:
                script_string_comment += f"   • <u>Background color:</u> Transparent<br>"
            script_string_comment += f"   • <u>Height:</u> {height}<br>"
            script_string_comment += f"   • <u>Offset:</u> ({self.OffsetX.getText()}, {self.OffsetY.getText()} {self.OffsetZ.getText()})<br>"
            script_string_comment += f"   • <u>Font:</u> \"{self.Font.currentText()}\"; <u>Size:</u> {self.Size.getText()}<br>"
            script_string_comment += f"   • <u>On Top:</u> {self.OnTop.isChecked()}<br>"
            script_string_comment += f"<br>"

        return [start_script_string_comment, script_string_comment, end_script_string_comment]

    def updateCommand(self) -> list[str]:
        super().updateCommand()

        if self.Run.isEnabled():
            objects = "".join(self.summary.used_model)
            if objects == "All":
                objects = f"<i>'{objects.lower()}'</i>"
            else:
                objects = f"<i>'{objects}'</i>"

            if self.Text.text() == "":
                label = f"{self.Structure.currentText().lower()}"
            else:
                label = f"text \"{self.Text.text()}\""
            if self.TextColorPicked != None:
                text_color = f"color {self.TextColorPicked.name()}"
            else:
                text_color = f""
            if self.BackgroundColorPicked != None:
                bg_color = f"bgColor {self.BackgroundColorPicked.name()}"
            else:
                bg_color = f""
            if self.Height.currentText() == "Fixed":
                height = f"height fixed"
            elif self.Height.currentText() == "Custom":
                height = f"height {self.HeightValue.getText()}"
                self.HeightValue.setEnabled(True)
            self.script_string += f"label {objects} {label} {text_color} {bg_color} {height} size {self.Size.getText()} font \"{self.Font.currentText()}\" offset {self.OffsetX.getText()},{self.OffsetY.getText()},{self.OffsetZ.getText()} onTop {self.OnTop.isChecked()}<br>"
            self.script_string += f"<br>"
        
        return [self.start_script_string, self.script_string, self.end_script_string]    

    def openTextColorDialog(self):
        self.TextColorPicked = self.TextColorDialog.getColor()
        self.TextColorLabel.setStyleSheet(f"QLabel {{ background-color : rgb({self.TextColorPicked.getRgb()[0]},{self.TextColorPicked.getRgb()[1]},{self.TextColorPicked.getRgb()[2]}); border: 1px solid black}}")
        self.internal_updateRun()
        
    def updateTextColor(self):
        self.TextColorLabel.setStyleSheet(f"QLabel {{ background-color : rgb({self.TextColorPicked.getRgb()[0]},{self.TextColorPicked.getRgb()[1]},{self.TextColorPicked.getRgb()[2]}); border: 1px solid black}}")
        
    def openBackgroundColorDialog(self):
        self.BackgroundColorPicked = self.BackgroundColorDialog.getColor()
        self.BackgroundColorLabel.setStyleSheet(f"QLabel {{ background-color : rgb({self.BackgroundColorPicked.getRgb()[0]},{self.BackgroundColorPicked.getRgb()[1]},{self.BackgroundColorPicked.getRgb()[2]}); border: 1px solid black}}")
        
    def updateBackgroundColor(self):
        self.BackgroundColorLabel.setStyleSheet(f"QLabel {{ background-color : rgb({self.BackgroundColorPicked.getRgb()[0]},{self.BackgroundColorPicked.getRgb()[1]},{self.BackgroundColorPicked.getRgb()[2]}); border: 1px solid black}}")
        
class AdvancedNodeMovement(NodeBase):
    def __init__(self, session, summary:AdvancedNodeSummary, title:str="", parent=None):
        super().__init__(session, summary, title, simple_node=False, parent=parent)

        self.initUI()

    def initUI(self):
        self.main_layout = QVBoxLayout()
        self.main_layout.setSpacing(5)
        self.main_layout.setContentsMargins(10, 10, 10, 10)
        self.setLayout(self.main_layout)

        self.layoutH1 = QHBoxLayout()
        self.lCofr = QLabel("Move to center of rotation")
        self.Cofr = QSwitchControl(self.summary.node.scene.parent)
        self.summary.node.scene.parent.switches.append(self.Cofr)
        self.Cofr.stateChanged.connect(self.updateMove)
        self.layoutH1.addWidget(self.lCofr)
        self.layoutH1.addWidget(self.Cofr)

        self.layoutH2 = QHBoxLayout()
        self.layoutH2.setSpacing(4)
        self.MoveX = QNumEdit(min=None, max=None, step=1, decimals=0, addSlider=False, label="X")
        self.MoveX.setText("0")
        self.MoveY = QNumEdit(min=None, max=None, step=1, decimals=0, addSlider=False, label="Y")
        self.MoveY.setText("0")
        self.MoveZ = QNumEdit(min=None, max=None, step=1, decimals=0, addSlider=False, label="Z")
        self.MoveZ.setText("0")
        self.layoutH2.addLayout(self.MoveX.widget_layout)
        self.layoutH2.addLayout(self.MoveY.widget_layout)
        self.layoutH2.addLayout(self.MoveZ.widget_layout)

        self.layoutH3 = QHBoxLayout()
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
        self.layoutH3.addWidget(self.Delete)
        self.layoutH3.addWidget(self.Run)
        self.layoutH3.addWidget(self.RunChain)

        self.main_layout.addLayout(self.layoutH1)
        self.main_layout.addLayout(self.layoutH2)
        self.main_layout.addLayout(self.layoutH3)
    
    def updateRun(self, chain_update:bool=False):
        current_run = self.Run.isEnabled()
        if self.summary.used_model != []:
            self.Run.setEnabled(True)
        else:
            self.Run.setEnabled(False)
        if current_run != self.Run.isEnabled():
            if not chain_update:
                self.summary.findLastNode()

    def updateTab(self, current_type:int):
        pass
    
    def updateComment(self) -> list[str]:
        start_script_string_comment = f""
        script_string_comment = f"<u><b>{self.summary.node.nodeType.name}: {self.summary.node.nodeID}</b></u><br>"
        end_script_string_comment = f""

        if self.Run.isEnabled():
            objects = "".join(self.summary.used_model)
            if objects == "All":
                objects = "all models"

            if self.Cofr.isChecked():
                script_string_comment += f"Moves <i>'{objects}'</i> to the center of rotation<br>"
            else:
                script_string_comment += f"Moves <i>'{objects}'</i> by:<br>"
                script_string_comment += f"   • <u>X:</u> {self.MoveX.getText()}<br>"
                script_string_comment += f"   • <u>Y:</u> {self.MoveY.getText()}<br>"
                script_string_comment += f"   • <u>Z:</u> {self.MoveZ.getText()}<br>"
            script_string_comment += f"<br>"

        return [start_script_string_comment, script_string_comment, end_script_string_comment]

    def updateCommand(self) -> list[str]:
        super().updateCommand()

        if self.Run.isEnabled():
            objects = "".join(self.summary.used_model)
            if objects == "All":
                objects = f"<i>'{objects.lower()}'</i>"
            else:
                objects = f"<i>'{objects}'</i>"

            if self.Cofr.isChecked():
                self.script_string += f"move cofr {objects}<br>"
            else:
                self.script_string += f"move {self.MoveX.getText()},{self.MoveY.getText()},{self.MoveZ.getText()} atoms {objects}<br>"
            self.script_string += f"<br>"
        
        return [self.start_script_string, self.script_string, self.end_script_string]    

    def updateMove(self):
        if self.Cofr.isChecked():
            self.MoveX.setEnabled(False)
            self.MoveY.setEnabled(False)
            self.MoveZ.setEnabled(False)
        else:
            self.MoveX.setEnabled(True)
            self.MoveY.setEnabled(True)
            self.MoveZ.setEnabled(True)

class AdvancedNodeRotation(NodeBase):
    def __init__(self, session, summary:AdvancedNodeSummary, title:str="", parent=None):
        super().__init__(session, summary, title, simple_node=False, parent=parent)

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
        self.lRelativeAxis = QLabel("Use Relative Axis")
        self.lRelativeAxis.setWordWrap(True)
        self.RelativeAxis = QSwitchControl(self.summary.node.scene.parent)
        self.RelativeAxis.stateChanged.connect(self.updateImportance)
        self.summary.node.scene.parent.switches.append(self.RelativeAxis)
        self.RelativeAxis.setChecked(True)
        self.layoutH1.addWidget(self.lAxis)     
        self.layoutH1.addWidget(self.Axis, alignment=Qt.AlignmentFlag.AlignLeft)
        self.layoutH1.addWidget(self.lRelativeAxis)
        self.layoutH1.addWidget(self.RelativeAxis, alignment=Qt.AlignmentFlag.AlignLeft)

        self.Angle = QNumEdit(min=0, max=360, step=1, decimals=1, addSlider=True, label="Angle")
        self.Angle.setText("90")
        self.Frames = QNumEdit(min=0, max=None, step=1, decimals=0, addSlider=False, label="Frames")
        self.Frames.setText("1")
        self.Frames.Text.textChanged.connect(self.summary.updateFrames)
        
        self.layoutH2 = QHBoxLayout()
        self.Tab = QTabWidget()    
        self.container1 = QWidget()   
        self.layoutH1T1H1 = QHBoxLayout(self.container1)
        self.container2 = QWidget()
        self.layoutH1T2H1 = QHBoxLayout(self.container2)
        self.RockCycle = QNumEdit(min=0, max=None, step=1, decimals=0, addSlider=False, label="Cycle")
        self.RockCycle.setText("0")
        self.layoutH1T2H1.addLayout(self.RockCycle.widget_layout)
        self.container3 = QWidget()
        self.layoutH1T3H1 = QHBoxLayout(self.container3)
        self.WobbleCycle = QNumEdit(min=0, max=None, step=1, decimals=0, addSlider=False, label="Cycle")
        self.WobbleCycle.setText("0")
        self.WobbleAspect = QNumEdit(min=None, max=None, step=1, decimals=1, addSlider=False, label="Wobble Aspect")
        self.WobbleAspect.setText("0.3")
        self.layoutH1T3H1.addLayout(self.WobbleCycle.widget_layout)
        self.layoutH1T3H1.addLayout(self.WobbleAspect.widget_layout)
        self.Tab.insertTab(0, self.container1, "Turn")
        self.Tab.insertTab(1, self.container2, "Rock")
        self.Tab.insertTab(2, self.container3, "Wobble")
        self.Tab.setFixedWidth(200)
        self.layoutH2.addWidget(self.Tab)
        
        self.layoutH3 = QHBoxLayout()
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
        self.layoutH3.addWidget(self.Delete)
        self.layoutH3.addWidget(self.Run)
        self.layoutH3.addWidget(self.RunChain)

        self.RelativeAxis.stateChanged.connect(self.internal_updateRun)

        self.main_layout.addLayout(self.layoutH1)        
        self.main_layout.addLayout(self.Angle.widget_layout)
        self.main_layout.addLayout(self.Frames.widget_layout)
        self.main_layout.addLayout(self.layoutH2)        
        self.main_layout.addLayout(self.layoutH3)        

    def updateRun(self, chain_update:bool=False):
        current_run = self.Run.isEnabled()
        if self.RelativeAxis.isChecked():
            if self.summary.used_center != []:
                if self.summary.used_model != []:
                    self.Run.setEnabled(True)
                else:
                    self.Run.setEnabled(False)
            else:
                self.Run.setEnabled(False)
        else:
            if self.summary.used_model != []:
                self.Run.setEnabled(True)
            else:
                self.Run.setEnabled(False)
        if current_run != self.Run.isEnabled():
            if not chain_update:
                self.summary.findLastNode()


    def updateTab(self, current_type:int):
        pass
    
    def updateComment(self) -> list[str]:
        start_script_string_comment = f""
        script_string_comment = f"<u><b>{self.summary.node.nodeType.name}: {self.summary.node.nodeID}</b></u><br>"
        end_script_string_comment = f""

        if self.Run.isEnabled():
            objects = "".join(self.summary.used_model)
            if objects == "All":
                objects = "all models"

            if self.RelativeAxis.isChecked():
                relative = "relative "
            else:
                relative = ""

            script_string_comment += f"Rotates <i>'{objects}'</i> around the {relative}{self.Axis.currentText().upper()} axis by {self.Angle.getText()}° for {self.Frames.getText()} frames<br>"

            center_object = "".join(self.summary.used_center)
            if self.summary.used_center is not None and center_object != "":
                if center_object == "All":
                    script_string_comment += f"Center of rotation is center of all of the objects<br>"
                else:
                    script_string_comment += f"Center of rotation is center of {center_object}<br>"
            script_string_comment += f"<br>"
        return [start_script_string_comment, script_string_comment, end_script_string_comment]

    def updateCommand(self) -> list[str]:
        super().updateCommand()

        if self.Run.isEnabled():
            center_object = "".join(self.summary.used_center)
            if self.summary.used_center is None:
                center = ""
            elif center_object == "":
                center = ""
            else:
                if center_object == "All":
                    center_object = "all"
                if self.RelativeAxis.isChecked() and center_object != "all":
                    center = f"coordinateSystem {center_object} center {center_object}"
                else:
                    center = f"center {center_object}"

            objects = "".join(self.summary.picker_model)
            if objects == "All":
                objects = f""
            else:
                objects = f" atoms <i>'{objects.lower()}'</i>"

            if self.Tab.currentIndex() == 0:
                rotationSpecific = f""
            elif self.Tab.currentIndex() == 1:
                rotationSpecific = f"rock {self.RockCycle.getText()} "
            elif self.Tab.currentIndex() == 2:
                rotationSpecific = f"wobble {self.WobbleCycle.getText()} wobbleAspect {self.WobbleAspect.getText()} "
            
            self.script_string += f"turn {self.Axis.currentText().lower()} {self.Angle.getText()} {self.Frames.getText()} {rotationSpecific}{center}{objects}<br>"
            self.script_string += f"<br>"
        
        return [self.start_script_string, self.script_string, self.end_script_string]    

    def updateImportance(self):
        if self.RelativeAxis.isChecked():
            self.summary.CenterImportant.setProperty("important", "True")
        else:
            self.summary.CenterImportant.setProperty("important", "False")
        self.summary.CenterImportant.style().unpolish(self.summary.CenterImportant)
        self.summary.CenterImportant.style().polish(self.summary.CenterImportant)

class AdvancedNodeCenterRotation(NodeBase):
    def __init__(self, session, summary:AdvancedNodeSummary, title:str="", parent=None):
        super().__init__(session, summary, title, simple_node=False, parent=parent)

        self.initUI()

    def initUI(self):
        self.main_layout = QVBoxLayout()
        self.main_layout.setSpacing(5)
        self.main_layout.setContentsMargins(10, 10, 10, 10)
        self.setLayout(self.main_layout)

        self.layoutH1 = QHBoxLayout()
        self.lMethod = QLabel("COFR method")
        self.lMethod.setWordWrap(True)
        self.Method = QComboBox()
        self.Method.addItems(["Front center", "Center of View", "Model"])
        self.Method.setCurrentIndex(1)
        self.layoutH1.addWidget(self.lMethod)
        self.layoutH1.addWidget(self.Method)

        self.layoutH2 = QHBoxLayout()
        self.lPivot = QLabel("Show Pivot")
        self.Pivot = QComboBox()
        self.Pivot.addItems(["True", "False", "Custom"])
        self.Pivot.setCurrentIndex(1)
        self.Pivot.currentIndexChanged.connect(self.updatePivot)
        self.layoutH2.addWidget(self.lPivot)
        self.layoutH2.addWidget(self.Pivot)

        self.Length = QNumEdit(min=0.01, max=None, step=1, decimals=2, addSlider=False, label="Length")
        self.Length.setText("2")
        self.Length.setEnabled(False)

        self.Radius = QNumEdit(min=0, max=None, step=1, decimals=2, addSlider=False, label="Radius")
        self.Radius.setText("0.05")
        self.Radius.setEnabled(False)

        self.layoutH3 = QHBoxLayout()
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
        self.layoutH3.addWidget(self.Delete)
        self.layoutH3.addWidget(self.Run)
        self.layoutH3.addWidget(self.RunChain)

        self.main_layout.addLayout(self.layoutH1)
        self.main_layout.addLayout(self.layoutH2)
        self.main_layout.addLayout(self.Length.widget_layout)
        self.main_layout.addLayout(self.Radius.widget_layout)
        self.main_layout.addLayout(self.layoutH3)

    def updateRun(self, chain_update:bool=False):
        current_run = self.Run.isEnabled()
        if self.summary.used_center != []:
            self.Run.setEnabled(True)
        else:
            self.Run.setEnabled(False)
        if current_run != self.Run.isEnabled():
            if not chain_update:
                self.summary.findLastNode()

    def updateTab(self, current_type:int):
        pass
    
    def updateComment(self) -> list[str]:
        start_script_string_comment = f""
        script_string_comment = f"<u><b>{self.summary.node.nodeType.name}: {self.summary.node.nodeID}</b></u><br>"
        end_script_string_comment = f""

        if self.Run.isEnabled():
            if self.Method.currentText() == "Front center":
                method = f"center of seen items"
            elif self.Method.currentText() == "Center of View":
                method = f"center of view"
            elif self.Method.currentText() == "Model":
                objects = "".join(self.summary.used_center)
                if objects == "All":
                    objects = "all models"
                method = f"center of <i>'{objects}'</i>" 

            script_string_comment += f"Sets the center of rotation to {method}<br>"
                
            if self.Pivot.currentText() == "Custom" or self.Pivot.currentText() == "True":
                script_string_comment += f"Creates a pivot:<br>"
                script_string_comment += f"   • <u>Length:</u> - {self.Length.getText()}<br>" 
                script_string_comment += f"   • <u>Radius:</u> - {self.Radius.getText()}"

            script_string_comment += f"<br>"
        return [start_script_string_comment, script_string_comment, end_script_string_comment]

    def updateCommand(self) -> list[str]:
        super().updateCommand()

        if self.Run.isEnabled():
            if self.Method.currentText() == "Front center":
                method = "frontCenter"
            elif self.Method.currentText() == "Center of View":
                method = "centerOfView"
            elif self.Method.currentText() == "Model":
                method = "".join(self.summary.used_center)
                method = f"<i>'{method}'</i>"

            if self.Pivot.currentText() == "Custom":
                pivot = f"{self.Length.getText()},{self.Radius.getText()}"
            else:
                pivot = self.Pivot.currentText().lower()
            
            self.script_string += f"cofr {method} showPivot {pivot}<br>"
        
        return [self.start_script_string, self.script_string, self.end_script_string]    

    def updatePivot(self):
        if self.Pivot.currentText() == "Custom":
            self.Length.setEnabled(True)
            self.Radius.setEnabled(True)
        else:
            self.Length.setText("2")
            self.Length.setEnabled(False)
            self.Length.setText("0.05")
            self.Radius.setEnabled(False)

class AdvancedNodeCenterMass(NodeBase):
    def __init__(self, session, summary:AdvancedNodeSummary, title:str="", parent=None):
        super().__init__(session, summary, title, simple_node=False, parent=parent)

        self.initUI()

    def initUI(self):
        self.main_layout = QVBoxLayout()
        self.main_layout.setSpacing(5)
        self.main_layout.setContentsMargins(10, 10, 10, 10)
        self.setLayout(self.main_layout)

        self.MarkColorValue = QColor("#B4B4B4")

        self.layoutH1 = QHBoxLayout()
        self.lName = QLabel("Name")
        self.Name = QLineEdit()
        self.lMark = QLabel("Mark")
        self.Mark = QSwitchControl(self.summary.node.scene.parent)
        self.Mark.setChecked(True)
        self.summary.node.scene.parent.switches.append(self.Mark)
        self.Mark.stateChanged.connect(self.updateRadius)
        self.Mark.stateChanged.connect(self.internal_updateRun)
        self.layoutH1.addWidget(self.lName)
        self.layoutH1.addWidget(self.Name)
        self.layoutH1.addWidget(self.lMark)
        self.layoutH1.addWidget(self.Mark)

        self.Radius = QNumEdit(min=0, max=None, step=1, decimals=2, addSlider=False, label="Radius")
        self.Radius.setText("0.05")
        self.Radius.setEnabled(False)

        self.layoutH2 = QHBoxLayout()
        self.MarkColor = QPushButton("Mark Color")    
        self.MarkColor.clicked.connect(self.openMarkColorDialog)
        self.MarkColorDialog = QColorDialog()
        self.MarkColorLabel = QLabel()   
        self.MarkColorLabel.setFixedWidth(50)
        self.MarkColorLabel.setFixedHeight(50)        
        self.MarkColorLabel.setStyleSheet(f"QLabel {{ background-color: {self.MarkColorValue.name()}; border: 1px solid black}}")
        self.layoutH2.addWidget(self.MarkColor)
        self.layoutH2.addWidget(self.MarkColorLabel)

        self.layoutH3 = QHBoxLayout()
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
        self.layoutH3.addWidget(self.Delete)
        self.layoutH3.addWidget(self.Run)
        self.layoutH3.addWidget(self.RunChain)

        self.main_layout.addLayout(self.layoutH1)
        self.main_layout.addLayout(self.Radius.widget_layout)
        self.main_layout.addLayout(self.layoutH2)
        self.main_layout.addLayout(self.layoutH3)
    
    def updateRun(self, chain_update:bool=False):
        current_run = self.Run.isEnabled()
        if self.summary.used_model != [] and ((self.Mark.isChecked()) or not self.Mark.isChecked()):
            self.Run.setEnabled(True)
        else:
            self.Run.setEnabled(False)
        if current_run != self.Run.isEnabled():
            if not chain_update:
                self.summary.findLastNode()

    def updateRadius(self):
        if self.Mark.isChecked():
            self.Radius.setEnabled(True)
        else:
            self.Radius.setEnabled(False)

    def updateTab(self, current_type:int):
        pass
    
    def updateComment(self) -> list[str]:
        start_script_string_comment = f""
        script_string_comment = f"<u><b>{self.summary.node.nodeType.name}: {self.summary.node.nodeID}</b></u><br>"
        end_script_string_comment = f""

        if self.Run.isEnabled():
            objects = "".join(self.summary.used_model)
            if objects == "All":
                objects = "all models"
                
            if self.Name.text() == "":
                name = f"name mass-<i>'{objects}'</i>"
            else:
                name = f"name {self.Name.text()}"

            script_string_comment += f"Creates a mark item:<br>"
            script_string_comment += f"   • <u>Name:</u>: {name}<br>"
            script_string_comment += f"   • <u>Position:</u>: center of mass of <i>'{objects}'</i><br>"
            script_string_comment += f"   • <u>Color:</u>: <a style='background-color:{self.MarkColorValue.name()};'>{self.MarkColorValue.name()}</a><br>"
            script_string_comment += f"   • <u>Radius:</u>: {self.Radius.getText()}<br>"
            script_string_comment += f"<br>"

        return [start_script_string_comment, script_string_comment, end_script_string_comment]

    def updateCommand(self) -> list[str]:
        super().updateCommand()

        if self.Run.isEnabled():
            objects = "".join(self.summary.used_model)
            if objects == "All":
                objects = f"<i>'{objects.lower()}'</i>"
            else:
                objects = f"<i>'{objects}'</i>"
            
            if self.Mark.isChecked():
                if float(self.Radius.getText()) >= 0.00:
                    radius = f"radius {self.Radius.getText()}"
                else:
                    radius=""
                
                if self.Name.text() == "":
                    name = f"name mass-{objects}"
                else:
                    name = f"name {self.Name.text()}"
                
                color = f"color {self.MarkColorValue.name()}"

                self.script_string += f"measure center {objects} mark True {radius} {color} {name}<br>"
            else:
                self.script_string += f"measure center {objects}<br>"
        
        return [self.start_script_string, self.script_string, self.end_script_string]    

    def openMarkColorDialog(self):
        self.MarkColorValue = self.MarkColorDialog.getColor()
        self.MarkColorLabel.setStyleSheet(f"QLabel {{ background-color : rgb({self.MarkColorValue.getRgb()[0]},{self.MarkColorValue.getRgb()[1]},{self.MarkColorValue.getRgb()[2]}); border: 1px solid black}}")
        self.updateRun()

    def updateMarkColorLabel(self):        
        self.MarkColorLabel.setStyleSheet(f"QLabel {{ background-color : rgb({self.MarkColorValue.getRgb()[0]},{self.MarkColorValue.getRgb()[1]},{self.MarkColorValue.getRgb()[2]}); border: 1px solid black}}")

    def updateNode(self):
        if self.Center.currentText() == "Mass":
            self.CenterSelect.setEnabled(True)
        else:
            self.CenterSelect.setEnabled(False)

class AdvancedNodeDelete(NodeBase):
    def __init__(self, session, scene:Scene, summary:AdvancedNodeSummary, title:str="", parent=None):
        super().__init__(session, summary, title, simple_node=False, parent=parent)

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
        if self.summary.picker_delete != []:
            self.Run.setEnabled(True)
        else:
            self.Run.setEnabled(False)
        
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

    def updateComment(self) -> list[str]:
        start_script_string_comment = f""
        script_string_comment = f"<u><b>{self.summary.node.nodeType.name}: {self.summary.node.nodeID}</b></u><br>"
        end_script_string_comment = f""

        if self.Run.isEnabled():
            objects = "".join(self.summary.used_model)
            if objects == "All":
                objects = "all models"
                
            script_string_comment += f"Deletes <i>'{objects}'</i><br>"
            script_string_comment += f"<br>"
            
        return [start_script_string_comment, script_string_comment, end_script_string_comment]

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
                    self.script_string += f"delete {objects} attachedHyds {self.AttachedHyds.isChecked()}<br>"
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

class AdvancedNodeWait(NodeBase):
    def __init__(self, session, summary:AdvancedNodeSummary, title:str="", parent=None):
        super().__init__(session, summary, title, simple_node=False, parent=parent)

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

    def updateComment(self) -> list[str]:
        start_script_string_comment = f""
        script_string_comment = f"<u><b>{self.summary.node.nodeType.name}: {self.summary.node.nodeID}</b></u><br>"
        end_script_string_comment = f""

        script_string_comment += f"Waits for {int(self.Frames.getText())} frames<br>"
        script_string_comment += f"<br>"
            
        return [start_script_string_comment, script_string_comment, end_script_string_comment]

    def updateCommand(self) -> list[str]:
        super().updateCommand()

        if int(self.Frames.getText()) > 0 :
            wait = f"wait {int(self.Frames.getText())}<br>"
        else:
            wait = f"wait"
        self.script_string += f"{wait}"
        self.script_string += f"<br>"
        
        return [self.start_script_string, self.script_string, self.end_script_string]    

class AdvancedNodeCrossfade(NodeBase):
    def __init__(self, session, summary:AdvancedNodeSummary, title:str="", parent=None):
        super().__init__(session, summary, title, simple_node=False, parent=parent)

        self.initUI()  

    def initUI(self):
        self.main_layout = QVBoxLayout()
        self.main_layout.setSpacing(5)
        self.main_layout.setContentsMargins(10, 10, 10, 10)
        self.setLayout(self.main_layout)

        self.Frames = QNumEdit(min=0, max=None, step=1, decimals=0, addSlider=False, label="Frames")
        self.Frames.setText("30")
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
    
    def updateComment(self) -> list[str]:
        start_script_string_comment = f""
        script_string_comment = f"<u><b>{self.summary.node.nodeType.name}: {self.summary.node.nodeID}</b></u><br>"
        end_script_string_comment = f""

        script_string_comment += f"Next nodes graphical changes will be performes with a crossfade of {int(self.Frames.getText())} frames if possible<br>"
        script_string_comment += f"<br>"
            
        return [start_script_string_comment, script_string_comment, end_script_string_comment]

    def updateCommand(self) -> list[str]:
        super().updateCommand()

        self.script_string += f"crossfade {int(self.Frames.getText())}<br>"
        self.script_string += f"<br>"
        
        return [self.start_script_string, self.script_string, self.end_script_string]    

class AdvancedNodeSaveView(NodeBase):
    def __init__(self, session, summary:AdvancedNodeSummary, title:str="", parent=None):
        super().__init__(session, summary, title, simple_node=False, parent=parent)

        self.initUI()  

    def initUI(self):
        self.main_layout = QVBoxLayout()
        self.main_layout.setSpacing(5)
        self.main_layout.setContentsMargins(10, 10, 10, 10)
        self.setLayout(self.main_layout)

        self.layoutH1 = QHBoxLayout()
        self.lName = QLabel("Name")
        self.Name = QLineEdit()
        self.Name.textChanged.connect(self.internal_updateRun)
        self.layoutH1.addWidget(self.lName)
        self.layoutH1.addWidget(self.Name)

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

        self.main_layout.addLayout(self.layoutH1)
        self.main_layout.addLayout(self.layoutH2)

    def updateRun(self, chain_update:bool=False):
        if self.Name.text() == "":
            self.Run.setEnabled(False)
        else:
            self.Run.setEnabled(True)

    def updateTab(self, current_type:int):
        pass
    
    def updateComment(self) -> list[str]:
        start_script_string_comment = f""
        script_string_comment = f"<u><b>{self.summary.node.nodeType.name}: {self.summary.node.nodeID}</b></u><br>"
        end_script_string_comment = f""

        if self.Run.isEnabled():
            script_string_comment += f"Saves a view with the name '{self.Name.text()}'<br>"
            script_string_comment += f"<br>"
            
        return [start_script_string_comment, script_string_comment, end_script_string_comment]

    def updateCommand(self) -> list[str]:
        super().updateCommand()

        if self.Run.isEnabled():
            if self.Name.text() != "":
                self.script_string += f"view name {self.Name.text()}<br>"
                self.script_string += f"<br>"

        return [self.start_script_string, self.script_string, self.end_script_string]

class AdvancedNodeLoadView(NodeBase):
    def __init__(self, session, summary:AdvancedNodeSummary, title:str="", parent=None):
        super().__init__(session, summary, title, simple_node=False, parent=parent)

        self.initUI()  

    def initUI(self):
        self.main_layout = QVBoxLayout()
        self.main_layout.setSpacing(5)
        self.main_layout.setContentsMargins(10, 10, 10, 10)
        self.setLayout(self.main_layout)

        self.layoutV1 = QVBoxLayout()
        self.layoutV1H1 = QHBoxLayout()
        self.lView = QLabel("View")
        self.View = QComboBox()
        self.View.addItems(["Original", "Orient", "Initial", "Custom"])
        self.View.currentIndexChanged.connect(self.internal_updateRun)
        self.layoutV1H1.addWidget(self.lView)
        self.layoutV1H1.addWidget(self.View)
        self.layoutV1H2 = QHBoxLayout()
        self.layoutV1H2V1 = QVBoxLayout()
        self.lClip = QLabel("Clip")
        self.Clip = QSwitchControl(self.summary.node.scene.parent)
        self.summary.node.scene.parent.switches.append(self.Clip)
        self.layoutV1H2V1.addWidget(self.lClip)
        self.layoutV1H2V1.addWidget(self.Clip)
        self.layoutV1H2V2 = QVBoxLayout()
        self.lCofr = QLabel("Cofr")
        self.Cofr = QSwitchControl(self.summary.node.scene.parent)
        self.summary.node.scene.parent.switches.append(self.Cofr)
        self.layoutV1H2V2.addWidget(self.lCofr)
        self.layoutV1H2V2.addWidget(self.Cofr)
        self.layoutV1H2.addLayout(self.layoutV1H2V1)
        self.layoutV1H2.addLayout(self.layoutV1H2V2)
        self.Pad = QNumEdit(min=None, max=1, step=1, decimals=2, addSlider=False, label="Pad")
        self.Pad.setText("0.05")
        self.layoutV1.addLayout(self.layoutV1H1)
        self.layoutV1.addLayout(self.layoutV1H2)
        self.layoutV1.addLayout(self.Pad.widget_layout)

        self.layoutH1 = QHBoxLayout()
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
        self.layoutH1.addWidget(self.Delete)
        self.layoutH1.addWidget(self.Run)
        self.layoutH1.addWidget(self.RunChain)

        self.main_layout.addLayout(self.layoutV1)
        self.main_layout.addLayout(self.layoutH1)

    def updateRun(self, chain_update:bool=False):
        current_run = self.Run.isEnabled()
        if (self.View.currentText() == "Custom" and self.summary.used_view == []):
            self.Run.setEnabled(False)
        else:
            self.Run.setEnabled(True)
        if current_run != self.Run.isEnabled():
            if not chain_update:
                self.summary.findLastNode()

    def updateTab(self, current_type:int):
        pass
    
    def updateComment(self) -> list[str]:
        start_script_string_comment = f""
        script_string_comment = f"<u><b>{self.summary.node.nodeType.name}: {self.summary.node.nodeID}</b></u><br>"
        end_script_string_comment = f""

        if self.Run.isEnabled():
            if self.View.currentText() == "Original":
                script_string_comment += f"Resets the view to the inital state and orient axis to standard orientation"
            elif self.View.currentText() == "Orient":
                script_string_comment += f"Orient axis to standard orientation"
            elif self.View.currentText() == "Initial":
                script_string_comment += f"Resets the view to the inital state"
            elif self.View.currentText() == "Custom":
                objects = "".join(self.summary.used_view)
                if objects == "All":
                    objects = "all models"
                view = f"Change view to <i>'{objects}'</i><br>"
                if self.Clip.isChecked():
                    clip = f"   • Clipping applied<br>;"
                else:
                    clip = ""
                if self.Pad.Text.text():
                    pad = f"   • Padding applied<br>;"
                else:
                    pad = ""
                if self.Cofr.isChecked():
                    cofr = f"   • Sets <i>'{objects}'</i> as center of rotation;"
                else:
                    cofr = ""
                script_string_comment += f"{view} {clip} {pad} {cofr}<br>"
            script_string_comment += f"<br>"
            
        return [start_script_string_comment, script_string_comment, end_script_string_comment]

    def updateCommand(self) -> list[str]:
        super().updateCommand()

        if self.Run.isEnabled():
            if self.View.currentText() == "Original":
                view = f"view orient; view initial"
                self.script_string += f"{view}<br>"
                self.script_string += f"<br>"
            elif self.View.currentText() == "Orient":
                view = f"view orient"
                self.script_string += f"{view}<br>"
                self.script_string += f"<br>"
            elif self.View.currentText() == "Initial":
                view = f"view initial"
                self.script_string += f"{view}<br>"
                self.script_string += f"<br>"
            elif self.View.currentText() == "Custom":
                objects = "".join(self.summary.used_view)
                if objects == "All":
                    objects = f"<i>'{objects.lower()}'</i>"
                else:
                    objects = f"<i>'{objects}'</i>"
                view = f"view {objects}"
                clip = f"clip {self.Clip.isChecked()}"
                pad = f"pad {self.Pad.getText()}"
                cofr = f"cofr {self.Cofr.isChecked()}"
                self.script_string += f"{view} {clip} {pad} {cofr}<br>"
                self.script_string += f"<br>"
        
        return [self.start_script_string, self.script_string, self.end_script_string]

class AdvancedNodeFly(NodeBase):
    def __init__(self, session, summary:AdvancedNodeSummary, title:str="", parent=None):
        super().__init__(session, summary, title, simple_node=False, parent=parent)

        self.transition_frames = []

        self.current_index = -1
        
        self.initUI()  

    def initUI(self):
        self.main_layout = QVBoxLayout()
        self.main_layout.setSpacing(5)
        self.main_layout.setContentsMargins(10, 10, 10, 10)
        self.setLayout(self.main_layout)

        self.layoutH1 = QHBoxLayout()
        self.Transition = QComboBox()
        self.Transition.currentIndexChanged.connect(self.changeFlySequence)
        self.Transition.setEnabled(False)  
        self.Transition.setFixedWidth(200)
        self.layoutH1.addWidget(self.Transition, alignment=Qt.AlignmentFlag.AlignCenter)

        self.Frames = QNumEdit(min=0, max=None, step=1, decimals=0, addSlider=False, label="Frames")
        self.Frames.setText("100")        
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
        self.main_layout.addLayout(self.Frames.widget_layout)
        self.main_layout.addLayout(self.layoutH2)

    def updateRun(self, chain_update:bool=False): 
        current_run = self.Run.isEnabled()  
        if self.summary.used_fly_groups != [] and len(self.summary.used_fly_groups) > 1: 
            self.Transition.setEnabled(True)
            self.Frames.setEnabled(True)
            self.Run.setEnabled(True)
        else:
            self.Transition.setEnabled(False)
            self.Frames.setEnabled(False)
            self.Run.setEnabled(False)   
        if current_run != self.Run.isEnabled():
            if not chain_update:
                self.summary.findLastNode() 
                
    def updateTab(self, current_type:int):
        pass
    
    def updateComment(self) -> list[str]:
        start_script_string_comment = f""
        script_string_comment = f"<u><b>{self.summary.node.nodeType.name}: {self.summary.node.nodeID}</b></u><br>"
        end_script_string_comment = f""

        if self.Run.isEnabled():
            for i in range(self.Transition.count()):
                script_string_comment += f"Flies from {self.summary.used_fly_groups[i]} to {self.summary.used_fly_groups[i + 1]} in {self.transition_frames[i]} frames<br>"
            script_string_comment += f"<br>"

        return [start_script_string_comment, script_string_comment, end_script_string_comment]

    def updateCommand(self) -> list[str]:
        super().updateCommand()

        if self.Run.isEnabled():
            self.script_string += f"fly"
            for i in range(self.Transition.count()):
                if i == 0:
                    start = self.summary.used_fly_groups[i]
                    self.script_string += f" {start}"
                frames = self.transition_frames[i]
                end = self.summary.used_fly_groups[i + 1]
                self.script_string += f" {frames} {end}"
            self.script_string += f"<br>"

        return [self.start_script_string, self.script_string, self.end_script_string]

    def updateUsedFlySequences(self):
        if self.summary.FlyToggle.isChecked():
            self.summary.used_fly_groups = self.summary.picker_fly_groups
        else:
            self.summary.used_fly_groups = self.summary.chain_fly_groups

    def generateFlySequences(self):
        self.Transition.currentIndexChanged.disconnect(self.changeFlySequence)
        self.Transition.clear()
        if len(self.summary.used_fly_groups) > 1:
            for i in range(len(self.summary.used_fly_groups) - 1):
                self.Transition.addItem(f"{self.summary.used_fly_groups[i]} to {self.summary.used_fly_groups[i + 1]}")
            self.current_index = self.Transition.currentIndex()
        else:
            self.current_index = self.Transition.currentIndex()
        self.Transition.currentIndexChanged.connect(self.changeFlySequence)   

    def addFlySequence(self): 
        self.updateUsedFlySequences()
        self.updateFlySequence()
        if len(self.summary.used_fly_groups) > 1:
            self.transition_frames.append("100")
        self.generateFlySequences()
        self.switchFlySequence()

    def addFlySequences(self):  
        self.updateUsedFlySequences()
        self.updateFlySequence()
        self.transition_frames = []
        if len(self.summary.used_fly_groups) > 1:
            for group in self.summary.used_fly_groups:
                self.transition_frames.append("100")
        self.generateFlySequences()
        self.switchFlySequence()

    def removeFlySequence(self, row_indexes, selected_len:int):
        self.updateUsedFlySequences()
        self.updateFlySequence()
        for index in sorted(row_indexes, reverse=True):
            if selected_len == 2:
                del self.transition_frames[index]
            elif selected_len > 2 :
                if index == 0:
                    del self.transition_frames[index]
                elif index == selected_len - 1:
                    del self.transition_frames[index - 1]
                else:
                    self.transition_frames[index] = "100"
                    del self.transition_frames[index - 1]
        self.generateFlySequences()
        self.switchFlySequence()

    def resetFlySequence(self):  
        self.updateUsedFlySequences()
        self.updateFlySequence()
        self.transition_frames = []
        if len(self.summary.used_fly_groups) > 1:
            for group in self.summary.used_fly_groups:
                self.transition_frames.append("100")
        self.generateFlySequences()
        self.switchFlySequence()
    
    def updateFlySequence(self):  
        if self.current_index > -1: 
            self.transition_frames[self.current_index] = self.Frames.getText()
            self.current_index = self.Transition.currentIndex()
            self.Frames.Text.textChanged.disconnect(self.summary.updateFrames)
            self.Frames.setText(self.transition_frames[self.current_index])  
            self.Frames.Text.textChanged.connect(self.summary.updateFrames) 

    def switchFlySequence(self):
        self.current_index = self.Transition.currentIndex()
        if self.current_index > -1:
            self.Frames.setText(self.transition_frames[self.current_index]) 
        else:
            self.Frames.setText("100") 

    def changeFlySequence(self):
        self.updateFlySequence()
        self.switchFlySequence()

class AdvancedNodeSplit(NodeBase):
    def __init__(self, session, summary:AdvancedNodeSummary, title:str="", parent=None):
        super().__init__(session, summary, title, simple_node=False, parent=parent)
                        
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
        if self.summary.used_model != []: 
            self.Run.setEnabled(True)
        else:
            self.Run.setEnabled(False)   
                
    def updateTab(self, current_type:int):
        pass
    
    def updateComment(self) -> list[str]:
        start_script_string_comment = f""
        script_string_comment = f"<u><b>{self.summary.node.nodeType.name}: {self.summary.node.nodeID}</b></u><br>"
        end_script_string_comment = f""

        if self.Run.isEnabled():
            objects = "".join(self.summary.used_model)
            if objects == "All":
                objects = "all models"
            script_string_comment += f"Splits <i>'{objects}'</i> based on {self.Model.currentText()}<br>"
            script_string_comment += f"<br>"

        return [start_script_string_comment, script_string_comment, end_script_string_comment]

    def updateCommand(self) -> list[str]:
        super().updateCommand()

        if self.Run.isEnabled():
            objects = "".join(self.summary.used_model)
            if objects == "All":
                objects = f"<i>'{objects.lower()}'</i>"
            else:
                objects = f"<i>'{objects}'</i>"
            self.script_string += f"split {objects} {self.Model.currentText().lower()}<br>"
            self.script_string += f"<br>"

        return [self.start_script_string, self.script_string, self.end_script_string]

class AdvancedNodeEnd(NodeBase):
    def __init__(self, session, summary:AdvancedNodeSummary, title:str="", parent=None):
        super().__init__(session, summary, title, simple_node=False, parent=parent)

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
    
    def updateComment(self) -> list[str]:
        start_script_string_comment = f""
        script_string_comment = f"<u><b>{self.summary.node.nodeType.name}: {self.summary.node.nodeID}</b></u><br>"
        end_script_string_comment = f""
        list_format = QTextListFormat()
        list_format.setStyle(QTextListFormat.Style.ListDisc)
        script_string_comment += f"Stops the movie<br>"
        script_string_comment += f"Saves the movie:<br>"
        script_string_comment += f"   • <u>Name:</u> {self.Name.text()}.{self.Format.currentText()}<br>"
        script_string_comment += f"   • <u>Quality:</u> {self.Quality.currentText()}<br>"
        script_string_comment += f"   • <u>Framerate:</u> {self.Framerate.getText()}<br>"
        script_string_comment += f"   • <u>Round Trip:</u> {self.Roundtrip.isChecked()}<br>"
        script_string_comment += f"<br>"

        return [start_script_string_comment, script_string_comment, end_script_string_comment]

    def updateCommand(self) -> list[str]:
        super().updateCommand()

        self.end_script_string += f"movie stop;<br>"
        self.end_script_string += f"movie encode {self.Name.text()}.{self.Format.currentText()} quality {self.Quality.currentText().lower()} framerate {self.Framerate.getText()} roundTrip {self.Roundtrip.isChecked()}"

        return [self.start_script_string, self.script_string, self.end_script_string]

class AdvancedNodeSummary(QWidget):
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
        self.chain_model = []
        self.chain_color_groups = []
        self.chain_center = []
        self.chain_view = []
        self.chain_fly_groups = []
        self.accumulated_frames = 0
        self.used_model = []
        self.used_color_groups = []
        self.used_center = []
        self.used_view = []
        self.used_fly_groups = []
        self.used_delete = []
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
            if model_input:
                self.layoutH1 = QHBoxLayout()
                self.ModelImportant = QCheckBox()
                self.ModelImportant.setEnabled(False)
                self.ModelImportant.setProperty("important", "True")
                self.lModel = QLabel("Model:")
                self.ModelToggle = QSwitchControl(self.node.scene.parent)
                self.node.scene.parent.switches.append(self.ModelToggle)
                self.ModelToggle.stateChanged.connect(self.updateModelPicker)
                self.ModelCheck = QCheckBox()
                self.ModelCheck.setEnabled(False)
                self.layoutH1.addWidget(self.ModelImportant, alignment=Qt.AlignmentFlag.AlignLeft)
                self.layoutH1.addWidget(self.lModel, alignment=Qt.AlignmentFlag.AlignLeft)
                if NodeType(self.node.nodeType) != NodeType.Split:
                    self.layoutH1.addWidget(self.ModelToggle, alignment=Qt.AlignmentFlag.AlignLeft)
                self.layoutH1.addWidget(self.ModelCheck, alignment=Qt.AlignmentFlag.AlignLeft)
                self.main_layout.addLayout(self.layoutH1)
            if color_input:
                self.layoutH1 = QHBoxLayout()
                self.ColorImportant = QCheckBox()
                self.ColorImportant.setEnabled(False)
                self.ColorImportant.setProperty("important", "True")
                self.lColor = QLabel("Color:")
                self.ColorToggle = QSwitchControl(self.node.scene.parent)
                self.node.scene.parent.switches.append(self.ColorToggle)
                self.ColorToggle.stateChanged.connect(self.updateColorPicker)
                self.ColorCheck = QCheckBox()
                self.ColorCheck.setEnabled(False)
                self.layoutH1.addWidget(self.ColorImportant, alignment=Qt.AlignmentFlag.AlignLeft)
                self.layoutH1.addWidget(self.lColor, alignment=Qt.AlignmentFlag.AlignLeft)
                self.layoutH1.addWidget(self.ColorToggle, alignment=Qt.AlignmentFlag.AlignLeft)
                self.layoutH1.addWidget(self.ColorCheck, alignment=Qt.AlignmentFlag.AlignLeft)
                self.main_layout.addLayout(self.layoutH1)
            if center_input:
                self.layoutH1 = QHBoxLayout()
                self.CenterImportant = QCheckBox()
                self.CenterImportant.setEnabled(False)
                if NodeType(self.node.nodeType) != NodeType.Rotation:
                    self.CenterImportant.setProperty("important", "True")
                else:
                    self.CenterImportant.setProperty("important", "False")
                self.lCenter = QLabel("Center:")
                self.CenterToggle = QSwitchControl(self.node.scene.parent)
                self.node.scene.parent.switches.append(self.CenterToggle)
                self.CenterToggle.stateChanged.connect(self.updateCenterPicker)
                self.CenterCheck = QCheckBox()
                self.CenterCheck.setEnabled(False)
                self.layoutH1.addWidget(self.CenterImportant, alignment=Qt.AlignmentFlag.AlignLeft)
                self.layoutH1.addWidget(self.lCenter, alignment=Qt.AlignmentFlag.AlignLeft)
                self.layoutH1.addWidget(self.CenterToggle, alignment=Qt.AlignmentFlag.AlignLeft)
                self.layoutH1.addWidget(self.CenterCheck, alignment=Qt.AlignmentFlag.AlignLeft)
                self.main_layout.addLayout(self.layoutH1)
            if view_input:
                self.layoutH1 = QHBoxLayout()
                self.ViewImportant = QCheckBox()
                self.ViewImportant.setEnabled(False)
                self.ViewImportant.setProperty("important", "True")
                self.lView = QLabel("View:")
                self.ViewToggle = QSwitchControl(self.node.scene.parent)
                self.node.scene.parent.switches.append(self.ViewToggle)
                self.ViewToggle.stateChanged.connect(self.updateViewPicker)
                self.ViewCheck = QCheckBox()
                self.ViewCheck.setEnabled(False)
                self.layoutH1.addWidget(self.ViewImportant, alignment=Qt.AlignmentFlag.AlignLeft)
                self.layoutH1.addWidget(self.lView, alignment=Qt.AlignmentFlag.AlignLeft)
                self.layoutH1.addWidget(self.ViewToggle, alignment=Qt.AlignmentFlag.AlignLeft)
                self.layoutH1.addWidget(self.ViewCheck, alignment=Qt.AlignmentFlag.AlignLeft)
                self.main_layout.addLayout(self.layoutH1)
            if fly_input:
                self.layoutH1 = QHBoxLayout()
                self.FlyImportant = QCheckBox()
                self.FlyImportant.setEnabled(False)
                self.FlyImportant.setProperty("important", "True")
                self.lFly = QLabel("Fly:")
                self.FlyToggle = QSwitchControl(self.node.scene.parent)
                self.node.scene.parent.switches.append(self.FlyToggle)
                self.FlyToggle.stateChanged.connect(self.updateFlyPicker)
                self.FlyCheck = QCheckBox()
                self.FlyCheck.setEnabled(False)
                self.layoutH1.addWidget(self.FlyImportant, alignment=Qt.AlignmentFlag.AlignLeft)
                self.layoutH1.addWidget(self.lFly, alignment=Qt.AlignmentFlag.AlignLeft)
                self.layoutH1.addWidget(self.FlyToggle, alignment=Qt.AlignmentFlag.AlignLeft)
                self.layoutH1.addWidget(self.FlyCheck, alignment=Qt.AlignmentFlag.AlignLeft)
                self.main_layout.addLayout(self.layoutH1)
            if NodeType(self.node.nodeType) == NodeType.Delete:
                self.layoutH1 = QHBoxLayout()
                self.DeleteImportant = QCheckBox()
                self.DeleteImportant.setEnabled(False)
                self.DeleteImportant.setProperty("important", "True")
                self.lDelete = QLabel("Delete:")
                self.DeleteCheck = QCheckBox()
                self.DeleteCheck.setEnabled(False)
                self.layoutH1.addWidget(self.DeleteImportant, alignment=Qt.AlignmentFlag.AlignLeft)
                self.layoutH1.addWidget(self.lDelete, alignment=Qt.AlignmentFlag.AlignLeft)
                self.layoutH1.addWidget(self.DeleteCheck, alignment=Qt.AlignmentFlag.AlignLeft)
                self.main_layout.addLayout(self.layoutH1)
            if self.node.has_input or self.node.has_output:
                self.layoutH2 = QHBoxLayout()
                self.lFrames = QLabel(f"Frames: {self.used_frames}")
                self.layoutH2.addWidget(self.lFrames, alignment=Qt.AlignmentFlag.AlignLeft)
                self.layoutH3 = QHBoxLayout()
                self.lTotalFrames = QLabel(f"Total Frames: {self.total_frames}")
                self.layoutH3.addWidget(self.lTotalFrames, alignment=Qt.AlignmentFlag.AlignLeft)
                self.layoutH4 = QHBoxLayout()
                self.lLength = QLabel(f"Length: {self.convertTime(0)}")
                self.layoutH4.addWidget(self.lLength, alignment=Qt.AlignmentFlag.AlignLeft)
                self.main_layout.addLayout(self.layoutH2)
                self.main_layout.addLayout(self.layoutH3)
                self.main_layout.addLayout(self.layoutH4)
            
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
    
    def updateModelPicker(self):
        if self.ModelToggle.isChecked():
            pos = self.node.pos
            count = len(self.node.picker_inputs)
            if self.node.node_input is not None:
                count += 1
            self.node.input_model.setSelfPos(pos.x(), pos.y(), count)
            self.node.input_model.grNode.show()
            self.node.input_model_edge.grEdge.show()
            self.node.input_model_edge.end_socket.socket_type = SocketType.MODEL_SOCKET
        else:
            self.node.input_model.grNode.hide()
            self.node.input_model_edge.grEdge.hide()
            self.node.input_model_edge.end_socket.socket_type = SocketType.DISABLED_SOCKET
        self.updateModel()

    def updateModel(self):
        if self.ModelToggle.isChecked():
            self.used_model = self.picker_model
        else:
            self.used_model = self.chain_model
        if self.used_model == []:
            self.ModelCheck.setChecked(False)
        else:
            self.ModelCheck.setChecked(True)
        self.node.content.updateRun(chain_update=True)
        self.updateModelValues()

    def updateColorPicker(self):
        if self.ColorToggle.isChecked():
            pos = self.node.pos
            count = len(self.node.picker_inputs)
            if self.node.node_input is not None:
                count += 1
            self.node.input_color.setSelfPos(pos.x(), pos.y(), count)
            self.node.input_color.grNode.show()
            self.node.input_color_edge.grEdge.show()
            self.node.input_color_edge.end_socket.socket_type = SocketType.COLOR_SOCKET
        else:
            self.node.input_color.grNode.hide()
            self.node.input_color_edge.grEdge.hide()
            self.node.input_color_edge.end_socket.socket_type = SocketType.DISABLED_SOCKET
        self.updateColor()

    def updateColor(self):
        if self.ColorToggle.isChecked():
            self.used_color_groups = self.picker_color_groups
        else:
            self.used_color_groups = self.chain_color_groups
        if self.used_color_groups == []:
            self.ColorCheck.setChecked(False)
        else:
            self.ColorCheck.setChecked(True)
        self.node.content.updateRun(chain_update=True)
        self.updateColorValues()

    def updateCenterPicker(self):
        if self.CenterToggle.isChecked():
            pos = self.node.pos
            count = len(self.node.picker_inputs)
            if self.node.node_input is not None:
                count += 1
            self.node.input_center.setSelfPos(pos.x(), pos.y(), count)
            self.node.input_center.grNode.show()
            self.node.input_center_edge.grEdge.show()
            self.node.input_center_edge.end_socket.socket_type = SocketType.CENTER_SOCKET
        else:
            self.node.input_center.grNode.hide()
            self.node.input_center_edge.grEdge.hide()
            self.node.input_center_edge.end_socket.socket_type = SocketType.DISABLED_SOCKET
        self.updateCenter()

    def updateCenter(self):
        if self.CenterToggle.isChecked():
            self.used_center = self.picker_center
        else:
            self.used_center = self.chain_center
        if self.used_center == []:
            self.CenterCheck.setChecked(False)
        else:
            self.CenterCheck.setChecked(True)
        self.node.content.updateRun(chain_update=True)
        self.updateCenterValues()

    def updateViewPicker(self):
        if self.ViewToggle.isChecked():
            pos = self.node.pos
            count = len(self.node.picker_inputs)
            if self.node.node_input is not None:
                count += 1
            self.node.input_view.setSelfPos(pos.x(), pos.y(), count)
            self.node.input_view.grNode.show()
            self.node.input_view_edge.grEdge.show()
            self.node.input_view_edge.end_socket.socket_type = SocketType.VIEW_SOCKET
        else:
            self.node.input_view.grNode.hide()
            self.node.input_view_edge.grEdge.hide()
            self.node.input_view_edge.end_socket.socket_type = SocketType.DISABLED_SOCKET
        self.updateView()

    def updateView(self):
        if self.ViewToggle.isChecked():
            self.used_view = self.picker_view
        else:
            self.used_view = self.chain_view
        if self.used_view == []:
            self.ViewCheck.setChecked(False)
        else:
            self.ViewCheck.setChecked(True)
        self.node.content.updateRun(chain_update=True)
        self.updateViewValues()

    def updateFlyPicker(self):
        if self.FlyToggle.isChecked():
            pos = self.node.pos
            count = len(self.node.picker_inputs)
            if self.node.node_input is not None:
                count += 1
            self.node.input_fly.setSelfPos(pos.x(), pos.y(), count)
            self.node.input_fly.grNode.show()
            self.node.input_fly_edge.grEdge.show()
            self.node.input_fly_edge.end_socket.socket_type = SocketType.FLY_SOCKET
        else:
            self.node.input_fly.grNode.hide()
            self.node.input_fly_edge.grEdge.hide()
            self.node.input_fly_edge.end_socket.socket_type = SocketType.DISABLED_SOCKET
        self.updateFly()

    def updateFly(self):
        if self.FlyToggle.isChecked():
            self.used_fly_groups = self.picker_fly_groups
        else:
            self.used_fly_groups = self.chain_fly_groups
        if len(self.used_fly_groups) <= 1:
            self.FlyCheck.setChecked(False)
        else:
            self.FlyCheck.setChecked(True)
        self.node.content.updateRun(chain_update=True)
        self.updateFlyValues()

    def updateDelete(self):
        self.used_delete = self.picker_delete
        if self.used_delete == []:
            self.DeleteCheck.setChecked(False)
        else:
            self.DeleteCheck.setChecked(True)
        self.node.content.updateRun(chain_update=True)

    def updateOutputValues(self, update_model:bool=True, update_color:bool=True, update_center:bool=True, Update_view:bool=True, update_fly:bool=True, update_frames:bool=True, check_update:bool=True):
        #pass frames, model, color, center, view, fly. check run when finished
        #frames:
        if NodeType(self.node.nodeType) == NodeType.Wait:
            if int(self.node.content.Frames.getText()) > 0 and int(self.node.content.Frames.getText()) > self.accumulated_frames:
                self.lFrames.setText(f"Frames: {int(self.node.content.Frames.getText())}")
                self.used_frames = int(self.node.content.Frames.getText())
            else:
                self.lFrames.setText(f"Frames: {self.accumulated_frames}")
                self.used_frames = self.accumulated_frames
            self.lTotalFrames.setText(f"Total Frames: {self.total_frames}")
            self.lLength.setText(f"Length: {self.convertTime(self.total_frames / int(self.node.scene.parent.nodeEnd.content.Framerate.getText()))}")
        elif NodeType(self.node.nodeType) == NodeType.End:
            self.lFrames.setText(f"Frames: {self.accumulated_frames}")
            self.lTotalFrames.setText(f"Total Frames: {self.total_frames}")
            self.lLength.setText(f"Length: {self.convertTime(self.total_frames / int(self.node.content.Framerate.getText()))}")
        elif NodeType(self.node.nodeType) == NodeType.Fly:
            frames = 0
            for frame in self.node.content.transition_frames:
                frames += int(frame)
            self.used_frames = frames
            self.lFrames.setText(f"Frames: {self.accumulated_frames + self.used_frames}")
            self.lTotalFrames.setText(f"Total Frames: {self.total_frames}")
            self.lLength.setText(f"Length: {self.convertTime((self.total_frames + self.used_frames) / int(self.node.scene.parent.nodeEnd.content.Framerate.getText()))}")
        else:
            if hasattr(self.node.content, "Frames"):
                self.used_frames = int(self.node.content.Frames.getText())
            else: 
                self.used_frames = 0
            self.lFrames.setText(f"Frames: {self.accumulated_frames + self.used_frames}")
            self.lTotalFrames.setText(f"Total Frames: {self.total_frames + self.used_frames}")
            self.lLength.setText(f"Length: {self.convertTime((self.total_frames + self.used_frames) / int(self.node.scene.parent.nodeEnd.content.Framerate.getText()))}")
        no_output = True
        
        if self.node.node_output is not None:
            if self.node.node_output.hasEdge():
                no_output = False
                self.node.node_output.edge.end_socket.node.summary.chain_model = self.used_model
                if (update_model and check_update) or not check_update:
                    if hasattr(self.node.node_output.edge.end_socket.node.summary, "ModelToggle"):
                        if not self.node.node_output.edge.end_socket.node.summary.ModelToggle.isChecked():
                            self.node.node_output.edge.end_socket.node.summary.used_model = self.used_model
                            if self.node.node_output.edge.end_socket.node.summary.used_model == []:
                                self.node.node_output.edge.end_socket.node.summary.ModelCheck.setChecked(False)
                            else:
                                self.node.node_output.edge.end_socket.node.summary.ModelCheck.setChecked(True)
                        else:
                            update_model = False
                    else:
                        self.node.node_output.edge.end_socket.node.summary.used_model = self.used_model
                self.node.node_output.edge.end_socket.node.summary.chain_color_groups = self.used_color_groups
                if (update_color and check_update) or not check_update:
                    if hasattr(self.node.node_output.edge.end_socket.node.summary, "ColorToggle"):
                        if not self.node.node_output.edge.end_socket.node.summary.ColorToggle.isChecked():
                            self.node.node_output.edge.end_socket.node.summary.used_color_groups = self.used_color_groups
                            self.node.node_output.edge.end_socket.node.content.addGroups()
                            if self.node.node_output.edge.end_socket.node.summary.used_color_groups == []:
                                self.node.node_output.edge.end_socket.node.summary.ColorCheck.setChecked(False)
                            else:
                                self.node.node_output.edge.end_socket.node.summary.ColorCheck.setChecked(True)
                        else:
                            update_color = False
                    else:
                        self.node.node_output.edge.end_socket.node.summary.used_color_groups = self.used_color_groups
                self.node.node_output.edge.end_socket.node.summary.chain_center = self.used_center
                if (update_center and check_update) or not check_update:
                    if hasattr(self.node.node_output.edge.end_socket.node.summary, "CenterToggle"):
                        if not self.node.node_output.edge.end_socket.node.summary.CenterToggle.isChecked():
                            self.node.node_output.edge.end_socket.node.summary.used_center = self.used_center
                            if self.node.node_output.edge.end_socket.node.summary.used_center == []:
                                self.node.node_output.edge.end_socket.node.summary.CenterCheck.setChecked(False)
                            else:
                                self.node.node_output.edge.end_socket.node.summary.CenterCheck.setChecked(True)
                        else:
                            update_center = False
                    else:
                        self.node.node_output.edge.end_socket.node.summary.used_center = self.used_center
                self.node.node_output.edge.end_socket.node.summary.chain_view = self.used_view
                if (Update_view and check_update) or not check_update:
                    if hasattr(self.node.node_output.edge.end_socket.node.summary, "ViewToggle"):
                        if not self.node.node_output.edge.end_socket.node.summary.ViewToggle.isChecked():
                            self.node.node_output.edge.end_socket.node.summary.used_view = self.used_view
                            if self.node.node_output.edge.end_socket.node.summary.used_view == []:
                                self.node.node_output.edge.end_socket.node.summary.ViewCheck.setChecked(False)
                            else:
                                self.node.node_output.edge.end_socket.node.summary.ViewCheck.setChecked(True)
                        else:
                            Update_view = False
                    else:
                        self.node.node_output.edge.end_socket.node.summary.used_view = self.used_view
                self.node.node_output.edge.end_socket.node.summary.chain_fly_groups = self.used_fly_groups
                if (update_fly and check_update) or not check_update:
                    if hasattr(self.node.node_output.edge.end_socket.node.summary, "FlyToggle"):
                        self.node.node_output.edge.end_socket.node.content.addFlySequences()
                        if not self.node.node_output.edge.end_socket.node.summary.FlyToggle.isChecked():
                            self.node.node_output.edge.end_socket.node.summary.used_fly_groups = self.used_fly_groups
                            if self.node.node_output.edge.end_socket.node.summary.used_fly_groups == []:
                                self.node.node_output.edge.end_socket.node.summary.FlyCheck.setChecked(False)
                            else:
                                self.node.node_output.edge.end_socket.node.summary.FlyCheck.setChecked(True)
                        else:
                            update_fly = False
                    else:
                        self.node.node_output.edge.end_socket.node.summary.used_fly_groups = self.used_fly_groups
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
                self.node.node_output.edge.end_socket.node.summary.updateOutputValues(update_model, update_color, update_center, Update_view, update_fly, update_frames, check_update)
        if no_output:
            self.updateChainRun()
                
    def updateModelValues(self):
        no_output=True
        if self.node.node_output is not None:
            if self.node.node_output.hasEdge():
                no_output=False        
                self.node.node_output.edge.end_socket.node.summary.chain_model = self.used_model
                if hasattr(self.node.node_output.edge.end_socket.node.summary, "ModelToggle"):
                    if not self.node.node_output.edge.end_socket.node.summary.ModelToggle.isChecked():
                        self.node.node_output.edge.end_socket.node.summary.used_model = self.used_model
                        if self.node.node_output.edge.end_socket.node.summary.used_model == []:
                            self.node.node_output.edge.end_socket.node.summary.ModelCheck.setChecked(False)
                        else:
                            self.node.node_output.edge.end_socket.node.summary.ModelCheck.setChecked(True)
                        self.node.node_output.edge.end_socket.node.summary.updateModelValues()
                else:
                    self.node.node_output.edge.end_socket.node.summary.used_model = self.used_model
                    self.node.node_output.edge.end_socket.node.summary.updateModelValues()
                self.node.node_output.edge.end_socket.node.content.updateRun(chain_update=True)        
        if no_output:
            self.updateChainRun()

    def updateColorValues(self):
        no_output=True
        if self.node.node_output is not None:
            if self.node.node_output.hasEdge():
                no_output=False
                self.node.node_output.edge.end_socket.node.summary.chain_color_groups = self.used_color_groups
                if hasattr(self.node.node_output.edge.end_socket.node.summary, "ColorToggle"):
                    if not self.node.node_output.edge.end_socket.node.summary.ColorToggle.isChecked():
                        self.node.node_output.edge.end_socket.node.summary.used_color_groups = self.used_color_groups
                        self.node.node_output.edge.end_socket.node.content.addGroups()
                        if self.node.node_output.edge.end_socket.node.summary.used_color_groups == []:
                            self.node.node_output.edge.end_socket.node.summary.ColorCheck.setChecked(False)
                        else:
                            self.node.node_output.edge.end_socket.node.summary.ColorCheck.setChecked(True)
                        self.node.node_output.edge.end_socket.node.summary.updateColorValues()
                else:
                    self.node.node_output.edge.end_socket.node.summary.used_color_groups = self.used_color_groups
                    self.node.node_output.edge.end_socket.node.summary.updateColorValues()
                self.node.node_output.edge.end_socket.node.content.updateRun(chain_update=True)      
        if no_output:
            self.updateChainRun()

    def updateCenterValues(self):
        no_output=True
        if self.node.node_output is not None:
            if self.node.node_output.hasEdge():
                no_output=False
                self.node.node_output.edge.end_socket.node.summary.chain_center = self.used_center
                if hasattr(self.node.node_output.edge.end_socket.node.summary, "CenterToggle"):
                    if not self.node.node_output.edge.end_socket.node.summary.CenterToggle.isChecked():
                        self.node.node_output.edge.end_socket.node.summary.used_center = self.used_center
                        if self.node.node_output.edge.end_socket.node.summary.used_center == []:
                            self.node.node_output.edge.end_socket.node.summary.CenterCheck.setChecked(False)
                        else:
                            self.node.node_output.edge.end_socket.node.summary.CenterCheck.setChecked(True)
                        self.node.node_output.edge.end_socket.node.summary.updateCenterValues()
                else:
                    self.node.node_output.edge.end_socket.node.summary.used_center = self.used_center
                    self.node.node_output.edge.end_socket.node.summary.updateCenterValues()
                self.node.node_output.edge.end_socket.node.content.updateRun(chain_update=True)    
        if no_output:
            self.updateChainRun()

    def updateViewValues(self):
        no_output=True
        if self.node.node_output is not None:
            if self.node.node_output.hasEdge():
                no_output=False
                self.node.node_output.edge.end_socket.node.summary.chain_view = self.used_view
                if hasattr(self.node.node_output.edge.end_socket.node.summary, "ViewToggle"):
                    if not self.node.node_output.edge.end_socket.node.summary.ViewToggle.isChecked():
                        self.node.node_output.edge.end_socket.node.summary.used_view = self.used_view
                        if self.node.node_output.edge.end_socket.node.summary.used_view == []:
                            self.node.node_output.edge.end_socket.node.summary.ViewCheck.setChecked(False)
                        else:
                            self.node.node_output.edge.end_socket.node.summary.ViewCheck.setChecked(True)
                        self.node.node_output.edge.end_socket.node.summary.updateViewValues()
                else:
                    self.node.node_output.edge.end_socket.node.summary.used_view = self.used_view
                    self.node.node_output.edge.end_socket.node.summary.updateViewValues()
                self.node.node_output.edge.end_socket.node.content.updateRun(chain_update=True)    
        if no_output:
            self.updateChainRun()

    def updateFlyValues(self):
        no_output=True
        if self.node.node_output is not None:
            if self.node.node_output.hasEdge():
                no_output=False
                self.node.node_output.edge.end_socket.node.summary.chain_fly_groups = self.used_fly_groups
                if hasattr(self.node.node_output.edge.end_socket.node.summary, "FlyToggle"):
                    if not self.node.node_output.edge.end_socket.node.summary.FlyToggle.isChecked():
                        self.node.node_output.edge.end_socket.node.summary.used_fly_groups = self.used_fly_groups
                        self.node.node_output.edge.end_socket.node.content.addFlySequences()
                        if self.node.node_output.edge.end_socket.node.summary.used_fly_groups == []:
                            self.node.node_output.edge.end_socket.node.summary.FlyCheck.setChecked(False)
                        else:
                            self.node.node_output.edge.end_socket.node.summary.FlyCheck.setChecked(True)
                        self.node.node_output.edge.end_socket.node.summary.updateFlyValues()
                else:
                    self.node.node_output.edge.end_socket.node.summary.used_fly_groups = self.used_fly_groups
                    self.node.node_output.edge.end_socket.node.summary.updateFlyValues()
                self.node.node_output.edge.end_socket.node.content.updateRun(chain_update=True)    
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
            self.lTotalFrames.setText(f"Total Frames: {self.total_frames}")
            self.lLength.setText(f"Length: {self.convertTime(self.total_frames / int(self.node.scene.parent.nodeEnd.content.Framerate.getText()))}")
        elif NodeType(self.node.nodeType) == NodeType.End:
            self.lFrames.setText(f"Frames: {self.accumulated_frames}")
            self.lTotalFrames.setText(f"Total Frames: {self.total_frames}")
            self.lLength.setText(f"Length: {self.convertTime(self.total_frames / int(self.node.content.Framerate.getText()))}")
        elif NodeType(self.node.nodeType) == NodeType.Fly:
            frames = 0
            for frame in self.node.content.transition_frames:
                frames += int(frame)
            self.used_frames = frames
            self.lFrames.setText(f"Frames: {self.accumulated_frames + self.used_frames}")
            self.lTotalFrames.setText(f"Total Frames: {self.total_frames + self.used_frames}")
            self.lLength.setText(f"Length: {self.convertTime((self.total_frames + self.used_frames) / int(self.node.scene.parent.nodeEnd.content.Framerate.getText()))}")
        else:
            if hasattr(self.node.content, "Frames"):
                self.used_frames = int(self.node.content.Frames.getText())
            else: 
                self.used_frames = 0
            self.lFrames.setText(f"Frames: {self.accumulated_frames + self.used_frames}")
            self.lTotalFrames.setText(f"Total Frames: {self.total_frames + self.used_frames}")
            self.lLength.setText(f"Length: {self.convertTime((self.total_frames + self.used_frames) / int(self.node.scene.parent.nodeEnd.content.Framerate.getText()))}")
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

    def resetOutputValues(self, reset_model:bool=True, reset_color:bool=True, reset_center:bool=True, reset_view:bool=True, reset_fly:bool=True, reset_frames:bool=True, update_frames:bool=True):
        if NodeType(self.node.nodeType) == NodeType.Wait:
            if int(self.node.content.Frames.getText()) > 0 and int(self.node.content.Frames.getText()) > self.accumulated_frames:
                self.lFrames.setText(f"Frames: {int(self.node.content.Frames.getText())}")
                self.used_frames = int(self.node.content.Frames.getText())
            else:
                self.lFrames.setText(f"Frames: {self.accumulated_frames}")
                self.used_frames = self.accumulated_frames
            self.lTotalFrames.setText(f"Total Frames: {self.total_frames}")
            self.lLength.setText(f"Length: {self.convertTime(self.total_frames / int(self.node.scene.parent.nodeEnd.content.Framerate.getText()))}")
        elif NodeType(self.node.nodeType) == NodeType.End:
            self.lFrames.setText(f"Frames: {self.accumulated_frames}")
            self.lTotalFrames.setText(f"Total Frames: {self.total_frames}")
            self.lLength.setText(f"Length: {self.convertTime(self.total_frames / int(self.node.content.Framerate.getText()))}")
        elif NodeType(self.node.nodeType) == NodeType.Fly:
            frames = 0
            for frame in self.node.content.transition_frames:
                frames += int(frame)
            self.used_frames = frames
            self.lFrames.setText(f"Frames: {self.accumulated_frames + self.used_frames}")
            self.lTotalFrames.setText(f"Total Frames: {self.total_frames + self.used_frames}")
            self.lLength.setText(f"Length: {self.convertTime((self.total_frames + self.used_frames) / int(self.node.scene.parent.nodeEnd.content.Framerate.getText()))}")
        else:
            if hasattr(self.node.content, "Frames"):
                self.used_frames = int(self.node.content.Frames.getText())
            else: 
                self.used_frames = 0
            self.lFrames.setText(f"Frames: {self.accumulated_frames + self.used_frames}")
            self.lTotalFrames.setText(f"Total Frames: {self.total_frames + self.used_frames}")
            self.lLength.setText(f"Length: {self.convertTime((self.total_frames + self.used_frames) / int(self.node.scene.parent.nodeEnd.content.Framerate.getText()))}")
        no_output=True
        if self.node.node_output is not None:
            if self.node.node_output.hasEdge():
                no_output=False
                self.node.node_output.edge.end_socket.node.summary.chain_model = []
                if reset_model:
                    if hasattr(self.node.node_output.edge.end_socket.node.summary, "ModelToggle"):
                        if not self.node.node_output.edge.end_socket.node.summary.ModelToggle.isChecked():
                            self.node.node_output.edge.end_socket.node.summary.used_model = []
                            self.node.node_output.edge.end_socket.node.summary.ModelCheck.setChecked(False)
                        else:
                            reset_model = False
                    else:
                        self.node.node_output.edge.end_socket.node.summary.used_model = []
                if reset_color:
                    self.node.node_output.edge.end_socket.node.summary.chain_color_groups = []
                    if hasattr(self.node.node_output.edge.end_socket.node.summary, "ColorToggle"):
                        if not self.node.node_output.edge.end_socket.node.summary.ColorToggle.isChecked():
                            self.node.node_output.edge.end_socket.node.summary.used_color_groups = []
                            self.node.node_output.edge.end_socket.node.summary.ColorCheck.setChecked(False)
                        else:
                            reset_color = False
                    else:
                        self.node.node_output.edge.end_socket.node.summary.used_color_groups = []
                if reset_center:
                    self.node.node_output.edge.end_socket.node.summary.chain_center = []
                    if hasattr(self.node.node_output.edge.end_socket.node.summary, "CenterToggle"):
                        if not self.node.node_output.edge.end_socket.node.summary.CenterToggle.isChecked():
                            self.node.node_output.edge.end_socket.node.summary.used_center = []
                            self.node.node_output.edge.end_socket.node.summary.CenterCheck.setChecked(False)
                        else:
                            reset_center = False
                    else:
                        self.node.node_output.edge.end_socket.node.summary.used_center = []
                if reset_view:
                    self.node.node_output.edge.end_socket.node.summary.chain_view = []
                    if hasattr(self.node.node_output.edge.end_socket.node.summary, "ViewToggle"):
                        if not self.node.node_output.edge.end_socket.node.summary.ViewToggle.isChecked():
                            self.node.node_output.edge.end_socket.node.summary.used_view = []
                            self.node.node_output.edge.end_socket.node.summary.ViewCheck.setChecked(False)
                        else:
                            reset_view = False
                    else:
                        self.node.node_output.edge.end_socket.node.summary.used_view = []
                if reset_fly:
                    self.node.node_output.edge.end_socket.node.summary.chain_fly_groups = []
                    if hasattr(self.node.node_output.edge.end_socket.node.summary, "FlyToggle"):
                        if not self.node.node_output.edge.end_socket.node.summary.FlyToggle.isChecked():
                            self.node.node_output.edge.end_socket.node.summary.used_fly_groups = []
                            self.node.node_output.edge.end_socket.node.summary.FlyCheck.setChecked(False)
                        else:
                            reset_fly = False
                    else:
                        self.node.node_output.edge.end_socket.node.summary.used_fly_groups = []
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
                self.node.node_output.edge.end_socket.node.summary.resetOutputValues(reset_model, reset_color, reset_center, reset_view, reset_fly, reset_frames, update_frames)
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