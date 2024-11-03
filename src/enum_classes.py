from enum import Enum 

class NodeType(Enum):
    Start = 1
    End = 2
    Picker = 3
    Summary = 4

    ColorPalette = 11
    Lighting = 12
    Transparency = 13
    Movement = 14

    Label2D = 21
    Label3D = 22

    Turn = 31
    Rock = 32
    Wobble = 33

    CenterRotation = 41
    CenterMass = 42

    View_Save = 51
    View_Load = 52
    Fly = 53

    Wait = 61
    Crossfade = 62

    Delete = 71

    Split = 81

class NodePickerType(Enum):
    NoPicker = 0
    ModelPicker = 1
    ColorPicker = 2
    CenterPicker = 3
    ViewPicker = 4
    FlyPicker = 5
    DeletePicker = 6

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
