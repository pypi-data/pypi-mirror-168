#!/usr/bin/env python3
#-*- coding:utf-8 -*-


import os
import sys
import time
import argparse
import requests
import warnings
from datetime import date
from netrc import netrc
from urllib3.exceptions import InsecureRequestWarning
from getpass import getpass
from subprocess import Popen
from collections import OrderedDict
from sentinelsat import SentinelAPI

# warnings.filterwarnings("ignore")
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
# query_kwargs = {
#         'platformname': 'Sentinel-2',
#         'producttype': 'S2MSI1C',
#         'date': ('NOW-14DAYS', 'NOW'),
#         'orbitdirection': 'ASCENDING',
#         'cloudcoverpercentage': (0, 30),
#         }

USERNAME = 'peterzhu'
PASSWORD = 'R#7qpDVCn&6Ub6L'
API_URL  = 'https://scihub.copernicus.eu/dhus'
LST_PROD = 'SL_2_LST___'
RBT_PROD = 'SL_1_RBT___'


class S3Downloader(object):
	def __init__(self):
		self.api = SentinelAPI(USERNAME, PASSWORD, API_URL)

	def query(self, platformname='Sentinel-3', producttype=RBT_PROD, date_ = ('NOW-14DAYS', 'NOW'), **kvargs):
		'''query to retrieve S3 data information, more details on https://scihub.copernicus.eu/userguide/FullTextSearch
		'''
		query_dict = {
				'platformname': platformname,
				'producttype': 'SL_2_LST___',
				'date': date_, # date(2019, 10, 28)
				# 'orbitdirection': 'ASCENDING',  # DESCENDING day / night
				# 'cloudcoverpercentage': 0,
			}
		return self.api.query(**query_dict)

	def query_download(self, platformname='Sentinel-3', producttype=RBT_PROD, date_ = ('NOW-14DAYS', 'NOW'), **kvargs):
		'''retrieve metadata of RBT product and download'''
		self.api.download_all(self.query(platformname, producttype, date_, **kvargs))

	def download(self, identifier):
		products = self.api.query(identifier=identifier)
		product_id = list(products)[0]
		self.api.download(product_id)

	def get_product_info(self, identifier):
		products = self.api.query(identifier=identifier)
		product_id = list(products)[0]
		print(self.api.get_product_odata(product_id))


def main():
	s3 = S3Downloader()
	# s3.query_download(date_=('2019-10-28T00:00:00.000Z', '2019-10-28T23:59:59.999Z'))
	identifier = 'S3B_SL_1_RBT____20190101T035522_20190101T035822_20190102T122833_0180_020_218_2520_LN2_O_NT_003'
	print(s3.download(identifier))
	# from osgeo import gdal
	# import numpy as np

	# filename = r'S2A.jp2'

	# class sentinel:
	# 	def read_img(self, filename):
	# 		ds = gdal.Open(filename)
	# 		Xsize = ds.RasterXSize
	# 		Ysize = ds.RasterYSize
	# 		bnum = ds.RasterCount

	# 		data = ds.ReadAsArray(0, 0, Xsize, Ysize)
	# 		proj = ds.GetProjection()
	# 		geotrans = ds.GetGeoTransform()

	# 		return proj, geotrans, data, Xsize, Ysize, bnum

	# 	def write_img(self, filename, outfile):
	# 		proj, geotrans, data, width, height, bands = self.read_img(filename)
	# 		driver = gdal.GetDriverByName('GTiff')
	# 		ds = driver.Create(outfile, width, height, bands, gdal.GDT_UInt16)
	# 		ds.SetGeoTransform(geotrans)
	# 		ds.SetProjection(proj)

	# 		if bands==1:
	# 			ds.GetRasterBand(1).WriteArray(data)
	# 		else:
	# 			for i in range(1, bands+1):
	# 				ds.GetRasterBand(i).WriteArray(data)
	# 		del ds

	# run = sentinel()
	# proj, geotrans, data = run.read_img(filename)
	# print(np.shape(data))


if __name__ == '__main__':
	pass
	# main()
	# s3 = S3Downloader()
	# identifier = sys.argv[1]
	# s3.download(identifier)
