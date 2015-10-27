# Copyright(c) 2015, Konrad Sobon
# @arch_laboratory, http://archi-lab.net

import clr
import sys
clr.AddReference('ProtoGeometry')

pyt_path = r'C:\Program Files (x86)\IronPython 2.7\Lib'
sys.path.append(pyt_path)

import os
test = []
appDataPath = os.getenv('APPDATA')
dynVersions = ["0.7", "0.8", "0.9"]
dynFolders = ["extra", "bin"]
for i in dynVersions:
	for j in dynFolders:
		part1 = "\\Dynamo\\"
		version = i
		part2 = "\\packages\\Mantis Shrimp\\"
		folder = j
		msPath = part1 + version + part2 + folder
		if j == "extra":
			if msPath not in sys.path:
				sys.path.Add(msPath)
		if j == "bin":
			dllName = "\\Rhino3dmIO.dll"
			rhDllPath = part1 + version + part2 + folder + dllName
			if msPath not in sys.path:
				sys.path.Add(msPath)
				if os.path.isfile(rhDllPath):
					clr.AddReferenceToFileAndPath(rhDllPath)

from Autodesk.DesignScript.Geometry import *
import Rhino as rc

#The inputs to this node will be stored as a list in the IN variable.
dataEnteringNode = IN
path = str(IN[0])

#Assign your output to the OUT variable
OUT = rc.FileIO.File3dm.Read(path)
