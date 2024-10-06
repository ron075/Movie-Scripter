from enum import Enum 

class NodeType(Enum):
    Start = -1
    End = -2

    ColorPalette = 1
    Lighting = 2
    Transparency = 3
    Label2D = 4
    Label3D = 5
    Movement = 6
    Rotation = 7
    Wait = 8
    Crossfade = 9
    Picker = 10
    CenterRotation = 11
    CenterMass = 12
    View_Save = 13
    View_Load = 14
    Fly = 15
    Delete = 16
    Summary = 17
    Split = 18

class NodePickerType(Enum):
    NoPicker = 0
    ModelPicker = 1
    ColorPicker = 2
    CenterPicker = 3
    ViewPicker = 4
    FlyPicker = 5
    DeletePicker = 6
    SplitPicker = 7

class Position(Enum):
    LEFT_TOP = 1
    LEFT_BOTTOM = 2
    RIGHT_TOP = 3
    RIGHT_BOTTOM = 4

class SocketType(Enum):
    DISABLED_SOCKET = 0
    INPUT_SOCKET = 1
    OUTPUT_SOCKET = 2
    MODEL_SOCKET = 3
    COLOR_SOCKET = 4
    CENTER_SOCKET = 5
    VIEW_SOCKET = 6
    FLY_SOCKET = 7
    DELETE_SOCKET = 8
    
class TempEdgeType(Enum):
    NONE = 1
    SOURCE = 2
    DESTINATION = 3

class ToolStatus(Enum):
    RUNNING = 1
    TERMINATING = 2

class ColorRangeType(Enum):
    Simple = 0
    Expert = 1
