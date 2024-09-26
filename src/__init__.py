# vim: set expandtab shiftwidth=4 softtabstop=4:

from chimerax.core.toolshed import BundleAPI

# Subclass from chimerax.core.toolshed.BundleAPI and
# override the method for registering commands,
# inheriting all other methods from the base class.

class _MyAPI(BundleAPI):
    api_version = 1     # start_tool called with BundleInfo and
                        # ToolInfo instance (vs. BundleInfo and
                        # tool name when api_version==0 [the default])

    # Override method

    @staticmethod
    def start_tool(session, bi, ti):
        # session is an instance of chimerax.core.session.Session
        # bi is an instance of chimerax.core.toolshed.BundleInfo
        # ti is an instance of chimerax.core.toolshed.ToolInfo

        # This method is called once for each time the tool is invoked.

        # We check the name of the tool, which should match one of the
        # ones listed in bundle_info.xml (without the leading and
        # trailing whitespace), and create and return an instance of the
        # appropriate class from the ``tool`` module.
        if ti.name == "MovieMaker":
            from . import main
            return main.MovieMaker(session, ti.name)
        raise ValueError("trying to start unknown tool: %s" % ti.name)

    @staticmethod
    def get_class(class_name):
        # class_name will be a string
        from . import main, main_window, node_base, sockets, edges, enum_classes
        if class_name == "MovieMaker":
            return main.MovieMaker
        elif class_name == "NodeEditor":
            return main_window.NodeEditor
        elif class_name == "Node":
            return node_base.Node
        elif class_name == "Socket":
            return sockets.Socket
        elif class_name == "Edge":
            return edges.Edge
        elif class_name == "NodeType":
            return enum_classes.NodeType
        elif class_name == "NodePickerType":
            return enum_classes.NodePickerType
        elif class_name == "Position":
            return enum_classes.Position
        elif class_name == "SocketType":
            return enum_classes.SocketType
        elif class_name == "TempEdgeType":
            return enum_classes.TempEdgeType
        raise ValueError("Unknown class name '%s'" % class_name)


# Create the ``bundle_api`` object that ChimeraX expects.
bundle_api = _MyAPI()
