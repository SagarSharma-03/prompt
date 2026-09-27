/*
==============================================================================
DELIVERABLE 1(c) - SPENDER BEHAVIOUR ANALYSIS
==============================================================================

PURPOSE:
Analyze spending concentration and purchase timing patterns:
1. Revenue concentration (top 1%, 10%, 50% of spenders)
2. Share of players who never pay
3. Time to first purchase
4. Repeat purchase gap

IMPORTANT NOTES:
- For revenue concentration, we rank PAYING players only (not all players)
- Time to first purchase = first_purchase_date - install_date
- Repeat purchase gap = time between consecutive purchases for each player
*/

-- PART 1: Revenue Concentration
-- ==============================

WITH player_revenue AS (
    SELECT 
        p.device_id,
        SUM(p.usd_amount) AS total_revenue
    FROM purchase p
    GROUP BY p.device_id
),

ranked_spenders AS (
    SELECT 
        device_id,
        total_revenue,
        ROW_NUMBER() OVER (ORDER BY total_revenue DESC) AS revenue_rank,
        COUNT(*) OVER () AS total_spenders,
        SUM(total_revenue) OVER () AS total_revenue_all
    FROM player_revenue
),

revenue_concentration AS (
    SELECT 
        'Top 1%' AS segment,
        COUNT(*) AS num_spenders,
        SUM(total_revenue) AS segment_revenue,
        MAX(total_revenue_all) AS total_revenue,
        SUM(total_revenue) / MAX(total_revenue_all) AS revenue_share
    FROM ranked_spenders
    WHERE revenue_rank <= CEIL(total_spenders * 0.01)
    
    UNION ALL
    
    SELECT 
        'Top 10%' AS segment,
        COUNT(*) AS num_spenders,
        SUM(total_revenue) AS segment_revenue,
        MAX(total_revenue_all) AS total_revenue,
        SUM(total_revenue) / MAX(total_revenue_all) AS revenue_share
    FROM ranked_spenders
    WHERE revenue_rank <= CEIL(total_spenders * 0.10)
    
    UNION ALL
    
    SELECT 
        'Top 50%' AS segment,
        COUNT(*) AS num_spenders,
        SUM(total_revenue) AS segment_revenue,
        MAX(total_revenue_all) AS total_revenue,
        SUM(total_revenue) / MAX(total_revenue_all) AS revenue_share
    FROM ranked_spenders
    WHERE revenue_rank <= CEIL(total_spenders * 0.50)
)

SELECT * FROM revenue_concentration;


-- PART 2: Payer vs Non-Payer Split
-- =================================

WITH payer_split AS (
    SELECT 
        COUNT(*) AS total_players,
        SUM(CASE WHEN first_purchase_date IS NOT NULL THEN 1 ELSE 0 END) AS payers,
        SUM(CASE WHEN first_purchase_date IS NULL THEN 1 ELSE 0 END) AS non_payers,
        SUM(CASE WHEN first_purchase_date IS NOT NULL THEN 1 ELSE 0 END) * 1.0 / COUNT(*) AS payer_rate,
        SUM(CASE WHEN first_purchase_date IS NULL THEN 1 ELSE 0 END) * 1.0 / COUNT(*) AS non_payer_rate
    FROM player_profile
)

SELECT * FROM payer_split;


-- PART 3: Time to First Purchase
-- ===============================

WITH time_to_purchase AS (
    SELECT 
        device_id,
        CAST(install_date AS DATE) AS install_date,
        CAST(first_purchase_date AS DATE) AS first_purchase_date,
        CAST(CAST(first_purchase_date AS DATE) - CAST(install_date AS DATE) AS INTEGER) AS days_to_first_purchase
    FROM player_profile
    WHERE first_purchase_date IS NOT NULL
)

SELECT 
    COUNT(*) AS total_payers,
    AVG(days_to_first_purchase) AS avg_days_to_first_purchase,
    MIN(days_to_first_purchase) AS min_days_to_first_purchase,
    MAX(days_to_first_purchase) AS max_days_to_first_purchase,
    PERCENTILE_CONT(0.25) WITHIN GROUP (ORDER BY days_to_first_purchase) AS p25_days,
    PERCENTILE_CONT(0.50) WITHIN GROUP (ORDER BY days_to_first_purchase) AS median_days,
    PERCENTILE_CONT(0.75) WITHIN GROUP (ORDER BY days_to_first_purchase) AS p75_days,
    -- Bucketed distribution
    SUM(CASE WHEN days_to_first_purchase = 0 THEN 1 ELSE 0 END) AS same_day_purchasers,
    SUM(CASE WHEN days_to_first_purchase BETWEEN 1 AND 7 THEN 1 ELSE 0 END) AS day_1_to_7,
    SUM(CASE WHEN days_to_first_purchase BETWEEN 8 AND 30 THEN 1 ELSE 0 END) AS day_8_to_30,
    SUM(CASE WHEN days_to_first_purchase > 30 THEN 1 ELSE 0 END) AS after_day_30
FROM time_to_purchase;


-- PART 4: Repeat Purchase Gap
-- ============================

WITH purchase_dates AS (
    SELECT 
        device_id,
        CAST(event_ts AS DATE) AS purchase_date,
        ROW_NUMBER() OVER (PARTITION BY device_id ORDER BY event_ts) AS purchase_number
    FROM purchase
),

purchase_gaps AS (
    SELECT 
        curr.device_id,
        curr.purchase_date AS current_purchase,
        prev.purchase_date AS previous_purchase,
        CAST(curr.purchase_date - prev.purchase_date AS INTEGER) AS days_between_purchases
    FROM purchase_dates curr
    INNER JOIN purchase_dates prev 
        ON curr.device_id = prev.device_id 
        AND curr.purchase_number = prev.purchase_number + 1
)

SELECT 
    COUNT(*) AS total_repeat_purchases,
    AVG(days_between_purchases) AS avg_days_between_purchases,
    MIN(days_between_purchases) AS min_days_between,
    MAX(days_between_purchases) AS max_days_between,
    PERCENTILE_CONT(0.25) WITHIN GROUP (ORDER BY days_between_purchases) AS p25_days_between,
    PERCENTILE_CONT(0.50) WITHIN GROUP (ORDER BY days_between_purchases) AS median_days_between,
    PERCENTILE_CONT(0.75) WITHIN GROUP (ORDER BY days_between_purchases) AS p75_days_between,
    -- Bucketed distribution
    SUM(CASE WHEN days_between_purchases = 0 THEN 1 ELSE 0 END) AS same_day_repeat,
    SUM(CASE WHEN days_between_purchases BETWEEN 1 AND 7 THEN 1 ELSE 0 END) AS within_week,
    SUM(CASE WHEN days_between_purchases BETWEEN 8 AND 30 THEN 1 ELSE 0 END) AS within_month,
    SUM(CASE WHEN days_between_purchases > 30 THEN 1 ELSE 0 END) AS after_month
FROM purchase_gaps;
