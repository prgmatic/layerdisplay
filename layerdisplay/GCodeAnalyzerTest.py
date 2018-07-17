import GCodeAnalyzer
import time
import os

file_name = "C:\Users\chatr\AppData\Roaming\OctoPrint\uploads\PLA_200_RubixCubeHolder.gcode"

print("Starting gcode analyzation")

start = time.time()

gcode = file(file_name, "r")
file_size = os.path.getsize(file_name)
layer_info = GCodeAnalyzer.get_print_job_layer_information(gcode, file_size)

end = time.time()
print("Analyzation complete")
print(end - start)
print("%d layers in gcode" % layer_info.get_layer_count())

gcode.close()
