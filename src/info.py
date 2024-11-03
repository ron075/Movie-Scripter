from __future__ import annotations

from typing import TYPE_CHECKING
from .enum_classes import *

if TYPE_CHECKING:
    from .node import Node

class Info():
    def set_info(self, node:Node=None) -> tuple[str, str]:
        link = f""
        info = f""
        if node is not None:
            if NodeType(node.nodeType) == NodeType.Start:
                    link = f"https://www.cgl.ucsf.edu/chimerax/docs/user/commands/movie.html"
                    info = f"Record controls and eneral scene and window settings(e.g. background color, window width, window height, etc...)"
            elif NodeType(node.nodeType) == NodeType.End:
                    link = f"https://www.cgl.ucsf.edu/chimerax/docs/user/commands/movie.html"
                    info = f"Movie file attributes (e.g. name, sufix, framerate, etc...)"
            elif NodeType(node.nodeType) == NodeType.ColorPalette:
                    link = f"https://www.cgl.ucsf.edu/chimerax/docs/user/commands/color.html"
                    info = f"This node allow manipulation of model coloring"
            elif NodeType(node.nodeType) == NodeType.Lighting:
                    link = f"https://www.cgl.ucsf.edu/chimerax/docs/user/commands/lighting.html"
                    info = f"This node allow manipulation of scene lighting based on ChimeraX base light schemes"
            elif NodeType(node.nodeType) == NodeType.Transparency:
                    link = f"https://www.cgl.ucsf.edu/chimerax/docs/user/commands/transparency.html"
                    info = f"Controls the transparency of the model surface, cartoon or atoms, and the atom style. Fully visible = 0, fully transparent = 100"
            elif NodeType(node.nodeType) == NodeType.Label2D:
                    link = f"https://www.cgl.ucsf.edu/chimerax/docs/user/commands/2dlabels.html"
                    info = f"Add of a custom 2D label to the scene"
            elif NodeType(node.nodeType) == NodeType.Label3D:
                    link = f"https://www.cgl.ucsf.edu/chimerax/docs/user/commands/label.html"
                    info = f"Add of a custom 3D label to a model"
            elif NodeType(node.nodeType) == NodeType.Movement:
                    link = f"https://www.cgl.ucsf.edu/chimerax/docs/user/commands/move.html"
                    info = f"Move a model on the scene XYZ coordinates system or to the center of the scene"
            elif NodeType(node.nodeType) == NodeType.Turn:
                    link = f"https://www.cgl.ucsf.edu/chimerax/docs/user/commands/turn.html"                    
                    info = f"Rotate a model around the scene or its own XYZ coordinates system"
            elif NodeType(node.nodeType) == NodeType.Rock:
                    link = f"https://www.cgl.ucsf.edu/chimerax/docs/user/commands/rock.html"                    
                    info = f"Rotate a model around the scene or its own XYZ coordinates system"
            elif NodeType(node.nodeType) == NodeType.Wobble:
                    link = f"https://www.cgl.ucsf.edu/chimerax/docs/user/commands/wobble.html"                    
                    info = f"Rotate a model around the scene or its own XYZ coordinates system"
            elif NodeType(node.nodeType) == NodeType.Wait:
                    link = f"https://www.cgl.ucsf.edu/chimerax/docs/user/commands/wait.html"
                    info = f"Delays the exceution of the next command in the movie"
            elif NodeType(node.nodeType) == NodeType.Crossfade:
                    link = f"https://www.cgl.ucsf.edu/chimerax/docs/user/commands/crossfade.html"
                    info = f"Applies crossfade to all nodes between this node and the next wait node"
            elif NodeType(node.nodeType) == NodeType.CenterRotation:
                    link = f"https://www.cgl.ucsf.edu/chimerax/docs/user/commands/cofr.html"
                    info = f"Calculates the Center of Roatation (cofr) based on the desired function"
            elif NodeType(node.nodeType) == NodeType.CenterMass:
                    link = f"https://www.cgl.ucsf.edu/chimerax/docs/user/commands/measure.html"
                    info = f"Calculates center of mass of map, atoms, and/or surface. A model can be placed in the center for later use"
            elif NodeType(node.nodeType) == NodeType.View_Save:
                    link = f"https://www.cgl.ucsf.edu/chimerax/docs/user/commands/view.html"
                    info = f"Save the current view with a name"
            elif NodeType(node.nodeType) == NodeType.View_Load:
                    link = f"https://www.cgl.ucsf.edu/chimerax/docs/user/commands/view.html"
                    info = f"Focuses the view on a saved view, specified items or “all”"
            elif NodeType(node.nodeType) == NodeType.Fly:
                    link = f"https://www.cgl.ucsf.edu/chimerax/docs/user/commands/fly.html"                    
                    info = f"Flys through a set of picked views or models"
            elif NodeType(node.nodeType) == NodeType.Delete:
                    link = f"https://www.cgl.ucsf.edu/chimerax/docs/user/commands/delete.html"
                    info = f"Deletes the specified type of object: Model, 2D label, 3D label or view"
            elif NodeType(node.nodeType) == NodeType.Summary:
                    link = f""
                    info = f""
            elif NodeType(node.nodeType) == NodeType.Split:
                    link = f"https://www.cgl.ucsf.edu/chimerax/docs/user/commands/split.html"
                    info = f"Split an existing model based on user preference"
            elif NodeType(node.nodeType) == NodeType.Picker:
                if NodePickerType(node.nodePickerType) == NodePickerType.ModelPicker:
                    link = f""
                    info = f"Pick a model for the node to use"
                elif NodePickerType(node.nodePickerType) == NodePickerType.ColorPicker:
                    link = f""
                    info = f"Pick groups for the node to use. If applying colors, the coloring of each group will appear in the node"
                elif NodePickerType(node.nodePickerType) == NodePickerType.CenterPicker:
                    link = f""
                    info = f"Pick a model for the node to use"
                elif NodePickerType(node.nodePickerType) == NodePickerType.ViewPicker:
                    link = f""
                    info = f"Pick a view for the node to use"
                elif NodePickerType(node.nodePickerType) == NodePickerType.FlyPicker:
                    link = f""
                    info = f"Pick groups of models or views for the node to use"
                elif NodePickerType(node.nodePickerType) == NodePickerType.DeletePicker:
                    link = f""
                    info = f"Pick a model, 2D label, 3D label or a view for the node to delete"
        return info, link