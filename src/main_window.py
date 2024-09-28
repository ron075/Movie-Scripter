from __future__ import annotations

from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *
from chimerax.core import objects, tasks
from chimerax.std_commands.view import NamedViews
import os
import time
from .node_base import *
from .edges import *
from .graphics_scene import *
from .presets import *
from .stylesheets import *
from .sub_window import *

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .main import MovieMaker

class NodeEditor(QWidget):
    def __init__(self, session, parent_tool:MovieMaker=None, parent=None):
        super().__init__(parent)
        self.parent_tool = parent_tool
        self.session = session  
        self.tool_status = ToolStatus.RUNNING

        self.initUI()

    def initUI(self):
        self.settings_menu = SettingsMenu(self.session, self)

        self.simple_mode = True

        self.movie_script = QTextDocument()

        self.view_model = QStandardItemModel()
        self.model_model = QStandardItemModel()
        self.label2D_model = QStandardItemModel()
        self.label3D_model = QStandardItemModel()
        
        #add typing here
        self.current_models = None

        self.viewer_texts:list[str] = []

        self.copy_selected_model_objects = None
        self.copy_selected_color_objects = None
        self.copy_selected_center_objects = None
        self.copy_selected_view_objects = None
        self.copy_selected_fly_objects = None
        self.copy_selected_fly_objects_transition_frames = None
        self.copy_selected_label2D_objects = None
        self.copy_selected_label3D_objects = None

        self.pickers:list[QTreeViewSelector] = []
        self.switches:list[QSwitchControl] = []

        # crate graphics scenec
        self.scene = Scene(self.session, self)

        self.stylesheets = { "DARK": "", "LIGHT": "" }
        _base_path = os.path.dirname(os.path.abspath(__file__))
        self.styles = Stylesheets()
        self.stylesheets = self.styles.styles(_base_path)
        
        self.nodeStart = Node(self.session, self.scene, NodeType.Start, removable=False, has_input=False, parent=self)
        self.nodeEnd = Node(self.session, self.scene, NodeType.End, removable=False, has_output=False, parent=self)

        self.nodeStart.setPos(-300,-300)
        self.nodeEnd.setPos(-200,-200)

        self.editor_layout = QVBoxLayout(self)

        # create graphics view
        self.layoutS1 = QSplitter(self)
        self.view = QDMGraphicsView(self.scene.grScene, self)
        self.script = QTextDocument()
        self.script_window = QTextEdit()
        self.script_window = QTextEdit()
        self.script_window.setDocument(self.script)
        self.script_window.setReadOnly(True)
        self.script_window.hide()
        self.layoutS1.addWidget(self.view)
        self.layoutS1.addWidget(self.script_window)
        
        self.layoutG1 = QGridLayout()
        self.presets_box = QComboBox()
        self.presets_box.setFixedHeight(30)
        self.load_button = QPushButton("Load Preset")
        self.load_button.clicked.connect(self.loadPreset)
        self.center_button = QPushButton("Center")
        self.center_button.clicked.connect(self.focusView)
        self.reset_button = QPushButton("Reset")
        self.reset_button.clicked.connect(self.reset)
        self.save_button = QPushButton("Save Script")
        self.save_button.clicked.connect(self.saveScript)
        self.run_button = QPushButton("Run Script")
        self.run_button.clicked.connect(self.runScript)
        self.viewer_button = QPushButton("Viewer: None")
        self.viewer_button.setProperty("State", "None")
        self.viewer_button.setEnabled(False)
        self.viewer_button.clicked.connect(self.scriptWindow)
        self.mode_button = QPushButton("Mode: Simple")
        self.mode_button.setProperty("State", "Simple")
        self.mode_button.clicked.connect(self.ToggleMode)
        self.light_mode = QLabel()
        self.light_mode.setObjectName("light_mode")
        self.light_mode.setFixedHeight(20)
        self.light_mode.setFixedWidth(20)
        self.theme_toggle = QSwitchControl(self, checked=True)
        self.switches.append(self.theme_toggle)
        self.theme_toggle.stateChanged.connect(self.changeStyle)
        self.theme_toggle.setObjectName("theme_toggle")
        self.dark_mode = QLabel()
        self.dark_mode.setObjectName("dark_mode")
        self.dark_mode.setFixedHeight(20)
        self.dark_mode.setFixedWidth(20)
        self.settings_button = QPushButton("")
        self.settings_button.setProperty("State", "Closed")
        self.settings_button.setObjectName("settings_button")
        self.settings_button.clicked.connect(self.settings_menu.openSettings)
        self.layoutG1.addWidget(self.presets_box, 0, 0, 1, 1)
        self.layoutG1.addWidget(self.load_button, 1, 0, 1, 1)
        self.layoutG1.addWidget(self.center_button, 0, 1, 1, 1)
        self.layoutG1.addWidget(self.reset_button, 1, 1, 1, 1)
        self.layoutG1.addWidget(self.save_button, 0, 2, 1, 1)
        self.layoutG1.addWidget(self.run_button, 1, 2, 1, 1)
        self.layoutG1.addWidget(self.viewer_button, 0, 3, 1, 1)
        self.layoutG1.addWidget(self.mode_button, 1, 3, 1, 1)
        self.layoutG1.addWidget(self.light_mode, 0, 4, 1, 1, alignment=Qt.AlignmentFlag.AlignCenter)
        self.layoutG1.addWidget(self.theme_toggle, 0, 5, 1, 1, alignment=Qt.AlignmentFlag.AlignCenter)
        self.layoutG1.addWidget(self.dark_mode, 0, 6, 1, 1, alignment=Qt.AlignmentFlag.AlignCenter)
        self.layoutG1.addWidget(self.settings_button, 1, 4, 1, 3, alignment=Qt.AlignmentFlag.AlignCenter)
        self.layoutG1.setColumnStretch(0, 2)  
        self.layoutG1.setColumnStretch(1, 2)  
        self.layoutG1.setColumnStretch(2, 2)  
        self.layoutG1.setColumnStretch(3, 2)  
        
        self.editor_layout.addWidget(self.layoutS1)
        self.editor_layout.addLayout(self.layoutG1)

        self.setLayout(self.editor_layout) 

        self.presets = Presets(self.session, self)
        self.reload_presets()
        self.presets_box.addItems(self.loaded_presets.keys())

        self.settings_menu.raise_()

        self.changeStyle()

        self.script_thread = ScriptJob(self.session, self)
        self.script_thread.start()
        self.model_thread = ModelJob(self.session, self)
        self.model_thread.start()
    
    def reload_presets(self):
        self.presets.prepare_presets()
        if self.mode_button.property("State") == "Simple":
            self.loaded_presets = self.presets.simple_prestes
        elif self.mode_button.property("State") == "Expert":
            self.loaded_presets = self.presets.expert_prestes

    def ToggleMode(self, simple_mode:bool|None=None):
        if self.mode_button.property("State") == "Simple":
            self.mode_button.setProperty("State", "Expert")
            self.mode_button.setText("Mode: Expert")
            self.loaded_presets = self.presets.expert_prestes
        elif self.mode_button.property("State") == "Expert":
            self.mode_button.setProperty("State", "Simple")
            self.mode_button.setText("Mode: Simple")
            self.loaded_presets = self.presets.simple_prestes
        if simple_mode is None:
            self.simple_mode = not self.simple_mode
        else:
            self.simple_mode = simple_mode  
        self.viewer_button.setProperty("State", "Close")
        self.viewer_button.setEnabled(not self.simple_mode)
        self.presets_box.clear()
        self.presets_box.addItems(self.loaded_presets.keys())
        self.scriptWindow()
        self.reset()

    def changeStyle(self):
        if self.theme_toggle.isChecked():
            style = Stylesheet.LIGHT
        else:
            style = Stylesheet.DARK
        self.parent_tool.pp.setStyleSheet(self.stylesheets[style.name])
        self.settings_menu.setStyleSheet(self.stylesheets[style.name])
        self.scene.changeStyle(style)
        for switch in self.switches:
            switch.changeStyle(style)

    def scriptWindow(self):
        if self.viewer_button.property("State") == "None":
            self.viewer_button.setProperty("State", "Script")
            self.viewer_button.setText("Viewer: Script")
            self.script_window.show()
            self.updateViewerText()
        elif self.viewer_button.property("State") == "Script":
            self.viewer_button.setProperty("State", "Comments")
            self.viewer_button.setText("Viewer: Comments")
            self.updateViewerText()
        elif self.viewer_button.property("State") == "Comments":
            self.viewer_button.setProperty("State", "Summary")
            self.viewer_button.setText("Viewer: Summary")
            self.updateViewerText()
        elif self.viewer_button.property("State") == "Summary":
            self.viewer_button.setProperty("State", "None")
            self.viewer_button.setText("Viewer: None")
            self.script_window.hide()
        elif self.viewer_button.property("State") == "Close":
            self.viewer_button.setProperty("State", "None")
            self.viewer_button.setText("Viewer: None")
            self.script_window.hide()

    def generateSummary(self):
        nlines = 0
        for line in self.movie_script.toPlainText().splitlines():
            if line.strip():
                nlines += 1

        total_node_frequency = {}
        for node in self.scene.nodes:
            if node.nodeType.value not in total_node_frequency.keys():
                total_node_frequency[node.nodeType.value] = 1
            else:
                total_node_frequency[node.nodeType.value] = total_node_frequency[node.nodeType.value] + 1
        total_node_frequency = dict(sorted(total_node_frequency.items()))

        frames = 0
        connected_nodes = 0
        current_node = self.nodeStart
        node_frequency = {}
        while current_node is not None:
            connected_nodes += 1
            if current_node.nodeType.value not in node_frequency.keys():
                node_frequency[current_node.nodeType.value] = 1
            else:
                node_frequency[current_node.nodeType.value] = node_frequency[current_node.nodeType.value] + 1
            frames = current_node.summary.total_frames
            if current_node.node_output is not None:
                if current_node.node_output.hasEdge():
                    current_node = current_node.node_output.edge.end_socket.node
                else:
                    current_node = None
            else:
                current_node = None
        node_frequency = dict(sorted(node_frequency.items()))

        length = self.convertTime(int(frames) / int(self.nodeEnd.content.Framerate.Text.text()))
                
        summary = f""    
        summary += f"<u><b>Total lines in script:</u></b> {nlines}<br>"
        summary += f"<br>"
        summary += f"<u><b>Nodes count:</u></b> {len(self.scene.nodes)}<br>"
        summary += f"<u><b>Edges count:</u></b> {len(self.scene.edges)}<br>"
        summary += f"<br>"
        summary += f"<u><b>Connected nodes count:</u></b> {connected_nodes}<br>"
        summary += f"<u><b>Connected edges count:</u></b> {connected_nodes - 1}<br>"
        summary += f"<br>"
        summary += f"<u><b>Total frame count:</u></b> {frames}<br>"
        summary += f"<u><b>Length:</u></b> {length}<br>"
        summary += f"<br>"
        
        summary += f"<u><b>Total Node Types:</u></b><br>"
        for node_type in total_node_frequency:
            summary += f"   • <u>{NodeType(node_type).name}:</u> {total_node_frequency[node_type]} count"
            if total_node_frequency[node_type] < 2:
                summary += "<br>"
            else:
                summary += "s<br>"
        summary += f"<br>"

        summary += f"<u><b>Connected Node Types:</u></b><br>"
        for node_type in node_frequency:
            summary += f"   • <u>{NodeType(node_type).name}:</u> {node_frequency[node_type]} count"
            if node_frequency[node_type] < 2:
                summary += "<br>"
            else:
                summary += "s<br>"
        summary += f"<br>"
        
        current_node = self.nodeStart
        summary += f"<u><b>Node Order (node type):</u></b><br>"
        summary += f"{current_node.nodeType.name}"
        while current_node is not None:
            if current_node.node_output is not None:
                if current_node.node_output.hasEdge():
                    current_node = current_node.node_output.edge.end_socket.node
                    summary += f" → {current_node.nodeType.name}"
                else:
                    current_node = None
            else:
                current_node = None
        summary += f"<br>"
        summary += f"<br>"

        current_node = self.nodeStart
        summary += f"<u><b>Node Order (node ID):</u></b><br>"
        summary += f"{current_node.nodeID}"
        while current_node is not None:
            if current_node.node_output is not None:
                if current_node.node_output.hasEdge():
                    current_node = current_node.node_output.edge.end_socket.node
                    summary += f" → {current_node.nodeID}"
                else:
                    current_node = None
            else:
                current_node = None
        summary += f"<br>"
        summary += f"<br>"
        return summary
    
    def generateViewer(self) -> list[str]:
        do_record = self.nodeStart.content.Record.isChecked()
        current_node = self.nodeStart
        start_command = ""
        command = ""
        end_command = ""
        start_comment = ""
        comment = ""
        end_comment = ""
        while current_node is not None:
            command_string = current_node.content.updateCommand()
            if command_string != []:
                start_command += command_string[0]
                command += command_string[1]
                end_command += command_string[2]
            if not self.simple_mode:
                comment_string = current_node.content.updateComment()
                summary = self.generateSummary()
                if comment_string != []:
                    start_comment += comment_string[0]
                    comment += comment_string[1]
                    end_comment += comment_string[2]
            else:
                comment_string = ""
                summary = ""
            if current_node.node_output is None:
                current_node = None
            else:
                if current_node.node_output.edge is None:
                    current_node = None
                else:
                    current_node = current_node.node_output.edge.end_socket.node
        if do_record:
            return [start_command + command + end_command, start_comment + comment + end_comment, summary]
        else:
            return [command, comment, summary]
        
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
                    return(f"{format(round(value, 2), '.2f')} Days")
                
    @pyqtSlot(list)
    def updateViewerText(self, text_list:list[str]=[]):
        if text_list != []:
            self.viewer_texts = text_list
        if self.viewer_texts != []:
            self.movie_script.setHtml(self.viewer_texts[0])
            if self.viewer_button.property("State") == "None":
                text = None
            elif self.viewer_button.property("State") == "Script":
                text = self.viewer_texts[0]
            elif self.viewer_button.property("State") == "Comments":
                text = self.viewer_texts[1]
            elif self.viewer_button.property("State") == "Summary":
                text = self.viewer_texts[2]
            if text is not None:
                self.script_window.setHtml(text)
            
    def loadPreset(self):
        self.reset(preset=True)
        if self.presets_box.currentIndex() > -1:
            self.loaded_presets[self.presets_box.currentText()]()

    def saveScript(self):
        path, filter = QFileDialog.getSaveFileName(self, "Save ChimerX Script", "", "Script (*.cxc)")
        if path:
            try:
                with open(path, 'w') as f:
                    f.write(self.movie_script.toPlainText())
            except Exception as e:
                pass

    def runScript(self):
        command = self.movie_script.toPlainText().replace("'", "")
        for cmd in command.splitlines():
            commands.run(self.session, cmd)

    def checkModels(self) -> list:
        return objects.AllObjects(self.session).models
        
    def checkViews(self) -> list:      
        if not hasattr(self.session, '_named_views'):
            self.session._named_views = nvs = NamedViews()
        views = [view for view in self.session._named_views.views]
        views.sort()
        return views

    @pyqtSlot(list)
    def updateModels(self, models:list):
        self.current_models = models
        for picker in self.pickers:
            picker.updateModels(self.current_models)
    
    def focusView(self):
        corners = self.scene.findSceneCorners()
        self.centerOn(corners[0], corners[1], corners[2], corners[3])
        self.scaleOn(corners[0], corners[1], corners[2], corners[3])

    def centerOn(self, x1:float, y1:float, x2:float|None=None, y2:float|None=None):  
        if x2 is None or y2 is None:
            self.view.centerOn(QPointF(x1, y1))
        else:
            self.view.centerOn(QPointF(float((x1+x2)/2), float((y1+y2)/2)))

    def scaleOn(self, x1:float, y1:float, x2:float, y2:float):
        zoom_factor_width = self.view.width() / abs(x2 - x1)
        zoom_factor_height = self.view.height() / abs(y2 - y1)
        if zoom_factor_width < zoom_factor_height:
            scale = zoom_factor_width
        else:
            scale = zoom_factor_height
        if scale == 1:
            self.view.total_scale = 1
            self.view.zoom = self.view.startZoomStep[self.view.platform_index]
            self.view.scale(self.view.total_scale, self.view.total_scale)
        elif scale > 1:
            for i, value in enumerate(range(self.view.startZoomStep[self.view.platform_index], self.view.zoomRange[self.view.platform_index][1], 1)): 
                if scale < pow(self.view.zoomInFactor[self.view.platform_index], i + 1) and scale > pow(self.view.zoomInFactor[self.view.platform_index], i):
                    zoomFactor = pow(self.view.zoomInFactor[self.view.platform_index], i + 1) / self.view.total_scale
                    if int(zoomFactor) != 1:
                        self.view.scale(zoomFactor, zoomFactor)
                        self.view.total_scale = pow(self.view.zoomInFactor[self.view.platform_index], i + 1)
                        self.view.zoom = value
                    break
                elif i == self.view.startZoomStep[self.view.platform_index]:
                    zoomFactor = pow(self.view.zoomInFactor[self.view.platform_index], i + 1) / self.view.total_scale
                    if int(zoomFactor) != 1:
                        self.view.scale(zoomFactor, zoomFactor)
                        self.view.total_scale = pow(self.view.zoomInFactor[self.view.platform_index], i + 1)
                        self.view.zoom = value
                    break
        elif scale < 1:
            zoomOutFactor = 1 / self.view.zoomInFactor[self.view.platform_index]
            for i, value in enumerate(range(self.view.startZoomStep[self.view.platform_index], self.view.zoomRange[self.view.platform_index][0], -1)):
                if scale < pow(zoomOutFactor, i) and scale > pow(zoomOutFactor, i + 1):
                    zoomFactor = pow(zoomOutFactor, i + 1) / self.view.total_scale
                    if int(zoomFactor) != 1:
                        self.view.scale(zoomFactor, zoomFactor)
                        self.view.total_scale = pow(zoomOutFactor, i + 1)
                        self.view.zoom = value
                    break
                elif i == self.view.startZoomStep[self.view.platform_index] - 1:
                    zoomFactor = pow(zoomOutFactor, i + 1) / self.view.total_scale
                    if int(zoomFactor) != 1:
                        self.view.scale(zoomFactor, zoomFactor)
                        self.view.total_scale = pow(zoomOutFactor, i + 1)
                        self.view.zoom = value
                    break

    def reset(self, preset:bool=False):  
        self.scene.nodes = []
        self.scene.nodes_id = []
        self.scene.edges = []
        if not preset:
            self.view.zoom = 10
            zoomFactor = 1 / self.view.total_scale
            self.view.scale(zoomFactor, zoomFactor)
            self.view.total_scale = 1
            self.centerOn(0, 0)
        
        self.view_model = QStandardItemModel()
        self.model_model = QStandardItemModel()
        self.label2D_model = QStandardItemModel()
        self.label3D_model = QStandardItemModel()

        self.copy_selected_model_objects = None
        self.copy_selected_color_objects = None
        self.copy_selected_center_objects = None
        self.copy_selected_view_objects = None
        self.copy_selected_fly_objects = None
        self.copy_selected_fly_objects_transition_frames = None
        self.copy_selected_label2D_objects = None
        self.copy_selected_label3D_objects = None

        self.pickers:list[QTreeViewSelector] = []


        self.scene.grScene.clear()
        
        self.nodeStart = Node(self.session, self.scene, NodeType.Start, removable=False, has_input=False)
        self.nodeEnd = Node(self.session, self.scene, NodeType.End, removable=False, has_output=False)

        self.nodeStart.setPos(-300,-300)
        self.nodeEnd.setPos(-200,-200)

        self.scene.grScene.update()

class ScriptJob(tasks.Job):
    def __init__(self, session, editor:NodeEditor, parent=None):
        super().__init__(session)

        self.updater = ScriptViewerUpdater(session, editor)

    def run(self):
        self.updater.run()
        return
        
class ScriptViewerUpdater(QObject):
    send_command = pyqtSignal(list)
    def __init__(self, session, editor:NodeEditor, parent=None):
        super().__init__(parent)
        self.editor = editor
        self.current_script = ""
        self.send_command.connect(self.editor.updateViewerText)

    def run(self):
        while ToolStatus(self.editor.tool_status) == ToolStatus.RUNNING:
            command_string = self.editor.generateViewer()
            if self.current_script != command_string:
                self.current_script = command_string
                self.send_command.emit(self.current_script)
            time.sleep(1)
        return

class ModelJob(tasks.Job):
    def __init__(self, session, editor:NodeEditor, parent=None):
        super().__init__(session)

        self.updater = ModelUpdater(session, editor)

    def run(self):
        self.updater.run()
        return
        
class ModelUpdater(QObject):
    send_command = pyqtSignal(list)
    def __init__(self, session, editor:NodeEditor, parent=None):
        super().__init__(parent)
        self.editor = editor
        self.objs_models = None
        self.views = None
        self.send_command.connect(self.editor.updateModels)

    def run(self):
        while ToolStatus(self.editor.tool_status) == ToolStatus.RUNNING:
            models_list = []
            models = False
            view = False
            objs_models = self.editor.checkModels()
            if self.objs_models is None:
                self.objs_models = objs_models
                models = True
            elif self.objs_models != objs_models:
                self.objs_models = objs_models
                models = True
            views = self.editor.checkViews()
            if self.views is None:
                self.views = views
                view = True
            elif self.views != views:     
                self.views = views
                view = True
            if models or view:
                models_list = [self.objs_models, self.views]
                self.send_command.emit(models_list)
            time.sleep(1)
        return
