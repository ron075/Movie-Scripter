from __future__ import annotations

from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
import re
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .simple_nodes import SimpleNodeSummary
    from .advanced_nodes import AdvancedNodeSummary

class NodeBase(QWidget):
    def __init__(self, session, summary:SimpleNodeSummary|AdvancedNodeSummary, title:str="", simple_node:bool=True, parent=None):
        super().__init__(parent)
        self.session = session
        self.summary = summary

        if simple_node:
            self.title = title
        else:
            self.title = f"{title}: {self.summary.node.nodeID}"
        self.start_script_string = f""
        self.script_string = f""
        self.end_script_string = f""
        
    def internal_updateRun(self):
        self.updateRun(False)

    def updateRun(self):
        pass

    def startRunCommand(self):
        self.summary.node.scene.parent.command_queue.put(f"movie reset")
        self.runCommand()
        
    def updateCommand(self):
        self.start_script_string = f""
        self.script_string = f""
        self.end_script_string = f""

    def runCommand(self):
        self.updateCommand()
        if self.start_script_string != "":
            command = self.strip_br_tags(self.start_script_string)
            for cmd in command.splitlines():
                self.summary.node.scene.parent.command_queue.put(cmd)
        if self.script_string != "":
            command = self.strip_br_tags(self.script_string)
            for cmd in command.splitlines():
                self.summary.node.scene.parent.command_queue.put(cmd)
        if self.end_script_string != "":
            command = self.strip_br_tags(self.end_script_string)
            for cmd in command.splitlines():
                self.summary.node.scene.parent.command_queue.put(cmd)

    def runCommandChain(self):
        start_point = True
        self.runCommandChainBackward(start_point)
        self.runCommand()
        self.runCommandChainForward(start_point)

    def runCommandChainBackward(self, start_point:bool):
        no_inputs = True
        if self.summary.node.node_input is not None:
            if self.summary.node.node_input.hasEdge():
                no_inputs = False
                self.summary.node.node_input.edge.start_socket.node.content.runCommandChainBackward(start_point = False)
        if no_inputs:
            self.startRunCommand()
        else:
            if not start_point:
                self.runCommand()

    def runCommandChainForward(self, start_point:bool):
        if self.summary.node.node_output is not None:
            if self.summary.node.node_output.hasEdge():
                self.summary.node.node_output.edge.end_socket.node.content.runCommandChainForward(start_point = False)
        if not start_point:
            self.runCommand()

    def deleteNode(self):
        self.summary.node.scene.parent.view.removeNode(self.summary.node)

        
    def strip_br_tags(self, html:str) -> str:
        return html.replace("<br>", "\n")
