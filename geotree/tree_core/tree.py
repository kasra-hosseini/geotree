#!/usr/bin/env python
# -*- coding: UTF-8 -*-

__author__ = "Kasra Hosseini"
__license__ = "MIT License"

import numpy as np
from scipy import spatial
from sklearn.neighbors import BallTree
from typing import Union

from geotree.utils import convert

class gtree:
    def __init__(self):
        # xyz: base
        # kdt: kd-tree created from base
        # xyz_q: query
        self.xyz = None
        self.xyz_q = None
        self.kdt = None
        self.balltree = None
        self.earth_radius = 6371000

    def add_lonlatdep(self, 
                      lons: Union[float, int, np.ndarray, list], 
                      lats: Union[float, int, np.ndarray, list], 
                      depths: Union[float, int, np.ndarray, list, None]=None,
                      convert2xyz: bool=True):
        """Add lons/lats/depths of the base

        Parameters
        ----------
        lons : Union[float, int, np.ndarray, list]
        lats : Union[float, int, np.ndarray, list]
        depths : Union[float, int, np.ndarray, list, None], optional
        """
        self.lons = lons
        self.lats = lats
        self.depths = depths
        if convert2xyz:
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
                            depths: Union[float, int, np.ndarray, list, None]=None,
                            convert2xyz: bool=True):
        """Add lons/lats/depths of the queries

        Parameters
        ----------
        lons : Union[float, int, np.ndarray, list]
        lats : Union[float, int, np.ndarray, list]
        depths : Union[float, int, np.ndarray, list, None], optional
        """
        self.lons_q = lons
        self.lats_q = lats
        self.depths_q = depths
        if convert2xyz:
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

    def create_kdt(self):
        """Create a KD-tree based on self.xyz
        """
        if self.xyz is None:
            try:
                self.xyz = convert.lonlatdep2xyz(self.lons, self.lats, self.depths)
            except Exception:
                print("[ERROR] xyz could not be found! Use add_lonlatdep_query.")
                return None
        self.kdt = spatial.cKDTree(self.xyz)
    
    def query_kdt(self, 
                  num_neighs: int=4, 
                  distance_upper: Union[int, float]=np.inf):
        """Query self.kdt (kd-tree)

        Parameters
        ----------
        num_neighs : int, optional
        distance_upper : Union[int, float, np.inf], optional
        """
        if self.xyz_q is None:
            try:
                self.xyz_q = convert.lonlatdep2xyz(self.lons_q, self.lats_q, self.depths_q)
            except Exception:
                print("[ERROR] Query's xyz_q could not be found! Use add_lonlatdep.")
                return None

        if self.kdt is None:
            print("[WARNING] kdt could not be found.")
            print("[WARNING] create kd-tree...")
            self.create_kdt()
            print("done")

        self.dists2query, self.indxs2query = \
            self.kdt.query(self.xyz_q, 
            k=num_neighs, 
            distance_upper_bound=distance_upper)
    
    def query_balltree(self, 
                       num_neighs: int=4):
        """Query self.balltree 

        Parameters
        ----------
        num_neighs : int, optional
        distance_upper : Union[int, float, np.inf], optional
        """

        if self.balltree is None:
            print("[WARNING] balltree could not be found.")
            print("[WARNING] create balltree...")
            self.create_balltree()
            print("done")

        self.dists2query, self.indxs2query = \
            self.balltree.query(np.radians(np.vstack([self.lats_q, self.lons_q]).T), 
                                k=num_neighs)
        self.dists2query *= self.earth_radius
    
    def create_balltree(self):
        self.balltree = BallTree(np.radians(np.vstack([self.lats, self.lons]).T), 
                                 metric="haversine")
    
    def interpolate(self, 
                    num_neighs: int=4, 
                    method: str="kdtree",
                    diveps: float=1e-10):
        """Interpolate values of one grid into another one

        Parameters
        ----------
        num_neighs : int, optional
        diveps : float, optional
        """
    
        # 1. dists/indices of neighbouring points
        self.interp_method = method
        if method == "kdtree":
            self.query_kdt(num_neighs)
        elif method == "balltree":
            self.query_balltree(num_neighs)
        else:
            print(f"method: {method} is not implemented!")
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