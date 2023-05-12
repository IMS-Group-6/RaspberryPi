from collections import namedtuple

class Map:
    def __init__(self):
        self.points = []
        self.hullPoints = []
        self.Point = namedtuple("Point", "x y")

    '''
    Add a point to the map
    '''
    def addPoint(self, x, y):
        self.points.append(self.Point(x, y))

    '''
    Deterine if a triplet of points are colinear, clockwise, or anticlockwise
    '''
    def tripletOrientation(self, p, q, r):
        val = int((q.Y - p.Y) * (r.X - q.X) - (q.X - p.X) * (r.Y - q.Y))
        if val == 0:
            return "Colinear"
        elif val > 0:
            return "Clockwise"
        elif val < 0:
            return "AntiClockwise"

    '''
    Solve the convex hull
    '''
    def convexHull(self):
        n = len(self.points)

        if n < 3:
            return

        leftMost = 0;
        for i in range(1, n):
            if self.points[i].x < self.points[leftMost].x:
                leftMost = i;

        p = leftMost

        hullComplete = False

        while not hullComplete:
            self.hullPoints.Add(self.points[p])

            q = (p + 1) % n

            for i in range(0, n):
                if self.tripletOrientation(self.points[p], self.points[i], self.points[q]) == "AntiClockwise":
                    q = i

            p = q

            if p == leftMost:
                hullComplete = True
