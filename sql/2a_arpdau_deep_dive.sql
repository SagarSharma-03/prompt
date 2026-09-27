/*
==============================================================================
DELIVERABLE 2(a) - ARPDAU DEEP DIVE
==============================================================================

PURPOSE:
Investigate why overall ARPDAU falls by ~16% comparing first 30 days vs last 30 days,
even though every country tier appears flat or improving.

HYPOTHESIS:
This could be Simpson's Paradox - a composition/mix shift effect where:
- Individual country tier ARPDAU trends are stable or improving
- But overall ARPDAU falls due to changes in the mix of players by country tier
- Lower-tier countries (which have lower ARPDAU) could be growing faster

ANALYSIS APPROACH:
1. Calculate overall ARPDAU for first 30 days vs last 30 days
2. Calculate ARPDAU by country_tier for both periods
3. Calculate DAU mix by country_tier for both periods
4. Quantify the composition effect
*/

-- PART 1: Overall ARPDAU Comparison (First 30 vs Last 30 days)
-- =============================================================

WITH date_ranges AS (
    SELECT 
        DATE '2026-01-01' AS first_period_start,
        DATE '2026-01-30' AS first_period_end,
        DATE '2026-04-01' AS last_period_start,
        DATE '2026-04-30' AS last_period_end
),

first_30_metrics AS (
    SELECT 
        COUNT(DISTINCT pd.device_id) AS dau,
        COALESCE(SUM(p.usd_amount), 0) AS revenue,
        COALESCE(SUM(p.usd_amount), 0) / COUNT(DISTINCT pd.device_id) AS arpdau
    FROM player_day pd
    CROSS JOIN date_ranges dr
    INNER JOIN player_profile pp ON pd.device_id = pp.device_id
    LEFT JOIN purchase p 
        ON pd.device_id = p.device_id 
        AND CAST(p.event_ts AS DATE) = CAST(STRPTIME(CAST(pd.activity_date AS VARCHAR), '%Y%m%d') AS DATE)
    WHERE CAST(STRPTIME(CAST(pd.activity_date AS VARCHAR), '%Y%m%d') AS DATE) BETWEEN dr.first_period_start AND dr.first_period_end
),

last_30_metrics AS (
    SELECT 
        COUNT(DISTINCT pd.device_id) AS dau,
        COALESCE(SUM(p.usd_amount), 0) AS revenue,
        COALESCE(SUM(p.usd_amount), 0) / COUNT(DISTINCT pd.device_id) AS arpdau
    FROM player_day pd
    CROSS JOIN date_ranges dr
    INNER JOIN player_profile pp ON pd.device_id = pp.device_id
    LEFT JOIN purchase p 
        ON pd.device_id = p.device_id 
        AND CAST(p.event_ts AS DATE) = CAST(STRPTIME(CAST(pd.activity_date AS VARCHAR), '%Y%m%d') AS DATE)
    WHERE CAST(STRPTIME(CAST(pd.activity_date AS VARCHAR), '%Y%m%d') AS DATE) BETWEEN dr.last_period_start AND dr.last_period_end
)

SELECT 
    'First 30 Days' AS period,
    dau,
    revenue,
    arpdau
FROM first_30_metrics

UNION ALL

SELECT 
    'Last 30 Days' AS period,
    dau,
    revenue,
    arpdau
FROM last_30_metrics;


-- PART 2: ARPDAU by Country Tier (First 30 vs Last 30 days)
-- ==========================================================

WITH date_ranges AS (
    SELECT 
        DATE '2026-01-01' AS first_period_start,
        DATE '2026-01-30' AS first_period_end,
        DATE '2026-04-01' AS last_period_start,
        DATE '2026-04-30' AS last_period_end
),

first_30_by_tier AS (
    SELECT 
        pp.country_tier,
        COUNT(DISTINCT pd.device_id) AS dau,
        COALESCE(SUM(p.usd_amount), 0) AS revenue,
        COALESCE(SUM(p.usd_amount), 0) / COUNT(DISTINCT pd.device_id) AS arpdau
    FROM player_day pd
    CROSS JOIN date_ranges dr
    INNER JOIN player_profile pp ON pd.device_id = pp.device_id
    LEFT JOIN purchase p 
        ON pd.device_id = p.device_id 
        AND CAST(p.event_ts AS DATE) = CAST(STRPTIME(CAST(pd.activity_date AS VARCHAR), '%Y%m%d') AS DATE)
    WHERE CAST(STRPTIME(CAST(pd.activity_date AS VARCHAR), '%Y%m%d') AS DATE) BETWEEN dr.first_period_start AND dr.first_period_end
    GROUP BY pp.country_tier
),

last_30_by_tier AS (
    SELECT 
        pp.country_tier,
        COUNT(DISTINCT pd.device_id) AS dau,
        COALESCE(SUM(p.usd_amount), 0) AS revenue,
        COALESCE(SUM(p.usd_amount), 0) / COUNT(DISTINCT pd.device_id) AS arpdau
    FROM player_day pd
    CROSS JOIN date_ranges dr
    INNER JOIN player_profile pp ON pd.device_id = pp.device_id
    LEFT JOIN purchase p 
        ON pd.device_id = p.device_id 
        AND CAST(p.event_ts AS DATE) = CAST(STRPTIME(CAST(pd.activity_date AS VARCHAR), '%Y%m%d') AS DATE)
    WHERE CAST(STRPTIME(CAST(pd.activity_date AS VARCHAR), '%Y%m%d') AS DATE) BETWEEN dr.last_period_start AND dr.last_period_end
    GROUP BY pp.country_tier
)

SELECT 
    f.country_tier,
    f.dau AS first_30_dau,
    f.revenue AS first_30_revenue,
    f.arpdau AS first_30_arpdau,
    l.dau AS last_30_dau,
    l.revenue AS last_30_revenue,
    l.arpdau AS last_30_arpdau,
    l.arpdau - f.arpdau AS arpdau_change,
    (l.arpdau - f.arpdau) / NULLIF(f.arpdau, 0) AS arpdau_pct_change
FROM first_30_by_tier f
INNER JOIN last_30_by_tier l ON f.country_tier = l.country_tier
ORDER BY f.country_tier;


-- PART 3: DAU Mix by Country Tier
-- ================================

WITH date_ranges AS (
    SELECT 
        DATE '2026-01-01' AS first_period_start,
        DATE '2026-01-30' AS first_period_end,
        DATE '2026-04-01' AS last_period_start,
        DATE '2026-04-30' AS last_period_end
),

first_30_mix AS (
    SELECT 
        pp.country_tier,
        COUNT(DISTINCT pd.device_id) AS dau,
        SUM(COUNT(DISTINCT pd.device_id)) OVER () AS total_dau,
        COUNT(DISTINCT pd.device_id) * 1.0 / SUM(COUNT(DISTINCT pd.device_id)) OVER () AS dau_share
    FROM player_day pd
    CROSS JOIN date_ranges dr
    INNER JOIN player_profile pp ON pd.device_id = pp.device_id
    WHERE CAST(STRPTIME(CAST(pd.activity_date AS VARCHAR), '%Y%m%d') AS DATE) BETWEEN dr.first_period_start AND dr.first_period_end
    GROUP BY pp.country_tier
),

last_30_mix AS (
    SELECT 
        pp.country_tier,
        COUNT(DISTINCT pd.device_id) AS dau,
        SUM(COUNT(DISTINCT pd.device_id)) OVER () AS total_dau,
        COUNT(DISTINCT pd.device_id) * 1.0 / SUM(COUNT(DISTINCT pd.device_id)) OVER () AS dau_share
    FROM player_day pd
    CROSS JOIN date_ranges dr
    INNER JOIN player_profile pp ON pd.device_id = pp.device_id
    WHERE CAST(STRPTIME(CAST(pd.activity_date AS VARCHAR), '%Y%m%d') AS DATE) BETWEEN dr.last_period_start AND dr.last_period_end
    GROUP BY pp.country_tier
)

SELECT 
    f.country_tier,
    f.dau AS first_30_dau,
    f.dau_share AS first_30_share,
    l.dau AS last_30_dau,
    l.dau_share AS last_30_share,
    l.dau_share - f.dau_share AS share_change
FROM first_30_mix f
INNER JOIN last_30_mix l ON f.country_tier = l.country_tier
ORDER BY f.country_tier;
