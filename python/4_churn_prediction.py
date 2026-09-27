"""
==============================================================================
DELIVERABLE 4 - CHURN PREDICTION MODEL
==============================================================================

PURPOSE:
Build a simple logistic regression model to predict which currently active 
players will churn (stop playing) in the next 14 days.

CHURN DEFINITION:
A player "churns" if they do not have any activity in the 14 days following
the observation date.

AS-OF DATE:
We'll use April 2, 2026 as the "as of" date, which gives us:
- Enough historical data to build features
- 14 days of future data to observe churn (through April 16, 2026)
- Remaining data (April 17-30) can be used for additional validation if needed

POPULATION:
- Players who were active on or before April 2, 2026
- Exclude players who installed after April 2 (too new to predict)

FEATURES:
Simple, interpretable features based on recent behavior (last 14 days before as-of date):
- days_active_last_14d: Number of days player was active
- total_playtime_last_14d: Total playtime minutes
- avg_session_count: Average sessions per active day
- player_level: Current player level
- days_since_install: Days since player installed
- made_purchase_last_14d: Binary flag if player made purchase
- revenue_last_14d: Total revenue in last 14 days
- ad_views_last_14d: Total ad views in last 14 days

TARGET VARIABLE:
- churned_next_14d: 1 if player has NO activity in next 14 days, 0 otherwise

TRAIN/TEST SPLIT:
- Time-based split (NOT random) to avoid leakage
- Train on players installed before March 15, 2026
- Test on players installed between March 15 and April 2, 2026
"""

import pandas as pd
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    confusion_matrix, classification_report, roc_auc_score, 
    roc_curve, precision_recall_curve, accuracy_score
)
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings('ignore')

print("="*80)
print("DELIVERABLE 4 - CHURN PREDICTION MODEL")
print("="*80)

# Configuration
AS_OF_DATE = pd.to_datetime('2026-04-02')
FEATURE_WINDOW_DAYS = 14  # Look back 14 days for features
CHURN_WINDOW_DAYS = 14    # Look forward 14 days for churn label
TRAIN_CUTOFF_DATE = pd.to_datetime('2026-03-15')  # Players installed before this = train set

print(f"\nModel Configuration:")
print(f"  As-of date: {AS_OF_DATE.date()}")
print(f"  Feature window: {FEATURE_WINDOW_DAYS} days (looking back)")
print(f"  Churn window: {CHURN_WINDOW_DAYS} days (looking forward)")
print(f"  Train/test split: Players installed before {TRAIN_CUTOFF_DATE.date()} = train")

# Load data
print("\nLoading data...")
df_profile = pd.read_csv('player_profile.csv')
df_day = pd.read_csv('player_day.csv')
df_purchase = pd.read_csv('purchase.csv')
df_ad = pd.read_csv('ad_view.csv')

# Convert dates
df_profile['install_date'] = pd.to_datetime(df_profile['install_date'])
df_day['activity_date'] = pd.to_datetime(df_day['activity_date'], format='%Y%m%d')
df_purchase['event_ts'] = pd.to_datetime(df_purchase['event_ts'])
df_ad['event_ts'] = pd.to_datetime(df_ad['event_ts'])

# Define time windows
feature_start = AS_OF_DATE - pd.Timedelta(days=FEATURE_WINDOW_DAYS)
feature_end = AS_OF_DATE
churn_start = AS_OF_DATE + pd.Timedelta(days=1)
churn_end = AS_OF_DATE + pd.Timedelta(days=CHURN_WINDOW_DAYS)

print(f"\nFeature window: {feature_start.date()} to {feature_end.date()}")
print(f"Churn observation window: {churn_start.date()} to {churn_end.date()}")

# Get players who were active on or before as-of date
# and installed before as-of date (exclude brand new players)
eligible_players = df_profile[df_profile['install_date'] <= AS_OF_DATE]['device_id'].values
active_by_as_of = df_day[df_day['activity_date'] <= AS_OF_DATE]['device_id'].unique()
eligible_players = np.intersect1d(eligible_players, active_by_as_of)

print(f"\nEligible players for prediction: {len(eligible_players):,}")

# Build features
print("\nBuilding features...")

# Feature: Activity in last 14 days
activity_features = df_day[
    (df_day['device_id'].isin(eligible_players)) &
    (df_day['activity_date'] >= feature_start) &
    (df_day['activity_date'] <= feature_end)
].groupby('device_id').agg({
    'activity_date': 'count',
    'playtime_minutes': 'sum',
    'session_count': 'sum',
    'player_level': 'max'
}).reset_index()

activity_features.columns = [
    'device_id', 'days_active_last_14d', 'total_playtime_last_14d', 
    'total_sessions_last_14d', 'player_level'
]

# Feature: Purchases in last 14 days
purchase_features = df_purchase[
    (df_purchase['device_id'].isin(eligible_players)) &
    (df_purchase['event_ts'] >= feature_start) &
    (df_purchase['event_ts'] <= feature_end)
].groupby('device_id').agg({
    'usd_amount': 'sum',
    'purchase_id': 'count'
}).reset_index()

purchase_features.columns = ['device_id', 'revenue_last_14d', 'num_purchases_last_14d']
purchase_features['made_purchase_last_14d'] = 1

# Feature: Ad views in last 14 days
ad_features = df_ad[
    (df_ad['device_id'].isin(eligible_players)) &
    (df_ad['event_ts'] >= feature_start) &
    (df_ad['event_ts'] <= feature_end)
].groupby('device_id').agg({
    'event_ts': 'count'
}).reset_index()

ad_features.columns = ['device_id', 'ad_views_last_14d']

# Target: Churn label (no activity in next 14 days)
churned_players = df_day[
    (df_day['activity_date'] >= churn_start) &
    (df_day['activity_date'] <= churn_end)
]['device_id'].unique()

# Merge all features
df_model = pd.DataFrame({'device_id': eligible_players})

# Merge with profile info
df_model = df_model.merge(
    df_profile[['device_id', 'install_date', 'platform', 'country_tier', 'acquisition_channel']], 
    on='device_id', 
    how='left'
)

# Calculate days since install
df_model['days_since_install'] = (AS_OF_DATE - df_model['install_date']).dt.days

# Merge activity features
df_model = df_model.merge(activity_features, on='device_id', how='left')

# Merge purchase features
df_model = df_model.merge(purchase_features, on='device_id', how='left')

# Merge ad features
df_model = df_model.merge(ad_features, on='device_id', how='left')

# Fill NaNs
df_model['days_active_last_14d'] = df_model['days_active_last_14d'].fillna(0)
df_model['total_playtime_last_14d'] = df_model['total_playtime_last_14d'].fillna(0)
df_model['total_sessions_last_14d'] = df_model['total_sessions_last_14d'].fillna(0)
df_model['player_level'] = df_model['player_level'].fillna(1)
df_model['revenue_last_14d'] = df_model['revenue_last_14d'].fillna(0)
df_model['num_purchases_last_14d'] = df_model['num_purchases_last_14d'].fillna(0)
df_model['made_purchase_last_14d'] = df_model['made_purchase_last_14d'].fillna(0)
df_model['ad_views_last_14d'] = df_model['ad_views_last_14d'].fillna(0)

# Create derived features
df_model['avg_playtime_per_day'] = np.where(
    df_model['days_active_last_14d'] > 0,
    df_model['total_playtime_last_14d'] / df_model['days_active_last_14d'],
    0
)

df_model['avg_sessions_per_day'] = np.where(
    df_model['days_active_last_14d'] > 0,
    df_model['total_sessions_last_14d'] / df_model['days_active_last_14d'],
    0
)

# Create churn label
df_model['churned_next_14d'] = np.where(df_model['device_id'].isin(churned_players), 0, 1)

print(f"\nTotal players in dataset: {len(df_model):,}")
print(f"Churned (1): {df_model['churned_next_14d'].sum():,} ({df_model['churned_next_14d'].mean()*100:.2f}%)")
print(f"Retained (0): {(1-df_model['churned_next_14d']).sum():,} ({(1-df_model['churned_next_14d']).mean()*100:.2f}%)")

# Train/test split (time-based)
train_mask = df_model['install_date'] < TRAIN_CUTOFF_DATE
test_mask = ~train_mask

df_train = df_model[train_mask].copy()
df_test = df_model[test_mask].copy()

print(f"\nTrain set: {len(df_train):,} players")
print(f"  Churn rate: {df_train['churned_next_14d'].mean()*100:.2f}%")
print(f"Test set: {len(df_test):,} players")
print(f"  Churn rate: {df_test['churned_next_14d'].mean()*100:.2f}%")

# Select features for model
feature_cols = [
    'days_active_last_14d',
    'total_playtime_last_14d',
    'avg_playtime_per_day',
    'avg_sessions_per_day',
    'player_level',
    'days_since_install',
    'made_purchase_last_14d',
    'revenue_last_14d',
    'ad_views_last_14d',
    'country_tier'
]

X_train = df_train[feature_cols].values
y_train = df_train['churned_next_14d'].values

X_test = df_test[feature_cols].values
y_test = df_test['churned_next_14d'].values

# Train logistic regression model
print("\nTraining logistic regression model...")
model = LogisticRegression(max_iter=1000, random_state=42)
model.fit(X_train, y_train)

# Predictions
y_pred_train = model.predict(X_train)
y_pred_test = model.predict(X_test)

y_pred_proba_train = model.predict_proba(X_train)[:, 1]
y_pred_proba_test = model.predict_proba(X_test)[:, 1]

# Evaluation
print("\n" + "="*80)
print("MODEL EVALUATION")
print("="*80)

print("\nTRAIN SET PERFORMANCE:")
print(f"  Accuracy: {accuracy_score(y_train, y_pred_train):.4f}")
print(f"  ROC-AUC: {roc_auc_score(y_train, y_pred_proba_train):.4f}")
print("\nConfusion Matrix:")
print(confusion_matrix(y_train, y_pred_train))
print("\nClassification Report:")
print(classification_report(y_train, y_pred_train, target_names=['Retained', 'Churned']))

print("\n" + "-"*80)
print("TEST SET PERFORMANCE:")
print(f"  Accuracy: {accuracy_score(y_test, y_pred_test):.4f}")
print(f"  ROC-AUC: {roc_auc_score(y_test, y_pred_proba_test):.4f}")
print("\nConfusion Matrix:")
print(confusion_matrix(y_test, y_pred_test))
print("\nClassification Report:")
print(classification_report(y_test, y_pred_test, target_names=['Retained', 'Churned']))

# Feature importance
print("\n" + "="*80)
print("FEATURE IMPORTANCE (Logistic Regression Coefficients)")
print("="*80)

feature_importance = pd.DataFrame({
    'feature': feature_cols,
    'coefficient': model.coef_[0]
}).sort_values('coefficient', ascending=False)

print(feature_importance.to_string(index=False))
print("\nInterpretation:")
print("  Positive coefficient = increases churn probability")
print("  Negative coefficient = decreases churn probability (increases retention)")

# Save results
df_test['churn_probability'] = y_pred_proba_test
df_test['predicted_churn'] = y_pred_test
df_test[['device_id', 'churned_next_14d', 'predicted_churn', 'churn_probability'] + feature_cols].to_csv(
    'ea_submission/results/4_churn_predictions.csv', index=False
)

feature_importance.to_csv('ea_submission/results/4_feature_importance.csv', index=False)

# Create ROC curve
fpr, tpr, thresholds = roc_curve(y_test, y_pred_proba_test)
plt.figure(figsize=(8, 6))
plt.plot(fpr, tpr, label=f'ROC Curve (AUC = {roc_auc_score(y_test, y_pred_proba_test):.3f})')
plt.plot([0, 1], [0, 1], 'k--', label='Random')
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.title('ROC Curve - Churn Prediction Model')
plt.legend()
plt.grid(alpha=0.3)
plt.tight_layout()
plt.savefig('ea_submission/results/4_roc_curve.png', dpi=150)
print("\nROC curve saved to: ea_submission/results/4_roc_curve.png")

# Create precision-recall curve
precision, recall, thresholds_pr = precision_recall_curve(y_test, y_pred_proba_test)
plt.figure(figsize=(8, 6))
plt.plot(recall, precision)
plt.xlabel('Recall')
plt.ylabel('Precision')
plt.title('Precision-Recall Curve - Churn Prediction Model')
plt.grid(alpha=0.3)
plt.tight_layout()
plt.savefig('ea_submission/results/4_precision_recall_curve.png', dpi=150)
print("Precision-Recall curve saved to: ea_submission/results/4_precision_recall_curve.png")

print("\n" + "="*80)
print("SUMMARY & INTERPRETATION")
print("="*80)
print("""
WHAT WAS BUILT:
- Logistic regression model to predict 14-day churn
- Uses simple, interpretable features based on recent player behavior
- Time-based train/test split to avoid data leakage

KEY FEATURES:
- Recent activity (days active, playtime, sessions)
- Player progression (level, days since install)
- Monetization (purchases, revenue)
- Engagement (ad views)
- Demographics (country tier)

MODEL PERFORMANCE:
- ROC-AUC indicates how well the model ranks churners vs non-churners
- Higher is better (0.5 = random, 1.0 = perfect)
- Confusion matrix shows true/false positives and negatives
- Precision = Of predicted churners, % who actually churned
- Recall = Of actual churners, % we correctly identified

BUSINESS USE:
- Can target high-risk players for retention campaigns
- Threshold can be adjusted based on business goals
- Lower threshold = catch more churners (higher recall, lower precision)
- Higher threshold = focus on most certain churners (lower recall, higher precision)

LIMITATIONS:
- Simple features only - could add more sophisticated signals
- 14-day window may be too short/long depending on game
- Does not account for external factors (seasonality, events, etc.)
- Time-based split means test set is more recent players (may differ from train)
""")

print("\n" + "="*80)
print("Analysis complete. Results saved to ea_submission/results/")
print("="*80)
