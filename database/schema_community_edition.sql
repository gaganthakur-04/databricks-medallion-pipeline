-- Databricks Community Edition — Database & Table Setup
-- Uses Hive metastore databases (no Unity Catalog).
-- Run in a Databricks notebook: %sql ... or spark.sql(...)

-- =============================================================================
-- Databases (Medallion layers)
-- =============================================================================
CREATE DATABASE IF NOT EXISTS bronze
COMMENT 'Raw ingested CSV data — no transformations';

CREATE DATABASE IF NOT EXISTS silver
COMMENT 'Validated data with quality_check_result flags';

CREATE DATABASE IF NOT EXISTS gold
COMMENT 'Business analytics aggregations';

-- =============================================================================
-- Bronze tables (Delta)
-- =============================================================================
CREATE TABLE IF NOT EXISTS bronze.customers (
    customer_id       INT,
    customer_name     STRING,
    email             STRING,
    country           STRING,
    signup_date       DATE,
    customer_segment  STRING,
    lifetime_value    DECIMAL(12, 2),
    _ingested_at      TIMESTAMP,
    _source_file      STRING,
    _batch_id         STRING
) USING DELTA
COMMENT 'Raw customers CSV ingest';

CREATE TABLE IF NOT EXISTS bronze.orders (
    order_id       INT,
    customer_id    INT,
    order_date     DATE,
    product_id     INT,
    quantity       INT,
    unit_price     DECIMAL(12, 2),
    total_amount   DECIMAL(12, 2),
    order_status   STRING,
    payment_date   DATE,
    _ingested_at   TIMESTAMP,
    _source_file   STRING,
    _batch_id      STRING
) USING DELTA
COMMENT 'Raw orders CSV ingest';

CREATE TABLE IF NOT EXISTS bronze.products (
    product_id      INT,
    product_name    STRING,
    category        STRING,
    price           DECIMAL(12, 2),
    cost            DECIMAL(12, 2),
    stock_quantity  INT,
    reorder_level   INT,
    _ingested_at    TIMESTAMP,
    _source_file    STRING,
    _batch_id       STRING
) USING DELTA
COMMENT 'Raw products CSV ingest';

-- =============================================================================
-- Silver tables (Delta) — created now for pipeline consistency; populated in Silver phase
-- =============================================================================
CREATE TABLE IF NOT EXISTS silver.customers (
    customer_id          INT,
    customer_name        STRING,
    email                STRING,
    country              STRING,
    signup_date          DATE,
    customer_segment     STRING,
    lifetime_value       DECIMAL(12, 2),
    quality_check_result STRING,
    _silver_processed_at TIMESTAMP
) USING DELTA;

CREATE TABLE IF NOT EXISTS silver.orders (
    order_id             INT,
    customer_id          INT,
    order_date           DATE,
    product_id           INT,
    quantity             INT,
    unit_price           DECIMAL(12, 2),
    total_amount         DECIMAL(12, 2),
    order_status         STRING,
    payment_date         DATE,
    quality_check_result STRING,
    _silver_processed_at TIMESTAMP
) USING DELTA;

CREATE TABLE IF NOT EXISTS silver.products (
    product_id           INT,
    product_name         STRING,
    category             STRING,
    price                DECIMAL(12, 2),
    cost                 DECIMAL(12, 2),
    stock_quantity       INT,
    reorder_level        INT,
    quality_check_result STRING,
    _silver_processed_at TIMESTAMP
) USING DELTA;

-- =============================================================================
-- Gold tables (Delta) — populated in Gold phase
-- =============================================================================
CREATE TABLE IF NOT EXISTS gold.sales_by_product (
    product_id       INT,
    product_name     STRING,
    category         STRING,
    total_orders     BIGINT,
    total_revenue    DECIMAL(18, 2),
    avg_order_value  DECIMAL(18, 2)
) USING DELTA;

CREATE TABLE IF NOT EXISTS gold.revenue_by_customer (
    customer_id            INT,
    customer_name          STRING,
    customer_segment       STRING,
    total_orders           BIGINT,
    total_revenue          DECIMAL(18, 2),
    avg_order_value        DECIMAL(18, 2),
    lifetime_value_actual  DECIMAL(18, 2)
) USING DELTA;

CREATE TABLE IF NOT EXISTS gold.customer_segmentation (
    segment_type   STRING,
    customer_count BIGINT,
    avg_revenue    DECIMAL(18, 2),
    total_revenue  DECIMAL(18, 2)
) USING DELTA;
