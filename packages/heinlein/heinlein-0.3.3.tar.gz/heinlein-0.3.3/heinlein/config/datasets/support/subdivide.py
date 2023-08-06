import pickle

with open("cfht_regions.reg", "rb") as f:
	data = pickle.load(f)


for reg in data:
	poly = reg.geometry
	print(poly)
	exit()