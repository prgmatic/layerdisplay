class Event:
	_callbacks = []

	def invoke(self, *args):
		for callback in self._callbacks:
			if args:
				callback(args)
			else:
				callback()

	def register_callback(self, callback):
		if callback not in self._callbacks:
			self._callbacks.append(callback)

	def remove_callback(self, callback):
		if callback in self._callbacks:
			self._callbacks.remove(callback)

	def remove_all_callbacks(self):
		self._callbacks = []
