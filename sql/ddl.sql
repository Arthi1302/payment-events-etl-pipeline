/* =========================================================
   Payment Events Data Model (Snowflake)
   ========================================================= */

-- ========================================================
-- Dimension: Users
-- ========================================================
CREATE OR REPLACE TABLE dim_users (
    user_id STRING COMMENT 'Unique identifier for each user'
)
COMMENT = 'User dimension table';


-- ========================================================
-- Dimension: Payment Methods
-- ========================================================
CREATE OR REPLACE TABLE dim_payment_methods (
    payment_method STRING COMMENT 'Payment method used (UPI, CARD, etc.)'
)
COMMENT = 'Payment method dimension table';


-- ========================================================
-- Fact: Transactions
-- ========================================================
CREATE OR REPLACE TABLE fact_transactions (
    transaction_id STRING COMMENT 'Unique transaction identifier',
    user_id STRING COMMENT 'User who performed the transaction',
    payment_method STRING COMMENT 'Payment method used',
    amount NUMBER(10,2) COMMENT 'Transaction amount',
    currency STRING COMMENT 'Transaction currency',
    status STRING COMMENT 'Transaction status (SUCCESS / FAILED)',
    failure_reason STRING COMMENT 'Reason for failure if transaction failed',
    event_timestamp TIMESTAMP_NTZ COMMENT 'Timestamp of transaction event'
)
COMMENT = 'Fact table storing payment transaction events';
