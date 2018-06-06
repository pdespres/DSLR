#!/usr/bin/env python 3.6
# waloo le encoding: utf-8 de malade

#TODO

import sys
import csv
import os.path

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

def prepare_data(headers, data):
	# looking for index of school column
	for index, lib in enumerate(headers):
		if lib == 'Hogwarts House':
			school_col = index
	
	# looking for diffenrent values of school	
	array = []
	for row in data:
	    if row[school_col] != '':
	        array.append(row[school_col])
	uniquearray = list(sorted(set(array)))
	school = [x for x in set(uniquearray)]
	school.sort()

	# dividing each numeric columns regarding schools
	index = -1
	results = []
	for i, lib in enumerate(school):
	    results.append([])

	for column in headers:
	    index += 1
	    # test if the column is entirely made of numbers
	    bNumeric = all_numeric(index)
	    if not bNumeric or column == 'Index':
	        continue
	    for i, lib in enumerate(school):
	        results[i] = []

	    for row in data:
	        for i, lib in enumerate(school):
	            if row[school_col] == lib and row[index] != '':
	                results[i].append(float(row[index]))

		# for each column printing histogram

def histogram(csvfile):
	headers, data = load_file(csvfile)
	prepare_data(headers, data)

def exit_error(string):
	print(string)
	sys.exit(42)
	return

if __name__ == "__main__":
	argc = len(sys.argv)
	if argc not in range(2, 3):
		print(__doc__)
	else:
		histogram(sys.argv[-1])