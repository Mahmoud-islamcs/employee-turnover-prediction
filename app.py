"""
Salifort Motors - Employee Retention (Google Advanced Data Analytics Capstone)
Static Streamlit app: presents the data, EDA, every model and the final results.
No model is loaded or executed here - every number below was taken from the notebook outputs.

Run:  streamlit run app.py
"""
from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(
    page_title="Salifort Motors | Employee Retention",
    layout="wide",
)

ASSETS = Path(__file__).parent / "assets"

# --------------------------------------------------------------------------- #
# Styling
# --------------------------------------------------------------------------- #
st.markdown(
    """
    <style>
      /* Desktop layout */
      .block-container {padding-top: 2rem; max-width: 1200px;}
      div[data-testid="stMetric"] {
          background: rgba(120,120,140,.08); border: 1px solid rgba(120,120,140,.2);
          padding: 14px 16px; border-radius: 12px;}
      .note {border-left: 4px solid #4C78A8; padding: 8px 14px; margin: 8px 0 18px 0;
             background: rgba(76,120,168,.08); border-radius: 4px;}
      .warn {border-left: 4px solid #E45756; padding: 8px 14px; margin: 8px 0 18px 0;
             background: rgba(228,87,86,.08); border-radius: 4px;}

      /* Mobile and tablet responsive optimizations */
      @media (max-width: 768px) {
        html, body, [data-testid="stAppViewContainer"] {
          overflow-x: hidden !important;
          max-width: 100vw !important;
        }
        .block-container {
          padding-top: 1rem !important;
          padding-left: 0.75rem !important;
          padding-right: 0.75rem !important;
          padding-bottom: 2rem !important;
          max-width: 100% !important;
        }
        /* Mobile metric cards: clean padding, legible responsive typography */
        div[data-testid="stMetric"] {
          padding: 10px 12px !important;
          margin-bottom: 8px !important;
          border-radius: 10px !important;
        }
        div[data-testid="stMetric"] [data-testid="stMetricLabel"] {
          font-size: 0.82rem !important;
          white-space: normal !important;
          word-break: break-word !important;
        }
        div[data-testid="stMetric"] [data-testid="stMetricValue"] {
          font-size: 1.45rem !important;
        }
        div[data-testid="stMetric"] [data-testid="stMetricDelta"] {
          font-size: 0.78rem !important;
        }
        /* Tabs: smooth horizontal touch scroll on narrow screens */
        div[data-testid="stTabs"] {
          overflow-x: auto !important;
          -webkit-overflow-scrolling: touch !important;
        }
        div[data-testid="stTabs"] button[role="tab"] {
          padding: 6px 10px !important;
          font-size: 0.85rem !important;
          white-space: nowrap !important;
        }
        /* Touch targets: minimum 44px height for mobile accessibility */
        button[data-testid="stBaseButton-secondary"],
        button[data-testid="stBaseButton-primary"],
        .stDownloadButton button {
          min-height: 44px !important;
          font-size: 0.88rem !important;
        }
        /* Callouts: compact padding and safe wrapping on mobile */
        .note, .warn {
          padding: 8px 10px !important;
          font-size: 0.9rem !important;
          margin: 8px 0 12px 0 !important;
          word-break: break-word !important;
        }
        /* Plotly charts: hide modebar clutter on touch screens */
        .js-plotly-plot .plotly .modebar {
          display: none !important;
        }
        .js-plotly-plot {
          max-width: 100% !important;
        }
        /* Dataframes and tables: fluid horizontal scroll */
        [data-testid="stDataFrame"], [data-testid="stTable"] {
          width: 100% !important;
          overflow-x: auto !important;
        }
      }
    </style>
    """,
    unsafe_allow_html=True,
)


def note(text: str, kind: str = "note"):
    st.markdown(f'<div class="{kind}">{text}</div>', unsafe_allow_html=True)


def show_image(name: str, caption: str = ""):
    path = ASSETS / f"{name}.webp"
    if path.exists():
        st.image(str(path), caption=caption or None, width='stretch')
    else:
        st.info(f"Image `assets/{name}.webp` not found - put the `assets/` folder next to app.py.")


# --------------------------------------------------------------------------- #
# Data (copied from notebook outputs)
# --------------------------------------------------------------------------- #
DATA_DICT = pd.DataFrame(
    [
        ("satisfaction_level", "satisfaction_level", "float", "Employee-reported job satisfaction [0-1]"),
        ("last_evaluation", "last_evaluation", "float", "Score of last performance review [0-1]"),
        ("number_project", "num_projects", "int", "Number of projects the employee contributes to"),
        ("average_montly_hours", "avg_monthly_hours", "int", "Average hours worked per month"),
        ("time_spend_company", "years_at_company", "int", "Tenure at the company (years)"),
        ("Work_accident", "work_accident", "int (0/1)", "Experienced a work accident"),
        ("left", "left", "int (0/1)", "TARGET - employee left the company"),
        ("promotion_last_5years", "promotion_last_5_years", "int (0/1)", "Promoted in the last 5 years"),
        ("Department", "department", "object", "Employee's department"),
        ("salary", "salary", "object", "Salary band: low / medium / high"),
    ],
    columns=["Original column", "Renamed to", "Type", "Description"],
)

DESCRIBE = pd.DataFrame(
    {
        "satisfaction_level": [0.612834, 0.248631, 0.09, 0.44, 0.64, 0.82, 1.0],
        "last_evaluation": [0.716102, 0.171169, 0.36, 0.56, 0.72, 0.87, 1.0],
        "number_project": [3.803054, 1.232592, 2, 3, 4, 5, 7],
        "average_montly_hours": [201.050337, 49.943099, 96, 156, 200, 245, 310],
        "time_spend_company": [3.498233, 1.460136, 2, 3, 3, 4, 10],
        "Work_accident": [0.144610, 0.351719, 0, 0, 0, 0, 1],
        "left": [0.238083, 0.425924, 0, 0, 0, 0, 1],
        "promotion_last_5years": [0.021268, 0.144281, 0, 0, 0, 0, 1],
    },
    index=["mean", "std", "min", "25%", "50%", "75%", "max"],
).T

DEPT_COUNTS = pd.DataFrame(
    {
        "department": ["sales", "technical", "support", "IT", "RandD", "product_mng",
                       "marketing", "accounting", "hr", "management"],
        "employees": [3239, 2244, 1821, 976, 694, 686, 673, 621, 601, 436],
    }
)

# Cross-validation (4-fold GridSearchCV, refit on ROC-AUC) - from make_results()
CV = pd.DataFrame(
    [
        ("Decision Tree 1", "All features", 0.947412, 0.922352, 0.973961, 0.982987, 0.964960),
        ("Random Forest 1", "All features", 0.955310, 0.923019, 0.989993, 0.985655, 0.976333),
        ("Decision Tree 2", "Feature-engineered", 0.891509, 0.889482, 0.893690, 0.964083, 0.953286),
        ("Random Forest 2", "Feature-engineered", 0.898913, 0.899532, 0.898341, 0.966419, 0.961375),
    ],
    columns=["Model", "Feature set", "F1", "Recall", "Precision", "Accuracy", "AUC"],
)

# Hold-out test set (25 %). Logistic regression is the "left" class row of classification_report.
TEST = pd.DataFrame(
    [
        ("Logistic Regression", "Baseline", 0.83, 0.47, 0.24, 0.32, 0.892),
        ("Logistic Regression", "class_weight='balanced'", 0.84, 0.51, 0.91, 0.65, None),
        ("Random Forest 1", "All features", 0.981654, 0.984649, 0.903421, 0.942288, 0.950311),
        ("Decision Tree 2", "Feature-engineered", 0.962, 0.87, 0.904, 0.887, 0.938),
        ("Random Forest 2 (champion)", "Feature-engineered", 0.959973, 0.866279, 0.897590, 0.881657, 0.934995),
    ],
    columns=["Model", "Version", "Accuracy", "Precision", "Recall", "F1", "AUC"],
)

BEST_PARAMS = pd.DataFrame(
    [
        ("Decision Tree 1", "6", "1", "4", "-", "-", "-"),
        ("Random Forest 1", "8", "3", "2", "1.0", "0.7", "500"),
        ("Decision Tree 2", "6", "2", "6", "-", "-", "-"),
        ("Random Forest 2", "5", "3", "2", "1.0", "0.7", "500"),
    ],
    columns=["Model", "max_depth", "min_samples_leaf", "min_samples_split",
             "max_features", "max_samples", "n_estimators"],
)

LR_COEF = pd.DataFrame(
    {
        "feature": ["satisfaction_level", "last_evaluation", "num_projects", "avg_monthly_hours",
                    "years_at_company", "work_accident", "promotion_last_5_years", "salary",
                    "department_IT", "department_RandD", "department_accounting", "department_hr",
                    "department_management", "department_marketing", "department_product_mng",
                    "department_sales", "department_support", "department_technical"],
        "coefficient": [-4.443964, -0.085910, -0.447506, 0.003232, 1.033212, -1.473440, -0.685443,
                        -0.506393, -0.030981, -0.368637, -0.200147, 0.058419, -0.164003, -0.062401,
                        -0.111811, 0.031732, -0.031995, 0.031987],
    }
)

DT2_IMPORTANCE = pd.DataFrame(
    {
        "feature": ["last_evaluation", "num_projects", "years_at_company", "overworked",
                    "department_technical", "salary", "department_sales", "department_support",
                    "work_accident", "department_IT", "department_marketing"],
        "importance": [0.344443, 0.344235, 0.214199, 0.093587, 0.001179, 0.000911,
                       0.000626, 0.000418, 0.000183, 0.000141, 0.000078],
    }
)

RF2_IMPORTANCE = pd.DataFrame(
    {
        "feature": [
            "department_accounting", "department_IT", "department_technical", "salary",
            "department_support", "department_sales", "overworked", "years_at_company",
            "num_projects", "last_evaluation"
        ],
        "importance": [
            0.000306, 0.000315, 0.000410, 0.000596,
            0.000693, 0.000715, 0.082375, 0.196298,
            0.358447, 0.359133
        ],
    }
)

ROC_POINTS = [
    (0.0, 0.0), (0.0151, 0.0127), (0.022, 0.0255), (0.0246, 0.0637),
    (0.0271, 0.0998), (0.0302, 0.1189), (0.0371, 0.1401), (0.0422, 0.1805),
    (0.0448, 0.2102), (0.0491, 0.2229), (0.0556, 0.2399), (0.0586, 0.2675),
    (0.0612, 0.293), (0.0638, 0.3206), (0.0659, 0.3609), (0.0689, 0.4098),
    (0.072, 0.4352), (0.075, 0.4671), (0.0806, 0.4989), (0.0853, 0.5265),
    (0.0896, 0.5563), (0.0931, 0.5839), (0.0978, 0.6285), (0.1025, 0.6667),
    (0.1056, 0.6794), (0.1094, 0.724), (0.1129, 0.7367), (0.1189, 0.7601),
    (0.1241, 0.7749), (0.1301, 0.7898), (0.137, 0.8089), (0.1461, 0.8217),
    (0.1517, 0.8365), (0.1607, 0.8535), (0.1706, 0.8705), (0.1848, 0.8832),
    (0.2029, 0.9045), (0.224, 0.9214), (0.2499, 0.9321), (0.2663, 0.9427),
    (0.3102, 0.9554), (0.3529, 0.966), (0.4632, 0.9788), (0.5523, 0.9894),
    (1.0, 1.0),
]


@st.cache_data
def get_clean_data() -> pd.DataFrame:
    p = Path(__file__).parent / "cleaned_hr_dataset.csv"
    if p.exists():
        df = pd.read_csv(p)
        df["status"] = df["left"].map({0: "Stayed", 1: "Left"})
        return df
    return pd.DataFrame()

# Confusion matrices [[TN, FP], [FN, TP]] read from the notebook plots
CONFUSION = {
    "Logistic Regression (baseline)": [[2193, 128], [359, 112]],
    "Logistic Regression (balanced)": [[1909, 412], [41, 430]],
    "Random Forest 2 (champion)": [[2431, 69], [51, 447]],
}


def confusion_fig(m, title):
    fig = px.imshow(
        m, text_auto=True, color_continuous_scale="Blues",
        x=["Predicted: stayed", "Predicted: left"], y=["Actual: stayed", "Actual: left"],
        aspect="equal",
    )
    fig.update_layout(title=title, coloraxis_showscale=False, height=360, margin=dict(t=50, b=10))
    return fig


# --------------------------------------------------------------------------- #
# Sidebar navigation
# --------------------------------------------------------------------------- #
@st.cache_data
def _load_deliverable(filename: str) -> bytes:
    fpath = Path(__file__).parent / filename
    if fpath.exists():
        return fpath.read_bytes()
    return b""


st.sidebar.title("Salifort Motors")
st.sidebar.caption("Alternative Energy Mobility | HR Analytics")
st.sidebar.markdown(
    "**Employee Retention Study**  \n"
    "[*Google Advanced Data Analytics Capstone*](https://www.coursera.org/account/accomplishments/professional-cert/6B958X2LX2G3)"
)

st.sidebar.divider()

# Navigation
st.sidebar.subheader("Navigation")
PAGES = [
    "1. Overview",
    "2. Data & Dictionary",
    "3. Exploratory Analysis",
    "4. Predictive Models",
    "5. Model Comparison",
    "6. HR Recommendations",
    "7. PACE Workflow",
]
page = st.sidebar.radio(
    "Select section:",
    PAGES,
    index=0,
    help="Navigate between data exploration, model benchmarks, and strategic recommendations."
)

st.sidebar.divider()

# Key Metrics Snapshot
st.sidebar.subheader("Key Highlights")
col_s1, col_s2 = st.sidebar.columns(2)
col_s1.metric("Turnover", "16.6%", help="1,991 leavers out of 11,991 employees (after deduplication)")
col_s2.metric("Best AUC", "0.935", help="Champion Random Forest 2 test set ROC-AUC")

# Expandable sections for deeper context without clutter
with st.sidebar.expander("Core Takeaways", expanded=False):
    st.markdown(
        "- **Severe Overwork**: Employees with 6–7 projects worked 14–32% above average. 100% of employees with 7 projects left.\n"
        "- **4-Year Tenure Risk**: Peak dissatisfaction and turnover observed at the 4-year mark.\n"
        "- **Two Leaver Profiles**: High performers burnt out by excessive hours vs. dissatisfied, under-utilized staff."
    )

with st.sidebar.expander("Champion Model", expanded=False):
    st.markdown(
        "**Random Forest 2 (Engineered)**\n"
        "- **ROC-AUC**: `0.935`\n"
        "- **Accuracy**: `96.0%`\n"
        "- **Recall**: `89.8%`\n"
        "- **Precision**: `86.6%`\n"
        "- **Key Drivers**: Evaluation score, project count, tenure, overwork status"
    )

with st.sidebar.expander("Project Deliverables", expanded=False):
    st.caption("Download reports and datasets generated during this project:")

    csv_bytes = _load_deliverable("cleaned_hr_dataset.csv")
    if csv_bytes:
        st.download_button(
            label="Cleaned Dataset (CSV)",
            data=csv_bytes,
            file_name="cleaned_hr_dataset.csv",
            mime="text/csv",
            width='stretch',
        )

    pdf_bytes = _load_deliverable("executive-summary.pdf")
    if pdf_bytes:
        st.download_button(
            label="Executive Summary (PDF)",
            data=pdf_bytes,
            file_name="Salifort_Executive_Summary.pdf",
            mime="application/pdf",
            width='stretch',
        )

    pdf_bytes = _load_deliverable("PACE-strategy-document.pdf")
    if pdf_bytes:
        st.download_button(
            label="PACE Strategy Doc (PDF)",
            data=pdf_bytes,
            file_name="PACE_Strategy_Document.pdf",
            mime="application/pdf",
            width='stretch',
        )

st.sidebar.divider()

# Sidebar footer
st.sidebar.markdown(
    "**[GitHub Repository](https://github.com/Mahmoud-islamcs/employee-turnover-prediction)**  \n"
    "**Mahmoud Islam**"
)
st.sidebar.caption("Static Dashboard · Streamlit & Plotly")

# --------------------------------------------------------------------------- #
# 1. Overview
# --------------------------------------------------------------------------- #
if page == PAGES[0]:
    st.title("Salifort Motors - Employee Retention")
    st.subheader("What's likely to make an employee leave the company?")
    st.write(
        "Salifort Motors' HR department collected employee survey and HR data but had no way to use it. "
        "The goal of this capstone is to analyse the data, build predictive models for whether an "
        "employee will leave (`left`), and give HR data-driven retention recommendations."
    )

    c = st.columns(4)
    with c[0]:
        st.metric(
            label="Raw Survey Records",
            value="14,999",
            delta="10 initial features",
            delta_color="off",
            delta_arrow="off",
            help="Full initial dataset collected across 10 company departments prior to validation and cleaning."
        )
        st.caption("10 departments · zero nulls")

    with c[1]:
        st.metric(
            label="Validated Workforce",
            value="11,991",
            delta="-3,008 duplicates (20.1%)",
            delta_color="normal",
            help="High-quality cohort retained after removing duplicate responses for reliable modeling."
        )
        st.caption("Clean modeling dataset")

    with c[2]:
        st.metric(
            label="Observed Turnover",
            value="1,991",
            delta="16.6% attrition rate",
            delta_color="inverse",
            help="1,991 employees left Salifort Motors while 10,000 stayed (moderate class imbalance of ~83.4% / 16.6%)."
        )
        st.caption("10,000 stayed · 1,991 left")

    with c[3]:
        st.metric(
            label="Champion Model (RF2)",
            value="0.935",
            delta="96.0% acc · 89.8% rec",
            delta_color="normal",
            help="Feature-engineered Random Forest model evaluated on the hold-out test set (test ROC-AUC: 0.935, recall: 89.8%, precision: 86.6%)."
        )
        st.caption("Hold-out test ROC-AUC score")

    st.markdown("### Project at a glance")
    left, right = st.columns(2)
    with left:
        st.markdown(
            """
            **Task type:** binary classification (`left` = 1 / 0)

            **Stakeholders**
            - Senior leadership team
            - HR department
            - Employees (indirectly affected)
            - Other data professionals on the team

            **Models built:** Logistic Regression, Decision Tree, Random Forest
            (tree models tuned with 4-fold GridSearchCV, refit on ROC-AUC)
            """
        )
    with right:
        st.markdown(
            """
            **Key findings**
            - Employees are **overworked**: most work well above the ~167 hrs/month norm.
            - **Everyone with 7 projects left**; 6-7 projects means ~14-32% more hours than average.
            - Leavers split in two groups: **burnt-out high performers** and
              **under-used, low-satisfaction** employees.
            - **Tenure of ~4 years** shows an unusually dissatisfied group of leavers.
            - Top predictors: `last_evaluation`, `num_projects`, `years_at_company`, `overworked`.
            """
        )

    note("Pages in the sidebar: <b>Data</b> (dictionary, cleaning), <b>EDA</b> (all plots with takeaways), "
         "<b>Models</b> (every model and its results), <b>Model comparison</b>, <b>Recommendations</b>, "
         "<b>PACE workflow</b>.")

# --------------------------------------------------------------------------- #
# 2. Data
# --------------------------------------------------------------------------- #
elif page == PAGES[1]:
    st.title("The data")
    st.caption("HR Analytics dataset (Kaggle: mfaisalqureshi/hr-analytics-and-job-prediction) - 15,000 rows, 10 columns")

    t1, t2, t3 = st.tabs(["Data dictionary", "Descriptive statistics", "Cleaning steps"])

    with t1:
        st.dataframe(DATA_DICT, width='stretch', hide_index=True)
        note("Columns were standardised to <code>snake_case</code>, a misspelling was fixed "
             "(<code>average_montly_hours</code>) and names were made more concise.")

    with t2:
        st.markdown("**`df0.describe()` on the raw dataset (14,999 rows)**")
        st.dataframe(DESCRIBE.style.format("{:.3f}"), width='stretch')
        st.markdown(
            "- No missing values in any column.\n"
            "- `satisfaction_level` and `last_evaluation` range from 0-1.\n"
            "- Hours range 96-310 per month; tenure 2-10 years; only ~2% were promoted in 5 years."
        )

    with t3:
        steps = pd.DataFrame(
            [
                ("1", "Load data", "14,999 rows x 10 columns"),
                ("2", "Rename columns", "snake_case + fix misspelling"),
                ("3", "Missing values", "None found"),
                ("4", "Duplicates", "3,008 duplicated rows found and dropped (keep='first')"),
                ("5", "Clean dataset", "11,991 rows x 10 columns (`cleaned_hr_dataset.csv`)"),
                ("6", "Outliers", "`years_at_company` IQR limits 1.5 - 5.5; outlier rows removed "
                                  "only for logistic regression (sensitive to outliers)"),
                ("7", "Encoding", "`salary` ordinal (low=0, medium=1, high=2); `department` one-hot"),
            ],
            columns=["#", "Step", "Result"],
        )
        st.dataframe(steps, width='stretch', hide_index=True)

        c1, c2 = st.columns([1, 1])
        with c1:
            st.markdown("**Employees per department (after cleaning)**")
            fig = px.bar(DEPT_COUNTS.sort_values("employees"), x="employees", y="department", orientation="h")
            fig.update_layout(height=380, margin=dict(t=10, b=10))
            st.plotly_chart(fig, width='stretch')
        with c2:
            st.markdown("**Target balance**")
            cc = st.columns(2)
            cc[0].metric("Left (clean data)", "1,991", "16.6%", delta_color="off", delta_arrow="off")
            cc[1].metric("Stayed (clean data)", "10,000", "83.4%", delta_color="off", delta_arrow="off")
            note("The imbalance (~83 / 17) is not severe (guideline for severe imbalance is 1:10 or worse), "
                 "so no resampling was applied. Stratified splits were used for the LR and second-round tree models.")
            df_clean = get_clean_data()
            if not df_clean.empty:
                fig_outliers = px.box(
                    df_clean, x="years_at_company", points="all",
                    title="Years at Company (Outlier Detection)",
                    labels={"years_at_company": "Years at Company"}
                )
                fig_outliers.update_layout(height=260, margin=dict(t=40, b=10, l=10, r=10))
                st.plotly_chart(fig_outliers, width='stretch')

# --------------------------------------------------------------------------- #
# 3. EDA
# --------------------------------------------------------------------------- #
elif page == PAGES[2]:
    st.title("Exploratory data analysis")
    note("All charts below are interactive Plotly visualizations generated directly from the cleaned dataset.")

    df_clean = get_clean_data()

    st.subheader("Hours worked and number of projects")
    if not df_clean.empty:
        c1, c2 = st.columns(2)
        with c1:
            fig_hp_box = px.box(
                df_clean, x="avg_monthly_hours", y="num_projects", color="status",
                orientation="h",
                color_discrete_map={"Stayed": "#4C78A8", "Left": "#E45756"},
                category_orders={"num_projects": [2, 3, 4, 5, 6, 7]},
                labels={"avg_monthly_hours": "Average Monthly Hours", "num_projects": "Number of Projects", "status": "Status"},
                title="Monthly Hours by Number of Projects"
            )
            fig_hp_box.update_layout(height=420, margin=dict(t=40, b=10))
            st.plotly_chart(fig_hp_box, width='stretch')
        with c2:
            fig_hp_hist = px.histogram(
                df_clean, x="num_projects", color="status", barmode="group",
                color_discrete_map={"Stayed": "#4C78A8", "Left": "#E45756"},
                labels={"num_projects": "Number of Projects", "status": "Status", "count": "Employee Count"},
                title="Employee Count by Number of Projects"
            )
            fig_hp_hist.update_layout(height=420, margin=dict(t=40, b=10))
            st.plotly_chart(fig_hp_hist, width='stretch')

    st.markdown(
        "- Mean monthly hours rise with the number of projects, as expected.\n"
        "- Leavers form two groups: **under-worked** vs. peers, and **heavily over-worked**.\n"
        "- **3-4 projects** looks optimal - very few leavers.\n"
        "- **All 145 employees with 7 projects left.**\n"
        "- Average hours: 7 projects = **275.6**, 6 projects = **230.4**, <6 projects = **200.5** "
        "(+31.8% and +14.1% vs. company average). A normal month is ~166.7 hrs."
    )

    st.divider()
    st.subheader("Hours vs. satisfaction")
    if not df_clean.empty:
        fig_hs = px.scatter(
            df_clean, x="avg_monthly_hours", y="satisfaction_level", color="status",
            opacity=0.45,
            color_discrete_map={"Stayed": "#4C78A8", "Left": "#E45756"},
            labels={"avg_monthly_hours": "Average Monthly Hours", "satisfaction_level": "Job Satisfaction [0-1]", "status": "Status"},
            title="Monthly Hours vs. Satisfaction Level"
        )
        fig_hs.add_vline(x=166.67, line_dash="dash", line_color="#D95F02", annotation_text="166.7 hrs/mo (Standard)", annotation_position="top left")
        fig_hs.update_layout(height=480, margin=dict(t=40, b=10))
        st.plotly_chart(fig_hs, width='stretch')

    st.markdown(
        "- A large group works ~240-315 hrs/month (75+ hrs/week) with satisfaction near zero - all left.\n"
        "- A second group of leavers works *fewer* than 166.7 hrs with satisfaction ~0.4.\n"
        "- The odd cluster shapes suggest the dataset is synthetic."
    )

    st.divider()
    st.subheader("Satisfaction vs. tenure")
    if not df_clean.empty:
        c1, c2 = st.columns(2)
        with c1:
            fig_st_box = px.box(
                df_clean, x="satisfaction_level", y="years_at_company", color="status",
                orientation="h",
                color_discrete_map={"Stayed": "#4C78A8", "Left": "#E45756"},
                category_orders={"years_at_company": [2, 3, 4, 5, 6, 7, 8, 10]},
                labels={"satisfaction_level": "Satisfaction Level", "years_at_company": "Years at Company", "status": "Status"},
                title="Satisfaction Level vs. Tenure"
            )
            fig_st_box.update_layout(height=420, margin=dict(t=40, b=10))
            st.plotly_chart(fig_st_box, width='stretch')
        with c2:
            fig_st_hist = px.histogram(
                df_clean, x="years_at_company", color="status", barmode="group",
                color_discrete_map={"Stayed": "#4C78A8", "Left": "#E45756"},
                labels={"years_at_company": "Years at Company", "status": "Status", "count": "Employee Count"},
                title="Tenure Distribution by Status"
            )
            fig_st_hist.update_layout(height=420, margin=dict(t=40, b=10))
            st.plotly_chart(fig_st_hist, width='stretch')

    st.markdown(
        "- Most departures happen in the **first ~2 years**; the longest-serving employees did not leave.\n"
        "- Leavers after **year 4** have unusually low satisfaction - worth investigating.\n"
        "- Median satisfaction: **stayed 0.69** vs **left 0.41** (mean 0.667 vs 0.440)."
    )
    sat = pd.DataFrame({"group": ["Stayed", "Left"], "mean": [0.667365, 0.440271], "median": [0.69, 0.41]})
    st.dataframe(sat, hide_index=True, width='content')

    st.divider()
    st.subheader("Salary and tenure")
    if not df_clean.empty:
        c1, c2 = st.columns(2)
        with c1:
            fig_sal_short = px.histogram(
                df_clean[df_clean["years_at_company"] < 7], x="years_at_company", color="salary", barmode="group",
                category_orders={"salary": ["low", "medium", "high"]},
                color_discrete_map={"low": "#E45756", "medium": "#F58518", "high": "#4C78A8"},
                title="Short-tenured Employees (< 7 years)",
                labels={"years_at_company": "Years at Company", "salary": "Salary Band"}
            )
            fig_sal_short.update_layout(height=380, margin=dict(t=40, b=10))
            st.plotly_chart(fig_sal_short, width='stretch')
        with c2:
            fig_sal_long = px.histogram(
                df_clean[df_clean["years_at_company"] >= 7], x="years_at_company", color="salary", barmode="group",
                category_orders={"salary": ["low", "medium", "high"]},
                color_discrete_map={"low": "#E45756", "medium": "#F58518", "high": "#4C78A8"},
                title="Long-tenured Employees (>= 7 years)",
                labels={"years_at_company": "Years at Company", "salary": "Salary Band"}
            )
            fig_sal_long.update_layout(height=380, margin=dict(t=40, b=10))
            st.plotly_chart(fig_sal_long, width='stretch')

    st.markdown("Long-tenured employees are **not** disproportionately high-paid - there are more medium-salary "
                "long-tenured employees.")

    st.divider()
    st.subheader("Hours vs. last evaluation")
    if not df_clean.empty:
        fig_he = px.scatter(
            df_clean, x="avg_monthly_hours", y="last_evaluation", color="status",
            opacity=0.45,
            color_discrete_map={"Stayed": "#4C78A8", "Left": "#E45756"},
            labels={"avg_monthly_hours": "Average Monthly Hours", "last_evaluation": "Last Evaluation Score [0-1]", "status": "Status"},
            title="Monthly Hours vs. Last Evaluation Score"
        )
        fig_he.add_vline(x=166.67, line_dash="dash", line_color="#D95F02", annotation_text="166.7 hrs/mo (Standard)", annotation_position="top left")
        fig_he.update_layout(height=480, margin=dict(t=40, b=10))
        st.plotly_chart(fig_he, width='stretch')

    st.markdown(
        "- Two leaver groups again: **over-worked high performers** and slightly under-hours employees with lower scores.\n"
        "- Hours and evaluation are correlated, but **long hours do not guarantee a high evaluation**.\n"
        "- Most employees work well above 166.7 hrs/month."
    )

    st.divider()
    st.subheader("Hours vs. promotion in the last 5 years")
    if not df_clean.empty:
        fig_hp = px.strip(
            df_clean, x="avg_monthly_hours", y="promotion_last_5_years", color="status",
            color_discrete_map={"Stayed": "#4C78A8", "Left": "#E45756"},
            labels={"avg_monthly_hours": "Average Monthly Hours", "promotion_last_5_years": "Promoted in Last 5 Years (0=No, 1=Yes)", "status": "Status"},
            title="Monthly Hours vs. Promotion in Last 5 Years"
        )
        fig_hp.add_vline(x=166.67, line_dash="dash", line_color="#D95F02", annotation_text="166.7 hrs/mo", annotation_position="top left")
        fig_hp.update_layout(height=380, margin=dict(t=40, b=10))
        st.plotly_chart(fig_hp, width='stretch')

    st.markdown("Very few were promoted, and very few of the longest-hours employees were promoted. "
                "All employees who left were among the longest-hours group.")

    st.divider()
    st.subheader("Departments")
    if not df_clean.empty:
        fig_dept = px.histogram(
            df_clean, x="department", color="status", barmode="group",
            color_discrete_map={"Stayed": "#4C78A8", "Left": "#E45756"},
            labels={"department": "Department", "status": "Status", "count": "Employee Count"},
            title="Employee Headcount & Leavers by Department"
        )
        fig_dept.update_layout(xaxis={"categoryorder": "total descending"}, height=420, margin=dict(t=40, b=10))
        st.plotly_chart(fig_dept, width='stretch')

    st.markdown("No department differs notably in its leave / stay proportion.")

    st.divider()
    st.subheader("Correlation heatmap")
    if not df_clean.empty:
        num_cols = ["satisfaction_level", "last_evaluation", "num_projects", "avg_monthly_hours", "years_at_company", "work_accident", "left", "promotion_last_5_years"]
        corr_matrix = df_clean[num_cols].corr()
        fig_corr = px.imshow(
            corr_matrix, text_auto=".2f", color_continuous_scale="RdBu_r", zmin=-1, zmax=1,
            title="Correlation Heatmap (Numerical Features)",
            aspect="auto"
        )
        fig_corr.update_layout(height=520, margin=dict(t=40, b=10))
        st.plotly_chart(fig_corr, width='stretch')
    st.markdown(
        "- `last_evaluation`, `num_projects` and `avg_monthly_hours` are positively correlated with each other.\n"
        "- `left` is negatively correlated with `satisfaction_level`.\n"
        "- `years_at_company` and `satisfaction_level` are negatively correlated."
    )

    note("<b>Insight:</b> leaving is tied to long hours, many projects and low satisfaction. Employees are "
         "working harder without extra incentives (promotion, evaluation) - probable burnout, and a case can be "
         "made for management issues. Employees beyond 5 years tend to stay.")

# --------------------------------------------------------------------------- #
# 4. Models
# --------------------------------------------------------------------------- #
elif page == PAGES[3]:
    st.title("Models")
    st.markdown(
        "**Prediction task:** binary classification of `left`. Logistic regression and tree-based models "
        "(Decision Tree, Random Forest) were appropriate."
    )

    tabs = st.tabs([
        "A. Logistic Regression",
        "B1. Trees - all features",
        "B2. Trees - feature engineering",
        "Feature importance",
    ])

    # ---- Logistic regression
    with tabs[0]:
        st.markdown("#### Logistic regression")
        c = st.columns(4)
        with c[0]:
            st.metric(
                label="Modeling Sample",
                value="11,167",
                delta="-824 outliers removed",
                delta_color="off",
                help="Total observations after filtering extreme tenure outliers (> 5.5 years) to satisfy logistic regression assumptions."
            )
            st.caption("8,375 train · 2,792 test")

        with c[1]:
            st.metric(
                label="Data Partition",
                value="75 / 25",
                delta="Stratified (rs=0)",
                delta_color="off",
                help="Stratified split preserving the exact 16.6% turnover class ratio across training and testing partitions."
            )
            st.caption("Stratified sampling")

        with c[2]:
            st.metric(
                label="Hold-out Test Set",
                value="2,792",
                delta="25% evaluation rows",
                delta_color="off",
                help="Independent hold-out test set used to evaluate true generalization, confusion matrix, and ROC-AUC."
            )
            st.caption("Unseen test rows")

        with c[3]:
            st.metric(
                label="Solver Iterations",
                value="500",
                delta="max_iter (converged)",
                delta_color="normal",
                help="Maximum iterations allocated to the L-BFGS optimization algorithm to guarantee complete gradient convergence."
            )
            st.caption("Guaranteed convergence")

        st.markdown("**Assumptions checked**")
        st.markdown(
            "- Binary outcome - yes\n"
            "- Independent observations - yes\n"
            "- No severe multicollinearity - highest pair `num_projects` vs `avg_monthly_hours` = 0.33, so OK\n"
            "- Extreme outliers - `years_at_company` outliers removed (IQR 1.5-5.5)"
        )
        cc = st.columns([1, 1])
        df_clean = get_clean_data()
        with cc[0]:
            if not df_clean.empty:
                lr_vars = ["satisfaction_level", "last_evaluation", "num_projects", "avg_monthly_hours", "years_at_company"]
                lr_corr = df_clean[lr_vars].corr()
                fig_lr_corr = px.imshow(
                    lr_corr, text_auto=".2f", color_continuous_scale="Viridis", zmin=0, zmax=1,
                    title="Multicollinearity Check (Continuous Features)",
                    aspect="auto"
                )
                fig_lr_corr.update_layout(height=380, margin=dict(t=40, b=10))
                st.plotly_chart(fig_lr_corr, width='stretch')
        with cc[1]:
            if not df_clean.empty:
                bal_df = df_clean["status"].value_counts().reset_index()
                bal_df.columns = ["Status", "Count"]
                bal_df["Percentage"] = (bal_df["Count"] / bal_df["Count"].sum() * 100).round(1).astype(str) + "%"
                fig_bal = px.bar(
                    bal_df, x="Status", y="Count", color="Status", text="Percentage",
                    color_discrete_map={"Stayed": "#4C78A8", "Left": "#E45756"},
                    title="Class Balance (Target Variable: left)"
                )
                fig_bal.update_traces(textposition="outside")
                fig_bal.update_layout(height=380, margin=dict(t=40, b=10), showlegend=False)
                st.plotly_chart(fig_bal, width='stretch')

        st.markdown("**Baseline vs. `class_weight='balanced'` (test set, class = left)**")
        lr_tbl = TEST.iloc[:2][["Version", "Accuracy", "Precision", "Recall", "F1"]]
        st.dataframe(lr_tbl, hide_index=True, width='stretch')
        note("Baseline recall for leavers was only <b>24%</b>. Balancing class weights raised recall to "
             "<b>91%</b> (precision 51%), catching far more leavers at the cost of more false alarms.")

        c1, c2 = st.columns(2)
        c1.plotly_chart(confusion_fig(CONFUSION["Logistic Regression (baseline)"], "Baseline"), width='stretch')
        c2.plotly_chart(confusion_fig(CONFUSION["Logistic Regression (balanced)"], "Balanced"), width='stretch')

        st.markdown("**ROC curve - AUC = 0.892**")
        df_roc = pd.DataFrame(ROC_POINTS, columns=["FPR", "TPR"])
        fig_roc = px.line(
            df_roc, x="FPR", y="TPR",
            title="Logistic Regression ROC Curve (Test AUC = 0.892)",
            labels={"FPR": "False Positive Rate (1 - Specificity)", "TPR": "True Positive Rate (Recall)"}
        )
        fig_roc.add_shape(type="line", line=dict(dash="dash", color="gray"), x0=0, x1=1, y0=0, y1=1)
        fig_roc.update_layout(height=420, margin=dict(t=40, b=10))
        st.plotly_chart(fig_roc, width='stretch')

        st.markdown("**Model coefficients**")
        coef = LR_COEF.sort_values("coefficient")
        fig = px.bar(coef, x="coefficient", y="feature", orientation="h",
                     color=coef["coefficient"] > 0,
                     color_discrete_map={True: "#E45756", False: "#4C78A8"})
        fig.update_layout(showlegend=False, height=520, margin=dict(t=10, b=10))
        st.plotly_chart(fig, width='stretch')
        st.caption("Blue lowers the log-odds of leaving, red raises it. Strongest: satisfaction_level (-4.44), "
                   "work_accident (-1.47), years_at_company (+1.03).")

        note("<b>Verdict:</b> logistic regression performed poorly on the class that matters (leavers). "
             "Overall metrics look fine mostly because of the majority class.", "warn")

    # ---- Trees round 1
    with tabs[1]:
        st.markdown("#### Decision Tree & Random Forest - first iteration (all features)")
        st.markdown(
            "Split 75/25 (random_state=42). `GridSearchCV` with 4-fold CV, scoring on "
            "accuracy / precision / recall / F1 / ROC-AUC, **refit on ROC-AUC**."
        )
        c1, c2 = st.columns(2)
        with c1:
            st.markdown("**Decision tree grid**")
            st.code("max_depth: [4, 6, 8, None]\nmin_samples_leaf: [1, 3, 5]\nmin_samples_split: [2, 4, 6]", language="text")
            st.markdown("Best: `max_depth=6, min_samples_leaf=1, min_samples_split=4` - CV AUC **0.9689** (grid)")
        with c2:
            st.markdown("**Random forest grid**")
            st.code("max_depth: [4, 6, 8, None]\nmax_features: [1.0]\nmax_samples: [0.7, 1.0]\n"
                    "min_samples_leaf: [1, 2, 3]\nmin_samples_split: [2, 3, 4]\nn_estimators: [500]", language="text")
            st.markdown("Best: `max_depth=8, max_samples=0.7, min_samples_leaf=3, min_samples_split=2` - "
                        "CV AUC **0.9789** (grid)")

        st.dataframe(CV.iloc[:2].style.format({c: "{:.3f}" for c in ["F1", "Recall", "Precision", "Accuracy", "AUC"]}),
                     hide_index=True, width='stretch')
        st.markdown("**Random Forest 1 on test set:** accuracy 0.982, precision 0.985, recall 0.903, F1 0.942, AUC 0.950")
        note("Scores looked <b>too good to be true</b> - suspected <b>data leakage</b>: "
             "`satisfaction_level` will not exist for every employee in production, and `avg_monthly_hours` "
             "may reflect people who had already decided to leave (or been flagged) working less. "
             "This motivated a second iteration with feature engineering.", "warn")
        with st.expander("Decision tree 1 - top levels structural diagram"):
            show_image("dt1_tree", "Decision tree (first iteration), top levels")

    # ---- Trees round 2
    with tabs[2]:
        st.markdown("#### Second iteration - feature engineering")
        st.markdown(
            "- **Dropped** `satisfaction_level` (not available for every employee).\n"
            "- **Created** `overworked` = 1 if `avg_monthly_hours` > 170 (~166.7 is a normal month), then "
            "**dropped** `avg_monthly_hours`.\n"
            "- Stratified 75/25 split (random_state=0)."
        )
        c1, c2 = st.columns(2)
        with c1:
            st.markdown("**Decision tree grid**")
            st.code("max_depth: [6, 8, 10, None]\nmin_samples_leaf: [1, 2, 3, 5]\nmin_samples_split: [2, 4, 6, 8]", language="text")
            st.markdown("Best: `max_depth=6, min_samples_leaf=2, min_samples_split=6` - CV AUC **0.9584** (grid)")
        with c2:
            st.markdown("**Random forest grid**")
            st.code("max_depth: [2, 3, 5, 8, None]\nmax_features: [1.0]\nmax_samples: [0.7, 1.0]\n"
                    "min_samples_leaf: [1, 2, 3]\nmin_samples_split: [2, 3, 4]\nn_estimators: [500]", language="text")
            st.markdown("Best: `max_depth=5, max_samples=0.7, min_samples_leaf=3, min_samples_split=2` - "
                        "CV AUC **0.9647** (grid; 90 candidates x 4 folds = 360 fits)")

        st.dataframe(CV.iloc[2:].style.format({c: "{:.3f}" for c in ["F1", "Recall", "Precision", "Accuracy", "AUC"]}),
                     hide_index=True, width='stretch')
        note("Scores dropped slightly versus round 1, as expected with fewer features, but the models remain strong "
             "and more realistic. The random forest beats the decision tree on cross-validated AUC.")

        st.markdown("**Champion - Random Forest 2 on the test set**")
        c = st.columns(5)
        for col, (k, v) in zip(c, [("Accuracy", "0.960"), ("Precision", "0.866"), ("Recall", "0.898"),
                                   ("F1", "0.882"), ("AUC", "0.935")]):
            col.metric(k, v)
        st.plotly_chart(confusion_fig(CONFUSION["Random Forest 2 (champion)"], "Random Forest 2 - test set"),
                        width='stretch')
        st.caption("2,431 true negatives, 69 false positives, 51 false negatives, 447 true positives. "
                   "More false positives than false negatives: some employees are flagged as at risk when they are not.")

        with st.expander("Decision tree 2 - full splits (large image)"):
            show_image("dt2_tree")

    # ---- Importances
    with tabs[3]:
        st.markdown("#### Feature importance (second iteration)")
        c1, c2 = st.columns(2)
        with c1:
            st.markdown("**Decision tree (Gini importance)**")
            d = DT2_IMPORTANCE.sort_values("importance")
            fig = px.bar(d, x="importance", y="feature", orientation="h")
            fig.update_layout(height=420, margin=dict(t=10, b=10))
            st.plotly_chart(fig, width='stretch')
        with c2:
            st.markdown("**Random forest (top 10)**")
            rf_top = RF2_IMPORTANCE.sort_values("importance")
            fig_rf2 = px.bar(
                rf_top, x="importance", y="feature", orientation="h",
                labels={"importance": "Importance", "feature": "Feature"}
            )
            fig_rf2.update_layout(height=420, margin=dict(t=10, b=10))
            st.plotly_chart(fig_rf2, width='stretch')
        note("Both models agree: <code>last_evaluation</code>, <code>num_projects</code>, "
             "<code>years_at_company</code> and <code>overworked</code> carry nearly all the predictive power. "
             "Department, salary and work accident are close to zero.")

# --------------------------------------------------------------------------- #
# 5. Comparison
# --------------------------------------------------------------------------- #
elif page == PAGES[4]:
    st.title("Model comparison")

    st.subheader("Cross-validation results (4-fold, training set)")
    st.dataframe(CV.style.format({c: "{:.3f}" for c in ["F1", "Recall", "Precision", "Accuracy", "AUC"]}),
                 hide_index=True, width='stretch')

    metric = st.selectbox("Metric to chart", ["AUC", "F1", "Recall", "Precision", "Accuracy"])
    cv_plot = CV.assign(Label=CV["Model"])
    fig = px.bar(cv_plot, x="Label", y=metric, color="Feature set", text=cv_plot[metric].round(3))
    fig.update_layout(height=380, yaxis_range=[0.8, 1.0], xaxis_title=None, margin=dict(t=10, b=10))
    st.plotly_chart(fig, width='stretch')

    st.subheader("Hold-out test results")
    st.dataframe(
        TEST.style.format({c: "{:.3f}" for c in ["Accuracy", "Precision", "Recall", "F1", "AUC"]}, na_rep="-"),
        hide_index=True, width='stretch',
    )
    st.caption("Logistic regression rows use the 'left' class from the classification report (test set of 2,792 "
               "after outlier removal). The LR AUC (0.892) was computed for the baseline model.")

    st.subheader("Best hyper-parameters")
    st.dataframe(BEST_PARAMS, hide_index=True, width='stretch')

    note("<b>Reading the results honestly:</b> Random Forest 2 is the champion because it has the best "
         "cross-validated AUC among the leak-reduced models (0.961 vs 0.953 for the decision tree). On the "
         "test set, however, the two are very close (AUC 0.935 vs 0.938) - the random forest's edge is modest. "
         "Round-1 scores (AUC 0.95-0.98) are higher but rely on `satisfaction_level` and `avg_monthly_hours`, "
         "which are likely leaky.")

    note("<b>Choosing a model:</b> to catch as many leavers as possible, recall matters most; the balanced "
         "logistic regression reaches 91% recall but with only 51% precision, while Random Forest 2 gives "
         "~90% recall at ~87% precision.")

# --------------------------------------------------------------------------- #
# 6. Recommendations
# --------------------------------------------------------------------------- #
elif page == PAGES[5]:
    st.title("Conclusion & recommendations")

    st.subheader("Summary of model results")
    st.markdown(
        "- **Logistic regression** performed poorly at predicting leavers (recall 24% baseline, 91% balanced but low precision).\n"
        "- **Tree-based models** after feature engineering reached, on the test set, AUC 93.8% / precision 87% / "
        "recall 90.4% / F1 88.7% / accuracy 96.2% (decision tree). The random forest modestly outperformed it in cross-validation.\n"
        "- Models and feature importances confirm that employees are **overworked**."
    )

    st.subheader("Recommendations for stakeholders")
    recs = [
        ("Cap the number of projects", "Employees with 6-7 projects work 14-32% more than average and all with 7 projects left."),
        ("Look at the 4-year mark", "Promote employees with 4+ years of tenure, or investigate why 4-year employees are so dissatisfied."),
        ("Reward or reduce overtime", "Either compensate employees for long hours, or do not require them."),
        ("Clarify overtime & time-off policies", "If employees are unaware of overtime pay or workload / time-off expectations, communicate them explicitly."),
        ("Discuss company culture", "Hold company-wide and team-level discussions to understand and address work culture."),
        ("Proportional evaluation scale", "High evaluation scores should not be reserved for people working 200+ hrs/month."),
    ]
    for i, (t, d) in enumerate(recs, 1):
        st.markdown(f"**{i}. {t}** - {d}")

    st.subheader("Next steps")
    st.markdown(
        "- Concern about leakage: `last_evaluation` may not exist for every employee in production - consider dropping it and re-evaluating.\n"
        "- Explore a **K-means** model and analyse the clusters.\n"
        "- Investigate the ~4-year tenure dissatisfaction spike and the under-worked leaver group."
    )

    st.subheader("Ethical considerations")
    st.markdown(
        "Data privacy and security, bias and fairness, anonymisation / aggregation, informed consent for "
        "surveys, and transparency about model methods and limitations."
    )

# --------------------------------------------------------------------------- #
# 7. PACE
# --------------------------------------------------------------------------- #
else:
    st.title("PACE workflow")
    st.caption("Plan - Analyze - Construct - Execute")

    st.dataframe(
        pd.DataFrame(
            [
                (1, "Understand the business scenario and define the problem", "Plan"),
                (2, "Data exploration and data cleaning", "Plan, Analyze"),
                (3, "Determine which models are most appropriate", "Analyze, Construct"),
                (4, "Construct the model", "Construct"),
                (5, "Confirm model assumptions", "Analyze, Construct"),
                (6, "Evaluate model results", "Analyze"),
                (7, "Interpret results and share actionable steps with stakeholders", "Execute"),
            ],
            columns=["Milestone", "Task", "PACE stage"],
        ),
        hide_index=True, width='stretch',
    )

    p, a, c, e = st.tabs(["Plan", "Analyze", "Construct", "Execute"])
    with p:
        st.markdown(
            "- **Problem:** HR wants to understand why employees leave and predict turnover.\n"
            "- **Audience / stakeholders:** senior leadership, HR, employees, fellow data professionals.\n"
            "- **Data:** 15,000 rows, 10 columns; no missing values; no obvious integrity issues.\n"
            "- **Initial question about the data:** satisfaction and evaluation both range 0-1.\n"
            "- **Ethics:** privacy, fairness, anonymisation, informed consent, transparency."
        )
    with a:
        st.markdown(
            "- No linear relationships between variables; positive correlation among hours, projects and evaluation; "
            "`left` negatively correlated with satisfaction.\n"
            "- Duplicates found and removed; tenure outliers identified.\n"
            "- EDA used to learn patterns and ask the right questions before modelling."
        )
    with c:
        st.markdown(
            "- Chose logistic regression and tree-based models; checked LR assumptions.\n"
            "- Tuned trees with GridSearchCV (refit on AUC).\n"
            "- Suspected leakage in round 1 -> removed `satisfaction_level`, engineered `overworked`, dropped `avg_monthly_hours`."
        )
    with e:
        st.markdown(
            "- Evaluated on a hold-out test set; random forest chosen as the champion.\n"
            "- Key drivers: evaluation score, number of projects, tenure, overwork.\n"
            "- Delivered actionable recommendations for HR (see Recommendations page)."
        )
