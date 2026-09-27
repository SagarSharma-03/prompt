"""
==============================================================================
DELIVERABLE 5 - PRODUCT DIRECTOR PRESENTATION (EXACTLY 8 SLIDES)
==============================================================================

Creates exactly 8 slides - NO appendix, as requested.
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

print("Creating EA Analyst Assignment Presentation (EXACTLY 8 SLIDES)...")

left = Inches(0.5)
top = Inches(1.5)
width = Inches(9)
height = Inches(5.5)

# ============================================================================
# SLIDE 1: EXECUTIVE SUMMARY
# ============================================================================
slide = add_content_slide(prs, "Executive Summary - Key Findings")

bullets = [
    "Game Growth: DAU grew 6x (1.8k → 11.1k), Revenue $216k (Jan-Apr)",
    "",
    "ARPDAU Paradox: Fell 10.6% overall BUT improved in every country tier",
    "   • Root Cause: Low-monetizing Tier 4 grew from 17% to 42% of player base",
    "   • This is Simpson's Paradox - composition shift driving overall decline",
    "",
    "Retention Crisis: 85% churn by Day 1, only 5.4% remain at Day 30",
    "",
    "Monetization: 86% never pay | Top 10% of spenders = 48% of revenue",
    "",
    "Acquisition: Paid Video shows +24 min engagement vs Paid Social (p<0.001)",
    "",
    "Churn Model: Built interpretable logistic regression (ROC-AUC 0.65)",
    "   • Ad engagement is the strongest retention signal",
]

text_box = slide.shapes.add_textbox(left, top, width, height)
text_frame = text_box.text_frame
text_frame.word_wrap = True

for bullet in bullets:
    p = text_frame.add_paragraph()
    p.text = bullet
    if bullet.startswith("   •"):
        p.level = 1
        p.font.size = Pt(14)
    else:
        p.level = 0
        p.font.size = Pt(16)

# ============================================================================
# SLIDE 2: GAME HEALTH OVERVIEW
# ============================================================================
slide = add_content_slide(prs, "Game Health - Strong Growth, Platform Differences")

bullets = [
    "Daily Active Users (DAU) - 6x Growth",
    "   • Android: 3,821 avg DAU (71% of total)",
    "   • iOS: 1,740 avg DAU (29% of total)",
    "   • Jan 1: 1,789 → Apr 30: 11,097",
    "",
    "Revenue & Monetization by Platform",
    "   • Total Revenue (Jan-Apr): $216,159",
    "   • iOS monetizes 2x better: ARPDAU $0.50 vs Android $0.25",
    "   • iOS Payer Rate: 3.5% | Android: 1.8%",
    "",
    "Retention (Cohort Average)",
    "   • Day 1: 14.7% | Day 7: 8.3% | Day 14: 6.8% | Day 30: 5.4%",
    "   • 85% of players churn by Day 1 - CRITICAL ISSUE",
]

text_box = slide.shapes.add_textbox(left, top, width, height)
text_frame = text_box.text_frame
text_frame.word_wrap = True

for bullet in bullets:
    p = text_frame.add_paragraph()
    p.text = bullet
    if bullet.startswith("   •"):
        p.level = 1
        p.font.size = Pt(14)
    else:
        p.level = 0
        p.font.size = Pt(16)
        p.font.bold = True

# ============================================================================
# SLIDE 3: MONETIZATION DEEP DIVE
# ============================================================================
slide = add_content_slide(prs, "Monetization - Highly Concentrated, Long Purchase Cycle")

bullets = [
    "Revenue Concentration",
    "   • Top 1% of spenders: 9.4% of revenue",
    "   • Top 10% of spenders: 48% of revenue",
    "   • Top 50% of spenders: 90% of revenue",
    "   • Overall: 13.8% of players ever pay (86% never monetize)",
    "",
    "Time to First Purchase - Slow Conversion",
    "   • Median: 22 days after install",
    "   • 25th percentile: 6 days | 75th percentile: 68 days",
    "   • Only 5.8% purchase on Day 0",
    "",
    "Repeat Purchase Behavior",
    "   • Median gap between purchases: 14 days",
    "   • 17% repeat within 7 days (fast repeaters)",
    "",
    "Insight: Long time-to-first-purchase = missed revenue opportunity",
]

text_box = slide.shapes.add_textbox(left, top, width, height)
text_frame = text_box.text_frame
text_frame.word_wrap = True

for bullet in bullets:
    p = text_frame.add_paragraph()
    p.text = bullet
    if bullet.startswith("   •"):
        p.level = 1
        p.font.size = Pt(14)
    else:
        p.level = 0
        p.font.size = Pt(16)
        p.font.bold = True

# ============================================================================
# SLIDE 4: ARPDAU PARADOX - SIMPSON'S PARADOX
# ============================================================================
slide = add_content_slide(prs, "ARPDAU Deep Dive - Simpson's Paradox Discovered")

bullets = [
    "The Paradox:",
    "   • Overall ARPDAU fell 10.6% (First 30 days vs Last 30 days)",
    "   • BUT every country tier IMPROVED:",
    "      Tier 1: +2.3% | Tier 2: +8.7% | Tier 3: +18.2% | Tier 4: +16.5%",
    "",
    "Root Cause: Composition Shift",
    "   • Tier 4 (lowest ARPDAU $0.66) grew from 17% → 42% of DAU (+24pp)",
    "   • Tier 1 (highest ARPDAU $1.90) fell from 35% → 23% of DAU (-12pp)",
    "   • Mix shift overwhelmed individual tier improvements",
    "",
    "Why This Matters:",
    "   • Each tier IS improving (positive signal)",
    "   • But player composition shifting toward low-value countries",
    "   • Need to understand: Why is Tier 4 growing fastest?",
    "",
    "Recommendations:",
    "   • Investigate Tier 4 growth drivers (organic? UA spend?)",
    "   • Consider rebalancing UA toward higher-value tiers",
    "   • Develop tier-specific monetization strategies",
]

text_box = slide.shapes.add_textbox(left, top, width, height)
text_frame = text_box.text_frame
text_frame.word_wrap = True

for bullet in bullets:
    p = text_frame.add_paragraph()
    p.text = bullet
    if "Tier 1:" in bullet or "Tier 2:" in bullet:
        p.level = 2
        p.font.size = Pt(13)
    elif bullet.startswith("   •"):
        p.level = 1
        p.font.size = Pt(14)
    else:
        p.level = 0
        p.font.size = Pt(16)
        p.font.bold = True

# ============================================================================
# SLIDE 5: ACQUISITION CHANNEL ANALYSIS
# ============================================================================
slide = add_content_slide(prs, "Acquisition - Paid Video Wins on Engagement")

bullets = [
    "Sample: 53,489 players with complete 30-day observation",
    "",
    "Engagement (Avg playtime in first 30 days):",
    "   • Paid Video: 114.8 min (HIGHEST)",
    "   • Organic: 97.8 min",
    "   • Paid Social: 90.9 min (LOWEST)",
    "   • Paid Video vs Paid Social: +23.9 min (p<0.001, highly significant)",
    "",
    "Revenue (Avg in first 30 days):",
    "   • Organic: $1.62 | Paid Social: $1.48 | Paid Video: $1.30",
    "   • Differences small, mostly NOT statistically significant",
    "   • Conversion rates similar across channels (7.6-8.8%)",
    "",
    "Key Insights:",
    "   • Paid Video acquires most engaged players (17-25% more playtime)",
    "   • Higher engagement doesn't translate to proportionally higher revenue",
    "   • Statistical significance ≠ business significance",
    "",
    "Recommendation: Prioritize Paid Video (pending full LTV - CPI analysis)",
]

text_box = slide.shapes.add_textbox(left, top, width, height)
text_frame = text_box.text_frame
text_frame.word_wrap = True

for bullet in bullets:
    p = text_frame.add_paragraph()
    p.text = bullet
    if bullet.startswith("   •"):
        p.level = 1
        p.font.size = Pt(13)
    else:
        p.level = 0
        p.font.size = Pt(15)
        if ":" in bullet and bullet.index(":") < 40:
            p.font.bold = True

# ============================================================================
# SLIDE 6: CHURN PREDICTION MODEL
# ============================================================================
slide = add_content_slide(prs, "Churn Prediction - Interpretable Model Built")

bullets = [
    "Objective: Predict which active players will churn in next 14 days",
    "",
    "Approach:",
    "   • Algorithm: Logistic Regression (simple, interpretable)",
    "   • Features: Recent behavior (activity, playtime, purchases, ads)",
    "   • Train/Test: Time-based split (no data leakage)",
    "   • As-of date: Apr 2, 2026",
    "",
    "Performance:",
    "   • ROC-AUC: 0.65 (moderate discrimination)",
    "   • Better than random targeting",
    "   • Test set: 12,069 players, 8.1% churn rate",
    "",
    "Top Predictive Features:",
    "   • Ad engagement: Strongest retention signal (-0.111)",
    "   • Session frequency: More sessions = lower churn (-0.093)",
    "   • Total playtime: More time = lower churn (-0.013)",
    "",
    "Business Use: Identify high-risk players for retention campaigns",
    "   • Target: Low ad engagement + declining playtime",
]

text_box = slide.shapes.add_textbox(left, top, width, height)
text_frame = text_box.text_frame
text_frame.word_wrap = True

for bullet in bullets:
    p = text_frame.add_paragraph()
    p.text = bullet
    if bullet.startswith("   •"):
        p.level = 1
        p.font.size = Pt(14)
    else:
        p.level = 0
        p.font.size = Pt(15)
        if ":" in bullet and bullet.index(":") < 40:
            p.font.bold = True

# ============================================================================
# SLIDE 7: KEY RECOMMENDATIONS (PRIORITIZED)
# ============================================================================
slide = add_content_slide(prs, "Recommendations - 5 Priority Actions")

bullets = [
    "1. Fix Early Retention (MOST CRITICAL)",
    "   • 85% Day 1 churn is a crisis - analyze FTUE immediately",
    "   • Target: Improve D1 retention from 15% → 25%",
    "   • A/B test onboarding improvements, reduce early friction",
    "",
    "2. Address Country Mix Shift",
    "   • Investigate why Tier 4 growing fastest",
    "   • Rebalance UA spend toward higher-value tiers if appropriate",
    "   • Develop tier-specific features and pricing",
    "",
    "3. Accelerate Time-to-First-Purchase",
    "   • Median 22 days is too long",
    "   • Test lower-priced entry offers ($0.99 starter pack?)",
    "   • Implement targeted campaigns at Day 7-14",
    "",
    "4. Leverage Ad Engagement for Retention",
    "   • Ad views = strongest churn predictor",
    "   • Only 1% hit daily cap - huge growth opportunity",
    "   • Increase visibility, rewards, and incentives",
    "",
    "5. Optimize Acquisition Mix",
    "   • Prioritize Paid Video (highest engagement)",
    "   • Calculate full ROI: (30-day LTV - CPI) by channel",
]

text_box = slide.shapes.add_textbox(left, top, width, height)
text_frame = text_box.text_frame
text_frame.word_wrap = True

for bullet in bullets:
    p = text_frame.add_paragraph()
    p.text = bullet
    if bullet.startswith("   •"):
        p.level = 1
        p.font.size = Pt(13)
    elif bullet and bullet[0].isdigit():
        p.level = 0
        p.font.size = Pt(15)
        p.font.bold = True
    else:
        p.level = 0
        p.font.size = Pt(15)

# ============================================================================
# SLIDE 8: LIMITATIONS & NEXT STEPS
# ============================================================================
slide = add_content_slide(prs, "Limitations & Next Steps")

bullets = [
    "Data Limitations:",
    "   • 4-month observation window only (Jan-Apr 2026)",
    "   • No marketing spend / CAC data for true ROI calculation",
    "   • Missing context: events, promotions, product changes",
    "   • Cannot assess seasonality or long-term trends",
    "",
    "Data Quality Issues Found & Handled:",
    "   • Ad view spike Apr 27-30 (flagged for investigation)",
    "   • Some purchase dates before install dates (documented)",
    "   • Early cohorts have incomplete observation (explained)",
    "",
    "Recommended Next Steps:",
    "   • URGENT: Conduct FTUE analysis (retention bottleneck)",
    "   • Investigate Tier 4 growth drivers and strategic fit",
    "   • A/B test first-purchase pricing and timing",
    "   • Calculate 90-day LTV by channel for full ROI picture",
    "   • Enhance churn model with social/progression features",
    "   • Run cohort-stratified analyses (are recent cohorts different?)",
]

text_box = slide.shapes.add_textbox(left, top, width, height)
text_frame = text_box.text_frame
text_frame.word_wrap = True

for bullet in bullets:
    p = text_frame.add_paragraph()
    p.text = bullet
    if bullet.startswith("   •"):
        p.level = 1
        p.font.size = Pt(13)
    else:
        p.level = 0
        p.font.size = Pt(15)
        p.font.bold = True

# Save presentation
output_path = 'ea_submission/EA_Product_Director_Presentation.pptx'
prs.save(output_path)

print(f"\n✓ Presentation created successfully!")
print(f"  Location: {output_path}")
print(f"  Total slides: {len(prs.slides)}")
print(f"\nPresentation Structure (EXACTLY 8 SLIDES):")
print("  Slide 1: Executive Summary")
print("  Slide 2: Game Health Overview")
print("  Slide 3: Monetization Deep Dive")
print("  Slide 4: ARPDAU Paradox (Simpson's Paradox)")
print("  Slide 5: Acquisition Channel Analysis")
print("  Slide 6: Churn Prediction Model")
print("  Slide 7: Key Recommendations (Prioritized)")
print("  Slide 8: Limitations & Next Steps")
print("\n✓ NO appendix slides - exactly 8 slides as requested!")
