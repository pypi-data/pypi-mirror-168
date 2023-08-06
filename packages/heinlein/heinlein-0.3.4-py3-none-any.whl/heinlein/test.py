
from heinlein import load_dataset, Region
from shapely import geometry
import astropy.units as u
import matplotlib.pyplot as plt
des_center = (13.4349,-20.2091)
hsc_center = (141.23246, 2.32358)
des_mutli_center = (19.546018,  -28.189612)
radius = 360*u.arcsec

hsc_error_center = (33.15582, -1.5446)
d = load_dataset("des")



a = d.cone_search(des_center, radius, dtypes=["catalog", "mask"])
print(a)

d = load_dataset("hsc")


a = d.cone_search(hsc_center, radius, dtypes=["catalog", "mask"])
print(a)
