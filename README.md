<div align="center">
    <br>
    <h2>GeoTree: nearest-neighbors on geographic coordinates</h2>
</div>

<p align="center">
    <a href="https://github.com/kasra-hosseini/geotree/blob/main/LICENSE">
        <img alt="License" src="https://img.shields.io/badge/License-MIT-yellow.svg">
    </a>
    <br>
    <p align="center">
        <img src="./images/header.png" alt="header" width="80%" align="center">
    </p>
    </br>
</p>

Table of contents
-----------------

- [Installation and setup](#installation)
- [Tutorials](#tutorials)
  - [Find closest neighbors (KDTree and BallTree)](#find-closest-neighbors-kdtree-and-balltree)
  - [Interpolate values of one grid into another one](#interpolate-values-of-one-grid-into-another-one)
  - [Conversion between lon/lat/depth and x/y/z](#conversion-between-lonlatdepth-and-xyz)
- [Tree build and query times, comparison between KDTree and BallTree](#tree-build-and-query-times-comparison)

## Installation

1. **install using pip**

    ```bash
    pip install git+https://github.com/kasra-hosseini/geotree.git
    ```

2. **install geotree from the source code**:

    * Clone geotree source code:

    ```bash
    git clone https://github.com/kasra-hosseini/geotree.git 
    ```

    * Install geotree:

    ```
    cd /path/to/my/geotree
    pip install -v -e .
    ```

    Alternatively:

    ```
    cd /path/to/my/geotree
    python setup.py install
    ```
  
# Tutorials

## Find closest neighbors (KDTree and BallTree)

:warning: [Jupyter notebook](notebooks/Find_closest_neighbors_kdtree_balltree.ipynb)

Instantiate gtree:

```python
from geotree import gtree
import matplotlib.pyplot as plt
import numpy as np

mytree = gtree()
```

Define the first set of points or `base`:

```python
npoints = 200
lons = np.random.randint(-180, 180, npoints)
lats = np.random.randint(-90, 90, npoints)
depths = np.zeros(npoints)
```

Add lons/lats/depths of the first set of points:

```python
mytree.add_lonlatdep(lons=lons, 
                     lats=lats, 
                     depths=depths)
```

:warning: NOTE: depth is specified with respect to the Earth surface and in meters. 
Its axis points towards the center of the Earth, that is, positive depths specify points inside the Earth.
Negative depths specify points above the Earth surface.

:warning: In the above example, we used `add_lonlatdep`. 
For KDTree, these values are converted into x/y/z (Cartesian coordinate system) internally (and in meters).
If you already have x/y/z in meters, you can use `add_xyz` function.

Define queries:

```python
q_npoints = 10
q_lons = np.random.randint(-150, 150, q_npoints)
q_lats = np.random.randint(-70, 70, q_npoints)
q_depths = np.zeros(q_npoints)
```

Add lons/lats/depths of queries:

```python
mytree.add_lonlatdep_query(lons=q_lons, 
                           lats=q_lats, 
                           depths=q_depths)
```

:warning: NOTE: depth is specified with respect to the Earth surface and in meters. 
Its axis points towards the center of the Earth, that is, positive depths specify points inside the Earth.
Negative depths specify points above the Earth surface.

:warning: In the above example, we used `add_lonlatdep_query`. 
For KDTree, these values are converted into x/y/z (Cartesian coordinate system) internally (and in meters).
If you already have x/y/z in meters, you can use `add_xyz_q` function.

### Find neighbors, kdtree:

Create KDTree (kdt):

```python
mytree.create_kdt()
```

Choose the desired number of neighbors (and upper bound for distance, if needed):

```python
mytree.query_kdt(num_neighs=3, distance_upper=np.inf)
```

Now, for each query, distances to the closest `base` neighbors and their indices are stored in (row-wise):

```python
# distances to the closest `base` neighbors
mytree.dists2query

# indices of the closest `base` neighbors
mytree.indxs2query
```

The results are shown in the following figure. 
The `base` points are shown in black dots and the queries are shown by `X`.
The closest three `base` neighbors are connected to each query.

<p align="center">
  <img src="./images/find_closest_kdtree.png" width="100%" title="find nearest neighbors, KDTreee">
</p>

Same results but on a interrupted Goode homolosine projection:

<p align="center">
  <img src="./images/find_closest_kdtree_projected.png" width="100%" title="find nearest neighbors, KDTreee">
</p>

### Find neighbors, Ball tree:

Create Ball tree:

```python
mytree.create_balltree()
```

Choose the desired number of neighbors:

```python
mytree.query_balltree(num_neighs=3)
```

Now, for each query, distances to the closest `base` neighbors and their indices are stored in (row-wise):

```python
# distances to the closest `base` neighbors
mytree.dists2query

# indices of the closest `base` neighbors
mytree.indxs2query
```

## Interpolate values of one grid into another one

:warning: [Jupyter notebook](notebooks/Interpolate_one_grid_into_another.ipynb)

Here, we have a set of points, labelled as `base` in the figure below, with some values (i.e., colors of those points).
We also have another set of points, `queries` in the figure, for which we want to compute values using the values of `base`. 
`Geotree` uses the following algorithm for this task:
1. it creates a tree (KDTree or BallTree) for `base` points.
2. for a `query` point, it finds the closest neighbors from `base` (the number of neighbors is specified by the user, in the figure below, this number was 4). 
3. it assigns a value to the `query` point by computing the weighted average of the values of the neighboring `base` points. The weights are proportional to the inverse distance.

(See more results below)

<p align="center">
  <img src="./images/interp_4.png" width="100%" title="interpolation with 4 neighbours">
</p>

Instantiate gtree:

```python
from geotree import gtree
import numpy as np

mytree = gtree()
```

Define the first set of points or `base`:

```python
npoints = 100
lons = np.random.randint(-180, 180, npoints)
lats = np.random.randint(-90, 90, npoints)
depths = np.zeros(npoints)

# assign some values (to each point)
vals = np.zeros(npoints)
vals[:(npoints//2)] = 0
vals[(npoints//2):] = 1
```

Add lons/lats/depths of the first set of points:

```python
mytree.add_lonlatdep(lons=lons, 
                     lats=lats, 
                     depths=depths)
```

:warning: NOTE: depth is specified with respect to the Earth surface and in meters. 
Its axis points towards the center of the Earth, that is, positive depths specify points inside the Earth.
Negative depths specify points above the Earth surface.

:warning: In the above example, we used `add_lonlatdep`. 
For KDTree, these values are converted into x/y/z (Cartesian coordinate system) internally (and in meters).
If you already have x/y/z in meters, you can use `add_xyz` function

Define queries:

```python
q_npoints = 10000
q_lons = np.random.randint(-180, 180, q_npoints)
q_lats = np.random.randint(-90, 90, q_npoints)
q_depths = np.zeros(q_npoints)
```

Add lons/lats/depths of queries:

```python
mytree.add_lonlatdep_query(lons=q_lons, 
                           lats=q_lats, 
                           depths=q_depths)
```

:warning: NOTE: depth is specified with respect to the Earth surface and in meters. 
Its axis points towards the center of the Earth, that is, positive depths specify points inside the Earth.
Negative depths specify points above the Earth surface.

:warning: In the above example, we used `add_lonlatdep_query`. 
For KDTree, these values are converted into x/y/z (Cartesian coordinate system) internally (and in meters).
If you already have x/y/z in meters, you can use `add_xyz_q` function.

Assign values to the first set of points: (note: size of vals should be the same as the first set of points)

```python
mytree.add_vals(vals)
```

**Interpolation:** compute the values of `queries` from the values of `base` points:

## KDTree

As the first example, we consider one neighbor (i.e., only the value of the closest `base` point to a query is used)

```python
mytree.interpolate(num_neighs=1, method="kdtree")
```

<p align="center">
  <img src="./images/interp_1.png" width="100%" title="KDTree, interpolation with 1 neighbours">
</p>

```python
mytree.interpolate(num_neighs=2, method="kdtree")
```

<p align="center">
  <img src="./images/interp_2.png" width="100%" title="KDTree, interpolation with 2 neighbours">
</p>

Or on a interrupted Goode homolosine projection:

<p align="center">
  <img src="./images/interp_2_homolosine.png" width="100%" title="KDTree, interpolation with 2 neighbours">
</p>


```python
mytree.interpolate(num_neighs=10, method="kdtree")
```

<p align="center">
  <img src="./images/interp_10.png" width="100%" title="KDTree, interpolation with 10 neighbours">
</p>

## BallTree

In the above examples, we used KDTree, we can change the method to `Ball tree` by simply:

```python
mytree.interpolate(num_neighs=2, method="balltree")
```

<p align="center">
  <img src="./images/interp_2_bt.png" width="100%" title="Ball tree, interpolation with 2 neighbours">
</p>


To plot the above figures:

```python
import matplotlib.pyplot as plt
plt.figure(figsize=(15, 7))
plt.scatter(q_lons, q_lats, 
            c=mytree.interp_vals, 
            marker="x", 
            vmin=min(vals), vmax=max(vals),
            label="queries")

plt.scatter(lons, lats,
            c=vals, 
            marker="o",
            vmin=min(vals), vmax=max(vals), edgecolors="r",
            label="base",
            zorder=100)

plt.legend(bbox_to_anchor=(0., 1.01, 1., .05), 
           loc="right", ncol=2, 
           fontsize=16,
           borderaxespad=0.)

plt.title(f"Method: {mytree.interp_method}", size=16)
plt.colorbar()
plt.grid()
plt.tight_layout()
plt.show()
```

## Conversion between lon/lat/depth and x/y/z

:warning: [Jupyter notebook](notebooks/Conversion_between_lon-lat-depth_and_x-y-z.ipynb)

`geotree` can read lon/lat/depth or x/y/z as inputs. Here is a list of relevant functions:
- `add_lonlatdep` (depth should be in meters; positive depths specify points inside the Earth.)
- `add_lonlatdep_query` (same as above except for queries)
- `add_xyz` (in meters)
- `add_xyz_q` (for queries, in meters)

In this section, we show two functions in geotree: `lonlatdep2xyz_spherical` and `xyz2lonlatdep_spherical`. 
These are used internally to convert between lon/lat/dep and x/y/z.

```python
from geotree import convert as geoconvert
import matplotlib.pyplot as plt
import numpy as np
```

Define a set of lons/lats/depths:

```python
npoints = 100
lons = np.random.randint(-180, 180, npoints)
lats = np.random.randint(-90, 90, npoints)
depths = np.zeros(npoints)
```

### lons/lats/depths ---> x/y/z

Here, we use `geoconvert.lonlatdep2xyz_spherical` to convert lons/lats/depths ---> x/y/z (in meters)

:warning: We set depths to zeros, i.e., all points are on a sphere with a radius of 6371000 meters.

```python
x, y, z = geoconvert.lonlatdep2xyz_spherical(lons, 
                                             lats, 
                                             depths, 
                                             return_one_arr=False)
```

In the figure:
- Left pabel: in geographic coordinate
- Right panel: x/y/z in meters (on a sphere with radius of 6371000m)

<p align="center">
  <img src="./images/lonlat_xyz.png" width="100%" title="Conversion between lon/lat/depth and x/y/z">
</p

To plot the above figure:

```python
fig = plt.figure(figsize=(12, 5))

plt.subplot(1, 2, 1)

plt.scatter(lons, lats,
            c="k", 
            marker="o",
            zorder=100)

plt.xlabel("lons", size=20)
plt.ylabel("lats", size=20)
plt.xticks(size=14); plt.yticks(size=14)
plt.xlim(-180, 180); plt.ylim(-90, 90)
plt.grid()

# ---
ax = fig.add_subplot(1, 2, 2, projection='3d')

ax.scatter3D(x, y, z, c="k", marker="o");

ax.set_xlabel('X (m)', size=16)
ax.set_ylabel('Y (m)', size=16)
ax.set_zlabel('Z (m)', size=16)

plt.tight_layout()
plt.show()
```

### x/y/z ---> lons/lats/depths

Just as test, we now use `geoconvert.xyz2lonlatdep_spherical` to convert x/y/z back to lons/lats/depths:

```python
lons_conv, lats_conv, depths_conv = geoconvert.xyz2lonlatdep_spherical(x, y, z, 
                                                                       return_one_arr=False)
```

and, we measure the L1 error between original lons/lats/depths and the ones computed above:

```python
print(max(abs(lons - lons_conv)))
print(max(abs(lats - lats_conv)))
print(max(abs(depths - depths_conv)))
```

Outputs:

```bash
2.842170943040401e-14
2.842170943040401e-14
9.313225746154785e-10
```

## Tree build and query times, comparison

:warning: [Jupyter notebook](notebooks/Tree_build_query_times.ipynb)

The figure compares KDTree and Ball tree for build (left) and query (right) times.
The left panel shows the build time as a function of number of points used in the tree.
The build times of the two methods are very similar.
In the right panel, we first constructed a tree for one million points and then measured the time to
query this tree with different number of queries (x-axis).

See [this Jupyter notebook](notebooks/Tree_build_query_times.ipynb) for details. 

<p align="center">
  <img src="./images/build_query_times.png" width="100%" title="Tree build and query times, comparison">
</p
