-- Total transaction count and amount by state and quarter
SELECT 
    state_name, 
    year, 
    quarter, 
    SUM(count) AS total_transactions,
    SUM(amount) AS total_amount
FROM aggregated_transactions
GROUP BY state_name, year, quarter
ORDER BY year, quarter, total_transactions DESC;
