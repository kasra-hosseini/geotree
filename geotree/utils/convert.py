#!/usr/bin/env python
# -*- coding: UTF-8 -*-

__author__ = "Kasra Hosseini"
__license__ = "MIT License"

import numpy as np
import pyproj
from typing import Union

# Define projections
ecef = pyproj.Proj(proj='geocent', ellps='WGS84', datum='WGS84')
lla = pyproj.Proj(proj='latlong', ellps='WGS84', datum='WGS84')

def lonlatdep2xyz(lons: Union[float, int, np.ndarray, list], 
                  lats: Union[float, int, np.ndarray, list], 
                  depths: Union[float, int, np.ndarray, list, None]=None,
                  return_one_arr: Union[bool]=True):
    """Convert lons/lats/depths to xyz

    Parameters
    ----------
    lons : Union[float, int, np.ndarray, list]
    lats : Union[float, int, np.ndarray, list]
    depths : Union[float, int, np.ndarray, list, None], optional
    return_one_arr : Union[bool], optional
    """

    lons = convert2array(lons)
    lats = convert2array(lats)
    if depths is None:
        depths = np.ones(len(lons))
    else:
        depths = convert2array(depths)

    # trainsform to x, y, z (in meters)
    x, y, z = pyproj.transform(lla, ecef,
                               lons, lats, depths,
                               radians=False)

    if return_one_arr:
        return np.vstack([x, y, z]).T 
    else:
        return x, y, z

def convert2array(myinp):
    """Convert myinp ---> np.ndarray"""
    if isinstance(myinp, np.ndarray):
        return myinp
    elif isinstance(myinp, list):
        return np.array(myinp)
    elif isinstance(myinp, int):
        return np.array([myinp])
    elif isinstance(myinp, float):
        return np.array([myinp])
    else:
        print(f"WARNING: input type cannot be converted: {type(myinp)}")
        return None