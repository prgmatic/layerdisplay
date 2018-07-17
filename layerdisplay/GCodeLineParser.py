import re

def strip_comment(line):
	commentPos = line.find(';')
	if commentPos == -1:
		return line
	return line[:commentPos].strip()

def parse_line(line):
	line = strip_comment(line)
	if len(line) == 0:
		return None
	if line.find('(') != -1:
		return None
	return line.split()
