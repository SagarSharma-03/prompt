# EA Analyst Assignment - Submission Package

## Author Information
- **Candidate:** Mathematics Student (SDE background, new to Analyst role)
- **SQL Experience:** Lower-intermediate level (SSMS 2022)
- **Python Experience:** Currently learning (Pandas, basic ML)
- **Submission Date:** [Today]

---

## Repository Structure

```
ea_submission/
├── README.md                          # This file
├── EXECUTIVE_SUMMARY.md               # Complete findings and recommendations
├── sql/                               # SQL queries (T-SQL compatible where possible)
│   ├── 1a_daily_health.sql
│   ├── 1b_retention.sql
│   ├── 1c_spender_behaviour.sql
│   ├── 1d_rewarded_ads.sql
│   └── 2a_arpdau_deep_dive.sql
├── python/                            # Python analysis scripts
│   ├── 3_acquisition_analysis.py
│   └── 4_churn_prediction.py
└── results/                           # Generated outputs
    ├── 1a_daily_health.csv
    ├── 1b_retention.csv
    ├── 1c_*.csv (multiple files)
    ├── 1d_*.csv (multiple files)
    ├── 2a_*.csv (multiple files)
    ├── 3_*.csv (multiple files)
    ├── 4_*.csv (multiple files)
    ├── 4_roc_curve.png
    └── 4_precision_recall_curve.png
```

---

## How to Run the Analysis

### Prerequisites

**Required Files (in parent directory):**
- `player_profile.csv`
- `player_day.csv`
- `purchase.csv`
- `currency_spend.csv`
- `ad_view.csv`

**Python Environment:**
- Python 3.8+
- See `requirements.txt` for package dependencies

### Installation

```bash
# Install required Python packages
pip install -r requirements.txt
```

### Running SQL Queries

The SQL queries were executed using DuckDB for data processing but are written to be compatible with Microsoft SQL Server / T-SQL where possible.

**To run in DuckDB (Python):**
```python
import duckdb

conn = duckdb.connect(':memory:')

# Load data
conn.execute("CREATE TABLE player_profile AS SELECT * FROM read_csv_auto('player_profile.csv')")
conn.execute("CREATE TABLE player_day AS SELECT * FROM read_csv_auto('player_day.csv')")
# ... load other tables

# Execute query
with open('ea_submission/sql/1a_daily_health.sql', 'r') as f:
    result = conn.execute(f.read()).fetchdf()
```

**To run in SQL Server:**
- Import CSV files into SQL Server tables
- Adjust date conversion syntax as needed (activity_date is stored as INT in YYYYMMDD format)
- Run queries in SSMS

### Running Python Scripts

```bash
cd /path/to/assignment/directory

# Acquisition analysis
python ea_submission/python/3_acquisition_analysis.py

# Churn prediction
python ea_submission/python/4_churn_prediction.py
```

**Note:** Scripts expect CSV files in the current directory and will save results to `ea_submission/results/`.

---

## Deliverables Completed

### ✅ Deliverable 1 - SQL Analysis

#### 1(a) Daily Health Metrics
- **File:** `sql/1a_daily_health.sql`
- **Output:** `results/1a_daily_health.csv`
- **Metrics:** DAU, Gross Revenue, ARPDAU, Payer Rate by date and platform
- **Key Finding:** iOS has higher ARPDAU ($0.50) than Android ($0.25)

#### 1(b) Retention Analysis
- **File:** `sql/1b_retention.sql`
- **Output:** `results/1b_retention.csv`
- **Metrics:** D1, D7, D14, D30 retention by install cohort
- **Key Finding:** Average D1 retention is 14.7%, stabilizes around 5-7% by D30

#### 1(c) Spender Behaviour
- **File:** `sql/1c_spender_behaviour.sql`
- **Output:** `results/1c_*.csv` (4 files)
- **Metrics:** Revenue concentration, payer rate, time-to-purchase, repeat purchase gaps
- **Key Findings:**
  - Top 10% of spenders generate 48% of revenue
  - 86% of players never pay
  - Median time to first purchase: 22 days
  - Data quality issue: some purchases before install date

#### 1(d) Rewarded Ads
- **File:** `sql/1d_rewarded_ads.sql`
- **Output:** `results/1d_*.csv` (5 files)
- **Metrics:** Ad cap hit rates, daily ad views, status breakdown, anomalies
- **Key Findings:**
  - Only 1-2% of players hit daily ad cap
  - 82% ad completion rate
  - Anomaly: Apr 27-30 show abnormally high ad views

### ✅ Deliverable 2(a) - ARPDAU Deep Dive

- **File:** `sql/2a_arpdau_deep_dive.sql`
- **Output:** `results/2a_*.csv` (3 files)
- **Analysis:** Simpson's Paradox investigation
- **Key Finding:** 
  - Overall ARPDAU fell 10.6% despite ALL country tiers improving
  - Caused by mix shift: Tier 4 (low ARPDAU) grew from 17% to 42% of player base

### ✅ Deliverable 3 - Acquisition Channel Analysis

- **File:** `python/3_acquisition_analysis.py`
- **Output:** `results/3_*.csv` (3 files)
- **Analysis:** Statistical comparison of organic, paid_social, paid_video channels
- **Key Findings:**
  - Paid Video has highest engagement (+17-24 min playtime vs others)
  - Revenue differences are small and mostly not statistically significant
  - All channels have similar conversion rates (8-9%)

### ✅ Deliverable 4 - Churn Prediction

- **File:** `python/4_churn_prediction.py`
- **Output:** `results/4_*.csv` (2 files) + `4_*.png` (2 charts)
- **Model:** Simple Logistic Regression (interpretable)
- **Performance:** ROC-AUC = 0.65 (moderate discrimination)
- **Key Findings:**
  - Ad engagement is strongest retention signal
  - High session frequency indicates stickiness
  - Counterintuitive: recent purchasers show higher churn risk (needs investigation)

### ✅ Deliverable 5 - Executive Summary

- **File:** `EXECUTIVE_SUMMARY.md`
- **Content:** 
  - All key findings
  - Business recommendations
  - Data quality issues
  - Interview preparation guide

### ❌ Deliverable 2(b) - Sales/Promotions Deep Dive

- **Status:** Skipped as instructed in assignment

### ❌ Deliverable 4(b) - 90-Day Install Value Prediction

- **Status:** Skipped as instructed in assignment

---

## Key Assumptions & Decisions

### Data Handling

1. **Date Formats:**
   - `player_day.activity_date` is stored as INTEGER in YYYYMMDD format
   - Converted using `STRPTIME` in DuckDB or appropriate function in SQL Server

2. **Missing Values:**
   - Left joins used to preserve all players
   - NULL values filled with 0 where appropriate (e.g., revenue, playtime)

3. **Observation Windows:**
   - Deliverable 3: Only players installed before 2026-03-31 (complete 30-day window)
   - Deliverable 4: As-of date 2026-04-02 with 14-day churn window

4. **Data Quality Issues:**
   - Negative time-to-purchase values identified but included in analysis
   - Ad view anomaly flagged but data used as-is
   - Documented in EXECUTIVE_SUMMARY.md

### Methodology Choices

1. **Why Logistic Regression?**
   - Simple and interpretable
   - Easy to explain in interview
   - Aligns with assignment preference for interpretability over complexity

2. **Why Time-Based Train/Test Split?**
   - Avoids data leakage
   - More realistic: predict future from past
   - Standard practice for time-series data

3. **Why 30-Day Windows?**
   - Balances data completeness with sample size
   - Industry standard
   - Sufficient to observe early behavior patterns

4. **Why T-Tests for Acquisition?**
   - Simple and interpretable
   - Appropriate for continuous metrics
   - Provides confidence intervals for business decisions

---

## Known Limitations

### Data Limitations

1. **Incomplete Observation for Early Cohorts:**
   - Player_day data starts 2026-01-01
   - Players installed before Dec 2025 have incomplete historical activity
   - Affects early cohort retention metrics

2. **Single Observation Period:**
   - Cannot assess seasonality or long-term trends
   - 4-month window may not capture full player lifecycle

3. **Missing Context:**
   - No information on game events, promotions, or product changes
   - No marketing spend or CAC data for true ROI analysis

### Model Limitations

1. **Churn Model:**
   - Moderate predictive power (ROC-AUC 0.65)
   - Distribution shift between train/test sets
   - Simple features only (no social, progression, or event features)
   - Time-based split means test set is more recent players

2. **Acquisition Analysis:**
   - Only 30-day window observed
   - True LTV requires longer observation period
   - No cost per install data for ROI calculation

3. **Statistical Tests:**
   - Assumes independence of observations
   - Large sample sizes mean small differences become statistically significant
   - Business significance must be evaluated separately

---

## Interview Preparation Notes

### Concepts to Review

1. **SQL:**
   - JOIN types and logic
   - Window functions (ROW_NUMBER, RANK)
   - Aggregation vs filtering (WHERE vs HAVING)
   - Date arithmetic

2. **Statistics:**
   - Confidence intervals and interpretation
   - p-values (what they mean, what they don't mean)
   - Statistical vs business significance
   - Simpson's Paradox

3. **Machine Learning:**
   - What is logistic regression? (log-odds, sigmoid, decision boundary)
   - What is a feature? What is a target variable?
   - Train/test split rationale
   - Evaluation metrics: accuracy, precision, recall, ROC-AUC
   - Confusion matrix
   - Overfitting and data leakage

4. **Business Metrics:**
   - DAU, MAU, retention
   - ARPDAU vs ARPPU vs LTV
   - Cohort analysis
   - Churn vs retention

### Likely Interview Questions

1. **ARPDAU Analysis:**
   - "Walk me through your ARPDAU analysis. Why did overall ARPDAU fall?"
   - "What is Simpson's Paradox?"
   - "How would you fix this issue?"

2. **Acquisition:**
   - "Which channel would you invest in and why?"
   - "What's missing from this analysis?"
   - "How do confidence intervals help decision-making?"

3. **Churn Model:**
   - "Explain your churn model in simple terms."
   - "Why did you choose these features?"
   - "What does ROC-AUC mean?"
   - "Why is accuracy high but ROC-AUC moderate?"
   - "Why time-based split instead of random?"

4. **Data Quality:**
   - "What data quality issues did you find?"
   - "How did you handle them?"
   - "What would you investigate further?"

5. **Next Steps:**
   - "If you had more time, what would you analyze?"
   - "What additional data would you want?"
   - "How would you validate your findings?"

---

## Technical Specifications

### SQL Environment
- **Executed in:** DuckDB (for Python integration)
- **Compatible with:** Microsoft SQL Server / T-SQL
- **Style:** Readable, commented, avoid unnecessary complexity
- **Note:** Some syntax adjustments may be needed for SSMS (mainly date conversion)

### Python Environment
- **Version:** Python 3.10
- **Key Libraries:** pandas, numpy, scipy, scikit-learn, matplotlib
- **Style:** Simple, well-commented, focused on correctness over optimization

### Hardware Used
- Standard laptop
- No special requirements

---

## Contact & Questions

For questions about methodology, assumptions, or to discuss findings:
- Be prepared to explain any query or analysis
- Can walk through logic in detail
- Open to feedback and alternative approaches

---

## Acknowledgments

- Used DuckDB for efficient CSV processing
- All analysis and code written from scratch for this assignment
- No external analysis tools or templates used

---

*Submission completed: [Today's Date]*
*Total analysis time: [Estimated hours]*
*Lines of SQL: ~400*
*Lines of Python: ~600*
