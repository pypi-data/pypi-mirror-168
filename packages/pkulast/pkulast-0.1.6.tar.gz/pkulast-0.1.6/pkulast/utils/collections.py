from __future__ import unicode_literals
import sys
import os
import logging
import requests
import urllib
import datetime
import numpy as np
from datetime import timezone
import matplotlib.pyplot as plt
from pysolar.solar import get_altitude, get_azimuth
from pkulast.config import DEM_DIR

sys.setrecursionlimit(1500)
LOG = logging.getLogger(__name__)


def get_elevation(lat, lon, method="linear"):
    # “linear”, “nearest”, “zero”, “slinear”, “quadratic”, “cubic”
    import rioxarray
    ds = rioxarray.open_rasterio(DEM_DIR)
    elev = np.squeeze(ds.interp(x=lon, y=lat, method=method).values)
    ds = None
    return elev / 1e3  #km


def get_elevation_online(lat, lon):
    """ get elevation from fixed point.
	"""
    url = r'https://api.opentopodata.org/v1/mapzen?'
    params = {
     'locations': f'{lat}, {lon}',
     'interpolation': 'cubic'
    }
    result = requests.get((url + urllib.parse.urlencode(params)))
    elevation = result.json()['results'][0]['elevation']
    return float(elevation) / 1000

def get_sun_position(lat, lon, date):
    """ solar zenith angle, solar azimuth angle
	"""
    return 90 -  get_altitude(lat, lon, date), get_azimuth(lat, lon, date)

def is_day(lat, lon, date):
    """ check whether specific date somewhere is day or not
	"""
    sza = 90 -  get_altitude(lat, lon, date)
    return sza <=90 and sza >=0

def get_bj_time():
    """ get current beijing time.
	"""
    utc_dc = datetime.datetime.now().replace(tzinfo=timezone.utc)
    bj_dt = utc_dc.astimezone(datetime.timezone(datetime.timedelta(hours=8)))
    return bj_dt.strftime('%Y-%m-%d %H:%M:%S')

def sort_data(x_vals, y_vals):
    """Sort the data so that x is monotonically increasing and contains no duplicates."""
    # Sort data
    # (This is needed in particular for EOS-Terra responses, as there are duplicates)
    idxs = np.argsort(x_vals)
    x_vals = x_vals[idxs]
    y_vals = y_vals[idxs]

    # De-duplicate data
    mask = np.r_[True, (np.diff(x_vals) > 0)]
    if not mask.all():
        numof_duplicates = np.repeat(mask, np.equal(mask, False)).shape[0]
        LOG.debug("Number of duplicates in the response function: %d - removing them",
                  numof_duplicates)
    x_vals = x_vals[mask]
    y_vals = y_vals[mask]

    return x_vals, y_vals

def convert2str(value):
    """Convert a value to string.
    Args:
        value: Either a str, bytes or 1-element numpy array
    """
    value = bytes2string(value)
    return np2str(value)

def np2str(value):
    """Convert an `numpy.string_` to str.
    Args:
        value (ndarray): scalar or 1-element numpy array to convert
    Raises:
        ValueError: if value is array larger than 1-element or it is not of
                    type `numpy.string_` or it is not a numpy array
    """
    if isinstance(value, str):
        return value

    if hasattr(value, 'dtype') and \
            issubclass(value.dtype.type, (np.str_, np.string_, np.object_)) \
            and value.size == 1:
        value = value.item()
        # python 3 - was scalar numpy array of bytes
        # otherwise python 2 - scalar numpy array of 'str'
        if not isinstance(value, str):
            return value.decode()
        return value

    raise ValueError("Array is not a string type or is larger than 1")

def bytes2string(var):
    """Decode a bytes variable and return a string."""
    if isinstance(var, bytes):
        return var.decode('utf-8')
    return var

def get_cmap(n, name='hsv'):
    ''' Returns a function that maps each index in 0, 1, ..., n-1 to a distinct
	RGB color; the keyword argument name must be a standard mpl colormap name.'''
    return plt.cm.get_cmap(name, n)

# from array to bytes
tobytes = lambda array: array.tobytes()
frombytes = lambda array, src: array.frombytes(src)

# read/open file function
def readline(fin): return fin.readline()
def open_file(filename): return open(filename, encoding='iso-8859-1')

# find file
def find_file_path(filename):
    '''
    Search cwd and SPECTRAL_DATA directories for the given file.
    '''
    pathname = None
    dirs = [os.curdir]
    if 'SPECTRAL_DATA' in os.environ:
        dirs += os.environ['SPECTRAL_DATA'].split(os.pathsep)
    for d in dirs:
        testpath = os.path.join(d, filename)
        if os.path.isfile(testpath):
            pathname = testpath
            break
    if not pathname:
        msg = 'Unable to locate file "%s". If the file exists, ' \
          'use its full path or place its directory in the ' \
          'SPECTRAL_DATA environment variable.'  % filename
        raise FileNotFoundError(msg)
    return pathname
