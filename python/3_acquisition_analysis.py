"""
==============================================================================
DELIVERABLE 3 - ACQUISITION CHANNEL ANALYSIS
==============================================================================

PURPOSE:
Compare acquisition channels (organic, paid_social, paid_video) to determine
if they genuinely differ in player quality.

METRICS:
1. Engagement metric: Average playtime per player in first 30 days after install
2. Revenue metric: Average revenue per player in first 30 days after install

STATISTICAL ANALYSIS:
- Calculate confidence intervals for differences
- Test statistical significance
- Distinguish between statistical and business significance

IMPORTANT CONSIDERATIONS:
- Different install volumes across channels
- Need to account for incomplete observation windows
- Avoid misleading pooled comparisons
"""

import pandas as pd
import numpy as np
from scipy import stats
import warnings
warnings.filterwarnings('ignore')

print("="*80)
print("DELIVERABLE 3 - ACQUISITION CHANNEL ANALYSIS")
print("="*80)

# Load data
print("\nLoading data...")
df_profile = pd.read_csv('player_profile.csv')
df_day = pd.read_csv('player_day.csv')
df_purchase = pd.read_csv('purchase.csv')

# Convert dates
df_profile['install_date'] = pd.to_datetime(df_profile['install_date'])
df_day['activity_date'] = pd.to_datetime(df_day['activity_date'], format='%Y%m%d')
df_purchase['event_ts'] = pd.to_datetime(df_purchase['event_ts'])

# Define observation window: only include players installed before 2026-03-31
# so they have at least 30 days of observation by 2026-04-30
observation_cutoff = pd.to_datetime('2026-03-31')
df_profile_filtered = df_profile[df_profile['install_date'] <= observation_cutoff].copy()

print(f"\nTotal players: {len(df_profile):,}")
print(f"Players with complete 30-day window: {len(df_profile_filtered):,}")
print(f"\nChannel distribution (complete observation):")
print(df_profile_filtered['acquisition_channel'].value_counts())

# Calculate metrics per player for first 30 days after install
print("\n" + "="*80)
print("CALCULATING PLAYER-LEVEL METRICS (First 30 days after install)")
print("="*80)

# Merge activity data with install dates
df_day_with_install = df_day.merge(
    df_profile_filtered[['device_id', 'install_date', 'acquisition_channel']], 
    on='device_id', 
    how='inner'
)

# Calculate days since install
df_day_with_install['days_since_install'] = (
    df_day_with_install['activity_date'] - df_day_with_install['install_date']
).dt.days

# Filter to first 30 days (0-29)
df_day_30d = df_day_with_install[
    (df_day_with_install['days_since_install'] >= 0) & 
    (df_day_with_install['days_since_install'] <= 29)
]

# Aggregate playtime by player
playtime_metrics = df_day_30d.groupby('device_id').agg({
    'playtime_minutes': 'sum',
    'activity_date': 'count'
}).reset_index()
playtime_metrics.columns = ['device_id', 'total_playtime_30d', 'active_days_30d']

# Merge purchase data with install dates
df_purchase_with_install = df_purchase.merge(
    df_profile_filtered[['device_id', 'install_date']], 
    on='device_id', 
    how='inner'
)

# Calculate days since install for purchases
df_purchase_with_install['days_since_install'] = (
    df_purchase_with_install['event_ts'] - df_purchase_with_install['install_date']
).dt.days

# Filter to first 30 days
df_purchase_30d = df_purchase_with_install[
    (df_purchase_with_install['days_since_install'] >= 0) & 
    (df_purchase_with_install['days_since_install'] <= 29)
]

# Aggregate revenue by player
revenue_metrics = df_purchase_30d.groupby('device_id').agg({
    'usd_amount': 'sum'
}).reset_index()
revenue_metrics.columns = ['device_id', 'total_revenue_30d']
revenue_metrics['made_purchase_30d'] = 1

# Start with all players in filtered profile
df_metrics = df_profile_filtered[['device_id', 'acquisition_channel', 'install_date']].copy()

# Merge playtime metrics (left join to keep all players)
df_metrics = df_metrics.merge(playtime_metrics, on='device_id', how='left')

# Merge revenue metrics (left join to keep all players)
df_metrics = df_metrics.merge(revenue_metrics, on='device_id', how='left')

# Fill NaN values with 0
df_metrics['total_playtime_30d'] = df_metrics['total_playtime_30d'].fillna(0)
df_metrics['active_days_30d'] = df_metrics['active_days_30d'].fillna(0)
df_metrics['total_revenue_30d'] = df_metrics['total_revenue_30d'].fillna(0)
df_metrics['made_purchase_30d'] = df_metrics['made_purchase_30d'].fillna(0)

print(f"Calculated metrics for {len(df_metrics):,} players")

# Save player-level metrics
df_metrics.to_csv('ea_submission/results/3_player_metrics_by_channel.csv', index=False)

print("\n" + "="*80)
print("SUMMARY BY ACQUISITION CHANNEL")
print("="*80)

summary = df_metrics.groupby('acquisition_channel').agg({
    'device_id': 'count',
    'total_playtime_30d': ['mean', 'std'],
    'active_days_30d': ['mean', 'std'],
    'total_revenue_30d': ['mean', 'std'],
    'made_purchase_30d': 'mean'
}).round(4)

summary.columns = ['_'.join(col).strip('_') for col in summary.columns]
summary = summary.rename(columns={
    'device_id_count': 'num_players',
    'total_playtime_30d_mean': 'avg_playtime_30d',
    'total_playtime_30d_std': 'std_playtime_30d',
    'active_days_30d_mean': 'avg_active_days_30d',
    'active_days_30d_std': 'std_active_days_30d',
    'total_revenue_30d_mean': 'avg_revenue_30d',
    'total_revenue_30d_std': 'std_revenue_30d',
    'made_purchase_30d_mean': 'conversion_rate_30d'
})

print("\n", summary)
summary.to_csv('ea_submission/results/3_summary_by_channel.csv')

# Statistical comparisons
print("\n" + "="*80)
print("STATISTICAL COMPARISONS (Pairwise)")
print("="*80)

channels = ['organic', 'paid_social', 'paid_video']
comparisons = []

for i in range(len(channels)):
    for j in range(i+1, len(channels)):
        channel_a = channels[i]
        channel_b = channels[j]
        
        data_a = df_metrics[df_metrics['acquisition_channel'] == channel_a]
        data_b = df_metrics[df_metrics['acquisition_channel'] == channel_b]
        
        # Engagement metric: playtime
        playtime_a = data_a['total_playtime_30d'].values
        playtime_b = data_b['total_playtime_30d'].values
        
        # Two-sample t-test for playtime
        t_stat_playtime, p_val_playtime = stats.ttest_ind(playtime_a, playtime_b)
        mean_diff_playtime = playtime_a.mean() - playtime_b.mean()
        
        # 95% confidence interval for difference in means (playtime)
        se_playtime = np.sqrt(playtime_a.var()/len(playtime_a) + playtime_b.var()/len(playtime_b))
        ci_low_playtime = mean_diff_playtime - 1.96 * se_playtime
        ci_high_playtime = mean_diff_playtime + 1.96 * se_playtime
        
        # Revenue metric
        revenue_a = data_a['total_revenue_30d'].values
        revenue_b = data_b['total_revenue_30d'].values
        
        # Two-sample t-test for revenue
        t_stat_revenue, p_val_revenue = stats.ttest_ind(revenue_a, revenue_b)
        mean_diff_revenue = revenue_a.mean() - revenue_b.mean()
        
        # 95% confidence interval for difference in means (revenue)
        se_revenue = np.sqrt(revenue_a.var()/len(revenue_a) + revenue_b.var()/len(revenue_b))
        ci_low_revenue = mean_diff_revenue - 1.96 * se_revenue
        ci_high_revenue = mean_diff_revenue + 1.96 * se_revenue
        
        comparisons.append({
            'comparison': f'{channel_a} vs {channel_b}',
            'n_a': len(data_a),
            'n_b': len(data_b),
            'mean_playtime_a': playtime_a.mean(),
            'mean_playtime_b': playtime_b.mean(),
            'playtime_diff': mean_diff_playtime,
            'playtime_ci_low': ci_low_playtime,
            'playtime_ci_high': ci_high_playtime,
            'playtime_p_value': p_val_playtime,
            'playtime_significant': 'Yes' if p_val_playtime < 0.05 else 'No',
            'mean_revenue_a': revenue_a.mean(),
            'mean_revenue_b': revenue_b.mean(),
            'revenue_diff': mean_diff_revenue,
            'revenue_ci_low': ci_low_revenue,
            'revenue_ci_high': ci_high_revenue,
            'revenue_p_value': p_val_revenue,
            'revenue_significant': 'Yes' if p_val_revenue < 0.05 else 'No'
        })

df_comparisons = pd.DataFrame(comparisons)
df_comparisons.to_csv('ea_submission/results/3_statistical_comparisons.csv', index=False)

# Display comparisons
for _, row in df_comparisons.iterrows():
    print(f"\n{row['comparison']}")
    print("-"*80)
    print(f"Sample sizes: {row['n_a']:,} vs {row['n_b']:,}")
    print(f"\nENGAGEMENT (Avg playtime in first 30 days):")
    print(f"  {row['comparison'].split(' vs ')[0]}: {row['mean_playtime_a']:.2f} minutes")
    print(f"  {row['comparison'].split(' vs ')[1]}: {row['mean_playtime_b']:.2f} minutes")
    print(f"  Difference: {row['playtime_diff']:.2f} minutes")
    print(f"  95% CI: [{row['playtime_ci_low']:.2f}, {row['playtime_ci_high']:.2f}]")
    print(f"  p-value: {row['playtime_p_value']:.4f}")
    print(f"  Statistically significant: {row['playtime_significant']}")
    
    print(f"\nREVENUE (Avg revenue in first 30 days):")
    print(f"  {row['comparison'].split(' vs ')[0]}: ${row['mean_revenue_a']:.2f}")
    print(f"  {row['comparison'].split(' vs ')[1]}: ${row['mean_revenue_b']:.2f}")
    print(f"  Difference: ${row['revenue_diff']:.2f}")
    print(f"  95% CI: [${row['revenue_ci_low']:.2f}, ${row['revenue_ci_high']:.2f}]")
    print(f"  p-value: {row['revenue_p_value']:.4f}")
    print(f"  Statistically significant: {row['revenue_significant']}")

print("\n" + "="*80)
print("KEY FINDINGS")
print("="*80)
print("""
1. Statistical vs Business Significance:
   - Statistical significance (p < 0.05) indicates the difference is unlikely due to chance
   - Business significance requires considering the magnitude of the difference
   - A small difference can be statistically significant with large sample sizes

2. Important Considerations:
   - Only players installed before 2026-03-31 are included (complete 30-day window)
   - Metrics measured in first 30 days after install for each player
   - Different sample sizes across channels affect confidence intervals
   
3. Next Steps:
   - Review confidence intervals to assess practical significance
   - Consider cohort effects (are channels trending differently over time?)
   - Investigate why certain channels perform better/worse
""")

print("\n" + "="*80)
print("Analysis complete. Results saved to ea_submission/results/")
print("="*80)
