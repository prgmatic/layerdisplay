class PositioningMode:
	absolute = 0
	relative = 1

class StepperTracker:

	__absolutePosition = 0
	__previousAbsolutePosition = 0

	__inputMode = PositioningMode.absolute

	
	def getAbsolutePosition(self):
		return self.__absolutePosition
	def getPreviousAbsolutePosition(self):
		return self.__previousAbsolutePosition

	def setPosition(self, newPosition):
		self.__previousAbsolutePosition = self.__absolutePosition
		if self.__inputMode == PositioningMode.absolute:
			self.__absolutePosition = newPosition
		else:
			self.__absolutePosition += newPosition

	def getPositioningMode(self):
		return __inputMode
	def setPositioningMode(self, newMode):
		self.__inputMode = newMode


