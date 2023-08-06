
import time
from heinlein import load_dataset, Region
from shapely import geometry
import astropy.units as u
import matplotlib.pyplot as plt
des_center = (13.4349,-20.2091)
hsc_center = (141.23246, 2.32358)
des_mutli_center = (19.546018,  -28.189612)
radius = 360*u.arcsec


start = time.time()
cfht = load_dataset("cfht")
end = time.time()
print(f"Setup took {end-start} seconds")

start = time.time()
data = cfht.cone_search((215.0, 56.0), radius, dtypes=["catalog", "mask"])
end = time.time()
print(f"Cone search took {end - start} seconds")

start = time.time()
data = cfht.cone_search((215.0, 56.0), radius, dtypes=["catalog", "mask"])
end = time.time()
print(f"Cone search took {end - start} seconds")


cat = data["catalog"]
mask = data["mask"]
start = time.time()
masked_cat = cat[mask]
end = time.time()
print(f"Masking took {end - start} seconds")

plt.scatter(cat['ra'], cat['dec'], c='red')
plt.scatter(masked_cat['ra'], masked_cat['dec'], c="blue")
plt.show()
exit()


hsc_error_center = (33.15582, -1.5446)
setup_start = time.time()
d = load_dataset("hsc")

setup_end = time.time()
print(f"Setup took {setup_end - setup_start} seconds")


get_start = time.time()
a = d.cone_search(hsc_error_center, radius, dtypes=["catalog", "mask"])
get_end = time.time()

print(f"Get took {get_end - get_start} seconds!")


start = time.time()
masked = a["catalog"][a["mask"]]
end = time.time()
print(f"Masking took {end - start} seconds")

get_start = time.time()
a = d.cone_search(hsc_center, radius, dtypes=["catalog", "mask"])
get_end = time.time()

print(f"Get took {get_end - get_start} seconds!")


import matplotlib.pyplot as plt
plt.scatter(a["catalog"]['ra'], a["catalog"]["dec"], c="red")
plt.scatter(masked["ra"], masked["dec"], c="blue")
plt.show()

