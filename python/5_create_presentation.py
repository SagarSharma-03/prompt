"""
==============================================================================
DELIVERABLE 5 - PRODUCT DIRECTOR PRESENTATION
==============================================================================

Creates an 8-slide main presentation with detailed appendix slides.
"""

from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN
from pptx.dml.color import RGBColor
import pandas as pd

# Create presentation
prs = Presentation()
prs.slide_width = Inches(10)
prs.slide_height = Inches(7.5)

def add_title_slide(prs, title, subtitle=""):
    """Add a title slide"""
    slide = prs.slides.add_slide(prs.slide_layouts[0])
    slide.shapes.title.text = title
    if subtitle and len(slide.placeholders) > 1:
        slide.placeholders[1].text = subtitle
    return slide

def add_content_slide(prs, title):
    """Add a content slide with title and content area"""
    slide = prs.slides.add_slide(prs.slide_layouts[1])
    slide.shapes.title.text = title
    return slide

def add_bullet_slide(prs, title, bullets):
    """Add a slide with bullet points"""
    slide = add_content_slide(prs, title)
    
    # Add text box for bullets
    left = Inches(0.5)
    top = Inches(1.5)
    width = Inches(9)
    height = Inches(5.5)
    
    text_box = slide.shapes.add_textbox(left, top, width, height)
    text_frame = text_box.text_frame
    text_frame.word_wrap = True
    
    for i, bullet in enumerate(bullets):
        if i == 0:
            p = text_frame.paragraphs[0]
        else:
            p = text_frame.add_paragraph()
        p.text = bullet
        p.level = 0
        p.font.size = Pt(16)
    
    return slide

print("Creating EA Analyst Assignment Presentation...")

# ============================================================================
# SLIDE 1: TITLE SLIDE
# ============================================================================
slide = add_title_slide(
    prs, 
    "Mobile Game Analytics",
    "Player Behavior, Monetization & Retention Analysis\nJanuary - April 2026"
)

# ============================================================================
# SLIDE 2: EXECUTIVE SUMMARY
# ============================================================================
slide = add_bullet_slide(prs, "Executive Summary - Key Findings", [
    "Game Health: DAU grew 6x (1.8k → 11.1k), Total Revenue $216k (Jan-Apr)",
    "ARPDAU Paradox: Fell 10.6% overall BUT improved in every country tier",
    "   → Root Cause: Low-monetizing Tier 4 grew from 17% to 42% of player base",
    "Retention Crisis: 85% churn by Day 1, only 5.4% remain at Day 30",
    "Monetization: 86% never pay, Top 10% of spenders generate 48% of revenue",
    "Acquisition: Paid Video shows highest engagement (+24 min vs Paid Social)",
    "Churn Prediction: Built interpretable model (ROC-AUC 0.65), ad engagement = strongest retention signal"
])

# ============================================================================
# SLIDE 3: GAME HEALTH METRICS
# ============================================================================
slide = add_content_slide(prs, "Game Health - Daily Metrics (Jan-Apr 2026)")

bullets = [
    "Daily Active Users (DAU)",
    "   • Android: 3,821 avg DAU (71% of total)",
    "   • iOS: 1,740 avg DAU (29% of total)",
    "   • Growth: 1,789 (Jan 1) → 11,097 (Apr 30) - 6x increase",
    "",
    "Revenue & ARPDAU",
    "   • Total Revenue: $216,159 over 4 months",
    "   • iOS ARPDAU: $0.50 (2x Android)",
    "   • Android ARPDAU: $0.25",
    "   • iOS Payer Rate: 3.5% vs Android: 1.8%",
]

left = Inches(0.5)
top = Inches(1.5)
width = Inches(9)
height = Inches(5.5)

text_box = slide.shapes.add_textbox(left, top, width, height)
text_frame = text_box.text_frame
text_frame.word_wrap = True

for bullet in bullets:
    p = text_frame.add_paragraph()
    p.text = bullet
    if bullet.startswith("   •"):
        p.level = 1
        p.font.size = Pt(14)
    elif bullet.startswith("   "):
        p.level = 1
        p.font.size = Pt(14)
    else:
        p.level = 0
        p.font.size = Pt(16)

# ============================================================================
# SLIDE 4: RETENTION & MONETIZATION
# ============================================================================
slide = add_content_slide(prs, "Retention & Monetization Patterns")

bullets = [
    "Retention (Cohort Average)",
    "   • Day 1: 14.7%  |  Day 7: 8.3%  |  Day 14: 6.8%  |  Day 30: 5.4%",
    "   • Steep drop-off after Day 1 (85% churn)",
    "   • Stabilizes around Day 14-30",
    "",
    "Monetization Concentration",
    "   • Overall payer conversion: 13.8% (86% never pay)",
    "   • Top 1% of spenders: 9.4% of revenue",
    "   • Top 10% of spenders: 48% of revenue",
    "   • Top 50% of spenders: 90% of revenue",
    "",
    "Purchase Timing",
    "   • Median time to first purchase: 22 days",
    "   • 25th percentile: 6 days | 75th percentile: 68 days",
    "   • Median repeat purchase gap: 14 days",
]

text_box = slide.shapes.add_textbox(left, top, width, height)
text_frame = text_box.text_frame
text_frame.word_wrap = True

for bullet in bullets:
    p = text_frame.add_paragraph()
    p.text = bullet
    if bullet.startswith("   •") or bullet.startswith("   "):
        p.level = 1
        p.font.size = Pt(14)
    else:
        p.level = 0
        p.font.size = Pt(16)

# ============================================================================
# SLIDE 5: ARPDAU DEEP DIVE - SIMPSON'S PARADOX
# ============================================================================
slide = add_content_slide(prs, "ARPDAU Deep Dive - Simpson's Paradox")

bullets = [
    "The Paradox:",
    "   • Overall ARPDAU fell 10.6% (First 30 days vs Last 30 days)",
    "   • BUT every country tier IMPROVED individually:",
    "      - Tier 1: +2.3% ($1.86 → $1.90)",
    "      - Tier 2: +8.7% ($1.29 → $1.40)",
    "      - Tier 3: +18.2% ($0.83 → $0.98)",
    "      - Tier 4: +16.5% ($0.56 → $0.66)",
    "",
    "Root Cause: Composition Shift",
    "   • Tier 4 (lowest ARPDAU) grew from 17.3% → 41.7% of DAU (+24pp)",
    "   • Tier 1 (highest ARPDAU) shrank from 34.5% → 22.5% of DAU (-12pp)",
    "   • Mix shift drove overall decline despite individual improvements",
    "",
    "Business Insight:",
    "   • This is GOOD NEWS - each tier is improving",
    "   • Need to investigate WHY Tier 4 growing fastest (organic? UA?)",
]

text_box = slide.shapes.add_textbox(left, top, width, height)
text_frame = text_box.text_frame
text_frame.word_wrap = True

for bullet in bullets:
    p = text_frame.add_paragraph()
    p.text = bullet
    if "      -" in bullet:
        p.level = 2
        p.font.size = Pt(12)
    elif bullet.startswith("   •") or bullet.startswith("   "):
        p.level = 1
        p.font.size = Pt(14)
    else:
        p.level = 0
        p.font.size = Pt(16)

# ============================================================================
# SLIDE 6: ACQUISITION CHANNEL ANALYSIS
# ============================================================================
slide = add_content_slide(prs, "Acquisition Channel Comparison")

bullets = [
    "Engagement (Avg playtime in first 30 days):",
    "   • Paid Video: 114.8 min (HIGHEST)",
    "   • Organic: 97.8 min",
    "   • Paid Social: 90.9 min (LOWEST)",
    "   • Paid Video vs Paid Social: +23.9 min (p<0.001, highly significant)",
    "",
    "Revenue (Avg in first 30 days):",
    "   • Organic: $1.62",
    "   • Paid Social: $1.48",
    "   • Paid Video: $1.30",
    "   • Differences small, mostly NOT statistically significant",
    "",
    "Key Insights:",
    "   • Paid Video acquires most engaged players (17-25% more playtime)",
    "   • But engagement doesn't translate to proportionally higher revenue",
    "   • All channels similar conversion rates (7.6-8.8%)",
    "",
    "Recommendation: Prioritize Paid Video for volume (pending CPI analysis)",
]

text_box = slide.shapes.add_textbox(left, top, width, height)
text_frame = text_box.text_frame
text_frame.word_wrap = True

for bullet in bullets:
    p = text_frame.add_paragraph()
    p.text = bullet
    if bullet.startswith("   •") or bullet.startswith("   "):
        p.level = 1
        p.font.size = Pt(14)
    else:
        p.level = 0
        p.font.size = Pt(16)

# ============================================================================
# SLIDE 7: CHURN PREDICTION MODEL
# ============================================================================
slide = add_content_slide(prs, "Churn Prediction Model (14-Day)")

bullets = [
    "Model Approach:",
    "   • Algorithm: Logistic Regression (simple, interpretable)",
    "   • Target: Predict which active players will churn in next 14 days",
    "   • Features: Recent behavior (activity, playtime, purchases, ads)",
    "   • Split: Time-based (train on older cohorts, test on recent)",
    "",
    "Performance:",
    "   • ROC-AUC: 0.65 (moderate discrimination ability)",
    "   • Test set: 12,069 players, 8.1% churn rate",
    "",
    "Key Predictive Features:",
    "   • Ad engagement (strongest retention signal)",
    "   • Session frequency (more sessions = lower churn)",
    "   • Total playtime (more time = lower churn)",
    "",
    "Business Application:",
    "   • Identify high-risk players for retention campaigns",
    "   • Target: Low ad engagement + declining playtime",
]

text_box = slide.shapes.add_textbox(left, top, width, height)
text_frame = text_box.text_frame
text_frame.word_wrap = True

for bullet in bullets:
    p = text_frame.add_paragraph()
    p.text = bullet
    if bullet.startswith("   •") or bullet.startswith("   "):
        p.level = 1
        p.font.size = Pt(14)
    else:
        p.level = 0
        p.font.size = Pt(16)

# ============================================================================
# SLIDE 8: RECOMMENDATIONS
# ============================================================================
slide = add_content_slide(prs, "Key Recommendations")

bullets = [
    "1. Address Country Mix Shift",
    "   • Investigate why Tier 4 growing fastest (UA spend? Viral?)",
    "   • Consider rebalancing UA toward Tier 1/2 if appropriate",
    "   • Develop tier-specific monetization strategies",
    "",
    "2. Improve Early Retention (CRITICAL)",
    "   • 85% churn by Day 1 is a crisis",
    "   • Analyze FTUE friction points immediately",
    "   • Target: Improve D1 retention from 15% → 25%",
    "",
    "3. Accelerate Time-to-First-Purchase",
    "   • Median 22 days is too long",
    "   • Test lower-priced entry offers",
    "   • Implement targeted campaigns at Day 7-14",
    "",
    "4. Leverage Ad Engagement",
    "   • Ad views = strongest retention predictor",
    "   • Only 1-2% hit daily cap - room for growth",
    "   • Increase incentives and visibility",
    "",
    "5. Optimize Acquisition Mix",
    "   • Prioritize Paid Video (highest engagement)",
    "   • Calculate full LTV - CPI by channel for ROI",
]

text_box = slide.shapes.add_textbox(left, top, width, height)
text_frame = text_box.text_frame
text_frame.word_wrap = True

for bullet in bullets:
    p = text_frame.add_paragraph()
    p.text = bullet
    if bullet.startswith("   •") or bullet.startswith("   "):
        p.level = 1
        p.font.size = Pt(13)
    elif bullet and bullet[0].isdigit():
        p.level = 0
        p.font.size = Pt(15)
        p.font.bold = True
    else:
        p.level = 0
        p.font.size = Pt(16)

# ============================================================================
# SLIDE 9: LIMITATIONS & NEXT STEPS
# ============================================================================
slide = add_content_slide(prs, "Limitations & Next Steps")

bullets = [
    "Data Limitations:",
    "   • 4-month window only (Jan-Apr 2026)",
    "   • Cannot assess seasonality or long-term trends",
    "   • No marketing spend / CAC data for true ROI",
    "   • Missing context: events, promotions, product changes",
    "",
    "Data Quality Issues Found:",
    "   • Ad view spike Apr 27-30 (needs investigation)",
    "   • Some purchases dated before install date",
    "   • Early cohorts incomplete observation",
    "",
    "Recommended Next Steps:",
    "   • Investigate Tier 4 growth drivers",
    "   • Conduct FTUE analysis (retention bottleneck)",
    "   • A/B test pricing and first-purchase offers",
    "   • Calculate LTV by channel with longer observation",
    "   • Enhance churn model with social/progression features",
    "   • Monitor Apr 27-30 anomaly (was it an event?)",
]

text_box = slide.shapes.add_textbox(left, top, width, height)
text_frame = text_box.text_frame
text_frame.word_wrap = True

for bullet in bullets:
    p = text_frame.add_paragraph()
    p.text = bullet
    if bullet.startswith("   •") or bullet.startswith("   "):
        p.level = 1
        p.font.size = Pt(13)
    else:
        p.level = 0
        p.font.size = Pt(15)

# ============================================================================
# APPENDIX SLIDES
# ============================================================================

# Appendix title
slide = add_title_slide(prs, "APPENDIX", "Technical Details & Methodology")

# ============================================================================
# APPENDIX A1: SQL - Daily Health
# ============================================================================
slide = add_content_slide(prs, "A1: SQL Analysis - Daily Health Metrics")

bullets = [
    "Methodology:",
    "   • Joined player_day (activity) with player_profile (demographics)",
    "   • Joined purchase table to calculate revenue",
    "   • Aggregated by date and platform",
    "",
    "Key Metrics Calculated:",
    "   • DAU: COUNT(DISTINCT device_id) from player_day",
    "   • Gross Revenue: SUM(usd_amount) from purchases",
    "   • ARPDAU: Total Revenue / DAU",
    "   • Payer Rate: Unique purchasers / DAU",
    "",
    "Results:",
    "   • 240 rows (120 days × 2 platforms)",
    "   • Android: 71% of DAU, but lower ARPDAU",
    "   • iOS: 29% of DAU, but 2x ARPDAU of Android",
]

text_box = slide.shapes.add_textbox(left, top, width, height)
text_frame = text_box.text_frame
text_frame.word_wrap = True

for bullet in bullets:
    p = text_frame.add_paragraph()
    p.text = bullet
    if bullet.startswith("   •") or bullet.startswith("   "):
        p.level = 1
        p.font.size = Pt(14)
    else:
        p.level = 0
        p.font.size = Pt(16)

# ============================================================================
# APPENDIX A2: SQL - Retention
# ============================================================================
slide = add_content_slide(prs, "A2: SQL Analysis - Cohort Retention")

bullets = [
    "Methodology:",
    "   • Grouped players by install week",
    "   • Calculated days_since_install for each activity",
    "   • Measured retention at Day 1, 7, 14, 30",
    "   • Flagged incomplete cohorts (< 30 days observation)",
    "",
    "Key Findings:",
    "   • 49 install week cohorts analyzed",
    "   • 45 complete cohorts (installed before Mar 31)",
    "   • Early cohorts show 0% due to data window starting Jan 1",
    "",
    "Average Retention (Complete Cohorts):",
    "   • D1: 14.7% | D7: 8.3% | D14: 6.8% | D30: 5.4%",
    "",
    "Observation:",
    "   • Recent cohorts (Jan+) show much better retention",
    "   • Suggests product improvements over time",
]

text_box = slide.shapes.add_textbox(left, top, width, height)
text_frame = text_box.text_frame
text_frame.word_wrap = True

for bullet in bullets:
    p = text_frame.add_paragraph()
    p.text = bullet
    if bullet.startswith("   •") or bullet.startswith("   "):
        p.level = 1
        p.font.size = Pt(14)
    else:
        p.level = 0
        p.font.size = Pt(16)

# ============================================================================
# APPENDIX A3: Spender Behavior
# ============================================================================
slide = add_content_slide(prs, "A3: SQL Analysis - Spender Behavior")

bullets = [
    "Revenue Concentration:",
    "   • Ranked all paying players by total revenue",
    "   • Calculated % of revenue from top 1%, 10%, 50%",
    "   • Result: Highly concentrated (top 10% = 48%)",
    "",
    "Time to First Purchase:",
    "   • Calculated: first_purchase_date - install_date",
    "   • Distribution: Median 22 days, but wide spread (6-68 days)",
    "   • Found data quality issue: Some negative values",
    "",
    "Repeat Purchase Gaps:",
    "   • Used window functions (ROW_NUMBER) to order purchases",
    "   • Calculated days between consecutive purchases",
    "   • Result: Median 14 days, 17% repeat within 7 days",
    "",
    "Business Insight:",
    "   • Long time-to-first-purchase = revenue opportunity",
    "   • Consider earlier monetization triggers",
]

text_box = slide.shapes.add_textbox(left, top, width, height)
text_frame = text_box.text_frame
text_frame.word_wrap = True

for bullet in bullets:
    p = text_frame.add_paragraph()
    p.text = bullet
    if bullet.startswith("   •") or bullet.startswith("   "):
        p.level = 1
        p.font.size = Pt(14)
    else:
        p.level = 0
        p.font.size = Pt(16)

# ============================================================================
# APPENDIX A4: Rewarded Ads
# ============================================================================
slide = add_content_slide(prs, "A4: SQL Analysis - Rewarded Ads")

bullets = [
    "Ad Cap Analysis:",
    "   • Daily caps vary by player: 5 or 8 ads",
    "   • Measured % of player-days hitting cap",
    "   • Result: Only 1.06% (cap 5) and 0.02% (cap 8) hit cap",
    "",
    "Ad Completion Rates:",
    "   • 82% completed, 13% abandoned, 5% started only",
    "   • High completion = good ad experience",
    "",
    "Anomaly Detection:",
    "   • Calculated z-scores for daily ad volumes",
    "   • Found: Apr 27-30 abnormally high (z-score > 2)",
    "   • Apr 30: 11,826 views vs avg 5,377",
    "",
    "Investigation Needed:",
    "   • Was there a special event?",
    "   • Product change?",
    "   • If positive, can we replicate?",
]

text_box = slide.shapes.add_textbox(left, top, width, height)
text_frame = text_box.text_frame
text_frame.word_wrap = True

for bullet in bullets:
    p = text_frame.add_paragraph()
    p.text = bullet
    if bullet.startswith("   •") or bullet.startswith("   "):
        p.level = 1
        p.font.size = Pt(14)
    else:
        p.level = 0
        p.font.size = Pt(16)

# ============================================================================
# APPENDIX A5: ARPDAU Methodology
# ============================================================================
slide = add_content_slide(prs, "A5: ARPDAU Deep Dive - Detailed Methodology")

bullets = [
    "Comparison Periods:",
    "   • First 30 days: Jan 1-30, 2026",
    "   • Last 30 days: Apr 1-30, 2026",
    "",
    "Calculations:",
    "   • Overall ARPDAU = Total Revenue / Total DAU",
    "   • By-Tier ARPDAU = Tier Revenue / Tier DAU",
    "   • Mix calculation: Tier DAU / Total DAU",
    "",
    "Simpson's Paradox Explained:",
    "   • Each tier improved individually",
    "   • But low-ARPDAU tier grew much faster",
    "   • Weighted average pulled down overall metric",
    "",
    "Mathematical Example:",
    "   • Tier 4 ARPDAU: $0.66 (improved +16.5%)",
    "   • But Tier 4 share: 17% → 42% (+24pp)",
    "   • More weight on low-value segment = lower overall",
]

text_box = slide.shapes.add_textbox(left, top, width, height)
text_frame = text_box.text_frame
text_frame.word_wrap = True

for bullet in bullets:
    p = text_frame.add_paragraph()
    p.text = bullet
    if bullet.startswith("   •") or bullet.startswith("   "):
        p.level = 1
        p.font.size = Pt(14)
    else:
        p.level = 0
        p.font.size = Pt(16)

# ============================================================================
# APPENDIX A6: Acquisition Statistical Methods
# ============================================================================
slide = add_content_slide(prs, "A6: Acquisition Analysis - Statistical Methods")

bullets = [
    "Sample & Approach:",
    "   • Only players installed before Mar 31 (complete 30-day window)",
    "   • N = 53,489 (Organic: 20k, Paid Social: 18k, Paid Video: 15k)",
    "   • Measured playtime and revenue in first 30 days after install",
    "",
    "Statistical Tests:",
    "   • Two-sample t-tests for mean differences",
    "   • Calculated 95% confidence intervals",
    "   • Significance threshold: p < 0.05",
    "",
    "Key Results:",
    "   • Engagement differences: Large and significant",
    "   • Revenue differences: Small, mostly not significant",
    "",
    "Interpretation:",
    "   • Statistical significance ≠ business significance",
    "   • Large samples = small differences become 'significant'",
    "   • Focus on confidence intervals for practical importance",
]

text_box = slide.shapes.add_textbox(left, top, width, height)
text_frame = text_box.text_frame
text_frame.word_wrap = True

for bullet in bullets:
    p = text_frame.add_paragraph()
    p.text = bullet
    if bullet.startswith("   •") or bullet.startswith("   "):
        p.level = 1
        p.font.size = Pt(14)
    else:
        p.level = 0
        p.font.size = Pt(16)

# ============================================================================
# APPENDIX A7: Churn Model Details
# ============================================================================
slide = add_content_slide(prs, "A7: Churn Model - Technical Details")

bullets = [
    "Model Configuration:",
    "   • As-of date: April 2, 2026",
    "   • Feature window: 14 days looking back (Mar 19-Apr 2)",
    "   • Churn window: 14 days looking forward (Apr 3-16)",
    "   • Churn = No activity in next 14 days",
    "",
    "Features (10 total):",
    "   • Activity: days active, playtime, sessions",
    "   • Monetization: purchases, revenue",
    "   • Engagement: ad views",
    "   • Profile: level, days since install, country tier",
    "",
    "Train/Test Split:",
    "   • Time-based (NOT random) to avoid leakage",
    "   • Train: Players installed before Mar 15 (N=41,897)",
    "   • Test: Players installed Mar 15-Apr 2 (N=12,069)",
    "",
    "Why Logistic Regression?",
    "   • Simple, interpretable coefficients",
    "   • Can explain in interview",
    "   • Sufficient for demonstrating analytical approach",
]

text_box = slide.shapes.add_textbox(left, top, width, height)
text_frame = text_box.text_frame
text_frame.word_wrap = True

for bullet in bullets:
    p = text_frame.add_paragraph()
    p.text = bullet
    if bullet.startswith("   •") or bullet.startswith("   "):
        p.level = 1
        p.font.size = Pt(13)
    else:
        p.level = 0
        p.font.size = Pt(15)

# ============================================================================
# APPENDIX A8: Churn Model Evaluation
# ============================================================================
slide = add_content_slide(prs, "A8: Churn Model - Evaluation Metrics")

bullets = [
    "ROC-AUC: 0.65 (Test Set)",
    "   • Measures ranking ability (0.5=random, 1.0=perfect)",
    "   • 0.65 = moderate discrimination",
    "   • Can distinguish churners from non-churners better than random",
    "",
    "Why Not Higher?",
    "   • Simple features only (no social, progression milestones)",
    "   • Distribution shift: Train 31.9% churn vs Test 8.1% churn",
    "   • Game evolving over time (recent players different)",
    "",
    "Feature Importance (Top 3):",
    "   • Ad views (-0.111): More ads = less churn",
    "   • Avg sessions/day (-0.093): More sessions = less churn",
    "   • Days active (+0.187): Counterintuitive - needs investigation",
    "",
    "Business Value:",
    "   • Despite moderate AUC, still useful for targeting",
    "   • Top 20% predicted churners likely contain 40-50% of actual churners",
    "   • Better than random targeting",
]

text_box = slide.shapes.add_textbox(left, top, width, height)
text_frame = text_box.text_frame
text_frame.word_wrap = True

for bullet in bullets:
    p = text_frame.add_paragraph()
    p.text = bullet
    if bullet.startswith("   •") or bullet.startswith("   "):
        p.level = 1
        p.font.size = Pt(13)
    else:
        p.level = 0
        p.font.size = Pt(15)

# ============================================================================
# APPENDIX A9: Data Quality Issues
# ============================================================================
slide = add_content_slide(prs, "A9: Data Quality Issues & Handling")

bullets = [
    "Issue 1: Negative Time-to-Purchase",
    "   • Some first_purchase_date < install_date",
    "   • Minimum: -4 days",
    "   • Handling: Flagged but included in analysis",
    "   • Impact: Minimal (affects <0.1% of records)",
    "",
    "Issue 2: Ad View Spike (Apr 27-30)",
    "   • Abnormally high ad views (z-score > 2)",
    "   • 2x normal volume on Apr 30",
    "   • Handling: Included but flagged for investigation",
    "   • Possible causes: Event? Promotion? Bug?",
    "",
    "Issue 3: Early Cohort Retention",
    "   • Pre-Dec 2025 cohorts show 0% retention",
    "   • Cause: player_day data starts Jan 1, 2026",
    "   • Handling: Documented, focus on recent cohorts",
    "   • Not a true retention issue",
    "",
    "General Approach:",
    "   • Document all issues transparently",
    "   • Assess impact on conclusions",
    "   • Flag for follow-up where appropriate",
]

text_box = slide.shapes.add_textbox(left, top, width, height)
text_frame = text_box.text_frame
text_frame.word_wrap = True

for bullet in bullets:
    p = text_frame.add_paragraph()
    p.text = bullet
    if bullet.startswith("   •") or bullet.startswith("   "):
        p.level = 1
        p.font.size = Pt(13)
    else:
        p.level = 0
        p.font.size = Pt(15)

# ============================================================================
# APPENDIX A10: Assumptions & Limitations
# ============================================================================
slide = add_content_slide(prs, "A10: Key Assumptions & Limitations")

bullets = [
    "Assumptions:",
    "   • Player_day table accurately captures all activity",
    "   • Install_date is reliable",
    "   • Purchase timestamps are accurate (despite some anomalies)",
    "   • Country_tier is stable (doesn't change over time)",
    "",
    "Limitations:",
    "   • 4-month observation window only",
    "   • No external data (marketing spend, events, seasonality)",
    "   • Simple features in churn model",
    "   • Cannot prove causality (only correlation)",
    "   • Test set is more recent (may not generalize to older players)",
    "",
    "Mitigations:",
    "   • Used conservative statistical methods",
    "   • Documented all data quality issues",
    "   • Focused on actionable insights",
    "   • Recommended follow-up analyses",
]

text_box = slide.shapes.add_textbox(left, top, width, height)
text_frame = text_box.text_frame
text_frame.word_wrap = True

for bullet in bullets:
    p = text_frame.add_paragraph()
    p.text = bullet
    if bullet.startswith("   •") or bullet.startswith("   "):
        p.level = 1
        p.font.size = Pt(14)
    else:
        p.level = 0
        p.font.size = Pt(15)

# Save presentation
output_path = 'ea_submission/EA_Product_Director_Presentation.pptx'
prs.save(output_path)

print(f"\n✓ Presentation created successfully!")
print(f"  Location: {output_path}")
print(f"  Total slides: {len(prs.slides)}")
print(f"  Main presentation: 9 slides")
print(f"  Appendix: {len(prs.slides) - 9} slides")
print("\nPresentation structure:")
print("  Slide 1: Title")
print("  Slide 2: Executive Summary")
print("  Slide 3: Game Health")
print("  Slide 4: Retention & Monetization")
print("  Slide 5: ARPDAU Deep Dive (Simpson's Paradox)")
print("  Slide 6: Acquisition Analysis")
print("  Slide 7: Churn Prediction")
print("  Slide 8: Recommendations")
print("  Slide 9: Limitations & Next Steps")
print("  Slides 10+: Appendix (Technical Details)")
