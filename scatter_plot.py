#!/usr/bin/env python 3.6
# waloo le encoding: utf-8 de malade

"""
\033[32musage:	python scatter_plot.py [-x] [dataset]

Supported options:
	-x 		xkcd		xkcd style\033[0m
"""

#TODO

import sys
import csv
import os.path
import matplotlib.pyplot as plt

csvfile = './data/dataset_train.csv'

def load_file(csvfile):
	#open file / create headers(column name) and data arrays
	if not os.path.isfile(csvfile):
		exit_error('can\'t find the file ' + csvfile)
	data = []
	with open(csvfile) as csv_iterator:
		data_reader = csv.reader(csv_iterator, delimiter=',')
		for row in data_reader:
			data.append(row)
	csv_iterator.close()
	if len(data) < 2:
		exit_error('file ' + csvfile + ' is empty')
	headers = data[0]
	del data[0]
	return headers, data

def is_number(value):
	#surprisingly hard to do in python
	try:
		float(value)
		return True
	except ValueError:
		return False

def all_numeric(data, index):
	for row in data:
		if row[index] != '' and is_number(row[index]) == False:
			return False
	return True

def params(param):
	#load params according to the command line options
	params.xkcd = False
	if param == 1:
		params.xkcd = True
	return

def print_splots(headers, data):

		
def scatter(csvfile, param=0):
	params(param)
	headers, data = load_file(csvfile)
	print('\nQUESTION: Quelles sont les deux features qui sont semblables ?\n')
	print_splots(headers, data)

def exit_error(string):
	print(string)
	sys.exit(42)
	return

if __name__ == "__main__":
	argc = len(sys.argv)
	if argc not in range(2, 4):
		print(__doc__)
	elif argc == 3:
		#traitement params
		param = 0
		if (sys.argv[1][0] == '-' and len(sys.argv[1]) == 2):
			if sys.argv[1].find('x') > 0:
				param += 1
			if param > 0:
				scatter(sys.argv[-1], param)
			else:
				print(__doc__)
		else:
			print(__doc__)
	else:
		scatter(sys.argv[-1])