import pandas as pd
import numpy as np
from scipy import stats
from statsmodels.stats.multicomp import pairwise_tukeyhsd
import matplotlib.pyplot as plt

df = pd.read_csv("pune_pixels.csv")

def zone(r):
    if r.ndwi > 0:                     return "Water"
    if r.ndvi >= 0.4:                  return "Vegetation"
    if r.ndbi > 0 and r.ndvi < 0.2:    return "Built-up"
    return "Mixed/Bare"

df["zone"] = df.apply(zone, axis=1)
print(df["zone"].value_counts())
print(df.groupby("zone")["temp_c"].agg(["count","mean","std","min","max"]))


b = df[df.zone == "Built-up"].temp_c
v = df[df.zone == "Vegetation"].temp_c

# 1. Welch t-test 
t, p = stats.ttest_ind(b, v, equal_var=False)
diff = b.mean() - v.mean()
se = np.sqrt(b.var()/len(b) + v.var()/len(v))
d = diff / np.sqrt((b.var() + v.var()) / 2)
print(f"t={t:.1f}, p={p:.3g}, diff={diff:.2f} C, "
      f"95% CI=({diff-1.96*se:.2f}, {diff+1.96*se:.2f}), d={d:.2f}")
# 2. One-way ANOVA across all 4 zones
groups = [g.temp_c for _, g in df.groupby("zone")]
print(stats.f_oneway(*groups))
print(pairwise_tukeyhsd(df.temp_c, df.zone))

# # 3. Boxplot
# df.boxplot(column="temp_c", by="zone", figsize=(7, 5))
# plt.show()

#4 Zone Map 
zone_map = np.select(
    [ndwi > 0, ndvi >= 0.4, (ndbi > 0) & (ndvi < 0.2)],
    [3, 2, 1], default=0
)  # 0=Mixed/Bare, 1=Built-up, 2=Vegetation, 3=Water

plt.figure(figsize=(7,6))
plt.imshow(zone_map, cmap="tab10")
plt.title("Final Land-Cover Classification")
plt.colorbar(ticks=[0,1,2,3], label="0=Mixed 1=Built-up 2=Veg 3=Water")
plt.axis("off")
plt.show()