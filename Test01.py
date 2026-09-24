# pip install pystac-client planetary-computer stackstac rioxarray
import pystac_client, planetary_computer as pc
import os
import numpy as np, pandas as pd, stackstac

catalog = pystac_client.Client.open(
    "https://planetarycomputer.microsoft.com/api/stac/v1",
    modifier=pc.sign_inplace,
)
search = catalog.search(
    collections=["landsat-c2-l2"],
    bbox=[73.75, 18.40, 73.98, 18.63],      # rough Pune box
    datetime="2026-03-01/2026-04-30",
    query={"eo:cloud_cover": {"lt": 10},
           "platform": {"in": ["landsat-8", "landsat-9"]}},
)
items = list(search.items())
for i in items:
    print(i.id, i.properties["eo:cloud_cover"])

item = min(items, key=lambda i: i.properties["eo:cloud_cover"])
print("Using:", item.id)

bands = ["green", "red", "nir08", "swir16", "lwir11", "qa_pixel"]
da = stackstac.stack([item], assets=bands, bounds_latlon=bbox, epsg=32643,
                     resolution=30, dtype="float64", fill_value=0,
                     rescale=False).squeeze("time").compute()

g, r, n, s, t, qa = [da.sel(band=b).values for b in bands]
cloud = (qa.astype(int) & 0b11010) != 0 # cloud, shadow, dilated cloud

sc = lambda x: x * 0.0000275 - 0.2  # reflectance scaling
g, r, n, s = map(sc, (g, r, n, s))
temp_c = t * 0.00341802 + 149.0 - 273.15 # surface temp in °C

with np.errstate(divide="ignore", invalid="ignore"):
    ndvi = (n - r) / (n + r)
    ndbi = (s - n) / (s + n)
    ndwi = (g - n) / (g + n)

valid = (t > 0) & ~cloud
ys, xs = np.where(valid)
df = pd.DataFrame({
    "x_m": da.x.values[xs], "y_m": da.y.values[ys],
    "temp_c": temp_c[valid], "ndvi": ndvi[valid],
    "ndbi": ndbi[valid], "ndwi": ndwi[valid],
}).replace([np.inf, -np.inf], np.nan).dropna()

df = df.sample(50000, random_state=42) # keeps the CSV small
os.makedirs("data/processed", exist_ok=True)
df.to_csv("data/processed/pune_pixels.csv", index=False)
print(df.describe())