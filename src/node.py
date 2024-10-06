from __future__ import annotations

from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from sys import platform
from .sockets import *
from .edges import *
from .node_base import *
from .simple_nodes import *
from .advanced_nodes import *
from .enum_classes import *
from .info import *
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .graphics_scene import Scene
    from .main_window import NodeEditor

class Node():
    def __init__(self, session, scene:Scene, nodeType:NodeType, has_input:bool=True, has_output:bool=True, node_id:str="", nodePickerType:NodePickerType=NodePickerType.NoPicker, removable:bool=True, model_input:bool=False, color_input:bool=False, center_input:bool=False, view_input:bool=False, fly_input:bool=False, delete_input:bool=False, split_input:bool=False, pos_x:int=0, pos_y:int=0, index:int=0, colormap_height:int=50, parent:NodeEditor=None):
        self.session = session

        self.parent = parent

        self.scene = scene
        self.nodeType = nodeType
        if node_id == "":
            self.nodeID = self.scene.assignID(self)
        else:
            self.nodeID = node_id
        self.colormap_height = colormap_height
        self.nodePickerType = nodePickerType
        
        self.removable = removable
        self.is_deleting = False
        self.has_input = has_input
        self.has_output = has_output

        self.index = index
        self.input_model:Node|None = None
        self.input_model_edge:Edge|None = None
        self.input_color:Node|None = None
        self.input_color_edge:Edge|None = None
        self.input_center:Node|None = None
        self.input_center_edge:Edge|None = None
        self.input_view:Node|None = None
        self.input_view_edge:Edge|None = None
        self.input_fly:Node|None = None
        self.input_fly_edge:Edge|None = None
        self.input_delete:Node|None = None
        self.input_delete_edge:Edge|None = None
        self.input_split:Node|None = None
        self.input_split_edge:Edge|None = None
        
        if self.scene.parent.simple_mode:
            self.summary = SimpleNodeSummary(self.session, self, model_input, color_input, center_input, view_input, fly_input)
            if NodeType(self.nodeType) == NodeType.Start:
                self.content = SimpleNodeStart(self.session, self.summary, "Record")
            elif NodeType(self.nodeType) == NodeType.Picker:
                self.content = SimpleNodePicker(self.session, self.scene, self.summary, all_views=True, selector_type=self.nodePickerType)
            elif NodeType(self.nodeType) == NodeType.ColorPalette:
                self.content = SimpleNodeColorPalette(self.session, self.summary, "Color Palette", self.colormap_height)
            elif NodeType(self.nodeType) == NodeType.Transparency:
                self.content = SimpleNodeTransparency(self.session, self.summary, "Transparency")
            elif NodeType(self.nodeType) == NodeType.Rotation:
                self.content = SimpleNodeRotation(self.session, self.summary, "Rotation")
            elif NodeType(self.nodeType) == NodeType.Wait:
                self.content = SimpleNodeWait(self.session, self.summary, "Wait")
            elif NodeType(self.nodeType) == NodeType.Delete:
                self.content = SimpleNodeDelete(self.session, self.scene, self.summary, "Delete")
            elif NodeType(self.nodeType) == NodeType.Split:
                self.content = SimpleNodeSplit(self.session, self.summary, "Split")
            elif NodeType(self.nodeType) == NodeType.End:
                self.content = SimpleNodeEnd(self.session, self.summary, "Finish")
        else:
            self.summary = AdvancedNodeSummary(self.session, self, model_input, color_input, center_input, view_input, fly_input)

            if NodeType(self.nodeType) == NodeType.Start:
                self.content = AdvancedNodeStart(self.session, self.summary, "Record")
            elif NodeType(self.nodeType) == NodeType.Picker:
                self.content = AdvancedNodePicker(self.session, self.scene, self.summary, all_views=True, selector_type=self.nodePickerType)
            elif NodeType(self.nodeType) == NodeType.ColorPalette:
                self.content = AdvancedNodeColorPalette(self.session, self.summary, "Color Palette", self.colormap_height)
            elif NodeType(self.nodeType) == NodeType.Lighting:
                self.content = AdvancedNodeLighting(self.session, self.summary, "Lighting")
            elif NodeType(self.nodeType) == NodeType.Transparency:
                self.content = AdvancedNodeTransparency(self.session, self.summary, "Transparency")
            elif NodeType(self.nodeType) == NodeType.Label2D:
                self.content = AdvancedNode2DLabel(self.session, self.summary, "2D Label")
            elif NodeType(self.nodeType) == NodeType.Label3D:
                self.content = AdvancedNode3DLabel(self.session, self.summary, "3D Label")
            elif NodeType(self.nodeType) == NodeType.Movement:
                self.content = AdvancedNodeMovement(self.session, self.summary, "Movement")
            elif NodeType(self.nodeType) == NodeType.Rotation:
                self.content = AdvancedNodeRotation(self.session, self.summary, "Rotation")
            elif NodeType(self.nodeType) == NodeType.CenterRotation:
                self.content = AdvancedNodeCenterRotation(self.session, self.summary, "Center of Rotation")
            elif NodeType(self.nodeType) == NodeType.CenterMass:
                self.content = AdvancedNodeCenterMass(self.session, self.summary, "Center of Mass")
            elif NodeType(self.nodeType) == NodeType.Delete:
                self.content = AdvancedNodeDelete(self.session, self.scene, self.summary, "Delete")
            elif NodeType(self.nodeType) == NodeType.Wait:
                self.content = AdvancedNodeWait(self.session, self.summary, "Wait")
            elif NodeType(self.nodeType) == NodeType.Crossfade:
                self.content = AdvancedNodeCrossfade(self.session, self.summary, "Crossfade")
            elif NodeType(self.nodeType) == NodeType.View_Save:
                self.content = AdvancedNodeSaveView(self.session, self.summary, "Save View")
            elif NodeType(self.nodeType) == NodeType.View_Load:
                self.content = AdvancedNodeLoadView(self.session, self.summary, "Load View")
            elif NodeType(self.nodeType) == NodeType.Fly:
                self.content = AdvancedNodeFly(self.session, self.summary, "Fly")
            elif NodeType(self.nodeType) == NodeType.Split:
                self.content = AdvancedNodeSplit(self.session, self.summary, "Split")
            elif NodeType(self.nodeType) == NodeType.End:
                self.content = AdvancedNodeEnd(self.session, self.summary, "Finish")
        
        self.title:str = self.content.title

        self.inputs_counter = 0
        if self.has_input or self.has_output or NodeType(self.nodeType) == NodeType.Picker:
            self.inputs_counter += 1
        if model_input:
            self.inputs_counter += 1
        if color_input:
            self.inputs_counter += 1
        if center_input:
            self.inputs_counter += 1
        if view_input:
            self.inputs_counter += 1
        if fly_input:
            self.inputs_counter += 1
        if delete_input:
            self.inputs_counter += 1

        self.grNode = QDMGraphicsNode(self, self.inputs_counter)
        self.setPos(pos_x, pos_y)

        self.help_strings = Info().set_info(self)
        self.set_info(self.scene.parent.settings_menu.current_info_type)

        self.scene.addNode(self)
        self.scene.grScene.addItem(self.grNode)

        self.socket_spacing = 22
        self.node_input:Socket|None = None
        self.node_output:Socket|None = None
        self.picker_inputs:list[Socket] = []
        
        counter = 0
        if model_input:
            socket = Socket(node=self, index=counter, position=Position.LEFT_TOP, socket_type=SocketType.MODEL_SOCKET)
            self.input_model = Node(self.session, self.scene, NodeType.Picker, nodePickerType=NodePickerType.ModelPicker, removable=False, index=counter, has_input=False, has_output=False, parent=self.parent)
            self.picker_inputs.append(socket)
            self.input_model_edge = Edge(self.scene, self.input_model.node_output, self.picker_inputs[counter], removable=False)
            if NodeType(self.nodeType) != NodeType.Split:
                if not self.scene.parent.simple_mode:
                    self.input_model.grNode.hide()
                    self.input_model_edge.grEdge.hide()
                else:
                    self.input_model.setSelfPos(self.pos.x(), self.pos.y(), self.inputs_counter)
            else:
                self.input_model.setSelfPos(self.pos.x(), self.pos.y(), self.inputs_counter)
            counter += 1
        if color_input:
            socket = Socket(node=self, index=counter, position=Position.LEFT_TOP, socket_type=SocketType.COLOR_SOCKET)
            self.input_color = Node(self.session, self.scene, NodeType.Picker, nodePickerType=NodePickerType.ColorPicker, removable=False, index=counter, has_input=False, has_output=False, parent=self.parent)
            self.picker_inputs.append(socket)
            self.input_color_edge = Edge(self.scene, self.input_color.node_output, self.picker_inputs[counter], removable=False)
            if not self.scene.parent.simple_mode:
                self.input_color.grNode.hide()
                self.input_color_edge.grEdge.hide()
            else:               
                self.input_color.setSelfPos(self.pos.x(), self.pos.y(), self.inputs_counter) 
            counter += 1
        if center_input:
            socket = Socket(node=self, index=counter, position=Position.LEFT_TOP, socket_type=SocketType.CENTER_SOCKET)
            self.input_center = Node(self.session, self.scene, NodeType.Picker, nodePickerType=NodePickerType.CenterPicker, removable=False, index=counter, has_input=False, has_output=False, parent=self.parent)
            self.picker_inputs.append(socket)
            self.input_center_edge = Edge(self.scene, self.input_center.node_output, self.picker_inputs[counter], removable=False)
            if not self.scene.parent.simple_mode:
                self.input_center.grNode.hide()  
                self.input_center_edge.grEdge.hide()
            else:
                self.input_center.setSelfPos(self.pos.x(), self.pos.y(), self.inputs_counter)  
            counter += 1
        if view_input:
            socket = Socket(node=self, index=counter, position=Position.LEFT_TOP, socket_type=SocketType.VIEW_SOCKET)
            self.input_view = Node(self.session, self.scene, NodeType.Picker, nodePickerType=NodePickerType.ViewPicker, removable=False, index=counter, has_input=False, has_output=False, parent=self.parent)
            self.picker_inputs.append(socket)
            self.input_view_edge = Edge(self.scene, self.input_view.node_output, self.picker_inputs[counter], removable=False)
            if not self.scene.parent.simple_mode:
                self.input_view.grNode.hide()
                self.input_view_edge.grEdge.hide()
            else:
                self.input_view.setSelfPos(self.pos.x(), self.pos.y(), self.inputs_counter)  
            counter += 1  
        if fly_input:
            socket = Socket(node=self, index=counter, position=Position.LEFT_TOP, socket_type=SocketType.FLY_SOCKET)
            self.input_fly = Node(self.session, self.scene, NodeType.Picker, nodePickerType=NodePickerType.FlyPicker, removable=False, index=counter, has_input=False, has_output=False, parent=self.parent)
            self.picker_inputs.append(socket)
            self.input_fly_edge = Edge(self.scene, self.input_fly.node_output, self.picker_inputs[counter], removable=False)
            if not self.scene.parent.simple_mode:
                self.input_fly.grNode.hide()
                self.input_fly_edge.grEdge.hide()
            else:
                self.input_fly.setSelfPos(self.pos.x(), self.pos.y(), self.inputs_counter)  
            counter += 1
        if delete_input:
            socket = Socket(node=self, index=counter, position=Position.LEFT_TOP, socket_type=SocketType.DELETE_SOCKET)
            self.input_delete = Node(self.session, self.scene, NodeType.Picker, nodePickerType=NodePickerType.DeletePicker, removable=False, index=counter, has_input=False, has_output=False, parent=self.parent)
            self.picker_inputs.append(socket)
            self.input_delete_edge = Edge(self.scene, self.input_delete.node_output, self.picker_inputs[counter], removable=False)
            counter += 1
        if self.has_input:
            socket = Socket(node=self, index=counter, position=Position.LEFT_TOP, socket_type=SocketType.INPUT_SOCKET)
            counter += 1
            self.node_input = (socket)

        counter = 0
        if NodeType(self.nodeType) == NodeType.Picker:
            if NodePickerType(self.nodePickerType) == NodePickerType.ModelPicker:
                socket = Socket(node=self, index=counter, position=Position.RIGHT_TOP, socket_type=SocketType.MODEL_SOCKET)
                counter += 1
                self.node_output = socket
            elif NodePickerType(self.nodePickerType) == NodePickerType.ColorPicker:
                socket = Socket(node=self, index=counter, position=Position.RIGHT_TOP, socket_type=SocketType.COLOR_SOCKET)
                counter += 1
                self.node_output = socket
            elif NodePickerType(self.nodePickerType) == NodePickerType.CenterPicker:
                socket = Socket(node=self, index=counter, position=Position.RIGHT_TOP, socket_type=SocketType.CENTER_SOCKET)
                counter += 1
                self.node_output = socket
            elif NodePickerType(self.nodePickerType) == NodePickerType.ViewPicker:
                socket = Socket(node=self, index=counter, position=Position.RIGHT_TOP, socket_type=SocketType.VIEW_SOCKET)
                counter += 1
                self.node_output = socket
            elif NodePickerType(self.nodePickerType) == NodePickerType.FlyPicker:
                socket = Socket(node=self, index=counter, position=Position.RIGHT_TOP, socket_type=SocketType.FLY_SOCKET)
                counter += 1
                self.node_output = socket
            elif NodePickerType(self.nodePickerType) == NodePickerType.DeletePicker:
                socket = Socket(node=self, index=counter, position=Position.RIGHT_TOP, socket_type=SocketType.DELETE_SOCKET)
                counter += 1
                self.node_output = socket
        elif self.has_output:
            socket = Socket(node=self, index=counter, position=Position.RIGHT_TOP, socket_type=SocketType.OUTPUT_SOCKET)
            counter += 1
            self.node_output = socket

        if NodeType(self.nodeType) != NodeType.Picker:
            if hasattr(self.scene.parent, "theme_toggle"):  
                if self.scene.parent.theme_toggle.isChecked():
                    self.changeStyle(Stylesheet.LIGHT)
                else:
                    self.changeStyle(Stylesheet.DARK)
                    
    def set_info(self, info_strings_format:int):
        self.grNode.info.setToolTip(self.help_strings[info_strings_format])

    def changeStyle(self, style:Stylesheet):
        self.grNode.info.setStyleSheet(self.scene.parent.stylesheets[style.name])
        self.summary.setStyleSheet(self.scene.parent.stylesheets[style.name])
        self.content.setStyleSheet(self.scene.parent.stylesheets[style.name])
        self.grNode._title_color = self.scene.parent.styles._title_color[style.value]
        self.grNode._title_color = self.scene.parent.styles._title_color[style.value]
        self.grNode.title_item.setDefaultTextColor(self.grNode._title_color)
        self.grNode._brush_title_color = QColor(self.scene.parent.styles._node_brush_title[style.value])
        self.grNode._brush_background_color = QColor(self.scene.parent.styles._node_brush_background[style.value])
        self.grNode.updateBrushesAlpha()
        self.grNode._brush_title.setColor(self.grNode._brush_title_color)
        self.grNode._brush_background.setColor(self.grNode._brush_background_color)   
        self.grNode._pen_default.setColor(QColor(self.scene.parent.styles._node_pen_default[style.value])) 
        if self.node_input is not None:
            self.node_input.changeStyle(style)       
        if self.node_output is not None:
            self.node_output.changeStyle(style)       
        if NodeType(self.nodeType) != NodeType.Picker:
            for picker in self.picker_inputs:
                picker.changeStyle(style)
                picker.edge.changeStyle(style)
                picker.edge.start_socket.node.changeStyle(style)
                picker.edge.start_socket.changeStyle(style)

    def setSelfPos(self, parent_x:int, parent_y:int, input_count:int):
        x = parent_x - 300
        y = parent_y - int(100 * input_count / 2) + 75 * (self.index)
        self.grNode.setPos(x, y)

    @property
    def pos(self):
        return self.grNode.pos()
    def setPos(self, x:float, y:float):
        self.grNode.setPos(x, y)
    
    def getSocketPosition(self, index:int, position:Position) -> list[int]:
        width = self.grNode.node_width if self.grNode.node_width > 0 else self.grNode.width
        x = 0 if (position in (Position.LEFT_TOP, Position.LEFT_BOTTOM)) else width
        if position in (Position.LEFT_BOTTOM, Position.RIGHT_BOTTOM):
            y = self.grNode.height - self.grNode.edge_size - self.grNode._padding - index * self.socket_spacing
        else :
            y = self.grNode.title_height + self.grNode._padding + self.grNode.edge_size + index * self.socket_spacing

        return [x, y]
    
    def updateConnectedEdges(self):
        if self.node_input is not None:
            self.node_input.edge.updatePositions()
        if self.node_output is not None:
            self.node_output.edge.updatePositions()
        for socket in self.picker_inputs:
            if socket.hasEdge():
                socket.edge.updatePositions()

class QDMGraphicsNode(QGraphicsItem):
    def __init__(self, node:Node, socket_count:int, parent=None):
        super().__init__(parent)        
        self.node = node   
        self.socket_count = socket_count
        self.info = QPushButton("")
        self.info.setObjectName("info")
        self.content = self.node.content
        self.summary = self.node.summary

        self.first_load_content = True
        self.first_load_summary= True

        self.selected = True

        self._title_color = Qt.GlobalColor.black
        self._title_font = QFont(QApplication.font().family(), QApplication.font().pointSize())
        self._title_font.setBold(True)

        self.width = 160
        self.node_width = 0
        self.height = 24 * (socket_count + 1)
        self.node_height = 0
        self.edge_size = 10
        self.title_height = 24
        self._padding = 4

        self._current_pen = QPen(QColor("#7F000000"))
        self._pen_default = QPen(QColor("#7F000000"))
        self._pen_input = QPen(QColor("#FFFF3333"))
        self._pen_output = QPen(QColor("#FF00CC77"))
        self._pen_input.setWidth(2)
        self._pen_input.setStyle(Qt.PenStyle.DashLine)
        self._pen_output.setWidth(2)        
        self._pen_output.setStyle(Qt.PenStyle.DashLine)

        if NodeType(self.node.nodeType) == NodeType.Picker:
            if NodePickerType(self.node.nodePickerType) == NodePickerType.ModelPicker:
                self._pen_picker = QPen(QColor("#FFEEEE88"))
            elif NodePickerType(self.node.nodePickerType) == NodePickerType.ColorPicker:
                self._pen_picker = QPen(QColor("#FF80E5FF"))
            elif NodePickerType(self.node.nodePickerType) == NodePickerType.CenterPicker:
                self._pen_picker = QPen(QColor("#FFE580FF"))
            elif NodePickerType(self.node.nodePickerType) == NodePickerType.ViewPicker:
                self._pen_picker = QPen(QColor("#FF6600BB"))
            elif NodePickerType(self.node.nodePickerType) == NodePickerType.FlyPicker:
                self._pen_picker = QPen(QColor("#FFFFBB44"))
            elif NodePickerType(self.node.nodePickerType) == NodePickerType.DeletePicker:
                self._pen_picker = QPen(QColor("#FFCCCCCC"))
            #elif NodePickerType(self.node.nodePickerType) == NodePickerType.SplitPicker:
                #self._pen_picker = QPen(QColor("#FF6655FF"))
            self._pen_selected = self._pen_picker
            self._pen_picker.setWidth(2)        
            self._pen_picker.setStyle(Qt.PenStyle.DashLine)
        else:
            self._pen_selected = QPen(QColor("#FF5656FF"))

        self._brush_title_color = QColor("#FF313131")
        self._brush_background_color = QColor("#E3212121")
        self.updateBrushesAlpha()

        # init title
        self.initTitle()
        self.title = self.node.title

        self.initUI()
    @property
    def title(self): 
        return self._title
    @title.setter
    def title(self, value:str):
        self._title = value
        self.title_item.setPlainText(self._title)

    def boundingRect(self):
        if self.isSelected():
            return QRectF(0, 0, self.checkWidth(), self.checkHeight()).normalized()        
        else:
            return QRectF(0, 0, self.checkWidth(), self.checkHeight(self.node.socket_spacing * (self.node.inputs_counter - 1))).normalized()

    def updateBrushesAlpha(self):
        self._brush_title_color.setAlphaF(self.node.scene.parent.settings_menu.nodes_transparency_title / 100)
        self._brush_background_color.setAlphaF(self.node.scene.parent.settings_menu.nodes_transparency_background / 100)
        self._brush_title = QBrush(self._brush_title_color)
        self._brush_background = QBrush(self._brush_background_color)
        self.update()

    def initUI(self):
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsSelectable)
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsMovable)


    def initTitle(self):
        self.title_item = QGraphicsTextItem(self)
        self.title_item.setDefaultTextColor(self._title_color)
        if self._title_font is not None:
            self.title_item.setFont(self._title_font)
        self.title_item.setPos(self._padding, 0)

    def paint(self, painter:QPainter, QStyleOptionGraphicsItem:QStyleOptionGraphicsItem, widget=None): 
        if not self.node.is_deleting:
            if self.isSelected():
                if self.first_load_content:
                    self.initContent()
                    self.first_load_content = False
                else:
                    self.content.show()

                if not self.first_load_summary:
                    self.summary.hide()
                    
                summary_size = self.summary.main_layout.contentsRect()
                content_size = self.content.main_layout.contentsRect()
                self.node_height = (summary_size.height() if summary_size.height() > content_size.height() else content_size.height()) + (2 * self.edge_size) + self.title_height
                self.node_width = (summary_size.width() if summary_size.width() > content_size.width() else content_size.width()) + (4 * self.edge_size)

                self.info.move(self.node_width - self.title_height - 2, -2)

                if self.node.node_input is not None:
                    self.node.node_input.grSocket.setPos(*self.node.node_input.node.getSocketPosition(self.node.node_input.index, self.node.node_input.position))
                    if self.node.node_input.hasEdge():
                        self.node.node_input.edge.updatePositions() 
                if self.node.node_output is not None:
                    self.node.node_output.grSocket.setPos(*self.node.node_output.node.getSocketPosition(self.node.node_output.index, self.node.node_output.position))
                    if self.node.node_output.hasEdge():
                        self.node.node_output.edge.updatePositions() 
                for socket in self.node.picker_inputs:
                    socket.grSocket.setPos(*socket.node.getSocketPosition(socket.index, socket.position))
                    if socket.hasEdge():
                        socket.edge.updatePositions() 

                if not self.selected:
                    if NodeType(self.node.nodeType) == NodeType.Picker:
                        self._current_pen = self._pen_picker
                    else:
                        self._current_pen = self._pen_selected
                    self.setZValue(100)
                    self.selected = True
            else:
                if not self.first_load_content:
                    self.content.hide() 

                if self.first_load_summary:
                    self.initSummary()
                    self.initInfo()
                    self.first_load_summary = False
                else:
                    self.summary.show()
                    self.info.move(self.node_width - self.title_height - 2, -2)

                default = True
                if self.node.node_input is not None:
                    self.node.node_input.grSocket.setPos(*self.node.node_input.node.getSocketPosition(self.node.node_input.index, self.node.node_input.position))
                    if self.node.node_input.hasEdge():
                        self.node.node_input.edge.updatePositions() 
                        if self.node.node_input.edge.grEdge.isSelected():
                            self._current_pen = self._pen_selected
                            self.setZValue(80)
                            default = False
                        elif self.node.node_input.edge.start_socket.node.grNode.isSelected():
                            self._current_pen = self._pen_output
                            self.setZValue(70)
                            default = False
                if self.node.node_output is not None:
                    self.node.node_output.grSocket.setPos(*self.node.node_output.node.getSocketPosition(self.node.node_output.index, self.node.node_output.position))
                    if self.node.node_output.hasEdge():
                        self.node.node_output.edge.updatePositions() 
                        if self.node.node_output.edge.grEdge.isSelected():
                            self._current_pen = self._pen_selected
                            self.setZValue(80)
                            default = False
                        elif self.node.node_output.edge.end_socket.node.grNode.isSelected():
                            if NodeType(self.node.nodeType) == NodeType.Picker:
                                self._current_pen = self._pen_picker
                            else:
                                self._current_pen = self._pen_input
                            self.setZValue(70)
                            default = False
                for input in self.node.picker_inputs:
                    input.grSocket.setPos(*input.node.getSocketPosition(input.index, input.position))
                    if input.hasEdge():
                        input.edge.updatePositions()
                        if input.edge.grEdge.isSelected():
                            self._current_pen = input.edge.start_socket.node.grNode._pen_picker
                            self.setZValue(80)
                            default = False
                            break
                        elif input.edge.start_socket.node.grNode.isSelected():
                            if NodeType(input.edge.start_socket.node.nodeType) == NodeType.Picker:
                                self._current_pen = input.edge.start_socket.node.grNode._pen_picker
                                self.setZValue(80)
                            else:
                                self._current_pen = self._pen_output
                                self.setZValue(70)
                            default = False
                            break
                if self.selected:
                    summary_size = self.summary.main_layout.contentsRect()
                    content_size = self.content.main_layout.contentsRect()
                    self.node_height = self.summary.main_layout.contentsRect().height() + (2 * self.edge_size) + self.node.socket_spacing * (self.node.inputs_counter - 1)
                    self.node_width = self.summary.main_layout.contentsRect().width() + (4 * self.edge_size)
                    self.selected = False
                if default:
                    self._current_pen = self._pen_default
                    self.setZValue(5)
                    
            # title
            path_title = QPainterPath()
            path_title.setFillRule(Qt.FillRule.WindingFill)
            path_title.addRoundedRect(0, 0, (self.node_width if self.node_width > 0 else self.width), self.title_height, self.edge_size, self.edge_size)
            path_title.addRect(0, self.title_height - self.edge_size, self.edge_size, self.edge_size)
            path_title.addRect((self.node_width if self.node_width > 0 else self.width) - self.edge_size, self.title_height - self.edge_size, self.edge_size, self.edge_size)
            painter.setPen(Qt.PenStyle.NoPen)
            painter.setBrush(self._brush_title)
            painter.drawPath(path_title.simplified())

            # content
            path_content = QPainterPath()
            path_content.setFillRule(Qt.FillRule.WindingFill)
            path_content.addRoundedRect(0, self.title_height, (self.node_width if self.node_width > 0 else self.width), self.checkHeight() - self.title_height, self.edge_size, self.edge_size)
            path_content.addRect(0, self.title_height, self.edge_size, self.edge_size)
            path_content.addRect((self.node_width if not self.isSelected() else self.node_width) - self.edge_size, self.title_height, self.edge_size, self.edge_size)
            painter.setPen(Qt.PenStyle.NoPen)
            painter.setBrush(self._brush_background)
            painter.drawPath(path_content.simplified())

            # outline
            path_outline = QPainterPath()
            path_outline.addRoundedRect(0, 0, (self.node_width if self.node_width > 0 else self.width), self.checkHeight(), self.edge_size, self.edge_size)
                
            painter.setPen(self._current_pen)
            painter.setBrush(Qt.BrushStyle.NoBrush)
            painter.drawPath(path_outline.simplified())
        
    def initInfo(self):
        self.grInfo = QGraphicsProxyWidget(self)
        self.info.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.info.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.grInfo.setWidget(self.info)
        self.info.setGeometry(self.width - self._padding - 2, -2, self.title_height + 4, self.title_height + 4)  

    def initContent(self):
        self.grContent = QGraphicsProxyWidget(self)
        self.content.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.content.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.grContent.setWidget(self.content)
        self.content.setGeometry(self.edge_size, self.title_height + self.edge_size, self.width, 0)

    def initSummary(self):
        self.grSummary = QGraphicsProxyWidget(self)
        self.summary.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.summary.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.grSummary.setWidget(self.summary)
        self.summary.setGeometry(self.edge_size, self.title_height - self._padding, self.width, 0) 
    
    def checkHeight(self, spacing:float = 0):
        if self.node_height > 0 and self.node_height + spacing > self.height:
            return self.node_height + self.title_height + spacing
        else:
            return self.height + self.title_height
        
    def checkWidth(self, spacing:float = 0):
        if self.node_width > 0 and self.node_width + spacing > self.width:
            return self.node_width + spacing
        else:
            return self.width
