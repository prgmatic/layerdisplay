import time
import timeit
import re
from Event import Event
from PrintJob import PrintJob
#from layerdisplay.gcode import LineParser
import GCodeLineParser


def testListener(name):
	print("Oh, I hear ya %s!" % name)

testEvent = Event()
testEvent.register_callback(testListener)
testEvent.invoke("John")
testEvent.remove_all_callbacks()
testEvent.invoke("Sally")

class TestClass:

	def test_listener(self, name):
		print("we found %s" % name)

test_obj = TestClass()
testEvent.register_callback(test_obj.test_listener)
testEvent.invoke("Ajax")
