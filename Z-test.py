import numpy as np
import pandas as pd
from statsmodels.stats.weightstats import ztest

# 1. Load the data
df = pd.read_csv("data/processed/pune_pixels.csv")
print("Rows loaded:", len(df))

threshold = 45 #degree Celcius, the value we compare against
temps = df["temp_c"]

n = len(temps)
mean = temps.mean()
std = temps.std(ddof=1)
se = std / np.sqrt(n)
print(f"n = {n}, mean = {mean:.2f} °C, std = {std:.2f} °C")

z, p = ztest(temps, value=threshold, alternative="larger")
print(f"\nz = {z:.2f}")
print(f"p-value = {p:.3g}")

lower = mean - 1.96 * se
upper = mean + 1.96 * se
print(f"95% CI for mean: ({lower:.2f}, {upper:.2f}) °C")

# Decision
alpha = 0.05
if p < alpha:
    print(f"\nReject H0: mean temperature is significantly above {threshold} °C.")
else:
    print(f"\nFail to reject H0: no evidence the mean is above {threshold} °C.")