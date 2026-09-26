import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
import pandas as pd
df = pd.read_csv("pune_pixels.csv")

# 1. Correlation + simple linear regression: temp_c vs ndvi
r, p_corr = stats.pearsonr(df.ndvi, df.temp_c)
slope, intercept, r_val, p_reg, se = stats.linregress(df.ndvi, df.temp_c)
print(f"Pearson r = {r:.3f}, p = {p_corr:.3g}")
print(f"temp_c = {intercept:.2f} + {slope:.2f} * ndvi   (R^2 = {r_val**2:.3f})")
print(f"Each +0.1 NDVI -> {slope*0.1:.2f} C change in temp_c")

plt.figure(figsize=(6,5))
plt.scatter(df.ndvi, df.temp_c, s=2, alpha=0.15)
xline = np.linspace(df.ndvi.min(), df.ndvi.max(), 100)
plt.plot(xline, intercept + slope*xline, color="red")
plt.xlabel("NDVI"); plt.ylabel("Surface Temp (°C)")
plt.title("Temperature vs NDVI")
plt.show()

# # 2. Normality check on temp_c (Shapiro needs a sample; full n=50000 is too large for it)
# sample = df.temp_c.sample(2000, random_state=1)
# stat, p_shapiro = stats.shapiro(sample)
# print(f"Shapiro-Wilk (n=2000 subsample): W={stat:.4f}, p={p_shapiro:.3g}")

# plt.figure(figsize=(5,5))
# stats.probplot(df.temp_c, dist="norm", plot=plt)
# plt.title("Q-Q Plot: temp_c")
# plt.show()