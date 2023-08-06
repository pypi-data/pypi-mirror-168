#!/usr/bin/env python3
#-*- coding:utf-8 -*-
"""
Atmospheric correction.
=====

Provides atmospheric correction for VNIR SWIR MIR TIR data.

"""
from itertools import product
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap, addcyclic


from pkulast.atmosphere.profile import Profile, NWPLibrary
# from simpir.utils.atmos import *

class AerosolOpticalDepth(object):
    ''' Aerosol Optical Depth(AOD) Retrieval
	1.
	https://aeronet.gsfc.nasa.gov/
	AeroNet CE318 aod@500nm / visibility
	中科院的网络

	'''
    def __init__(self):
        pass


class WaterVapor(object):
    ''' Water Vapor Retrieval

	1.
	tau(lambda_wv) = L(lambda_wv) / L(lambda_nwv)
	or tau(lambda_wv) = L(lambda_wv) / (c1*L(lambda_nwv1) + c2*L(lambda_nwv2))

	then wv = (alpha - ln(tau / beta))^2

	2.
	https://aeronet.gsfc.nasa.gov/
	AeroNet CE318  WV@946nm

	3.
	Split-Window covariance-variance ratio

	tau_j / tau_i = epsilon_i * R_ji / epsilon_j aeq R_ji = convariance / variance
	R = tau_j / tau_i
	wv = aR^2 + bR + c
	MODIS Landsat S3/SLSTR GF5/VIMS HJ-2 0.5g/cm^2

	high calibretion requirements and low noise level
	perform poorly in water body

	4. 
	NWP based method
	'''
    def __init__(self):
        pass
