import rhinoscriptsyntax as rs
import Rhino

srfs = []


srfCut = rs.GetObject("Select Cutting Surface")
brepPrint = rs.GetObject("Select Object to slice")
intDist = rs.GetInteger("Layer Thickness?", 1)

rs.EnableRedraw(False)

bbSrf = rs.BoundingBox(srfCut)
distSrf = int(round(rs.Distance(bbSrf[0], bbSrf[4])) + 1)

bbBrep = rs.BoundingBox(brepPrint)
distBrep = int(round(rs.Distance(bbBrep[0], bbBrep[4])) + 1)

intOffset = distBrep + distSrf

for i in range(intOffset):
    srfCut = rs.CopyObject(srfCut, (0,0, intDist))
    #xBrepSrf = rs.IntersectBreps(brepPrint, srfCut)
    xBrepSrf = rs.MeshMeshIntersection(brepPrint, srfCut)
    if xBrepSrf:
        for points in xBrepSrf:
            rs.AddPolyline(points)
    srfs.append(srfCut)
    if not xBrepSrf:
        continue
    
rs.DeleteObjects(srfs)
rs.EnableRedraw(True)

