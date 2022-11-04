from svg.path import parse_path
from svg.path.path import Line, CubicBezier, QuadraticBezier
from xml.dom import minidom

import UI.Nodes as Nodes
import UI.DrawingShapes as DrawingShapes

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

                line = DrawingShapes.Line([node0, node1], canvas)
                canvas.drawnShapes.append(line)

            if isinstance(object, QuadraticBezier):
                node0 = Nodes.Node(object.start.real, object.start.imag)
                node1 = Nodes.Node(object.control.real, object.control.imag)
                node2 = Nodes.Node(object.end.real, object.end.imag)

                curve = DrawingShapes.QuadraticBezier(canvas, [node0, node1, node2])
                canvas.drawnShapes.append(curve)

            if isinstance(object, CubicBezier):
                node0 = Nodes.Node(object.start.real, object.start.imag)
                node1 = Nodes.Node(object.control1.real, object.control1.imag)
                node2 = Nodes.Node(object.control2.real, object.control2.imag)
                node3 = Nodes.Node(object.end.real, object.end.imag)

                curve = DrawingShapes.CubicBezier(canvas, [node0, node1, node2, node3])
                canvas.drawnShapes.append(curve)

            

