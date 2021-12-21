import rhinoscriptsyntax as rs
import random
import itertools

steps = rs.GetInteger("How many candles do you want to make?", 10, 1)
loops = rs.GetInteger("How many loops do you want in the candle?", 10, 1)

distOffset = 250
rs.EnableRedraw(False)
    
for i in range(steps):
    crvs = []
    heights = []
    s = 0
    height2 = []
    for j in range(loops):
        height = random.randint(20,40)
        heights.append(height)
    
    for n in heights:
        s = s + n
        height2.append(s)
    heights = height2

    for j in range(loops):
        radius = random.randint(50, 90)
        point = (0,i*distOffset, heights[j])
        crv = rs.AddCircle(point, radius/2)
        crvs.append(crv)
    loft = rs.AddLoftSrf(crvs)
    rs.DeleteObjects(crvs)
rs.EnableRedraw(True)

