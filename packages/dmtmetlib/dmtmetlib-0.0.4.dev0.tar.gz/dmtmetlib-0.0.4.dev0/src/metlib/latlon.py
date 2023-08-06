#!/usr/bin/env python3

import json
import numpy as np
from scipy.spatial import cKDTree
from met.nora3.field import Field
from met.nora3.fieldpoint import FieldPoint


def __read_coordinates(filepath):
    with open(filepath, "r",encoding='utf8') as fp:
        return json.load(fp)

coordinates = __read_coordinates("coordinates.json")
lat = np.array(coordinates["lat"])
lon = np.array(coordinates["lon"])


def nearest(lon, lat, lon_pos, lat_pos):
    """Function to find index to nearest point """
    M = np.c_[np.ravel(lon), np.ravel(lat)]
    tree = cKDTree(M)
    _, ii = tree.query([lon_pos, lat_pos], k=1)
    idy, idx = np.where((lon == M[ii][0]) & (lat == M[ii][1]))
    return int(idx), int(idy)


def find_nearest(field: Field):
    """Find nearest wind hindcast coordinates"""

    f_lon = field.longitude
    f_lat = field.latitude

    for (lat_pos,lon_pos) in zip(f_lat,f_lon):
        idx,idy = __nearest(lon, lat, lon_pos, lat_pos)
        grid_lon_pkt=float(lon[idy,idx])
        grid_lat_pkt=float(lat[idy,idx])
        field.points.append(FieldPoint(latitude=grid_lat_pkt,longitude=grid_lon_pkt))
