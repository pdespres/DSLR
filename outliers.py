#!/usr/bin/env python 3.6
# waloo le encoding: utf-8 de malade

"""
\033[32musage:	python outliers.py dataset_file\033[0m

"""

import sys
import csv
import os.path
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

def load_file(csvfile):
	df = pd.read_csv('./data/dataset_train.csv')
	df.drop(['Index', 'First Name', 'Last Name', 'Birthday', 'Best Hand', \
		'Arithmancy','Care of Magical Creatures','Defense Against the Dark Arts'], axis=1, inplace=True)
	df.fillna(df.mean(), inplace=True)
	y = pd.DataFrame()
	y = df['Hogwarts House']
	df.drop(['Hogwarts House'], axis=1, inplace=True)
	df.apply(pd.to_numeric,downcast='float')
	df = (df-df.mean())/df.std()
	return df, y

def print_pca(df, y):
	from sklearn import decomposition

	pca = decomposition.PCA(n_components=2)
	pca.fit(df)
	train_red = pca.transform(df)

	ycolor = y.astype('category').cat.codes
	plt.figure(figsize=(12, 8))
	plt.scatter(train_red[:,0],train_red[:,1], c=ycolor, alpha=0.5)
	plt.legend(loc='best')
	plt.suptitle('Data visualization after a 2D transform with PCA.', size = 12)
	plt.show()

	return train_red

def record_outliers(train_red, y):
	outliers = []
	for index, row in enumerate(train_red):
	    if row[0] > 3 and y[index] != 'Gryffindor':
	        outliers.append(index)
	    if row[0] < -1 and row[1] < -0.5 and y[index] != 'Ravenclaw':
	        outliers.append(index)
	    if row[0] < 0 and row[1] > 2 and y[index] != 'Slytherin':
	        outliers.append(index)
	    if row[0] < 1.2 and row[0] > -1 and row[1] < 1.1 and row[1] > -1 and y[index] != 'Hufflepuff':
	        outliers.append(index)
	print('outliers found: ',len(outliers))
	outliers = pd.DataFrame(outliers)
	outliers.to_csv('./data/outliers.csv' , index=False)
	df = pd.read_csv('./data/dataset_train.csv')
	df_red = df.drop(df.index[outliers[0]])
	df_red.to_csv('./data/dataset_reduce.csv' , index=False)
	print('new dataset available ./data/dataset_reduce.csv', 'rows: ', df_red.shape[0])

def outliers(csvfile):
	df, y = load_file(csvfile)
	train_red = print_pca(df, y)
	record_outliers(train_red, y)

def exit_error(string):
	print(string)
	sys.exit(42)
	return

if __name__ == "__main__":
	argc = len(sys.argv)
	if argc not in range(2, 3):
		print(__doc__)
	else:
		outliers(sys.argv[-1])