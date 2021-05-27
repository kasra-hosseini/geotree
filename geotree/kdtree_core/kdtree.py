#!/usr/bin/env python
# -*- coding: UTF-8 -*-

__author__ = "Kasra Hosseini"
__license__ = "MIT License"

import numpy as np
from scipy import spatial
from typing import Union

from geotree.utils import convert

class gkdtree:
    def __init__(self):
        # xyz: base
        # kdt: kd-tree created from base
        # xyz_q: query
        self.xyz = None
        self.kdt = None
        self.xyz_q = None

    def add_lonlatdep(self, 
                      lons: Union[float, int, np.ndarray, list], 
                      lats: Union[float, int, np.ndarray, list], 
                      depths: Union[float, int, np.ndarray, list, None]=None):
        """Add lons/lats/depths of the base

        Parameters
        ----------
        lons : Union[float, int, np.ndarray, list]
        lats : Union[float, int, np.ndarray, list]
        depths : Union[float, int, np.ndarray, list, None], optional
        """
        self.xyz = convert.lonlatdep2xyz(lons, lats, depths)
    
    def add_vals(self,
                 vals: Union[float, int, np.ndarray, list]):
        """Add values (e.g., for interpolation)

        Parameters
        ----------
        vals : Union[float, int, np.ndarray, list]
        """
        if len(vals) != self.xyz.shape[0]:
            print(f"[ERROR] vals should have {self.xyz.shape[0]} values")
            return None
        self.vals = convert.convert2array(vals)
    
    def add_lonlatdep_query(self, 
                            lons: Union[float, int, np.ndarray, list], 
                            lats: Union[float, int, np.ndarray, list], 
                            depths: Union[float, int, np.ndarray, list, None]=None):
        """Add lons/lats/depths of the queries

        Parameters
        ----------
        lons : Union[float, int, np.ndarray, list]
        lats : Union[float, int, np.ndarray, list]
        depths : Union[float, int, np.ndarray, list, None], optional
        """
        self.xyz_q = convert.lonlatdep2xyz(lons, lats, depths)

    def add_xyz(self, 
                x: Union[list, np.ndarray], 
                y: Union[list, np.ndarray], 
                z: Union[list, np.ndarray]):
        """Add x/y/z of the base

        Parameters
        ----------
        x : Union[list, np.ndarray]
        y : Union[list, np.ndarray]
        z : Union[list, np.ndarray]
        """
        x = convert.convert2array(x)
        y = convert.convert2array(y)
        z = convert.convert2array(z)
        self.xyz = np.vstack([x, y, z]).T
    
    def add_xyz_q(self, 
                  x: Union[list, np.ndarray], 
                  y: Union[list, np.ndarray], 
                  z: Union[list, np.ndarray]):
        """Add x/y/z of the query

        Parameters
        ----------
        x : Union[list, np.ndarray]
        y : Union[list, np.ndarray]
        z : Union[list, np.ndarray]
        """
        x = convert.convert2array(x)
        y = convert.convert2array(y)
        z = convert.convert2array(z)
        self.xyz_q = np.vstack([x, y, z]).T

    def create_tree(self):
        """Create a KD-tree based on self.xyz
        """
        if self.xyz is None:
            print("[ERROR] xyz could not be found! Use add_lonlatdep.")
            return None
        self.kdt = spatial.cKDTree(self.xyz)
    
    def query(self, 
              num_neighs: int=4, 
              distance_upper: Union[int, float]=np.inf):
        """Query self.kdt (kd-tree)

        Parameters
        ----------
        num_neighs : int, optional
        distance_upper : Union[int, float, np.inf], optional
        """
        if self.kdt is None:
            print("[WARNING] kdt could not be found.")
            print("[WARNING] create kd-tree...")
            self.create_tree()
            print("done")
        self.dists2query, self.indxs2query = \
            self.kdt.query(self.xyz_q, 
            k=num_neighs, 
            distance_upper_bound=distance_upper)
    
    def interpolate(self, 
                    num_neighs: int=4, 
                    diveps: float=1e-10):
        """Interpolate values of one grid into another one

        Parameters
        ----------
        num_neighs : int, optional
        diveps : float, optional
        """
    
        # 1. dists/indices of neighbouring points
        self.query(num_neighs)
        if num_neighs == 1:
            self.dists2query = self.dists2query.reshape(-1, 1)
            self.indxs2query = self.indxs2query.reshape(-1, 1)

        # 2. weights
        self.dists2query[self.dists2query < diveps] = diveps 
        weights = np.divide(1., self.dists2query)

        # 3. weighted values
        weighted_vals = weights*self.vals[self.indxs2query] 
        self.interp_vals = \
            np.sum(weighted_vals, axis=1)/np.sum(weights, axis=1)