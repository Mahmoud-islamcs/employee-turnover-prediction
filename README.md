# Salifort Motors - Employee Turnover Prediction

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://employee-turnover-prediction.streamlit.app/)

**Live app:** https://employee-turnover-prediction.streamlit.app/

![Streamlit app screenshot](assets/Screenshot%202026-11-18%20145816.png)

## Project Overview
This repository contains the capstone project for the **Google Advanced Data Analytics Professional Certificate** ([credential on Coursera](https://www.coursera.org/account/accomplishments/professional-cert/6B958X2LX2G3)).

The goal is to analyze HR survey data from **Salifort Motors** (a fictional alternative energy vehicle manufacturer), build models that predict whether an employee will leave, and give HR data-driven recommendations to improve retention.

## Business Problem
Salifort Motors' senior leadership wants to increase employee retention. The HR department collected employee data (satisfaction, evaluation, projects, hours, tenure, department, salary...) but had no way to use it. The question: **what is likely to make an employee leave the company?**

## Dataset
- Source: [HR Analytics and Job Prediction (Kaggle)](https://www.kaggle.com/datasets/mfaisalqureshi/hr-analytics-and-job-prediction?select=HR_comma_sep.csv)
- 14,999 rows x 10 columns, no missing values
- 3,008 duplicate rows removed -> **11,991 rows** (`cleaned_hr_dataset.csv`)
- Target: `left` (1,991 left / 10,000 stayed = **16.6% turnover**)

## Approach (PACE)
1. **Plan:** define the problem, stakeholders and data.
2. **Analyze:** cleaning (renaming, duplicates, outliers), EDA and visualizations.
3. **Construct:** Logistic Regression, Decision Tree and Random Forest, tuned with 4-fold `GridSearchCV` (refit on ROC-AUC).
4. **Execute:** evaluate on a hold-out test set and share recommendations.

Round 1 of the tree models scored suspiciously high, so data leakage was suspected. Round 2 dropped `satisfaction_level`, replaced `avg_monthly_hours` with a binary `overworked` feature (> 170 hrs/month), and became the final comparison.

## Results (hold-out test set)

| Model | Accuracy | Precision | Recall | F1 | AUC |
|---|---|---|---|---|---|
| Logistic Regression (baseline, class "left") | 0.83 | 0.47 | 0.24 | 0.32 | 0.892 |
| Logistic Regression (balanced, class "left") | 0.84 | 0.51 | 0.91 | 0.65 | - |
| Decision Tree 2 (feature-engineered) | 0.962 | 0.87 | 0.904 | 0.887 | 0.938 |
| **Random Forest 2 (champion)** | **0.960** | **0.866** | **0.898** | **0.882** | **0.935** |

Random Forest 2 has the best cross-validated AUC (0.961 vs 0.953 for the decision tree); on the test set the two models are very close.

## Key Insights
- Employees are **overworked**: most work well above the ~167 hrs/month norm.
- **Everyone with 7 projects left**; employees with 6-7 projects worked ~14-32% more than average.
- Leavers fall into two groups: burnt-out high performers, and under-used, low-satisfaction employees.
- Employees around the **4-year tenure** mark show unusually low satisfaction.
- Top predictors: `last_evaluation`, `num_projects`, `years_at_company`, `overworked`.

## Recommendations
- Cap the number of projects per employee.
- Promote employees with 4+ years of tenure, or investigate why they are dissatisfied.
- Reward employees for long hours, or do not require them.
- Make overtime pay and time-off policies explicit.
- Hold company-wide and team-level discussions on work culture.
- Do not reserve high evaluation scores for employees working 200+ hours per month.

## Next Steps
- `last_evaluation` may not exist for every employee in production, so re-evaluate the model without it.
- Explore a K-means model and analyze the clusters.

## Repository Structure
```
employee-turnover-prediction/
├── app.py                        # Streamlit app (static report, no model is executed)
├── cleaned_hr_dataset.csv        # Cleaned dataset used by the app
├── assets/                       # Images used by the app and README
├── executive-summary.pdf         # Executive summary for stakeholders
├── PACE-strategy-document.pdf   # PACE strategy document
├── requirements.txt
└── README.md
```

## Run Locally
```bash
pip install -r requirements.txt
streamlit run app.py
```

## Tech Stack
Python, Pandas, Scikit-learn, Matplotlib, Seaborn, Plotly, Streamlit