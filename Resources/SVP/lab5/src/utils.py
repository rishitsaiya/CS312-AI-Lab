class Point(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.value = float('inf')
        self.parent = None
        
    def distance(self, other):
        delX, delY = self.x - other.x, self.y - other.y
        return ( delX**2 + delY**2 )**0.5