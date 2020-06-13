from .StepperTracker import StepperTracker, PositioningMode
from .PrintJobLayerInformation import PrintJobLayerInformation
from . import GCodeLineParser

EXTRUSIONS_REQUIRED_FOR_FIRST_LAYER = 3

class GCodeAnalyzer:

	def __init__(self):
		self._current_file_position = 0
		self._working = False

	def get_current_file_position(self):
		return self._current_file_position

	def is_working(self):
		return self._working

	def prepare_for_job(self):
		self._working = True

	def get_print_job_layer_information(self, gcode, file_size):
		self._progress = 0
		self._working = True
		z_axis =   StepperTracker()
		extruder = StepperTracker()
		previous_extrude_height = 0
		number_of_extrusions_this_layer = 0
		layer_change_positions = []

		file_position = 0

		for line in gcode:
			# Keep track of out position in the file
			file_position = gcode.tell() + len(line)
			self._current_file_position = file_position

			# Parse line into components
			line_components = GCodeLineParser.parse_line(line)
			if not line_components:
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
							if z_axis.get_absolute_position() != previous_extrude_height:
								# In order to ignore purges as layers, we make sure more than one extrude
								# has happened at this height to verify it is actually a layer.
								if len(layer_change_positions) or number_of_extrusions_this_layer >= EXTRUSIONS_REQUIRED_FOR_FIRST_LAYER:
									layer_change_positions.append(float(file_position) / file_size)
								previous_extrude_height = z_axis.get_absolute_position()
								# Rest number of extrusions this layer since moving to new one
								number_of_extrusions_this_layer = 1
							# keep track of how many extrusion happened this layer
							else:
								number_of_extrusions_this_layer += 1
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

		self._working = False
		return PrintJobLayerInformation(layer_change_positions)


