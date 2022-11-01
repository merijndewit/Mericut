from svg.path import parse_path
from svg.path.path import Line
from xml.dom import minidom

import UI.Nodes as Nodes
import UI.CanvasShapes as CanvasShapes

def LoadSVG(canvas):
    doc = minidom.parse('Test/svg.svg')
    path_strings = [path.getAttribute('d') for path
                    in doc.getElementsByTagName('path')]
    doc.unlink()

    for path_string in path_strings:
        path = parse_path(path_string)
        for object in path:
            if isinstance(object, Line):
                node0 = Nodes.Node(object.start.real, object.start.imag)
                node1 = Nodes.Node(object.end.real, object.end.imag)

                line = CanvasShapes.Line([node0, node1], canvas)
                canvas.drawnShapes.append(line)
