-- Find states with highest growth in transaction count over time
WITH state_growth AS (
    SELECT 
        state_name,
        year,
        quarter,
        SUM(count) AS tx_count
    FROM aggregated_transactions
    GROUP BY state_name, year, quarter
)
SELECT 
    a.state_name,
    a.year AS current_year,
    a.quarter AS current_quarter,
    a.tx_count AS current_tx,
    b.tx_count AS previous_tx,
    (a.tx_count - b.tx_count) AS growth,
    ROUND((a.tx_count - b.tx_count) * 100.0 / NULLIF(b.tx_count, 0), 2) AS growth_percent
FROM state_growth a
LEFT JOIN state_growth b
    ON a.state_name = b.state_name
   AND (a.year = b.year AND a.quarter = b.quarter + 1 OR a.year = b.year + 1 AND a.quarter = 1 AND b.quarter = 4)
ORDER BY growth_percent DESC NULLS LAST;