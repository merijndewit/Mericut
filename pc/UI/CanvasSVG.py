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
    scale = 0.10
    yOffset = 0

    for path_string in path_strings:
        path = parse_path(path_string)
        for object in path:
            if isinstance(object, Line):
                node0 = Nodes.Node(object.start.real * scale, (object.start.imag * scale) - yOffset, canvas.selectedLayer)
                node1 = Nodes.Node(object.end.real * scale, (object.end.imag * scale) - yOffset, canvas.selectedLayer)

                line = DrawingShapes.Line([node0, node1], canvas)
                canvas.selectedLayer.drawnShapes.append(line)
                continue

            if isinstance(object, QuadraticBezier):
                node0 = Nodes.Node(object.start.real * scale, object.start.imag * scale - yOffset, canvas.selectedLayer)
                node1 = Nodes.Node(object.control.real * scale, object.control.imag * scale - yOffset, canvas.selectedLayer)
                node2 = Nodes.Node(object.end.real * scale, object.end.imag * scale - yOffset, canvas.selectedLayer)

                curve = DrawingShapes.QuadraticBezier(canvas, [node0, node1, node2])
                canvas.selectedLayer.drawnShapes.append(curve)
                continue

            if isinstance(object, CubicBezier):
                node0 = Nodes.Node(object.start.real * scale, object.start.imag * scale - yOffset, canvas.selectedLayer)
                node1 = Nodes.Node(object.control1.real * scale, object.control1.imag * scale - yOffset, canvas.selectedLayer)
                node2 = Nodes.Node(object.control2.real * scale, object.control2.imag * scale - yOffset, canvas.selectedLayer)
                node3 = Nodes.Node(object.end.real * scale, object.end.imag * scale - yOffset, canvas.selectedLayer)

                curve = DrawingShapes.CubicBezier(canvas, [node0, node1, node2, node3])
                canvas.selectedLayer.drawnShapes.append(curve)
                continue
