# -*- coding:utf-8 -*-
# Copyright (c) 2021-2022.

################################################################
# The contents of this file are subject to the GPLv3 License
# you may not use this file except in
# compliance with the License. You may obtain a copy of the License at
# https://www.gnu.org/licenses/gpl-3.0.en.html

# Software distributed under the License is distributed on an "AS IS"
# basis, WITHOUT WARRANTY OF ANY KIND, either express or implied. See the
# License for the specific language governing rights and limitations
# under the License.

# The Original Code is part of the PKULAST python package.

# Initial Dev of the Original Code is Jinshun Zhu, PhD Student,
# Institute of Remote Sensing and Geographic Information System,
# Peking Universiy Copyright (C) 2022
# All Rights Reserved.

# Contributor(s): Jinshun Zhu (created, refactored and updated original code).
###############################################################
"""
Common utilities.

"""
import requests
import urllib
import numpy as np
from datetime import datetime
import pylab as plt
from pysolar import solar


__all__ = [
    'str2fp',
    'str2int',
    'str2date',
    'get_elevation',
    'get_sun_position',
    'is_daytime',
    'get_bj_time',
    'get_cmap'
]


def str2fp(num):
    """
    Convert string to float.
    Args:
        num (str): String.
    Returns:
        float: Float.
    """
    try:
        return float(num.strip())
    except Exception as ex:
        raise ValueError(
            f"{ex}, input string can not converted to float point number")


def str2int(num):
    """
    Convert string to int.
    Args:
        num (str): String.
    Returns:
        int: Int.
    """
    try:
        return int(num.strip())
    except Exception as ex:
        raise ValueError(f"{ex},input string can not converted to integer")


def str2date(date_str):
    """
    Convert string to date.
    Args:
        date_str (str): String.
    Returns:
        datetime.datetime: Date.
    """
    year = 1900 + int(date_str[:2])
    month = int(date_str[2:4])
    day = int(date_str[4:])
    if day:
        return datetime(year, month, day)
    else:  # dd is not defined
        return datetime(year, month, day + 1)
        # return f"{year}-{month:02d}-na"


def get_elevation(lat, lon):
    """
    Get elevation from latitude and longitude.

    Args:
        lat (float or ndarray): Latitude.
        lon (float or ndarray): Longitude.

    Returns:
        float or ndarray: Elevation. unit:km

    Examples:
        >>> get_elevation(30, 120)
        0.0
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
    """
    Get sun position from latitude, longitude and date.

    Args:
        lat (float or ndarray): Latitude.
        lon (float or ndarray): Longitude.
        date (datetime.datetime or ndarray): Date.

    Returns:
        float or ndarray: Sun position.

    Examples:
        >>> get_sun_position(30, 120, datetime.datetime(2020, 1, 1))
        0.0
    """
    return 90 - solar.get_altitude(lat, lon, date), solar.get_azimuth(lat, lon, date)


def is_daytime(lat, lon, date):
    """
    Check if it is daytime.

    Args:
        lat (float or ndarray): Latitude.
        lon (float or ndarray): Longitude.
        date (datetime.datetime or ndarray): Date.

    Returns:
        bool or ndarray: True if it is daytime.

    Examples:
        >>> is_daytime(30, 120, datetime.datetime(2020, 1, 1))
        True
    """
    sun_position = get_sun_position(lat, lon, date)
    return sun_position[0] > 0 and sun_position[0] <= 90

def get_bj_time():
    """
    Get Beijing time.

    Returns:
        datetime.datetime: Beijing time.

    Examples:
        >>> get_bj_time()
        datetime.datetime(2020, 1, 1, 0, 0)
    """
    bj_dt = datetime.utcnow() + datetime.timedelta(hours=8)
    return bj_dt.strftime('%Y-%m-%d %H:%M:%S')


def get_cmap(n, name='hsv'):
    """
    Get color map.

    Args:
        n (int): Number of colors.
        name (str): Color map name.

    Returns:
        matplotlib.colors.ListedColormap: Color map.

    Examples:
        >>> get_cmap(10)
        <matplotlib.colors.ListedColormap object at 0x7f0e7f8c8e10>
    """
    return plt.cm.get_cmap(name, n)

def sort_array(x_vals, y_vals):
    """
    Sort array by x_vals in descending order.

    Args:
        x_vals (ndarray): X values.
        y_vals (ndarray): Y values.

    Returns:
        ndarray: Sorted x_vals.
        ndarray: Sorted y_vals.

    Examples:
        >>> sort_array(np.array([1, 2, 3]), np.array([4, 5, 6]))
        (array([1, 2, 3]), array([4, 5, 6]))
    """
    x_vals, y_vals = np.array(x_vals), np.array(y_vals)
    idx = np.argsort(x_vals)
    x_vals = x_vals[idx]
    y_vals = y_vals[idx]

    # Delete duplicate x_vals
    mask = np.r_[True, (np.diff(x_vals)>0)]
    # if not mask.all():
    #     num_of_duplicates = np.repeat(mask, np.equal(mask, False)).shape[0]
    x_vals = x_vals[mask]
    y_vals = y_vals[mask]
    return x_vals, y_vals
