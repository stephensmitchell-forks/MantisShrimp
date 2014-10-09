#Copyright(c) 2014, Konrad Sobon
# @arch_laboratory, http://archi-lab.net

import clr
import sys
clr.AddReference('ProtoGeometry')

RhinoCommonPath = r'C:\Program Files\Rhinoceros 5 (64-bit)\System'
if RhinoCommonPath not in sys.path:
	sys.path.Add(RhinoCommonPath)
clr.AddReferenceToFileAndPath(RhinoCommonPath + r"\RhinoCommon.dll")

pyt_path = r'C:\Program Files (x86)\IronPython 2.7\Lib'
sys.path.append(pyt_path)

from Autodesk.DesignScript.Geometry import *
import Rhino as rc

from System import Array
from System.Collections.Generic import *

#The inputs to this node will be stored as a list in the IN variable.
dataEnteringNode = IN
rhObjects = IN[0]

#point/control point conversion function
def rhPointToPoint(rhPoint):
	try:
		rhPoint = rhPoint.Geometry
	except:
		pass
	rhPointX = rhPoint.Location.X
	rhPointY = rhPoint.Location.Y
	rhPointZ = rhPoint.Location.Z
	dsPoint = Point.ByCoordinates(rhPointX, rhPointY, rhPointZ)
	return dsPoint

#NurbsCurve conversion function
#Ellipse is considered NurbsCurve so it will be processed here
def rhCurveToNurbsCurve(rhCurve):
	try:
		rhCurve = rhCurve.Geometry
	except:
		pass
	if rhCurve.HasNurbsForm() == float(1):
		rhCurve = rhCurve.ToNurbsCurve()
		#get control points
		ptArray, weights = [], []
		knots = []
		rhControlPoints = rhCurve.Points
		for rhPoint in rhControlPoints:
			dsPoint = rhPointToPoint(rhPoint)
			ptArray.append(dsPoint)
			#get weights for each point
			weights.append(rhPoint.Weight)
		#convert Python list to IEnumerable[]
		ptArray = List[Point](ptArray)
		weights = Array[float](weights)
		#get degree of the curve
		degree = rhCurve.Degree
		#get knots of the curve
		rhKnots = rhCurve.Knots
		for i in rhKnots:
			knots.append(i)
		knots.insert(0, knots[0])
		knots.insert(len(knots), knots[(len(knots)-1)])
		knots = Array[float](knots)
		#create ds curve from points, weights and knots
		dsNurbsCurve = NurbsCurve.ByControlPointsWeightsKnots(ptArray, weights, knots, degree)
		ptArray.Clear()
		Array.Clear(weights, 0, len(weights))
		Array.Clear(knots, 0, len(knots))
		return dsNurbsCurve

#convert rhino/gh geometry to ds geometry
dsNurbsCurves = []
for i in rhObjects:
	dsNurbsCurves.append(rhCurveToNurbsCurve(i))

#Assign your output to the OUT variable
OUT = dsNurbsCurves