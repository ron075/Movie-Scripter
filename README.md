# Movie-Scripter
A GUI tool for ChimeraX, for script production

To install it you need to go into ChemiraX and write: "toolshed install "C:\Users\UserName \Desktop\A\MovieMaker-0.3-py3-none-any.whl" " (Change the path as needed to reach where you have put the file). After installing, you can open the tool by clicking on Tools->Movie->MovieMaker.

The Grid: The grid contains the scene (nodes – ChimeraX commands, and edges – links between one command to the next)

Mouse Controls: Right clicking on the grid will open a menu from which you can create different nodes Left click on node/edge - will select the node or edge, mark their inputs and outputs, and open the node card (from which you can edit the command) Left click on node/edge –moves the grid Left clicking while holding control – removing the node or the edges that are clicked (some edges and nodes can't be removed) Mouse Wheel – zoom in or out

Nodes: Each node has one main input (red) and output (green). Additionally, some nodes will have special inputs (model selection – yellow, selecting groups for coloring – light blue, selecting views – orange, selecting center (e.g for rotation) – pink, selecting views for fly command (fly sequence between multiple views) – purple, picking models/labels/views for deletion – dark gray) The value used in the special input can be passed through the chain of nodes (nodes inherit the values from previous nodes). On the node card (unselected node), there are toggles for each special input. If the toggle is turned on (blue), it will not inherit the value, and the user will need to pick it. If the toggle is off (gray) it will inherit the value. Each node type has different contents based on the command that it implements.

Attached is the whl file you need to install in chimeraX
