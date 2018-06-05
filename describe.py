#!/usr/bin/env python 3.6
# waloo le encoding: utf-8 de malade

"""
\033[32musage:	python describe.py [-svgf] [dataset]

Supported options:
	-b 		bonus		bonus fields\033[0m
"""

#TODO
#rajouts bonus khi2?

import sys
import csv
import os.path

def load_file(csvfile):
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

def calculate_stats(headers, data):
	index = -1
	results = []
	for column in headers:
		index += 1

		# test if the column is entirely made of numbers
		bNumeric = all_numeric(data, index)
		if not bNumeric and params.bonus == False:
			continue
		if column == 'Index' and params.bonus == True:
			continue

		# create an array with all non empty values
		array = []
		for row in data:
			if row[index] != '':
				if bNumeric:
					value = float(row[index])
				else:
					value = row[index]
				array.append(value)
		count = len(array)
		if count == 0:
			continue
		array.sort()

		result = {}
		result[''] = column
		result['Count'] = count
		if bNumeric:
			mean = sum(array) / count
			result['Mean'] = mean
			if count > 1:
				result['Std'] = (sum(list(map((lambda x: (x - mean) ** 2), array))) / (count - 1)) ** 0.5
			result['Min'] = array[0]
			result['25%'] = array[max(int(count * 0.25) - 1, 0)]
			result['50%'] = array[max(int(count * 0.50) - 1, 0)]
			result['75%'] = array[max(int(count * 0.75) - 1, 0)]
			result['Max'] = array[count - 1]
			#bonus
			#bonus
		else:
			#bonus
			uniquearray = list(sorted(set(array)))
			result['Unique'] = len(uniquearray)
			temp = [[array.count(x), x] for x in set(uniquearray)]
			temp.sort()
			tempmax = temp[len(temp) - 1]
			result['Top'] = tempmax[1]
			result['Freq'] = tempmax[0]
			#bonus

		results.append(result)

	return results

def print_results(results, stats):
	for y in stats:
		line = y.ljust(7)
		for x in results:
			padding = max(len(x['']) + 1, 14)
			if y in x.keys():
				input = x[y]
				if is_number(input):
					if y in ('Count','Unique','Freq'):
						line += '{0:.0f}'.format(x[y]).rjust(padding)
					else:
						line += '{0:.6f}'.format(x[y]).rjust(padding)
				else:
					line += x[y].rjust(padding)
			else:
				line += 'NaN'.rjust(padding)
		print(line)
	return

def describe(csvfile, param=0):
	params(param)
	stats = ['','Count','Mean','Std','Min','25%','50%','75%','Max']
	if params.bonus:
		stats = ['','Count','Unique','Top','Freq','Mean','Std','Min','25%','50%','75%','Max']
	headers, data = load_file(csvfile)
	results = calculate_stats(headers, data)
	print_results(results, stats)
	return

def params(param):
	#load params according to the command line options
	params.bonus = False
	if param == 1:
		params.bonus = True
	return

def exit_error(string):
	print(string)
	return

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