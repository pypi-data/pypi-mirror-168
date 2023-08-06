
import numpy as np

def get_rsquare(yT, yP):
	''' calculate r_square
	'''
	yB = np.mean(yT)
	ssreg = np.sum((yP - yB) ** 2)
	ssres = np.sum((yP - yT) ** 2)
	sstot = np.sum((yT - yB) ** 2)
	return 1 - ssres / sstot

def get_bias(yT, yP):
	return np.mean(yT-yP)

def get_rmse(yT, yP):
	''' calculate RMSE
	'''
	return np.sqrt(np.mean((yT - yP)**2))