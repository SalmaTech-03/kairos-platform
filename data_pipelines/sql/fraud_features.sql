-- Transformation: User Transaction Velocity
-- Calculates how many transactions a user made in the last hour/day

CREATE OR REPLACE TABLE `kairos-platform.fraud_data.user_velocity` AS
SELECT
    user_id,
    COUNT(*) AS tx_count_1h,
    SUM(amount) AS total_spend_1h,
    AVG(amount) AS avg_spend_1h,
    CURRENT_TIMESTAMP() AS calculation_time
FROM
    `kairos-platform.fraud_data.transactions`
WHERE
    event_timestamp >= TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 1 HOUR)
GROUP BY
    user_id;