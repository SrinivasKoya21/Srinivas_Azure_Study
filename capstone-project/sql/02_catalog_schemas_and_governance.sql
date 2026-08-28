-- 02_catalog_schemas_and_governance.sql

-- Run these in a Databricks SQL editor / notebook %sql cell, in order.

-- Part A: catalog, schemas, and the landing volume

CREATE CATALOG IF NOT EXISTS retail_lakehouse
  COMMENT 'Capstone project: NorthWind Retail lakehouse';

CREATE SCHEMA IF NOT EXISTS retail_lakehouse.bronze
  COMMENT 'Raw, as-landed data — no cleaning applied';

CREATE SCHEMA IF NOT EXISTS retail_lakehouse.silver
  COMMENT 'Cleaned, deduplicated, conformed data with DQ enforcement';

CREATE SCHEMA IF NOT EXISTS retail_lakehouse.gold
  COMMENT 'Business-ready aggregates for reporting and analytics';

-- A managed Unity Catalog Volume to act as the "landing zone" that the
-- order-generator script writes into and Auto Loader reads from.
CREATE VOLUME IF NOT EXISTS retail_lakehouse.bronze.landing
  COMMENT 'Landing zone for raw order-event JSON files';

-- Part B: analyst group privileges (run after creating the `analysts` group --

-- see Part 5.4 / Part 2 of the book for how to create an account-level group)

GRANT USE CATALOG ON CATALOG retail_lakehouse TO `analysts`;
GRANT USE SCHEMA ON SCHEMA retail_lakehouse.silver TO `analysts`;
GRANT USE SCHEMA ON SCHEMA retail_lakehouse.gold TO `analysts`;

GRANT SELECT ON TABLE retail_lakehouse.silver.orders TO `analysts`;
GRANT SELECT ON TABLE retail_lakehouse.silver.customers TO `analysts`;
GRANT SELECT ON TABLE retail_lakehouse.silver.products TO `analysts`;
GRANT SELECT ON SCHEMA retail_lakehouse.gold TO `analysts`;   -- analysts can read all gold tables

-- Analysts should NOT be able to see or touch raw bronze data at all
REVOKE ALL PRIVILEGES ON SCHEMA retail_lakehouse.bronze FROM `analysts`;

-- Part C: column mask on customers.email

CREATE OR REPLACE FUNCTION retail_lakehouse.silver.mask_email(email STRING)
RETURNS STRING
RETURN
  CASE
    WHEN is_account_group_member('analysts') THEN
      concat('***MASKED***@', split(email, '@')[1])
    ELSE
      email
  END;

ALTER TABLE retail_lakehouse.silver.customers
  ALTER COLUMN email SET MASK retail_lakehouse.silver.mask_email;

-- Part D: row filter on customers.region

CREATE OR REPLACE FUNCTION retail_lakehouse.silver.region_row_filter(region STRING)
RETURNS BOOLEAN
RETURN
  is_account_group_member('admins')                              -- admins see everything
  OR is_account_group_member('analysts_apac') AND region = 'APAC' -- APAC analysts see only APAC
  OR NOT is_account_group_member('analysts_apac');                -- everyone else unaffected by this filter

ALTER TABLE retail_lakehouse.silver.customers
  SET ROW FILTER retail_lakehouse.silver.region_row_filter ON (region);
