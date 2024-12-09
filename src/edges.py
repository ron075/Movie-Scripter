from __future__ import annotations

from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from .enum_classes import *
from .stylesheets import *
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .sockets import Socket
    from .graphics_scene import Scene

class Edge():
    def __init__(self, scene:Scene, start_socket:Socket|None, end_socket:Socket|None, removable:bool=True, temp:bool=False, mousePos:list[int]=[0, 0]):
        self.scene = scene

        self.removable = removable
        self.is_deleting = False

        self.temp = temp
        self.mousePos = mousePos
        

        self.start_socket = start_socket
        self.end_socket = end_socket

        self.posSource:list[int] = []
        self.posDestination:list[int] = []

        if self.start_socket is not None:
            self.start_socket.edge = self if not self.temp else None
        if self.end_socket is not None:
            self.end_socket.edge = self if not self.temp else None

        self.grEdge = QDMGraphicsEdge(self)
        
        if hasattr(self.scene.parent, "theme_toggle"):  
            if self.scene.parent.theme_toggle.isChecked():
                self.changeStyle(Stylesheet.LIGHT)
            else:
                self.changeStyle(Stylesheet.DARK)

        if not self.temp:
            self.updatePositions()
        else:
            self.updateTempPositions(self.mousePos)
    
        if not self.temp:
            self.scene.addEdge(self)
        self.scene.grScene.addItem(self.grEdge)  

    def changeStyle(self, style:Stylesheet):
        self.grEdge._pen_default.setColor(QColor(self.scene.parent.styles._edge_pen_default[style.value]))

    def updatePositions(self):
        source_pos = self.start_socket.getSocketPosition()
        source_pos[0] += self.start_socket.node.grNode.pos().x() + self.start_socket.grSocket.radius + self.start_socket.grSocket._pen_output.width()
        source_pos[1] += self.start_socket.node.grNode.pos().y()
        self.grEdge.setSource(*source_pos)
        if self.end_socket is not None:
            end_pos = self.end_socket.getSocketPosition()
            end_pos[0] += self.end_socket.node.grNode.pos().x() - self.end_socket.grSocket.radius - self.end_socket.grSocket._pen_input.width()
            end_pos[1] += self.end_socket.node.grNode.pos().y()
            self.grEdge.setDestination(*end_pos)

    def updateTempPositions(self, mousePos:list[int]=[0, 0]):
        self.mousePos = mousePos
        if self.start_socket is not None:
            source_pos = self.start_socket.getSocketPosition()
            source_pos[0] += self.start_socket.node.grNode.pos().x() + self.start_socket.grSocket.radius + self.start_socket.grSocket._pen_output.width()
            source_pos[1] += self.start_socket.node.grNode.pos().y()
            end_pos = [0, 0]
            end_pos[0] = self.mousePos.x()
            end_pos[1] = self.mousePos.y()
            self.grEdge.setSource(*source_pos)
            self.grEdge.setDestination(*end_pos)
        elif self.end_socket is not None:
            source_pos = [0, 0]
            source_pos[0] = self.mousePos.x()
            source_pos[1] = self.mousePos.y()
            self.grEdge.setSource(*source_pos)
            end_pos = self.end_socket.getSocketPosition()
            end_pos[0] += self.end_socket.node.grNode.pos().x() - self.end_socket.grSocket.radius - self.end_socket.grSocket._pen_input.width()
            end_pos[1] += self.end_socket.node.grNode.pos().y()
            self.grEdge.setDestination(*end_pos)
        self.grEdge.update()

class QDMGraphicsEdge(QGraphicsPathItem):
    def __init__(self, edge:Edge, parent=None):
        super().__init__(parent)        
        self.edge = edge

        self._pen_default = QPen(QColor("#FFFFFFFF"))
        self._pen_selected = QPen(QColor("#FF5656FF"))
        self._pen_input = QPen(QColor("#FFFF3333"))
        self._pen_output = QPen(QColor("#FF00CC77"))
        self._pen_default.setWidth(3)
        self._pen_selected.setWidth(3)
        self._pen_input.setWidth(3)
        self._pen_output.setWidth(3)

        if self.edge.start_socket is not None:
            if NodeType(self.edge.start_socket.node.nodeType) == NodeType.Picker:
                if NodePickerType(self.edge.start_socket.node.nodePickerType) == NodePickerType.ModelPicker:
                    self._pen_picker = QPen(QColor("#FFEEEE88"))
                elif NodePickerType(self.edge.start_socket.node.nodePickerType) == NodePickerType.ColorPicker:
                    self._pen_picker = QPen(QColor("#FF80E5FF"))
                elif NodePickerType(self.edge.start_socket.node.nodePickerType) == NodePickerType.CenterPicker:
                    self._pen_picker = QPen(QColor("#FFE580FF"))
                elif NodePickerType(self.edge.start_socket.node.nodePickerType) == NodePickerType.ViewPicker:
                    self._pen_picker = QPen(QColor("#FF6600BB"))
                elif NodePickerType(self.edge.start_socket.node.nodePickerType) == NodePickerType.FlyPicker:
                    self._pen_picker = QPen(QColor("#FFFFBB44"))
                elif NodePickerType(self.edge.start_socket.node.nodePickerType) == NodePickerType.DeletePicker:
                    self._pen_picker = QPen(QColor("#FFCCCCCC"))
                #elif NodePickerType(self.edge.start_socket.node.nodePickerType) == NodePickerType.SplitPicker:
                    #self._pen_picker = QPen(QColor("#FF6655FF"))
                self._pen_picker.setWidth(3)

        self.posSource = [0, 0]
        self.posDestination = [200, 100]

        self.arrow_size = 10

        self.setZValue(0)

        self.initUI()

    def setSource(self, x:int, y:int):
        self.posSource = [x, y]

    def setDestination(self, x:int, y:int):
        self.posDestination = [x, y]

    def initUI(self):
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsSelectable)
        self.setOpacity(self.edge.scene.parent.settings_menu.node_transparency / 100)

    def boundingRect(self) -> QRectF:  
        return QRectF(self.posSource[0], self.posSource[1], self.posDestination[0] - self.posSource[0], self.posDestination[1] - self.posSource[1]).normalized()

    def paint(self, painter:QPainter, QStyleOptionGraphicsItem:QStyleOptionGraphicsItem, widget=None):
        if not self.edge.is_deleting:
            if self.edge.start_socket is not None and self.edge.end_socket is not None:
                if NodeType(self.edge.start_socket.node.nodeType) == NodeType.Picker:
                    pen = self._pen_picker
                    if self.edge.start_socket.node.grNode.isSelected() or self.edge.end_socket.node.grNode.isSelected() or self.isSelected():
                        self.setZValue(60)
                    else:
                        self.setZValue(0)
                elif self.isSelected():
                    pen = self._pen_selected
                    self.setZValue(60)
                else:
                    if self.edge.start_socket.node.grNode.isSelected():
                        pen = self._pen_output
                        self.setZValue(60)
                    elif self.edge.end_socket.node.grNode.isSelected():
                        pen = self._pen_input
                        self.setZValue(60)
                    else:
                        pen = self._pen_default
                        self.setZValue(0)
            else:
                pen = self._pen_default
                self.setZValue(0)
            painter.setPen(pen)
            painter.setBrush(Qt.BrushStyle.NoBrush)

            self.setPath(self.update_path())
            painter.drawPath(self.path())
                
    def update_path(self) -> QPainterPath:
        s = self.posSource
        d = self.posDestination
        distX = 100
        distY = 0
        path = QPainterPath(QPointF(s[0], s[1]))
        path.cubicTo(s[0] + distX, s[1] + distY, d[0] - distX, d[1] - distY, d[0], d[1])
        arrow_up = QPainterPath(QPointF(d[0] - self.arrow_size, d[1] - self.arrow_size))
        arrow_up.lineTo(d[0], d[1])
        path.addPath(arrow_up)
        arrow_down = QPainterPath(QPointF(d[0] - self.arrow_size, d[1] + self.arrow_size))
        arrow_down.lineTo(d[0], d[1])
        path.addPath(arrow_down)
        return path
    