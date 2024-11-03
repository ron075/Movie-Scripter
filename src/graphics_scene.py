from __future__ import annotations

import math
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from sys import platform
from .node import *
from .sockets import *
from .edges import *
from .enum_classes import *
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .main_window import NodeEditor

class Scene():
    def __init__(self, session, parent:NodeEditor|None=None):
        self.session = session

        self.parent = parent
        self.nodes:list[Node] = []
        self.nodes_id:list[str] = []
        self.edges:list[Edge] = []

        self.scene_width = 64000
        self.scene_height = 64000

        self.initUI()

    def initUI(self):
        self.grScene = QDMGraphicsScene(self.session, self, self.parent)
        self.grScene.setGrScene(self.scene_width, self.scene_height)

    def assignID(self, node:Node) -> str:
        node_id = f"{node.nodeType.value}-{random.randint(0,50000)}"
        while node_id in self.nodes_id:
            node_id = f"{node.nodeType.value}-{random.randint(0,50000)}"
        return node_id
    
    def findNode(self, node_id:str) -> Node|None:
        if node_id in self.nodes_id:
            return self.nodes[self.nodes_id.index(node_id)]
        else:
            return None

    def replaceID(self, current_id:str, new_id:str):
        if current_id in self.nodes_id:
            self.nodes_id[self.nodes_id.index(current_id)] = new_id
    
    def findSceneCorners(self) -> list[float]:
        x1:float = 0.0
        y1:float = 0.0
        x2:float = 0.0
        y2:float = 0.0
        for node in self.nodes:      
            if x1 > node.pos.x() - 120:
                x1 = node.pos.x() - 120
            if y1 > node.pos.y() - 120:
                y1 = node.pos.y() - 120
            if x2 < node.pos.x() + (node.grNode.node_width if node.grNode.node_width > 0 else node.grNode.width) + 120:
                x2 = node.pos.x() + (node.grNode.node_width if node.grNode.node_width > 0 else node.grNode.width) + 120
            if y2 < node.pos.y() + (node.grNode.node_height + node.grNode.title_height if node.grNode.node_height > 0 else node.grNode.height) + 120:
                y2 = node.pos.y() + (node.grNode.node_height + node.grNode.title_height if node.grNode.node_height > 0 else node.grNode.height) + 120
            for picker in node.picker_inputs:
                if picker.edge.start_socket.node.grNode.isVisible():
                    if x1 > picker.edge.start_socket.node.pos.x() - 120:
                        x1 = picker.edge.start_socket.node.pos.x() - 120
                    if y1 > picker.edge.start_socket.node.pos.y() - 120:
                        y1 = picker.edge.start_socket.node.pos.y() - 120
                    if x2 < picker.edge.start_socket.node.pos.x() + (picker.edge.start_socket.node.grNode.node_width if picker.edge.start_socket.node.grNode.node_width > 0 else picker.edge.start_socket.node.grNode.width) + 120:
                        x2 = picker.edge.start_socket.node.pos.x() + (picker.edge.start_socket.node.grNode.node_width if picker.edge.start_socket.node.grNode.node_width > 0 else picker.edge.start_socket.node.grNode.width) + 120
                    if y2 < picker.edge.start_socket.node.pos.y() + (picker.edge.start_socket.node.grNode.node_height + picker.edge.start_socket.node.grNode.title_height if picker.edge.start_socket.node.grNode.node_height > 0 else picker.edge.start_socket.node.grNode.height) + 120:
                        y2 = picker.edge.start_socket.node.pos.y() + (picker.edge.start_socket.node.grNode.node_height + picker.edge.start_socket.node.grNode.title_height if picker.edge.start_socket.node.grNode.node_height > 0 else picker.edge.start_socket.node.grNode.height) + 120
        return [x1, y1, x2, y2]

    def changeStyle(self, style:Stylesheet):
        self.grScene._color_background = QColor(self.parent.styles._color_background[style.value])
        self.grScene._color_light = QColor(self.parent.styles._color_light[style.value])
        self.grScene._color_dark = QColor(self.parent.styles._color_dark[style.value])
        self.grScene.setBackgroundBrush(self.grScene._color_background)
        self.grScene._pen_light = QPen(self.grScene._color_light)
        self.grScene._pen_light.setWidth(1)
        self.grScene._pen_dark = QPen(self.grScene._color_dark)
        self.grScene._pen_dark.setWidth(3)
        for node in self.nodes:
            node.changeStyle(style)
        for edge in self.edges:
            edge.changeStyle(style)

    def addNode(self, node:Node):
        if NodeType(node.nodeType) != NodeType.Picker:
            self.nodes.append(node)
            self.nodes_id.append(node.nodeID)
        for obj in node.content.children():
            if type(obj) is QSwitchControl:
                self.parent.switches.append(obj)
        for obj in node.summary.children():
            if type(obj) is QSwitchControl:
                self.parent.switches.append(obj)

    def addEdge(self, edge:Edge):
        if not edge.temp:
            if NodeType(edge.start_socket.node.nodeType) != NodeType.Picker:
                self.edges.append(edge)

    def removeNode(self, node:Node):
        for obj in node.content.children():
            if type(obj) is QSwitchControl:
                self.parent.switches.remove(obj)
        for obj in node.summary.children():
            if type(obj) is QSwitchControl:
                self.parent.switches.remove(obj)
        self.nodes.remove(node)
        self.nodes_id.remove(node.nodeID)

    def removeEdge(self, edge:Edge):
        self.edges.remove(edge)

class QDMGraphicsScene(QGraphicsScene):
    def __init__(self, session, scene:Scene, parent=None):
        super().__init__(parent)
        
        self.session = session
        
        self.pa = parent
        self.scene = scene

        # settings

        self._color_background = QColor("#393939")
        self._color_light = QColor("#2f2f2f")
        self._color_dark = QColor("#292929")

        self._pen_light = QPen(self._color_light)
        self._pen_light.setWidth(1)
        self._pen_dark = QPen(self._color_dark)
        self._pen_dark.setWidth(3)

        self.setBackgroundBrush(self._color_background)

    def setGrScene(self, width:int, height:int):
        self.setSceneRect(-width // 2, -height // 2, width, height)

    def drawBackground(self, painter:QPainter, rect:QRectF):
        super().drawBackground(painter, rect)

        # here we create our grid
        left = int(math.floor(rect.left()))
        right = int(math.ceil(rect.right()))
        top = int(math.floor(rect.top()))
        bottom = int(math.ceil(rect.bottom()))

        first_left = left - (left % self.scene.parent.settings_menu.grid_size)
        first_top = top - (top % self.scene.parent.settings_menu.grid_size)

        # compute all lines to be drawn
        lines_light, lines_dark = [], []
        for x in range(first_left, right, self.scene.parent.settings_menu.grid_size):
            if (x % (self.scene.parent.settings_menu.grid_size*self.scene.parent.settings_menu.grid_squares) != 0): lines_light.append(QLine(x, top, x, bottom))
            else: lines_dark.append(QLine(x, top, x, bottom))

        for y in range(first_top, bottom, self.scene.parent.settings_menu.grid_size):
            if (y % (self.scene.parent.settings_menu.grid_size*self.scene.parent.settings_menu.grid_squares) != 0): lines_light.append(QLine(left, y, right, y))
            else: lines_dark.append(QLine(left, y, right, y))

        # draw the lines
        if lines_light:
            painter.setPen(self._pen_light)
            painter.drawLines(*lines_light)

        if lines_dark:
            painter.setPen(self._pen_dark)
            painter.drawLines(*lines_dark)
        
    def contextMenuEvent(self, event:QGraphicsSceneContextMenuEvent):
        item = self.scene.parent.view.itemAt(self.scene.parent.view.mapFromScene(event.scenePos()))
        self.scene.parent.view.last_lmb_click_scene_pos = self.scene.parent.view.mapFromScene(event.scenePos())
        if item is not None:
            if type(item) is QGraphicsTextItem or type(item) is QGraphicsProxyWidget:
                if type(item.parentItem()) is QDMGraphicsNode:
                    return
                elif type(item.parentItem()) is QDMGraphicsSocket:  
                    return
            elif type(item) is QDMGraphicsNode:
                return
            elif type(item) is QDMGraphicsSocket:  
                return
            elif type(item) is QDMGraphicsEdge:
                return
            
        # Creating a menu object with the central widget as parent
        menu = QMenu(self.pa)
        actionTitle = menu.addAction("Add a node")     
        changeEnabled(actionTitle, False) 
        if self.scene.parent.simple_mode:
            action1 = menu.addAction("Color Palette")
            action2 = menu.addAction("Transparency")
            action3 = menu.addAction("Turn")
            action4 = menu.addAction("Wait")
            action5 = menu.addAction("Delete")
            action6 = menu.addAction("Split")

            menu.setFixedWidth(menu.width() + 15)

            selected_action = menu.exec(event.screenPos())
            pos = event.scenePos()
            if selected_action == action1:
                self.AddNodeColorPalette(pos.x(), pos.y())
            elif selected_action == action2:
                self.AddNodeTransparency(pos.x(), pos.y())
            elif selected_action == action3:
                self.AddNodeTurn(pos.x(), pos.y())
            elif selected_action == action4:
                self.AddNodeWait(pos.x(), pos.y())
            elif selected_action == action5:
                self.AddNodeDelete(pos.x(), pos.y())
            elif selected_action == action6:
                self.AddNodeSplit(pos.x(), pos.y())
        else:
            menu_general = QMenu(menu)
            menu_general.setTitle("General")
            menu_Special = QMenu(menu)
            menu_Special.setTitle("Special")
            menu.addMenu(menu_general)
            menu.addMenu(menu_Special)

            # Populating the menu with actions
            actionG1 = menu_general.addAction("Color Palette")
            actionG2 = menu_general.addAction("Lighting")
            actionG3 = menu_general.addAction("Transparency")
            menu_Labels = QMenu(menu_general)
            menu_Labels.setTitle("Labels")
            menu_general.addMenu(menu_Labels)
            actionG4L1 = menu_Labels.addAction("2D Label")
            actionG4L2 = menu_Labels.addAction("3D Label")
            actionG5 = menu_general.addAction("Movement")
            menu_Rotation = QMenu(menu_general)
            menu_Rotation.setTitle("Rotation")
            menu_general.addMenu(menu_Rotation)
            actionG6R1 = menu_Rotation.addAction("Turn")
            actionG6R2 = menu_Rotation.addAction("Rock")
            actionG6R3 = menu_Rotation.addAction("Wobble")
            actionG7 = menu_general.addAction("Center of Rotation")
            actionG8 = menu_general.addAction("Center of Mass")
            actionG9 = menu_general.addAction("Wait")
            actionG10 = menu_general.addAction("Crossfade")
            actionG11 = menu_general.addAction("Load View")
            actionG12 = menu_general.addAction("Fly")
            actionS1 = menu_Special.addAction("Delete")
            actionS2 = menu_Special.addAction("Split")
            actionS3 = menu_Special.addAction("Save View")
        
            menu.setFixedWidth(menu.sizeHint().width())
            menu_general.setFixedWidth(menu_general.sizeHint().width() + 10)
            menu_Special.setFixedWidth(menu_Special.sizeHint().width() + 5)

            selected_action = menu.exec(event.screenPos())
            pos = event.scenePos()
            if selected_action == actionG1:
                self.AddNodeColorPalette(pos.x(), pos.y())
            elif selected_action == actionG2:
                self.AddNodeLighting(pos.x(), pos.y())
            elif selected_action == actionG3:
                self.AddNodeTransparency(pos.x(), pos.y())
            elif selected_action == actionG4L1:
                self.AddNode2DLabel(pos.x(), pos.y())
            elif selected_action == actionG4L2:
                self.AddNode3DLabel(pos.x(), pos.y())
            elif selected_action == actionG5:
                self.AddNodeMovement(pos.x(), pos.y())
            elif selected_action == actionG6R1:
                self.AddNodeTurn(pos.x(), pos.y())
            elif selected_action == actionG6R2:
                self.AddNodeRock(pos.x(), pos.y())
            elif selected_action == actionG6R3:
                self.AddNodeWobble(pos.x(), pos.y())
            elif selected_action == actionG7:
                self.AddNodeCenterRotation(pos.x(), pos.y())
            elif selected_action == actionG8:
                self.AddNodeCenterMass(pos.x(), pos.y())
            elif selected_action == actionG9:
                self.AddNodeWait(pos.x(), pos.y())
            elif selected_action == actionG10:
                self.AddNodeCrossfade(pos.x(), pos.y())
            elif selected_action == actionG11:
                self.AddNodeLoadView(pos.x(), pos.y())
            elif selected_action == actionG12:
                self.AddNodeFly(pos.x(), pos.y())
            elif selected_action == actionS1:
                self.AddNodeDelete(pos.x(), pos.y())
            elif selected_action == actionS2:
                self.AddNodeSplit(pos.x(), pos.y())
            elif selected_action == actionS3:
                self.AddNodeSaveView(pos.x(), pos.y())
        menu.deleteLater()

    def AddNodeColorPalette(self, x:float, y:float):
        node = Node(self.session, self.scene, NodeType.ColorPalette, color_input=True, parent=self.scene.parent, pos_x=x, pos_y=y)
    def AddNodeLighting(self, x:float, y:float):
        node = Node(self.session, self.scene, NodeType.Lighting, parent=self.scene.parent, pos_x=x, pos_y=y)
    def AddNodeTransparency(self, x:float, y:float):
        node = Node(self.session, self.scene, NodeType.Transparency, model_input=True, parent=self.scene.parent, pos_x=x, pos_y=y)
    def AddNode2DLabel(self, x:float, y:float):
        node = Node(self.session, self.scene, NodeType.Label2D, parent=self.scene.parent, pos_x=x, pos_y=y)
    def AddNode3DLabel(self, x:float, y:float):
        node = Node(self.session, self.scene, NodeType.Label3D, model_input=True, parent=self.scene.parent, pos_x=x, pos_y=y)
    def AddNodeMovement(self, x:float, y:float):
        node = Node(self.session, self.scene, NodeType.Movement, model_input=True, parent=self.scene.parent, pos_x=x, pos_y=y)
    def AddNodeTurn(self, x:float, y:float):
        node = Node(self.session, self.scene, NodeType.Turn, model_input=True, center_input=True, parent=self.scene.parent, pos_x=x, pos_y=y)
    def AddNodeRock(self, x:float, y:float):
        node = Node(self.session, self.scene, NodeType.Rock, model_input=True, center_input=True, parent=self.scene.parent, pos_x=x, pos_y=y)
    def AddNodeWobble(self, x:float, y:float):
        node = Node(self.session, self.scene, NodeType.Wobble, model_input=True, center_input=True, parent=self.scene.parent, pos_x=x, pos_y=y)
    def AddNodeCenterRotation(self, x:float, y:float):
        node = Node(self.session, self.scene, NodeType.CenterRotation, center_input=True, parent=self.scene.parent, pos_x=x, pos_y=y)
    def AddNodeCenterMass(self, x:float, y:float):
        node = Node(self.session, self.scene, NodeType.CenterMass, model_input=True, parent=self.scene.parent, pos_x=x, pos_y=y)
    def AddNodeDelete(self, x:float, y:float):
        node = Node(self.session, self.scene, NodeType.Delete, has_input=False, has_output=False, delete_input=True, parent=self.scene.parent, pos_x=x, pos_y=y)
        pos = node.pos
        node.input_delete.setSelfPos(pos.x(), pos.y(), node.inputs_counter)
    def AddNodeWait(self, x:float, y:float):
        node = Node(self.session, self.scene, NodeType.Wait, parent=self.scene.parent, pos_x=x, pos_y=y)
    def AddNodeCrossfade(self, x:float, y:float):
        node = Node(self.session, self.scene, NodeType.Crossfade, parent=self.scene.parent, pos_x=x, pos_y=y)
    def AddNodeSaveView(self, x:float, y:float):
        node = Node(self.session, self.scene, NodeType.View_Save, has_input=False, has_output=False, parent=self.scene.parent, pos_x=x, pos_y=y)
    def AddNodeLoadView(self, x:float, y:float):
        node = Node(self.session, self.scene, NodeType.View_Load, view_input=True, parent=self.scene.parent, pos_x=x, pos_y=y)
    def AddNodeFly(self, x:float, y:float):
        node = Node(self.session, self.scene, NodeType.Fly, fly_input=True, parent=self.scene.parent, pos_x=x, pos_y=y)
    def AddNodeSplit(self, x:float, y:float):
        node = Node(self.session, self.scene, NodeType.Split, has_input=False, has_output=False, model_input=True, parent=self.scene.parent, pos_x=x, pos_y=y)
        pos = node.pos
        node.input_model.setSelfPos(pos.x(), pos.y(), node.inputs_counter)

class QDMGraphicsView(QGraphicsView):
    def __init__(self, grScene:QDMGraphicsScene, parent:NodeEditor|None=None):
        super().__init__(parent)
        self.grScene = grScene
        self.viewParent = parent
        
        self.start_socket = None
        self.end_socket = None

        self.temp_edge = None
        self.draw_temp_edge = TempEdgeType.NONE
        self.arrow_size = 10
        self.arrow_offset = 8

        if platform == "darwin":
            self.platform_index = 1
        else: 
            self.platform_index = 0
        self.zoomInFactor = [1.25, 1.05]
        self.zoomClamp = False
        self.startZoomStep = [8, 20]
        self.zoom = self.startZoomStep[self.platform_index]
        self.zoomStep = 1
        self.zoomRange = [[0, 12], [0, 50]]
        self.zoomFactor = 1
        self.total_scale = 1
    
        self.initUI()
        
        self.setScene(self.grScene)

    def initUI(self):
        self.setRenderHints(QPainter.RenderHint.Antialiasing | QPainter.RenderHint.TextAntialiasing | QPainter.RenderHint.SmoothPixmapTransform)

        self.setViewportUpdateMode(QGraphicsView.ViewportUpdateMode.FullViewportUpdate)

        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.verticalScrollBar().installEventFilter(self)
        self.horizontalScrollBar().installEventFilter(self)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
         
        self.setTransformationAnchor(QGraphicsView.ViewportAnchor.AnchorUnderMouse)

    def eventFilter(self, object:QObject, event:QEvent) -> bool:
        if object == self.verticalScrollBar() and event.type() == QEvent.Type.Wheel:
            return True
        elif object == self.horizontalScrollBar() and event.type() == QEvent.Type.Wheel:
            return True
        return False

    def wheelEvent(self, event:QWheelEvent):
        item = self.itemAt(event.position().toPoint())
        if item is None:
            zoomOutFactor = 1 / self.zoomInFactor[self.platform_index]

            if event.angleDelta().y() > 0:
                self.zoom += self.zoomStep
                if self.zoom > self.zoomRange[self.platform_index][1]:
                    self.zoom = self.zoomRange[self.platform_index][1]
                else:
                    self.zoomFactor = self.zoomInFactor[self.platform_index]
                    self.scale(self.zoomFactor, self.zoomFactor)
                    self.total_scale = self.total_scale * self.zoomFactor
            elif event.angleDelta().y() < 0:  
                self.zoom -= self.zoomStep
                if self.zoom < self.zoomRange[self.platform_index][0]:
                    self.zoom = self.zoomRange[self.platform_index][0]
                else:
                    self.zoomFactor = zoomOutFactor
                    self.scale(self.zoomFactor, self.zoomFactor)
                    self.total_scale = self.total_scale * self.zoomFactor
        else:    
            super().wheelEvent(event)
                
    def mousePressEvent(self, event:QMouseEvent):
        if event.button() == Qt.MouseButton.LeftButton:
            if event.modifiers() == Qt.KeyboardModifier.ControlModifier:
                self.leftMouseButtonControlModifierPress(event)
            else:
                self.leftMouseButtonNoModifierPress(event)
        else:
            super().mousePressEvent(event)

    def mouseReleaseEvent(self, event:QMouseEvent):
        if event.button() == Qt.MouseButton.LeftButton:
            if event.modifiers() == Qt.KeyboardModifier.ControlModifier:
                pass
            else:
                self.leftMouseButtonNoModifierRelease(event)      

    def leftMouseButtonControlModifierPress(self, event:QMouseEvent):
        item = self.itemAt(event.pos())
        self.last_lmb_click_scene_pos = self.mapToScene(event.pos())
        if item is not None:
            if type(item) is QGraphicsTextItem or type(item) is QGraphicsProxyWidget:
                if type(item.parentItem()) is QDMGraphicsNode:
                    if item.parentItem().node.removable:
                        item.parentItem().node.summary.resetOutputValues()
                        self.removeNode(item.parentItem().node)
                elif type(item.parentItem()) is QDMGraphicsSocket:
                    if item.parentItem().socket.node.removable:
                        item.parentItem().socket.node.summary.resetOutputValues()
                        self.removeNode(item.parentItem().socket.node)        
            elif type(item) is QDMGraphicsNode:
                if item.node.removable:
                    item.node.summary.resetOutputValues()
                    self.removeNode(item.node)
            elif type(item) is QDMGraphicsSocket:                
                if item.socket.node.removable:
                    item.socket.node.summary.resetOutputValues()
                    self.removeNode(item.socket.node)
            elif type(item) is QDMGraphicsEdge:
                if item.edge.removable:
                    item.edge.start_socket.node.summary.resetOutputValues()
                    self.removeEdge(item.edge)
            else:
                pass

    def removeNode(self, node:Node):
        node.is_deleting = True
        if node.node_input is not None:
            if node.node_input.hasEdge():
                node.node_input.edge.is_deleting = True
                self.grScene.removeItem(node.node_input.edge.grEdge)
                self.grScene.removeItem(node.node_input.grSocket)
                self.grScene.scene.removeEdge(node.node_input.edge)
                node.node_input.edge.start_socket.edge = None
                del node.node_input.edge
                del node.node_input
        if node.node_output is not None:
            if node.node_output.hasEdge():
                node.node_output.edge.is_deleting = True
                self.grScene.removeItem(node.node_output.edge.grEdge)
                self.grScene.removeItem(node.node_output.grSocket)
                self.grScene.scene.removeEdge(node.node_output.edge)
                node.node_output.edge.end_socket.node.summary.chain_model = []
                node.node_output.edge.end_socket.node.summary.chain_color_groups = []
                node.node_output.edge.end_socket.node.summary.chain_center = []
                node.node_output.edge.end_socket.node.summary.chain_view = []
                node.node_output.edge.end_socket.node.summary.chain_fly_groups = []
                node.node_output.edge.end_socket.node.content.updateRun()
                node.node_output.edge.end_socket.edge = None
                del node.node_output.edge
                del node.node_output

        if node.input_model is not None:
            node.input_model.is_deleting = True
            self.grScene.removeItem(node.input_model.grNode)
            self.grScene.removeItem(node.input_model_edge.grEdge)
            del node.input_model
            del node.input_model_edge
        if node.input_color is not None:
            node.input_color.is_deleting = True
            self.grScene.removeItem(node.input_color.grNode)
            self.grScene.removeItem(node.input_color_edge.grEdge)
            del node.input_color
            del node.input_color_edge
        if node.input_center is not None:
            node.input_center.is_deleting = True
            self.grScene.removeItem(node.input_center.grNode)
            self.grScene.removeItem(node.input_center_edge.grEdge)
            del node.input_center
            del node.input_center_edge
        if node.input_view is not None:
            node.input_view.is_deleting = True
            self.grScene.removeItem(node.input_view.grNode)
            self.grScene.removeItem(node.input_view_edge.grEdge)
            del node.input_view
            del node.input_view_edge
        if node.input_fly is not None:
            node.input_fly.is_deleting = True
            self.grScene.removeItem(node.input_fly.grNode)
            self.grScene.removeItem(node.input_fly_edge.grEdge)
            del node.input_fly
            del node.input_fly_edge
        if node.input_delete is not None:
            node.input_delete.is_deleting = True
            self.grScene.removeItem(node.input_delete.grNode)
            self.grScene.removeItem(node.input_delete_edge.grEdge)
            del node.input_delete
            del node.input_delete_edge

        self.grScene.removeItem(node.grNode)
        self.grScene.scene.removeNode(node)

        del node.picker_inputs[:]
        
        del node

    def removeEdge(self, edge:Edge):
        edge.is_deleting = True
        self.grScene.removeItem(edge.grEdge)
        self.grScene.scene.removeEdge(edge)
        edge.end_socket.node.summary.chain_model = []
        edge.end_socket.node.summary.chain_color_groups = []
        edge.end_socket.node.summary.chain_center = []
        edge.end_socket.node.summary.chain_view = []
        edge.end_socket.node.summary.chain_fly_groups = []
        edge.end_socket.node.summary.updateOutputValues()
        edge.end_socket.node.content.updateRun()
        edge.start_socket.edge = None
        edge.end_socket.edge = None
        del edge

    def leftMouseButtonNoModifierPress(self, event:QMouseEvent):
        item = self.itemAt(event.pos())
        self.last_lmb_click_scene_pos = self.mapToScene(event.pos())
        if item is None:
            self.setDragMode(QGraphicsView.DragMode.ScrollHandDrag)
        elif type(item) is QDMGraphicsSocket:
            self.start_socket = None
            self.end_socket = None
            if item.socket.edge is None:
                if SocketType(item.socket.socket_type) == SocketType.OUTPUT_SOCKET:
                    self.start_socket = item
                    self.draw_temp_edge = TempEdgeType.SOURCE
                    self.temp_edge = Edge(scene=self.viewParent.scene, start_socket=self.start_socket.socket, end_socket=None, removable=True, temp=True, mousePos=self.mapToScene(event.pos()))
                elif SocketType(item.socket.socket_type)  == SocketType.INPUT_SOCKET:
                    self.end_socket = item
                    self.draw_temp_edge = TempEdgeType.DESTINATION                        
                    self.temp_edge = Edge(scene=self.viewParent.scene, start_socket=None, end_socket=self.end_socket.socket, removable=True, temp=True, mousePos=self.mapToScene(event.pos()))
        elif type(item) is QGraphicsProxyWidget:
            if hasattr(item, "node"):
                if NodeType(item.parentItem().node.nodeType) == NodeType.Picker:
                    item.parentItem().setSelected(True)
        super().mousePressEvent(event)

    def leftMouseButtonNoModifierRelease(self, event:QMouseEvent):
        item = self.itemAt(event.pos())
        self.last_lmb_click_scene_pos = self.mapToScene(event.pos())
        if self.draw_temp_edge in (TempEdgeType.SOURCE, TempEdgeType.DESTINATION):
            self.grScene.removeItem(self.temp_edge.grEdge)
            self.draw_temp_edge = TempEdgeType.NONE
            self.temp_edge = None
            self.scene().update()
            self.update()

        self.setDragMode(QGraphicsView.DragMode.NoDrag) 

        if item is not None:
            if type(item) is QGraphicsTextItem or type(item) is QGraphicsProxyWidget:
                if type(item.parentItem()) is QDMGraphicsNode:
                    item.parentItem().node.setPos(item.parentItem().node.pos.x(), item.parentItem().node.pos.y())  
            elif type(item) is QDMGraphicsNode:                    
                item.node.setPos(item.node.pos.x(), item.node.pos.y())  
            elif type(item) is QDMGraphicsSocket:
                if item.socket.edge is None:
                    if SocketType(item.socket.socket_type) == SocketType.OUTPUT_SOCKET and self.end_socket is not None:
                        self.start_socket = item
                        if self.end_socket.socket.node != self.start_socket.socket.node:
                            if not self.checkLoop(self.start_socket.socket, self.end_socket.socket):
                                Edge(self.viewParent.scene, self.start_socket.socket, self.end_socket.socket)
                                self.start_socket.socket.node.summary.updateOutputValues()
                    elif SocketType(item.socket.socket_type) == SocketType.INPUT_SOCKET and self.start_socket is not None:
                        self.end_socket = item
                        if self.end_socket.socket.node != self.start_socket.socket.node:
                            if not self.checkLoop(self.start_socket.socket, self.end_socket.socket):
                                Edge(self.viewParent.scene, self.start_socket.socket, self.end_socket.socket)  
                                self.start_socket.socket.node.summary.updateOutputValues()     
                            
        super().mouseReleaseEvent(event)

    def checkLoop(self, start_socket:Socket, current_socket:Socket) -> bool:
        if current_socket.node.node_output is not None:
            if current_socket.node.node_output is start_socket:
                return True
            else:
                if current_socket.node.node_output.hasEdge():
                    return self.checkLoop(start_socket, current_socket.node.node_output.edge.end_socket)
                else:
                    return False
        return False
    
    def mouseMoveEvent(self, event:QMouseEvent):
        if self.draw_temp_edge in (TempEdgeType.SOURCE, TempEdgeType.DESTINATION) and self.temp_edge is not None:
            mousePos = self.mapToScene(event.pos())
            self.temp_edge.updateTempPositions(mousePos)
            
        super().mouseMoveEvent(event)