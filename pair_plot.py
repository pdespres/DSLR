#!/usr/bin/env python 3.6
# waloo le encoding: utf-8 de malade

"""
\033[32musage:	python pair_plot.py [-x] [dataset]

Supported options:
	-x 		xkcd		xkcd style\033[0m
"""

#TODO

import sys
import csv
import os.path
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from PIL import Image

def load_file(csvfile):
	#open file > drop Nan rows > drop non-interesting colums > change date and categorical to numeric 
	if not os.path.isfile(csvfile):
		exit_error('can\'t find the file ' + csvfile)
	data = pd.read_csv(csvfile)
	if data.shape[0] < 1:
		exit_error('file ' + csvfile + ' is empty')
	data.dropna(inplace=True)
	df = data.drop(['Index','Hogwarts House','First Name','Last Name'], axis=1)
	df['Birthday'] = pd.to_datetime(df['Birthday'], format='%Y-%m-%d')
	df['Birthday'] = pd.to_numeric(df.Birthday)
	df['Best Hand'] = pd.Categorical(df['Best Hand']).codes
	df_norm = (df - df.min()) / (df.max() - df.min())
	df_norm['Hogwarts House'] = data['Hogwarts House']
	return df_norm

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

def print_pair(data):
	if params.xkcd:
		plt.xkcd()
		sns.despine()
	# pairPlot = sns.pairplot(data, hue='Hogwarts House', diag_kind='kde', \
	pairPlot = sns.pairplot(data, hue='Hogwarts House', \
		plot_kws = {'alpha': 0.6, 's': 80, 'edgecolor': 'k'})
	pairPlot.fig.suptitle('À partir de cette visualisation, quelles caractéristiques allez-vous utiliser pour entraîner votre prochaine régression logistique ?', fontsize=30)
	pairPlot.fig.subplots_adjust(top=.95)
	pairPlot.fig.subplots_adjust(right=.95)
	# graph is too big for easy use under plt. So save as png and open it as img file
	pairPlot.savefig("./data/pair_plot.png")
	img = Image.open("./data/pair_plot.png")
	img.show()
		
def pair(csvfile, param=0):
	params(param)
	data = load_file(csvfile)
	print_pair(data)

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
				pair(sys.argv[-1], param)
			else:
				print(__doc__)
		else:
			print(__doc__)
	else:
		pair(sys.argv[-1])