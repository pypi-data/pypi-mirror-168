#!/usr/bin/env python3
#-*- coding:utf-8 -*-


'''
Remote sensing data Reader.
=====

Provides remote sensing data readers for a variety of satellite-borne/airborne sensors

'''
import glob
import warnings
import numpy as np
from pyproj import CRS
from affine import Affine
from datetime import datetime
import matplotlib.pyplot as plt
from dask.diagnostics import ProgressBar

from satpy.scene import Scene
from satpy.dataset import combine_metadata
from satpy import find_files_and_readers, available_writers
from pyresample import load_area, save_quicklook, SwathDefinition, create_area_def, get_area_def, image, geometry
warnings.filterwarnings("ignore")

from pkulast.utils.raster import utmcode


class Reader(object):
	""" Abstract Reader for satellite-borne/air-borne rs data
	"""
	def __init__(self, filepath):
		self.filepath = filepath
		self.lats = None
		self.lons = None
		self.scene = None

	def load_data(self):
		pass
	
	def available_datasets(self):
		if self.scene is not None:
			return self.scene.available_dataset_names()
		else:
			return None

	def quick_look(self, dataset, cmp='Spectral_r'):
		self.scene[dataset].plot.imshow(cmap=cmp)
		plt.show()

	def get_corners(self):
		swath_def = SwathDefinition(lons=self.lons, lats=self.lats)
		return swath_def.corners
	
	def get_extent(self):
		max_lat = float(self.scene['latitude'].max().values)
		min_lat = float(self.scene['latitude'].min().values)
		max_lon = float(self.scene['longitude'].max().values)
		min_lon = float(self.scene['longitude'].min().values)
		return (min_lat, max_lat, min_lon, max_lon)

	def get_swath_def(self):
		return SwathDefinition(lons=self.lons, lats=self.lats)

	def add_data(self, dataset, array, show_fig=False):
		self.scene[dataset] = array
		self.scene[dataset].attrs = self.scene['longitude'].attrs
		self.scene[dataset].attrs['name'] = dataset
		if show_fig:
			self.quick_look(dataset)
	
	def diff(self, datasetA, datasetB, key=None, show_fig=False):
		if not key:
			key = 'diff_{}_{}'.format(datasetA, datasetB)
		left = self.scene[datasetA]
		right = self.scene[datasetB]
		self.scene[key] = left - right
		self.scene[key].attrs = combine_metadata(left, right)
		self.scene[key].attrs['name'] = key
		if show_fig:
			self.quick_look(key)
		return self.scene[key].values

	def resample(self, areadef):
		self.scene = self.scene.resample(areadef)

	def get_area_def(self, dataset, proj="UTM", utmzone=None):
		center = [int(self.lats.shape[1]/2)-1, int(self.lats.shape[0]/2)-1]
		center_latitude, center_longitude = float(self.lats[center[0]][center[1]]), float(self.lons[center[0]][center[1]])
		if proj == "UTM":
			if utmzone is None:
				epsg = utmcode(center_latitude, center_longitude)
			else:
				epsg = utmzone
			proj_dict = {'proj': 'utm', 'zone': epsg[-2:], 'ellps': 'WGS84', 'datum': 'WGS84', 'units': 'm'}
			if epsg[2] == "7":
				proj_dict['south'] = 'True'
		elif proj == "GEO":
			epsg = "4326"
			proj_dict = {'proj': 'longlat', 'datum': 'WGS84'}
		area_def = self.scene[dataset].area.compute_optimal_bb_area(proj_dict)

	def save_tiff(self, dataset, filename, proj="UTM", utmzone=None, fill_value=np.nan):
		# lons, lats = self.scene[dataset].area.get_lonlats()
		lines, cols = self.lons.shape
		center_latitude, center_longitude = float(self.lats[int(lines / 2), int(cols / 2)]) , float(self.lons[int(lines / 2), int(cols / 2)])
		if proj == "UTM":
			if utmzone is None:
				epsg = utmcode(center_latitude, center_longitude)
			else:
				epsg = utmzone
			proj_dict = {'proj': 'utm', 'zone': epsg[-2:], 'ellps': 'WGS84', 'datum': 'WGS84', 'units': 'm'}
			if epsg[2] == "7":
				proj_dict['south'] = 'True'
		elif proj == "GEO":
			epsg = "4326"
			proj_dict = {'proj': 'longlat', 'datum': 'WGS84'}
		area_def = self.scene[dataset].area.compute_optimal_bb_area(proj_dict)
		new_scn = self.scene.resample(area_def, nprocs=4) # resampler='bilinear', 
		height, width = new_scn[dataset].shape
		profile = {
				'affine': Affine(area_def.pixel_size_x, 0.0, area_def.area_extent[0], 0.0, -area_def.pixel_size_y, area_def.area_extent[3]),
				'count': 1,
				'crs': CRS(f'EPSG:{epsg}'),
				'driver': 'GTiff',
				'dtype': np.float32,
				'height': height,
				'interleave': 'band',
				'nodata': fill_value,
				'tiled': False,
				'transform': (area_def.area_extent[0], area_def.pixel_size_x, 0.0, area_def.area_extent[3], 0.0, -area_def.pixel_size_y),  
				'width': width}
		with ProgressBar():
			new_scn.save_dataset(dataset, filename=filename, writer='geotiff', enhance=False, **profile)

	def save_nc(self, dataset, filename):
		with ProgressBar():
			self.scene.save_datasets( datasets= dataset, 
									  writer='cf', 
									  filename= filename, 
									  exclude_attrs=['raw_metadata'],
									  engine='netcdf4')

	def exists(self, dataset):
		if self.available_datasets() and dataset in self.available_datasets():
			return True
		return False

	def __getitem__(self, dataset):
		if self.exists(dataset):
			return self.scene[dataset].values
		raise ValueError(f'no dataset named {dataset}.')

class SLSTRReader(Reader):
	""" Sentinel 3 slstr Reader
	"""
	def __init__(self, filepath):
		super().__init__(filepath)

	def load_data(self, start_time, end_time):
		files = find_files_and_readers(sensor='slstr',
							   start_time=start_time,
							   end_time=end_time,
							   base_dir=self.filepath,
							   reader='slstr_l1b')
		self.scene = Scene(filenames=files)
		noneed = ['F1', 'F2', 'satellite_zenith_angle','satellite_azimuth_angle', 'pointing', 
		'satellite_azimuth_angle', 'solar_zenith_angle', 'solar_azimuth_angle', 'bayes', 
		'confidence','pointing', 'cloud']
		keys = self.scene.available_dataset_names()
		self.available_dataset_names = list(set(keys) - set(noneed))
		self.scene.load(self.available_dataset_names)
		self.lats = self.scene['latitude']
		self.lons = self.scene['longitude']
		self.start_time = self.scene['latitude'].attrs['start_time']
		self.end_time = self.scene['latitude'].attrs['end_time']

	@property
	def tir_data(self):
		S7 = self.scene['S7'].values
		S8 = self.scene['S8'].values
		S9 = self.scene['S9'].values
		return np.array((S7, S8, S9))

class MERSI2Reader(Reader):
	""" FY-3D mersi2 reader
	"""
	def __init__(self, filepath):
		super().__init__(filepath)
		self.load_data()

	
	def load_data(self):
		""" Load dataset
		"""
		self.scene = Scene(filenames=glob.glob(self.filepath + "/*.HDF"), reader="mersi2_l1b")
		self.scene.load(self.available_datasets())
		self.lats = self.scene['latitude']
		self.lons = self.scene['longitude']
		self.start_time = self.scene['latitude'].attrs['start_time']
		self.end_time = self.scene['latitude'].attrs['end_time']

	@property
	def tir_data(self):
		B22 = self.scene['22'].values
		B23 = self.scene['23'].values
		B24 = self.scene['24'].values
		B25 = self.scene['25'].values
		return np.array((B22, B23, B24, B25))