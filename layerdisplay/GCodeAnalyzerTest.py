from .GCodeAnalyzer import GCodeAnalyzer
import time
import os
import threading


file_name = r"C:\Users\chatr\AppData\Roaming\OctoPrint\uploads\20m_sphere.gcode"

print("Starting gcode analyzation")

gCodeAnalyzer = GCodeAnalyzer()
gcode = file(file_name, "r")
file_size = os.path.getsize(file_name)

def analyze_gcode():
	start = time.time()

	layer_info = gCodeAnalyzer.get_print_job_layer_information(gcode, file_size)

	end = time.time()
	print("Analyzation complete")
	print(end - start)
	print("%d layers in gcode" % layer_info.get_layer_count())

	gcode.close()

gCodeAnalyzer.prepare_for_job()
thread = threading.Thread(target=analyze_gcode)
thread.start()

while gCodeAnalyzer.is_working():
	file_pos = float(gCodeAnalyzer.get_current_file_position())
	print("%%%.1f" %  (file_pos / file_size * 100))
