import numpy as np
from scipy import stats
from statsmodels.stats.multicomp import pairwise_tukeyhsd
import matplotlib.pyplot as plt
import pandas as pd

df = pd.read_csv("pune_pixels.csv")

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

# 3. Boxplot
df.boxplot(column="temp_c", by="zone", figsize=(7, 5))
plt.show()