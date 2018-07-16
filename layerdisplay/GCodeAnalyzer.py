import re
from StepperTracker import StepperTracker, PositioningMode

class GCodeAnalyzer:
	
	def __init__(self):
		self._zAxis =    StepperTracker()
		self._extruder = StepperTracker()
		self._previousExtrudeHeight = 0
		self._layerChangePositions = []

	def analyze_gcode(self, gcode, gcodeSize):
		self._zAxis =    StepperTracker()
		self._extruder = StepperTracker()
		self._previousExtrudeHeight = 0
		self._layerChangePositions = []

		filePosition = 0

		lineIndex = -1;
		for line in gcode:
			filePosition += len(line) + 1
			lineIndex += 1
			if not line:
				continue
			line = self.__stripLine(line)
			if line == None:
				continue
			self.__handleLine(line, filePosition, gcodeSize)

	def getLayerChangePositions(self):
		return self._layerChangePositions

	def getLayerCount(self):
		return len(self._layerChangePositions)

	def __handleLine(self, line, filePosition, fileSize):
		lineComponents = line.split()
		gCode = lineComponents[0]

		if gCode == 'G0' or gCode == 'G1' or gCode == 'G2' or gCode == 'G3':
			for componentIndex in range(1, len(lineComponents)):
				# Handle extrusion component of line
				if lineComponents[componentIndex][0] == 'E':
					value = float(lineComponents[componentIndex][1:])
					self._extruder.setPosition(value)
					# Check if extruder extruded and not retracted
					if self._extruder.getAbsolutePosition() > self._extruder.getPreviousAbsolutePosition():
						# See if extruded at higher z height then previous extrusion z height
						if self._zAxis.getAbsolutePosition() > self._previousExtrudeHeight:
							self._layerChangePositions.append(float(filePosition) / fileSize)
							self._previousExtrudeHeight = self._zAxis.getAbsolutePosition()
				# Handle Z component of line
				elif lineComponents[componentIndex][0] == 'Z':
					value = float(lineComponents[componentIndex][1:])
					self._zAxis.setPosition(value)
		elif gCode == 'G90':
			self._zAxis.setPositioningMode(PositioningMode.absolute)
		elif gCode == 'G91':
			self._zAxis.setPositioningMode(PositioningMode.relative)
		elif gCode == 'M82':
			self._extruder.setPositioningMode(PositioningMode.absolute)
		elif gCode == 'M83':
			self._extruder.setPositioningMode(PositioningMode.relative)
		

	def __stripLine(self, line):
		# split line by comment character,
		# only text to left of first comment character is valid.
		result = re.split('[\(;]', line)[0]
		result = result.strip()
		if len(result) == 0:
			return None
		return result
