#!/usr/bin/env python 3.6
# waloo le encoding: utf-8 de malade

"""
\033[32musage:	python logreg_train.py [-v] dataset_file [weights_files]

Supported options:
	-v 		verbose		print epochs\033[0m
"""

#TODO weight file en input

import sys
import csv
import os.path
import numpy as np

def load_file(csvfile, weightfile):
	#open file / create headers(column name) and data arrays
	if not os.path.isfile(csvfile):
		exit_error('can\'t find the file ' + csvfile)
	if not os.path.isfile(weightfile):
		exit_error('can\'t find the file ' + weightfile)
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

def params(param):
	#load params according to the command line options
	params.verbose = False
	if param == 1:
		params.verbose = True
	return

def sigmoid(z):
	return 1 / (1 + np.exp(-z))

def prep_data(headers, data, medians):
	featuresToReject = ['Index','Hogwarts House','First Name','Last Name','Arithmancy','Care of Magical Creatures', \
						'Defense Against the Dark Arts','Birthday']
	featuresToKeep = []
	features = []
						
	for index, column in enumerate(headers):
		if column in featuresToReject:
			continue
		featuresToKeep.append(index)
		features.append([])
			
	for index, numCol in enumerate(featuresToKeep):
		# Replace categorical value with numeric
		if headers[numCol] == 'Best Hand':
			for row in data:
				if row[numCol] == 'Left':
					row[numCol] = 0
				else:
					row[numCol] = 1
		# Replace NaN data with median
		median = medians[index]
		for row in data:
			if row[numCol] == '':
				row[numCol] = median

	# Create a marix for the data
	for index, numCol in enumerate(featuresToKeep):
		for row in data:
			features[index].append(float(row[numCol]))

	# Normalize data
	for index, feature in enumerate(features):
		features[index] = [(x - min(feature)) / (max(feature) - min(feature)) for x in feature]
	
	return  features

def predict_lr(csvfile, weightfile, param=0):
	params(param)
	headers, data = load_file(csvfile, weightfile)
	medians = np.load('./data/medians.npy')
	schools = np.load('./data/schools.npy')
	#weights = np.load('./data/weights.npy')
	weights = np.load(weightfile)
	probas = []
	features = prep_data(headers, data, medians)
	test = np.array(features).T
	# add intercept
	test = np.insert(test, 0, 1, axis=1)

	# compute probas for each school
	for index, school in enumerate(schools):
		theta = weights[index]
		temp = np.dot(test, theta)
		yhat = sigmoid(temp)
		probas.append(yhat)

	# choose the most probable school and write result
	yhats = np.array(probas).T
	with open('./data/houses.csv', 'w') as outputfile:
		writer = csv.writer(outputfile, delimiter=',')
		writer.writerow(["Index", "Hogwarts House"])
		for index, row in enumerate(yhats):
			if params.verbose:
			#if row[row.argmax()] < 0.90:
				print(index, ['{0:.4f}'.format(i) for i in row], row.argmax(), '{0:.2f}'.format(row[row.argmax()]), \
					' => ', schools[row.argmax()])
			writer.writerow((index, schools[row.argmax()]))
	print('Predictions are done! houses.csv in ./data/')

def exit_error(string):
	print(string)
	sys.exit(42)
	return

if __name__ == "__main__":
	argc = len(sys.argv)
	if argc not in range(2, 5):
		print(__doc__)
	#traitement params
	param = 0 ; paramExists = False
	if (sys.argv[1][0] == '-' and len(sys.argv[1]) == 2):
		if sys.argv[1].find('v') > 0:
			param += 1
		else:
			print(__doc__)
	#weightfile optional
	weightfile = './data/weights.npy'
	if argc - param == 3:
		weightfile = sys.argv[-1]
	predict_lr(sys.argv[1 - argc + param], weightfile, param)