/*
==============================================================================
DELIVERABLE 1(a) - DAILY HEALTH METRICS
==============================================================================

PURPOSE:
Calculate daily game health metrics by day and platform:
- Daily Active Players (DAU)
- Gross Revenue
- ARPDAU (Average Revenue Per Daily Active User)
- Share of active players who made a purchase

IMPORTANT NOTES:
- Uses player_day table for DAU (one row per player per day of activity)
- Uses purchase table for revenue (purchases timestamped to specific datetime)
- ARPDAU = Total Revenue / DAU for that day and platform
- Payer rate = Unique purchasers / DAU for that day and platform
- Date range: 2026-01-01 to 2026-04-30
*/

-- Step 1: Get Daily Active Users by platform
-- Table grain: player_day is already at device_id + activity_date level
-- Note: activity_date is stored as integer in YYYYMMDD format
WITH daily_active_users AS (
    SELECT 
        CAST(STRPTIME(CAST(pd.activity_date AS VARCHAR), '%Y%m%d') AS DATE) AS activity_date,
        pp.platform,
        COUNT(DISTINCT pd.device_id) AS dau
    FROM player_day pd
    INNER JOIN player_profile pp ON pd.device_id = pp.device_id
    WHERE CAST(STRPTIME(CAST(pd.activity_date AS VARCHAR), '%Y%m%d') AS DATE) BETWEEN '2026-01-01' AND '2026-04-30'
    GROUP BY CAST(STRPTIME(CAST(pd.activity_date AS VARCHAR), '%Y%m%d') AS DATE), pp.platform
),

-- Step 2: Get daily revenue by platform
-- Join purchase to profile to get platform
-- Extract date from timestamp for daily aggregation
daily_revenue AS (
    SELECT 
        CAST(p.event_ts AS DATE) AS purchase_date,
        pp.platform,
        SUM(p.usd_amount) AS gross_revenue,
        COUNT(DISTINCT p.device_id) AS unique_purchasers
    FROM purchase p
    INNER JOIN player_profile pp ON p.device_id = pp.device_id
    WHERE CAST(p.event_ts AS DATE) BETWEEN '2026-01-01' AND '2026-04-30'
    GROUP BY CAST(p.event_ts AS DATE), pp.platform
)

-- Step 3: Combine DAU and revenue metrics
SELECT 
    dau.activity_date,
    dau.platform,
    dau.dau AS daily_active_players,
    COALESCE(rev.gross_revenue, 0) AS gross_revenue,
    COALESCE(rev.gross_revenue, 0) / dau.dau AS arpdau,
    COALESCE(rev.unique_purchasers, 0) * 1.0 / dau.dau AS payer_rate
FROM daily_active_users dau
LEFT JOIN daily_revenue rev 
    ON dau.activity_date = rev.purchase_date 
    AND dau.platform = rev.platform
ORDER BY dau.activity_date, dau.platform;
