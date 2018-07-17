import re

def strip_comment(line):
	comment_pos = line.find(';')
	if comment_pos == -1:
		return line
	return line[:comment_pos].strip()

def parse_line(line):
	line = strip_comment(line)
	if len(line) == 0:
		return None
	if line.find('(') != -1:
		return None
	return line.split()
