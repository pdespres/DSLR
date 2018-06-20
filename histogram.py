#!/usr/bin/env python 3.6
# waloo le encoding: utf-8 de malade

"""
\033[32musage:	python histogram.py [-x] dataset_file

Supported options:
	-x 		xkcd		xkcd style\033[0m
"""

#TODO
# auto-detection du meilleur?

import sys
import csv
import os.path
import matplotlib.pyplot as plt

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

def print_histos(headers, data):
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

	cpt = 0
	if params.xkcd:
		plt.xkcd()
	plt.figure(figsize=(22,15))
	plt.subplots_adjust(bottom=None, top=0.95)
	for column in headers:
		index += 1
		# test if the column is entirely made of numbers
		bNumeric = all_numeric(data, index)
		if not bNumeric or column == 'Index':
			continue
		for i, lib in enumerate(school):
			results[i] = []

		for row in data:
			for i, lib in enumerate(school):
				if row[school_col] == lib and row[index] != '':
					results[i].append(float(row[index]))

		# for each column printing histogram
		for x in results:
		   x.sort()
		cpt += 1
		ax = plt.subplot(3,5,cpt)

		for i, lib in enumerate(school):
			# data normalization
			array_norm = list(map((lambda x: (x - results[i][0]) / (results[i][-1] - results[i][0])), results[i]))
			plt.hist(array_norm, alpha=0.4, label=lib)
		plt.title(column, fontsize=12)
		if params.xkcd:
			ax.spines['right'].set_color('none')
			ax.spines['top'].set_color('none')
		# tagging the answer(s) 2 features are VERY VERY close, impossible to separate without mean calculus & variance
		meanSum = 0; gMean = 0; sumVar = 0
		if column in ('Arithmancy', 'Care of Magical Creatures'):
			for i, lib in enumerate(school):
				meanSum += sum(array_norm)/len(results[i])
				print(column, lib, 'mean:', '{0:.2f}'.format(sum(array_norm)/len(results[i])))
			gMean = meanSum/4
			print(column, 'Global', 'mean:', '{0:.2f}'.format(gMean))
			for i, lib in enumerate(school):
				sumVar += (sum(array_norm)/len(results[i]) - gMean) ** 2
			print(column, 'Global', 'Std:', '{0:.3f}'.format((sumVar/4)**0.5) + '\n')
			if column == 'Arithmancy':
				ax.set_facecolor('xkcd:mint green')
		plt.xlabel('grade', fontsize=8)
		plt.ylabel('students')
		plt.legend(loc='best')
		plt.suptitle('Quel cours de Poudlard a une répartition des notes homogènes entre les quatres maisons ?', size = 12)
	plt.show()

def params(param):
	#load params according to the command line options
	params.xkcd = False
	if param == 1:
		params.xkcd = True
	return

def histogram(csvfile, param=0):
	params(param)
	headers, data = load_file(csvfile)
	print_histos(headers, data)

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
				histogram(sys.argv[-1], param)
			else:
				print(__doc__)
		else:
			print(__doc__)
	else:
		histogram(sys.argv[-1])