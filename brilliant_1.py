import numpy as np
import math

class Line:
    #the line is defined as ax + by = c
    def __init__(self, a,b,c):
        self.a = a
        self.b = b
        self.c = c
        self.matrix = np.array([self.a, self.b])

    
        
    def intersect(self, other):
        a = np.array([[self.a, self.b],[other.a, other.b]])
        b = np.array([self.c, other.c])
        res = np.linalg.solve(a,b)
        return res

        
    def pointIsOnLine(self, point):
        return np.allclose(np.dot(self.matrix, point), self.b)

    def pointOffset(self, point):
        return self.a*point[0]+self.b*point[1] - self.c
    

    def __str__(self):
        return "{:2.2}x + {:2.2}y = {:2.2}".format(self.a, self.b, self.c)
    @staticmethod
    def lineFromParametre(point, angle):
        x1 = point[0]
        x2 = point[1]
        return Line(-np.sin(angle), np.cos(angle),
                    -np.sin(angle)*x1+np.cos(angle)*x2)

def mirrorRight(angle):
    alpha = np.radians(210)
    return 2*alpha - angle - np.radians(180)

def mirrorLeft(angle):
    alpha = np.radians(-30)
    return 2*alpha - angle - np.radians(180)

mirrors = [mirrorLeft, mirrorRight, mirrorLeft, mirrorLeft]

leftLine = Line(-np.sqrt(3), 1, np.sqrt(3)/2)
rightLine = Line(np.sqrt(3), 1, np.sqrt(3)/2)
bottomLine = Line(0, 1, 0)
lines = [leftLine, rightLine, bottomLine, bottomLine]

pointOne = np.array([0,  math.sqrt(3)/6])
angleOne = np.radians(97.589089)



def advance():
    nextRay = Line.lineFromParametre(visited[-1][0], visited[-1][1])
    nextPoint = lines[len(visited)-1].intersect(nextRay)
    nextAngle = mirrors[len(visited)-1](visited[-1][1])
    visited.append([nextPoint, nextAngle])

visited = [(pointOne, angleOne)]


while len(visited)<5:
    advance()

for n,x in enumerate(visited):
    print("{}: Point: {},{:4.4} Angle: {:4}".format(n, x[0][0], x[0][1],
                                                          np.degrees(x[1])%360))
                                        
                                        
print("res", 1/3+2*(60-7.589)/180+3*7.589/180)
