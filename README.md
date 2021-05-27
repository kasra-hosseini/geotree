<div align="center">
    <br>
    <h2>GeoTree: find nearest-neighbours on geographic coordinates</h2>
</div>

<p align="center">
    <a href="https://github.com/kasra-hosseini/geotree/blob/main/LICENSE">
        <img alt="License" src="https://img.shields.io/badge/License-MIT-yellow.svg">
    </a>
    <br/>
</p>

Table of contents
-----------------

- [Installation and setup](#installation)
- [Interpolate values of one grid into another one](#interpolate-values-from-one-grid-into-another-one)

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

## Interpolate values of one grid into another one

Instantiate gkdtree:

```python
from geotree import gkdtree
import numpy as np

# instantiate gkdtree
mykdtree = gkdtree()
```

Define the first set of points

```python
npoints = 100
lons = np.random.randint(-180, 180, npoints)
lats = np.random.randint(-90, 90, npoints)
depths = np.zeros(npoints)
```

Some random values (for each point)

```python
vals = np.zeros(npoints)
vals[:(npoints//2)] = 0
vals[(npoints//2):] = 1
```

Add lons/lats/depths of the first set of points
```python
mykdtree.add_lonlatdep(lons=lons, 
                       lats=lats, 
                       depths=depths)
```

Define queries:

```python
q_npoints = 10000
q_lons = np.random.randint(-180, 180, q_npoints)
q_lats = np.random.randint(-90, 90, q_npoints)
q_depths = np.zeros(q_npoints)
```

Add lons/lats/depths of queries

```python
mykdtree.add_lonlatdep_query(lons=q_lons, 
                             lats=q_lats, 
                             depths=q_depths)
```

Add values, note: size of vals should be the same as the first set of points

```python
mykdtree.add_vals(vals)
```

Interpolate values from the first set of points into the queries (using 4 neighbours):

```python
mykdtree.interpolate(num_neighs=4)
```

<p align="center">
  <img src="./images/interp_4.png" width="80%" title="interpolation with 4 neighbours">
</p>

```python
mykdtree.interpolate(num_neighs=1)
```

<p align="center">
  <img src="./images/interp_1.png" width="80%" title="interpolation with 1 neighbours">
</p>

```python
mykdtree.interpolate(num_neighs=2)
```

<p align="center">
  <img src="./images/interp_2.png" width="80%" title="interpolation with 2 neighbours">
</p>

```python
mykdtree.interpolate(num_neighs=10)
```

<p align="center">
  <img src="./images/interp_10.png" width="80%" title="interpolation with 10 neighbours">
</p>

To plot the above figures:

```python
import matplotlib.pyplot as plt
plt.figure(figsize=(15, 7))
plt.scatter(q_lons, q_lats, 
            c=mykdtree.interp_vals, 
            marker="x", 
            vmin=min(vals), vmax=max(vals),
            label="queries")

plt.scatter(lons, lats,
            c=vals, 
            marker="o",
            vmin=min(vals), vmax=max(vals), edgecolors="r",
            label="base",
            zorder=100)

plt.legend(bbox_to_anchor=(0., 1.02, 1., .102), 
           loc="center", ncol=2, 
           fontsize=16,
           borderaxespad=0.)

plt.colorbar()
plt.grid()
```