-- Total registered users and app opens per device brand
SELECT 
    brand, 
    SUM(count) AS total_registered_users, 
    ROUND(AVG(percentage)::numeric, 2) AS avg_percentage_usage
FROM users_by_device
GROUP BY brand
ORDER BY total_registered_users DESC;
