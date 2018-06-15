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

def prep_data(headers, data):
	featuresToKeep = []
	features = []
	# test if the column is entirely made of numbers
	for index, column in enumerate(headers):
		bNumeric = all_numeric(data, index)
		if not bNumeric or column == 'Index':
			continue
		featuresToKeep.append(index)
		features.append([])

	for row in data:
		# Don't keep the empty results
		bNaN = False
		for index, numCol in enumerate(featuresToKeep):
			if row[numCol] == '':
				bNaN = True
		if bNaN:
			continue
		# Create an array for the data of each feature
		for index, numCol in enumerate(featuresToKeep):
			features[index].append(float(row[numCol]))
	return featuresToKeep, features

def pearson_score(X, Y):
    xmean = sum(X) / len(X)
    ymean = sum(Y) / len(Y)
    xsub = [i - xmean for i in X]
    ysub = [i - ymean for i in Y]
    xsub_times_ysub = [a * b for a, b in list(zip(xsub, ysub))]
    etx = (sum(list(map((lambda x: (x - xmean) ** 2), X))) / (len(X) - 1)) ** 0.5
    ety = (sum(list(map((lambda x: (x - ymean) ** 2), Y))) / (len(Y) - 1)) ** 0.5
    return (sum(xsub_times_ysub) / len(xsub_times_ysub) / (etx * ety))

def find_highest_correlation(headers, data):
	featuresToKeep, features = prep_data(headers, data)
	pmax = 0
	for i, column1 in enumerate(featuresToKeep):
	    for j, column2 in enumerate(featuresToKeep):
	        if i >= j:
	            continue
	        coefCorr = pearson_score(features[i], features[j])
	        print(abs(coefCorr))
	        if abs(coefCorr) > pmax:
	            pmax = abs(coefCorr)
	            result = (i,j)
	return result, pmax
	            
def scatter(csvfile, param=0):
	params(param)
	headers, data = load_file(csvfile)
	print('\nQUESTION: Quelles sont les deux features qui sont semblables ?\n')
	highest, pmax = find_highest_correlation(headers, data)

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