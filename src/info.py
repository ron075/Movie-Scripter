from __future__ import annotations

from typing import TYPE_CHECKING
from .enum_classes import *

if TYPE_CHECKING:
    from .node import Node

class Info():
    def set_info(self, node:Node=None) -> str:
        formal_help_str = f""
        simple_help_str = f""
        if node is not None:
            if NodeType(node.nodeType) == NodeType.Start:
                    formal_help_str = f"Record controls general scene and window settings(e.g. background color, window width, window height, etc...)"
                    simple_help_str = f"Record controls and eneral scene and window settings(e.g. background color, window width, window height, etc...)"
            elif NodeType(node.nodeType) == NodeType.End:
                    formal_help_str = f"Movie file attributes (e.g. name, sufix, framerate, etc...)"
                    simple_help_str = f"Movie file attributes (e.g. name, sufix, framerate, etc...)"
            elif NodeType(node.nodeType) == NodeType.ColorPalette:
                    formal_help_str = f"https://www.cgl.ucsf.edu/chimerax/docs/user/commands/color.html"
                    simple_help_str = f"This node allow manipulation of model coloring"
            elif NodeType(node.nodeType) == NodeType.Lighting:
                    formal_help_str = f"The lighting command controls global lighting parameters, through individual options and in convenient preset combinations"
                    simple_help_str = f"This node allow manipulation of scene lighting based on ChimeraX base light schemes"
            elif NodeType(node.nodeType) == NodeType.Transparency:
                    formal_help_str = f"The transparency command sets the transparency of atomic representations, molecular surfaces, and volume (map) isosurfaces to the specified percent, where 0% is completely opaque and 100% is completely transparent, without otherwise changing colors"
                    simple_help_str = f"Controls the transparency of the model surface, cartoon or atoms, and the atom style. Fully visible = 0, fully transparent = 100"
            elif NodeType(node.nodeType) == NodeType.Label2D:
                    formal_help_str = f"The 2dlabels command adds text, symbols, and straight arrows to the display for presentation-quality images and movies. These 2D labels exist in the X,Y plane of the screen and do not move along with the 3D scene"
                    simple_help_str = f"Add of a custom 2D label to the scene"
            elif NodeType(node.nodeType) == NodeType.Label3D:
                    formal_help_str = f"The label command shows labels that move along with the associated items in 3D. These “3D” (although flat in appearance) labels can be of multiple colors and sizes. A label is automatically hidden, however, when the corresponding item is hidden"
                    simple_help_str = f"Add of a custom 3D label to a model"
            elif NodeType(node.nodeType) == NodeType.Movement:
                    formal_help_str = f"The move command translates the specified models or atoms by distance along axis at each of a specified number of image update frames (default 1 frame). The move cofr command translates the specified models collectively (without changing their positions relative to one another) to center their bounding box at the current center of rotation. Only displayed parts are used to compute the bounding box. "
                    simple_help_str = f"Move a model on the scene XYZ coordinates system or to the center of the scene"
            elif NodeType(node.nodeType) == NodeType.Rotation:
                    formal_help_str = f"The turn command performs a rotation of angle around a specified axis  at each of a specified number of image update frames. The commands turn and roll are the same except for their default values of angle and frames"
                    simple_help_str = f"Rotate a model around the scene or its own XYZ coordinates system"
            elif NodeType(node.nodeType) == NodeType.Wait:
                    formal_help_str = f"The wait command updates the display for a specified number of wait-frames before allowing execution of the next command in a script"
                    simple_help_str = f"Delays the exceution of the next command in the movie"
            elif NodeType(node.nodeType) == NodeType.Crossfade:
                    formal_help_str = f"The crossfade command fades the current display image over a specified number of subsequent frames"
                    simple_help_str = f"Applies crossfade to all nodes between this node and the next wait node"
            elif NodeType(node.nodeType) == NodeType.CenterRotation:
                    formal_help_str = f"Cofr reports the coordinates of the current center of rotation in the laboratory frame of reference. The center can be shown with “+” crosshairs"
                    simple_help_str = f"Calculates the Center of Roatation (cofr) based on the desired function"
            elif NodeType(node.nodeType) == NodeType.CenterMass:
                    formal_help_str = f"https://www.cgl.ucsf.edu/chimerax/docs/user/commands/measure.html"
                    simple_help_str = f"Calculates center of mass of map, atoms, and/or surface. A model can be placed in the center for later use"
            elif NodeType(node.nodeType) == NodeType.View_Save:
                    formal_help_str = f"Save the current view with a name"
                    simple_help_str = f"Save the current view with a name"
            elif NodeType(node.nodeType) == NodeType.View_Load:
                    formal_help_str = f"Focuses the view on a saved view, specified items or “all”"
                    simple_help_str = f"Focuses the view on a saved view, specified items or “all”"
            elif NodeType(node.nodeType) == NodeType.Fly:
                    formal_help_str = f"Fly uses cubic interpolation to smoothly traverse a series of views previously named and saved with view name. The view command can also interpolate between views, but it only considers a pair of views (start and end) at a time, whereas fly can consider multiple views and generate a path that visits and leaves intermediate views without discontinuities in motion. However, fly does not interpolate clipping plane positions, whereas view does."
                    simple_help_str = f"Flys through a set of picked views or models"
            elif NodeType(node.nodeType) == NodeType.Delete:
                    formal_help_str = f"The delete command deletes the specified type of object"
                    simple_help_str = f"Deletes the specified type of object: Model, 2D label, 3D label or view"
            elif NodeType(node.nodeType) == NodeType.Summary:
                    formal_help_str = f""
                    simple_help_str = f""
            elif NodeType(node.nodeType) == NodeType.Split:
                    formal_help_str = f"The split command partitions atomic models into separate submodels in the hierarchy. Splitting parts of a model into separate submodels may facilitate their independent control"
                    simple_help_str = f"Split an existing model based on user preference"
            elif NodeType(node.nodeType) == NodeType.Picker:
                if NodePickerType(node.nodePickerType) == NodePickerType.ModelPicker:
                    formal_help_str = f"Pick a model for the node to use"
                    simple_help_str = f"Pick a model for the node to use"
                elif NodePickerType(node.nodePickerType) == NodePickerType.ColorPicker:
                    formal_help_str = f"Pick groups for the node to use. If applying colors, the coloring of each group will appear in the node"
                    simple_help_str = f"Pick groups for the node to use. If applying colors, the coloring of each group will appear in the node"
                elif NodePickerType(node.nodePickerType) == NodePickerType.CenterPicker:
                    formal_help_str = f"Pick a model for the node to use"
                    simple_help_str = f"Pick a model for the node to use"
                elif NodePickerType(node.nodePickerType) == NodePickerType.ViewPicker:
                    formal_help_str = f"Pick a view for the node to use"
                    simple_help_str = f"Pick a view for the node to use"
                elif NodePickerType(node.nodePickerType) == NodePickerType.FlyPicker:
                    formal_help_str = f"Pick groups of models or views for the node to use"
                    simple_help_str = f"Pick groups of models or views for the node to use"
                elif NodePickerType(node.nodePickerType) == NodePickerType.DeletePicker:
                    formal_help_str = f"Pick a model, 2D label, 3D label or a view for the node to delete"
                    simple_help_str = f"Pick a model, 2D label, 3D label or a view for the node to delete"
        return [simple_help_str, formal_help_str]