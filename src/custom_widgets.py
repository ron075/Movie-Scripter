from __future__ import annotations

from PyQt6.QtCore import *
from PyQt6.QtCore import QEvent
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
import re
import random
from .stylesheets import *
from .enum_classes import *
from chimerax.core import models
from chimerax.markers import markers
from chimerax.label import label2d, label3d
from chimerax.atomic import structure
from chimerax.map import volume
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .graphics_scene import Scene
    from .node_base import Node
    from .main_window import NodeEditor

class QColorMap(QWidget):
    def __init__(self, colormap_height:int, parent=None):

        super().__init__(parent)

        self.colormap_height = colormap_height

        self.colorRangeLibrary = {
            "BrBG":[ColorRangeType.Expert, [QColor("#543005"), QColor("#8c510a"), QColor("#bf812d"), QColor("#dfc27d"), QColor("#f6e8c3"), QColor("#f5f5f5"), QColor("#c7eae5"), QColor("#80cdc1"), QColor("#35978f"), QColor("#01665e"), QColor("#003c30")]],
            "Cool":[ColorRangeType.Simple, [QColor("#00ffff"), QColor("#11eeff"), QColor("#22ddff"), QColor("#33ccff"), QColor("#44bbff"), QColor("#55aaff"), QColor("#6699ff"), QColor("#7788ff"), QColor("#8877ff"), QColor("#9966ff"), QColor("#aa55ff"), QColor("#bb44ff"), QColor("#cc33ff"), QColor("#dd22ff"), QColor("#ee11ff"), QColor("#ff00ff")]],
            "Greys":[ColorRangeType.Expert, [QColor("#000000"), QColor("#111111"), QColor("#222222"), QColor("#333333"), QColor("#444444"), QColor("#555555"), QColor("#666666"), QColor("#777777"), QColor("#888888"), QColor("#999999"), QColor("#aaaaaa"), QColor("#bbbbbb"), QColor("#cccccc"), QColor("#dddddd"), QColor("#eeeeee"), QColor("#ffffff")]],
            "Hot":[ColorRangeType.Simple, [QColor("#2b0000"), QColor("#550000"), QColor("#800000"), QColor("#aa0000"), QColor("#d50000"), QColor("#ff0000"), QColor("#ff2b00"), QColor("#ff5500"), QColor("#ff8000"), QColor("#ffaa00"), QColor("#ffd500"), QColor("#ffff00"), QColor("#ffff40"), QColor("#ffff80"), QColor("#ffffbf"), QColor("#ffffff")]],
            "Jet":[ColorRangeType.Simple, [QColor("#0000bf"), QColor("#0000ff"), QColor("#003fff"), QColor("#007fff"), QColor("#00bfff"), QColor("#00ffff"), QColor("#3fffff"), QColor("#7fffbf"), QColor("#bfff7f"), QColor("#ffff3f"), QColor("#ffff00"), QColor("#ffbf00"), QColor("#ff7f00"), QColor("#ff3f00"), QColor("#ff0000"), QColor("#bf0000")]],
            "Pink":[ColorRangeType.Expert, [QColor("#3c0000"), QColor("#643535"), QColor("#814c4c"), QColor("#985d5d"), QColor("#ac6b6b"), QColor("#be7878"), QColor("#c69184"), QColor("#cda68e"), QColor("#d4b898"), QColor("#dbc9a1"), QColor("#e1d9aa"), QColor("#e8e8b2"), QColor("#eeeec9"), QColor("#f4f4dc"), QColor("#fafaef"), QColor("#ffffff")]],
            "PiYG":[ColorRangeType.Expert, [QColor("#8e0152"), QColor("#c51b7d"), QColor("#de77ae"), QColor("#f1b6da"), QColor("#fde0ef"), QColor("#f7f7f7"), QColor("#e6f5d0"), QColor("#b8e186"), QColor("#7fbc41"), QColor("#4d9221"), QColor("#276419")]],
            "Plasma":[ColorRangeType.Expert, [QColor("#0c0786"), QColor("#1b068c"), QColor("#250591"), QColor("#2f0495"), QColor("#380499"),
             QColor("#42039d"), QColor("#4a02a0"), QColor("#5201a3"), QColor("#5a00a5"), QColor("#6400a7"),
             QColor("#6c00a8"), QColor("#7300a8"), QColor("#7b02a8"), QColor("#8204a7"), QColor("#8b09a4"),
             QColor("#920fa2"), QColor("#99149f"), QColor("#9f1a9b"), QColor("#a72197"), QColor("#ad2692"),
             QColor("#b22c8e"), QColor("#b83289"), QColor("#bd3784"), QColor("#c33e7f"), QColor("#c8447a"),
             QColor("#cd4975"), QColor("#d14f71"), QColor("#d7566c"), QColor("#db5b67"), QColor("#df6163"),
             QColor("#e3675f"), QColor("#e66d5a"), QColor("#ea7455"), QColor("#ed7b51"), QColor("#f0814d"),
             QColor("#f38748"), QColor("#f68f43"), QColor("#f8963f"), QColor("#fa9d3a"), QColor("#fba436"),
             QColor("#fcac32"), QColor("#fdb52d"), QColor("#fdbc2a"), QColor("#fdc427"), QColor("#fccc25"),
             QColor("#fad624"), QColor("#f8df24"), QColor("#f5e726"), QColor("#f2f026"), QColor("#eff821")]],
            "RdBu":[ColorRangeType.Expert, [QColor("#67001f"), QColor("#b2182b"), QColor("#d6604d"), QColor("#f4a582"), QColor("#fddbc7"), QColor("#f7f7f7"), QColor("#d1e5f0"), QColor("#92c5de"), QColor("#4393c3"), QColor("#2166ac"), QColor("#053061")]],
            "Spectral":[ColorRangeType.Simple, [QColor("#9e0142"), QColor("#d53e4f"), QColor("#f46d43"), QColor("#fdae61"), QColor("#fee08b"), QColor("#ffffbf"), QColor("#e6f598"), QColor("#abdda4"), QColor("#66c2a5"), QColor("#3288bd"), QColor("#5e4fa2")]],
            "Tol":[ColorRangeType.Simple, [QColor("#332288"), QColor("#117733"), QColor("#44AA99"), QColor("#88CCEE"), QColor("#DDCC77"), QColor("#CC6677"), QColor("#AA4499"), QColor("#882255")]],
            "Viridis":[ColorRangeType.Expert, [QColor("#440154"), QColor("#471164"), QColor("#481f70"), QColor("#472d7b"), QColor("#443a83"),
             QColor("#404688"), QColor("#3b528b"), QColor("#365d8d"), QColor("#31688e"), QColor("#2c728e"),
             QColor("#287c8e"), QColor("#24868e"), QColor("#21908c"), QColor("#1f9a8a"), QColor("#20a486"),
             QColor("#27ad81"), QColor("#35b779"), QColor("#47c16e"), QColor("#5dc863"), QColor("#75d054"),
             QColor("#8fd744"), QColor("#aadc32"), QColor("#c7e020"), QColor("#e3e418"), QColor("#fde725")]]
        }
        self.widget_layout = QVBoxLayout()
        
        self.colormap_label = QLabel()        
        self.colormap_label.setSizePolicy(QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.MinimumExpanding)
        self.colormap_label.setFixedHeight(self.colormap_height)
        self.widget_layout.addWidget(self.colormap_label)
        
    def updateColormap(self, currentRangeKey:str):
        self.colorMap = self.colorRangeLibrary[currentRangeKey][1]
        self.gradient = QLinearGradient(0, 0, self.colormap_label.size().width(), 0)

        stylesheet = "QLabel { background-color :qlineargradient(x1:0, x2:1"
        for i in range(len(self.colorMap)):
            self.gradient.setColorAt(i / (len(self.colorMap) - 1), self.colorMap[i])
            stylesheet += f", stop:{i / (len(self.colorMap) - 1)} {self.colorMap[i].name()}"
        stylesheet += "); border:1px solid black}"

        self.colormap_label.setStyleSheet(stylesheet)  

    def get_colors(self, rangeKey:str, group_count:int, random_colors:bool) -> list[QColor]:
        group_step = 1.0 / (group_count + 1)
        color_step = 1.0 / (len(self.colorRangeLibrary[rangeKey][1]) - 1)
        color_list = []
        for i in range(1, group_count + 1):
            interval = len(self.colorRangeLibrary[rangeKey][1]) - 1
            value = (i * group_step if not random_colors else random.uniform(0, 1))
            for j in range(0, len(self.colorRangeLibrary[rangeKey][1])):
                if value <= j * color_step:
                    interval = j - 1
                    break
            percentage = (value - color_step * interval) / color_step
            color_list.append(QColor(self.interpolate(self.colorRangeLibrary[rangeKey][1][interval], self.colorRangeLibrary[rangeKey][1][interval + 1], percentage)))
        return color_list
    
    def interpolate(self, start:QColor, end:QColor, ratio):
        r = (int)(ratio * start.red() + (1 - ratio) * end.red())
        g = (int)(ratio * start.green() + (1 - ratio) * end.green())
        b = (int)(ratio * start.blue() + (1 - ratio) * end.blue())
        a = 255
        color = QColor().fromRgb(r, g, b, a)
        return color.name()

class QNumEdit(QWidget):
    def __init__(self, min:int=None, max:int=None, step:int=1, decimals:int=0, horizontal:bool=True, label:str="", addSlider:bool=False, parent=None):

        super().__init__(parent)

        self.min = min
        self.max = max
        self.horizontal = horizontal
        self.decimals = decimals
        self.addSlider = addSlider
        self.text = ""
        self.label = label
        self.multi = 10 ** self.decimals
        if step < 1:
            self.step = 1 / self.multi
        else:
            self.step = step / self.multi

        self.widget_layout = QVBoxLayout()

        self.widget_layout.setSpacing(4)

        self.Label = QLabel(self.label)
        if self.addSlider:
            self.Slider = QSlider(orientation=Qt.Orientation.Horizontal if self.horizontal else Qt.Orientation.Vertical)
            if self.min is not None:
                self.Min = QLabel(str(int(self.min) if self.decimals <= 0 else round(self.min, self.decimals)))
                self.Slider.setMinimum(int(self.min * self.multi))
            if self.max is not None:
                self.Max = QLabel(str(int(self.max) if self.decimals <= 0 else round(self.max, self.decimals)))
                self.Slider.setMaximum(int(self.max * self.multi))

            if self.min is not None and self.max is not None:
                self.Slider.setValue(int((self.min + self.max) / 2 * self.multi))
            elif self.min is not None:
                self.Slider.setValue(int(self.min * self.multi))
            elif self.min is not None:
                self.Slider.setValue(int(self.max * self.multi))
            else:
                self.Slider.setValue(0)
            self.Slider.sliderMoved.connect(self.updateTextFromSlider)
        self.Text = QLineEdit()
        if addSlider:
            value = round(self.Slider.value() / self.multi, self.decimals)
            if self.decimals <= 0:
                value = int(value)
            self.Text.setText(str(value))
        else:
            if self.min is not None and self.max is not None:
                value = round((self.min + self.max) / 2 * self.multi, self.decimals)
                if self.decimals <= 0:
                    value = int(value)
                self.Text.setText(str(value))
            elif self.min is not None:
                value = round(self.min * self.multi, self.decimals)
                if self.decimals <= 0:
                    value = int(value)
                self.Text.setText(str(value))
            elif self.min is not None:
                value = round(self.max * self.multi, self.decimals)
                if self.decimals <= 0:
                    value = int(value)
                self.Text.setText(str(value))
            else:
                self.Text.setText("0")
        if self.decimals > 0:
            if self.min is not None and self.max is not None:
                self.Text.setValidator(QDoubleValidator(bottom=self.min, top=self.max, decimals=self.decimals))
            elif self.min is not None:
                self.Text.setValidator(QDoubleValidator(bottom=self.min, decimals=self.decimals))
            elif self.min is not None:
                self.Text.setValidator(QDoubleValidator(top=self.max, decimals=self.decimals))
            else:
                self.Text.setValidator(QDoubleValidator(decimals=self.decimals))
        else:
            if self.min is not None and self.max is not None:
                self.Text.setValidator(QIntValidator(bottom=self.min, top=self.max))
            elif self.min is not None:
                self.Text.setValidator(QIntValidator(bottom=self.min))
            elif self.min is not None:
                self.Text.setValidator(QIntValidator(top=self.max))
            else:
                self.Text.setValidator(QIntValidator())
        self.Text.setFixedWidth(40)
        self.Text.textChanged.connect(self.updateSliderFromText)
        self.Plus = QPushButton("+")
        self.Plus.setFixedWidth(20)
        self.Plus.clicked.connect(self.increaseValueByStep)
        self.Minus = QPushButton("-")
        self.Minus.setFixedWidth(20)
        self.Minus.clicked.connect(self.decreaseValueByStep)

        if self.addSlider:
            self.layoutH1 = QHBoxLayout()
            if self.min is not None:
                self.layoutH1.addWidget(self.Min)
            self.layoutH1.addWidget(self.Slider)
            if self.max is not None:
                self.layoutH1.addWidget(self.Max)
        self.layoutH2 = QHBoxLayout()
        self.layoutH2V1 = QVBoxLayout()
        self.layoutH2V1.addWidget(self.Plus, alignment=Qt.AlignmentFlag.AlignCenter)
        self.layoutH2V1.addWidget(self.Minus, alignment=Qt.AlignmentFlag.AlignCenter)
        self.layoutH2.addLayout(self.layoutH2V1)
        self.layoutH2.addWidget(self.Text, alignment=Qt.AlignmentFlag.AlignCenter)
            
        self.widget_layout.addWidget(self.Label, alignment=Qt.AlignmentFlag.AlignCenter)
        if self.addSlider:
            self.widget_layout.addLayout(self.layoutH1)
        self.widget_layout.addLayout(self.layoutH2)

    def increaseValueByStep(self):
        value = (float(self.getText()) + self.step)
        if self.min is not None:
            if value < self.min:
                value = self.min
        if self.max is not None:
            if value > self.max:
                value = self.max
        if self.addSlider:
            self.Slider.setValue(int(value * self.multi))
        self.Text.setText(str(int(value) if self.decimals <= 0 else round(value, self.decimals)))

    def decreaseValueByStep(self):
        value = (float(self.getText()) - self.step)
        if self.min is not None:
            if value < self.min:
                value = self.min
        if self.max is not None:
            if value > self.max:
                value = self.max
        if self.addSlider:
            self.Slider.setValue(int(value * self.multi))
        self.Text.setText(str(int(value) if self.decimals <= 0 else round(value, self.decimals)))

    def updateSliderFromText(self, text):
        if text != "":
            value = round(float(text), self.decimals)
            if self.decimals <= 0:
                value = int(value)
            if self.min is not None:
                if value < self.min:
                    value = self.min
                    self.Text.setText(str(value))
            if self.max is not None:
                if value > self.max:
                    value = self.max
                    self.Text.setText(str(value))
            if self.addSlider:
                self.Slider.setValue(int(value * self.multi))
 
    def updateTextFromSlider(self, value):
        if value is None:
            value = self.Slider.value()
        value = value / self.multi
        self.Text.setText(str(int(value) if self.decimals <= 0 else round(value, self.decimals)))

    def setMin(self, min_value:int|float):
        self.min = min_value
        self.Text.setValidator(QIntValidator(bottom=min_value))

    def setMax(self, max_value:int|float):
        self.max = max_value
        self.Text.setValidator(QIntValidator(top=max_value))

    def setText(self, text:str):
        value = round(float(text), self.decimals)
        if self.decimals <= 0:
            value = int(value)
        self.Text.setText(str(value))
        if self.min is not None:
            if value < self.min:
                value = self.min
                self.Text.setText(str(value))
        if self.max is not None:
            if value > self.max:
                value = self.max
                self.Text.setText(str(value))
        if self.addSlider:
            self.Slider.setValue(int(value * self.multi))

    def getText(self) -> str:
        text = self.Text.text()
        if self.Text.text() == "":
            text = "0"
        return text
            
    def setEnabled(self, a0:bool):
        if self.addSlider:
            self.Slider.setEnabled(a0)
        self.Text.setEnabled(a0)
        self.Plus.setEnabled(a0)
        self.Minus.setEnabled(a0)
        return super().setEnabled(a0)
    
    def removeWidgets(self):
        if self.addSlider:
            if self.min is not None:
                self.layoutH1.removeWidget(self.Min)
            self.layoutH1.removeWidget(self.Slider)
            if self.max is not None:
                self.layoutH1.removeWidget(self.Max)
            self.layoutH2V1.removeWidget(self.Plus)
            self.layoutH2V1.removeWidget(self.Minus)
            self.layoutH2.removeWidget(self.Text)
        else:
            self.layoutH2V1.removeWidget(self.Plus)
            self.layoutH2V1.removeWidget(self.Minus)
            self.layoutH2.removeWidget(self.Text)
            
    
    def addWidgets(self):
        if self.addSlider:
            if self.min is not None:
                self.layoutH1.addWidget(self.Min)
            self.layoutH1.addWidget(self.Slider)
            if self.max is not None:
                self.layoutH1.addWidget(self.Max)
            self.layoutH2V1.addWidget(self.Plus)
            self.layoutH2V1.addWidget(self.Minus)
            self.layoutH2.addWidget(self.Text)
        else:
            self.layoutH2V1.addWidget(self.Plus)
            self.layoutH2V1.addWidget(self.Minus)
            self.layoutH2.addWidget(self.Text)

class QTreeViewSelector(QWidget):
    def __init__(self, session, scene:Scene, node:Node, all_views:bool, selector_type:NodePickerType=NodePickerType.ModelPicker, parent=None):
        super().__init__(parent)

        self.session = session
        self.scene = scene
        self.node = node

        self.selected_model = []
        self.selected_color_groups = []
        self.selected_2dlabel = []
        self.selected_3dlabel = []
        self.selected_view = []

        self.selected_fly_groups = []

        self.all_views = all_views

        self.selector_type = selector_type

        self.widget_layout = QVBoxLayout()
        self.widget_layout.setSpacing(4)
        self.layoutH1 = QHBoxLayout()   
        if NodePickerType(self.selector_type) == NodePickerType.ModelPicker:
            self.Tab = QTabWidget()    
            self.container1 = QWidget()                    
            self.layoutH1T1H1 = QHBoxLayout(self.container1)
            self.ModelTree = QTreeView()
            self.ModelTree.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
            self.ModelTree.setFixedHeight(200)
            self.ModelTree.setFixedWidth(130)            
            self.ModelTreeModel = QStandardItemModel()
            self.updateModels(self.scene.parent.current_models)
            self.ModelPicked = QTextEdit()
            self.ModelPicked.setFixedHeight(200)
            self.ModelPicked.setFixedWidth(130)
            self.ModelPicked.setReadOnly(True)
            self.layoutH1T1H1.addWidget(self.ModelTree)
            self.layoutH1T1H1.addWidget(self.ModelPicked)
            self.Tab.insertTab(0, self.container1, "Models")
            self.Tab.currentChanged.connect(self.updateTab)
            self.layoutH1.addWidget(self.Tab)
        elif NodePickerType(self.selector_type) == NodePickerType.ColorPicker:
            self.Tab = QTabWidget()    
            self.container1 = QWidget()   
            self.layoutH1T1H1 = QHBoxLayout(self.container1)
            self.layoutH1T1V1 = QVBoxLayout()
            self.ModelTree = QTreeView()
            self.ModelTree.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
            self.ModelTree.setFixedHeight(200)
            self.ModelTree.setFixedWidth(130)
            self.ModelTreeModel = QStandardItemModel()
            self.updateModels(self.scene.parent.current_models)
            self.ModelPicked = QListView()
            self.ModelPickedModel = QStandardItemModel()
            self.ModelPicked.setModel(self.ModelPickedModel)
            self.ModelPicked.selectionModel().selectionChanged.connect(self.updateGroup)
            self.ModelPicked.setFixedHeight(100)
            self.ModelPicked.setFixedWidth(130)
            self.ModelPicked.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
            self.ModelGroup = QTextEdit()
            self.ModelGroup.setReadOnly(True)
            self.ModelGroup.setFixedHeight(100)
            self.ModelGroup.setFixedWidth(130)
            self.layoutH1T1V1.addWidget(self.ModelPicked)
            self.layoutH1T1V1.addWidget(self.ModelGroup)
            self.layoutH1T1H1.addWidget(self.ModelTree)
            self.layoutH1T1H1.addLayout(self.layoutH1T1V1)
            self.Tab.insertTab(0, self.container1, "Models")
            self.Tab.currentChanged.connect(self.updateTab)
            self.layoutH1.addWidget(self.Tab)
        elif NodePickerType(self.selector_type) == NodePickerType.CenterPicker:
            self.Tab = QTabWidget()    
            self.container1 = QWidget()   
            self.layoutH1T1V1 = QVBoxLayout(self.container1)
            self.ModelTree = QTreeView()
            self.ModelTree.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
            self.ModelTree.setFixedHeight(200)
            self.ModelTreeModel = QStandardItemModel()
            self.updateModels(self.scene.parent.current_models)
            self.ModelPicked = QLineEdit()
            self.ModelPicked.setReadOnly(True)
            self.layoutH1T1V1.addWidget(self.ModelTree)
            self.layoutH1T1V1.addWidget(self.ModelPicked)
            self.Tab.insertTab(0, self.container1, "Models")
            self.Tab.currentChanged.connect(self.updateTab)
            self.layoutH1.addWidget(self.Tab)
        elif NodePickerType(self.selector_type) == NodePickerType.ViewPicker:
            self.Tab = QTabWidget()
            self.container1 = QWidget()            
            self.layoutH1T1H1 = QHBoxLayout(self.container1)
            self.ModelTree = QTreeView()
            self.ModelTree.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
            self.ModelTree.setFixedHeight(200)
            self.ModelTree.setFixedWidth(130)
            self.ModelTreeModel = QStandardItemModel()
            self.container2 = QWidget()            
            self.layoutH1T2H1 = QHBoxLayout(self.container2)
            self.ViewTree = QTreeView()
            self.ViewTree.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
            self.ViewTree.setFixedHeight(200)
            self.ViewTree.setFixedWidth(130)
            self.ViewTreeModel = QStandardItemModel()
            self.updateModels(self.scene.parent.current_models)
            self.ModelPicked = QTextEdit()
            self.ModelPicked.setFixedHeight(200)
            self.ModelPicked.setFixedWidth(130)
            self.ModelPicked.setReadOnly(True)
            self.layoutH1T1H1.addWidget(self.ModelTree)
            self.layoutH1T1H1.addWidget(self.ModelPicked)
            self.ViewPicked = QTextEdit()
            self.ViewPicked.setFixedHeight(200)
            self.ViewPicked.setFixedWidth(130)
            self.ViewPicked.setReadOnly(True)
            self.layoutH1T2H1.addWidget(self.ViewTree)
            self.layoutH1T2H1.addWidget(self.ViewPicked)
            self.Tab.insertTab(0, self.container1, "Models")
            self.Tab.insertTab(1, self.container2, "Views")  
            self.Tab.currentChanged.connect(self.updateTab)
            self.layoutH1.addWidget(self.Tab)    
        elif NodePickerType(self.selector_type) == NodePickerType.FlyPicker:
            self.Tab = QTabWidget()    
            self.container1 = QWidget()      
            self.layoutH1T1 = QHBoxLayout(self.container1)
            self.ViewTree = QTreeView()
            self.ViewTree.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
            self.ViewTree.setFixedHeight(200)
            self.ViewTree.setFixedWidth(130)
            self.ViewTreeModel = QStandardItemModel()
            self.updateModels(self.scene.parent.current_models)
            self.ViewPicked = QListView()
            self.ViewPickedModel = QStandardItemModel()
            self.ViewPicked.setModel(self.ViewPickedModel)
            self.ViewPicked.setFixedHeight(200)
            self.ViewPicked.setFixedWidth(130)
            self.ViewPicked.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
            self.layoutH1T1.addWidget(self.ViewTree)
            self.layoutH1T1.addWidget(self.ViewPicked)
            self.Tab.insertTab(0, self.container1, "Views")
            self.Tab.currentChanged.connect(self.updateTab)     
            self.layoutH1.addWidget(self.Tab)
        elif NodePickerType(self.selector_type) == NodePickerType.DeletePicker:
            self.Tab = QTabWidget()
            self.container1 = QWidget()            
            self.layoutH1T1H1 = QHBoxLayout(self.container1)
            self.ModelTree = QTreeView()
            self.ModelTree.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
            self.ModelTree.setFixedHeight(200)
            self.ModelTree.setFixedWidth(130)
            self.ModelTreeModel = QStandardItemModel()
            self.container2 = QWidget()            
            self.layoutH1T2H1 = QHBoxLayout(self.container2)
            self.Label2DTree = QTreeView()
            self.Label2DTree.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
            self.Label2DTree.setFixedHeight(200)
            self.Label2DTree.setFixedWidth(130)
            self.Label2DTreeModel = QStandardItemModel()
            self.container3 = QWidget()            
            self.layoutH1T3H1 = QHBoxLayout(self.container3)
            self.Label3DTree = QTreeView()
            self.Label3DTree.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
            self.Label3DTree.setFixedHeight(200)
            self.Label3DTree.setFixedWidth(130)
            self.Label3DTreeModel = QStandardItemModel()
            self.container4 = QWidget()            
            self.layoutH1T4H1 = QHBoxLayout(self.container4)
            self.ViewTree = QTreeView()
            self.ViewTree.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
            self.ViewTree.setFixedHeight(200)
            self.ViewTree.setFixedWidth(130)
            self.ViewTreeModel = QStandardItemModel()
            self.updateModels(self.scene.parent.current_models)
            self.ModelPicked = QTextEdit()
            self.ModelPicked.setFixedHeight(200)
            self.ModelPicked.setFixedWidth(130)
            self.ModelPicked.setReadOnly(True)
            self.layoutH1T1H1.addWidget(self.ModelTree)
            self.layoutH1T1H1.addWidget(self.ModelPicked)
            self.Label2DPicked = QTextEdit()
            self.Label2DPicked.setFixedHeight(200)
            self.Label2DPicked.setFixedWidth(130)
            self.Label2DPicked.setReadOnly(True)
            self.layoutH1T2H1.addWidget(self.Label2DTree)
            self.layoutH1T2H1.addWidget(self.Label2DPicked)
            self.Label3DPicked = QTextEdit()
            self.Label3DPicked.setFixedHeight(200)
            self.Label3DPicked.setFixedWidth(130)
            self.Label3DPicked.setReadOnly(True)
            self.layoutH1T3H1.addWidget(self.Label3DTree)
            self.layoutH1T3H1.addWidget(self.Label3DPicked)
            self.ViewPicked = QTextEdit()
            self.ViewPicked.setFixedHeight(200)
            self.ViewPicked.setFixedWidth(130)
            self.ViewPicked.setReadOnly(True)
            self.layoutH1T4H1.addWidget(self.ViewTree)
            self.layoutH1T4H1.addWidget(self.ViewPicked)
            self.Tab.insertTab(0, self.container1, "Models")
            self.Tab.insertTab(1, self.container2, "2D labels")
            self.Tab.insertTab(2, self.container3, "3D labels")
            self.Tab.insertTab(3, self.container4, "Views")
            self.Tab.currentChanged.connect(self.updateTab)
            self.layoutH1.addWidget(self.Tab)

        if NodePickerType(self.selector_type) == NodePickerType.ModelPicker or NodePickerType(self.selector_type) == NodePickerType.ColorPicker:
            self.ModelTree.setSelectionMode(QAbstractItemView.SelectionMode.MultiSelection)
        elif NodePickerType(self.selector_type) == NodePickerType.CenterPicker:
            self.ModelTree.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        elif NodePickerType(self.selector_type) == NodePickerType.ViewPicker:
            self.ModelTree.setSelectionMode(QAbstractItemView.SelectionMode.MultiSelection)
            self.ViewTree.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        elif NodePickerType(self.selector_type) == NodePickerType.FlyPicker:
            self.ViewTree.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        elif NodePickerType(self.selector_type) == NodePickerType.DeletePicker:
            self.ModelTree.setSelectionMode(QAbstractItemView.SelectionMode.MultiSelection)
            self.Label2DTree.setSelectionMode(QAbstractItemView.SelectionMode.MultiSelection)
            self.Label3DTree.setSelectionMode(QAbstractItemView.SelectionMode.MultiSelection)
            self.ViewTree.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)

        self.layoutH2 = QHBoxLayout()
        if NodePickerType(self.selector_type) == NodePickerType.ModelPicker:
            self.Set = QPushButton("Pick Structure")
            self.Set.clicked.connect(self.select)
            self.layoutH2.addWidget(self.Set)
        elif NodePickerType(self.selector_type) == NodePickerType.ColorPicker:
            self.layoutH2V1 = QVBoxLayout()
            self.Add = QPushButton("Add Group")
            self.Add.clicked.connect(self.AddGroup)
            self.Remove = QPushButton("Remove Group")
            self.Remove.clicked.connect(self.removeGroup)
            self.Remove.setEnabled(False)
            self.layoutH2V1.addWidget(self.Add)
            self.layoutH2V1.addWidget(self.Remove)
            self.layoutH2.addLayout(self.layoutH2V1)
        elif NodePickerType(self.selector_type) == NodePickerType.CenterPicker:
            self.Set = QPushButton("Pick Center")
            self.Set.clicked.connect(self.select)
            self.layoutH2.addWidget(self.Set)
        elif NodePickerType(self.selector_type) == NodePickerType.ViewPicker:
            self.layoutH2V1 = QVBoxLayout()
            self.Set = QPushButton("Pick View")
            self.Set.clicked.connect(self.select)
            self.layoutH2.addWidget(self.Set)
        elif NodePickerType(self.selector_type) == NodePickerType.FlyPicker:
            self.layoutH2V1 = QVBoxLayout()
            self.Add = QPushButton("Add Point")
            self.Add.clicked.connect(self.AddGroup)
            self.Remove = QPushButton("Remove Point")
            self.Remove.clicked.connect(self.removeGroup)
            self.Remove.setEnabled(False)
            self.layoutH2V1.addWidget(self.Add)
            self.layoutH2V1.addWidget(self.Remove)
            self.layoutH2.addLayout(self.layoutH2V1)
        elif NodePickerType(self.selector_type) == NodePickerType.DeletePicker:
            self.layoutH2V1 = QVBoxLayout()
            self.Set = QPushButton("Pick Object")
            self.Set.clicked.connect(self.select)
            self.layoutH2.addWidget(self.Set)
        
        self.layoutH2V2 = QVBoxLayout()
        self.Reset = QPushButton("Reset")
        self.Reset.clicked.connect(self.resetModels)
        self.Reset.setEnabled(False)
        self.layoutH2.addWidget(self.Reset)
        if NodePickerType(self.selector_type) != NodePickerType.DeletePicker:
            self.Copy = QPushButton("Copy Pick")
            self.Copy.clicked.connect(self.copyModels)
            self.Paste = QPushButton("Paste Pick")
            self.Paste.clicked.connect(self.pasteModels)
            self.layoutH2V2.addWidget(self.Copy)
            self.layoutH2V2.addWidget(self.Paste)
            self.layoutH2.addLayout(self.layoutH2V2)
        
        self.widget_layout.addLayout(self.layoutH1)
        self.widget_layout.addLayout(self.layoutH2)

        self.updateTab()

    def updateModel(self) -> list[str]:
        selected_temp = []
        if self.Tab.currentIndex() == 0:
            index = self.ModelTree.selectionModel().selectedIndexes()
        elif self.Tab.currentIndex() == 1:
            index = self.Label2DTree.selectionModel().selectedIndexes()
        elif self.Tab.currentIndex() == 2:
            index = self.Label3DTree.selectionModel().selectedIndexes()

        model_list = []
        chain_list = []
        residue_list = []
        atom_list = []
        for i in index:
            item = i.model().itemFromIndex(i)
            mod = None
            if item.parent() is not None:
                if item.parent().parent() is not None:
                    if item.parent().parent().parent() is not None:
                        if item.parent().text() == "Special Residue":
                            m = item.parent().parent().parent().text().split("#")[1]
                            c = item.parent().parent().text().split("-")[0]
                            res_num = item.text().split(" ")[1]
                            mod = f"#{m}.{c}:{res_num}"
                            residue_list.append(mod)
                        else:
                            m = item.parent().parent().parent().text().split("#")[1]
                            c = item.parent().parent().text().split("-")[0]
                            res_num = item.parent().text().split(" ")[1]
                            mod = f"#{m}.{c}:{res_num}@{item.text()}"
                            atom_list.append(mod)
                    else:
                        if item.text() == "Special Residue":
                            for j in range(item.rowCount()):
                                m = item.parent().parent().text().split("#")[1]
                                c = item.parent().text().split("-")[0]
                                res_num = item.child(j).text().split(" ")[1]
                                mod = f"#{m}.{c}:{res_num}"
                                residue_list.append(mod)
                        elif item.parent().text() == "Special Residue":
                            m = item.parent().parent().text().split("#")[1]
                            text = item.text().split(" ")[1]
                            mod = f"#{m}.{text}"
                            residue_list.append(mod)
                        else:
                            m = item.parent().parent().text().split("#")[1]
                            c = item.parent().text().split("-")[0]
                            res_num = item.text().split(" ")[1]
                            mod = f"#{m}.{c}:{res_num}"
                            residue_list.append(mod)
                else:
                    if item.text() == "Special Residue":
                        for j in range(item.rowCount()):
                            m = item.parent().text().split("#")[1]
                            text = item.child(j).text().split(" ")[1]
                            mod = f"#{m}.{text}"
                            residue_list.append(mod)
                    elif item.parent().text() == "Special Residue":
                        text = item.text().split(" ")[1]
                        mod = f"#{text}"
                        residue_list.append(mod)
                    else:
                        m = item.parent().text().split("#")[1]
                        c = item.text().split("-")[0]
                        mod = f"#{m}.{c}"
                        chain_list.append(mod)
            else:
                if item.text() == "All":
                    model_list.append(item.text())
                elif item.text() == "Special Residue":
                    for j in range(item.rowCount()):
                        text:str = item.child(j).text().split(" ")[1]
                        mod = f"#{text}"
                        residue_list.append(mod)
                else:
                    m = item.text().split("#")[1]
                    mod = f"#{m}"
                    model_list.append(mod)
        if "All" not in model_list:
            split_model_list = [re.split("#|\\.|:|@", mod)[1:] for mod in model_list]
            split_model_list.sort()
            if self.Tab.currentIndex() == 2:
                split_chain_list = [re.split("#|\\.|:|@", chain, maxsplit=4)[2:] for chain in chain_list]
                split_chain_list.sort()
            else:
                split_chain_list = [re.split("#|\\.|:|@", chain)[1:] for chain in chain_list]
                split_chain_list.sort()
            split_residue_list = [re.split("#|\\.|:|@", residue)[1:] for residue in residue_list]
            split_residue_list.sort()
            split_atom_list = [re.split("#|\\.|:|@", atom)[1:] for atom in atom_list]
            split_atom_list.sort()
            del model_list, chain_list, residue_list, atom_list

            filtered0_model_list = []
            filtered0_chain_list = []
            filtered0_residue_list = []
            filtered0_atom_list = []
            for mod in split_model_list:
                filtered0_model_list.append(mod[:])
            for chain in split_chain_list:
                exists = False
                for i, s in enumerate(split_model_list):
                    if chain[0] == s[0]:
                        exists = True
                        break
                if not exists:
                    if filtered0_chain_list == []:
                        filtered0_chain_list.append(chain[:])
                    else:
                        for i, s in enumerate(filtered0_chain_list):
                            if chain[0] == s[0] and chain[1] not in s[1]:
                                filtered0_chain_list[i][1] += f",{chain[1]}"
                                exists = True
                                break
                            elif chain[0] not in s[0] and chain[1] == s[1]:
                                filtered0_chain_list[i][0] += f",{chain[0]}"
                                exists = True
                                break
                        if not exists:
                            filtered0_chain_list.append(chain[:])
            for residue in split_residue_list:
                exists = False
                for i, s in enumerate(split_model_list):
                    if residue[0] == s[0]:
                        exists = True
                        break
                if not exists:
                    for i, s in enumerate(split_chain_list):
                        if residue[0] == s[0] and residue[1] == s[1]:
                            exists = True
                            break
                if not exists:
                    if filtered0_residue_list == []:
                        filtered0_residue_list.append(residue[:])
                    else:
                        for i, s in enumerate(filtered0_residue_list):
                            if residue[0] == s[0] and residue[1] == s[1] and residue[2] not in s[2]:
                                filtered0_residue_list[i][2] += f",{residue[2]}"
                                exists = True
                                break
                            elif residue[0] == s[0] and residue[1] not in s[1] and residue[2] == s[2]:
                                filtered0_residue_list[i][1] += f",{residue[1]}"
                                exists = True
                                break
                            elif residue[0] not in s[0] and residue[1] == s[1] and residue[2] == s[2]:
                                filtered0_residue_list[i][0] += f",{residue[0]}"
                                exists = True
                                break
                        if not exists:
                            filtered0_residue_list.append(residue[:])
            for atom in split_atom_list:
                exists = False
                for i, s in enumerate(split_model_list):
                    if atom[0] == s[0]:
                        exists = True
                        break
                if not exists:
                    for i, s in enumerate(split_chain_list):
                        if atom[0] == s[0] and atom[1] == s[1]:
                            exists = True
                            break
                if not exists:
                    for i, s in enumerate(split_residue_list):
                        if atom[0] == s[0] and atom[1] == s[1] and atom[2] == s[2]:
                            exists = True
                            break
                if not exists:
                    if filtered0_atom_list == []:
                        filtered0_atom_list.append(atom[:])
                    else:
                        for i, s in enumerate(filtered0_atom_list):
                            if atom[0] == s[0] and atom[1] == s[1] and atom[2] == s[2] and atom[3] not in s[3]:
                                filtered0_atom_list[i][3] += f",{atom[3]}"
                                exists = True
                                break
                            elif atom[0] == s[0] and atom[1] == s[1] and atom[2] not in s[2] and atom[3] == s[3]:
                                filtered0_atom_list[i][2] += f",{atom[2]}"
                                exists = True
                                break
                            elif atom[0] == s[0] and atom[1] not in s[1] and atom[2] == s[2] and atom[3] == s[3]:
                                filtered0_atom_list[i][1] += f",{atom[1]}"
                                exists = True
                                break
                            elif atom[0] not in s[0] and atom[1] == s[1] and atom[2] == s[2] and atom[3] == s[3]:
                                filtered0_atom_list[i][0] += f",{atom[0]}"
                                exists = True
                                break
                        if not exists:
                            filtered0_atom_list.append(atom[:])

            filtered1_model_list = []
            filtered1_chain_list = []
            filtered1_residue_list = []
            filtered1_atom_list = []

            for mod in filtered0_model_list:
                if filtered1_model_list == []:
                    filtered1_model_list.append(mod)
                else:
                    filtered1_model_list[0][0] += f",{mod[0]}"
            for chain in filtered0_chain_list:
                if filtered1_chain_list == []:
                    filtered1_chain_list.append(chain[:])
                else:
                    exists = False
                    for i, s in enumerate(filtered1_chain_list):
                        if chain[0] == s[0] and chain[1] not in s[1]:
                            filtered1_chain_list[i][1] += f",{chain[1]}"
                            exists = True
                            break
                        elif chain[0] not in s[0] and chain[1] == s[1]:
                            filtered1_chain_list[i][0] += f",{chain[0]}"
                            exists = True
                            break
                    if not exists:
                        filtered1_chain_list.append(chain[:])
            for residue in filtered0_residue_list:
                if filtered1_residue_list == []:
                    filtered1_residue_list.append(residue[:])
                else:
                    exists = False
                    for i, s in enumerate(filtered1_residue_list):
                        if residue[0] == s[0] and residue[1] == s[1] and residue[2] not in s[2]:
                            filtered1_residue_list[i][2] += f",{residue[2]}"
                            exists = True
                            break
                        elif residue[0] == s[0] and residue[1] not in s[1] and residue[2] == s[2]:
                            filtered1_residue_list[i][1] += f",{residue[1]}"
                            exists = True
                            break
                        elif residue[0] not in s[0] and residue[1] == s[1] and residue[2] == s[2]:
                            filtered1_residue_list[i][0] += f",{residue[0]}"
                            exists = True
                            break
                    if not exists:
                        filtered1_residue_list.append(residue[:])
            for atom in filtered0_atom_list:
                if filtered1_atom_list == []:
                    filtered1_atom_list.append(atom[:])
                else:
                    exists = False
                    for i, s in enumerate(filtered1_atom_list):
                        if atom[0] == s[0] and atom[1] == s[1] and atom[2] == s[2] and atom[3] not in s[3]:
                            filtered1_atom_list[i][3] += f",{atom[3]}"
                            exists = True
                            break
                        elif atom[0] == s[0] and atom[1] == s[1] and atom[2] not in s[2] and atom[3] == s[3]:
                            filtered1_atom_list[i][2] += f",{atom[2]}"
                            exists = True
                            break
                        elif atom[0] == s[0] and atom[1] not in s[1] and atom[2] == s[2] and atom[3] == s[3]:
                            filtered1_atom_list[i][1] += f",{atom[1]}"
                            exists = True
                            break
                        elif atom[0] not in s[0] and atom[1] == s[1] and atom[2] == s[2] and atom[3] == s[3]:
                            filtered1_atom_list[i][0] += f",{atom[0]}"
                            exists = True
                            break
                    if not exists:
                        filtered1_atom_list.append(atom[:])
                        
            filtered2_residue_list = []
            filtered2_atom_list = []
            for residue in filtered1_residue_list:
                if filtered2_residue_list == []:
                    filtered2_residue_list.append(residue[:])
                else:
                    exists = False
                    for i, s in enumerate(filtered2_residue_list):
                        if residue[0] == s[0] and residue[1] == s[1] and residue[2] not in s[2]:
                            filtered2_residue_list[i][2] += f",{residue[2]}"
                            exists = True
                            break
                        elif residue[0] == s[0] and residue[1] not in s[1] and residue[2] == s[2]:
                            filtered2_residue_list[i][1] += f",{residue[1]}"
                            exists = True
                            break
                        elif residue[0] not in s[0] and residue[1] == s[1] and residue[2] == s[2]:
                            filtered2_residue_list[i][0] += f",{residue[0]}"
                            exists = True
                            break
                    if not exists:
                        filtered2_residue_list.append(residue[:])
            for atom in filtered1_atom_list:
                if filtered2_atom_list == []:
                    filtered2_atom_list.append(atom[:])
                else:
                    exists = False
                    for i, s in enumerate(filtered2_atom_list):
                        if atom[0] == s[0] and atom[1] == s[1] and atom[2] == s[2] and atom[3] not in s[3]:
                            filtered2_atom_list[i][3] += f",{atom[3]}"
                            exists = True
                            break
                        elif atom[0] == s[0] and atom[1] == s[1] and atom[2] not in s[2] and atom[3] == s[3]:
                            filtered2_atom_list[i][2] += f",{atom[2]}"
                            exists = True
                            break
                        elif atom[0] == s[0] and atom[1] not in s[1] and atom[2] == s[2] and atom[3] == s[3]:
                            filtered2_atom_list[i][1] += f",{atom[1]}"
                            exists = True
                            break
                        elif atom[0] not in s[0] and atom[1] == s[1] and atom[2] == s[2] and atom[3] == s[3]:
                            filtered2_atom_list[i][0] += f",{atom[0]}"
                            exists = True
                            break
                    if not exists:
                        filtered2_atom_list.append(atom[:])

            filtered3_atom_list = []
            for atom in filtered2_atom_list:
                if filtered3_atom_list == []:
                    filtered3_atom_list.append(atom[:])
                else:
                    exists = False
                    for i, s in enumerate(filtered3_atom_list):
                        if atom[0] == s[0] and atom[1] == s[1] and atom[2] == s[2] and atom[3] not in s[3]:
                            filtered3_atom_list[i][3] += f",{atom[3]}"
                            exists = True
                            break
                        elif atom[0] == s[0] and atom[1] == s[1] and atom[2] not in s[2] and atom[3] == s[3]:
                            filtered3_atom_list[i][2] += f",{atom[2]}"
                            exists = True
                            break
                        elif atom[0] == s[0] and atom[1] not in s[1] and atom[2] == s[2] and atom[3] == s[3]:
                            filtered3_atom_list[i][1] += f",{atom[1]}"
                            exists = True
                            break
                        elif atom[0] not in s[0] and atom[1] == s[1] and atom[2] == s[2] and atom[3] == s[3]:
                            filtered3_atom_list[i][0] += f",{atom[0]}"
                            exists = True
                            break
                    if not exists:
                        filtered3_atom_list.append(atom[:])

            for mol in filtered1_model_list:
                if all([s.isnumeric() for s in mol[0].split(",")]):
                    map_model = [int(i) for i in mol[0] .split(",")]
                    m_num = True
                else:
                    map_model = list(map(ord, mol[0].split(",")))
                    m_num = False
                map_model.sort()
                model_ranges = self.get_consecutive_ranges(map_model)
                if m_num:
                    model_ranges = [f"{r[0]}-{r[1]}" if r[0] != r[1] else f"{r[0]}" for r in model_ranges]
                else:
                    model_ranges = [f"{chr(r[0])}-{chr(r[1])}" if r[0] != r[1] else f"{chr(r[0])}" for r in model_ranges]
                selected_temp.append(f"#{','.join(model_ranges)}")
            for mol in filtered1_chain_list:
                if all([s.isnumeric() for s in mol[0].split(",")]):
                    map_model = [int(i) for i in mol[0].split(",")]
                    m_num = True
                else:
                    map_model = list(map(ord, mol[0].split(",")))
                    m_num = False
                map_model.sort()
                if all([s.isnumeric() for s in mol[1].split(",")]):
                    map_chain = [int(i) for i in mol[1].split(",")]
                    c_num = True
                else:
                    map_chain = list(map(ord, mol[1].split(",")))
                    c_num = False
                map_chain.sort()
                model_ranges = self.get_consecutive_ranges(map_model)
                if m_num:
                    model_ranges = [f"{r[0]}-{r[1]}" if r[0] != r[1] else f"{r[0]}" for r in model_ranges]
                else:
                    model_ranges = [f"{chr(r[0])}-{chr(r[1])}" if r[0] != r[1] else f"{chr(r[0])}" for r in model_ranges]
                chain_ranges = self.get_consecutive_ranges(map_chain)
                if c_num:
                    chain_ranges = [f"{r[0]}-{r[1]}" if r[0] != r[1] else f"{r[0]}" for r in chain_ranges]
                else:
                    chain_ranges = [f"{chr(r[0])}-{chr(r[1])}" if r[0] != r[1] else f"{chr(r[0])}" for r in chain_ranges]
                selected_temp.append(f"#{','.join(model_ranges)}.{','.join(chain_ranges)}")
            for mol in filtered2_residue_list:
                if all([s.isnumeric() for s in mol[0].split(",")]):
                    map_model = [int(i) for i in mol[0].split(",")]
                    m_num = True
                else:
                    map_model = list(map(ord, mol[0].split(",")))
                    m_num = False
                map_model.sort()
                if all([s.isnumeric() for s in mol[1].split(",")]):
                    map_chain = [int(i) for i in mol[1].split(",")]
                    c_num = True
                else:
                    map_chain = list(map(ord, mol[1].split(",")))
                    c_num = False
                map_chain.sort()
                if all([s.isnumeric() for s in mol[2].split(",")]):
                    map_redisue = [int(i) for i in mol[2].split(",")]
                    r_num = True
                else:
                    map_redisue = list(map(ord, mol[2].split(",")))
                    r_num = False
                map_redisue.sort()
                model_ranges = self.get_consecutive_ranges(map_model)
                if m_num:
                    model_ranges = [f"{r[0]}-{r[1]}" if r[0] != r[1] else f"{r[0]}" for r in model_ranges]
                else:
                    model_ranges = [f"{chr(r[0])}-{chr(r[1])}" if r[0] != r[1] else f"{chr(r[0])}" for r in model_ranges]
                chain_ranges = self.get_consecutive_ranges(map_chain)
                if c_num:
                    chain_ranges = [f"{r[0]}-{r[1]}" if r[0] != r[1] else f"{r[0]}" for r in chain_ranges]
                else:
                    chain_ranges = [f"{chr(r[0])}-{chr(r[1])}" if r[0] != r[1] else f"{chr(r[0])}" for r in chain_ranges]
                residue_ranges = self.get_consecutive_ranges(map_redisue)
                if r_num:
                    residue_ranges = [f"{r[0]}-{r[1]}" if r[0] != r[1] else f"{r[0]}" for r in residue_ranges]
                else:
                    residue_ranges = [f"{chr(r[0])}-{chr(r[1])}" if r[0] != r[1] else f"{chr(r[0])}" for r in residue_ranges]
                selected_temp.append(f"#{','.join(model_ranges)}.{','.join(chain_ranges)}:{','.join(residue_ranges)}")
            for mol in filtered3_atom_list:
                if all([s.isnumeric() for s in mol[0].split(",")]):
                    map_model = [int(i) for i in mol[0].split(",")]
                    m_num = True
                else:
                    map_model = list(map(ord, mol[0].split(",")))
                    m_num = False
                map_model.sort()
                if all([s.isnumeric() for s in mol[1].split(",")]):
                    map_chain = [int(i) for i in mol[1].split(",")]
                    c_num = True
                else:
                    map_chain = list(map(ord, mol[1].split(",")))
                    c_num = False
                map_chain.sort()
                if all([s.isnumeric() for s in mol[2].split(",")]):
                    map_redisue = [int(i) for i in mol[2].split(",")]
                    r_num = True
                else:
                    map_redisue = list(map(ord, mol[2].split(",")))
                    r_num = False
                map_redisue.sort()
                model_ranges = self.get_consecutive_ranges(map_model)
                if m_num:
                    model_ranges = [f"{r[0]}-{r[1]}" if r[0] != r[1] else f"{r[0]}" for r in model_ranges]
                else:
                    model_ranges = [f"{chr(r[0])}-{chr(r[1])}" if r[0] != r[1] else f"{chr(r[0])}" for r in model_ranges]
                chain_ranges = self.get_consecutive_ranges(map_chain)
                if c_num:
                    chain_ranges = [f"{r[0]}-{r[1]}" if r[0] != r[1] else f"{r[0]}" for r in chain_ranges]
                else:
                    chain_ranges = [f"{chr(r[0])}-{chr(r[1])}" if r[0] != r[1] else f"{chr(r[0])}" for r in chain_ranges]
                residue_ranges = self.get_consecutive_ranges(map_redisue)
                if r_num:
                    residue_ranges = [f"{r[0]}-{r[1]}" if r[0] != r[1] else f"{r[0]}" for r in residue_ranges]
                else:
                    residue_ranges = [f"{chr(r[0])}-{chr(r[1])}" if r[0] != r[1] else f"{chr(r[0])}" for r in residue_ranges]
                selected_temp.append(f"#{','.join(model_ranges)}.{','.join(chain_ranges)}:{','.join(residue_ranges)}@{mol[3]}")
        else:
            selected_temp = ["All"]
        return selected_temp
    
    def updateViews(self) -> list[str]:
        selected_temp = []
        index = self.ViewTree.selectionModel().selectedIndexes()
        for i in index:
            item = i.model().itemFromIndex(i)
            selected_temp.append(item.text())
        if "All" in selected_temp:
            selected_temp = ["All"]
        return selected_temp

    def updateModelswithValue(self, selected_temp:list[str]|None, index:int=None, restore:bool=False):
        if NodePickerType(self.selector_type) == NodePickerType.ModelPicker:
            self.selected_model = selected_temp
            if not restore:
                self.ModelPicked.clear()    
                self.ModelPicked.setText("\n".join(self.selected_model))
            self.node.node_output.edge.end_socket.node.summary.picker_model = self.selected_model
            self.node.summary.ModelText.setText("\n".join(self.selected_model))
            if self.selected_model != []:
                self.Copy.setEnabled(True)
                self.Reset.setEnabled(True)
            else:
                self.Copy.setEnabled(False)
                self.Reset.setEnabled(False)
            if not restore:
                self.node.node_output.edge.end_socket.node.summary.updateModel()
        elif NodePickerType(self.selector_type) == NodePickerType.ColorPicker:
            self.selected_model = selected_temp
            self.ModelGroup.clear()    
            if self.selected_model != []:
                if not restore:
                    item = QStandardItem(f"Group {self.ModelPickedModel.rowCount() + 1}")
                    self.ModelPickedModel.appendRow(item)
                    self.selected_color_groups.append(self.selected_model)
                    self.node.node_output.edge.end_socket.node.summary.picker_color_groups = self.selected_color_groups
                    self.node.node_output.edge.end_socket.node.content.addGroup()
                else:
                    self.node.node_output.edge.end_socket.node.summary.picker_color_groups = self.selected_color_groups
                self.node.summary.ColorText.setText(f"{len(self.selected_color_groups)} groups")
                self.Remove.setEnabled(True) 
                self.Copy.setEnabled(True)
                self.Reset.setEnabled(True)
            else:
                self.Copy.setEnabled(False)
                self.Reset.setEnabled(False)
            if not restore:
                self.node.node_output.edge.end_socket.node.summary.updateColor()
        elif NodePickerType(self.selector_type) == NodePickerType.CenterPicker:
            self.selected_model = selected_temp
            if not restore:
                self.ModelPicked.clear()    
                self.ModelPicked.setText("\n".join(self.selected_model))
            self.node.node_output.edge.end_socket.node.summary.picker_center = self.selected_model
            self.node.summary.CenterText.setText("\n".join(self.selected_model))
            if self.selected_model != []:
                self.Copy.setEnabled(True)
                self.Reset.setEnabled(True)
            else:
                self.Copy.setEnabled(False)
                self.Reset.setEnabled(False)
            if not restore:
                self.node.node_output.edge.end_socket.node.summary.updateCenter()
        elif NodePickerType(self.selector_type) == NodePickerType.DeletePicker:
            if not restore:
                if index == 0:
                    self.selected_model = selected_temp
                    self.ModelPicked.clear()  
                    self.ModelPicked.setText("\n".join(self.selected_model))
                    self.node.node_output.edge.end_socket.node.summary.picker_delete = self.selected_model
                    self.node.summary.DeleteText.setText("\n".join(self.selected_model))
                    if self.selected_model != []:
                        self.Reset.setEnabled(True)
                    else:
                        self.Reset.setEnabled(False)
                elif index == 1:
                    self.selected_2dlabel = selected_temp
                    self.Label2DPicked.clear()  
                    self.Label2DPicked.setText("\n".join(self.selected_2dlabel))
                    self.node.node_output.edge.end_socket.node.summary.picker_delete = self.selected_2dlabel
                    self.node.summary.DeleteText.setText("\n".join(self.selected_2dlabel))
                    if self.selected_2dlabel != []:
                        self.Reset.setEnabled(True)
                    else:
                        self.Reset.setEnabled(False)
                elif index == 2:
                    self.selected_3dlabel = selected_temp
                    self.Label3DPicked.clear()   
                    self.Label3DPicked.setText("\n".join(self.selected_3dlabel)) 
                    self.node.node_output.edge.end_socket.node.summary.picker_delete = self.selected_3dlabel
                    self.node.summary.DeleteText.setText("\n".join(self.selected_3dlabel))
                    if self.selected_3dlabel != []:
                        self.Reset.setEnabled(True)
                    else:
                        self.Reset.setEnabled(False)
            if not restore:
                self.node.node_output.edge.end_socket.node.summary.updateDelete()
        elif NodePickerType(self.selector_type) == NodePickerType.ViewPicker:
            self.selected_model = selected_temp
            if not restore:
                self.ModelPicked.clear()    
                self.ModelPicked.setText("\n".join(self.selected_model))
            self.node.node_output.edge.end_socket.node.summary.picker_view = self.selected_model
            self.node.summary.ViewText.setText("\n".join(self.selected_model))
            if self.selected_model != []:
                self.Copy.setEnabled(True)
                self.Reset.setEnabled(True)
            else:
                self.Copy.setEnabled(False)
                self.Reset.setEnabled(False)
            if not restore:
                self.node.node_output.edge.end_socket.node.summary.updateView()

    def updateViewswithValue(self, selected_temp:list[str]|None, index:int=None, restore:bool=False):
        if selected_temp is None:
            selected_temp = []
        self.selected_view = selected_temp
        if NodePickerType(self.selector_type) == NodePickerType.ViewPicker:
            if not restore:
                self.ViewPicked.clear()
                self.ViewPicked.setText("\n".join(self.selected_view))
            self.node.node_output.edge.end_socket.node.summary.picker_view = self.selected_view
            self.node.summary.ViewText.setText("\n".join(self.selected_view))
            if self.selected_view != []:
                self.Copy.setEnabled(True)
                self.Reset.setEnabled(True)
            else:
                self.Copy.setEnabled(False)
                self.Reset.setEnabled(False)
            if not restore:
                self.node.node_output.edge.end_socket.node.summary.updateView()
        elif NodePickerType(self.selector_type) == NodePickerType.FlyPicker:
            if self.selected_view != []:
                if not restore:
                    item = QStandardItem(f"{self.selected_view[0]}")
                    self.ViewPickedModel.appendRow(item)
                    self.selected_fly_groups.append(self.selected_view[0])
                    self.node.node_output.edge.end_socket.node.summary.picker_fly_groups = self.selected_fly_groups
                    if len(self.selected_fly_groups) < 2:
                        self.node.summary.FlyText.setText("0 transitions")
                    else:
                        self.node.summary.FlyText.setText(f"{len(self.selected_fly_groups)} transitions")
                    self.node.node_output.edge.end_socket.node.content.addFlySequence()
                self.Remove.setEnabled(True)
                self.Copy.setEnabled(True)
                self.Reset.setEnabled(True)
            else:
                self.Copy.setEnabled(False)
                self.Reset.setEnabled(False)
                if not restore:
                    self.node.node_output.edge.end_socket.node.summary.updateFly()
        elif NodePickerType(self.selector_type) == NodePickerType.DeletePicker:
            if not restore:
                if index == 3:
                    self.ModelPicked.clear()  
                    self.ViewPicked.setText("\n".join(self.selected_view))
            self.node.node_output.edge.end_socket.node.summary.picker_delete = self.selected_view
            self.node.summary.DeleteText.setText("\n".join(self.selected_view))
            if self.selected_view != []:
                self.Reset.setEnabled(True)
            else:
                self.Reset.setEnabled(False)
            if not restore:
                self.node.node_output.edge.end_socket.node.summary.updateDelete()

    def select(self):
        if NodePickerType(self.selector_type) == NodePickerType.FlyPicker:
            if self.Tab.currentIndex() == 0:
                self.updateViewswithValue(self.updateViews(), self.Tab.currentIndex())
        elif NodePickerType(self.selector_type) == NodePickerType.ViewPicker:
            if self.Tab.currentIndex() == 0:
                self.updateModelswithValue(self.updateModel(), self.Tab.currentIndex())
            elif self.Tab.currentIndex() == 1:
                self.updateViewswithValue(self.updateViews(), self.Tab.currentIndex())
        else:
            if self.Tab.currentIndex() == 0:
                self.updateModelswithValue(self.updateModel(), self.Tab.currentIndex())
            elif self.Tab.currentIndex() == 1:
                self.updateModelswithValue(self.updateModel(), self.Tab.currentIndex())
            elif self.Tab.currentIndex() == 2:
                self.updateModelswithValue(self.updateModel(), self.Tab.currentIndex())
            elif self.Tab.currentIndex() == 3:
                self.updateViewswithValue(self.updateViews(), self.Tab.currentIndex())

    def get_consecutive_ranges(self, numbers:list[int]):
        start,stop = None,None
        for num in numbers:
            if stop is None:
                start, stop = num, num
            elif stop == num-1:
                stop += 1
            else:
                yield [start, stop]
                start, stop = num, num
        yield [start, stop]
    
    def updateGroup(self):
        if NodePickerType(self.selector_type) == NodePickerType.ColorPicker:
            for index in self.ModelPicked.selectionModel().selectedIndexes():
                self.ModelGroup.setText("\n".join(self.selected_color_groups[index.row()]))

    def AddGroup(self):
        if NodePickerType(self.selector_type) == NodePickerType.ColorPicker:
            self.select()
            self.ModelTree.selectionModel().clearSelection()
            self.ModelPicked.selectionModel().clearSelection()
        elif NodePickerType(self.selector_type) == NodePickerType.FlyPicker:
            self.select()
            self.ViewTree.selectionModel().clearSelection()
            self.ViewPicked.selectionModel().clearSelection()

    def removeGroup(self):
        row_indexes = []
        if NodePickerType(self.selector_type) == NodePickerType.ColorPicker:
            indexes = self.ModelPicked.selectionModel().selectedIndexes()
            for index in indexes:
                row_indexes.append(index.row())
                self.ModelPickedModel.removeRow(index.row())
            for index in sorted(row_indexes, reverse=True):
                del self.selected_color_groups[index]
            self.node.node_output.edge.end_socket.node.summary.picker_color_groups = self.selected_color_groups
            self.node.summary.ColorText.setText(f"{len(self.selected_color_groups)} groups")
            self.node.node_output.edge.end_socket.node.content.removeGroup(sorted(row_indexes, reverse=True))
            self.node.node_output.edge.end_socket.node.summary.updateColor()
            self.ModelPickedModel.clear()
            for i, mod in enumerate(self.selected_color_groups):
                item = QStandardItem(f"Group {i + 1}")
                self.ModelPickedModel.appendRow(item)
            if self.selected_color_groups == []:
                self.Copy.setEnabled(False)
                self.Remove.setEnabled(False)
            self.ModelTree.selectionModel().clearSelection()
            self.ModelPicked.selectionModel().clearSelection()
            self.ModelGroup.setText("")
        elif NodePickerType(self.selector_type) == NodePickerType.FlyPicker:
            indexes = self.ViewPicked.selectionModel().selectedIndexes()
            for index in indexes:
                row_indexes.append(index.row())
                self.ViewPickedModel.removeRow(index.row())
            group_count = len(self.selected_fly_groups)
            for index in sorted(row_indexes, reverse=True):
                del self.selected_fly_groups[index]
            self.node.node_output.edge.end_socket.node.summary.picker_fly_groups = self.selected_fly_groups
            self.node.summary.FlyText.setText(f"{len(self.selected_fly_groups)} transitions")
            self.node.node_output.edge.end_socket.node.content.removeFlySequence(sorted(row_indexes, reverse=True), group_count)
            self.node.node_output.edge.end_socket.node.summary.updateFly()
            self.ViewPickedModel.clear()
            for i, mod in enumerate(self.selected_fly_groups):
                item = QStandardItem(f"{self.selected_fly_groups[i]}")
                self.ViewPickedModel.appendRow(item)
            if self.selected_fly_groups == []:
                self.Copy.setEnabled(False)
                self.Remove.setEnabled(False)
            self.ViewTree.selectionModel().clearSelection()
            self.ViewPicked.selectionModel().clearSelection()

    def resetModels(self):
        if NodePickerType(self.selector_type) == NodePickerType.ModelPicker:
            self.selected_model = []
            self.node.node_output.edge.end_socket.node.summary.picker_model = self.selected_model
            self.node.summary.ModelText.setText("None")
            self.node.node_output.edge.end_socket.node.summary.updateModel()
            self.ModelTree.selectionModel().clearSelection()
            self.ModelPicked.setText("")
        elif NodePickerType(self.selector_type) == NodePickerType.ColorPicker:
            self.selected_color_groups = []
            self.node.node_output.edge.end_socket.node.summary.picker_color_groups = self.selected_color_groups
            self.node.summary.ColorText.setText("0 Groups")
            self.node.node_output.edge.end_socket.node.content.resetGroups()
            self.node.node_output.edge.end_socket.node.summary.updateColor()
            self.ModelTree.selectionModel().clearSelection()
            self.ModelPicked.reset()
            self.ModelPickedModel.clear()
            self.ModelGroup.setText("")
            self.Remove.setEnabled(False)
        elif NodePickerType(self.selector_type) == NodePickerType.CenterPicker:
            self.selected_model = []
            self.node.node_output.edge.end_socket.node.summary.picker_center = self.selected_model
            self.node.summary.CenterText.setText("None")
            self.node.node_output.edge.end_socket.node.summary.updateCenter()
            self.ModelTree.selectionModel().clearSelection()
            self.ModelPicked.setText("")
        elif NodePickerType(self.selector_type) == NodePickerType.ViewPicker:
            if self.Tab.currentIndex() == 0:
                self.selected_model = []
                self.node.node_output.edge.end_socket.node.summary.picker_view = self.selected_model
                self.ModelTree.selectionModel().clearSelection()
                self.ModelPicked.setText("")
            elif self.Tab.currentIndex() == 1:
                self.selected_view = []
                self.node.node_output.edge.end_socket.node.summary.picker_view = self.selected_view
                self.ViewTree.selectionModel().clearSelection()
                self.ViewPicked.setText("")
            self.node.summary.ViewText.setText("None")
            self.node.node_output.edge.end_socket.node.summary.updateView()
        elif NodePickerType(self.selector_type) == NodePickerType.FlyPicker:
            self.selected_fly_groups = []
            self.node.node_output.edge.end_socket.node.summary.picker_fly_groups = self.selected_fly_groups
            self.node.summary.FlyText.setText(f"0 transitions")
            self.node.node_output.edge.end_socket.node.content.resetFlySequence()
            self.node.node_output.edge.end_socket.node.summary.updateFly()
            self.ViewTree.selectionModel().clearSelection()
            self.ViewPicked.reset()
            self.ViewPickedModel.clear()
            self.Remove.setEnabled(False)
        elif NodePickerType(self.selector_type) == NodePickerType.DeletePicker:
            if self.Tab.currentIndex() == 0:
                self.selected_model = []
                self.node.node_output.edge.end_socket.node.summary.picker_delete = self.selected_model
                self.ModelTree.selectionModel().clearSelection()
                self.ModelPicked.setText("")
            elif self.Tab.currentIndex() == 1:
                self.selected_2dlabel = []
                self.node.node_output.edge.end_socket.node.summary.picker_delete = self.selected_2dlabel
                self.Label2DTree.selectionModel().clearSelection()
                self.Label2DPicked.setText("")
            elif self.Tab.currentIndex() == 2:
                self.selected_3dlabel = []
                self.node.node_output.edge.end_socket.node.summary.picker_delete = self.selected_3dlabel
                self.Label3DTree.selectionModel().clearSelection()
                self.Label3DPicked.setText("")
            elif self.Tab.currentIndex() == 3:
                self.selected_view = []
                self.node.node_output.edge.end_socket.node.summary.picker_delete = self.selected_view
                self.ViewTree.selectionModel().clearSelection()
                self.ViewPicked.setText("")
            self.node.summary.DeleteText.setText("None")
            self.node.node_output.edge.end_socket.node.summary.updateDelete()
        if hasattr(self, "Copy"):
            self.Copy.setEnabled(False)
        self.Reset.setEnabled(False)

    def copyModels(self):
        if NodePickerType(self.selector_type) == NodePickerType.ModelPicker:
            self.scene.parent.copy_selected_model_objects = self.selected_model
        elif NodePickerType(self.selector_type) == NodePickerType.ColorPicker:
            self.scene.parent.copy_selected_color_objects = [group for group in self.selected_color_groups]
        elif NodePickerType(self.selector_type) == NodePickerType.CenterPicker:
            self.scene.parent.copy_selected_center_objects = self.selected_model
        elif NodePickerType(self.selector_type) == NodePickerType.ViewPicker:
            if self.Tab.currentIndex() == 0:
                self.scene.parent.copy_selected_model_objects = self.selected_model
            elif self.Tab.currentIndex() == 1:
                self.scene.parent.copy_selected_view_objects = self.selected_view
        elif NodePickerType(self.selector_type) == NodePickerType.FlyPicker:
                self.scene.parent.copy_selected_fly_objects = [group for group in self.selected_fly_groups]
                self.scene.parent.copy_selected_fly_objects_transition_frames = self.node.node_output.edge.end_socket.node.content.transition_frames
        for picker in self.scene.parent.pickers:
            picker.refreshTabPaste()

    def pasteModels(self):
        enable = False
        if NodePickerType(self.selector_type) == NodePickerType.ModelPicker:
            if self.scene.parent.copy_selected_model_objects is not None:
                self.selected_model = self.scene.parent.copy_selected_model_objects
                self.ModelPicked.setText("\n".join(self.selected_model))
                enable = True
                self.node.node_output.edge.end_socket.node.summary.picker_model = self.selected_model
                self.node.summary.ModelText.setText("\n".join(self.selected_model))
                self.node.node_output.edge.end_socket.node.summary.updateModel()
        elif NodePickerType(self.selector_type) == NodePickerType.ColorPicker:
            if self.scene.parent.copy_selected_color_objects is not None:
                self.ModelPickedModel.clear()
                self.selected_color_groups = []
                self.node.node_output.edge.end_socket.node.summary.picker_color_groups = self.selected_color_groups
                self.node.node_output.edge.end_socket.node.content.resetGroups()
                self.selected_color_groups = self.scene.parent.copy_selected_color_objects
                for i, mod in enumerate(self.selected_color_groups):
                    item = QStandardItem(f"Group {i + 1}")
                    self.ModelPickedModel.appendRow(item)
                if len(self.selected_color_groups) > 0:
                    self.Remove.setEnabled(True)
                enable = True
                self.node.node_output.edge.end_socket.node.summary.picker_color_groups = self.selected_color_groups
                self.node.summary.ColorText.setText(f"{len(self.selected_color_groups)} Groups")
                self.node.node_output.edge.end_socket.node.content.addGroups()
                self.node.node_output.edge.end_socket.node.summary.updateColor()
        elif NodePickerType(self.selector_type) == NodePickerType.CenterPicker:
            if self.scene.parent.copy_selected_center_objects is not None:
                self.selected_model = self.scene.parent.copy_selected_center_objects
                self.ModelPicked.setText("\n".join(self.selected_model))
                enable = True
                self.node.node_output.edge.end_socket.node.summary.picker_center = self.selected_model
                self.node.summary.CenterText.setText("\n".join(self.selected_model))
                self.node.node_output.edge.end_socket.node.summary.updateCenter()
        elif NodePickerType(self.selector_type) == NodePickerType.ViewPicker:
            if self.Tab.currentIndex() == 0:
                if self.scene.parent.copy_selected_model_objects is not None:
                    self.selected_model = self.scene.parent.copy_selected_model_objects
                    self.ModelPicked.setText("\n".join(self.selected_model))
                    enable = True
                    self.node.node_output.edge.end_socket.node.summary.picker_view = self.selected_model
                    self.node.summary.ViewText.setText("\n".join(self.selected_model))
                    self.node.node_output.edge.end_socket.node.summary.updateView()
            elif self.Tab.currentIndex() == 1:
                if self.scene.parent.copy_selected_view_objects is not None:
                    self.selected_view = self.scene.parent.copy_selected_view_objects
                    self.ViewPicked.setText("\n".join(self.selected_view))
                    enable = True
                    self.node.node_output.edge.end_socket.node.summary.picker_view = self.selected_view
                    self.node.summary.ViewText.setText("\n".join(self.selected_view))
                    self.node.node_output.edge.end_socket.node.summary.updateView()
        elif NodePickerType(self.selector_type) == NodePickerType.FlyPicker:
            if self.scene.parent.copy_selected_fly_objects is not None:
                self.ViewPickedModel.clear()
                self.selected_fly_groups = []
                self.node.node_output.edge.end_socket.node.summary.picker_fly_groups = self.selected_fly_groups
                self.node.node_output.edge.end_socket.node.content.resetFlySequence()
                self.selected_fly_groups = self.scene.parent.copy_selected_fly_objects
                for i, mod in enumerate(self.selected_fly_groups):
                    item = QStandardItem(f"{self.selected_fly_groups[i]}")
                    self.ViewPickedModel.appendRow(item)
                if len(self.selected_fly_groups) > 0:
                    self.Remove.setEnabled(True)
                enable = True
                self.node.node_output.edge.end_socket.node.summary.picker_fly_groups = self.selected_fly_groups
                self.node.summary.ViewText.setText(f"{len(self.selected_fly_groups)} Groups")
                self.node.node_output.edge.end_socket.node.content.addFlySequences()
                self.node.node_output.edge.end_socket.node.summary.updateFly()
        if enable:
            self.Copy.setEnabled(True)     
            self.Reset.setEnabled(True)
        
    def refreshTabPaste(self):
        if NodePickerType(self.selector_type) == NodePickerType.ModelPicker:
            if self.Tab.currentIndex() == 0:# Model, Center, Color
                if self.scene.parent.copy_selected_model_objects is not None:
                    self.Paste.setEnabled(True)
                else:
                    self.Paste.setEnabled(False)
            elif self.Tab.currentIndex() == 1:# Label2D
                if self.scene.parent.copy_selected_label2D_objects is not None:
                    self.Paste.setEnabled(True)
                else:
                    self.Paste.setEnabled(False)
            elif self.Tab.currentIndex() == 2:# Label3D
                if self.scene.parent.copy_selected_label3D_objects is not None:
                    self.Paste.setEnabled(True)
                else:
                    self.Paste.setEnabled(False)
            elif self.Tab.currentIndex() == 3:# View
                if self.scene.parent.copy_selected_view_objects is not None:
                    self.Paste.setEnabled(True)
                else:
                    self.Paste.setEnabled(False)
        elif NodePickerType(self.selector_type) == NodePickerType.ColorPicker:
            if self.scene.parent.copy_selected_color_objects is not None:
                self.Paste.setEnabled(True)
            else:
                self.Paste.setEnabled(False)
        elif NodePickerType(self.selector_type) == NodePickerType.CenterPicker:
            if self.scene.parent.copy_selected_center_objects is not None:
                self.Paste.setEnabled(True)
            else:
                self.Paste.setEnabled(False)
        elif NodePickerType(self.selector_type) == NodePickerType.ViewPicker:
            if self.Tab.currentIndex() == 0:# Model
                if self.scene.parent.copy_selected_model_objects is not None:
                    self.Paste.setEnabled(True)
                else:
                    self.Paste.setEnabled(False)
            elif self.Tab.currentIndex() == 1:# View
                if self.scene.parent.copy_selected_view_objects is not None:
                    self.Paste.setEnabled(True)
                else:
                    self.Paste.setEnabled(False)
        elif NodePickerType(self.selector_type) == NodePickerType.FlyPicker:
            if self.scene.parent.copy_selected_fly_objects is not None:
                self.Paste.setEnabled(True)
            else:
                self.Paste.setEnabled(False)
        
    def updateTab(self, index:int=None):
        if index is not None:
            if NodePickerType(self.selector_type) == NodePickerType.ModelPicker:
                if index == 0:
                    if hasattr(self.node, "node_output"):
                        self.node.node_output.edge.end_socket.node.summary.picker_model = self.selected_model
                        self.node.node_output.edge.end_socket.node.summary.updateModel()
                        text = "\n".join(self.selected_model)
                        if text == "":
                            text = "None"
                        self.node.summary.ModelText.setText(text)
                    if self.ModelPicked.toPlainText() != "":
                        self.Copy.setEnabled(True)
                        self.Reset.setEnabled(True)
                    else:
                        self.Copy.setEnabled(False)
                        self.Reset.setEnabled(False)
                elif index == 1:# Label2D
                    if hasattr(self.node, "node_output"):
                        self.node.node_output.edge.end_socket.node.summary.picker_model = self.selected_2dlabel
                        self.node.node_output.edge.end_socket.node.summary.updateModel()
                        text = "\n".join(self.selected_2dlabel)
                        if text == "":
                            text = "None"
                        self.node.summary.ModelText.setText(text)
                    if self.Label2DPicked.toPlainText() != "":
                        self.Copy.setEnabled(True)
                        self.Reset.setEnabled(True)
                    else:
                        self.Copy.setEnabled(False)
                        self.Reset.setEnabled(False)
                elif index == 2:# Label3D
                    if hasattr(self.node, "node_output"):
                        self.node.node_output.edge.end_socket.node.summary.picker_model = self.selected_3dlabel
                        self.node.node_output.edge.end_socket.node.summary.updateModel()
                        text = "\n".join(self.selected_3dlabel)
                        if text == "":
                            text = "None"
                        self.node.summary.ModelText.setText(text)
                    if self.Label3DPicked.toPlainText() != "":
                        self.Copy.setEnabled(True)
                        self.Reset.setEnabled(True)
                    else:
                        self.Copy.setEnabled(False)
                        self.Reset.setEnabled(False)
                elif index == 3:# View
                    if hasattr(self.node, "node_output"):
                        self.node.node_output.edge.end_socket.node.summary.picker_model = self.selected_view
                        self.node.node_output.edge.end_socket.node.summary.updateModel()
                        text = "\n".join(self.selected_view)
                        if text == "":
                            text = "None"
                        self.node.summary.ModelText.setText(text)
                    if self.ViewPicked.toPlainText() != "":
                        self.Copy.setEnabled(True)
                        self.Reset.setEnabled(True)
                    else:
                        self.Copy.setEnabled(False)
                        self.Reset.setEnabled(False)
                self.refreshTabPaste()
            elif NodePickerType(self.selector_type) == NodePickerType.ColorPicker:
                if self.ModelPicked.model().rowCount() > 0:
                    self.Copy.setEnabled(True)
                    self.Reset.setEnabled(True)
                else:
                    self.Copy.setEnabled(False)
                    self.Reset.setEnabled(False)
                self.refreshTabPaste()
            elif NodePickerType(self.selector_type) == NodePickerType.CenterPicker:
                if self.ModelPicked.text() != "":
                    self.Copy.setEnabled(True)
                    self.Reset.setEnabled(True)
                else:
                    self.Copy.setEnabled(False)
                    self.Reset.setEnabled(False)
                self.refreshTabPaste()
            elif NodePickerType(self.selector_type) == NodePickerType.ViewPicker:
                if index == 0:# Model
                    if hasattr(self.node, "node_output"):
                        self.node.node_output.edge.end_socket.node.summary.picker_view = self.selected_model
                        self.node.node_output.edge.end_socket.node.summary.updateView()
                        text = "\n".join(self.selected_model)
                        if text == "":
                            text = "None"
                        self.node.summary.ViewText.setText(text)
                    if self.ModelPicked.toPlainText() != "":
                        self.Copy.setEnabled(True)
                        self.Reset.setEnabled(True)
                    else:
                        self.Copy.setEnabled(False)
                        self.Reset.setEnabled(False)
                elif index == 1:# View
                    if hasattr(self.node, "node_output"):
                        self.node.node_output.edge.end_socket.node.summary.picker_view = self.selected_view
                        self.node.node_output.edge.end_socket.node.summary.updateView()
                        text = "\n".join(self.selected_view)
                        if text == "":
                            text = "None"
                        self.node.summary.ViewText.setText(text)
                    if self.ViewPicked.toPlainText() != "":
                        self.Copy.setEnabled(True)
                        self.Reset.setEnabled(True)
                    else:
                        self.Copy.setEnabled(False)
                        self.Reset.setEnabled(False)
                self.refreshTabPaste()
            elif NodePickerType(self.selector_type) == NodePickerType.FlyPicker:
                if self.ViewPicked.model().rowCount() > 0:
                    self.Copy.setEnabled(True)
                    self.Reset.setEnabled(True)
                else:
                    self.Copy.setEnabled(False)
                    self.Reset.setEnabled(False)
                self.refreshTabPaste()
            elif NodePickerType(self.selector_type) == NodePickerType.DeletePicker:
                if index == 0:# Model, Center, Color
                    if hasattr(self.node, "node_output"):
                        self.node.node_output.edge.end_socket.node.summary.picker_delete = self.selected_model
                        self.node.node_output.edge.end_socket.node.summary.updateDelete()
                        text = "\n".join(self.selected_model)
                        if text == "":
                            text = "None"
                        self.node.summary.DeleteText.setText(text)
                    if self.ModelPicked.toPlainText() != "":
                        self.Reset.setEnabled(True)
                    else:
                        self.Reset.setEnabled(False)
                elif index == 1:# Label2D
                    if hasattr(self.node, "node_output"):
                        self.node.node_output.edge.end_socket.node.summary.picker_delete = self.selected_2dlabel
                        self.node.node_output.edge.end_socket.node.summary.updateDelete()
                        text = "\n".join(self.selected_2dlabel)
                        if text == "":
                            text = "None"
                        self.node.summary.DeleteText.setText(text)
                    if self.Label2DPicked.toPlainText() != "":
                        self.Reset.setEnabled(True)
                    else:
                        self.Reset.setEnabled(False)
                elif index == 2:# Label3D
                    if hasattr(self.node, "node_output"):
                        self.node.node_output.edge.end_socket.node.summary.picker_delete = self.selected_3dlabel
                        self.node.node_output.edge.end_socket.node.summary.updateDelete()
                        text = "\n".join(self.selected_3dlabel)
                        if text == "":
                            text = "None"
                        self.node.summary.DeleteText.setText(text)
                    if self.Label3DPicked.toPlainText() != "":
                        self.Reset.setEnabled(True)
                    else:
                        self.Reset.setEnabled(False)
                elif index == 3:# View
                    if hasattr(self.node, "node_output"):
                        self.node.node_output.edge.end_socket.node.summary.picker_delete = self.selected_view
                        self.node.node_output.edge.end_socket.node.summary.updateDelete()
                        text = "\n".join(self.selected_view)
                        if text == "":
                            text = "None"
                        self.node.summary.DeleteText.setText(text)
                    if self.ViewPicked.toPlainText() != "":
                        self.Reset.setEnabled(True)
                    else:
                        self.Reset.setEnabled(False)

            if hasattr(self.node, "node_output"):
                self.node.node_output.edge.end_socket.node.content.updateTab(index)

    def checkSpecialResidue(self, residue:str) -> bool:
        if residue in self.scene.parent.settings_menu.normal_residues:
            return False
        return True
        
    def generateModels(self, objs:list) -> list[QStandardItemModel]:
        model = QStandardItemModel()
        model.clear()
        
        first_special_residue_item:bool = True
        for obj in objs:
            if type(obj) == structure.AtomicStructure:
                if obj.id is not None:
                    if len(obj.id) == 1:
                        model_item = QStandardItem(f"Model #{int(obj.id[0])}")
                        model.appendRow(model_item)
            elif type(obj) == models.Model:
                first_special_residue_item_in_model:bool = True
                model_item = QStandardItem(f"Model #{obj.id[0]}")
                model.appendRow(model_item)
                i = 1
                for struct in obj.child_models():
                    if type(struct) == structure.AtomicStructure:
                        for chain in struct.chains:
                            first_special_residue_item_in_chain:bool = True
                            chain_item = QStandardItem(f"{i}-{chain.chain_id}")
                            model_item.appendRow(chain_item)
                            if self.scene.parent.settings_menu.model_residues:
                                for residue in chain.residues:
                                    residue_text = str(residue).split(" ")
                                    if self.scene.parent.settings_menu.model_special_residues:
                                        if self.checkSpecialResidue(residue_text[-2]):
                                            if first_special_residue_item:
                                                special_residue_item = QStandardItem("Special Residue")
                                                model.insertRow(0, special_residue_item)
                                                first_special_residue_item = False
                                            if first_special_residue_item_in_model:
                                                special_residue_item_in_model = QStandardItem("Special Residue")
                                                model_item.insertRow(0, special_residue_item_in_model)
                                                first_special_residue_item_in_model = False
                                            if first_special_residue_item_in_chain:
                                                special_residue_item_in_chain = QStandardItem("Special Residue")
                                                chain_item.insertRow(0, special_residue_item_in_chain)
                                                first_special_residue_item_in_chain = False
                                            special_residue_item.appendRow(QStandardItem(f"{residue_text[-2]} {obj.id[0]}.{i}:{residue_text[-1]}"))
                                            special_residue_item_in_model.appendRow(QStandardItem(f"{residue_text[-2]} {i}:{residue_text[-1]}"))
                                            special_residue_item_in_chain.appendRow(QStandardItem(f"{residue_text[-2]} {residue_text[-1]}"))
                                    residue_text = f"{residue_text[-2]} {residue_text[-1]}" 
                                    residue_item = QStandardItem(residue_text)
                                    chain_item.appendRow(residue_item)
                                    if self.scene.parent.settings_menu.model_atoms:
                                        for atom in residue.atoms:
                                            atom_text = str(atom).split(" ")
                                            atom_item = QStandardItem(atom_text[-1])
                                            residue_item.appendRow(atom_item)
                            i += 1
            elif type(obj) == volume.Volume:
                volume_item = QStandardItem(f"Volume #{obj.id[0]}")
                model.appendRow(volume_item)
                for struct in obj.child_models():
                    if type(struct) == volume.VolumeSurface:
                        surface_item = QStandardItem(f"{struct.id[1]}-{struct.name}")
                        volume_item.appendRow(surface_item)
            elif type(obj) == markers.MarkerSet:
                marker_item = QStandardItem(f"{obj.id[0]} - {obj.name}")
                model.appendRow(marker_item)
        return [model]
    
    def generateAllModels(self, objs:list) -> list[QStandardItemModel]:
        model = QStandardItemModel()
        model.clear()
        label2D = QStandardItemModel()
        label2D.clear()
        label3D = QStandardItemModel()
        label3D.clear()

        self.label2D_list = []
        self.label3D_model_list = []
        self.label3D_list = []

        for obj in objs:
            if type(obj) == structure.AtomicStructure:
                if obj.id is not None:
                    if len(obj.id) == 1:
                        model_item = QStandardItem(f"Model #{int(obj.id[0])}")
                        model.appendRow(model_item)
            elif type(obj) == models.Model:
                first_special_residue_item_in_model:bool = True
                model_item = QStandardItem(f"Model #{obj.id[0]}")
                model.appendRow(model_item)
                i = 1
                for struct in obj.child_models():
                    if type(struct) == structure.AtomicStructure:
                        for chain in struct.chains:
                            first_special_residue_item_in_chain:bool = True
                            chain_item = QStandardItem(f"{i}-{chain.chain_id}")
                            model_item.appendRow(chain_item)
                            if self.scene.parent.settings_menu.model_residues:
                                for residue in chain.residues:
                                    residue_text = str(residue).split(" ")
                                    if self.scene.parent.settings_menu.model_special_residues:
                                        if self.checkSpecialResidue(residue_text[-2]):
                                            if first_special_residue_item:
                                                special_residue_item = QStandardItem("Special Residue")
                                                model.insertRow(0, special_residue_item)
                                                first_special_residue_item = False
                                            if first_special_residue_item_in_model:
                                                special_residue_item_in_model = QStandardItem("Special Residue")
                                                model_item.insertRow(0, special_residue_item_in_model)
                                                first_special_residue_item_in_model = False
                                            if first_special_residue_item_in_chain:
                                                special_residue_item_in_chain = QStandardItem("Special Residue")
                                                chain_item.insertRow(0, special_residue_item_in_chain)
                                                first_special_residue_item_in_chain = False
                                            special_residue_item.appendRow(QStandardItem(f"{residue_text[-2]} {obj.id[0]}.{i}:{residue_text[-1]}"))
                                            special_residue_item_in_model.appendRow(QStandardItem(f"{residue_text[-2]} {i}:{residue_text[-1]}"))
                                            special_residue_item_in_chain.appendRow(QStandardItem(f"{residue_text[-2]} {residue_text[-1]}"))
                                    residue_text = f"{residue_text[-2]} {residue_text[-1]}" 
                                    residue_item = QStandardItem(residue_text)
                                    chain_item.appendRow(residue_item)
                                    if self.scene.parent.settings_menu.model_atoms:
                                        for atom in residue.atoms:
                                            atom_text = str(atom).split(" ")
                                            atom_item = QStandardItem(atom_text[-1])
                                            residue_item.appendRow(atom_item)
                            i += 1
            elif type(obj) == volume.Volume:
                volume_item = QStandardItem(f"Volume #{obj.id[0]}")
                model.appendRow(volume_item)
                for struct in obj.child_models():
                    if type(struct) == volume.VolumeSurface:
                        surface_item = QStandardItem(f"{struct.id[1]}-{struct.name}")
                        volume_item.appendRow(surface_item)
            elif type(obj) == markers.MarkerSet:
                marker_item = QStandardItem(f"{obj.id[0]} - {obj.name}")
                self.scene.parent.marker_list.append(f"{obj.id[0]} - {obj.name}")
                model.appendRow(marker_item)
            elif type(obj) == label2d.LabelModel:
                self.label2D_list.append([int(obj.id[0]), QStandardItem(f"{int(obj.id[1])}-{obj.name}")])
            elif type(obj) == label3d.ObjectLabels:
                self.label3D_list.append(obj.id)
                if obj.id[0] not in self.label3D_model_list:
                    self.label3D_model_list.append(obj.id[0])
        self.label2D_list = sorted(self.label2D_list, key=lambda x:x[0])
        current_label_model = 0
        label2d_item = None
        for label in self.label2D_list:
            if current_label_model != label[0]:
                current_label_model = label[0]
                label2d_item = QStandardItem(f"Model {current_label_model}")
                label2D.appendRow(label2d_item)
            label2d_item.appendRow(label[1])
        self.label3D_model_list.sort()
        self.label3D_list.sort()
        for mod in self.label3D_model_list:
            label3d_item = QStandardItem(f"Model {mod}")
            label3D.appendRow(label3d_item)
            for label in self.label3D_list:
                if label[0] == mod:
                    l = ".".join([str(i) for i in label])
                    label_item = QStandardItem(f"{l}")
                    label3d_item.appendRow(label_item)
        return [model, label2D, label3D]
             
    def generateViews(self, views:list) -> list[QStandardItemModel]:
        view_model = QStandardItemModel()
        view_model.clear()
        for view in views:
            view_item = QStandardItem(str(view))
            view_model.appendRow(view_item)
        return [view_model]
    
    def updateModels(self, models:list):
        if NodePickerType(self.selector_type) == NodePickerType.ModelPicker or NodePickerType(self.selector_type) == NodePickerType.ColorPicker or NodePickerType(self.selector_type) == NodePickerType.CenterPicker:
            if models is not None:
                models_list = self.generateModels(models[0])
                self.ModelTreeModel:QStandardItemModel = models_list[0]
                self.ModelTreeModel.setHorizontalHeaderLabels(["Pick Models"])
                self.ModelTreeModel.horizontalHeaderItem(0).setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.ModelTreeModel.insertRow(0, QStandardItem("All"))
                self.ModelTree.setModel(self.ModelTreeModel)
                self.ModelTree.header().setFirstSectionMovable(False)
        elif NodePickerType(self.selector_type) == NodePickerType.DeletePicker:
            models_list:QStandardItemModel = []
            if models is not None:
                models_list += self.generateAllModels(models[0])
                models_list += self.generateViews(models[1])
                self.ModelTreeModel:QStandardItemModel = models_list[0]
                self.ModelTreeModel.setHorizontalHeaderLabels(["Pick Models"])
                self.ModelTreeModel.horizontalHeaderItem(0).setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.Label2DTreeModel:QStandardItemModel = models_list[1]
                self.Label2DTreeModel.setHorizontalHeaderLabels(["Pick 2D Labels"])
                self.Label2DTreeModel.horizontalHeaderItem(0).setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.Label3DTreeModel:QStandardItemModel = models_list[2]
                self.Label3DTreeModel.setHorizontalHeaderLabels(["Pick 3D Labels"])
                self.Label3DTreeModel.horizontalHeaderItem(0).setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.ViewTreeModel:QStandardItemModel = models_list[3]
                self.ViewTreeModel.setHorizontalHeaderLabels(["Pick View"])
                self.ViewTreeModel.horizontalHeaderItem(0).setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.ModelTreeModel.insertRow(0, QStandardItem("All"))
                self.Label2DTreeModel.insertRow(0, QStandardItem("All"))
                self.Label3DTreeModel.insertRow(0, QStandardItem("All"))
                if self.all_views:
                    self.ViewTreeModel.insertRow(0, QStandardItem("All"))
                self.ModelTree.setModel(self.ModelTreeModel)
                self.ModelTree.header().setFirstSectionMovable(False)
                self.Label2DTree.setModel(self.Label2DTreeModel)
                self.Label2DTree.header().setFirstSectionMovable(False)
                self.Label3DTree.setModel(self.Label3DTreeModel)
                self.Label3DTree.header().setFirstSectionMovable(False)
                self.ViewTree.setModel(self.ViewTreeModel)
                self.ViewTree.header().setFirstSectionMovable(False)
        elif NodePickerType(self.selector_type) == NodePickerType.ViewPicker:
            models_list = []
            if models is not None:
                models_list += self.generateModels(models[0])
                models_list += self.generateViews(models[1])
                self.ModelTreeModel:QStandardItemModel = models_list[0]
                self.ModelTreeModel.setHorizontalHeaderLabels(["Pick Models"])
                self.ModelTreeModel.horizontalHeaderItem(0).setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.ViewTreeModel:QStandardItemModel = models_list[1]
                self.ViewTreeModel.setHorizontalHeaderLabels(["Pick View"])
                self.ViewTreeModel.horizontalHeaderItem(0).setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.ModelTreeModel.insertRow(0, QStandardItem("All"))
                if self.all_views:
                    self.ViewTreeModel.insertRow(0, QStandardItem("All"))
                self.ModelTree.setModel(self.ModelTreeModel)
                self.ModelTree.header().setFirstSectionMovable(False)
                self.ViewTree.setModel(self.ViewTreeModel)
                self.ViewTree.header().setFirstSectionMovable(False)
        elif NodePickerType(self.selector_type) == NodePickerType.FlyPicker:
            models_list = []
            if models is not None:
                models_list += self.generateViews(models[1])
                self.ViewTreeModel:QStandardItemModel = models_list[0]
                self.ViewTreeModel.setHorizontalHeaderLabels(["Pick View"])
                self.ViewTreeModel.horizontalHeaderItem(0).setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                if self.all_views:
                    self.ViewTreeModel.insertRow(0, QStandardItem("All"))
                self.ViewTree.setModel(self.ViewTreeModel)
                self.ViewTree.header().setFirstSectionMovable(False)

class QSwitchCircle(QWidget):
    def __init__(self, parent:QSwitchControl, color:str):
        super().__init__(parent=parent)
        self.color = color
        
    def paintEvent(self, event):
        painter = QPainter()
        painter.begin(self)
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(QColor(self.color))
        painter.drawEllipse(0, 0, 12, 12)
        painter.end()

class QSwitchControl(QCheckBox):
    def __init__(self, editor:NodeEditor, checked:bool=False, parent=None):
        if parent is None:
            super().__init__()
        else:
            super().__init__(parent=parent)

        self.setProperty("type", "switch")

        self.editor = editor
        self.bg_color = ""
        self.bg_active = ""
        self.circle_color = ""
        self.setFixedSize(28, 14)
        self.animation_curve = QEasingCurve.Type=QEasingCurve.Type.OutCirc
        self.animation_duration = 250
        self.__circle = QSwitchCircle(self, self.circle_color)
        self.checked = checked
        if self.checked:
            self.__circle.move(1, 1)
            self.setChecked(True)
        elif not self.checked:
            self.__circle.move(self.width() - 14, 1)
            self.setChecked(False)
        self.animation = QPropertyAnimation(self.__circle, b"pos")
        self.animation.setEasingCurve(self.animation_curve)
        self.animation.setDuration(self.animation_duration)
        self.stateChanged.connect(self.updateState)
        
        if hasattr(self.editor, "theme_toggle"):
            if self.editor.theme_toggle.isChecked():
                self.changeStyle(Stylesheet.LIGHT)
            else:
                self.changeStyle(Stylesheet.DARK)

    def changeStyle(self, style:Stylesheet):
        if self.objectName() == "theme_toggle":
            if self.isChecked():
                self.__circle.color = self.editor.styles._switch_handle[0]
            else:
                self.__circle.color = self.editor.styles._switch_handle[1]
        else:
            if self.isEnabled():
                self.__circle.color = self.editor.styles._switch_handle[style.value]
            else:
                self.__circle.color = self.editor.styles._switch_handle_disabled[style.value]

    def start_animation(self):
        self.animation.stop()
        self.animation.setStartValue(self.__circle.pos())
        if self.isChecked():
            self.animation.setEndValue(QPoint(2, self.__circle.y()))
        else:
            self.animation.setEndValue(QPoint(self.width() - 14, self.__circle.y()))
        self.animation.start()

    def paintEvent(self, event):
        super().paintEvent(event)

    def hitButton(self, pos):
        return self.contentsRect().contains(pos)

    def mousePressEvent(self, event):
        self.setChecked(not self.isChecked())

    def updateState(self, event):
        self.start_animation()