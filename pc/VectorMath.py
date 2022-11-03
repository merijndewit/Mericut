def Lerp(node0, node1, t):
    x = (t * node0[0]) + ((1-t) * node1[0])
    y = (t * node0[1]) + ((1-t) * node1[1])
    return [x, y]

def QuadraticBezier(node0, node1, node2, t):
	point0 = Lerp(node0, node1, t)
	point1 = Lerp(node1, node2, t)
	return Lerp(point0, point1, t)
	
