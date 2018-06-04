#!/usr/bin/env python 3.6
# waloo le encoding: utf-8 de malade

"""
\033[32musage:	python describe.py [-svgf] [dataset]

Supported options:
	-b 		bonus		bonus fields\033[0m
"""

#TODO
#rajouts bonus khi2, gmean, 

import sys
import csv

def load_file():
    if not csvfile.is_file():
    	exit_error('can\'t find the file ' + csvfile)
    data = []
    with open(csvfile) as csv_iterator:
        data_reader = csv.reader(csv_iterator, delimiter=',')
        for row in data_reader:
            data.append(row)
    csv_iterator.close()
    if len(data < 2):
    	exit_error('file ' + csvfile + ' is empty')
    headers = data[0]
    del data[0]
    return headers, data

def describe(csvfile, param=0):
	params(param)
	headers, data = load_file(csvfile)
	
	return

def params(param):
	#load params according to the command line options
	params.bonus = False
	if param in (1):
		params.bonus = True

def exit_error(error_mes):
	if error_mes != "":
		print("\033[7;31mError:\033[0m " + error_mes + '\n'
	sys.exit(42)

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