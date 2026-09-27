/*
==============================================================================
DELIVERABLE 1(d) - REWARDED ADS ANALYSIS
==============================================================================

PURPOSE:
Analyze rewarded ad viewing behavior:
1. Share of ad-watching player-days that hit the daily cap (by cap value)
2. Total daily ad views across the analysis window
3. Investigate any suspicious patterns in daily ad view data

IMPORTANT NOTES:
- ad_daily_cap: maximum ads a player can watch per day (varies: 5 or 8)
- ad_daily_count: the current count for that player on that day
- A player "hits cap" when ad_daily_count reaches ad_daily_cap
- Date range: focus on 2026-01-01 to 2026-04-30 for consistency
*/

-- PART 1: Daily Ad Cap Analysis
-- ==============================

WITH player_day_ad_summary AS (
    -- Get the maximum ad count reached by each player each day
    SELECT 
        device_id,
        CAST(event_ts AS DATE) AS event_date,
        MAX(ad_daily_count) AS max_ad_count,
        MAX(ad_daily_cap) AS ad_daily_cap
    FROM ad_view
    WHERE CAST(event_ts AS DATE) BETWEEN '2026-01-01' AND '2026-04-30'
    GROUP BY device_id, CAST(event_ts AS DATE)
),

cap_hits AS (
    SELECT 
        ad_daily_cap,
        COUNT(*) AS total_player_days,
        SUM(CASE WHEN max_ad_count >= ad_daily_cap THEN 1 ELSE 0 END) AS player_days_hit_cap,
        SUM(CASE WHEN max_ad_count >= ad_daily_cap THEN 1 ELSE 0 END) * 1.0 / COUNT(*) AS cap_hit_rate
    FROM player_day_ad_summary
    GROUP BY ad_daily_cap
)

SELECT * FROM cap_hits
ORDER BY ad_daily_cap;


-- PART 2: Total Daily Ad Views
-- =============================

WITH daily_ad_counts AS (
    SELECT 
        CAST(event_ts AS DATE) AS event_date,
        COUNT(*) AS total_ad_views,
        COUNT(DISTINCT device_id) AS unique_viewers,
        COUNT(*) * 1.0 / COUNT(DISTINCT device_id) AS avg_ads_per_viewer,
        SUM(CASE WHEN status = 'completed' THEN 1 ELSE 0 END) AS completed_views,
        SUM(CASE WHEN status = 'abandoned' THEN 1 ELSE 0 END) AS abandoned_views,
        SUM(CASE WHEN status = 'started' THEN 1 ELSE 0 END) AS started_views
    FROM ad_view
    WHERE CAST(event_ts AS DATE) BETWEEN '2026-01-01' AND '2026-04-30'
    GROUP BY CAST(event_ts AS DATE)
)

SELECT * FROM daily_ad_counts
ORDER BY event_date;


-- PART 3: Ad View by Status
-- ==========================

WITH ad_status_summary AS (
    SELECT 
        status,
        COUNT(*) AS total_events,
        COUNT(DISTINCT device_id) AS unique_players,
        COUNT(*) * 1.0 / (SELECT COUNT(*) FROM ad_view WHERE CAST(event_ts AS DATE) BETWEEN '2026-01-01' AND '2026-04-30') AS pct_of_total
    FROM ad_view
    WHERE CAST(event_ts AS DATE) BETWEEN '2026-01-01' AND '2026-04-30'
    GROUP BY status
)

SELECT * FROM ad_status_summary;


-- PART 4: Investigate Unusual Patterns
-- =====================================

-- Check for any dates with anomalous ad volumes
WITH daily_stats AS (
    SELECT 
        CAST(event_ts AS DATE) AS event_date,
        COUNT(*) AS ad_views,
        COUNT(DISTINCT device_id) AS unique_viewers
    FROM ad_view
    WHERE CAST(event_ts AS DATE) BETWEEN '2026-01-01' AND '2026-04-30'
    GROUP BY CAST(event_ts AS DATE)
),

stats_with_avg AS (
    SELECT 
        *,
        AVG(ad_views) OVER () AS avg_daily_views,
        STDDEV(ad_views) OVER () AS stddev_daily_views
    FROM daily_stats
)

SELECT 
    event_date,
    ad_views,
    unique_viewers,
    avg_daily_views,
    (ad_views - avg_daily_views) / NULLIF(stddev_daily_views, 0) AS z_score
FROM stats_with_avg
WHERE ABS((ad_views - avg_daily_views) / NULLIF(stddev_daily_views, 0)) > 2  -- Flag outliers
ORDER BY event_date;


-- PART 5: Ad Cap Distribution Over Time
-- ======================================

WITH cap_by_date AS (
    SELECT 
        CAST(event_ts AS DATE) AS event_date,
        ad_daily_cap,
        COUNT(DISTINCT device_id) AS unique_players_with_cap
    FROM ad_view
    WHERE CAST(event_ts AS DATE) BETWEEN '2026-01-01' AND '2026-04-30'
    GROUP BY CAST(event_ts AS DATE), ad_daily_cap
)

SELECT 
    event_date,
    SUM(CASE WHEN ad_daily_cap = 5 THEN unique_players_with_cap ELSE 0 END) AS players_cap_5,
    SUM(CASE WHEN ad_daily_cap = 8 THEN unique_players_with_cap ELSE 0 END) AS players_cap_8
FROM cap_by_date
GROUP BY event_date
ORDER BY event_date;
