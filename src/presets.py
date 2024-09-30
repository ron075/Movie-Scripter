from __future__ import annotations

from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtGui import *
from sys import platform 
from .node import *    
from .edges import *    

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .main_window import NodeEditor
                
class Presets():
    def __init__(self, session, editor:NodeEditor):
        self.session = session
        self.editor = editor

    def prepare_presets(self):
        self.simple_prestes = {"Rotation Preset - Atoms":self.simple_rotation_preset_atoms,
                               "Rotation Preset - Cartoons":self.simple_rotation_preset_cartoons,
                               "Rotation Preset - Surfaces":self.simple_rotation_preset_surfaces}
        self.expert_prestes = {"Rotation Preset - Atoms":self.rotation_preset_atoms,
                               "Rotation Preset - Cartoons":self.rotation_preset_cartoons,
                               "Rotation Preset - Surfaces":self.rotation_preset_surfaces}
        
        if self.editor.settings_menu.model_special_residues:
            self.simple_prestes["Rotation Preset - Special Atoms"] = self.simple_rotation_preset_cartoons_special_atoms
            self.expert_prestes["Rotation Preset - Special Atoms"] = self.rotation_preset_cartoons_special_atoms
        
    def simple_rotation_preset_atoms(self):
        posX = -300
        posY = -200
        self.editor.nodeStart.setPos(posX, posY)

        previousNode = self.editor.nodeStart

        posX += 300
        posY = -300

        node = Node(self.session, self.editor.scene, NodeType.ColorPalette, color_input=True)
        node.setPos(posX, posY)
        selected_color_groups = []
        if node.input_color.content.Molecule.ModelTree.model().rowCount() > 1:
            for i in range(node.input_color.content.Molecule.ModelTree.model().rowCount()):
                if node.input_color.content.Molecule.ModelTree.model().index(i, 0).data() != "All" and node.input_color.content.Molecule.ModelTree.model().index(i, 0).data() != "Special Residue":
                    model:QStandardItemModel = node.input_color.content.Molecule.ModelTree.model()
                    item = model.item(i, 0)
                    if item.rowCount() > 0:
                        for j in range(item.rowCount()):
                            if model.index(j, 0, model.index(i, 0)).data() != "Special Residue":
                                node.input_color.content.Molecule.ModelTree.selectionModel().select(model.index(j, 0, model.index(i, 0)), QItemSelectionModel.SelectionFlag.Select)
                                node.input_color.content.Molecule.AddGroup()
                    else:            
                        node.input_color.content.Molecule.ModelTree.selectionModel().select(model.index(i, 0), QItemSelectionModel.SelectionFlag.Select)
                        node.input_color.content.Molecule.AddGroup()
        else:
            node.input_color.content.Molecule.ModelTree.selectionModel().select(node.input_color.content.Molecule.ModelTree.model().index(0, 0), QItemSelectionModel.SelectionFlag.Select)
            node.input_color.content.Molecule.AddGroup()
        node.input_color.content.Molecule.select()        
        node.input_color.setSelfPos(posX, posY, node.inputs_counter)
        node.content.Color.setCurrentIndex(1)
        node.content.CustomColor.setCurrentIndex(2)
        selected_color_groups = node.summary.picker_color_groups

        Edge(self.editor.scene, previousNode.node_output, node.node_input)        
        previousNode = node

        node = Node(self.session, self.editor.scene, NodeType.Transparency, model_input=True)
        posY += 100
        node.setPos(posX, posY)
        node.input_model.content.Molecule.ModelTree.selectionModel().select(node.input_model.content.Molecule.ModelTree.model().index(0, 0), QItemSelectionModel.SelectionFlag.Select)
        node.input_model.content.Molecule.select()       
        node.input_model.setSelfPos(posX, posY, node.inputs_counter)
        node.content.Surfaces.setText("100")
        node.content.Cartoons.setText("100")
        node.content.Atoms.setText("100")

        Edge(self.editor.scene, previousNode.node_output, node.node_input)   
        previousNode = node
        
        posX += 300

        for index, value in enumerate(selected_color_groups):
            posY = -300
            node = Node(self.session, self.editor.scene, NodeType.Transparency, model_input=True)
            node.setPos(posX, posY)
            count = 0
            if node.input_model.content.Molecule.ModelTree.model().rowCount() > 1:
                for i in range(node.input_model.content.Molecule.ModelTree.model().rowCount()):
                    if node.input_model.content.Molecule.ModelTree.model().index(i, 0).data() != "All" and node.input_model.content.Molecule.ModelTree.model().index(i, 0).data() != "Special Residue":
                        model:QStandardItemModel = node.input_model.content.Molecule.ModelTree.model()
                        item = model.item(i, 0)
                        if item.rowCount() > 0:
                            for j in range(item.rowCount()):
                                if model.index(j, 0, model.index(i, 0)).data() != "Special Residue":
                                    node.input_model.content.Molecule.ModelTree.selectionModel().select(model.index(j, 0, model.index(i, 0)), QItemSelectionModel.SelectionFlag.Select)
                                    count += 1
                                if count >= index + 1:
                                    break
                        else:                                                
                            node.input_model.content.Molecule.ModelTree.selectionModel().select(model.index(i, 0), QItemSelectionModel.SelectionFlag.Select)
                            count += 1
                        if count >= index + 1:
                            break
                    if count >= index + 1:
                        break
            else:
                node.input_model.content.Molecule.ModelTree.selectionModel().select(node.input_model.content.Molecule.ModelTree.model().index(0, 0), QItemSelectionModel.SelectionFlag.Select)
                node.input_model.content.Molecule.select()
            node.input_model.content.Molecule.select()
            node.input_model.setSelfPos(posX, posY, node.inputs_counter)
            node.content.Surfaces.setText("100")
            node.content.Cartoons.setText("100")
            node.content.Atoms.setText("0")

            Edge(self.editor.scene, previousNode.node_output, node.node_input)        
            previousNode = node

            node = Node(self.session, self.editor.scene, NodeType.Rotation, model_input=True, center_input=True)
            posY += 350
            node.setPos(posX, posY)
            node.input_model.content.Molecule.ModelTree.selectionModel().select(node.input_model.content.Molecule.ModelTree.model().index(0, 0), QItemSelectionModel.SelectionFlag.Select)
            node.input_model.content.Molecule.select()
            node.input_center.content.Molecule.ModelTree.selectionModel().select(node.input_center.content.Molecule.ModelTree.model().index(0, 0), QItemSelectionModel.SelectionFlag.Select)
            node.input_center.content.Molecule.select()
            node.input_model.setSelfPos(posX, posY, node.inputs_counter)
            node.input_center.setSelfPos(posX, posY, node.inputs_counter)
            node.content.Axis.setCurrentIndex(1)
            node.content.Angle.setText("6")
            node.content.Frames.setText("60")

            Edge(self.editor.scene, previousNode.node_output, node.node_input)        
            previousNode = node

            node = Node(self.session, self.editor.scene, NodeType.Wait)
            posY += 120
            node.setPos(posX, posY)
            posX += 300

            Edge(self.editor.scene, previousNode.node_output, node.node_input)        
            previousNode = node

        self.editor.nodeEnd.setPos(posX, posY)

        Edge(self.editor.scene, previousNode.node_output, self.editor.nodeEnd.node_input)        

        chain_start:list[Node] = []
        for edge in self.editor.scene.edges:
            starting_node = edge.start_socket.node.nodeID
            if starting_node not in [e.end_socket.node.nodeID for e in self.editor.scene.edges]:
                chain_start.append(edge.start_socket.node)
        for n in chain_start:
            n.summary.updateOutputValues(check_update=False)

        corners = self.editor.scene.findSceneCorners()
        self.editor.centerOn(corners[0], corners[1], corners[2], corners[3])
        self.editor.scaleOn(corners[0], corners[1], corners[2], corners[3])

    def simple_rotation_preset_cartoons(self):
        posX = -300
        posY = -200
        self.editor.nodeStart.setPos(posX, posY)

        previousNode = self.editor.nodeStart

        posX += 300
        posY = -300

        node = Node(self.session, self.editor.scene, NodeType.ColorPalette, color_input=True)
        node.setPos(posX, posY)
        selected_color_groups = []
        if node.input_color.content.Molecule.ModelTree.model().rowCount() > 1:
            for i in range(node.input_color.content.Molecule.ModelTree.model().rowCount()):
                if  node.input_color.content.Molecule.ModelTree.model().index(i, 0).data() != "All" and node.input_color.content.Molecule.ModelTree.model().index(i, 0).data() != "Special Residue":
                    model:QStandardItemModel = node.input_color.content.Molecule.ModelTree.model()
                    item = model.item(i, 0)
                    if item.rowCount() > 0:
                        for j in range(item.rowCount()):
                            if model.index(j, 0, model.index(i, 0)).data() != "Special Residue":
                                node.input_color.content.Molecule.ModelTree.selectionModel().select(model.index(j, 0, model.index(i, 0)), QItemSelectionModel.SelectionFlag.Select)
                                node.input_color.content.Molecule.AddGroup()
                    else:            
                        node.input_color.content.Molecule.ModelTree.selectionModel().select(model.index(i, 0), QItemSelectionModel.SelectionFlag.Select)
                        node.input_color.content.Molecule.AddGroup()
        else:
            node.input_color.content.Molecule.ModelTree.selectionModel().select(node.input_color.content.Molecule.ModelTree.model().index(0, 0), QItemSelectionModel.SelectionFlag.Select)
            node.input_color.content.Molecule.AddGroup()
        node.input_color.content.Molecule.select()
        node.input_color.setSelfPos(posX, posY, node.inputs_counter)
        node.content.Color.setCurrentIndex(1)
        node.content.CustomColor.setCurrentIndex(2)
        selected_color_groups = node.summary.picker_color_groups

        Edge(self.editor.scene, previousNode.node_output, node.node_input)        
        previousNode = node

        node = Node(self.session, self.editor.scene, NodeType.Transparency, model_input=True)
        posY += 100
        node.setPos(posX, posY)
        node.input_model.content.Molecule.ModelTree.selectionModel().select(node.input_model.content.Molecule.ModelTree.model().index(0, 0), QItemSelectionModel.SelectionFlag.Select)
        node.input_model.content.Molecule.select()
        node.input_model.setSelfPos(posX, posY, node.inputs_counter)
        node.content.Surfaces.setText("100")
        node.content.Cartoons.setText("100")
        node.content.Atoms.setText("100")

        Edge(self.editor.scene, previousNode.node_output, node.node_input)   
        previousNode = node
        
        posX += 300

        for index, value in enumerate(selected_color_groups):
            posY = -300
            node = Node(self.session, self.editor.scene, NodeType.Transparency, model_input=True)
            node.setPos(posX, posY)
            count = 0
            if node.input_model.content.Molecule.ModelTree.model().rowCount() > 1:
                for i in range(node.input_model.content.Molecule.ModelTree.model().rowCount()):
                    if node.input_model.content.Molecule.ModelTree.model().index(i, 0).data() != "All" and node.input_model.content.Molecule.ModelTree.model().index(i, 0).data() != "Special Residue":
                        model:QStandardItemModel = node.input_model.content.Molecule.ModelTree.model()
                        item = model.item(i, 0)
                        if item.rowCount() > 0:
                            for j in range(item.rowCount()):
                                if model.index(j, 0, model.index(i, 0)).data() != "Special Residue":
                                    node.input_model.content.Molecule.ModelTree.selectionModel().select(model.index(j, 0, model.index(i, 0)), QItemSelectionModel.SelectionFlag.Select)
                                    count += 1
                                if count >= index + 1:
                                    break
                        else:                                                
                            node.input_model.content.Molecule.ModelTree.selectionModel().select(model.index(i, 0), QItemSelectionModel.SelectionFlag.Select)
                            count += 1
                        if count >= index + 1:
                            break
                    if count >= index + 1:
                        break
            else:
                node.input_model.content.Molecule.ModelTree.selectionModel().select(node.input_model.content.Molecule.ModelTree.model().index(0, 0), QItemSelectionModel.SelectionFlag.Select)
                node.input_model.content.Molecule.select()
            node.input_model.content.Molecule.select()
            node.input_model.setSelfPos(posX, posY, node.inputs_counter)
            node.content.Surfaces.setText("100")
            node.content.Cartoons.setText("0")
            node.content.Atoms.setText("100")

            Edge(self.editor.scene, previousNode.node_output, node.node_input)        
            previousNode = node

            node = Node(self.session, self.editor.scene, NodeType.Rotation, model_input=True, center_input=True)
            posY += 350
            node.setPos(posX, posY)
            node.input_model.content.Molecule.ModelTree.selectionModel().select(node.input_model.content.Molecule.ModelTree.model().index(0, 0), QItemSelectionModel.SelectionFlag.Select)
            node.input_model.content.Molecule.select()
            node.input_center.content.Molecule.ModelTree.selectionModel().select(node.input_center.content.Molecule.ModelTree.model().index(0, 0), QItemSelectionModel.SelectionFlag.Select)
            node.input_center.content.Molecule.select()
            node.input_model.setSelfPos(posX, posY, node.inputs_counter)
            node.input_center.setSelfPos(posX, posY, node.inputs_counter)
            node.content.Axis.setCurrentIndex(1)
            node.content.Angle.setText("6")
            node.content.Frames.setText("60")

            Edge(self.editor.scene, previousNode.node_output, node.node_input)        
            previousNode = node

            node = Node(self.session, self.editor.scene, NodeType.Wait)
            posY += 120
            node.setPos(posX, posY)
            posX += 300

            Edge(self.editor.scene, previousNode.node_output, node.node_input)        
            previousNode = node

        self.editor.nodeEnd.setPos(posX, posY)

        Edge(self.editor.scene, previousNode.node_output, self.editor.nodeEnd.node_input)        

        chain_start:list[Node] = []
        for edge in self.editor.scene.edges:
            starting_node = edge.start_socket.node.nodeID
            if starting_node not in [e.end_socket.node.nodeID for e in self.editor.scene.edges]:
                chain_start.append(edge.start_socket.node)
        for n in chain_start:
            n.summary.updateOutputValues(check_update=False)

        corners = self.editor.scene.findSceneCorners()
        self.editor.centerOn(corners[0], corners[1], corners[2], corners[3])
        self.editor.scaleOn(corners[0], corners[1], corners[2], corners[3])

    def simple_rotation_preset_surfaces(self):
        posX = -300
        posY = -200
        self.editor.nodeStart.setPos(posX, posY)

        previousNode = self.editor.nodeStart

        posX += 300
        posY = -300

        node = Node(self.session, self.editor.scene, NodeType.ColorPalette, color_input=True)
        node.setPos(posX, posY)
        selected_color_groups = []
        if node.input_color.content.Molecule.ModelTree.model().rowCount() > 1:
            for i in range(node.input_color.content.Molecule.ModelTree.model().rowCount()):
                if  node.input_color.content.Molecule.ModelTree.model().index(i, 0).data() != "All" and node.input_color.content.Molecule.ModelTree.model().index(i, 0).data() != "Special Residue":
                    model:QStandardItemModel = node.input_color.content.Molecule.ModelTree.model()
                    item = model.item(i, 0)
                    if item.rowCount() > 0:
                        for j in range(item.rowCount()):
                            if model.index(j, 0, model.index(i, 0)).data() != "Special Residue":
                                node.input_color.content.Molecule.ModelTree.selectionModel().select(model.index(j, 0, model.index(i, 0)), QItemSelectionModel.SelectionFlag.Select)
                                node.input_color.content.Molecule.AddGroup()
                    else:            
                        node.input_color.content.Molecule.ModelTree.selectionModel().select(model.index(i, 0), QItemSelectionModel.SelectionFlag.Select)
                        node.input_color.content.Molecule.AddGroup()
        else:
            node.input_color.content.Molecule.ModelTree.selectionModel().select(node.input_color.content.Molecule.ModelTree.model().index(0, 0), QItemSelectionModel.SelectionFlag.Select)
            node.input_color.content.Molecule.AddGroup()
        node.input_color.content.Molecule.select()
        node.input_color.setSelfPos(posX, posY, node.inputs_counter)
        node.content.Color.setCurrentIndex(1)
        node.content.CustomColor.setCurrentIndex(2)
        selected_color_groups = node.summary.picker_color_groups

        Edge(self.editor.scene, previousNode.node_output, node.node_input)        
        previousNode = node

        node = Node(self.session, self.editor.scene, NodeType.Transparency, model_input=True)
        posY += 100
        node.setPos(posX, posY)
        node.input_model.content.Molecule.ModelTree.selectionModel().select(node.input_model.content.Molecule.ModelTree.model().index(0, 0), QItemSelectionModel.SelectionFlag.Select)
        node.input_model.content.Molecule.select()
        node.input_model.setSelfPos(posX, posY, node.inputs_counter)
        node.content.Surfaces.setText("100")
        node.content.Cartoons.setText("100")
        node.content.Atoms.setText("100")

        Edge(self.editor.scene, previousNode.node_output, node.node_input)   
        previousNode = node
        
        posX += 300

        for index, value in enumerate(selected_color_groups):
            posY = -300
            node = Node(self.session, self.editor.scene, NodeType.Transparency, model_input=True)
            node.setPos(posX, posY)
            count = 0
            if node.input_model.content.Molecule.ModelTree.model().rowCount() > 1:
                for i in range(node.input_model.content.Molecule.ModelTree.model().rowCount()):
                    if node.input_model.content.Molecule.ModelTree.model().index(i, 0).data() != "All" and node.input_model.content.Molecule.ModelTree.model().index(i, 0).data() != "Special Residue":
                        model:QStandardItemModel = node.input_model.content.Molecule.ModelTree.model()
                        item = model.item(i, 0)
                        if item.rowCount() > 0:
                            for j in range(item.rowCount()):
                                if model.index(j, 0, model.index(i, 0)).data() != "Special Residue":
                                    node.input_model.content.Molecule.ModelTree.selectionModel().select(model.index(j, 0, model.index(i, 0)), QItemSelectionModel.SelectionFlag.Select)
                                    count += 1
                                if count >= index + 1:
                                    break
                        else:                                                
                            node.input_model.content.Molecule.ModelTree.selectionModel().select(model.index(i, 0), QItemSelectionModel.SelectionFlag.Select)
                            count += 1
                        if count >= index + 1:
                            break
                    if count >= index + 1:
                        break
            else:
                node.input_model.content.Molecule.ModelTree.selectionModel().select(node.input_model.content.Molecule.ModelTree.model().index(0, 0), QItemSelectionModel.SelectionFlag.Select)
                node.input_model.content.Molecule.select()
            node.input_model.content.Molecule.select()
            node.input_model.setSelfPos(posX, posY, node.inputs_counter)
            node.content.Surfaces.setText("0")
            node.content.Cartoons.setText("100")
            node.content.Atoms.setText("100")

            Edge(self.editor.scene, previousNode.node_output, node.node_input)        
            previousNode = node

            node = Node(self.session, self.editor.scene, NodeType.Rotation, model_input=True, center_input=True)
            posY += 350
            node.setPos(posX, posY)
            node.input_model.content.Molecule.ModelTree.selectionModel().select(node.input_model.content.Molecule.ModelTree.model().index(0, 0), QItemSelectionModel.SelectionFlag.Select)
            node.input_model.content.Molecule.select()
            node.input_center.content.Molecule.ModelTree.selectionModel().select(node.input_center.content.Molecule.ModelTree.model().index(0, 0), QItemSelectionModel.SelectionFlag.Select)
            node.input_center.content.Molecule.select()
            node.input_model.setSelfPos(posX, posY, node.inputs_counter)
            node.input_center.setSelfPos(posX, posY, node.inputs_counter)
            node.content.Axis.setCurrentIndex(1)
            node.content.Angle.setText("6")
            node.content.Frames.setText("60")

            Edge(self.editor.scene, previousNode.node_output, node.node_input)        
            previousNode = node

            node = Node(self.session, self.editor.scene, NodeType.Wait)
            posY += 120
            node.setPos(posX, posY)
            posX += 300

            Edge(self.editor.scene, previousNode.node_output, node.node_input)        
            previousNode = node

        self.editor.nodeEnd.setPos(posX, posY)

        Edge(self.editor.scene, previousNode.node_output, self.editor.nodeEnd.node_input)        

        chain_start:list[Node] = []
        for edge in self.editor.scene.edges:
            starting_node = edge.start_socket.node.nodeID
            if starting_node not in [e.end_socket.node.nodeID for e in self.editor.scene.edges]:
                chain_start.append(edge.start_socket.node)
        for n in chain_start:
            n.summary.updateOutputValues(check_update=False)

        corners = self.editor.scene.findSceneCorners()
        self.editor.centerOn(corners[0], corners[1], corners[2], corners[3])
        self.editor.scaleOn(corners[0], corners[1], corners[2], corners[3])

    def simple_rotation_preset_cartoons_special_atoms(self):
        posX = -300
        posY = -100
        self.editor.nodeStart.setPos(posX, posY)

        previousNode = self.editor.nodeStart

        posX += 300
        posY = -300

        node = Node(self.session, self.editor.scene, NodeType.ColorPalette, color_input=True)
        node.setPos(posX, posY)
        selected_color_groups = []
        if node.input_color.content.Molecule.ModelTree.model().rowCount() > 1:
            for i in range(node.input_color.content.Molecule.ModelTree.model().rowCount()):
                if  node.input_color.content.Molecule.ModelTree.model().index(i, 0).data() != "All" and node.input_color.content.Molecule.ModelTree.model().index(i, 0).data() != "Special Residue":
                    model:QStandardItemModel = node.input_color.content.Molecule.ModelTree.model()
                    item = model.item(i, 0)
                    if item.rowCount() > 0:
                        for j in range(item.rowCount()):
                            if model.index(j, 0, model.index(i, 0)).data() != "Special Residue":
                                node.input_color.content.Molecule.ModelTree.selectionModel().select(model.index(j, 0, model.index(i, 0)), QItemSelectionModel.SelectionFlag.Select)
                                node.input_color.content.Molecule.AddGroup()
                    else:            
                        node.input_color.content.Molecule.ModelTree.selectionModel().select(model.index(i, 0), QItemSelectionModel.SelectionFlag.Select)
                        node.input_color.content.Molecule.AddGroup()
        else:
            node.input_color.content.Molecule.ModelTree.selectionModel().select(node.input_color.content.Molecule.ModelTree.model().index(0, 0), QItemSelectionModel.SelectionFlag.Select)
            node.input_color.content.Molecule.AddGroup()
        node.input_color.content.Molecule.select()
        node.input_color.setSelfPos(posX, posY, node.inputs_counter)
        node.content.Color.setCurrentIndex(1)
        node.content.CustomColor.setCurrentIndex(2)
        selected_color_groups = node.summary.picker_color_groups

        Edge(self.editor.scene, previousNode.node_output, node.node_input)        
        previousNode = node

        node = Node(self.session, self.editor.scene, NodeType.ColorPalette, color_input=True)
        posY += 200
        node.setPos(posX, posY)
        if node.input_color.content.Molecule.ModelTree.model().rowCount() > 1:
            for i in range(node.input_color.content.Molecule.ModelTree.model().rowCount()):
                if  node.input_color.content.Molecule.ModelTree.model().index(i, 0).data() != "All" and node.input_color.content.Molecule.ModelTree.model().index(i, 0).data() != "Special Residue":
                    model:QStandardItemModel = node.input_color.content.Molecule.ModelTree.model()
                    item = model.item(i, 0)
                    if item.rowCount() > 0:
                        for j in range(item.rowCount()):
                            if model.index(j, 0, model.index(i, 0)).data() == "Special Residue":
                                node.input_color.content.Molecule.ModelTree.selectionModel().select(model.index(j, 0, model.index(i, 0)), QItemSelectionModel.SelectionFlag.Select)
                                node.input_color.content.Molecule.AddGroup()
        node.input_color.content.Molecule.select()
        node.input_color.setSelfPos(posX, posY, node.inputs_counter)
        node.content.Color.setCurrentIndex(0)

        Edge(self.editor.scene, previousNode.node_output, node.node_input)        
        previousNode = node

        node = Node(self.session, self.editor.scene, NodeType.Transparency, model_input=True)
        posY += 100
        node.setPos(posX, posY)
        node.input_model.content.Molecule.ModelTree.selectionModel().select(node.input_model.content.Molecule.ModelTree.model().index(0, 0), QItemSelectionModel.SelectionFlag.Select)
        node.input_model.content.Molecule.select()
        node.input_model.setSelfPos(posX, posY, node.inputs_counter)
        node.content.Surfaces.setText("100")
        node.content.Cartoons.setText("100")
        node.content.Atoms.setText("100")

        Edge(self.editor.scene, previousNode.node_output, node.node_input)   
        previousNode = node
        
        posX += 300

        for index, value in enumerate(selected_color_groups):
            posY = -300
            node = Node(self.session, self.editor.scene, NodeType.Transparency, model_input=True)
            node.setPos(posX, posY)
            count = 0
            if node.input_model.content.Molecule.ModelTree.model().rowCount() > 1:
                for i in range(node.input_model.content.Molecule.ModelTree.model().rowCount()):
                    if node.input_model.content.Molecule.ModelTree.model().index(i, 0).data() != "All" and node.input_model.content.Molecule.ModelTree.model().index(i, 0).data() != "Special Residue":
                        model:QStandardItemModel = node.input_model.content.Molecule.ModelTree.model()
                        item = model.item(i, 0)
                        if item.rowCount() > 0:
                            for j in range(item.rowCount()):
                                if model.index(j, 0, model.index(i, 0)).data() != "Special Residue":
                                    node.input_model.content.Molecule.ModelTree.selectionModel().select(model.index(j, 0, model.index(i, 0)), QItemSelectionModel.SelectionFlag.Select)
                                    count += 1
                                if count >= index + 1:
                                    break
                        else:                                                
                            node.input_model.content.Molecule.ModelTree.selectionModel().select(model.index(i, 0), QItemSelectionModel.SelectionFlag.Select)
                            count += 1
                        if count >= index + 1:
                            break
                    if count >= index + 1:
                        break
            else:
                node.input_model.content.Molecule.ModelTree.selectionModel().select(node.input_model.content.Molecule.ModelTree.model().index(0, 0), QItemSelectionModel.SelectionFlag.Select)
                node.input_model.content.Molecule.select()
            node.input_model.content.Molecule.select()
            node.input_model.setSelfPos(posX, posY, node.inputs_counter)
            node.content.Surfaces.setText("100")
            node.content.Cartoons.setText("0")
            node.content.Atoms.setText("100")

            Edge(self.editor.scene, previousNode.node_output, node.node_input)        
            previousNode = node

            posY += 200
            node = Node(self.session, self.editor.scene, NodeType.Transparency, model_input=True)
            node.setPos(posX, posY)
            count = 0
            if node.input_model.content.Molecule.ModelTree.model().rowCount() > 1:
                for i in range(node.input_model.content.Molecule.ModelTree.model().rowCount()):
                    if node.input_model.content.Molecule.ModelTree.model().index(i, 0).data() != "All" and node.input_model.content.Molecule.ModelTree.model().index(i, 0).data() != "Special Residue":
                        model:QStandardItemModel = node.input_model.content.Molecule.ModelTree.model()
                        item = model.item(i, 0)
                        if item.rowCount() > 0:
                            for j in range(item.rowCount()):
                                if model.index(j, 0, model.index(i, 0)).data() != "Special Residue":
                                    if model.index(0, 0, model.index(j, 0, model.index(i, 0))).data() == "Special Residue":
                                        node.input_model.content.Molecule.ModelTree.selectionModel().select(model.index(0, 0, model.index(j, 0, model.index(i, 0))), QItemSelectionModel.SelectionFlag.Select)
                                    count += 1
                                    if count >= index + 1:
                                        break
                    if count >= index + 1:
                        break
            node.input_model.content.Molecule.select()
            node.input_model.setSelfPos(posX, posY, node.inputs_counter)
            node.content.Surfaces.setText("100")
            node.content.Cartoons.setText("100")
            node.content.Atoms.setText("0")
            node.content.AtomsStyle.setCurrentIndex(1)

            Edge(self.editor.scene, previousNode.node_output, node.node_input)        
            previousNode = node

            node = Node(self.session, self.editor.scene, NodeType.Rotation, model_input=True, center_input=True)
            posY += 350
            node.setPos(posX, posY)
            node.input_model.content.Molecule.ModelTree.selectionModel().select(node.input_model.content.Molecule.ModelTree.model().index(0, 0), QItemSelectionModel.SelectionFlag.Select)
            node.input_model.content.Molecule.select()
            node.input_center.content.Molecule.ModelTree.selectionModel().select(node.input_center.content.Molecule.ModelTree.model().index(0, 0), QItemSelectionModel.SelectionFlag.Select)
            node.input_center.content.Molecule.select()
            node.input_model.setSelfPos(posX, posY, node.inputs_counter)
            node.input_center.setSelfPos(posX, posY, node.inputs_counter)
            node.content.Axis.setCurrentIndex(1)
            node.content.Angle.setText("6")
            node.content.Frames.setText("60")

            Edge(self.editor.scene, previousNode.node_output, node.node_input)        
            previousNode = node

            node = Node(self.session, self.editor.scene, NodeType.Wait)
            posY += 120
            node.setPos(posX, posY)
            posX += 300

            Edge(self.editor.scene, previousNode.node_output, node.node_input)        
            previousNode = node

        self.editor.nodeEnd.setPos(posX, posY)

        Edge(self.editor.scene, previousNode.node_output, self.editor.nodeEnd.node_input)        

        chain_start:list[Node] = []
        for edge in self.editor.scene.edges:
            starting_node = edge.start_socket.node.nodeID
            if starting_node not in [e.end_socket.node.nodeID for e in self.editor.scene.edges]:
                chain_start.append(edge.start_socket.node)
        for n in chain_start:
            n.summary.updateOutputValues(check_update=False)

        corners = self.editor.scene.findSceneCorners()
        self.editor.centerOn(corners[0], corners[1], corners[2], corners[3])
        self.editor.scaleOn(corners[0], corners[1], corners[2], corners[3])

    def rotation_preset_atoms(self):
        posX = -300
        posY = -200
        self.editor.nodeStart.setPos(posX, posY)

        previousNode = self.editor.nodeStart

        posX += 300
        posY = -300

        node = Node(self.session, self.editor.scene, NodeType.ColorPalette, color_input=True)
        node.setPos(posX, posY)
        selected_color_groups = []
        if node.input_color.content.Molecule.ModelTree.model().rowCount() > 1:
            for i in range(node.input_color.content.Molecule.ModelTree.model().rowCount()):
                if  node.input_color.content.Molecule.ModelTree.model().index(i, 0).data() != "All" and node.input_color.content.Molecule.ModelTree.model().index(i, 0).data() != "Special Residue":
                    model:QStandardItemModel = node.input_color.content.Molecule.ModelTree.model()
                    item = model.item(i, 0)
                    if item.rowCount() > 0:
                        for j in range(item.rowCount()):
                            if model.index(j, 0, model.index(i, 0)).data() != "Special Residue":
                                node.input_color.content.Molecule.ModelTree.selectionModel().select(model.index(j, 0, model.index(i, 0)), QItemSelectionModel.SelectionFlag.Select)
                                node.input_color.content.Molecule.AddGroup()
                    else:            
                        node.input_color.content.Molecule.ModelTree.selectionModel().select(model.index(i, 0), QItemSelectionModel.SelectionFlag.Select)
                        node.input_color.content.Molecule.AddGroup()
        else:
            node.input_color.content.Molecule.ModelTree.selectionModel().select(node.input_color.content.Molecule.ModelTree.model().index(0, 0), QItemSelectionModel.SelectionFlag.Select)
            node.input_color.content.Molecule.AddGroup()
        node.input_color.content.Molecule.select()
        node.summary.ColorToggle.setChecked(True)
        node.content.Color.setCurrentIndex(8)
        node.content.CustomColor.setCurrentIndex(4)
        selected_color_groups = node.summary.picker_color_groups

        Edge(self.editor.scene, previousNode.node_output, node.node_input)        
        previousNode = node

        node = Node(self.session, self.editor.scene, NodeType.Transparency, model_input=True)
        posY += 200
        node.setPos(posX, posY)
        node.input_model.content.Molecule.ModelTree.selectionModel().select(node.input_model.content.Molecule.ModelTree.model().index(0, 0), QItemSelectionModel.SelectionFlag.Select)
        node.input_model.content.Molecule.select()
        node.content.Surfaces.setText("100")
        node.content.Cartoons.setText("100")
        node.content.Atoms.setText("100")
        node.summary.ModelToggle.setChecked(True)

        Edge(self.editor.scene, previousNode.node_output, node.node_input)   
        previousNode = node
        
        posX += 300

        for index, value in enumerate(selected_color_groups):
            posY = -300
            node = Node(self.session, self.editor.scene, NodeType.Crossfade,)
            node.setPos(posX, posY)
            node.content.Frames.setText("50")

            Edge(self.editor.scene, previousNode.node_output, node.node_input)        
            previousNode = node

            node = Node(self.session, self.editor.scene, NodeType.Transparency, model_input=True)
            posY += 200
            node.setPos(posX, posY)
            count = 0
            if node.input_model.content.Molecule.ModelTree.model().rowCount() > 1:
                for i in range(node.input_model.content.Molecule.ModelTree.model().rowCount()):
                    if node.input_model.content.Molecule.ModelTree.model().index(i, 0).data() != "All" and node.input_model.content.Molecule.ModelTree.model().index(i, 0).data() != "Special Residue":
                        model:QStandardItemModel = node.input_model.content.Molecule.ModelTree.model()
                        item = model.item(i, 0)
                        if item.rowCount() > 0:
                            for j in range(item.rowCount()):
                                if model.index(j, 0, model.index(i, 0)).data() != "Special Residue":
                                    node.input_model.content.Molecule.ModelTree.selectionModel().select(model.index(j, 0, model.index(i, 0)), QItemSelectionModel.SelectionFlag.Select)
                                    count += 1
                                if count >= index + 1:
                                    break
                        else:                                                
                            node.input_model.content.Molecule.ModelTree.selectionModel().select(model.index(i, 0), QItemSelectionModel.SelectionFlag.Select)
                            count += 1
                        if count >= index + 1:
                            break
                    if count >= index + 1:
                        break
            else:
                node.input_model.content.Molecule.ModelTree.selectionModel().select(node.input_model.content.Molecule.ModelTree.model().index(0, 0), QItemSelectionModel.SelectionFlag.Select)
                node.input_model.content.Molecule.select()
            node.input_model.content.Molecule.select()
            node.content.Surfaces.setText("100")
            node.content.Cartoons.setText("100")
            node.content.Atoms.setText("0")
            node.summary.ModelToggle.setChecked(True)

            Edge(self.editor.scene, previousNode.node_output, node.node_input)        
            previousNode = node

            node = Node(self.session, self.editor.scene, NodeType.Wait)
            posY += 200
            node.setPos(posX, posY)

            Edge(self.editor.scene, previousNode.node_output, node.node_input)        
            previousNode = node

            node = Node(self.session, self.editor.scene, NodeType.Rotation, model_input=True, center_input=True)
            posY += 200
            node.setPos(posX, posY)
            node.summary.ModelToggle.setChecked(False)
            if index == 0:
                node.input_center.content.Molecule.ModelTree.selectionModel().select(node.input_center.content.Molecule.ModelTree.model().index(0, 0), QItemSelectionModel.SelectionFlag.Select)
                node.input_center.content.Molecule.select()
                node.summary.CenterToggle.setChecked(True)
            else:
                node.summary.CenterToggle.setChecked(False)
            node.content.Axis.setCurrentIndex(1)
            node.content.Angle.setText("6")
            node.content.Frames.setText("60")

            Edge(self.editor.scene, previousNode.node_output, node.node_input)        
            previousNode = node

            node = Node(self.session, self.editor.scene, NodeType.Wait)
            posY += 200
            node.setPos(posX, posY)
            posX += 300

            Edge(self.editor.scene, previousNode.node_output, node.node_input)        
            previousNode = node

        self.editor.nodeEnd.setPos(posX, posY)

        Edge(self.editor.scene, previousNode.node_output, self.editor.nodeEnd.node_input)        

        chain_start:list[Node] = []
        for edge in self.editor.scene.edges:
            starting_node = edge.start_socket.node.nodeID
            if starting_node not in [e.end_socket.node.nodeID for e in self.editor.scene.edges]:
                chain_start.append(edge.start_socket.node)
        for n in chain_start:
            n.summary.updateOutputValues(check_update=False)

        corners = self.editor.scene.findSceneCorners()
        self.editor.centerOn(corners[0], corners[1], corners[2], corners[3])
        self.editor.scaleOn(corners[0], corners[1], corners[2], corners[3])

    def rotation_preset_cartoons(self):
        posX = -300
        posY = -200
        self.editor.nodeStart.setPos(posX, posY)

        previousNode = self.editor.nodeStart

        posX += 300
        posY = -300

        node = Node(self.session, self.editor.scene, NodeType.ColorPalette, color_input=True)
        node.setPos(posX, posY)
        selected_color_groups = []
        if node.input_color.content.Molecule.ModelTree.model().rowCount() > 1:
            for i in range(node.input_color.content.Molecule.ModelTree.model().rowCount()):
                if  node.input_color.content.Molecule.ModelTree.model().index(i, 0).data() != "All" and node.input_color.content.Molecule.ModelTree.model().index(i, 0).data() != "Special Residue":
                    model:QStandardItemModel = node.input_color.content.Molecule.ModelTree.model()
                    item = model.item(i, 0)
                    if item.rowCount() > 0:
                        for j in range(item.rowCount()):
                            if model.index(j, 0, model.index(i, 0)).data() != "Special Residue":
                                node.input_color.content.Molecule.ModelTree.selectionModel().select(model.index(j, 0, model.index(i, 0)), QItemSelectionModel.SelectionFlag.Select)
                                node.input_color.content.Molecule.AddGroup()
                    else:            
                        node.input_color.content.Molecule.ModelTree.selectionModel().select(model.index(i, 0), QItemSelectionModel.SelectionFlag.Select)
                        node.input_color.content.Molecule.AddGroup()
        else:
            node.input_color.content.Molecule.ModelTree.selectionModel().select(node.input_color.content.Molecule.ModelTree.model().index(0, 0), QItemSelectionModel.SelectionFlag.Select)
            node.input_color.content.Molecule.AddGroup()
        node.input_color.content.Molecule.select()
        node.summary.ColorToggle.setChecked(True)
        node.content.Color.setCurrentIndex(8)
        node.content.CustomColor.setCurrentIndex(4)
        selected_color_groups = node.summary.picker_color_groups

        Edge(self.editor.scene, previousNode.node_output, node.node_input)        
        previousNode = node

        node = Node(self.session, self.editor.scene, NodeType.Transparency, model_input=True)
        posY += 200
        node.setPos(posX, posY)
        node.input_model.content.Molecule.ModelTree.selectionModel().select(node.input_model.content.Molecule.ModelTree.model().index(0, 0), QItemSelectionModel.SelectionFlag.Select)
        node.input_model.content.Molecule.select()
        node.content.Surfaces.setText("100")
        node.content.Cartoons.setText("100")
        node.content.Atoms.setText("100")
        node.summary.ModelToggle.setChecked(True)

        Edge(self.editor.scene, previousNode.node_output, node.node_input)   
        previousNode = node
        
        posX += 300

        for index, value in enumerate(selected_color_groups):
            posY = -300
            node = Node(self.session, self.editor.scene, NodeType.Crossfade,)
            node.setPos(posX, posY)
            node.content.Frames.setText("50")

            Edge(self.editor.scene, previousNode.node_output, node.node_input)        
            previousNode = node

            node = Node(self.session, self.editor.scene, NodeType.Transparency, model_input=True)
            posY += 200
            node.setPos(posX, posY)
            count = 0
            if node.input_model.content.Molecule.ModelTree.model().rowCount() > 1:
                for i in range(node.input_model.content.Molecule.ModelTree.model().rowCount()):
                    if node.input_model.content.Molecule.ModelTree.model().index(i, 0).data() != "All" and node.input_model.content.Molecule.ModelTree.model().index(i, 0).data() != "Special Residue":
                        model:QStandardItemModel = node.input_model.content.Molecule.ModelTree.model()
                        item = model.item(i, 0)
                        if item.rowCount() > 0:
                            for j in range(item.rowCount()):
                                if model.index(j, 0, model.index(i, 0)).data() != "Special Residue":
                                    node.input_model.content.Molecule.ModelTree.selectionModel().select(model.index(j, 0, model.index(i, 0)), QItemSelectionModel.SelectionFlag.Select)
                                    count += 1
                                if count >= index + 1:
                                    break
                        else:                                                
                            node.input_model.content.Molecule.ModelTree.selectionModel().select(model.index(i, 0), QItemSelectionModel.SelectionFlag.Select)
                            count += 1
                        if count >= index + 1:
                            break
                    if count >= index + 1:
                        break
            else:
                node.input_model.content.Molecule.ModelTree.selectionModel().select(node.input_model.content.Molecule.ModelTree.model().index(0, 0), QItemSelectionModel.SelectionFlag.Select)
                node.input_model.content.Molecule.select()
            node.input_model.content.Molecule.select()
            node.content.Surfaces.setText("100")
            node.content.Cartoons.setText("0")
            node.content.Atoms.setText("100")
            node.summary.ModelToggle.setChecked(True)

            Edge(self.editor.scene, previousNode.node_output, node.node_input)        
            previousNode = node

            node = Node(self.session, self.editor.scene, NodeType.Wait)
            posY += 200
            node.setPos(posX, posY)

            Edge(self.editor.scene, previousNode.node_output, node.node_input)        
            previousNode = node

            node = Node(self.session, self.editor.scene, NodeType.Rotation, model_input=True, center_input=True)
            posY += 200
            node.setPos(posX, posY)
            node.summary.ModelToggle.setChecked(False)
            if index == 0:
                node.input_center.content.Molecule.ModelTree.selectionModel().select(node.input_center.content.Molecule.ModelTree.model().index(0, 0), QItemSelectionModel.SelectionFlag.Select)
                node.input_center.content.Molecule.select()
                node.summary.CenterToggle.setChecked(True)
            else:
                node.summary.CenterToggle.setChecked(False)
            node.content.Axis.setCurrentIndex(1)
            node.content.Angle.setText("6")
            node.content.Frames.setText("60")

            Edge(self.editor.scene, previousNode.node_output, node.node_input)        
            previousNode = node

            node = Node(self.session, self.editor.scene, NodeType.Wait)
            posY += 200
            node.setPos(posX, posY)
            posX += 300

            Edge(self.editor.scene, previousNode.node_output, node.node_input)        
            previousNode = node

        self.editor.nodeEnd.setPos(posX, posY)

        Edge(self.editor.scene, previousNode.node_output, self.editor.nodeEnd.node_input)        

        chain_start:list[Node] = []
        for edge in self.editor.scene.edges:
            starting_node = edge.start_socket.node.nodeID
            if starting_node not in [e.end_socket.node.nodeID for e in self.editor.scene.edges]:
                chain_start.append(edge.start_socket.node)
        for n in chain_start:
            n.summary.updateOutputValues(check_update=False)

        corners = self.editor.scene.findSceneCorners()
        self.editor.centerOn(corners[0], corners[1], corners[2], corners[3])
        self.editor.scaleOn(corners[0], corners[1], corners[2], corners[3])

    def rotation_preset_surfaces(self):
        posX = -300
        posY = -200
        self.editor.nodeStart.setPos(posX, posY)

        previousNode = self.editor.nodeStart

        posX += 300
        posY = -300

        node = Node(self.session, self.editor.scene, NodeType.ColorPalette, color_input=True)
        node.setPos(posX, posY)
        selected_color_groups = []
        if node.input_color.content.Molecule.ModelTree.model().rowCount() > 1:
            for i in range(node.input_color.content.Molecule.ModelTree.model().rowCount()):
                if  node.input_color.content.Molecule.ModelTree.model().index(i, 0).data() != "All" and node.input_color.content.Molecule.ModelTree.model().index(i, 0).data() != "Special Residue":
                    model:QStandardItemModel = node.input_color.content.Molecule.ModelTree.model()
                    item = model.item(i, 0)
                    if item.rowCount() > 0:
                        for j in range(item.rowCount()):
                            if model.index(j, 0, model.index(i, 0)).data() != "Special Residue":
                                node.input_color.content.Molecule.ModelTree.selectionModel().select(model.index(j, 0, model.index(i, 0)), QItemSelectionModel.SelectionFlag.Select)
                                node.input_color.content.Molecule.AddGroup()
                    else:            
                        node.input_color.content.Molecule.ModelTree.selectionModel().select(model.index(i, 0), QItemSelectionModel.SelectionFlag.Select)
                        node.input_color.content.Molecule.AddGroup()
        else:
            node.input_color.content.Molecule.ModelTree.selectionModel().select(node.input_color.content.Molecule.ModelTree.model().index(0, 0), QItemSelectionModel.SelectionFlag.Select)
            node.input_color.content.Molecule.AddGroup()
        node.input_color.content.Molecule.select()
        node.summary.ColorToggle.setChecked(True)
        node.content.Color.setCurrentIndex(8)
        node.content.CustomColor.setCurrentIndex(4)
        selected_color_groups = node.summary.picker_color_groups

        Edge(self.editor.scene, previousNode.node_output, node.node_input)        
        previousNode = node

        node = Node(self.session, self.editor.scene, NodeType.Transparency, model_input=True)
        posY += 200
        node.setPos(posX, posY)
        node.input_model.content.Molecule.ModelTree.selectionModel().select(node.input_model.content.Molecule.ModelTree.model().index(0, 0), QItemSelectionModel.SelectionFlag.Select)
        node.input_model.content.Molecule.select()
        node.content.Surfaces.setText("100")
        node.content.Cartoons.setText("100")
        node.content.Atoms.setText("100")
        node.summary.ModelToggle.setChecked(True)

        Edge(self.editor.scene, previousNode.node_output, node.node_input)   
        previousNode = node
        
        posX += 300

        for index, value in enumerate(selected_color_groups):
            posY = -300
            node = Node(self.session, self.editor.scene, NodeType.Crossfade,)
            node.setPos(posX, posY)
            node.content.Frames.setText("50")

            Edge(self.editor.scene, previousNode.node_output, node.node_input)        
            previousNode = node

            node = Node(self.session, self.editor.scene, NodeType.Transparency, model_input=True)
            posY += 200
            node.setPos(posX, posY)
            count = 0
            if node.input_model.content.Molecule.ModelTree.model().rowCount() > 1:
                for i in range(node.input_model.content.Molecule.ModelTree.model().rowCount()):
                    if node.input_model.content.Molecule.ModelTree.model().index(i, 0).data() != "All" and node.input_model.content.Molecule.ModelTree.model().index(i, 0).data() != "Special Residue":
                        model:QStandardItemModel = node.input_model.content.Molecule.ModelTree.model()
                        item = model.item(i, 0)
                        if item.rowCount() > 0:
                            for j in range(item.rowCount()):
                                if model.index(j, 0, model.index(i, 0)).data() != "Special Residue":
                                    node.input_model.content.Molecule.ModelTree.selectionModel().select(model.index(j, 0, model.index(i, 0)), QItemSelectionModel.SelectionFlag.Select)
                                    count += 1
                                if count >= index + 1:
                                    break
                        else:                                                
                            node.input_model.content.Molecule.ModelTree.selectionModel().select(model.index(i, 0), QItemSelectionModel.SelectionFlag.Select)
                            count += 1
                        if count >= index + 1:
                            break
                    if count >= index + 1:
                        break
            else:
                node.input_model.content.Molecule.ModelTree.selectionModel().select(node.input_model.content.Molecule.ModelTree.model().index(0, 0), QItemSelectionModel.SelectionFlag.Select)
                node.input_model.content.Molecule.select()
            node.input_model.content.Molecule.select()
            node.content.Surfaces.setText("0")
            node.content.Cartoons.setText("100")
            node.content.Atoms.setText("100")
            node.summary.ModelToggle.setChecked(True)

            Edge(self.editor.scene, previousNode.node_output, node.node_input)        
            previousNode = node

            node = Node(self.session, self.editor.scene, NodeType.Wait)
            posY += 200
            node.setPos(posX, posY)

            Edge(self.editor.scene, previousNode.node_output, node.node_input)        
            previousNode = node

            node = Node(self.session, self.editor.scene, NodeType.Rotation, model_input=True, center_input=True)
            posY += 200
            node.setPos(posX, posY)
            node.summary.ModelToggle.setChecked(False)
            if index == 0:
                node.input_center.content.Molecule.ModelTree.selectionModel().select(node.input_center.content.Molecule.ModelTree.model().index(0, 0), QItemSelectionModel.SelectionFlag.Select)
                node.input_center.content.Molecule.select()
                node.summary.CenterToggle.setChecked(True)
            else:
                node.summary.CenterToggle.setChecked(False)
            node.content.Axis.setCurrentIndex(1)
            node.content.Angle.setText("6")
            node.content.Frames.setText("60")

            Edge(self.editor.scene, previousNode.node_output, node.node_input)        
            previousNode = node

            node = Node(self.session, self.editor.scene, NodeType.Wait)
            posY += 200
            node.setPos(posX, posY)
            posX += 300

            Edge(self.editor.scene, previousNode.node_output, node.node_input)        
            previousNode = node

        self.editor.nodeEnd.setPos(posX, posY)

        Edge(self.editor.scene, previousNode.node_output, self.editor.nodeEnd.node_input)        

        chain_start:list[Node] = []
        for edge in self.editor.scene.edges:
            starting_node = edge.start_socket.node.nodeID
            if starting_node not in [e.end_socket.node.nodeID for e in self.editor.scene.edges]:
                chain_start.append(edge.start_socket.node)
        for n in chain_start:
            n.summary.updateOutputValues(check_update=False)

        corners = self.editor.scene.findSceneCorners()
        self.editor.centerOn(corners[0], corners[1], corners[2], corners[3])
        self.editor.scaleOn(corners[0], corners[1], corners[2], corners[3])

        
    def rotation_preset_cartoons_special_atoms(self):
        posX = -300
        posY = -300
        self.editor.nodeStart.setPos(posX, posY)

        previousNode = self.editor.nodeStart

        posX += 300
        posY = -300

        node = Node(self.session, self.editor.scene, NodeType.ColorPalette, color_input=True)
        node.setPos(posX, posY)
        selected_color_groups = []
        if node.input_color.content.Molecule.ModelTree.model().rowCount() > 1:
            for i in range(node.input_color.content.Molecule.ModelTree.model().rowCount()):
                if  node.input_color.content.Molecule.ModelTree.model().index(i, 0).data() != "All" and node.input_color.content.Molecule.ModelTree.model().index(i, 0).data() != "Special Residue":
                    model:QStandardItemModel = node.input_color.content.Molecule.ModelTree.model()
                    item = model.item(i, 0)
                    if item.rowCount() > 0:
                        for j in range(item.rowCount()):
                            if model.index(j, 0, model.index(i, 0)).data() != "Special Residue":
                                node.input_color.content.Molecule.ModelTree.selectionModel().select(model.index(j, 0, model.index(i, 0)), QItemSelectionModel.SelectionFlag.Select)
                                node.input_color.content.Molecule.AddGroup()
                    else:            
                        node.input_color.content.Molecule.ModelTree.selectionModel().select(model.index(i, 0), QItemSelectionModel.SelectionFlag.Select)
                        node.input_color.content.Molecule.AddGroup()
        else:
            node.input_color.content.Molecule.ModelTree.selectionModel().select(node.input_color.content.Molecule.ModelTree.model().index(0, 0), QItemSelectionModel.SelectionFlag.Select)
            node.input_color.content.Molecule.AddGroup()
        node.input_color.content.Molecule.select()
        node.summary.ColorToggle.setChecked(True)
        node.content.Color.setCurrentIndex(8)
        node.content.CustomColor.setCurrentIndex(4)
        selected_color_groups = node.summary.picker_color_groups

        Edge(self.editor.scene, previousNode.node_output, node.node_input)        
        previousNode = node

        node = Node(self.session, self.editor.scene, NodeType.ColorPalette, color_input=True)
        posY += 250
        node.setPos(posX, posY)
        selected_color_groups = []
        if node.input_color.content.Molecule.ModelTree.model().rowCount() > 1:
            for i in range(node.input_color.content.Molecule.ModelTree.model().rowCount()):
                if  node.input_color.content.Molecule.ModelTree.model().index(i, 0).data() != "All" and node.input_color.content.Molecule.ModelTree.model().index(i, 0).data() != "Special Residue":
                    model:QStandardItemModel = node.input_color.content.Molecule.ModelTree.model()
                    item = model.item(i, 0)
                    if item.rowCount() > 0:
                        for j in range(item.rowCount()):
                            if model.index(j, 0, model.index(i, 0)).data() != "Special Residue":
                                node.input_color.content.Molecule.ModelTree.selectionModel().select(model.index(j, 0, model.index(i, 0)), QItemSelectionModel.SelectionFlag.Select)
                                node.input_color.content.Molecule.AddGroup()
                    else:            
                        node.input_color.content.Molecule.ModelTree.selectionModel().select(model.index(i, 0), QItemSelectionModel.SelectionFlag.Select)
                        node.input_color.content.Molecule.AddGroup()
        else:
            node.input_color.content.Molecule.ModelTree.selectionModel().select(node.input_color.content.Molecule.ModelTree.model().index(0, 0), QItemSelectionModel.SelectionFlag.Select)
            node.input_color.content.Molecule.AddGroup()
        node.input_color.content.Molecule.select()
        node.summary.ColorToggle.setChecked(True)
        node.content.Color.setCurrentIndex(1)
        selected_color_groups = node.summary.picker_color_groups

        Edge(self.editor.scene, previousNode.node_output, node.node_input)        
        previousNode = node

        node = Node(self.session, self.editor.scene, NodeType.Transparency, model_input=True)
        posY += 250
        node.setPos(posX, posY)
        node.input_model.content.Molecule.ModelTree.selectionModel().select(node.input_model.content.Molecule.ModelTree.model().index(0, 0), QItemSelectionModel.SelectionFlag.Select)
        node.input_model.content.Molecule.select()
        node.content.Surfaces.setText("100")
        node.content.Cartoons.setText("100")
        node.content.Atoms.setText("100")
        node.summary.ModelToggle.setChecked(True)

        Edge(self.editor.scene, previousNode.node_output, node.node_input)   
        previousNode = node
        
        posX += 300

        for index, value in enumerate(selected_color_groups):
            posY = -300
            node = Node(self.session, self.editor.scene, NodeType.Crossfade)
            node.setPos(posX, posY)
            node.content.Frames.setText("50")

            Edge(self.editor.scene, previousNode.node_output, node.node_input)        
            previousNode = node

            node = Node(self.session, self.editor.scene, NodeType.Transparency, model_input=True)
            posY += 250
            node.setPos(posX, posY)
            count = 0
            if node.input_model.content.Molecule.ModelTree.model().rowCount() > 1:
                for i in range(node.input_model.content.Molecule.ModelTree.model().rowCount()):
                    if node.input_model.content.Molecule.ModelTree.model().index(i, 0).data() != "All" and node.input_model.content.Molecule.ModelTree.model().index(i, 0).data() != "Special Residue":
                        model:QStandardItemModel = node.input_model.content.Molecule.ModelTree.model()
                        item = model.item(i, 0)
                        if item.rowCount() > 0:
                            for j in range(item.rowCount()):
                                if model.index(j, 0, model.index(i, 0)).data() != "Special Residue":
                                    node.input_model.content.Molecule.ModelTree.selectionModel().select(model.index(j, 0, model.index(i, 0)), QItemSelectionModel.SelectionFlag.Select)
                                    count += 1
                                if count >= index + 1:
                                    break
                        else:                                                
                            node.input_model.content.Molecule.ModelTree.selectionModel().select(model.index(i, 0), QItemSelectionModel.SelectionFlag.Select)
                            count += 1
                        if count >= index + 1:
                            break
                    if count >= index + 1:
                        break
            else:
                node.input_model.content.Molecule.ModelTree.selectionModel().select(node.input_model.content.Molecule.ModelTree.model().index(0, 0), QItemSelectionModel.SelectionFlag.Select)
                node.input_model.content.Molecule.select()
            node.input_model.content.Molecule.select()
            node.content.Surfaces.setText("100")
            node.content.Cartoons.setText("0")
            node.content.Atoms.setText("100")
            node.summary.ModelToggle.setChecked(True)

            Edge(self.editor.scene, previousNode.node_output, node.node_input)        
            previousNode = node

            posY += 250
            node = Node(self.session, self.editor.scene, NodeType.Transparency, model_input=True)
            node.setPos(posX, posY)
            count = 0
            if node.input_model.content.Molecule.ModelTree.model().rowCount() > 1:
                for i in range(node.input_model.content.Molecule.ModelTree.model().rowCount()):
                    if node.input_model.content.Molecule.ModelTree.model().index(i, 0).data() != "All" and node.input_model.content.Molecule.ModelTree.model().index(i, 0).data() != "Special Residue":
                        model:QStandardItemModel = node.input_model.content.Molecule.ModelTree.model()
                        item = model.item(i, 0)
                        if item.rowCount() > 0:
                            for j in range(item.rowCount()):
                                if model.index(j, 0, model.index(i, 0)).data() != "Special Residue":
                                    if model.index(0, 0, model.index(j, 0, model.index(i, 0))).data() == "Special Residue":
                                        node.input_model.content.Molecule.ModelTree.selectionModel().select(model.index(0, 0, model.index(j, 0, model.index(i, 0))), QItemSelectionModel.SelectionFlag.Select)
                                    count += 1
                                    if count >= index + 1:
                                        break
                    if count >= index + 1:
                        break
            node.input_model.content.Molecule.select()
            node.content.Surfaces.setText("100")
            node.content.Cartoons.setText("100")
            node.content.Atoms.setText("0")
            node.content.AtomsStyle.setCurrentIndex(1)
            node.summary.ModelToggle.setChecked(True)

            Edge(self.editor.scene, previousNode.node_output, node.node_input)        
            previousNode = node

            node = Node(self.session, self.editor.scene, NodeType.Wait)
            posY += 200
            node.setPos(posX, posY)

            Edge(self.editor.scene, previousNode.node_output, node.node_input)        
            previousNode = node

            node = Node(self.session, self.editor.scene, NodeType.Rotation, model_input=True, center_input=True)
            posY += 200
            node.setPos(posX, posY)
            node.summary.ModelToggle.setChecked(False)
            if index == 0:
                node.input_center.content.Molecule.ModelTree.selectionModel().select(node.input_center.content.Molecule.ModelTree.model().index(0, 0), QItemSelectionModel.SelectionFlag.Select)
                node.input_center.content.Molecule.select()
                node.summary.CenterToggle.setChecked(True)
            else:
                node.summary.CenterToggle.setChecked(False)
            node.content.Axis.setCurrentIndex(1)
            node.content.Angle.setText("6")
            node.content.Frames.setText("60")

            Edge(self.editor.scene, previousNode.node_output, node.node_input)        
            previousNode = node

            node = Node(self.session, self.editor.scene, NodeType.Wait)
            posY += 200
            node.setPos(posX, posY)
            posX += 300

            Edge(self.editor.scene, previousNode.node_output, node.node_input)        
            previousNode = node

        self.editor.nodeEnd.setPos(posX, posY)

        Edge(self.editor.scene, previousNode.node_output, self.editor.nodeEnd.node_input)        

        chain_start:list[Node] = []
        for edge in self.editor.scene.edges:
            starting_node = edge.start_socket.node.nodeID
            if starting_node not in [e.end_socket.node.nodeID for e in self.editor.scene.edges]:
                chain_start.append(edge.start_socket.node)
        for n in chain_start:
            n.summary.updateOutputValues(check_update=False)

        corners = self.editor.scene.findSceneCorners()
        self.editor.centerOn(corners[0], corners[1], corners[2], corners[3])
        self.editor.scaleOn(corners[0], corners[1], corners[2], corners[3])
