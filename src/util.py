from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *

class CustomQWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

class CustomQCheckBox(QCheckBox):
    def __init__(self, parent=None):
        super().__init__(parent)

def changeCursor(item:QObject):
    if type(item) is list:
        for ite in item:
            changeCursor(ite)
    elif type(item) is QTabWidget:
        if item.isEnabled():
            item.tabBar().setCursor(Qt.CursorShape.PointingHandCursor)
        if item.children():
            changeCursor(item.children())
    elif type(item) is QPushButton or type(item) is QComboBox or type(item) is QSlider or isinstance(item, CustomQCheckBox):
        if item.isEnabled():
            item.setCursor(Qt.CursorShape.PointingHandCursor)
        else:
            item.setCursor(Qt.CursorShape.ArrowCursor)
    elif type(item) is QTextEdit or type(item) is QLineEdit:
        if item.isEnabled():
            if item.isReadOnly():
                item.viewport().setCursor(Qt.CursorShape.ArrowCursor)
        else:
            item.setCursor(Qt.CursorShape.ArrowCursor)
    elif type(item) is QWidget or isinstance(item, CustomQWidget) or type(item) is QSplitter or type(item) is QStackedWidget:
        if item.children():
            changeCursor(item.children())
    
def changeEnabled(item:QWidget, state:bool):
    item.setEnabled(state)
    changeCursor(item)

def convertTime(value:int|float) -> str:
    if value < 60:
        return(f"{format(round(value, 2), '.2f')} Seconds")
    else:
        value = value / 60
        if value < 60:
            return(f"{format(round(value, 2), '.2f')} Minutes")
        else:
            value = value / 60
            if value < 24:
                return(f"{format(round(value, 2), '.2f')} Hours")
            else:
                value = value / 24
                return(f"{format(round(value, 2), '.2f')} Days")