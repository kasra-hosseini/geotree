#!/usr/bin/env python
# -*- coding: UTF-8 -*-

__author__ = "Kasra Hosseini"
__license__ = "MIT License"

import numpy as np
from typing import Union

try:
    import pyproj
    pyproj_imported = True
except ImportError:
    pyproj_imported = False


def lonlatdep2xyz_spherical(lons: Union[float, int, np.ndarray, list], 
                            lats: Union[float, int, np.ndarray, list], 
                            depths: Union[float, int, np.ndarray, list, None]=None,
                            return_one_arr: Union[bool]=True, 
                            earth_radius_m: Union[float, int]=6371000):
    """Convert lons/lats/depths to x/y/z

    Parameters
    ----------
    lons : Union[float, int, np.ndarray, list]
    lats : Union[float, int, np.ndarray, list]
    depths : Union[float, int, np.ndarray, list, None], optional
    return_one_arr : Union[bool], optional
    earth_radius_m : Union[float, int], optional
    """
    # co-latitudes:
    colats = 90.0 - lats
    # radii
    r = earth_radius_m - depths

    x = r * np.sin(np.deg2rad(colats)) * np.cos(np.deg2rad(lons))
    y = r * np.sin(np.deg2rad(colats)) * np.sin(np.deg2rad(lons))
    z = r * np.cos(np.deg2rad(colats))

    if return_one_arr:
        return np.vstack([x, y, z]).T 
    else:
        return x, y, z

def xyz2lonlatdep_spherical(x: Union[float, int, np.ndarray, list], 
                            y: Union[float, int, np.ndarray, list], 
                            z: Union[float, int, np.ndarray, list, None]=None,
                            return_one_arr: Union[bool]=True, 
                            earth_radius_m: Union[float, int]=6371000):
    """Convert x/y/z/ to lons/lats/depths

    Parameters
    ----------
    x : Union[float, int, np.ndarray, list]
    y : Union[float, int, np.ndarray, list]
    z : Union[float, int, np.ndarray, list, None], optional
    return_one_arr : Union[bool], optional
    earth_radius_m : Union[float, int], optional
    """
    rxy = np.sqrt(x**2 + y**2)
    lons = np.arctan2(y, x)*180./np.pi
    lats = np.arctan2(z, rxy)*180./np.pi
    depths = earth_radius_m - np.sqrt(x**2 + y**2 + z**2)

    if return_one_arr:
        return np.vstack([lons, lats, depths]).T 
    else:
        return lons, lats, depths

def lonlatdep2xyz(lons: Union[float, int, np.ndarray, list], 
                  lats: Union[float, int, np.ndarray, list], 
                  depths: Union[float, int, np.ndarray, list, None]=None,
                  return_one_arr: Union[bool]=True):
    """Convert lons/lats/depths to x/y/z

    Parameters
    ----------
    lons : Union[float, int, np.ndarray, list]
    lats : Union[float, int, np.ndarray, list]
    depths : Union[float, int, np.ndarray, list, None], optional
    return_one_arr : Union[bool], optional
    """
    
    if not pyproj_imported:
        print(f"[WARNING] pyproj could not be imported.")
        print(f"[WARNING] lonlatdep2xyz_spherical will be used insted.")
        lonlatdep2xyz_spherical(lons, lats, depths, return_one_arr)
    
    # Define projections
    ecef = pyproj.Proj(proj='geocent', ellps='WGS84', datum='WGS84')
    lla = pyproj.Proj(proj='latlong', ellps='WGS84', datum='WGS84')

    lons = convert2array(lons)
    lats = convert2array(lats)
    if depths is None:
        depths = np.ones(len(lons))
    else:
        depths = convert2array(depths)

    # trainsform to x, y, z (in meters)
    # -1 * depth as pyproj.transform expects altitude
    x, y, z = pyproj.transform(lla, ecef,
                               lons, lats, -1*depths,
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