#!/usr/bin/env python 2.7
# waloo le encoding: utf-8 de malade

"""
\033[32musage:	python describe.py [-svgf] [dataset]

Supported options:
	-b 		bonus		bonus fields\033[0m
"""

#TODO

import sys
import csv

def describe(file, param=0):
	params(param)
	return

def params(param):
	#load params according to the command line options
	params.bonus = False
	if param in (1):
		params.bonus = True

if __name__ == "__main__":
	argc = len(sys.argv)
	if argc not in range(2, 4):
		print(__doc__)
	elif argc == 3:
		#traitement params
		param = 0
		if (sys.argv[1][0] == '-' and len(sys.argv[1]) == 2):
			if sys.argv[1].find('b') > 0:
				param += 1
			if param > 0:
				describe(sys.argv[-1], param)
			else:
				print(__doc__)
		else:
			print(__doc__)
	else:
		describe(sys.argv[-1])