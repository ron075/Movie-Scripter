from __future__ import annotations

import sys
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from .enum_classes import *
from .node import *
from chimerax.core.commands import run
from chimerax.core.tools import ToolInstance

from chimerax.ui import MainToolWindow


class MovieMaker(ToolInstance):

    SESSION_ENDURING = False
    SESSION_SAVE = True

    def __init__(self, session, tool_name):
        # Initialize base class.
        super().__init__(session, tool_name)
        self.tool_session = session

        self.display_name = "Movie Maker"
        self.tool_window = MainToolWindow(self)
        self.parent:QWidget = self.tool_window.ui_area
        self.pp:QDockWidget = self.parent.parent().parent()
        self.pp.resize(1000,800)
        self._build_ui()

    def _build_ui(self):
        from .main_window import NodeEditor
        self.layout = QGridLayout()
        self.layout.setContentsMargins(10, 10, 10, 10)

        self.parent.setLayout(self.layout)
        self.parent.setObjectName("frame")
        self.frame = NodeEditor(self.tool_session, self)

        self.layout.addWidget(self.frame)

        self.tool_window.manage(placement=None, allowed_areas=Qt.DockWidgetArea.NoDockWidgetArea)

    def delete(self):
        self.frame.tool_status = ToolStatus.TERMINATING
        self.tool_window.cleanup()
        super().delete()

    def node_to_variant(self, item:Node) -> dict:
        data = {}
        if type(item) is Node: 
            if NodeType(item.nodeType) != NodeType.Picker:
                data["nodeType"] = item.nodeType.value
                data["nodeID"] = item.nodeID

                data["pos.X"] = item.pos.x()
                data["pos.Y"] = item.pos.y()
                node = item.content
                if NodeType(item.nodeType) == NodeType.Start:
                    data["content.Record"] = node.Record.isChecked()
                    data["content.Resolution"] = node.Resolution.currentIndex()
                    data["content.Height"] = node.Height.Text.text()
                    data["content.Width"] = node.Width.Text.text()
                elif NodeType(item.nodeType) == NodeType.ColorPalette:
                    data["content.colormap_height"] = node.colormap_height
                    data["content.current_index"] = node.current_index
                    data["content.Color.currentText"] = node.Color.currentText()
                    if node.Color.currentText() == "From Palette" or node.Color.currentText() == "Partial Random":
                        data["content.group_colors"] = [color.name() for color in node.group_colors]
                    else:
                        data["content.group_colors"] = node.group_colors
                    data["content.Color"] = node.Color.currentIndex()
                    data["content.CustomColor"] = node.CustomColor.currentIndex()
                    data["content.Group"] = node.Group.currentIndex()
                    if not self.frame.simple_mode:
                        data["content.group_target"] = node.group_target
                        data["content.group_halfbond"] = node.group_halfbond
                        data["content.group_change_transparency"] = node.group_change_transparency
                        data["content.group_transparency"] = node.group_transparency
                        data["content.group_level"] = node.group_level
                        data["content.Tab"] = node.Tab.currentIndex()
                    node.resetGroups()
                elif NodeType(item.nodeType) == NodeType.Lighting:
                    data["content.Preset"] = node.Preset.currentIndex()
                elif NodeType(item.nodeType) == NodeType.Transparency:
                    data["content.Surfaces"] = node.Surfaces.Text.text()
                    data["content.Cartoons"] = node.Cartoons.Text.text()
                    data["content.Atoms"] = node.Atoms.Text.text()
                    data["content.AtomsStyle"] = node.AtomsStyle.currentIndex()
                elif NodeType(item.nodeType) == NodeType.Label2D:
                    data["content.Text"] = node.Text.text()
                    if node.TextColorPicked:
                        data["content.TextColorPicked"] = node.TextColorPicked.name()
                    else:
                        data["content.TextColorPicked"] = "default"
                    if node.BackgroundColorPicked:
                        data["content.BackgroundColorPicked"] = node.BackgroundColorPicked.name()
                    else:
                        data["content.BackgroundColorPicked"] = ""
                    data["content.X"] = node.X.Text.text()
                    data["content.Y"] = node.Y.Text.text()
                    data["content.Size"] = node.Size.Text.text()
                    data["content.Outline"] = node.Outline.Text.text()
                    data["content.Margin"] = node.Margin.Text.text()
                    data["content.Font"] = node.Font.currentIndex()
                    data["content.Bold"] = node.Bold.isChecked()
                    data["content.Italic"] = node.Italic.isChecked()
                    data["content.Visibility"] = node.Visibility.isChecked()
                elif NodeType(item.nodeType) == NodeType.Label3D:
                    data["content.Text"] = node.Text.text()
                    if node.TextColorPicked:
                        data["content.TextColorPicked"] = node.TextColorPicked.name()
                    else:
                        data["content.TextColorPicked"] = ""
                    if node.BackgroundColorPicked:
                        data["content.BackgroundColorPicked"] = node.BackgroundColorPicked.name()
                    else:
                        data["content.BackgroundColorPicked"] = ""
                    data["content.Structure"] = node.Structure.currentIndex()
                    data["content.Height"] = node.Height.currentIndex()
                    data["content.HeightValue"] = node.HeightValue.Text.text()
                    data["content.Size"] = node.Size.Text.text()
                    data["content.OffsetX"] = node.OffsetX.Text.text()
                    data["content.OffsetY"] = node.OffsetY.Text.text()
                    data["content.OffsetZ"] = node.OffsetZ.Text.text()
                    data["content.Font"] = node.Font.currentIndex()
                    data["content.OnTop"] = node.OnTop.isChecked()
                elif NodeType(item.nodeType) == NodeType.Movement:
                    data["content.Cofr"] = node.Cofr.isChecked()
                    data["content.MoveX"] = node.MoveX.Text.text()
                    data["content.MoveY"] = node.MoveY.Text.text()
                    data["content.MoveZ"] = node.MoveZ.Text.text()
                elif NodeType(item.nodeType) == NodeType.Turn:
                    data["content.Axis"] = node.Axis.currentIndex()
                    data["content.Angle"] = node.Angle.Text.text()
                    data["content.Frames"] = node.Frames.Text.text()
                    if not self.frame.simple_mode:
                        data["content.RelativeAxis"] = node.RelativeAxis.isChecked()
                elif NodeType(item.nodeType) == NodeType.Rock:
                    data["content.Axis"] = node.Axis.currentIndex()
                    data["content.Angle"] = node.Angle.Text.text()
                    data["content.Frames"] = node.Frames.Text.text()
                    if not self.frame.simple_mode:
                        data["content.RelativeAxis"] = node.RelativeAxis.isChecked()
                    data["content.RockCycle"] = node.RockCycle.Text.text()
                elif NodeType(item.nodeType) == NodeType.Wobble:
                    data["content.Axis"] = node.Axis.currentIndex()
                    data["content.Angle"] = node.Angle.Text.text()
                    data["content.Frames"] = node.Frames.Text.text()
                    if not self.frame.simple_mode:
                        data["content.RelativeAxis"] = node.RelativeAxis.isChecked()
                    data["content.WobbleCycle"] = node.WobbleCycle.Text.text()
                    data["content.WobbleAspect"] = node.WobbleAspect.Text.text()
                elif NodeType(item.nodeType) == NodeType.CenterRotation:
                    data["content.Method"] = node.Method.currentIndex()
                    data["content.Pivot"] = node.Pivot.currentIndex()
                    data["content.Length"] = node.Length.Text.text()
                    data["content.Radius"] = node.Radius.Text.text()
                elif NodeType(item.nodeType) == NodeType.CenterMass:
                    data["content.Name"] = node.Name.text()
                    data["content.Mark"] = node.Mark.isChecked()
                    data["content.Radius"] = node.Radius.Text.text()
                    if node.MarkColorValue is not None:
                        data["content.MarkColorValue"] = node.MarkColorValue.name()
                    else:
                        data["content.MarkColorValue"] = None
                elif NodeType(item.nodeType) == NodeType.Delete:
                    data["content.Type"] = node.Type.currentIndex()
                    data["content.AttachedHyds"] = node.AttachedHyds.isChecked()
                elif NodeType(item.nodeType) == NodeType.Wait:
                    data["content.Frames"] = node.Frames.Text.text()
                elif NodeType(item.nodeType) == NodeType.Crossfade:
                    data["content.Frames"] = node.Frames.Text.text()
                elif NodeType(item.nodeType) == NodeType.View_Save:
                    data["content.Name"] = node.Name.text()
                elif NodeType(item.nodeType) == NodeType.View_Load:
                    data["content.View"] = node.View.currentIndex()
                    data["content.Clip"] = node.Clip.isChecked()
                    data["content.Cofr"] = node.Cofr.isChecked()
                    data["content.Pad"] = node.Pad.Text.text()
                elif NodeType(item.nodeType) == NodeType.Fly:
                    if len(node.transition_frames) > 0:
                        node.transition_frames[node.current_index] = node.Frames.getText()
                    data["content.transition_frames"] = node.transition_frames
                elif NodeType(item.nodeType) == NodeType.Split:
                    data["content.Model"] = node.Model.currentIndex()
                elif NodeType(item.nodeType) == NodeType.End:
                    data["content.Framerate"] = node.Framerate.Text.text()
                    data["content.Quality"] = node.Quality.currentIndex()
                    data["content.Name"] = node.Name.text()
                    data["content.Roundtrip"] = node.Roundtrip.isChecked()
                    data["content.Format"] = node.Format.currentIndex()

                if item.input_model is not None:
                    if not self.frame.simple_mode:
                        data["summary.ModelToggle"] = node.summary.ModelToggle.isChecked()

                    data["input_model.pos.X"] = item.input_model.pos.x()
                    data["input_model.pos.Y"] = item.input_model.pos.y()

                    picker = item.input_model.content
                    data["input_model.content.Molecule.selected_model"] = picker.Molecule.selected_model

                    data["input_model.content.Molecule.all_views"] = picker.Molecule.all_views
                    
                    data["input_model.content.Molecule.ModelPicked"] = picker.Molecule.ModelPicked.toPlainText()

                if item.input_color is not None:
                    if not self.frame.simple_mode:
                        data["summary.ColorToggle"] = node.summary.ColorToggle.isChecked()

                    data["input_color.pos.X"] = item.input_color.pos.x()
                    data["input_color.pos.Y"] = item.input_color.pos.y()

                    picker = item.input_color.content
                    data["input_color.content.Molecule.selected_color_groups"] = picker.Molecule.selected_color_groups

                    data["input_color.content.Molecule.all_views"] = picker.Molecule.all_views
                    
                    data["input_color.content.Molecule.Tab"] = picker.Molecule.Tab.currentIndex()
                    data["input_color.content.Molecule.ModelPicked.selectedIndexes"] = [index.row() for index in picker.Molecule.ModelPicked.selectedIndexes()]

                if item.input_center is not None:
                    if not self.frame.simple_mode:
                        data["summary.CenterToggle"] = node.summary.CenterToggle.isChecked()
                    
                    data["input_center.pos.X"] = item.input_center.pos.x()
                    data["input_center.pos.Y"] = item.input_center.pos.y()

                    picker = item.input_center.content
                    data["input_center.content.Molecule.selected_model"] = picker.Molecule.selected_model

                    data["input_center.content.Molecule.all_views"] = picker.Molecule.all_views
                    
                    data["input_center.content.Molecule.ModelPicked"] = picker.Molecule.ModelPicked.text()

                if item.input_view is not None:
                    if not self.frame.simple_mode:
                        data["summary.ViewToggle"] = node.summary.ViewToggle.isChecked()
                    
                    data["input_view.pos.X"] = item.input_view.pos.x()
                    data["input_view.pos.Y"] = item.input_view.pos.y()

                    picker = item.input_view.content
                    data["input_view.content.Molecule.selected_model"] = picker.Molecule.selected_model
                    data["input_view.content.Molecule.selected_fly_groups"] = picker.Molecule.selected_fly_groups

                    data["input_view.content.Molecule.all_views"] = picker.Molecule.all_views
                    
                    data["input_view.content.Molecule.Tab"] = picker.Molecule.Tab.currentIndex()
                    data["input_view.content.Molecule.ModelPicked"] = picker.Molecule.ModelPicked.toPlainText()
                    data["input_view.content.Molecule.ViewPicked"] = picker.Molecule.ViewPicked.toPlainText()

                if item.input_fly is not None:
                    if not self.frame.simple_mode:
                        data["summary.FlyToggle"] = node.summary.FlyToggle.isChecked()
                    
                    data["input_fly.pos.X"] = item.input_fly.pos.x()
                    data["input_fly.pos.Y"] = item.input_fly.pos.y()

                    picker = item.input_fly.content
                    data["input_fly.content.Molecule.selected_fly_groups"] = picker.Molecule.selected_fly_groups

                    data["input_fly.content.Molecule.all_views"] = picker.Molecule.all_views
                    
                    data["input_fly.content.Molecule.Tab"] = picker.Molecule.Tab.currentIndex()
                    
                if item.input_delete is not None:
                    data["input_delete.pos.X"] = item.input_delete.pos.x()
                    data["input_delete.pos.Y"] = item.input_delete.pos.y()

                    picker = item.input_delete.content
                    data["input_delete.content.Molecule.selected_model"] = picker.Molecule.selected_model

                    data["input_delete.content.Molecule.all_views"] = picker.Molecule.all_views
                    
                    data["input_delete.content.Molecule.Tab"] = picker.Molecule.Tab.currentIndex()
                    data["input_delete.content.Molecule.ModelPicked"] = picker.Molecule.ModelPicked.toPlainText()
                    data["input_delete.content.Molecule.Label2DPicked"] = picker.Molecule.Label2DPicked.toPlainText()
                    data["input_delete.content.Molecule.Label3DPicked"] = picker.Molecule.Label3DPicked.toPlainText()
                    data["input_delete.content.Molecule.ViewPicked"] = picker.Molecule.ViewPicked.toPlainText()
        return data
            
    def edge_to_variant(self, item:Edge) -> dict:
        data = {}
        data["start_node.id"] = item.start_socket.node.nodeID
        data["end_node.id"] = item.end_socket.node.nodeID
        return data
    
    def node_from_variant(self, data:dict):
        node = None
        if NodeType(data["nodeType"]) == NodeType.Start:
            node = self.frame.nodeStart
            self.frame.scene.replaceID(node.nodeID, data["nodeID"])
            node.nodeID = data["nodeID"]
            node.content.Record.setChecked(bool(data["content.Record"]))
            node.content.Resolution.setCurrentIndex(int(data["content.Resolution"]))
            if node.content.Resolution.currentText() == "Custom":
                node.content.Height.setText(data["content.Height"])
                node.content.Width.setText(data["content.Width"])
        elif NodeType(data["nodeType"]) == NodeType.ColorPalette:
            node = Node(self.tool_session, self.frame.scene, NodeType.ColorPalette, data["nodeID"], color_input=True, colormap_height=int(data["content.colormap_height"]))
            node.content.current_index = int(data["content.current_index"])
            if data["content.Color.currentText"] == "From Palette" or data["content.Color.currentText"] == "Partial Random":
                node.content.group_colors = [QColor(color) for color in data["content.group_colors"]]
            else:
                node.content.group_colors = data["content.group_colors"]
            node.content.Color.currentIndexChanged.disconnect(node.content.switchColors)
            node.content.CustomColor.currentIndexChanged.disconnect(node.content.switchColors)
            node.content.Color.setCurrentIndex(int(data["content.Color"]))
            node.content.CustomColor.setCurrentIndex(int(data["content.CustomColor"]))
            node.content.Group.currentIndexChanged.disconnect(node.content.groupChange)
            node.content.Group.setCurrentIndex(int(data["content.Group"]))
            node.content.current_index = node.content.Group.currentIndex()
            node.content.Group.currentIndexChanged.connect(node.content.groupChange)
            node.content.Color.currentIndexChanged.connect(node.content.switchColors)
            node.content.CustomColor.currentIndexChanged.connect(node.content.switchColors)
            if not self.frame.simple_mode:
                node.content.group_target = data["content.group_target"]
                node.content.group_halfbond = data["content.group_halfbond"]
                node.content.group_change_transparency = data["content.group_change_transparency"]
                node.content.group_transparency = data["content.group_transparency"]
                node.content.group_level = data["content.group_level"]
                node.content.Tab.setCurrentIndex(int(data["content.Tab"]))
        elif NodeType(data["nodeType"]) == NodeType.Lighting:
            node = Node(self.tool_session, self.frame.scene, NodeType.Lighting, data["nodeID"])
            node.content.Preset.setCurrentIndex(int(data["content.Preset"]))
        elif NodeType(data["nodeType"]) == NodeType.Transparency:            
            node = Node(self.tool_session, self.frame.scene, NodeType.Transparency, data["nodeID"], model_input=True)
            node.content.Surfaces.setText(data["content.Surfaces"])
            node.content.Cartoons.setText(data["content.Cartoons"])
            node.content.Atoms.setText(data["content.Atoms"])
            node.content.AtomsStyle.setCurrentIndex(int(data["content.AtomsStyle"]))
        elif NodeType(data["nodeType"]) == NodeType.Label2D:
            node = Node(self.tool_session, self.frame.scene, NodeType.Label2D, data["nodeID"])
            node.content.Text.setText(data["content.Text"])
            if data["content.TextColorPicked"] == "default":
                node.content.TextColorPicked  = None
            else:
                node.content.TextColorPicked = QColor(data["content.TextColorPicked"])
                node.content.updateTextColor()
            if data["content.BackgroundColorPicked"] == "":
                node.content.BackgroundColorPicked  = None
            else:
                node.content.BackgroundColorPicked = QColor(data["content.BackgroundColorPicked"])
                node.content.updateBackgroundColor()
            node.content.X.setText(data["content.X"])
            node.content.Y.setText(data["content.Y"])
            node.content.Size.setText(data["content.Size"])
            node.content.Outline.setText(data["content.Outline"])
            node.content.Margin.setText(data["content.Margin"])
            node.content.Font.setCurrentIndex(int(data["content.Font"]))
            node.content.Bold.setChecked(data["content.Bold"])
            node.content.Italic.setChecked(data["content.Italic"])
            node.content.Visibility.setChecked(data["content.Visibility"])
        elif NodeType(data["nodeType"]) == NodeType.Label3D:
            node = Node(self.tool_session, self.frame.scene, NodeType.Label3D, data["nodeID"])
            node.content.Text.setText(data["content.Text"])
            if data["content.TextColorPicked"] == "":
                node.content.TextColorPicked  = None
            else:
                node.content.TextColorPicked = QColor(data["content.TextColorPicked"])
                node.content.updateTextColor()
            if data["content.BackgroundColorPicked"] == "":
                node.content.BackgroundColorPicked  = None
            else:
                node.content.BackgroundColorPicked = QColor(data["content.BackgroundColorPicked"])
                node.content.updateBackgroundColor()
            node.content.Structure.setCurrentIndex(int(data["content.Structure"]))
            node.content.Height.setCurrentIndex(int(data["content.Height"]))
            node.content.HeightValue.setText(data["content.HeightValue"])
            node.content.Size.setText(data["content.Size"])
            node.content.OffsetX.setText(data["content.OffsetX"])
            node.content.OffsetY.setText(data["content.OffsetY"])
            node.content.OffsetZ.setText(data["content.OffsetZ"])
            node.content.Font.setCurrentIndex(int(data["content.Font"]))
            node.content.OnTop.setChecked(data["content.OnTop"])
        elif NodeType(data["nodeType"]) == NodeType.Movement:
            node = Node(self.tool_session, self.frame.scene, NodeType.Movement, data["nodeID"], model_input=True)
            node.content.Cofr.setChecked(data["content.Cofr"])
            node.content.MoveX.setText(data["content.MoveX"])
            node.content.MoveY.setText(data["content.MoveY"])
            node.content.MoveZ.setText(data["content.MoveZ"])
        elif NodeType(data["nodeType"]) == NodeType.Turn:
            node = Node(self.tool_session, self.frame.scene, NodeType.Turn, data["nodeID"], model_input=True, center_input=True)
            node.content.Axis.setCurrentIndex(int(data["content.Axis"]))
            node.content.Angle.setText(data["content.Angle"])
            node.content.Frames.setText(data["content.Frames"])
            if not self.frame.simple_mode:
                node.content.RelativeAxis.setChecked(data["content.RelativeAxis"])
        elif NodeType(data["nodeType"]) == NodeType.Rock:
            node = Node(self.tool_session, self.frame.scene, NodeType.Rock, data["nodeID"], model_input=True, center_input=True)
            node.content.Axis.setCurrentIndex(int(data["content.Axis"]))
            node.content.Angle.setText(data["content.Angle"])
            node.content.Frames.setText(data["content.Frames"])
            if not self.frame.simple_mode:
                node.content.RelativeAxis.setChecked(data["content.RelativeAxis"])
            node.content.RockCycle.setText(data["content.RockCycle"])
        elif NodeType(data["nodeType"]) == NodeType.Wobble:
            node = Node(self.tool_session, self.frame.scene, NodeType.Wobble, data["nodeID"], model_input=True, center_input=True)
            node.content.Axis.setCurrentIndex(int(data["content.Axis"]))
            node.content.Angle.setText(data["content.Angle"])
            node.content.Frames.setText(data["content.Frames"])
            if not self.frame.simple_mode:
                node.content.RelativeAxis.setChecked(data["content.RelativeAxis"])
            node.content.WobbleCycle.setText(data["content.WobbleCycle"])
            node.content.WobbleAspect.setText(data["content.WobbleAspect"])
        elif NodeType(data["nodeType"]) == NodeType.CenterRotation:
            node = Node(self.tool_session, self.frame.scene, NodeType.CenterRotation, data["nodeID"], center_input=True)
            node.content.Method.setCurrentIndex(int(data["content.Method"]))
            node.content.Pivot.setCurrentIndex(int(data["content.Pivot"]))
            node.content.Length.setText(data["content.Length"])
            node.content.Radius.setText(data["content.Radius"])
        elif NodeType(data["nodeType"]) == NodeType.CenterMass:
            node = Node(self.tool_session, self.frame.scene, NodeType.CenterMass, data["nodeID"], model_input=True)
            node.content.Name.setText(data["content.Name"])
            node.content.Mark.setChecked(data["content.Mark"])
            node.content.Radius.setText(data["content.Radius"])
            if data["content.MarkColorValue"] is None:
                node.content.MarkColorValue = None
            else:
                node.content.MarkColorValue = QColor(data["content.MarkColorValue"])
                node.content.updateMarkColorLabel()
        elif NodeType(data["nodeType"]) == NodeType.Delete:
            node = Node(self.tool_session, self.frame.scene, NodeType.Delete, data["nodeID"], delete_input=True)
            node.content.Type.setCurrentIndex(int(data["content.Type"]))
            node.content.AttachedHyds.setChecked(data["content.AttachedHyds"])
        elif NodeType(data["nodeType"]) == NodeType.Wait:
            node = Node(self.tool_session, self.frame.scene, NodeType.Wait, data["nodeID"])
            node.content.Frames.setText(data["content.Frames"])
        elif NodeType(data["nodeType"]) == NodeType.Crossfade:
            node = Node(self.tool_session, self.frame.scene, NodeType.Crossfade, data["nodeID"])
            node.content.Frames.setText(data["content.Frames"])
        elif NodeType(data["nodeType"]) == NodeType.View_Save:
            node = Node(self.tool_session, self.frame.scene, NodeType.View_Save, data["nodeID"], view_input=True)
            node.content.Name.setText(data["content.Name"])
        elif NodeType(data["nodeType"]) == NodeType.View_Load:
            node = Node(self.tool_session, self.frame.scene, NodeType.View_Load, data["nodeID"], view_input=True)
            node.content.View.setCurrentIndex(int(data["content.View"]))
            node.content.Clip.setChecked(data["content.Clip"])
            node.content.Cofr.setChecked(data["content.Cofr"])
            node.content.Pad.setText(data["content.Pad"])
        elif NodeType(data["nodeType"]) == NodeType.Fly:
            node = Node(self.tool_session, self.frame.scene, NodeType.Fly, data["nodeID"], fly_input=True)
            node.content.transition_frames = data["content.transition_frames"]
            if len(node.content.transition_frames) > 0:
                node.content.Frames.Text.textChanged.disconnect(node.summary.updateFramesValues)
                node.content.Frames.Text.setText(node.content.transition_frames[0])
                node.content.Frames.Text.textChanged.connect(node.summary.updateFramesValues)
        elif NodeType(data["nodeType"]) == NodeType.Split:
            node = Node(self.tool_session, self.frame.scene, NodeType.Split, has_input=False, has_output=False, node_id=data["nodeID"], model_input=True)
            node.content.Model.setCurrentIndex(data["content.Model"])
        elif NodeType(data["nodeType"]) == NodeType.End:        
            node = self.frame.nodeEnd
            self.frame.scene.replaceID(node.nodeID, data["nodeID"])
            node.nodeID = data["nodeID"]
            node.content.Framerate.setText(data["content.Framerate"])
            node.content.Quality.setCurrentIndex(int(data["content.Quality"]))
            node.content.Name.setText(data["content.Name"])
            node.content.Roundtrip.setChecked(data["content.Roundtrip"])
            node.content.Format.setCurrentIndex(int(data["content.Format"]))
        if node is not None:
            node.grNode.initContent()
            node.grNode.first_load_content = False
            node.grNode.content.hide()
            node.setPos(float(data["pos.X"]), float(data["pos.Y"]))
            if node.input_model is not None:
                node.input_model.setPos(float(data["input_model.pos.X"]), float(data["input_model.pos.Y"]))

                node.input_model.content.Molecule.selected_model = data["input_model.content.Molecule.selected_model"]

                node.input_model.content.Molecule.all_views = data["input_model.content.Molecule.all_views"]
                
                node.input_model.content.Molecule.ModelPicked.setText(data["input_model.content.Molecule.ModelPicked"])

                if node.input_model.content.Molecule.Tab.currentIndex() == 0:
                    node.input_model.content.Molecule.updateModelswithValue(node.input_model.content.Molecule.selected_model, restore=True)

                if not self.frame.simple_mode:
                    node.summary.ModelToggle.setChecked(data["summary.ModelToggle"])

            if node.input_color is not None:
                node.input_color.setPos(float(data["input_color.pos.X"]), float(data["input_color.pos.Y"]))

                node.input_color.content.Molecule.selected_color_groups = data["input_color.content.Molecule.selected_color_groups"]

                node.input_color.content.Molecule.all_views = data["input_color.content.Molecule.all_views"]
                
                node.input_color.content.Molecule.Tab.setCurrentIndex(int(data["input_color.content.Molecule.Tab"]))
                selected_index = data["input_color.content.Molecule.ModelPicked.selectedIndexes"]
                
                for group in node.input_color.content.Molecule.selected_color_groups:
                    item = QStandardItem(f"Group {node.input_color.content.Molecule.ModelPickedModel.rowCount() + 1}")
                    node.input_color.content.Molecule.ModelPickedModel.appendRow(item)
                
                for index in selected_index:
                    node.input_color.content.Molecule.ModelGroup.setText("\n".join(node.input_color.content.Molecule.selected_color_groups[index]))

                if node.input_color.content.Molecule.Tab.currentIndex() == 0:
                    node.input_color.content.Molecule.updateModelswithValue(node.input_color.content.Molecule.selected_color_groups, restore=True)
                    node.content.Group.setCurrentIndex(node.content.current_index)

                if not self.frame.simple_mode:
                    node.summary.ColorToggle.setChecked(data["summary.ColorToggle"])

            if node.input_center is not None:
                node.input_center.setPos(float(data["input_center.pos.X"]), float(data["input_center.pos.Y"]))

                node.input_center.content.Molecule.selected_model = data["input_center.content.Molecule.selected_model"]

                node.input_center.content.Molecule.all_views = data["input_center.content.Molecule.all_views"]
                
                node.input_center.content.Molecule.ModelPicked.setText(data["input_center.content.Molecule.ModelPicked"])

                if node.input_center.content.Molecule.Tab.currentIndex() == 0:
                    node.input_center.content.Molecule.updateModelswithValue(node.input_center.content.Molecule.selected_model, restore=True)
                
                if not self.frame.simple_mode:
                    node.summary.CenterToggle.setChecked(data["summary.CenterToggle"])

            if node.input_view is not None:
                node.input_view.setPos(float(data["input_view.pos.X"]), float(data["input_view.pos.Y"]))

                node.input_view.content.Molecule.selected_model = data["input_view.content.Molecule.selected_model"]
                node.input_view.content.Molecule.selected_fly_groups = data["input_view.content.Molecule.selected_fly_groups"]

                node.input_view.content.Molecule.all_views = data["input_view.content.Molecule.all_views"]
                
                node.input_view.content.Molecule.Tab.setCurrentIndex(int(data["input_view.content.Molecule.Tab"]))
                node.input_view.content.Molecule.ModelPicked.setText(data["input_view.content.Molecule.ModelPicked"])
                node.input_view.content.Molecule.ViewPicked.setText(data["input_view.content.Molecule.ViewPicked"])

                if node.input_view.content.Molecule.Tab.currentIndex() == 0:
                    node.input_view.content.Molecule.updateModelswithValue(node.input_view.content.Molecule.selected_model, restore=True)
                elif node.input_view.content.Molecule.Tab.currentIndex() == 1:
                    node.input_view.content.Molecule.updateViewswithValue(node.input_view.content.Molecule.selected_fly_groups, restore=True)

                if not self.frame.simple_mode:
                    node.summary.ViewToggle.setChecked(data["summary.ViewToggle"])

            if node.input_fly is not None:
                node.input_fly.setPos(float(data["input_fly.pos.X"]), float(data["input_fly.pos.Y"]))

                node.input_fly.content.Molecule.selected_fly_groups = data["input_fly.content.Molecule.selected_fly_groups"]

                node.input_fly.content.Molecule.all_views = data["input_fly.content.Molecule.all_views"]
                
                node.input_fly.content.Molecule.Tab.setCurrentIndex(int(data["input_fly.content.Molecule.Tab"]))
                
                for view in node.input_fly.content.Molecule.selected_fly_groups:
                    item = QStandardItem(f"{view}")
                    node.input_fly.content.Molecule.ViewPickedModel.appendRow(item)
                    
                if node.input_fly.content.Molecule.Tab.currentIndex() == 0:
                    node.input_fly.content.Molecule.updateViewswithValue(node.input_fly.content.Molecule.selected_fly_groups, restore=True)
                    
                if not self.frame.simple_mode:
                    node.summary.FlyToggle.setChecked(data["summary.FlyToggle"])
                    
            if node.input_delete is not None:
                node.input_delete.setPos(float(data["input_delete.pos.X"]), float(data["input_delete.pos.Y"]))

                node.input_delete.content.Molecule.selected_model = data["input_delete.content.Molecule.selected_model"]

                node.input_delete.content.Molecule.all_views = data["input_delete.content.Molecule.all_views"]
                
                node.input_delete.content.Molecule.Tab.setCurrentIndex(int(data["input_delete.content.Molecule.Tab"]))
                node.input_delete.content.Molecule.ModelPicked.setText(data["input_delete.content.Molecule.ModelPicked"])
                node.input_delete.content.Molecule.Label2DPicked.setText(data["input_delete.content.Molecule.Label2DPicked"])
                node.input_delete.content.Molecule.Label3DPicked.setText(data["input_delete.content.Molecule.Label3DPicked"])
                node.input_delete.content.Molecule.ViewPicked.setText(data["input_delete.content.Molecule.ViewPicked"])

                if node.input_delete.content.Molecule.Tab.currentIndex() == 0:
                    node.input_delete.content.Molecule.updateModelswithValue(node.input_delete.content.Molecule.selected_model, restore=True)
                elif node.input_delete.content.Molecule.Tab.currentIndex() == 1:
                    node.input_delete.content.Molecule.updateModelswithValue(node.input_delete.content.Molecule.selected_model, restore=True)
                elif node.input_delete.content.Molecule.Tab.currentIndex() == 2:
                    node.input_delete.content.Molecule.updateModelswithValue(node.input_delete.content.Molecule.selected_model, restore=True)
                elif node.input_delete.content.Molecule.Tab.currentIndex() == 3:
                    node.input_delete.content.Molecule.updateViewswithValue(node.input_delete.content.Molecule.selected_model, restore=True)
 
    def edge_from_variant(self, data:dict):
        start_node = self.frame.scene.findNode(data["start_node.id"])
        if start_node is not None:
            start_socekt = start_node.node_output
        end_node = self.frame.scene.findNode(data["end_node.id"])
        if end_node is not None:
            end_socekt = end_node.node_input
        if start_node is not None and end_node is not None:
            edge = Edge(self.frame.scene, start_socekt, end_socekt)


    def saveSession(self) -> dict:
        data = {}
        data["settings.model_residues"] = self.frame.settings_menu.model_residues
        data["settings.model_atoms"] = self.frame.settings_menu.model_atoms
        data["settings.model_hetero"] = self.frame.settings_menu.model_hetero
        data["settings.model_water"] = self.frame.settings_menu.model_water
        data["settings.model_refresh"] = self.frame.settings_menu.model_refresh
        data["settings.save_script_folder"] = self.frame.settings_menu.save_script_folder
        data["settings.save_log_folder"] = self.frame.settings_menu.save_log_folder
        data["settings.nodes_transparency_title"] = self.frame.settings_menu.nodes_transparency_title
        data["settings.nodes_transparency_background"] = self.frame.settings_menu.nodes_transparency_background
        data["settings.command_delay"] = self.frame.settings_menu.command_delay
        data["settings.allow_info_link"] = self.frame.settings_menu.allow_info_link
        data["settings.grid_squares"] = self.frame.settings_menu.grid_squares
        data["settings.grid_size"] = self.frame.settings_menu.grid_size
        data["settings.grid_snap"] = self.frame.settings_menu.grid_snap
        data["settings.viewer_refresh"] = self.frame.settings_menu.viewer_refresh
        data["log"] = self.frame.log

        data["style_mode"] = self.frame.theme_toggle.isChecked()
        data["simple_mode"] = self.frame.simple_mode
        data["scene.nodes_id"] = self.frame.scene.nodes_id
        center_point = QPoint(self.frame.view.pos().x() + int(self.frame.view.width() / 2), self.frame.view.pos().y() + int(self.frame.view.height() / 2))
        data["scene.x"] = self.frame.view.mapToScene(center_point).x()
        data["scene.y"] = self.frame.view.mapToScene(center_point).y()
        data["view.zoom"] = self.frame.view.zoom
        data["view.total_scale"] = self.frame.view.total_scale
        data["copy_selected_model_objects"] = self.frame.copy_selected_model_objects
        data["copy_selected_color_objects"] = self.frame.copy_selected_color_objects
        data["copy_selected_center_objects"] = self.frame.copy_selected_center_objects
        data["copy_selected_view_objects"] = self.frame.copy_selected_view_objects
        data["copy_selected_fly_objects"] = self.frame.copy_selected_fly_objects
        data["copy_selected_fly_objects_transition_frames"] = self.frame.copy_selected_fly_objects_transition_frames
        data["copy_selected_label2D_objects"] = self.frame.copy_selected_label2D_objects
        data["copy_selected_label3D_objects"] = self.frame.copy_selected_label3D_objects
        nodes_list = []
        for node in self.frame.scene.nodes:
            node_dict = self.node_to_variant(node)
            if node_dict:
                nodes_list.append(node_dict)
        edges_list = []
        for edge in self.frame.scene.edges:
            edge_dict = self.edge_to_variant(edge)
            if edge_dict:
                edges_list.append(edge_dict)
        data["nodes"] = nodes_list
        data["edges"] = edges_list
        return data

    def loadSession(self, data:dict[str,]):
        self.frame.settings_menu.model_residues = data["settings.model_residues"]
        self.frame.settings_menu.model_atoms = data["settings.model_atoms"]
        self.frame.settings_menu.model_hetero = data["settings.model_hetero"]
        self.frame.settings_menu.model_water = data["settings.model_water"]
        self.frame.settings_menu.model_refresh = float(data["settings.model_refresh"])
        self.frame.settings_menu.save_script_folder = data["settings.save_script_folder"]
        self.frame.settings_menu.save_log_folder = data["settings.save_log_folder"]
        self.frame.settings_menu.nodes_transparency_title = int(data["settings.nodes_transparency_title"])
        self.frame.settings_menu.nodes_transparency_background = int(data["settings.nodes_transparency_background"])
        self.frame.settings_menu.command_delay = float(data["settings.command_delay"])
        self.frame.log = data["log"]
        self.frame.settings_menu.allow_info_link = bool(data["settings.allow_info_link"])
        self.frame.settings_menu.grid_squares = int(data["settings.grid_squares"])
        self.frame.settings_menu.grid_size = int(data["settings.grid_size"])
        self.frame.settings_menu.grid_snap = bool(data["settings.grid_snap"])
        self.frame.settings_menu.viewer_refresh = float(data["settings.viewer_refresh"])

        self.frame.theme_toggle.setChecked(data["style_mode"])
        self.frame.simple_mode = not data["simple_mode"]
        self.frame.ToggleMode()

        self.frame.scene.nodes_id = data["scene.nodes_id"]
        self.frame.centerOn(float(data["scene.x"]), float(data["scene.y"]))
        self.frame.view.zoom = data["view.zoom"]
        self.frame.view.total_scale = data["view.total_scale"]
        self.frame.view.scale(self.frame.view.total_scale, self.frame.view.total_scale)
        self.frame.copy_selected_model_objects = data["copy_selected_model_objects"]
        self.frame.copy_selected_color_objects = data["copy_selected_color_objects"]
        self.frame.copy_selected_center_objects = data["copy_selected_center_objects"]
        self.frame.copy_selected_view_objects = data["copy_selected_view_objects"]
        self.frame.copy_selected_fly_objects = data["copy_selected_fly_objects"]
        self.frame.copy_selected_fly_objects_transition_frames = data["copy_selected_fly_objects_transition_frames"]
        self.frame.copy_selected_label2D_objects = data["copy_selected_label2D_objects"]
        self.frame.copy_selected_label3D_objects = data["copy_selected_label3D_objects"]

        for node in data["nodes"]:
            self.node_from_variant(node)
        for edge in data["edges"]:
            self.edge_from_variant(edge)

        chain_start:list[Node] = []
        for edge in self.frame.scene.edges:
            starting_node = edge.start_socket.node.nodeID
            if starting_node not in [e.end_socket.node.nodeID for e in self.frame.scene.edges]:
                chain_start.append(edge.start_socket.node)
        for node in chain_start:
            node.summary.updateOutputValues(check_update=False)
        
    def take_snapshot(self, session, flags) -> dict[str,]:
        return {
            'version': 1,
            'data': self.saveSession()
        }

    @classmethod
    def restore_snapshot(class_obj, session, data:dict[str,]):
        # Instead of using a fixed string when calling the constructor below, we could
        # have saved the tool name during take_snapshot() (from self.tool_name, inherited
        # from ToolInstance) and used that saved tool name.  There are pros and cons to
        # both approaches.
        inst = class_obj(session, "MovieMaker")
        inst.loadSession(data["data"])
        return inst
        