-- Transformation: User Risk Profile
-- Aggregates historical fraud flags

CREATE OR REPLACE VIEW `kairos-platform.fraud_data.user_risk_profile` AS
SELECT
    user_id,
    COUNTIF(is_fraud = 1) AS total_fraud_tx,
    MAX(event_timestamp) AS last_active,
    STDDEV(amount) AS amount_std_dev
FROM
    `kairos-platform.fraud_data.transactions`
GROUP BY
    user_id;