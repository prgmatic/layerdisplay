from StepperTracker import StepperTracker, PositioningMode
from PrintJobLayerInformation import PrintJobLayerInformation
import GCodeLineParser

def get_print_job_layer_information(gcode, fileSize):
	z_axis =    StepperTracker()
	extruder = StepperTracker()
	previous_extrude_height = 0
	layer_change_positions = []

	filePosition = 0

	for line in gcode:
		# Keep track of out position in the file
		filePosition += len(line) + 1

		# Parse line into components
		lineComponents = GCodeLineParser.parse_line(line)
		if lineComponents == None:
			continue

		gCode = lineComponents[0]
		if gCode == 'G0' or gCode == 'G1' or gCode == 'G2' or gCode == 'G3':
			for componentIndex in range(1, len(lineComponents)):
				# Handle extrusion component of line
				if lineComponents[componentIndex][0] == 'E':
					value = float(lineComponents[componentIndex][1:])
					extruder.setPosition(value)
					# Check if extruder extruded and not retracted
					if extruder.getAbsolutePosition() > extruder.getPreviousAbsolutePosition():
						# See if extruded at higher z height then previous extrusion z height
						if z_axis.getAbsolutePosition() > previous_extrude_height:
							layer_change_positions.append(float(filePosition) / fileSize)
							previous_extrude_height = z_axis.getAbsolutePosition()
				# Handle Z component of line
				elif lineComponents[componentIndex][0] == 'Z':
					value = float(lineComponents[componentIndex][1:])
					z_axis.setPosition(value)
		elif gCode == 'G90':
			z_axis.setPositioningMode(PositioningMode.absolute)
		elif gCode == 'G91':
			z_axis.setPositioningMode(PositioningMode.relative)
		elif gCode == 'M82':
			extruder.setPositioningMode(PositioningMode.absolute)
		elif gCode == 'M83':
			extruder.setPositioningMode(PositioningMode.relative)

	return PrintJobLayerInformation(layer_change_positions)


