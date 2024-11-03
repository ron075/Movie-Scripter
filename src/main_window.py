from __future__ import annotations

from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *
from chimerax.core import objects, tasks
from chimerax.std_commands.view import NamedViews
import os
import time
import queue
from .util import *
from .node import *
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
        self.help_menu = HelpMenu(self.session, self)

        self.command_queue = queue.Queue()

        self.log = f"<u><b>Commands Log:</u></b><br>"
        self.log_count:int = 1

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
        
        self.nodeStart = Node(self.session, self.scene, NodeType.Start, removable=False, parent=self)
        self.nodeEnd = Node(self.session, self.scene, NodeType.End, removable=False, has_output=False, parent=self)

        self.nodeStart.setPos(-300,-300)
        self.nodeEnd.setPos(-150,-150)

        self.editor_layout = QVBoxLayout(self)

        # create graphics view
        self.layoutS1 = QSplitter(self)
        self.view = QDMGraphicsView(self.scene.grScene, self)
        self.script = QTextDocument()
        self.script_window_widget = QWidget(self)
        self.layoutS1V1 = QVBoxLayout()
        self.layoutS1V1.setContentsMargins(0, 0, 0, 0)
        self.script_window = QTextEdit()
        self.script_window.setCursor(Qt.CursorShape.ArrowCursor)
        self.script_window.setDocument(self.script)
        self.script_window.setReadOnly(True)
        self.script_window.hide()
        self.script_window.setMinimumWidth(200)
        self.layoutS1V1H1 = QHBoxLayout()
        self.save_log = QPushButton("Save")
        self.save_log.hide()
        self.save_log.clicked.connect(self.saveLog)
        self.reset_log = QPushButton("Reset")
        self.reset_log.hide()
        self.reset_log.clicked.connect(self.resetLog)
        self.layoutS1V1H1.addWidget(self.save_log)
        self.layoutS1V1H1.addWidget(self.reset_log)
        self.layoutS1V1.addWidget(self.script_window)
        self.layoutS1V1.addLayout(self.layoutS1V1H1)
        self.script_window_widget.setLayout(self.layoutS1V1)
        self.layoutS1.addWidget(self.view)
        self.layoutS1.addWidget(self.script_window_widget)
        
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
        changeEnabled(self.viewer_button, False)
        self.viewer_button.clicked.connect(self.scriptWindow)
        self.mode_button = QPushButton("Mode: Simple")
        self.mode_button.setProperty("State", "Simple")
        self.mode_button.clicked.connect(self.ToggleMode)
        self.light_mode = QLabel()
        self.light_mode.setObjectName("light_mode")
        self.light_mode.setFixedHeight(30)
        self.light_mode.setFixedWidth(30)
        self.theme_toggle = QSwitchControl(self, checked=True, radius=20)
        self.switches.append(self.theme_toggle)
        self.theme_toggle.stateChanged.connect(self.changeStyle)
        self.theme_toggle.setObjectName("theme_toggle")
        self.dark_mode = QLabel()
        self.dark_mode.setObjectName("dark_mode")
        self.dark_mode.setFixedHeight(30)
        self.dark_mode.setFixedWidth(30)
        self.settings_button = QPushButton("")
        self.settings_button.setProperty("State", "Closed")
        self.settings_button.setObjectName("settings_button")
        self.settings_button.clicked.connect(self.settings_menu.openSettings)
        self.help_button = QPushButton("")
        self.help_button.setObjectName("help_button")
        self.help_button.clicked.connect(self.help_menu.openHelp)
        self.layoutG1.addWidget(self.presets_box, 0, 0, 1, 1)
        self.layoutG1.addWidget(self.load_button, 1, 0, 1, 1)
        self.layoutG1.addWidget(self.center_button, 0, 1, 1, 1)
        self.layoutG1.addWidget(self.reset_button, 1, 1, 1, 1)
        self.layoutG1.addWidget(self.save_button, 0, 2, 1, 1)
        self.layoutG1.addWidget(self.run_button, 1, 2, 1, 1)
        self.layoutG1.addWidget(self.viewer_button, 0, 3, 1, 1)
        self.layoutG1.addWidget(self.mode_button, 1, 3, 1, 1)
        self.layoutG1.addWidget(self.light_mode, 0, 4, 1, 2, alignment=Qt.AlignmentFlag.AlignCenter)
        self.layoutG1.addWidget(self.theme_toggle, 0, 6, 1, 2, alignment=Qt.AlignmentFlag.AlignCenter)
        self.layoutG1.addWidget(self.dark_mode, 0, 8, 1, 2, alignment=Qt.AlignmentFlag.AlignCenter)
        self.layoutG1.addWidget(self.settings_button, 1, 4, 1, 3, alignment=Qt.AlignmentFlag.AlignCenter)
        self.layoutG1.addWidget(self.help_button, 1, 7, 1, 3, alignment=Qt.AlignmentFlag.AlignCenter)
        self.layoutG1.setColumnStretch(0, 2)  
        self.layoutG1.setColumnStretch(1, 2)  
        self.layoutG1.setColumnStretch(2, 2)  
        self.layoutG1.setColumnStretch(3, 2)  
        
        self.editor_layout.addWidget(self.layoutS1)
        self.editor_layout.addLayout(self.layoutG1)

        self.setLayout(self.editor_layout) 

        self.presets = Presets(self.session, self)
        self.reload_presets()

        self.settings_menu.raise_()

        self.scene.grScene.addItem(self.help_menu.grHelp)

        self.changeStyle()

        changeCursor(self.children())

        self.script_thread = ScriptJob(self.session, self)
        self.script_thread.start()
        self.model_thread = ModelJob(self.session, self)
        self.model_thread.start()
        self.command_thread = CommandJob(self.session, self)
        self.command_thread.start()
        
    @pyqtSlot(str)
    def runCommand(self, command:str):
        commands.run(self.session, self.strip_html_tags(command))
        if '#' in command:
            cmd = []
            for c in command.split(" "):
                if c != "":
                    if c[0] == "#":
                        cmd.append(f"<a style='background-color:{c};'>{c}</a>")
                    else:
                        cmd.append(c)
            command = " ".join(cmd)
        self.log += f"<b>{self.log_count}.</b> {command}<br>"
        self.log_count += 1
        value = self.script_window.verticalScrollBar().value()
        self.script_window.setHtml(self.log)
        if self.script_window.verticalScrollBar().maximum() < value:
            self.script_window.verticalScrollBar().setValue(self.script_window.verticalScrollBar().maximum())
        else:
            self.script_window.verticalScrollBar().setValue(value)

    def reload_presets(self):
        self.presets.prepare_presets()
        if self.mode_button.property("State") == "Simple":
            self.loaded_presets = self.presets.simple_prestes
        elif self.mode_button.property("State") == "Advanced":
            self.loaded_presets = self.presets.advanced_prestes
        self.presets_box.clear()
        self.presets_box.addItems(self.loaded_presets.keys())

    def ToggleMode(self):
        if self.mode_button.property("State") == "Simple":
            self.mode_button.setProperty("State", "Advanced")
            self.mode_button.setText("Mode: Advanced")
            self.loaded_presets = self.presets.advanced_prestes
        elif self.mode_button.property("State") == "Advanced":
            self.mode_button.setProperty("State", "Simple")
            self.mode_button.setText("Mode: Simple")
            self.loaded_presets = self.presets.simple_prestes
        self.simple_mode = not self.simple_mode  
        if self.viewer_button.property("State") == "Log":
            self.save_log.hide()
            self.reset_log.hide()
        self.viewer_button.setProperty("State", "Close")
        changeEnabled(self.viewer_button, not self.simple_mode)
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
        self.help_menu.changeStyle(style)
        self.scene.changeStyle(style)
        for switch in self.switches:
            if hasattr(switch.editor, "theme_toggle"):
                switch.changeStyle(style)

    def scriptWindow(self):
        if self.viewer_button.property("State") == "None":
            self.viewer_button.setProperty("State", "Script")
            self.viewer_button.setText("Viewer: Script")
            self.script_window.show()
            self.updateViewerText()
        elif self.viewer_button.property("State") == "Script":
            self.viewer_button.setProperty("State", "Queue")
            self.viewer_button.setText("Viewer: Queue")
            self.updateViewerText()
        elif self.viewer_button.property("State") == "Queue":
            self.viewer_button.setProperty("State", "Log")
            self.viewer_button.setText("Viewer: Log")
            self.save_log.show()
            self.reset_log.show()
            self.updateViewerText()
        elif self.viewer_button.property("State") == "Log":
            self.viewer_button.setProperty("State", "Comments")
            self.viewer_button.setText("Viewer: Comments")
            self.save_log.hide()
            self.reset_log.hide()
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

    def strip_html_tags(self, html:str) -> str:
        html = html.replace("'", "")
        clean = re.compile('<.*?>')
        return re.sub(clean, '', html)
    
    def generateQueueSummary(self) -> str:
        summary = f"<u><b>Command delay:</u></b> {self.settings_menu.command_delay}<br>"
        summary += f"<u><b>Commands Queue:</u></b><br>"
        i = 1
        for cmd in self.command_queue.queue:
            if cmd != "":
                if '#' in cmd:
                    new_cmd = []
                    for c in cmd.split(" "):
                        if c != "":
                            if c[0] == "#":
                                new_cmd.append(f"<a style='background-color:{c};'>{c}</a>")
                            else:
                                new_cmd.append(c)
                    cmd = " ".join(new_cmd)
                summary += f"<b>{i}.</b> {cmd}<br>"
                i += 1
        return summary

    def generateSummary(self) -> str:
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
        while current_node.has_input:
            if current_node.node_input is not None:
                if current_node.node_input.hasEdge():
                    current_node = current_node.node_input.edge.start_socket.node
                else:
                    break

        starting_node = current_node
        node_order_type = f"{starting_node.nodeType.name}"
        node_order_id = f"{starting_node.nodeID}"

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
                    node_order_type += f" → {current_node.nodeType.name}"
                    node_order_id += f" → {current_node.nodeID}"
                else:
                    current_node = None
            else:
                current_node = None
        node_frequency = dict(sorted(node_frequency.items()))

        length = convertTime(int(frames) / int(self.nodeEnd.content.Framerate.Text.text()))
                
        summary = f""    
        summary += f"<u><b>Model Refresh Rate (sec):</u></b> {self.settings_menu.model_refresh}<br>"
        summary += f"<u><b>Viewer Refresh Rate (sec):</u></b> {self.settings_menu.viewer_refresh}<br>"
        summary += f"<u><b>Command delay:</u></b> {self.settings_menu.command_delay}<br>"
        summary += f"<br>"
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
        
        summary += f"<u><b>Node Order (node type):</u></b><br>"
        summary += f"{node_order_type}"
        summary += f"<br>"
        summary += f"<br>"

        summary += f"<u><b>Node Order (node ID):</u></b><br>"
        summary += f"{node_order_id}"
        summary += f"<br>"
        summary += f"<br>"
        return summary
    
    def generateViewer(self) -> list[str]:
        do_record = self.nodeStart.content.Record.isChecked()
        current_node = self.nodeStart
        while current_node.has_input:
            if current_node.node_input is not None:
                if current_node.node_input.hasEdge():
                    current_node = current_node.node_input.edge.start_socket.node
                else:
                    break
        start_command = ""
        command = ""
        end_command = ""
        queue_string = ""
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
                queue_string = self.generateQueueSummary()
                comment_string = current_node.content.updateComment()
                summary = self.generateSummary()
                if comment_string != []:
                    start_comment += comment_string[0]
                    comment += comment_string[1]
                    end_comment += comment_string[2]
            else:
                queue_string = ""
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
            return [start_command + command + end_command, queue_string, start_comment + comment + end_comment, summary]
        else:
            return [command, queue_string, comment, summary]
        
    def saveLog(self):
        if self.settings_menu.save_log_folder != "":
            if not os.path.exists(self.settings_menu.save_log_folder):
                self.settings_menu.save_log_folder = ""
        path, filter = QFileDialog.getSaveFileName(self, "Save command log", self.settings_menu.save_log_folder, "text (*.txt)")
        if path:
            folder = path.rsplit('/', 1)[0]
            if folder != "":
                self.settings_menu.save_log_folder = path.rsplit('/', 1)[0]
                self.settings_menu.lSaveLogFolder.setText(folder)
            try:
                log_document = QTextDocument()
                log_document.setHtml(self.log)
                with open(path, 'w') as f:
                    f.write(log_document.toPlainText())
            except Exception as e:
                pass

    def resetLog(self):
        self.log = f"<u><b>Commands Log:</u></b><br>"
        self.log_count:int = 1
        self.script_window.setHtml(self.log)
                
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
            elif self.viewer_button.property("State") == "Queue":
                text = self.viewer_texts[1]
            elif self.viewer_button.property("State") == "Log":
                text = self.log
            elif self.viewer_button.property("State") == "Comments":
                text = self.viewer_texts[2]
            elif self.viewer_button.property("State") == "Summary":
                text = self.viewer_texts[3]
            if text is not None:
                value = self.script_window.verticalScrollBar().value()
                self.script_window.setHtml(text)
                if self.script_window.verticalScrollBar().maximum() < value:
                    self.script_window.verticalScrollBar().setValue(self.script_window.verticalScrollBar().maximum())
                else:
                    self.script_window.verticalScrollBar().setValue(value)
            
    def loadPreset(self):
        self.reset(preset=True)
        if self.presets_box.currentIndex() > -1:
            self.loaded_presets[self.presets_box.currentText()]()

    def saveScript(self):
        if self.settings_menu.save_script_folder != "":
            if not os.path.exists(self.settings_menu.save_script_folder):
                self.settings_menu.save_script_folder = ""
        path, filter = QFileDialog.getSaveFileName(self, "Save ChimerX Script", self.settings_menu.save_script_folder, "Script (*.cxc)")
        if path:
            folder = path.rsplit('/', 1)[0]
            if folder != "":
                self.settings_menu.save_script_folder = path.rsplit('/', 1)[0]
                self.settings_menu.lSaveScriptFolder.setText(folder)
            try:
                with open(path, 'w') as f:
                    f.write(self.movie_script.toPlainText())
            except Exception as e:
                pass

    def runScript(self):
        command = self.movie_script.toPlainText().replace("'", "")
        for cmd in command.splitlines():
            self.command_queue.put(cmd)

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
        with self.command_queue.mutex:
            self.command_queue.queue.clear()
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
        self.switches:list[QSwitchControl] = []

        self.scene.grScene.clear()
        
        self.nodeStart = Node(self.session, self.scene, NodeType.Start, removable=False)
        self.nodeEnd = Node(self.session, self.scene, NodeType.End, removable=False, has_output=False)

        self.nodeStart.setPos(-300,-300)
        self.nodeEnd.setPos(-150,-150)

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
        self.current_script = []
        self.send_command.connect(self.editor.updateViewerText)

    def run(self):
        while ToolStatus(self.editor.tool_status) == ToolStatus.RUNNING:
            command_string = self.editor.generateViewer()
            if self.current_script != command_string:
                self.current_script = command_string
                self.send_command.emit(self.current_script)
            time.sleep(self.editor.settings_menu.viewer_refresh)
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
            time.sleep(self.editor.settings_menu.model_refresh)
        return

class CommandJob(tasks.Job):
    def __init__(self, session, editor:NodeEditor, parent=None):
        super().__init__(session)

        self.updater = CommandSender(session, editor)

    def run(self):
        self.updater.run()
        return
        
class CommandSender(QObject):
    send_command = pyqtSignal(str)
    def __init__(self, session, editor:NodeEditor, parent=None):
        super().__init__(parent)
        self.editor = editor
        self.send_command.connect(self.editor.runCommand)

    def run(self):
        while ToolStatus(self.editor.tool_status) == ToolStatus.RUNNING:
            if self.editor.command_queue.qsize() > 0:
                cmd = self.editor.command_queue.get()
                if cmd != "":
                    self.send_command.emit(cmd)
                time.sleep(self.editor.settings_menu.command_delay)
            else:
                time.sleep(1)
        return