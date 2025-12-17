-- Create a dedicated schema for BI tools
CREATE SCHEMA IF NOT EXISTS analytics;

-- 1. Daily Risk Trends (Materialized View)
CREATE TABLE analytics.daily_risk_summary AS
SELECT 
    DATE(event_timestamp) as report_date,
    COUNT(*) as total_tx,
    SUM(CASE WHEN is_fraud = 1 THEN 1 ELSE 0 END) as fraud_cases,
    AVG(amount) as avg_transaction_value
FROM offline_store.transactions
GROUP BY DATE(event_timestamp);

-- 2. High Risk Users Table
CREATE VIEW analytics.high_risk_users AS
SELECT 
    user_id,
    COUNT(*) as tx_count,
    SUM(amount) as total_spend
FROM offline_store.transactions
WHERE is_fraud = 1
GROUP BY user_id
ORDER BY total_spend DESC;