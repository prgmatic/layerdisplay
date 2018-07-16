from GCodeAnalyzer import GCodeAnalyzer
import time
import os

class DummyLogger:
	def info(self, msg):
		print(msg)


fileName = "C:\Users\chatr\AppData\Roaming\OctoPrint\uploads\PLA_200_RubixCubeHolder.gcode"

print("Starting gcode analyzation")

start = time.time()

gcode = file(fileName, "r")
fileSize = os.path.getsize(fileName)
analyzer = GCodeAnalyzer()
analyzer.analyze_gcode(gcode, fileSize)

end = time.time()
print("Analyzation complete")
print(end - start)
print("%d layers in gcode" % len(analyzer.getLayerChangePositions()))

gcode.close()
