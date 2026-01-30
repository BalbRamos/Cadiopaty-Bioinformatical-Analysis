# DS204 — Cardiovascular Disease Dataset Analysis

This repository contains my DS 204 final project analyzing a cardiovascular disease (CVD) clinical examination dataset and quantifying **association strength** (not causality) between CVD status and systolic blood pressure (SBP), BMI, and their joint presence. [file:79]

## Project overview
- Dataset: `cardiotrain.csv` with n = 70,000 observations and target `cardio` (0/1). [file:79]  
- Goal: compare association strength of SBP vs BMI with CVD status, and evaluate combined hypertension + obesity groups using risk metrics (RR/OR/RD). [file:79]  
- Approach follows the course guide: EDA → hypothesis testing → correlation analyses → interpretation and real-world application. [file:1]

## Dataset
The dataset is commonly referenced as the “Cardiovascular Disease Dataset” and is available from Kaggle. [page:2]  
Place the file locally as `data/cardiotrain.csv` (semicolon-separated). [file:79]  
Note: this repository may exclude the raw dataset file to respect third‑party dataset redistribution rules; please download it from the source and store it locally. [page:2]

## Methods (statistics used)
Feature engineering:
- AgeYears = AgeDays / 365.25. [file:79]  
- BMI = Weight_kg / (Height_m²). [file:79]  

Data cleaning:
- Blood pressure plausibility filter: ap_hi 70–250, ap_lo 40–150, and ap_hi ≥ ap_lo (kept 68,668 of 70,000 records for BP analyses). [file:79]  

Hypothesis tests:
- Welch two-sample t-tests for group mean differences by `cardio`. [file:79]  
- One-way ANOVA for SBP differences across cholesterol categories (1/2/3). [file:79]  

Correlation suite:
- Pearson, Spearman, Kendall’s Tau, point-biserial (binary–continuous), and Phi (binary–binary). [file:79]  

Joint exposure analysis:
- Obesity: BMI ≥ 30; Hypertension: SBP ≥ 140 or DBP ≥ 90 (BP-plausible subset). [file:79]  
- Risk ratio (RR), odds ratio (OR), risk difference (RD), and 95% confidence intervals. [file:79]

## Key findings (high level)
SBP showed a substantially stronger association with CVD status than BMI in this dataset based on effect sizes and point-biserial correlations. [file:79]  
- BMI difference (cardio=1 vs cardio=0): Cohen’s d = 0.3359 (Welch t = 44.4318). [file:79]  
- SBP difference (cardio=1 vs cardio=0): Cohen’s d = 0.9475 (Welch t = 123.7266). [file:79]  
- Point-biserial: cardio vs BMI r_pb = 0.1656; cardio vs SBP r_pb = 0.4281. [file:79]  

Joint group results (relative to “Neither”):
- Obese only: RR = 1.4009; OR = 1.7275; RD = 0.1285. [file:79]  
- Hypertensive only: RR = 2.4031; OR = 7.1064; RD = 0.4497. [file:79]  
- Both: RR = 2.4828; OR = 8.2611; RD = 0.4753. [file:79]  

Cholesterol category was associated with higher mean SBP (ANOVA F = 1393.6225, η² = 0.0390). [file:79]

## Repository structure
src/ # Analysis script(s)
data/ # Local dataset location (not necessarily committed)
outputs/ # Generated figures/tables (optional to commit)
report/ # Final PDF report
presentation/ # Slide outline / presentation materials
docs/ # Methodology, glossary, notes
references/ # Dataset reference and citations


## How to run
1. Create and activate a Python environment (venv/conda).  
2. Install requirements:

pip install -r requirements.txt

3. Download `cardiotrain.csv` and place it at:
data/cardiotrain.csv

4. Run the analysis:
python src/cardio_project_analysis.py

The analysis script writes figures (PNG) and result tables (CSV) to an output directory (default: `cardio_outputs/`). [code_file:58]

## Outputs
Expected figures include BMI and SBP histograms, boxplots by CVD status, scatterplots (e.g., BMI vs SBP), and a correlation heatmap. [code_file:58]  
Expected tables include descriptive statistics and hypothesis/correlation outputs used in the report. [file:79]

## Deliverables
- Final report (PDF): `report/Final_Report_CardioV-BALBINORAMOS.pdf`. [file:79]  
- Presentation outline: `presentation/slides.md`.  

## Academic note
All results are interpreted as associations from cross-sectional observational data and do not establish causation. [file:79]

## Acknowledgments
Course: DS 204 – Analysis for Data Science, Cornerstone Community College. [file:79]  
Instructor: Prof. M.Eng. Atabak Eghbal. [file:79]

