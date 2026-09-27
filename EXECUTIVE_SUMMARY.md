# EA Analyst Assignment - Executive Summary

## Overview
This document summarizes the key findings from the mobile game analytics assignment analyzing player behavior, monetization, and retention patterns from January-April 2026.

---

## KEY FINDINGS

### 1. GAME HEALTH METRICS (Deliverable 1a)

**Daily Active Users (DAU):**
- Android: ~3,821 average DAU (71% of total)
- iOS: ~1,740 average DAU (29% of total)
- Growth trend: DAU increased from ~1,789 on Jan 1 to ~11,097 on Apr 30

**Revenue & ARPDAU:**
- Total Revenue (Jan-Apr): $216,159
- Overall ARPDAU: $0.254 (Android) vs $0.499 (iOS)
- iOS players monetize at nearly 2x the rate of Android
- iOS payer rate: 3.48% vs Android: 1.76%

---

### 2. RETENTION (Deliverable 1b)

**Cohort Retention Rates (Complete cohorts avg):**
- Day 1: 14.7%
- Day 7: 8.3%
- Day 14: 6.8%
- Day 30: 5.4%

**Key Observations:**
- Steep drop-off after Day 1
- Retention stabilizes around Day 14-30
- Recent cohorts (post-Dec 2025) show much higher retention than early cohorts
- Early cohorts (pre-Dec 2025) show 0% retention due to observation window limitations

---

### 3. MONETIZATION & SPENDER BEHAVIOR (Deliverable 1c)

**Revenue Concentration:**
- Top 1% of spenders: 9.4% of revenue
- Top 10% of spenders: 48.1% of revenue
- Top 50% of spenders: 90.2% of revenue

**Payer Conversion:**
- Overall payer rate: 13.8%
- Non-payers: 86.2%

**Time to First Purchase:**
- Median: 22 days after install
- 25th percentile: 6 days
- 75th percentile: 68 days
- Same-day purchasers: 5.8%

**Repeat Purchase Behavior:**
- Median time between purchases: 14 days
- 4,372 repeat purchases observed
- 17% of purchases occur within 7 days of previous purchase

**DATA QUALITY ISSUE:**
- Found negative days to first purchase (-4 days minimum)
- Indicates data inconsistency (purchase_date before install_date)

---

### 4. REWARDED ADS (Deliverable 1d)

**Ad Cap Hit Rates:**
- Cap 5: 1.06% of player-days hit cap
- Cap 8: 0.02% of player-days hit cap
- Most players don't reach daily ad limits

**Ad Completion:**
- 82.0% completed
- 13.0% abandoned
- 5.0% started but not completed

**ANOMALY DETECTED:**
- Last 4 days of April (27-30) show abnormally high ad views (z-score > 2)
- Apr 30: 11,826 ad views vs avg 5,377
- Could indicate:
  - Special event/promotion
  - Data quality issue
  - Seasonal effect
  - Product change

---

### 5. ARPDAU DEEP DIVE - SIMPSON'S PARADOX (Deliverable 2a)

**The Paradox:**
- Overall ARPDAU FELL 10.6% (Jan vs Apr)
- BUT every country tier IMPROVED individually:
  - Tier 1: +2.3% ($1.86 → $1.90)
  - Tier 2: +8.7% ($1.29 → $1.40)
  - Tier 3: +18.2% ($0.83 → $0.98)
  - Tier 4: +16.5% ($0.56 → $0.66)

**Root Cause: Composition Shift**
| Country Tier | ARPDAU | Jan DAU Share | Apr DAU Share | Change |
|--------------|--------|---------------|---------------|---------|
| Tier 1 (High) | $1.90 | 34.5% | 22.5% | **-12.0pp** |
| Tier 2 | $1.40 | 26.3% | 17.1% | **-9.2pp** |
| Tier 3 | $0.98 | 21.9% | 18.6% | **-3.3pp** |
| Tier 4 (Low) | $0.66 | 17.3% | 41.7% | **+24.4pp** |

**Explanation:**
- Tier 4 (lowest ARPDAU) grew from 17% to 42% of player base
- High-value tiers (1 & 2) shrunk from 61% to 40% of player base
- This mix shift drove overall ARPDAU down despite individual improvements

---

### 6. ACQUISITION CHANNEL ANALYSIS (Deliverable 3)

**Sample Sizes (Complete 30-day observation):**
- Organic: 20,159 players
- Paid Social: 17,857 players
- Paid Video: 15,473 players

**Engagement (Avg playtime in first 30 days):**
| Channel | Playtime | vs Organic | vs Paid Social |
|---------|----------|------------|----------------|
| Organic | 97.8 min | - | +6.8 min*** |
| Paid Social | 90.9 min | -6.8 min*** | - |
| Paid Video | 114.8 min | +17.1 min*** | +23.9 min*** |

**Revenue (Avg revenue in first 30 days):**
| Channel | Revenue | vs Organic | vs Paid Social |
|---------|---------|------------|----------------|
| Organic | $1.62 | - | +$0.14 (ns) |
| Paid Social | $1.48 | -$0.14 (ns) | - |
| Paid Video | $1.30 | +$0.32** | +$0.18 (ns) |

**Statistical Significance:**
- ***: p < 0.001 (highly significant)
- **: p < 0.01 (significant)
- ns: not significant (p > 0.05)

**Key Insights:**
1. **Paid Video** shows HIGHEST engagement (+17-24 min vs others)
   - Statistically significant
   - Business significant: 17-25% more playtime

2. **Revenue differences are SMALL and mostly NOT statistically significant**
   - Organic vs Paid Social: $0.14 difference (NS)
   - Organic vs Paid Video: $0.32 difference (significant but small)
   - Paid Social vs Paid Video: $0.18 difference (NS)

3. **Interpretation:**
   - Paid Video acquires more engaged players (higher playtime)
   - But engagement doesn't translate to proportionally higher revenue
   - All channels have similar conversion rates (8-9%)

**Business Recommendation:**
- Paid Video appears to be the highest quality channel (engagement)
- Revenue differences are too small to be actionable
- Consider: Cost per install + LTV analysis needed for true ROI assessment

---

### 7. CHURN PREDICTION MODEL (Deliverable 4)

**Model Configuration:**
- Algorithm: Logistic Regression (simple, interpretable)
- Prediction target: 14-day churn
- As-of date: April 2, 2026
- Features: 10 behavioral features from previous 14 days

**Performance (Test Set):**
- ROC-AUC: 0.651 (moderate discrimination)
- Accuracy: 91.9%
- Note: High accuracy driven by class imbalance (91.9% non-churners)

**Most Important Features (Coefficients):**

*Increases Churn Risk (Positive):*
1. **days_active_last_14d** (+0.187): More active days = higher churn risk (counterintuitive - may indicate data issue or spurious correlation)
2. **made_purchase_last_14d** (+0.053): Recent purchasers more likely to churn (concerning - needs investigation)

*Decreases Churn Risk (Negative):*
1. **ad_views_last_14d** (-0.111): More ad views = lower churn
2. **avg_sessions_per_day** (-0.093): More sessions = lower churn
3. **total_playtime_last_14d** (-0.013): More playtime = lower churn

**Interpretation:**
- Ad engagement is strongest retention signal
- High session frequency indicates stickiness
- Counterintuitive results (recent purchase increases churn risk) may indicate:
  - One-time purchasers who leave after buying
  - Need for post-purchase engagement strategies

**Business Application:**
- Identify high-risk players for targeted retention campaigns
- Focus on players with:
  - Low ad engagement
  - Low session frequency
  - Declining playtime

**Model Limitations:**
- Moderate predictive power (ROC-AUC 0.65)
- Time-based split shows distribution shift (train: 31.9% churn vs test: 8.1% churn)
- Simple features only - could be enhanced with:
  - Social features
  - Progression milestones
  - Event participation
  - Historical patterns

---

## CRITICAL DATA QUALITY ISSUES

1. **Negative Time-to-Purchase:**
   - Some first_purchase_date < install_date
   - Affects time-to-purchase calculations

2. **Ad View Anomaly (Late April):**
   - Spike in ad views Apr 27-30
   - Needs investigation

3. **Early Cohort Retention:**
   - Pre-December 2025 cohorts show 0% retention
   - Due to observation window starting Jan 2026
   - Not a true retention issue

4. **Churn Model Performance:**
   - Significant distribution shift between train/test sets
   - May indicate game evolution or cohort effects

---

## TOP BUSINESS RECOMMENDATIONS

### IMMEDIATE ACTIONS:

1. **Address Country Mix Shift:**
   - **Problem:** Tier 4 countries growing fastest, dragging down ARPDAU despite individual improvements
   - **Actions:**
     - Investigate WHY Tier 4 is growing faster (UA spend? Organic growth? Viral mechanics?)
     - If intentional: Celebrate per-tier ARPDAU improvements
     - If unintentional: Rebalance UA spend toward Tier 1/2 countries
     - Consider: Tier-specific product features or pricing

2. **Optimize Acquisition Channel Mix:**
   - **Problem:** Paid Video shows highest engagement but not proportionally higher revenue
   - **Actions:**
     - Prioritize Paid Video for volume (if CPI is reasonable)
     - Calculate true ROI: (30-day LTV - CPI) by channel
     - Investigate why high engagement doesn't convert to revenue
     - Test: Onboarding flows optimized by channel

3. **Improve Early Retention:**
   - **Problem:** 85% of players churn by Day 1
   - **Actions:**
     - Analyze FTUE (First Time User Experience) friction points
     - A/B test onboarding improvements
     - Implement early retention hooks (rewards, social features)
     - Target: Improve D1 retention from 15% to 25%+

4. **Monetization Optimization:**
   - **Problem:** 86% of players never pay
   - **Actions:**
     - Test pricing strategies (lower entry price point?)
     - Improve conversion from free to paid
     - Target first purchase timing (median 22 days - can we accelerate?)
     - Implement "first purchase incentive" campaigns at Day 7-14

5. **Ad Engagement Strategy:**
   - **Problem:** Only 1-2% hit daily ad cap
   - **Actions:**
     - Increase ad cap visibility/incentivization
     - Test higher-value rewards for ad viewing
     - Ad views strongly correlated with retention - lean into this

### FURTHER INVESTIGATION NEEDED:

1. **Apr 27-30 Ad Spike:**
   - Was this an event? Bug? Promotion?
   - Can we replicate the engagement?

2. **Purchase→Churn Pattern:**
   - Why do recent purchasers show higher churn risk?
   - Are they "buying their way out" of progression walls?
   - Post-purchase experience needs improvement

3. **Country Tier Growth Drivers:**
   - Is Tier 4 growth organic or paid?
   - Can we maintain growth while improving monetization?

4. **Revenue Concentration:**
   - Top 10% generate 48% of revenue
   - How do we identify and nurture whales?
   - Retention strategies for high-value players

---

## NEXT STEPS FOR INTERVIEW PREPARATION

### Concepts to Learn:

1. **Statistics:**
   - Confidence intervals
   - p-values and statistical significance
   - Type I and Type II errors
   - Simpson's Paradox

2. **Machine Learning:**
   - What logistic regression does (log-odds, sigmoid function)
   - Train/test split rationale
   - Overfitting vs underfitting
   - Evaluation metrics: Accuracy, Precision, Recall, ROC-AUC
   - Confusion matrix interpretation

3. **SQL:**
   - Review all queries in `ea_submission/sql/`
   - Be able to explain JOIN logic
   - Window functions (ROW_NUMBER, RANK)
   - Aggregation vs filtering

4. **Business Metrics:**
   - DAU, MAU, retention curves
   - ARPDAU vs ARPPU vs LTV
   - Cohort analysis
   - Funnel analysis

### Potential Interview Questions:

1. "Walk me through your ARPDAU analysis. Why did overall ARPDAU fall?"
2. "How would you decide which acquisition channel to invest in?"
3. "Explain your churn model. Why did you choose those features?"
4. "What's the difference between statistical and business significance?"
5. "What data quality issues did you find? How did you handle them?"
6. "If you had more time, what would you analyze next?"
7. "How would you validate your churn model in production?"
8. "Why use a time-based train/test split instead of random?"

---

## FILES DELIVERED

### SQL Queries:
- `1a_daily_health.sql` - DAU, revenue, ARPDAU by day and platform
- `1b_retention.sql` - Cohort retention analysis
- `1c_spender_behaviour.sql` - Revenue concentration, time-to-purchase, repeat purchase patterns
- `1d_rewarded_ads.sql` - Ad cap analysis, daily ad views, anomaly detection
- `2a_arpdau_deep_dive.sql` - Simpson's Paradox investigation

### Python Scripts:
- `3_acquisition_analysis.py` - Channel comparison with statistical tests
- `4_churn_prediction.py` - Logistic regression churn model

### Results:
- All analysis results saved to `ea_submission/results/`
- Includes CSVs, charts, and model outputs

---

## METHODOLOGY DECISIONS

### Why These Choices?

1. **Simple Logistic Regression (not XGBoost/Random Forest):**
   - Interpretable coefficients
   - Can explain in interview
   - Sufficient for demonstrating analytical thinking
   - Assignment explicitly preferred interpretability

2. **Time-Based Train/Test Split:**
   - Avoids data leakage
   - Realistic: predict future behavior from past data
   - More robust than random split for time-series data

3. **30-Day Observation Windows:**
   - Balances data completeness with sample size
   - Aligns with industry standards
   - Avoids incomplete cohorts biasing results

4. **T-Tests for Acquisition Analysis:**
   - Simple, interpretable
   - Appropriate for continuous metrics (playtime, revenue)
   - Provides confidence intervals for business decisions

5. **SQL-First Approach:**
   - Follows assignment priority
   - Readable queries for someone learning SQL
   - Compatible with Microsoft SQL Server syntax where possible

---

*Analysis completed: [Today's Date]*
*Analyst: Mathematics Student Candidate*
*Dataset: EA Mobile Game Analytics (Jan-Apr 2026)*
