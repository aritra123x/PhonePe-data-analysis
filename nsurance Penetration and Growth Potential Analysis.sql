-- State-wise insurance counts and amounts
SELECT 
    state_name, 
    year, 
    quarter, 
    SUM(count) AS total_policies_sold, 
    SUM(amount) AS total_value
FROM aggregated_insurance
WHERE state_name IS NOT NULL
GROUP BY state_name, year, quarter
ORDER BY total_policies_sold DESC;
