-- Q1: What is the WoW (Week over Week) fraud growth?
SELECT 
    DATE_TRUNC('week', event_timestamp) as week,
    COUNT(*) as fraud_count
FROM offline_store.transactions
WHERE is_fraud = 1
GROUP BY 1
ORDER BY 1;

-- Q2: Are high-value transactions riskier?
SELECT 
    CASE 
        WHEN amount < 50 THEN 'Low Value'
        WHEN amount BETWEEN 50 AND 200 THEN 'Mid Value'
        ELSE 'High Value'
    END as tx_bucket,
    AVG(is_fraud) as fraud_rate
FROM offline_store.transactions
GROUP BY 1;