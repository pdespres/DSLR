#!/usr/bin/env python 3.6
# waloo le encoding: utf-8 de malade

"""
\033[32musage:	python logreg_train.py [-b] [dataset]

Supported options:
	-b 		bonus		bonus fields\033[0m
"""

# TODO clean nan data
#
import sys
import csv
import os.path
import math

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
	params.xkcd = False
	if param == 1:
		params.xkcd = True
	return

def sigmoid(z):
    return 1 / (1 + exp(-z))

def loss(yhat, y):
    return (-y * log(yhat) - (1 - y) * log(1 - yhat)).mean()

def train_lr():
	params(param)
	headers, data = load_file(csvfile)
	learning_rate = 0.1
	iterations = 200
    # if self.fit_intercept:
    #     X = self.__add_intercept(X)
    
    # # weights initialization
    # self.theta = np.zeros(X.shape[1])
    
    # for i in range(self.num_iter):
    #     z = np.dot(X, self.theta)
    #     h = self.__sigmoid(z)
    #     gradient = np.dot(X.T, (h - y)) / y.size
    #     self.theta -= self.lr * gradient
        
    #     if(self.verbose == True and i % 10000 == 0):
    #         z = np.dot(X, self.theta)
    #         h = self.__sigmoid(z)
    #         print(f'loss: {self.__loss(h, y)} \t')

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
				train_lr(sys.argv[-1], param)
			else:
				print(__doc__)
		else:
			print(__doc__)
	else:
		train_lr(sys.argv[-1])