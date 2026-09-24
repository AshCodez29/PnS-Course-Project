import pandas as pd
df = pd.read_csv("pune_pixels.csv")

def zone(r):
    if r.ndwi > 0:                     return "Water"
    if r.ndvi >= 0.4:                  return "Vegetation"
    if r.ndbi > 0 and r.ndvi < 0.2:    return "Built-up"
    return "Mixed/Bare"

df["zone"] = df.apply(zone, axis=1)
print(df["zone"].value_counts())
print(df.groupby("zone")["temp_c"].agg(["count","mean","std","min","max"]))