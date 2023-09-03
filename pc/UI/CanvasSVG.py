from svg.path import parse_path
from xml.dom import minidom


import UI.Nodes as Nodes
import UI.DrawingShapes as DrawingShapes
from UI.Layer import Layer

def LoadSVG(canvas, dir):
    from svg.path.path import Line, CubicBezier, QuadraticBezier, Arc
    doc = minidom.parse(dir)
    path_strings = [path.getAttribute('d') for path
                    in doc.getElementsByTagName('path')]
    doc.unlink()
    scale = 0.50
    yOffset = 0

    for path_string in path_strings:
        path = parse_path(path_string)
        for object in path:
            if isinstance(object, Line):
                node0 = Nodes.Node(object.start.real * scale, (object.start.imag * scale) - yOffset)
                node1 = Nodes.Node(object.end.real * scale, (object.end.imag * scale) - yOffset)

                line = DrawingShapes.Line([node0, node1], canvas)
                canvas.selectedLayer.AddShape(line)
                continue

            if isinstance(object, QuadraticBezier):
                node0 = Nodes.Node(object.start.real * scale, object.start.imag * scale - yOffset)
                node1 = Nodes.Node(object.control.real * scale, object.control.imag * scale - yOffset)
                node2 = Nodes.Node(object.end.real * scale, object.end.imag * scale - yOffset)

                curve = DrawingShapes.QuadraticBezier(canvas, [node0, node1, node2])
                canvas.selectedLayer.AddShape(curve)
                continue

            if isinstance(object, CubicBezier):
                node0 = Nodes.Node(object.start.real * scale, object.start.imag * scale - yOffset)
                node1 = Nodes.Node(object.control1.real * scale, object.control1.imag * scale - yOffset)
                node2 = Nodes.Node(object.control2.real * scale, object.control2.imag * scale - yOffset)
                node3 = Nodes.Node(object.end.real * scale, object.end.imag * scale - yOffset)

                curve = DrawingShapes.CubicBezier(canvas, [node0, node1, node2, node3])
                canvas.selectedLayer.AddShape(curve)
                continue

            if isinstance(object, Arc):
                node0 = Nodes.Node(object.start.real * scale, object.start.imag * scale - yOffset)
                node1 = Nodes.Node(object.center * scale, object.center.imag * scale - yOffset)
                node2 = Nodes.Node(object.end.real * scale, object.end.imag * scale - yOffset)
                arc = DrawingShapes.Arc(canvas, [node0, node1, node2])
                canvas.selectedLayer.AddShape(arc)
                continue

def SaveSVG(canvas):
    from svgpathtools import Path, Line, QuadraticBezier, CubicBezier, Arc, paths2svg
    pathSegments = []
    path = Path()
    for i in range(len(canvas.layers)):
        layer :Layer = canvas.layers[i]
        for shape in range(len(layer.drawnShapes)):
            if isinstance(layer.drawnShapes[shape], DrawingShapes.Line):
                startPosition = layer.drawnShapes[shape].nodes[0].GetPosition()
                endPosition = layer.drawnShapes[shape].nodes[1].GetPosition()
                line = Line(complex(startPosition[0], startPosition[1]), complex(endPosition[0], endPosition[1]))
                path.append(line)
            if isinstance(layer.drawnShapes[shape], DrawingShapes.QuadraticBezier):
                startPosition = layer.drawnShapes[shape].nodes[0].GetPosition()
                controlPosition = layer.drawnShapes[shape].nodes[1].GetPosition()
                endPosition = layer.drawnShapes[shape].nodes[2].GetPosition()
                line = QuadraticBezier(complex(startPosition[0], startPosition[1]), complex(controlPosition[0], controlPosition[1]), complex(endPosition[0], endPosition[1]))
                path.append(line)
            if isinstance(layer.drawnShapes[shape], DrawingShapes.CubicBezier):
                startPosition = layer.drawnShapes[shape].nodes[0].GetPosition()
                control0Position = layer.drawnShapes[shape].nodes[1].GetPosition()
                control1Position = layer.drawnShapes[shape].nodes[2].GetPosition()
                endPosition = layer.drawnShapes[shape].nodes[3].GetPosition()
                line = CubicBezier(complex(startPosition[0], startPosition[1]), complex(control0Position[0], control0Position[1]), complex(control1Position[0], control1Position[1]), complex(endPosition[0], endPosition[1]))
                path.append(line)

    paths2svg.disvg(path, filename="test.svg", openinbrowser=False)
