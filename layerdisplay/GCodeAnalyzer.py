from StepperTracker import StepperTracker, PositioningMode
from PrintJobLayerInformation import PrintJobLayerInformation
import GCodeLineParser

def get_print_job_layer_information(gcode, file_size):
	z_axis =    StepperTracker()
	extruder = StepperTracker()
	previous_extrude_height = 0
	layer_change_positions = []

	file_position = 0

	for line in gcode:
		# Keep track of out position in the file
		file_position += len(line) + 1

		# Parse line into components
		line_components = GCodeLineParser.parse_line(line)
		if line_components == None:
			continue

		gCode = line_components[0]
		if gCode == 'G0' or gCode == 'G1' or gCode == 'G2' or gCode == 'G3':
			for component_index in range(1, len(line_components)):
				# Handle extrusion component of line
				if line_components[component_index][0] == 'E':
					value = float(line_components[component_index][1:])
					extruder.set_position(value)
					# Check if extruder extruded and not retracted
					if extruder.get_absolute_position() > extruder.get_previous_absolute_position():
						# See if extruded at higher z height then previous extrusion z height
						if z_axis.get_absolute_position() > previous_extrude_height:
							layer_change_positions.append(float(file_position) / file_size)
							previous_extrude_height = z_axis.get_absolute_position()
				# Handle Z component of line
				elif line_components[component_index][0] == 'Z':
					value = float(line_components[component_index][1:])
					z_axis.set_position(value)
		elif gCode == 'G90':
			z_axis.set_positioning_mode(PositioningMode.absolute)
		elif gCode == 'G91':
			z_axis.set_positioning_mode(PositioningMode.relative)
		elif gCode == 'M82':
			extruder.set_positioning_mode(PositioningMode.absolute)
		elif gCode == 'M83':
			extruder.set_positioning_mode(PositioningMode.relative)

	return PrintJobLayerInformation(layer_change_positions)


