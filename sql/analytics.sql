/* =========================================================
   Payment Events Analytics
   ========================================================= */

/* 1. Daily Transaction Volume & Value */
SELECT
    DATE(event_timestamp) AS txn_date,
    COUNT(*) AS total_transactions,
    SUM(amount) AS total_amount
FROM fact_transactions
GROUP BY 1
ORDER BY 1;


/* 2. Daily Active Users (DAU) */
SELECT
    DATE(event_timestamp) AS activity_date,
    COUNT(DISTINCT user_id) AS daily_active_users
FROM fact_transactions
GROUP BY 1
ORDER BY 1;


/* 3. Transaction Success vs Failure Rate */
SELECT
    status,
    COUNT(*) AS txn_count,
    ROUND(
        COUNT(*) * 100.0 / SUM(COUNT(*)) OVER (),
        2
    ) AS percentage
FROM fact_transactions
GROUP BY status;


/* 4. Failure Rate by Payment Method */
SELECT
    payment_method,
    COUNT(*) AS total_txns,
    SUM(CASE WHEN status = 'FAILED' THEN 1 ELSE 0 END) AS failed_txns,
    ROUND(
        SUM(CASE WHEN status = 'FAILED' THEN 1 ELSE 0 END) * 100.0 / COUNT(*),
        2
    ) AS failure_rate_pct
FROM fact_transactions
GROUP BY payment_method
ORDER BY failure_rate_pct DESC;


/* 5. Top Users by Total Spend */
SELECT
    user_id,
    COUNT(*) AS txn_count,
    SUM(amount) AS total_spent
FROM fact_transactions
GROUP BY user_id
ORDER BY total_spent DESC
LIMIT 10;


/* 6. Hourly Transaction Distribution */
SELECT
    EXTRACT(HOUR FROM event_timestamp) AS hour_of_day,
    COUNT(*) AS txn_count
FROM fact_transactions
GROUP BY hour_of_day
ORDER BY hour_of_day;
