#!/usr/bin/env python 3.6
# waloo le encoding: utf-8 de malade

"""
\033[32musage:	python logreg_train.py [-vs] dataset_file.npy

Supported options:
	-v 		verbose		print epochs\033[0m
	-s 		stochastic	optimization with stochastic gradient descent
	-a 		adam		optimization with adam method
"""

# implement SGD + adam?

import sys
import csv
import os.path
import numpy as np

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

def params(param):
	#load params according to the command line options
	params.verbose = False
	params.stochastic = False
	params.adam = False
	if param in (1,3,5):
		params.verbose = True
	if param in (2,3):
		params.stochastic = True
	if param in (4,5):
		params.adam = True
	return

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

def get_median(data, index):
	array = []
	for row in data:
		if row[index] != '':
			array.append(float(row[index]))
	count = len(array)
	if count == 0:
		return 0
	array.sort()
	return array[max(int(count * 0.50) - 1, 0)]
	
def sigmoid(z):
	return 1 / (1 + np.exp(-z))

def loss(yhat, y):
	return sum(y * np.log(yhat) + (1 - y) * np.log(1 - yhat)) / (-(y.shape[0]))

def prep_data(headers, data):
	medians = []
	featuresToReject = ['Index','Hogwarts House','First Name','Last Name','Arithmancy','Care of Magical Creatures', \
						'Defense Against the Dark Arts','Birthday']
	featuresToKeep = []
	features = []
	y = []

	# Separate y = Hogwarts House
	for index, column in enumerate(headers):
		if column == 'Hogwarts House':
			for row in data:
				y.append(row[index])
						
	# Which features do we keep?
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
		median = get_median(data, numCol)
		medians.append(median)
		for row in data:
			if row[numCol] == '':
				row[numCol] = median
	# save for easy retrieval in predict.py
	np.save('./data/medians.npy', medians)

	# Create a matrix for the data
	for index, numCol in enumerate(featuresToKeep):
		for row in data:
			features[index].append(float(row[numCol]))

	# Normalize data
	for index, feature in enumerate(features):
		features[index] = [(x - min(feature)) / (max(feature) - min(feature)) for x in feature]
	
	return  features, y

def get_schools(data, headers):
	# get schools
	array = []
	for index, lib in enumerate(headers):
		if lib == 'Hogwarts House':
			school_col = index
	for row in data:
		if row[school_col] != '':
			array.append(row[school_col])
	uniquearray = list(sorted(set(array)))
	school = [x for x in set(uniquearray)]
	school.sort()
	# save for easy retrieval in predict.py
	np.save('./data/schools.npy', school)
	return school

def f(i, school):
	if i == school:
		return 1
	else:
		return 0

#bonus stochastic_gradient_descent => adjustement of theta at each row
def stochastic_gradient_descent(train, y, theta, school):
	# params to modify
	learning_rate = 0.05
	iterations = 200

	cpt = 0
	while cpt < iterations:
		
		# shuffling
		p = np.random.permutation(len(train))
		train = train[p]
		y = y[p]

		for i in range(train.shape[0]):
			temp = np.dot(train[i], theta)
			yhat = sigmoid(temp)
			cost = -(y[i] * np.log(yhat) + (1 - y[i]) * np.log(1 - yhat))
			gradient = np.dot((yhat - y[i]), train[i])
			theta -= gradient * learning_rate
		if params.verbose and cpt % 20 == 0:
			temp = np.dot(train, theta)
			yhat = sigmoid(temp)
			cost = loss(yhat, y)
			print(school, cpt, cost)
		cpt += 1
	return theta

#bonus adam => adjustement of theta AND separate learning rate (with momentum) at each row
def adam(train, y, theta, school):
	# params to modify
	learning_rate = 0.001
	epsilon = 0.00000001
	beta1 = 0.9
	beta2 = 0.999
	iterations = 200

	cpt = 0
	M = np.zeros(train.shape[1])
	R = np.zeros(train.shape[1])
	while cpt < iterations:

		# shuffling
		p = np.random.permutation(len(train))
		train = train[p]
		y = y[p]

		for i in range(train.shape[0]):
			temp = np.dot(train[i], theta)
			yhat = sigmoid(temp)
			cost = -(y[i] * np.log(yhat) + (1 - y[i]) * np.log(1 - yhat))
			gradient = np.dot((yhat - y[i]), train[i])

			for k,_ in enumerate(gradient):
				M[k] = beta1 * M[k] + (1. - beta1) * gradient[k]
				R[k] = beta2 * R[k] + (1. - beta2) * gradient[k]**2

				m_k_hat = M[k] / (1. - beta1**(i+1))
				r_k_hat = R[k] / (1. - beta2**(i+1))

				theta[k] -= learning_rate / (np.sqrt(r_k_hat) + epsilon) * m_k_hat

		if params.verbose and cpt % 20 == 0:
			temp = np.dot(train, theta)
			yhat = sigmoid(temp)
			cost = loss(yhat, y)
			print(school, cpt, cost)
		cpt += 1
	return theta

def gradient_descent(train, y, theta, school):
	# params to modify
	learning_rate = 0.1
	param_stop = 0.000001

	cost = 1
	for i in range(100000):
		temp = np.dot(train, theta)
		yhat = sigmoid(temp)
		prev_cost = cost
		cost = loss(yhat, y)
		if params.verbose and i % 500 == 0:
			print(school, i, cost)
		if prev_cost - cost < param_stop:
			if params.verbose:
				print(school, i, cost)
			break
		gradient = np.dot((yhat - y), train) / y.shape[0]
		theta -= gradient * learning_rate
	return theta

def train_lr(csvfile, param=0):
	params(param)
	headers, data = load_file(csvfile)
	features, yraw = prep_data(headers, data)
	schools = get_schools(data, headers)

	# Using from now numpy lib to ease coding. checked with ademenet (only basic numpy functions)
	# one vs all => 1 logistic regression for each school
	weights = []
	train = np.array(features).T
	# add intercept
	train = np.insert(train, 0, 1, axis=1)
	for school in schools:
		y = np.array([f(i, school) for i in yraw])
		theta = np.zeros(train.shape[1])

		# different optimizations
		if params.stochastic == True:
			name = 'stochastic gradient descent'
			theta = stochastic_gradient_descent(train, y, theta, school)
		elif params.adam == True:
			name = 'adam'
			theta = adam(train, y, theta, school)
		else:
			name = 'gradient descent'
			theta = gradient_descent(train, y, theta, school)

		if params.verbose:
			print(school, theta)
		weights.append(theta)

	# save weights
	np.save('./data/weights.npy', weights)
	print('Training with %s is done!' % (name))


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
		if (sys.argv[1][0] == '-' and len(sys.argv[1]) in range(2,4)):
			if sys.argv[1].find('v') > 0:
				param += 1
			if sys.argv[1].find('s') > 0:
				param += 2
			if sys.argv[1].find('a') > 0:
				param += 4
			if param > 0 and param < 6:
				train_lr(sys.argv[-1], param)
			else:
				print(__doc__)
		else:
			print(__doc__)
	else:
		train_lr(sys.argv[-1])