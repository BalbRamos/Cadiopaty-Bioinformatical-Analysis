# cardio_project_analysis.py
# Run: python cardio_project_analysis.py
# Requires: pandas, numpy, scipy, matplotlib, seaborn

import os
import numpy as np
import pandas as pd
from scipy import stats
import matplotlib.pyplot as plt
import seaborn as sns

DATA_FILE = "cardiotrain.csv"
OUTDIR = "cardio_outputs"
os.makedirs(OUTDIR, exist_ok=True)

# Load data (semicolon-separated)
df = pd.read_csv(DATA_FILE, sep=";")

# Feature engineering
# Age in years and BMI
# BMI = weight(kg) / (height(m)^2)
df["age_years"] = df["age"] / 365.25
df["height_m"] = df["height"] / 100.0
df["bmi"] = df["weight"] / (df["height_m"] ** 2)

# Numeric conversion
for c in ["ap_hi","ap_lo","cholesterol","gluc","smoke","alco","active","cardio","gender"]:
    df[c] = pd.to_numeric(df[c], errors="coerce")

# BP plausibility filter
bp_mask = df["ap_hi"].between(70,250) & df["ap_lo"].between(40,150) & (df["ap_hi"] >= df["ap_lo"])
bp_df = df.loc[bp_mask].copy()

# Clinical flags
# Hypertension: systolic>=140 OR diastolic>=90 (within plausible BP)
bp_df["hypertensive"] = ((bp_df["ap_hi"] >= 140) | (bp_df["ap_lo"] >= 90)).astype(int)
# Obesity: BMI>=30
bp_df["obese"] = (bp_df["bmi"] >= 30).astype(int)

# Risk groups (BP-plausible subset)
sub = bp_df.copy()
sub["risk_group"] = np.select(
    [ (sub["obese"]==0) & (sub["hypertensive"]==0),
      (sub["obese"]==1) & (sub["hypertensive"]==0),
      (sub["obese"]==0) & (sub["hypertensive"]==1),
      (sub["obese"]==1) & (sub["hypertensive"]==1)],
    ["Neither","Obese only","Hypertensive only","Both"],
    default=np.nan
)

# --- EDA tables ---
continuous = ["age_years","height","weight","bmi","ap_hi","ap_lo"]
cont=[]
for c in continuous:
    src = bp_df[c] if c in ["ap_hi","ap_lo"] else df[c]
    s = pd.to_numeric(src, errors="coerce").dropna()
    cont.append({"variable":c,"n":len(s),"mean":s.mean(),"median":s.median(),"std":s.std(ddof=1)})
pd.DataFrame(cont).to_csv(f"{OUTDIR}/eda_continuous_summary.csv", index=False)

cat=[]
N=len(df)
for c in ["gender","cholesterol","gluc","smoke","alco","active","cardio"]:
    vc=df[c].value_counts(dropna=False).sort_index()
    for level,count in vc.items():
        cat.append({"variable":c,"level":level,"count":int(count),"percent":float(count/N*100)})
pd.DataFrame(cat).to_csv(f"{OUTDIR}/eda_categorical_summary.csv", index=False)

# --- Figures ---
sns.set_theme(style="whitegrid")

plt.figure(figsize=(8,5))
sns.histplot(df["bmi"].dropna(), bins=40, kde=True)
plt.title("Histogram of BMI")
plt.tight_layout()
plt.savefig(f"{OUTDIR}/fig_hist_bmi.png", dpi=200)
plt.close()

plt.figure(figsize=(8,5))
sns.histplot(bp_df["ap_hi"].dropna(), bins=40, kde=True)
plt.title("Histogram of Systolic BP (ap_hi)")
plt.tight_layout()
plt.savefig(f"{OUTDIR}/fig_hist_ap_hi.png", dpi=200)
plt.close()

plt.figure(figsize=(8,5))
sns.histplot(df["age_years"].dropna(), bins=40, kde=True)
plt.title("Histogram of Age (years)")
plt.tight_layout()
plt.savefig(f"{OUTDIR}/fig_hist_age.png", dpi=200)
plt.close()

plt.figure(figsize=(8,5))
sns.boxplot(data=df, x="cardio", y="bmi")
plt.title("BMI by CVD status")
plt.tight_layout()
plt.savefig(f"{OUTDIR}/fig_box_bmi_by_cardio.png", dpi=200)
plt.close()

plt.figure(figsize=(8,5))
sns.boxplot(data=bp_df, x="cardio", y="ap_hi")
plt.title("Systolic BP by CVD status")
plt.tight_layout()
plt.savefig(f"{OUTDIR}/fig_box_ap_hi_by_cardio.png", dpi=200)
plt.close()

plt.figure(figsize=(8,5))
sns.boxplot(data=bp_df, x="cholesterol", y="ap_hi")
plt.title("Systolic BP by cholesterol category")
plt.tight_layout()
plt.savefig(f"{OUTDIR}/fig_box_ap_hi_by_cholesterol.png", dpi=200)
plt.close()

plt.figure(figsize=(8,5))
sns.scatterplot(data=bp_df.sample(min(15000,len(bp_df)), random_state=1), x="bmi", y="ap_hi", hue="cardio", alpha=0.35)
plt.title("Scatterplot: BMI vs systolic BP (ap_hi)")
plt.tight_layout()
plt.savefig(f"{OUTDIR}/fig_scatter_bmi_vs_ap_hi.png", dpi=200)
plt.close()

plt.figure(figsize=(8,5))
sns.scatterplot(data=bp_df.sample(min(15000,len(bp_df)), random_state=1), x="age_years", y="ap_hi", hue="cardio", alpha=0.35)
plt.title("Scatterplot: Age vs systolic BP (ap_hi)")
plt.tight_layout()
plt.savefig(f"{OUTDIR}/fig_scatter_age_vs_ap_hi.png", dpi=200)
plt.close()

plt.figure(figsize=(10,7))
hm = bp_df[["age_years","bmi","ap_hi","ap_lo","cholesterol","gluc","smoke","alco","active","cardio"]].corr(method="pearson")
sns.heatmap(hm, cmap="vlag", center=0)
plt.title("Correlation heatmap (Pearson)")
plt.tight_layout()
plt.savefig(f"{OUTDIR}/fig_heatmap.png", dpi=200)
plt.close()

# --- Hypothesis tests ---
# Welch t-tests (one-sided): cardio=1 greater than cardio=0
ap1 = bp_df.loc[bp_df["cardio"]==1,"ap_hi"].dropna()
ap0 = bp_df.loc[bp_df["cardio"]==0,"ap_hi"].dropna()
res_ap = stats.ttest_ind(ap1, ap0, equal_var=False, alternative="greater")

b1 = df.loc[df["cardio"]==1,"bmi"].dropna()
b0 = df.loc[df["cardio"]==0,"bmi"].dropna()
res_bmi = stats.ttest_ind(b1, b0, equal_var=False, alternative="greater")

anova_df = bp_df.loc[bp_df["cholesterol"].isin([1,2,3]), ["cholesterol","ap_hi"]].dropna()
res_anova = stats.f_oneway(*(anova_df.loc[anova_df["cholesterol"]==lev,"ap_hi"].values for lev in [1,2,3]))

pd.DataFrame([
    {"test":"Welch t-test ap_hi (cardio1>cardio0)","t_stat":res_ap.statistic,"p_value":res_ap.pvalue},
    {"test":"Welch t-test BMI (cardio1>cardio0)","t_stat":res_bmi.statistic,"p_value":res_bmi.pvalue},
    {"test":"ANOVA ap_hi by cholesterol","F_stat":res_anova.statistic,"p_value":res_anova.pvalue},
]).to_csv(f"{OUTDIR}/hypothesis_tests.csv", index=False)

print("Done. Outputs in", OUTDIR)
