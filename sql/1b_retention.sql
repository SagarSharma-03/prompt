/*
==============================================================================
DELIVERABLE 1(b) - COHORT RETENTION ANALYSIS
==============================================================================

PURPOSE:
Create a cohort retention table showing Day 1, Day 7, Day 14, and Day 30 retention
for players grouped by install week.

DEFINITIONS:
- Install week: Week starting on the date of install (e.g., week of 2025-06-01)
- Day N retention: % of installs in that cohort who were active on Day N after install
- Day 0 = install date, Day 1 = day after install, etc.

IMPORTANT NOTES:
- Recent cohorts may be incomplete (not enough time has passed to observe Day 30)
- We will calculate retention for all cohorts but flag incomplete observation periods
- A player is "retained" on Day N if they have a record in player_day on that specific day
*/

-- Step 1: Get install cohorts (week of install)
WITH install_cohorts AS (
    SELECT 
        device_id,
        CAST(install_date AS DATE) AS install_date,
        DATE_TRUNC('week', CAST(install_date AS DATE)) AS install_week
    FROM player_profile
),

-- Step 2: Get all player activity dates
player_activity AS (
    SELECT 
        device_id,
        CAST(STRPTIME(CAST(activity_date AS VARCHAR), '%Y%m%d') AS DATE) AS activity_date
    FROM player_day
),

-- Step 3: Calculate days since install for each activity
activity_with_days_since_install AS (
    SELECT 
        ic.device_id,
        ic.install_week,
        ic.install_date,
        pa.activity_date,
        CAST((pa.activity_date - ic.install_date) AS INTEGER) AS days_since_install
    FROM install_cohorts ic
    INNER JOIN player_activity pa ON ic.device_id = pa.device_id
),

-- Step 4: Get cohort sizes (all installs)
cohort_sizes AS (
    SELECT 
        install_week,
        COUNT(DISTINCT device_id) AS cohort_size
    FROM install_cohorts
    GROUP BY install_week
),

-- Step 5: Calculate retention by cohort
cohort_retention AS (
    SELECT 
        a.install_week,
        COUNT(DISTINCT CASE WHEN a.days_since_install = 1 THEN a.device_id END) AS day1_retained,
        COUNT(DISTINCT CASE WHEN a.days_since_install = 7 THEN a.device_id END) AS day7_retained,
        COUNT(DISTINCT CASE WHEN a.days_since_install = 14 THEN a.device_id END) AS day14_retained,
        COUNT(DISTINCT CASE WHEN a.days_since_install = 30 THEN a.device_id END) AS day30_retained
    FROM activity_with_days_since_install a
    WHERE a.days_since_install IN (1, 7, 14, 30)
    GROUP BY a.install_week
)

-- Step 6: Calculate retention rates
SELECT 
    cs.install_week,
    cs.cohort_size,
    COALESCE(cr.day1_retained, 0) AS day1_retained,
    CAST(COALESCE(cr.day1_retained, 0) AS FLOAT) / cs.cohort_size AS day1_retention,
    COALESCE(cr.day7_retained, 0) AS day7_retained,
    CAST(COALESCE(cr.day7_retained, 0) AS FLOAT) / cs.cohort_size AS day7_retention,
    COALESCE(cr.day14_retained, 0) AS day14_retained,
    CAST(COALESCE(cr.day14_retained, 0) AS FLOAT) / cs.cohort_size AS day14_retention,
    COALESCE(cr.day30_retained, 0) AS day30_retained,
    CAST(COALESCE(cr.day30_retained, 0) AS FLOAT) / cs.cohort_size AS day30_retention,
    -- Flag incomplete cohorts (installed less than 30 days before end of observation period)
    CASE 
        WHEN cs.install_week > DATE '2026-04-30' - INTERVAL '30 days' THEN 'Incomplete'
        ELSE 'Complete'
    END AS cohort_status
FROM cohort_sizes cs
LEFT JOIN cohort_retention cr ON cs.install_week = cr.install_week
ORDER BY cs.install_week;
