from __future__ import annotations

from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from sys import platform
from .edges import *
from .enum_classes import *
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .node import Node
    from .stylesheets import Stylesheet

class Socket():
    def __init__(self, node:Node, index:int=0, position:Position=Position.LEFT_TOP, socket_type:SocketType=SocketType.INPUT_SOCKET, parent=None):

        self.parent = parent

        self.node = node
        self.index = index
        self.position = position    
        self.socket_type = socket_type
        self.grSocket = QDMGraphicsSocket(self)

        self.grSocket.setPos(*self.node.getSocketPosition(index, position))

        self.edge:Edge|None = None
        
    def changeStyle(self, style:Stylesheet):
        self.grSocket._pen.setColor(QColor(self.node.scene.parent.styles._socket_pen[style.value]))
        self.grSocket._pen_disabled.setColor(QColor(self.node.scene.parent.styles._socket_pen_disabled[style.value]))

    def getSocketPosition(self):
        return self.node.getSocketPosition(self.index, self.position)

    def setConnectedEdge(self, edge:Edge|None=None):
        self.edge = edge    
        
    def hasEdge(self):
        return self.edge is not None


class QDMGraphicsSocket(QGraphicsItem):
    def __init__(self, socket:Socket):
        super().__init__(socket.node.grNode)
        self.socket = socket
        self.style_changed = False
        
        self.radius = 6
        self.outline_width = 2

        self._pen = QPen(QColor("#FF000000"))
        self._pen_disabled = QPen(QColor("#FF000000"))
        self._pen_selected = QPen(QColor("#FF5656FF"))
        self._pen_input = QPen(QColor("#FFFF3333"))
        self._pen_output = QPen(QColor("#FF00CC77"))

        self._color_background_disabled = QColor("#FF555555")
        self._color_background_input = QColor("#FFFF3333")
        self._color_background_output = QColor("#FF00CC77")

        if SocketType(self.socket.socket_type) == SocketType.MODEL_SOCKET:
            self._pen_picker = QPen(QColor("#FFEEEE88"))
            self._picker_background_color = QColor("#FFEEEE88")
        elif SocketType(self.socket.socket_type) == SocketType.COLOR_SOCKET:
            self._pen_picker = QPen(QColor("#FF80E5FF"))
            self._picker_background_color = QColor("#FF80E5FF")
        elif SocketType(self.socket.socket_type) == SocketType.CENTER_SOCKET:
            self._pen_picker = QPen(QColor("#FFE580FF"))
            self._picker_background_color = QColor("#FFE580FF")
        elif SocketType(self.socket.socket_type) == SocketType.VIEW_SOCKET:
            self._pen_picker = QPen(QColor("#FF6600BB"))
            self._picker_background_color = QColor("#FF6600BB")
        elif SocketType(self.socket.socket_type) == SocketType.FLY_SOCKET:
            self._pen_picker = QPen(QColor("#FFFFBB44"))
            self._picker_background_color = QColor("#FFFFBB44")
        elif SocketType(self.socket.socket_type) == SocketType.DELETE_SOCKET:
            self._pen_picker = QPen(QColor("#FFCCCCCC"))
            self._picker_background_color = QColor("#FFCCCCCC")

        self._brush_disabled = QBrush(self._color_background_disabled)
        self._brush_output = QBrush(self._color_background_output)
        self._brush_input = QBrush(self._color_background_input)
        
        self._pen.setWidth(self.outline_width)
        self._pen_disabled.setWidth(self.outline_width)
        self._pen_selected.setWidth(self.outline_width)
        self._pen_input.setWidth(self.outline_width)
        self._pen_output.setWidth(self.outline_width)

        if hasattr(self, "_pen_picker"):
            self._pen_picker.setWidth(self.outline_width)
            self._brush_picker = QBrush(self._picker_background_color)
            if NodeType(self.socket.node.nodeType) != NodeType.Picker and NodeType(self.socket.node.nodeType) != NodeType.Delete and NodeType(self.socket.node.nodeType) != NodeType.Split and not self.socket.node.scene.parent.simple_mode:
                self.socket.socket_type = SocketType.DISABLED_SOCKET
        
        self.initUI()     

    def initUI(self):
        #self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsSelectable)
        pass

    def paint(self, painter:QPainter, QStyleOptionGraphicsItem:QStyleOptionGraphicsItem, widget=None):
        if SocketType(self.socket.socket_type) == SocketType.DISABLED_SOCKET:
            painter.setBrush(self._brush_disabled)
        elif SocketType(self.socket.socket_type) == SocketType.INPUT_SOCKET:
            painter.setBrush(self._brush_input)
        elif SocketType(self.socket.socket_type) == SocketType.OUTPUT_SOCKET:
            painter.setBrush(self._brush_output)
        else:
            painter.setBrush(self._brush_picker)

        if self.socket.node.grNode.isSelected():
            if SocketType(self.socket.socket_type) == SocketType.DISABLED_SOCKET:
                pen = self._pen_disabled
            elif SocketType(self.socket.socket_type) == SocketType.INPUT_SOCKET:
                pen = self._pen_input
            elif SocketType(self.socket.socket_type) == SocketType.OUTPUT_SOCKET:
                pen = self._pen_output
            else:
                pen = self._pen_picker
        elif self.socket.hasEdge():
            if self.socket.edge.grEdge.isSelected():
                if NodeType(self.socket.edge.start_socket.node.nodeType) == NodeType.Picker:
                    pen = self._pen_picker
                else:
                    pen = self._pen_selected
            else:
                pen = self._pen
        else:
            pen = self._pen
                    
        painter.setPen(pen)
        painter.drawEllipse(-self.radius, -self.radius, 2 * self.radius, 2 * self.radius)

    def boundingRect(self):
        return QRectF(- self.radius - self.outline_width, - self.radius - self.outline_width, 2 * (self.radius + self.outline_width), 2 * (self.radius + self.outline_width),)
